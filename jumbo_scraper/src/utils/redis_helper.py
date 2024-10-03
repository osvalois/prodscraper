import json
from typing import Dict, Any
from redis import asyncio as aioredis
from ..core.config import settings

redis_client = aioredis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True,
    max_connections=settings.REDIS_MAX_CONNECTIONS,
    socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
    retry_on_timeout=settings.REDIS_RETRY_ON_TIMEOUT
)

async def get_cached_result(url: str) -> Dict[str, Any]:
    cached_result = await redis_client.get(url)
    if cached_result:
        return json.loads(cached_result)
    return None

async def set_cached_result(url: str, result: Dict[str, Any]):
    await redis_client.setex(url, settings.REDIS_CACHE_EXPIRATION, json.dumps(result))