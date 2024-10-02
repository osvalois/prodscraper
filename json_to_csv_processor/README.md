# Product Attribute Extractor

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Requirements](#requirements)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Usage](#usage)
8. [API Documentation](#api-documentation)
9. [Development](#development)
10. [Testing](#testing)
11. [Continuous Integration](#continuous-integration)
12. [Acknowledgements](#acknowledgements)

## Overview

The Product Attribute Extractor is a high-performance, asynchronous Python application designed to fetch product data from a JSON API, extract specific attributes, and output them to a CSV file. This project demonstrates best practices in Python development, including asynchronous programming, robust error handling, and comprehensive testing.

## Features

- Asynchronous data fetching for improved performance
- Robust error handling and logging
- Configurable via environment variables
- Comprehensive unit testing with high coverage
- Type hinting for improved code quality and IDE support
- Follows PEP 8 style guide and industry best practices
- Modular architecture for easy maintenance and extensibility
- Caching mechanism for optimized performance
- Detailed documentation and inline comments

## Architecture

The application follows a modular, single-responsibility principle design with the following main components:

1. **JSONFetcher**: Handles asynchronous fetching of JSON data from the API.
2. **ProductAttributeExtractor**: Responsible for parsing and extracting relevant product attributes.
3. **CSVWriter**: Manages the output of extracted data to CSV format.
4. **ProductProcessor**: Orchestrates the entire process, coordinating between other components.

For a detailed explanation of architectural decisions and their justifications, please refer to [docs/architecture.md](docs/architecture.md).

## Requirements

- Python 3.8+
- aiohttp
- python-dotenv
- Other dependencies as listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/osvalois/prodscraper.git
   cd product-attribute-extractor
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

The application uses environment variables for configuration. Create a `.env` file in the project root with the following variables:

- `JSON_URL`: URL of the JSON data source
- `OUTPUT_FILE`: Path to the output CSV file

Example `.env` file:
```
JSON_URL=https://api.example.com/products
OUTPUT_FILE=output-product.csv
```

For more advanced configuration options, please refer to [docs/configuration.md](docs/configuration.md).

## Usage

1. Ensure your `.env` file is set up correctly.

2. Run the main script:
   ```
   python main.py
   ```

3. Check the output CSV file (default: `output-product.csv`).

For more detailed usage instructions and examples, please see [docs/usage.md](docs/usage.md).

## API Documentation

For detailed information about each component's API, including method signatures, parameters, return types, and exceptions, please refer to [docs/api.md](docs/api.md).

## Development

### Setting Up the Development Environment

1. Follow the [Installation](#installation) steps.
2. Install additional development dependencies:
   ```
   pip install -r requirements-dev.txt
   ```

### Code Style and Linting

We adhere to the PEP 8 style guide and use the following tools:

- Black for code formatting
- isort for import sorting
- Flake8 for linting
- mypy for static type checking

Run all style checks:

```
black .
isort .
flake8
mypy .
```
## Testing

We use pytest for unit testing. To run the tests:

```
pytest
```

For test coverage information:

```
pytest --cov=.
```

Aim for 90%+ test coverage for new code contributions.

## Continuous Integration

We use GitHub Actions for CI. The configuration can be found in `.github/workflows/ci.yml`. CI runs include:

- Linting and style checks
- Unit tests
- Test coverage reporting

## Acknowledgements

- Thanks to the aiohttp team for their excellent asynchronous HTTP client.
- Appreciation to all contributors who have helped shape this project.

---

For any questions or support, please open an issue on the GitHub repository or contact the maintainers directly.