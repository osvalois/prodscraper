import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import logging
from typing import Dict, Any
import aiohttp
from models import Product
import time
from urllib.parse import urlparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, calls: int, period: float):
        self.calls = calls
        self.period = period
        self.timestamps = []

    async def wait(self):
        now = time.time()
        self.timestamps = [t for t in self.timestamps if now - t < self.period]
        if len(self.timestamps) >= self.calls:
            sleep_time = self.period - (now - self.timestamps[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        self.timestamps.append(time.time())

rate_limiter = RateLimiter(calls=1, period=1)  # 1 request per second

async def is_valid_url(url: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url, allow_redirects=True) as response:
                return response.status < 400
    except aiohttp.ClientError:
        return False

async def scrape_products(url: str, timeout: int = 30000) -> Dict[str, Any]:
    if not await is_valid_url(url):
        logger.error(f"Invalid URL: {url}")
        return {"url": url, "products": [], "error": "Invalid URL"}

    await rate_limiter.wait()

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = await context.new_page()
            
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=timeout)
                content = await page.content()
            except PlaywrightTimeoutError:
                logger.error(f"Timeout occurred while loading {url}")
                return {"url": url, "products": [], "error": "Timeout"}
            finally:
                await browser.close()

        soup = BeautifulSoup(content, 'html.parser')
        product_elements = soup.select('.vtex-product-summary-2-x-element')

        products = []
        for elem in product_elements:
            try:
                name_elem = elem.select_one('.vtex-product-summary-2-x-productNameContainer')
                price_elem = elem.select_one('.tiendasjumboqaio-jumbo-minicart-2-x-price')
                promo_price_elem = elem.select_one('.tiendasjumboqaio-jumbo-minicart-2-x-priceWithDiscounts')

                name = name_elem.text.strip() if name_elem else "N/A"
                price = price_elem.text.strip() if price_elem else "N/A"
                promo_price = promo_price_elem.text.strip() if promo_price_elem else price

                product = Product(name=name, price=price, promo_price=promo_price)
                products.append(product.dict())
            except ValueError as ve:
                logger.warning(f"Skipping invalid product: {str(ve)}")
            except Exception as e:
                logger.error(f"Error processing product: {str(e)}")

        logger.info(f"Successfully scraped {len(products)} products from {url}")
        return {"url": url, "products": products}

    except Exception as e:
        logger.error(f"Error occurred while scraping {url}: {str(e)}")
        return {"url": url, "products": [], "error": str(e)}