from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from ..core.security import get_api_key
from ..models.product import ScrapeRequest, MultiScrapeRequest
from ..services.scraper import scrape_products
from ..utils.redis_helper import get_cached_result, set_cached_result
from ..core.config import settings
from ..services.prometheus_metrics import SCRAPE_REQUESTS_TOTAL, SUCCESSFUL_SCRAPES_TOTAL, SCRAPE_ERRORS_TOTAL

router = APIRouter()

@router.post("/scrape", response_model=Dict[str, Any], tags=["scraping"])
async def scrape(request: ScrapeRequest, api_key: str = Depends(get_api_key)):
    try:
        url = str(request.url)
        SCRAPE_REQUESTS_TOTAL.inc()
        
        cached_result = await get_cached_result(url)
        if cached_result:
            return cached_result
        
        result = await scrape_products(url, timeout=settings.SCRAPE_TIMEOUT)
        
        if 'error' not in result:
            SUCCESSFUL_SCRAPES_TOTAL.inc()
            await set_cached_result(url, result)
        else:
            SCRAPE_ERRORS_TOTAL.inc()
        
        return result
    except Exception as e:
        SCRAPE_ERRORS_TOTAL.inc()
        raise HTTPException(status_code=500, detail=f"Error during scraping: {str(e)}")

@router.post("/scrape_multiple", response_model=List[Dict[str, Any]], tags=["scraping"])
async def scrape_multiple(request: MultiScrapeRequest, api_key: str = Depends(get_api_key)):
    try:
        results = []
        for url in request.urls:
            SCRAPE_REQUESTS_TOTAL.inc()
            cached_result = await get_cached_result(str(url))
            if cached_result:
                results.append(cached_result)
            else:
                result = await scrape_products(str(url), timeout=settings.SCRAPE_TIMEOUT)
                results.append(result)
                if 'error' not in result:
                    SUCCESSFUL_SCRAPES_TOTAL.inc()
                    await set_cached_result(result["url"], result)
                else:
                    SCRAPE_ERRORS_TOTAL.inc()
        
        return results
    except Exception as e:
        SCRAPE_ERRORS_TOTAL.inc()
        raise HTTPException(status_code=500, detail=f"Error during multiple scraping: {str(e)}")