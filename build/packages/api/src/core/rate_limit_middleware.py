"""Rate limiting middleware and endpoint decorator."""

from typing import Callable

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from src.config import settings
from src.core.rate_limit import (
    RATE_LIMITS,
    _rate_limiter,
    get_rate_limit_key,
    get_rate_limit_type,
)


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
            # Skip in test environment (consistent with middleware)
            if settings.ENVIRONMENT == "test":
                return await func(request, *args, **kwargs)

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
