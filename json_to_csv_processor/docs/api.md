# API Documentation

## JSONFetcher

### `fetch(url: str, session: ClientSession) -> Dict[str, Any]`

Asynchronously fetches JSON data from a given URL.

#### Parameters:
- `url` (str): The URL to fetch data from.
- `session` (ClientSession): An aiohttp ClientSession object.

#### Returns:
- `Dict[str, Any]`: The parsed JSON data.

#### Raises:
- `aiohttp.ClientError`: If there's an error fetching the data.

## ProductAttributeExtractor

### `extract(data: str) -> Dict[str, Any]`

Extracts custom attributes from the JSON data.

#### Parameters:
- `data` (str): JSON string containing product data.

#### Returns:
- `Dict[str, Any]`: Extracted custom attributes.

#### Raises:
- `ValueError`: If custom attributes are not found or are invalid.

### `parse(custom_attributes: Dict[str, Any]) -> ProductAttributes`

Parses custom attributes into a ProductAttributes object.

#### Parameters:
- `custom_attributes` (Dict[str, Any]): Custom attributes to parse.

#### Returns:
- `ProductAttributes`: Parsed product attributes.

#### Raises:
- `KeyError`: If a required attribute is missing.
- `ValueError`: If an attribute has an invalid value.

## CSVWriter

### `write(attributes: ProductAttributes, output_file: Path)`

Writes product attributes to a CSV file.

#### Parameters:
- `attributes` (ProductAttributes): The product attributes to write.
- `output_file` (Path): The path to the output CSV file.

#### Raises:
- `IOError`: If there's an error writing to the file.

## ProductProcessor

### `process()`

Processes the product data: fetches JSON, extracts attributes, and writes to CSV.

#### Raises:
- `Exception`: If any error occurs during processing.

These API definitions provide a clear interface for each component of the system, facilitating usage and integration within the application or for potential external use.