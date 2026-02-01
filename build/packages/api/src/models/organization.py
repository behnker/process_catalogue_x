"""
Organization (tenant) and User models.

Blueprint §6.1.4: Organization entity model
Blueprint §6.2: Authentication — passwordless, domain-restricted
Blueprint §6.4: RBAC roles and permissions
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base, BaseModel, TenantModel

import enum


# ── Enums ────────────────────────────────────────────

class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    PORTFOLIO_MANAGER = "portfolio_manager"
    PROCESS_OWNER = "process_owner"
    BUSINESS_ANALYST = "business_analyst"
    PROJECT_MANAGER = "project_manager"
    QUALITY_MANAGER = "quality_manager"
    CHANGE_MANAGER = "change_manager"
    VIEWER = "viewer"
    EXTERNAL = "external"


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INVITED = "invited"
    DISABLED = "disabled"


# ── Organization ─────────────────────────────────────

class Organization(BaseModel):
    """
    Multi-tenant organization (tenant boundary).
    All data is scoped to an organization via RLS.
    """

    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    subscription_tier: Mapped[str] = mapped_column(
        String(20), default=SubscriptionTier.FREE.value
    )
    settings: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict)
    branding: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict)
    data_region: Mapped[str] = mapped_column(String(20), default="global")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    users: Mapped[list["User"]] = relationship(back_populates="organization", lazy="selectin")
    allowed_domains: Mapped[list["AllowedDomain"]] = relationship(
        back_populates="organization", lazy="selectin"
    )


# ── Allowed Domains (for magic link domain restriction) ──

class AllowedDomain(BaseModel):
    """
    Email domains allowed to authenticate for an organization.
    Blueprint §6.2.3: Domain verification via DNS TXT or email.
    """

    __tablename__ = "allowed_domains"

    organization_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("organizations.id"), nullable=False
    )
    domain: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verification_method: Mapped[Optional[str]] = mapped_column(String(20))  # dns_txt, email
    verification_token: Mapped[Optional[str]] = mapped_column(String(255))

    organization: Mapped["Organization"] = relationship(back_populates="allowed_domains")


# ── User ─────────────────────────────────────────────

class User(BaseModel):
    """
    User account. No password field — authentication is via magic links only.
    Users belong to one or more organizations via UserOrganization.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    display_name: Mapped[Optional[str]] = mapped_column(String(255))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Default organization (for users in multiple orgs)
    default_organization_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("organizations.id")
    )

    # Relationships
    organization: Mapped[Optional["Organization"]] = relationship(
        back_populates="users", foreign_keys=[default_organization_id]
    )
    memberships: Mapped[list["UserOrganization"]] = relationship(
        back_populates="user", lazy="selectin"
    )


# ── User-Organization Membership ─────────────────────

class UserOrganization(BaseModel):
    """
    Many-to-many: user belongs to organizations with a role in each.
    Blueprint §6.4.2: Standard roles per org membership.
    """

    __tablename__ = "user_organizations"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )
    organization_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("organizations.id"), nullable=False
    )
    role: Mapped[str] = mapped_column(String(50), default=UserRole.VIEWER.value)
    status: Mapped[str] = mapped_column(String(20), default=UserStatus.INVITED.value)
    invited_by: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False))
    invited_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="memberships")


# ── Magic Link Token ─────────────────────────────────

class MagicLinkToken(BaseModel):
    """
    Single-use magic link tokens for passwordless authentication.
    Blueprint §6.2.2: Token expires in 15 minutes, single-use.
    """

    __tablename__ = "magic_link_tokens"

    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(String(500))


# ── Audit Log ────────────────────────────────────────

class AuditLog(BaseModel):
    """
    Comprehensive audit trail for all CRUD operations.
    Blueprint §8.2: All CRUD operations logged with user/timestamp.
    """

    __tablename__ = "audit_logs"

    organization_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("organizations.id"), nullable=False, index=True
    )
    user_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False))
    action: Mapped[str] = mapped_column(String(20), nullable=False)  # create, update, delete
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)
    changes: Mapped[Optional[dict]] = mapped_column(JSONB)  # {field: {old, new}}
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(String(500))
