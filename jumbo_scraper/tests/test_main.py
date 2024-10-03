import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from main import app, get_api_key
from models import ScrapeRequest, MultiScrapeRequest

client = TestClient(app)

@pytest.fixture
def mock_api_key():
    return "test_api_key"

@pytest.fixture
def mock_settings(mock_api_key):
    with patch("main.settings") as mock_settings:
        mock_settings.API_KEY = mock_api_key
        yield mock_settings

@pytest.fixture
def mock_mongo_client():
    with patch("main.mongo_client") as mock_client:
        yield mock_client

@pytest.fixture
def mock_redis_client():
    with patch("main.redis_client") as mock_client:
        yield mock_client

@pytest.fixture
def mock_scrape_products():
    with patch("main.scrape_products") as mock_scrape:
        yield mock_scrape

def test_get_api_key_valid(mock_settings):
    assert get_api_key(mock_settings.API_KEY) == mock_settings.API_KEY

def test_get_api_key_invalid(mock_settings):
    with pytest.raises(Exception):
        get_api_key("invalid_key")

@pytest.mark.asyncio
async def test_scrape_endpoint_success(mock_api_key, mock_scrape_products, mock_mongo_client, mock_redis_client):
    mock_scrape_products.return_value = {
        "url": "https://example.com",
        "products": [{"name": "Test Product", "price": "10.00", "promo_price": "9.00"}]
    }
    mock_redis_client.get.return_value = None

    response = client.post(
        "/scrape",
        json={"url": "https://example.com"},
        headers={"X-API-Key": mock_api_key}
    )

    assert response.status_code == 200
    assert "url" in response.json()
    assert "products" in response.json()

@pytest.mark.asyncio
async def test_scrape_endpoint_cached(mock_api_key, mock_redis_client):
    cached_result = {
        "url": "https://example.com",
        "products": [{"name": "Cached Product", "price": "15.00", "promo_price": "14.00"}]
    }
    mock_redis_client.get.return_value = json.dumps(cached_result)

    response = client.post(
        "/scrape",
        json={"url": "https://example.com"},
        headers={"X-API-Key": mock_api_key}
    )

    assert response.status_code == 200
    assert response.json() == cached_result

@pytest.mark.asyncio
async def test_scrape_endpoint_error(mock_api_key, mock_scrape_products, mock_redis_client):
    mock_scrape_products.side_effect = Exception("Scraping error")
    mock_redis_client.get.return_value = None

    response = client.post(
        "/scrape",
        json={"url": "https://example.com"},
        headers={"X-API-Key": mock_api_key}
    )

    assert response.status_code == 500
    assert "Error during scraping" in response.json()["detail"]

@pytest.mark.asyncio
async def test_scrape_multiple_endpoint_success(mock_api_key, mock_scrape_products, mock_mongo_client, mock_redis_client):
    mock_scrape_products.return_value = {
        "url": "https://example.com",
        "products": [{"name": "Test Product", "price": "10.00", "promo_price": "9.00"}]
    }
    mock_redis_client.get.return_value = None

    response = client.post(
        "/scrape_multiple",
        json={"urls": ["https://example.com", "https://example2.com"]},
        headers={"X-API-Key": mock_api_key}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_scrape_multiple_endpoint_partially_cached(mock_api_key, mock_scrape_products, mock_redis_client):
    cached_result = {
        "url": "https://example.com",
        "products": [{"name": "Cached Product", "price": "15.00", "promo_price": "14.00"}]
    }
    mock_redis_client.get.side_effect = [json.dumps(cached_result), None]
    mock_scrape_products.return_value = {
        "url": "https://example2.com",
        "products": [{"name": "Test Product", "price": "10.00", "promo_price": "9.00"}]
    }

    response = client.post(
        "/scrape_multiple",
        json={"urls": ["https://example.com", "https://example2.com"]},
        headers={"X-API-Key": mock_api_key}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
    assert response.json()[0] == cached_result

@pytest.mark.asyncio
async def test_health_check_success(mock_mongo_client, mock_redis_client):
    mock_mongo_client.command.return_value = True
    mock_redis_client.ping.return_value = True

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "mongodb": "connected", "redis": "connected"}

@pytest.mark.asyncio
async def test_health_check_failure(mock_mongo_client, mock_redis_client):
    mock_mongo_client.command.side_effect = Exception("MongoDB connection error")

    response = client.get("/health")

    assert response.status_code == 500
    assert "Health check failed" in response.json()["detail"]

def test_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"