from fastapi import FastAPI, HTTPException, Depends, Security, Request
from fastapi.security.api_key import APIKeyHeader, APIKey
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from prometheus_client import start_http_server
from prometheus_metrics import REGISTRY
from typing import List, Dict, Any
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import json
from redis import asyncio as aioredis
from models import ScrapeRequest, MultiScrapeRequest, ScrapeResponse, MultiScrapeResponse
from config import settings
from scraper import scrape_products, RateLimiter

app = FastAPI(
    title="Product Scraper API",
    description="An optimized API for scraping product information from websites with Redis caching",
    version="1.2.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# MongoDB Atlas client
mongo_client = None
db = None

# Redis client
redis_client = None

# Rate limiter
rate_limiter = RateLimiter(calls=settings.RATE_LIMIT_CALLS, period=settings.RATE_LIMIT_PERIOD)

# API Key Config
API_KEY = settings.API_KEY
API_KEY_NAME = settings.API_KEY_NAME
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        REGISTRY['scrape_duration_seconds'].observe(process_time)
        return response

app.add_middleware(PrometheusMiddleware)

@app.on_event("startup")
async def startup_event():
    global mongo_client, db, redis_client
    mongo_client = AsyncIOMotorClient(
        settings.MONGODB_URL,
        maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
        minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
        maxIdleTimeMS=settings.MONGODB_MAX_IDLE_TIME_MS
    )
    db = mongo_client[settings.mongodb_database]
    
    redis_client = aioredis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
        max_connections=settings.REDIS_MAX_CONNECTIONS,
        socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
        retry_on_timeout=settings.REDIS_RETRY_ON_TIMEOUT
    )
    
    start_http_server(8000)

@app.on_event("shutdown")
async def shutdown_event():
    if mongo_client:
        await mongo_client.close()
    if redis_client:
        await redis_client.close()

async def get_cached_result(url: str) -> Dict[str, Any]:
    cached_result = await redis_client.get(url)
    if cached_result:
        return json.loads(cached_result)
    return None

async def set_cached_result(url: str, result: Dict[str, Any]):
    await redis_client.setex(url, settings.REDIS_CACHE_EXPIRATION, json.dumps(result))

@app.post("/scrape", response_model=Dict[str, Any], tags=["scraping"])
async def scrape(request: ScrapeRequest, api_key: APIKey = Depends(get_api_key)):
    try:
        url = str(request.url)
        cached_result = await get_cached_result(url)
        
        if cached_result:
            REGISTRY['scrape_requests_total'].inc()
            return cached_result
        
        await rate_limiter.wait()
        result = await scrape_products(url, timeout=settings.SCRAPE_TIMEOUT)
        REGISTRY['scrape_requests_total'].inc()
        
        if 'error' not in result:
            REGISTRY['successful_scrapes_total'].inc()
            
            # Store the result in MongoDB
            await db.results.insert_one({
                "url": result["url"],
                "products": result["products"],
                "timestamp": time.time()
            })
            
            # Cache the result
            await set_cached_result(url, result)
        else:
            REGISTRY['scrape_errors_total'].inc()
        
        return result
    except Exception as e:
        REGISTRY['scrape_errors_total'].inc()
        raise HTTPException(status_code=500, detail=f"Error during scraping: {str(e)}")

@app.post("/scrape_multiple", response_model=List[Dict[str, Any]], tags=["scraping"])
async def scrape_multiple(request: MultiScrapeRequest, api_key: APIKey = Depends(get_api_key)):
    try:
        results = []
        tasks = []
        
        for url in request.urls:
            cached_result = await get_cached_result(str(url))
            if cached_result:
                results.append(cached_result)
                REGISTRY['scrape_requests_total'].inc()
            else:
                tasks.append(scrape_products(str(url), timeout=settings.SCRAPE_TIMEOUT))
        
        if tasks:
            await rate_limiter.wait()
            scraped_results = await asyncio.gather(*tasks)
            for result in scraped_results:
                results.append(result)
                REGISTRY['scrape_requests_total'].inc()
                
                if 'error' not in result:
                    REGISTRY['successful_scrapes_total'].inc()
                    
                    # Store each result in MongoDB
                    await db.results.insert_one({
                        "url": result["url"],
                        "products": result["products"],
                        "timestamp": time.time()
                    })
                    
                    # Cache the result
                    await set_cached_result(result["url"], result)
                else:
                    REGISTRY['scrape_errors_total'].inc()
        
        return results
    except Exception as e:
        REGISTRY['scrape_errors_total'].inc()
        raise HTTPException(status_code=500, detail=f"Error during multiple scraping: {str(e)}")

@app.get("/health", tags=["health"])
async def health_check():
    try:
        await db.command('ping')
        await redis_client.ping()
        return {"status": "healthy", "mongodb": "connected", "redis": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/metrics")
async def metrics():
    from prometheus_client import generate_latest
    return Response(generate_latest(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)