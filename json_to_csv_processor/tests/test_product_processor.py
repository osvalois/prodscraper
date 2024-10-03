import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
from decimal import Decimal
import aiohttp

from main import ProductProcessor, ProductAttributes, JSONFetcher, ProductAttributeExtractor, CSVWriter

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

        mock_write.assert_called_once()
        actual_attributes, actual_path = mock_write.call_args[0]
        assert actual_attributes == expected_attributes
        assert actual_path == Path("output.csv")

def test_product_attribute_extractor():
    sample_data = {
        "allVariants": [{
            "attributesRaw": [{
                "name": "custom_attributes",
                "value": {
                    "es-CR": json.dumps({
                        "allergens": {"value": [{"name": "Nuts"}]},
                        "sku": {"value": "54321"},
                        "vegan": {"value": True},
                        "kosher": {"value": False},
                        "organic": {"value": True},
                        "vegetarian": {"value": True},
                        "gluten_free": {"value": False},
                        "lactose_free": {"value": True},
                        "package_quantity": {"value": 2},
                        "unit_size": {"value": "250"},
                        "net_weight": {"value": "500"}
                    })
                }
            }]
        }]
    }
    
    custom_attributes = ProductAttributeExtractor.extract(json.dumps(sample_data))
    product_attributes = ProductAttributeExtractor.parse(custom_attributes)
    
    assert product_attributes.allergens == ["Nuts"]
    assert product_attributes.sku == "54321"
    assert product_attributes.vegan == True
    assert product_attributes.kosher == False
    assert product_attributes.organic == True
    assert product_attributes.vegetarian == True
    assert product_attributes.gluten_free == False
    assert product_attributes.lactose_free == True
    assert product_attributes.package_quantity == Decimal('2')
    assert product_attributes.unit_size == Decimal('250')
    assert product_attributes.net_weight == Decimal('500')

@pytest.mark.asyncio
async def test_csv_writer(tmp_path):
    attributes = ProductAttributes(
        allergens=["Soy"],
        sku="67890",
        vegan=True,
        kosher=True,
        organic=True,
        vegetarian=True,
        gluten_free=True,
        lactose_free=True,
        package_quantity=Decimal('3'),
        unit_size=Decimal('100'),
        net_weight=Decimal('300')
    )
    
    output_file = tmp_path / "test_output.csv"
    await CSVWriter.write(attributes, output_file)
    
    assert output_file.exists()
    with output_file.open('r') as f:
        content = f.read()
        assert "Soy" in content
        assert "67890" in content
        assert "True" in content
        assert "3" in content
        assert "100" in content
        assert "300" in content

def test_product_attribute_extractor_error():
    invalid_data = {"invalid": "data"}
    
    with pytest.raises(ValueError):
        ProductAttributeExtractor.extract(json.dumps(invalid_data))

@pytest.mark.asyncio
async def test_csv_writer_error(tmp_path):
    attributes = ProductAttributes()
    invalid_path = tmp_path / "non_existent_directory" / "test_output.csv"
    
    with pytest.raises(OSError):
        await CSVWriter.write(attributes, invalid_path)