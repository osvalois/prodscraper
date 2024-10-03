from fastapi import FastAPI
from .api import endpoints
from .core.config import settings
from .services.prometheus_metrics import PrometheusMiddleware, metrics
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Product Scraper API",
    description="An optimized API for scraping product information from websites with Redis caching",
    version="1.2.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)

app.include_router(endpoints.router)

app.add_route("/metrics", metrics)

@app.on_event("startup")
async def startup_event():
    # Initializing the Redis client
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Close any closing connections
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)