import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_products(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()

    soup = BeautifulSoup(content, 'html.parser')
    product_elements = soup.select('.vtex-product-summary-2-x-element')

    products = []
    for elem in product_elements:
        name_elem = elem.select_one('.vtex-product-summary-2-x-productNameContainer')
        name = name_elem.text.strip() if name_elem else "N/A"

        price_elem = elem.select_one('.tiendasjumboqaio-jumbo-minicart-2-x-price')
        price = price_elem.text.strip() if price_elem else "N/A"

        promo_price_elem = elem.select_one('.tiendasjumboqaio-jumbo-minicart-2-x-priceWithDiscounts')
        promo_price = promo_price_elem.text.strip() if promo_price_elem else price

        products.append({
            "name": name,
            "price": price,
            "promo_price": promo_price
        })

    return {
        "url": url,
        "products": products
    }