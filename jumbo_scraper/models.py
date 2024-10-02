from pydantic import BaseModel, HttpUrl
from typing import List

class ScrapeRequest(BaseModel):
    url: HttpUrl

class MultiScrapeRequest(BaseModel):
    urls: List[HttpUrl]

class ProductInfo(BaseModel):
    name: str
    price: str
    promo_price: str

class ScrapeResponse(BaseModel):
    url: HttpUrl
    products: List[ProductInfo]

class MultiScrapeResponse(BaseModel):
    results: List[ScrapeResponse]