from pydantic import BaseModel, HttpUrl, validator
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

class Product(BaseModel):
    name: str
    price: str
    promo_price: str

    @validator('name', 'price', 'promo_price')
    def check_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v