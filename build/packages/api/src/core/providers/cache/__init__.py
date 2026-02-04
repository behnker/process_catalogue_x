"""
Cache provider abstraction.

Global: Upstash Redis
China: Alibaba Redis
"""

from src.config import settings

from .base import CacheProvider


def get_cache_provider() -> CacheProvider:
    """Factory function to get the configured cache provider."""
    provider = getattr(settings, "CACHE_PROVIDER", "memory")

    if provider == "redis":
        from .redis import RedisProvider
        return RedisProvider()
    else:
        from .memory import InMemoryCacheProvider
        return InMemoryCacheProvider()


__all__ = [
    "CacheProvider",
    "get_cache_provider",
]
