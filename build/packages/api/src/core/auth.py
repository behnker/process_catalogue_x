"""
Passwordless Magic Link Authentication.

Blueprint §6.2.2: No passwords are stored or required.
Users authenticate via email-only magic links.

Flow:
  1. User enters email → POST /api/v1/auth/magic-link
  2. System validates domain against registered organizations
  3. System generates single-use token (UUID + HMAC signature)
  4. System emails magic link to user
  5. User clicks link → GET /api/v1/auth/verify/{token}
  6. System validates token (not expired, not used, domain matches)
  7. System creates session → returns JWT access + refresh tokens
"""

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import uuid4

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.core.database import get_db

# JWT configuration
ALGORITHM = "HS256"
security = HTTPBearer(auto_error=False)


def create_magic_link_token(email: str) -> tuple[str, str, datetime]:
    """
    Generate a secure magic link token.
    Returns (token_id, token_hash, expires_at).
    """
    token_id = str(uuid4())
    raw_token = secrets.token_urlsafe(48)

    # HMAC signature binds token to email
    token_hash = hmac.new(
        settings.MAGIC_LINK_SECRET.encode(),
        f"{token_id}:{raw_token}:{email}".encode(),
        hashlib.sha256,
    ).hexdigest()

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.MAGIC_LINK_EXPIRY_MINUTES
    )

    # The URL-safe token sent to user is {token_id}.{raw_token}
    full_token = f"{token_id}.{raw_token}"

    return full_token, token_hash, expires_at


def verify_magic_link_token(full_token: str, email: str, stored_hash: str) -> bool:
    """Verify a magic link token against its stored hash."""
    try:
        token_id, raw_token = full_token.split(".", 1)
    except ValueError:
        return False

    expected_hash = hmac.new(
        settings.MAGIC_LINK_SECRET.encode(),
        f"{token_id}:{raw_token}:{email}".encode(),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected_hash, stored_hash)


def create_access_token(
    user_id: str,
    organization_id: str,
    role: str,
    email: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT access token."""
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {
        "sub": user_id,
        "org": organization_id,
        "role": role,
        "email": email,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: str, organization_id: str) -> str:
    """Create a JWT refresh token (longer-lived)."""
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    payload = {
        "sub": user_id,
        "org": organization_id,
        "exp": expire,
        "type": "refresh",
        "jti": str(uuid4()),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


class CurrentUser:
    """Represents the authenticated user extracted from JWT."""

    def __init__(self, user_id: str, organization_id: str, role: str, email: str):
        self.id = user_id
        self.organization_id = organization_id
        self.role = role
        self.email = email


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> CurrentUser:
    """
    FastAPI dependency: extract and validate the authenticated user from JWT.
    Also sets request.state.organization_id for tenant middleware.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_token(credentials.credentials)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    user = CurrentUser(
        user_id=payload["sub"],
        organization_id=payload["org"],
        role=payload.get("role", "viewer"),
        email=payload.get("email", ""),
    )

    # Set org context for tenant middleware
    request.state.organization_id = user.organization_id

    return user


def require_role(*allowed_roles: str):
    """
    Factory for role-based access control.
    Usage: Depends(require_role("admin", "portfolio_manager"))
    """

    async def role_checker(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if user.role not in allowed_roles and user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user.role}' does not have access. Required: {', '.join(allowed_roles)}",
            )
        return user

    return role_checker
