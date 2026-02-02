"""
Cache provider abstraction.

Global: Upstash Redis
China: Alibaba Redis

Provides a unified interface for caching across providers.
"""

import json
from abc import ABC, abstractmethod
from typing import Any, Optional

from src.config import settings


class CacheProvider(ABC):
    """Abstract cache provider interface."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        pass

    @abstractmethod
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        """Set a value in cache with optional TTL in seconds."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete a key from cache."""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if a key exists."""
        pass

    @abstractmethod
    async def incr(self, key: str) -> int:
        """Increment a counter."""
        pass

    @abstractmethod
    async def expire(self, key: str, ttl: int) -> bool:
        """Set TTL on an existing key."""
        pass

    @abstractmethod
    async def keys(self, pattern: str) -> list[str]:
        """Get keys matching pattern."""
        pass

    @abstractmethod
    async def flush(self) -> bool:
        """Flush all keys (use with caution)."""
        pass


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


class InMemoryCacheProvider(CacheProvider):
    """
    In-memory cache provider for development.
    Uses a simple dict with TTL support.
    """

    def __init__(self):
        import time
        self._cache: dict[str, tuple[Any, Optional[float]]] = {}
        self._time = time

    def _is_expired(self, key: str) -> bool:
        if key not in self._cache:
            return True
        _, expiry = self._cache[key]
        if expiry is None:
            return False
        return self._time.time() > expiry

    def _cleanup(self):
        """Remove expired keys."""
        now = self._time.time()
        expired = [
            k for k, (_, exp) in self._cache.items()
            if exp is not None and now > exp
        ]
        for k in expired:
            del self._cache[k]

    async def get(self, key: str) -> Optional[Any]:
        if self._is_expired(key):
            if key in self._cache:
                del self._cache[key]
            return None
        value, _ = self._cache[key]
        return value

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        expiry = None
        if ttl:
            expiry = self._time.time() + ttl
        self._cache[key] = (value, expiry)
        return True

    async def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
        return True

    async def exists(self, key: str) -> bool:
        return key in self._cache and not self._is_expired(key)

    async def incr(self, key: str) -> int:
        if self._is_expired(key):
            self._cache[key] = (1, None)
            return 1
        value, expiry = self._cache[key]
        new_value = int(value) + 1
        self._cache[key] = (new_value, expiry)
        return new_value

    async def expire(self, key: str, ttl: int) -> bool:
        if key not in self._cache:
            return False
        value, _ = self._cache[key]
        self._cache[key] = (value, self._time.time() + ttl)
        return True

    async def keys(self, pattern: str) -> list[str]:
        import fnmatch
        self._cleanup()
        return [k for k in self._cache.keys() if fnmatch.fnmatch(k, pattern)]

    async def flush(self) -> bool:
        self._cache.clear()
        return True


def get_cache_provider() -> CacheProvider:
    """
    Factory function to get the configured cache provider.
    """
    provider = getattr(settings, "CACHE_PROVIDER", "memory")

    if provider == "redis":
        return RedisProvider()
    else:
        return InMemoryCacheProvider()
