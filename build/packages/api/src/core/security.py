"""
Security middleware and utilities.

Implements security hardening per OWASP Top 10:
- Security headers
- Suspicious activity detection
- Request validation
"""

import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.config import settings

# Backward-compatible re-exports
from src.core.encryption import (  # noqa: F401
    decrypt_sensitive_data,
    encrypt_sensitive_data,
    generate_encryption_key,
)
from src.core.audit import (  # noqa: F401
    AuditEvent,
    audit_logger,
    detect_suspicious_activity,
    get_client_ip,
    log_audit_event,
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses.

    OWASP recommendations:
    - X-Content-Type-Options: Prevent MIME sniffing
    - X-Frame-Options: Prevent clickjacking
    - X-XSS-Protection: Enable XSS filter
    - Strict-Transport-Security: Enforce HTTPS
    - Content-Security-Policy: Restrict resource loading
    - Referrer-Policy: Control referrer information
    - Permissions-Policy: Restrict browser features
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        if settings.is_production:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"

        response.headers["Permissions-Policy"] = (
            "accelerometer=(), camera=(), geolocation=(), gyroscope=(), "
            "magnetometer=(), microphone=(), payment=(), usb=()"
        )

        if "server" in response.headers:
            del response.headers["server"]

        return response


class SuspiciousActivityMiddleware(BaseHTTPMiddleware):
    """Detect and log suspicious activity."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        suspicious = detect_suspicious_activity(request)

        if suspicious:
            log_audit_event(
                event_type=AuditEvent.SUSPICIOUS_ACTIVITY,
                ip_address=get_client_ip(request),
                user_agent=request.headers.get("user-agent", "")[:500],
                details={"reason": suspicious, "path": request.url.path},
                success=False,
            )

            if settings.is_production:
                pass  # Consider blocking or additional validation

        return await call_next(request)


def validate_uuid(value: str) -> bool:
    """Validate UUID format to prevent injection."""
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError):
        return False


def sanitize_string(value: str, max_length: int = 1000) -> str:
    """Sanitize string input."""
    if not value:
        return ""
    value = value[:max_length]
    value = value.replace("\x00", "")
    return value
