# Configuration Guide

The Product Attribute Extractor uses environment variables for configuration. This guide explains how to set up and manage these configurations.

## Environment Variables

### Required Variables

1. `JSON_URL`: The URL of the JSON data source.
   - Example: `https://api.example.com/products`

2. `OUTPUT_FILE`: The path where the output CSV file will be saved.
   - Example: `output-product.csv`

### Optional Variables

1. `LOG_LEVEL`: The logging level for the application.
   - Default: `INFO`
   - Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

2. `CACHE_SIZE`: The maximum size of the LRU cache for attribute extraction.
   - Default: `128`
   - Set to `0` to disable caching

## Setting Up Environment Variables

1. Create a `.env` file in the root directory of the project.
2. Add your configurations to the file:
- JSON_URL=https://api.example.com/products
- OUTPUT_FILE=output-product.csv
- LOG_LEVEL=INFO
- CACHE_SIZE=256
3. The application will automatically load these variables when it runs.

## Configuration Best Practices

1. Never commit the `.env` file to version control. It's already added to `.gitignore`.
2. Use different `.env` files for different environments (development, staging, production).
3. For production deployments, set environment variables through your deployment platform or container orchestration tool.