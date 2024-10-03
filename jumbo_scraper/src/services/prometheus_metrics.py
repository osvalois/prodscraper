from prometheus_client import Counter, Histogram, generate_latest, CollectorRegistry
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

# Create a custom registry
REGISTRY = CollectorRegistry()

# Define Prometheus metrics
SCRAPE_REQUESTS_TOTAL = Counter('scrape_requests_total', 'Total number of scrape requests', registry=REGISTRY)
SUCCESSFUL_SCRAPES_TOTAL = Counter('successful_scrapes_total', 'Total number of successful scrapes', registry=REGISTRY)
SCRAPE_ERRORS_TOTAL = Counter('scrape_errors_total', 'Total number of scrape errors', registry=REGISTRY)
SCRAPE_DURATION_SECONDS = Histogram('scrape_duration_seconds', 'Duration of scrape requests', buckets=[0.1, 0.5, 1, 2, 5, 10, 30, 60, 120], registry=REGISTRY)

def initialize_metrics():
    # This function is now empty as we're initializing metrics at module level
    pass

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        SCRAPE_DURATION_SECONDS.observe(process_time)
        return response

async def metrics(request: Request) -> Response:
    return Response(generate_latest(REGISTRY), media_type="text/plain")