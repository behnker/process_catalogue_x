"""Cache provider base class."""

from abc import ABC, abstractmethod
from typing import Any, Optional


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
