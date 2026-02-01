"""
Authentication API schemas.
Blueprint §6.2.10: Authentication Endpoints
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class MagicLinkRequest(BaseModel):
    """POST /api/v1/auth/magic-link"""
    email: EmailStr


class MagicLinkResponse(BaseModel):
    """Response after requesting a magic link."""
    message: str = "If an account exists for this email, a login link has been sent."
    expires_in_minutes: int = 15


class TokenVerifyResponse(BaseModel):
    """Response after verifying a magic link token."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: "UserBrief"


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class UserBrief(BaseModel):
    id: str
    email: str
    display_name: Optional[str]
    avatar_url: Optional[str]
    role: str
    organization_id: str
    organization_name: str


class OrganizationBrief(BaseModel):
    id: str
    name: str
    slug: str
    role: str


class UserProfile(BaseModel):
    id: str
    email: str
    display_name: Optional[str]
    avatar_url: Optional[str]
    organizations: list[OrganizationBrief]
    default_organization_id: Optional[str]
    last_login_at: Optional[datetime]


# Resolve forward ref
TokenVerifyResponse.model_rebuild()
