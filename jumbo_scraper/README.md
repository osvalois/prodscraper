# ProdScraper: High-Performance E-commerce Product Scraper API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=flat&logo=redis&logoColor=white)](https://redis.io/)

## 🚀 Overview

ProdScraper is a API designed for efficient and scalable scraping. Built on the robust FastAPI framework and leveraging Redis for intelligent caching, ProdScraper offers unparalleled speed and reliability in data extraction while adhering to ethical scraping practices.

## ✨ Key Features

- **🚄 Lightning-Fast Scraping**: Harnesses the power of Playwright for robust and speedy web scraping.
- **📦 Intelligent Caching**: Utilizes Redis to optimize performance and minimize redundant scraping operations.
- **🛡️ Ethical Scraping**: Implements rate limiting to respect website policies and prevent overloading of target servers.
- **🔐 Secure Access**: Employs API key authentication to ensure controlled and secure access to scraping capabilities.
- **📊 Advanced Monitoring**: Integrates Prometheus metrics for real-time performance tracking and analytics.
- **🐳 Containerized Deployment**: Supports seamless deployment via Docker and Docker Compose for consistent environments.
- **🔄 Asynchronous Architecture**: Built on FastAPI to handle high concurrency and ensure optimal performance.

## 🛠️ Technology Stack

- **FastAPI**: For building high-performance APIs with Python 3.9+
- **Playwright**: For reliable web scraping and browser automation
- **Redis**: For efficient caching and data storage
- **Prometheus**: For comprehensive system monitoring and metrics
- **Docker & Docker Compose**: For containerized deployment and scaling
- **Pydantic**: For data validation and settings management
- **Starlette**: For additional web server features and middleware support

## 📋 Prerequisites

- Python 3.9+
- Redis server
- Docker and Docker Compose (for containerized deployment)

## 🚀 Quick Start

1. **Clone the Repository**

   ```bash
   git clone https://github.com/osvalois/prodscraper.git
   cd prodscraper
   ```

2. **Set Up Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   ```bash
   cp .env.example .env
   # Edit .env with your specific configurations
   ```

5. **Launch the Application**

   ```bash
   uvicorn src.main:app --reload
   ```

   The API will be accessible at `http://localhost:8000`. Swagger documentation is available at `/docs`.

## 🐳 Docker Deployment

1. **Build and Launch Containers**

   ```bash
   docker-compose up --build
   ```

2. Access the API at `http://localhost:8000`

## 🔗 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/scrape` | POST | Scrape a single URL |
| `/scrape_multiple` | POST | Scrape multiple URLs concurrently |
| `/metrics` | GET | Access Prometheus metrics |

For detailed API documentation, refer to the Swagger UI at `/docs` when the server is running.

## ⚙️ Configuration

Key configuration options in `.env`:

| Variable | Description |
|----------|-------------|
| `REDIS_HOST` | Redis server hostname |
| `REDIS_PORT` | Redis server port |
| `API_KEY` | Secret key for API authentication |
| `SCRAPE_TIMEOUT` | Timeout for scraping operations (ms) |
| `RATE_LIMIT_CALLS` | Number of allowed API calls per period |
| `RATE_LIMIT_PERIOD` | Time period for rate limiting (seconds) |

## 📊 Monitoring & Metrics

Prometheus metrics are available at the `/metrics` endpoint. Key metrics include:

- `scrape_requests_total`: Total number of scrape requests
- `successful_scrapes_total`: Total number of successful scrapes
- `scrape_errors_total`: Total number of scrape errors
- `scrape_duration_seconds`: Duration of scrape requests

## 🧪 Testing

Execute the test suite:

```bash
pytest
```

## 🤝 Contributing

We welcome contributions to ProdScraper! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details on how to get started.

## 📄 License

ProdScraper is open-sourced under the [MIT License](LICENSE).

## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) for the fantastic API framework
- [Playwright](https://playwright.dev/) for powerful browser automation
- [Redis](https://redis.io/) for high-performance caching
- All our contributors and supporters

---

Developed with ❤️ by [Osvalois](https://github.com/osvalois)