"""
Security middleware and utilities.

Implements security hardening per OWASP Top 10:
- Security headers
- Audit logging
- Request validation
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Callable, Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.config import settings

# Audit logger - separate from application logs
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)

# Create file handler for audit logs
if not audit_logger.handlers:
    handler = logging.FileHandler("audit.log")
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    audit_logger.addHandler(handler)


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

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # HSTS (only in production)
        if settings.is_production:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        # CSP for API (restrictive since we're not serving HTML)
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"

        # Permissions Policy
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), camera=(), geolocation=(), gyroscope=(), "
            "magnetometer=(), microphone=(), payment=(), usb=()"
        )

        # Remove server header
        if "server" in response.headers:
            del response.headers["server"]

        return response


class AuditEvent:
    """Audit event types."""
    LOGIN_ATTEMPT = "login_attempt"
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    LOGOUT = "logout"
    TOKEN_REFRESH = "token_refresh"
    PASSWORD_RESET_REQUEST = "password_reset_request"
    PERMISSION_DENIED = "permission_denied"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    DATA_ACCESS = "data_access"
    DATA_MUTATION = "data_mutation"
    ADMIN_ACTION = "admin_action"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"


def log_audit_event(
    event_type: str,
    user_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    action: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[dict] = None,
    success: bool = True,
):
    """
    Log an audit event.

    Blueprint §Security: All auth events, data mutations, admin actions logged.
    """
    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "organization_id": organization_id,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "action": action,
        "ip_address": ip_address,
        "user_agent": user_agent,
        "success": success,
        "details": details or {},
    }

    # Log to audit file
    audit_logger.info(str(event))

    # In production, also send to external audit service (SIEM)
    if settings.is_production:
        # TODO: Send to external audit service
        pass


def get_client_ip(request: Request) -> str:
    """Extract client IP from request, handling proxies."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip
    return request.client.host if request.client else "unknown"


def detect_suspicious_activity(request: Request) -> Optional[str]:
    """
    Detect potentially suspicious activity.

    Checks:
    - SQL injection patterns
    - XSS patterns
    - Path traversal
    - Command injection
    """
    suspicious_patterns = [
        # SQL Injection
        "' OR '1'='1",
        "'; DROP TABLE",
        "UNION SELECT",
        "1=1--",
        # XSS
        "<script>",
        "javascript:",
        "onerror=",
        "onload=",
        # Path traversal
        "../",
        "..\\",
        "%2e%2e%2f",
        # Command injection
        "; cat /etc/passwd",
        "| ls -la",
        "&& whoami",
    ]

    # Check URL path
    path = request.url.path.lower()
    for pattern in suspicious_patterns:
        if pattern.lower() in path:
            return f"Suspicious pattern in path: {pattern}"

    # Check query parameters
    for key, value in request.query_params.items():
        combined = f"{key}={value}".lower()
        for pattern in suspicious_patterns:
            if pattern.lower() in combined:
                return f"Suspicious pattern in query: {pattern}"

    return None


class SuspiciousActivityMiddleware(BaseHTTPMiddleware):
    """
    Detect and log suspicious activity.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Check for suspicious activity
        suspicious = detect_suspicious_activity(request)

        if suspicious:
            log_audit_event(
                event_type=AuditEvent.SUSPICIOUS_ACTIVITY,
                ip_address=get_client_ip(request),
                user_agent=request.headers.get("user-agent", "")[:500],
                details={"reason": suspicious, "path": request.url.path},
                success=False,
            )

            # In production, you might want to block the request
            # For now, we just log and continue
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
    # Truncate
    value = value[:max_length]
    # Remove null bytes
    value = value.replace("\x00", "")
    return value
