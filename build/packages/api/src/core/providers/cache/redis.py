"""Redis cache provider (Upstash Global / Alibaba China)."""

import json
from typing import Any, Optional

from src.config import settings

from .base import CacheProvider


class RedisProvider(CacheProvider):
    """
    Redis cache provider.
    Works with both Upstash (Global) and Alibaba Redis (China).
    """

    def __init__(self):
        try:
            import redis.asyncio as aioredis
            self.redis = aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
            )
        except ImportError:
            raise ImportError("redis package required. Install with: pip install redis")

    async def get(self, key: str) -> Optional[Any]:
        value = await self.redis.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        try:
            if ttl:
                await self.redis.setex(key, ttl, value)
            else:
                await self.redis.set(key, value)
            return True
        except Exception:
            return False

    async def delete(self, key: str) -> bool:
        try:
            await self.redis.delete(key)
            return True
        except Exception:
            return False

    async def exists(self, key: str) -> bool:
        return await self.redis.exists(key) > 0

    async def incr(self, key: str) -> int:
        return await self.redis.incr(key)

    async def expire(self, key: str, ttl: int) -> bool:
        return await self.redis.expire(key, ttl)

    async def keys(self, pattern: str) -> list[str]:
        return await self.redis.keys(pattern)

    async def flush(self) -> bool:
        try:
            await self.redis.flushdb()
            return True
        except Exception:
            return False
