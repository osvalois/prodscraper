"""
Product Attribute Extractor

This script fetches product data from a JSON API, extracts specific attributes,
and writes them to a CSV file.

Usage:
    python main.py

Environment Variables:
    JSON_URL: URL of the JSON data source
    OUTPUT_FILE: Path to the output CSV file
"""

import asyncio
import csv
import json
from pathlib import Path
from typing import Dict, Any, List
from decimal import Decimal
import logging
from dataclasses import dataclass, asdict, field
from functools import lru_cache

import aiohttp
from aiohttp import ClientSession
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class ProductAttributes:
    """Represents the attributes of a product."""
    allergens: List[str] = field(default_factory=list)
    sku: str = ""
    vegan: bool = False
    kosher: bool = False
    organic: bool = False
    vegetarian: bool = False
    gluten_free: bool = False
    lactose_free: bool = False
    package_quantity: Decimal = Decimal('0')
    unit_size: Decimal = Decimal('0')
    net_weight: Decimal = Decimal('0')

class JSONFetcher:
    """Handles fetching JSON data from a URL."""

    @staticmethod
    async def fetch(url: str, session: ClientSession) -> Dict[str, Any]:
        """
        Fetches JSON data from the specified URL.

        Args:
            url (str): The URL to fetch data from.
            session (ClientSession): The aiohttp ClientSession to use for the request.

        Returns:
            Dict[str, Any]: The parsed JSON data.

        Raises:
            aiohttp.ClientError: If there's an error fetching the data.
        """
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"Error fetching JSON data: {e}")
            raise

class ProductAttributeExtractor:
    """Extracts and parses product attributes from JSON data."""

    @staticmethod
    @lru_cache(maxsize=None)
    def extract(data: str) -> Dict[str, Any]:
        """
        Extracts custom attributes from the JSON data.

        Args:
            data (str): JSON string containing product data.

        Returns:
            Dict[str, Any]: Extracted custom attributes.

        Raises:
            ValueError: If custom attributes are not found or are invalid.
        """
        try:
            parsed_data = json.loads(data)
            all_variants = parsed_data['allVariants']
            attributes_raw = next(attr for attr in all_variants[0]['attributesRaw'] if attr['name'] == 'custom_attributes')
            return json.loads(attributes_raw['value']['es-CR'])
        except (KeyError, StopIteration, json.JSONDecodeError) as e:
            logger.error(f"Error extracting custom attributes: {e}")
            raise ValueError("Custom attributes not found or invalid in JSON data")

    @staticmethod
    def parse(custom_attributes: Dict[str, Any]) -> ProductAttributes:
        """
        Parses custom attributes into a ProductAttributes object.

        Args:
            custom_attributes (Dict[str, Any]): Custom attributes to parse.

        Returns:
            ProductAttributes: Parsed product attributes.

        Raises:
            KeyError: If a required attribute is missing.
            ValueError: If an attribute has an invalid value.
        """
        try:
            return ProductAttributes(
                allergens=[allergen['name'] for allergen in custom_attributes['allergens']['value']],
                sku=custom_attributes['sku']['value'],
                vegan=custom_attributes['vegan']['value'],
                kosher=custom_attributes['kosher']['value'],
                organic=custom_attributes['organic']['value'],
                vegetarian=custom_attributes['vegetarian']['value'],
                gluten_free=custom_attributes['gluten_free']['value'],
                lactose_free=custom_attributes['lactose_free']['value'],
                package_quantity=Decimal(str(custom_attributes['package_quantity']['value'])),
                unit_size=Decimal(custom_attributes['unit_size']['value']),
                net_weight=Decimal(custom_attributes['net_weight']['value'])
            )
        except KeyError as e:
            logger.error(f"Missing attribute in custom attributes: {e}")
            raise
        except ValueError as e:
            logger.error(f"Invalid value in custom attributes: {e}")
            raise

class CSVWriter:
    """Handles writing product attributes to a CSV file."""

    @staticmethod
    async def write(attributes: ProductAttributes, output_file: Path):
        """
        Writes product attributes to a CSV file.

        Args:
            attributes (ProductAttributes): The product attributes to write.
            output_file (Path): The path to the output CSV file.

        Raises:
            IOError: If there's an error writing to the file.
        """
        try:
            with output_file.open('w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=asdict(attributes).keys())
                writer.writeheader()
                writer.writerow(asdict(attributes))
            logger.info(f"CSV file '{output_file}' has been created successfully.")
        except IOError as e:
            logger.error(f"Error writing to CSV file: {e}")
            raise

class ProductProcessor:
    """Coordinates the process of fetching, extracting, and writing product data."""

    def __init__(self, json_url: str, output_file: Path):
        self.json_url = json_url
        self.output_file = output_file

    async def process(self):
        """
        Processes the product data: fetches JSON, extracts attributes, and writes to CSV.

        Raises:
            Exception: If any error occurs during processing.
        """
        try:
            async with aiohttp.ClientSession() as session:
                json_data = await JSONFetcher.fetch(self.json_url, session)
                custom_attributes = ProductAttributeExtractor.extract(json.dumps(json_data))
                product_attributes = ProductAttributeExtractor.parse(custom_attributes)
                await CSVWriter.write(product_attributes, self.output_file)
        except Exception as e:
            logger.error(f"An error occurred during processing: {e}")
            raise

async def main():
    """Main function to run the product attribute extraction process."""
    json_url = os.getenv('JSON_URL', 'https://storage.googleapis.com/resources-prod-shelftia/scrapers-prueba/product.json')
    output_file = Path(os.getenv('OUTPUT_FILE', 'output-product.csv'))

    processor = ProductProcessor(json_url, output_file)
    
    try:
        await processor.process()
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())