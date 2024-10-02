from prometheus_client import Counter, Histogram

# Define Prometheus metrics
REGISTRY = {
    'scrape_requests_total': Counter('scrape_requests_total', 'Total number of scrape requests'),
    'successful_scrapes_total': Counter('successful_scrapes_total', 'Total number of successful scrapes'),
    'scrape_errors_total': Counter('scrape_errors_total', 'Total number of scrape errors'),
    'scrape_duration_seconds': Histogram('scrape_duration_seconds', 'Duration of scrape requests', buckets=[0.1, 0.5, 1, 2, 5, 10, 30, 60, 120])
}