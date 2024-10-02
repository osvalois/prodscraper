import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from decimal import Decimal

from product_scraper import ProductProcessor, ProductAttributes, JSONFetcher, ProductAttributeExtractor, CSVWriter

@pytest.fixture
def sample_json_data():
    return {
        "allVariants": [{
            "attributesRaw": [{
                "name": "custom_attributes",
                "value": {
                    "es-CR": json.dumps({
                        "allergens": {"value": [{"name": "Milk"}]},
                        "sku": {"value": "12345"},
                        "vegan": {"value": False},
                        "kosher": {"value": True},
                        "organic": {"value": False},
                        "vegetarian": {"value": True},
                        "gluten_free": {"value": True},
                        "lactose_free": {"value": False},
                        "package_quantity": {"value": 1},
                        "unit_size": {"value": "500"},
                        "net_weight": {"value": "500"}
                    })
                }
            }]
        }]
    }

@pytest.mark.asyncio
async def test_product_processor(sample_json_data):
    with patch.object(JSONFetcher, 'fetch', return_value=sample_json_data), \
         patch.object(CSVWriter, 'write') as mock_write:
        
        processor = ProductProcessor("http://api.example.com", Path("output.csv"))
        await processor.process()

        expected_attributes = ProductAttributes(
            allergens=["Milk"],
            sku="12345",
            vegan=False,
            kosher=True,
            organic=False,
            vegetarian=True,
            gluten_free=True,
            lactose_free=False,
            package_quantity=Decimal('1'),
            unit_size=Decimal('500'),
            net_weight=Decimal('500')
        )

        mock_write.assert_called_once_with(expected_attributes, Path("output.csv"))