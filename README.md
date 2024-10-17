## Overview

The `prodscraper` repository contains two main projects:

1. `json_to_csv_processor`: A tool for processing JSON data and converting it to CSV format.
2. `jumbo_scraper`: An API-based scraper, likely for fetching product data from Jumbo (possibly a supermarket chain).

## Project Structure

```
prodscraper/
├── .github/
├── json_to_csv_processor/
│   ├── docs/
│   ├── tests/
│   ├── .flake8
│   ├── Makefile
│   ├── README.md
│   ├── main.py
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── setup.cfg
├── jumbo_scraper/
│   ├── src/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   ├── .dockerignore
│   ├── .env.example
│   ├── Dockerfile
│   ├── LICENSE
│   ├── Makefile
│   ├── README.md
│   ├── config.py
│   ├── dump.rdb
│   ├── fly.toml
│   ├── main.py
│   ├── pyproject.toml
│   └── requirements.txt
└── .gitignore
```

## json_to_csv_processor

This project focuses on processing JSON data and converting it to CSV format. It includes:

- Documentation (`docs/`)
- Unit tests (`tests/`)
- Configuration files for linting and formatting (`.flake8`, `pyproject.toml`, `setup.cfg`)
- Main execution script (`main.py`)
- Project dependencies (`requirements.txt`)
- Build automation (`Makefile`)

Key features:
- Asynchronous data fetching
- Error handling and logging
- Configurable via environment variables
- Comprehensive unit testing
- Type hinting
- Modular architecture

## jumbo_scraper

This project appears to be an API-based scraper, likely for fetching product data from Jumbo. It has a more complex structure:

- Source code (`src/`)
  - API endpoints (`api/`)
  - Core functionality (`core/`)
  - Data models (`models/`)
  - Services (`services/`)
  - Utility functions (`utils/`)
- Unit tests (`tests/`)
- Docker configuration (`.dockerignore`, `Dockerfile`)
- Environment configuration (`.env.example`)
- Deployment configuration (`fly.toml`)
- License information (`LICENSE`)
- Build automation (`Makefile`)
- Main execution script (`main.py`)
- Project configuration (`config.py`, `pyproject.toml`)
- Dependencies (`requirements.txt`)

Key features:
- API-based architecture
- Docker containerization
- Deployment ready (possibly using Fly.io)
- Redis integration (implied by `dump.rdb`)
- Modular structure with separation of concerns
