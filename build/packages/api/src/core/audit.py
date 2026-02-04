"""
Audit logging for security events.

Blueprint §Security: All auth events, data mutations, admin actions logged.
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import Request

from src.config import settings


# Audit logger - separate from application logs
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)

if not audit_logger.handlers:
    handler = logging.FileHandler("audit.log")
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    audit_logger.addHandler(handler)


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
    """Log an audit event."""
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

    audit_logger.info(str(event))

    if settings.is_production:
        # TODO: Send to external audit service (SIEM)
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

    Checks for SQL injection, XSS, path traversal, and command injection patterns.
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

    path = request.url.path.lower()
    for pattern in suspicious_patterns:
        if pattern.lower() in path:
            return f"Suspicious pattern in path: {pattern}"

    for key, value in request.query_params.items():
        combined = f"{key}={value}".lower()
        for pattern in suspicious_patterns:
            if pattern.lower() in combined:
                return f"Suspicious pattern in query: {pattern}"

    return None
