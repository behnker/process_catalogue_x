"""In-memory cache provider for development."""

import fnmatch
import time
from typing import Any, Optional

from .base import CacheProvider


class InMemoryCacheProvider(CacheProvider):
    """
    In-memory cache provider for development.
    Uses a simple dict with TTL support.
    """

    def __init__(self):
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
        self._cleanup()
        return [k for k in self._cache.keys() if fnmatch.fnmatch(k, pattern)]

    async def flush(self) -> bool:
        self._cache.clear()
        return True
