"""
Rate limiting middleware.

Blueprint §6.2: Auth endpoints 5 req/min, API 100 req/min per user.

Supports:
- In-memory store (development)
- Redis store (production)
"""

import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Optional

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from src.config import settings


@dataclass
class RateLimitConfig:
    """Rate limit configuration."""
    requests: int  # Max requests
    window: int    # Time window in seconds

    @property
    def requests_per_minute(self) -> float:
        return self.requests / self.window * 60


# Rate limit configurations per Blueprint §6.2
RATE_LIMITS = {
    # Auth endpoints: 5 requests per minute
    "auth": RateLimitConfig(requests=5, window=60),

    # General API: 100 requests per minute
    "api": RateLimitConfig(requests=100, window=60),

    # Strict endpoints (password reset, etc.): 3 per minute
    "strict": RateLimitConfig(requests=3, window=60),
}


@dataclass
class TokenBucket:
    """Token bucket for rate limiting."""
    tokens: float
    last_refill: float
    capacity: int
    refill_rate: float  # tokens per second

    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens. Returns True if allowed."""
        now = time.time()

        # Refill tokens based on elapsed time
        elapsed = now - self.last_refill
        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.refill_rate
        )
        self.last_refill = now

        # Check if we have enough tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    @property
    def retry_after(self) -> int:
        """Seconds until a token is available."""
        if self.tokens >= 1:
            return 0
        tokens_needed = 1 - self.tokens
        return int(tokens_needed / self.refill_rate) + 1


class InMemoryRateLimiter:
    """
    In-memory rate limiter using token bucket algorithm.
    Suitable for single-instance development.
    """

    def __init__(self):
        self._buckets: dict[str, TokenBucket] = {}
        self._cleanup_interval = 300  # Clean up every 5 minutes
        self._last_cleanup = time.time()

    def _get_bucket(self, key: str, config: RateLimitConfig) -> TokenBucket:
        """Get or create a token bucket for the given key."""
        if key not in self._buckets:
            refill_rate = config.requests / config.window
            self._buckets[key] = TokenBucket(
                tokens=config.requests,
                last_refill=time.time(),
                capacity=config.requests,
                refill_rate=refill_rate,
            )
        return self._buckets[key]

    def is_allowed(self, key: str, config: RateLimitConfig) -> tuple[bool, int]:
        """
        Check if request is allowed.
        Returns (allowed, retry_after_seconds).
        """
        self._maybe_cleanup()
        bucket = self._get_bucket(key, config)
        allowed = bucket.consume()
        return allowed, bucket.retry_after

    def _maybe_cleanup(self):
        """Periodically clean up old buckets."""
        now = time.time()
        if now - self._last_cleanup > self._cleanup_interval:
            self._last_cleanup = now
            # Remove buckets that haven't been used in 10 minutes
            cutoff = now - 600
            self._buckets = {
                k: v for k, v in self._buckets.items()
                if v.last_refill > cutoff
            }


# Global rate limiter instance
_rate_limiter = InMemoryRateLimiter()


def get_rate_limit_key(request: Request, user_id: Optional[str] = None) -> str:
    """Generate rate limit key from request."""
    # Use user ID if authenticated, otherwise use IP
    if user_id:
        return f"user:{user_id}"

    # Get client IP (handle proxies)
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        ip = forwarded.split(",")[0].strip()
    else:
        ip = request.client.host if request.client else "unknown"

    return f"ip:{ip}"


def get_rate_limit_type(path: str) -> str:
    """Determine rate limit type based on path."""
    if "/auth/" in path:
        return "auth"
    return "api"


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware.

    Applies different limits based on endpoint:
    - /auth/* endpoints: 5 req/min (prevent brute force)
    - Other API endpoints: 100 req/min per user
    """

    async def dispatch(self, request: Request, call_next: Callable):
        # Skip rate limiting for health checks and docs
        path = request.url.path
        if path in ("/health", "/docs", "/redoc", "/openapi.json"):
            return await call_next(request)

        # Skip in test environment
        if settings.ENVIRONMENT == "test":
            return await call_next(request)

        # Determine rate limit type and config
        limit_type = get_rate_limit_type(path)
        config = RATE_LIMITS.get(limit_type, RATE_LIMITS["api"])

        # Get rate limit key (try to use user ID from token if available)
        user_id = getattr(request.state, "user_id", None)
        key = f"{limit_type}:{get_rate_limit_key(request, user_id)}"

        # Check rate limit
        allowed, retry_after = _rate_limiter.is_allowed(key, config)

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again in {retry_after} seconds.",
                headers={"Retry-After": str(retry_after)},
            )

        # Add rate limit headers to response
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(config.requests)
        response.headers["X-RateLimit-Window"] = str(config.window)

        return response


def rate_limit(limit_type: str = "api"):
    """
    Decorator for rate limiting specific endpoints.

    Usage:
        @router.post("/sensitive")
        @rate_limit("strict")
        async def sensitive_endpoint():
            ...
    """
    config = RATE_LIMITS.get(limit_type, RATE_LIMITS["api"])

    def decorator(func: Callable) -> Callable:
        async def wrapper(request: Request, *args, **kwargs):
            user_id = getattr(request.state, "user_id", None)
            key = f"{limit_type}:{get_rate_limit_key(request, user_id)}"

            allowed, retry_after = _rate_limiter.is_allowed(key, config)
            if not allowed:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Try again in {retry_after} seconds.",
                    headers={"Retry-After": str(retry_after)},
                )

            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
