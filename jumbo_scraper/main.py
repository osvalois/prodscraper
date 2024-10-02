from fastapi import FastAPI, HTTPException, Depends, Security, Request
from fastapi.security.api_key import APIKeyHeader, APIKey
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from prometheus_client import start_http_server
from prometheus_metrics import REGISTRY
from typing import List
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from models import ScrapeRequest, MultiScrapeRequest, ScrapeResponse, MultiScrapeResponse
from config import settings
from scraper import scrape_products

app = FastAPI(
    title="Product Scraper API",
    description="An API for scraping product information from websites",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# MongoDB Atlas client
mongo_client = None
db = None

# API Key Config
API_KEY = settings.API_KEY
API_KEY_NAME = "X-API-Key"
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
    global mongo_client, db
    mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = mongo_client[settings.mongodb_database]
    start_http_server(8000)

@app.on_event("shutdown")
async def shutdown_event():
    if mongo_client:
        await mongo_client.close()

@app.post("/scrape", response_model=ScrapeResponse, tags=["scraping"])
async def scrape(request: ScrapeRequest, api_key: APIKey = Depends(get_api_key)):
    try:
        result = await scrape_products(str(request.url))
        REGISTRY['scrape_requests_total'].inc()
        REGISTRY['successful_scrapes_total'].inc()
        
        # Store the result in MongoDB
        await db.results.insert_one({
            "url": result["url"],
            "products": result["products"],
            "timestamp": time.time()
        })
        
        return result
    except Exception as e:
        REGISTRY['scrape_errors_total'].inc()
        raise HTTPException(status_code=500, detail=f"Error during scraping: {str(e)}")

@app.post("/scrape_multiple", response_model=MultiScrapeResponse, tags=["scraping"])
async def scrape_multiple(request: MultiScrapeRequest, api_key: APIKey = Depends(get_api_key)):
    try:
        results = []
        for url in request.urls:
            result = await scrape_products(str(url))
            results.append(result)
            REGISTRY['scrape_requests_total'].inc()
            REGISTRY['successful_scrapes_total'].inc()
            
            # Store each result in MongoDB
            await db.results.insert_one({
                "url": result["url"],
                "products": result["products"],
                "timestamp": time.time()
            })
        
        return MultiScrapeResponse(results=results)
    except Exception as e:
        REGISTRY['scrape_errors_total'].inc()
        raise HTTPException(status_code=500, detail=f"Error during multiple scraping: {str(e)}")

@app.get("/health", tags=["health"])
async def health_check():
    try:
        await db.command('ping')
        return {"status": "healthy", "mongodb": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/metrics")
async def metrics():
    from prometheus_client import generate_latest
    return Response(generate_latest(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)