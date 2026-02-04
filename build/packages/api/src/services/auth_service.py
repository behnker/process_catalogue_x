"""
Authentication service — business logic extracted from magic link endpoints.

Handles user creation, org membership, and token generation.
"""

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.core.auth import (
    create_access_token,
    create_refresh_token,
)
from src.models.organization import (
    AllowedDomain,
    Organization,
    User,
    UserOrganization,
)
from src.schemas.auth import TokenVerifyResponse, UserBrief


async def create_dev_session(db: AsyncSession) -> TokenVerifyResponse:
    """
    Create a development session with test org/user.
    Only callable in development/test environments.
    """
    # Find or create test organization
    result = await db.execute(
        select(Organization).where(Organization.slug == "dev-org")
    )
    org = result.scalar_one_or_none()

    if not org:
        org = Organization(
            name="Development Organization",
            slug="dev-org",
            settings={"theme": "default"},
        )
        db.add(org)
        await db.flush()

        allowed = AllowedDomain(
            organization_id=org.id,
            domain="dev.local",
            is_verified=True,
        )
        db.add(allowed)
        await db.flush()

    # Find or create admin user
    user = await find_or_create_user(db, "admin@dev.local")

    if not user.default_organization_id:
        user.default_organization_id = org.id

    await ensure_org_membership(db, user.id, org.id, role="admin")

    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()

    return build_token_response(user, org, role="admin")


async def find_or_create_user(
    db: AsyncSession,
    email: str,
) -> User:
    """Find existing user or create on first login."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            email=email,
            display_name=email.split("@")[0].replace(".", " ").title(),
        )
        db.add(user)
        await db.flush()

    return user


async def ensure_org_membership(
    db: AsyncSession,
    user_id: str,
    org_id: str,
    role: str = "viewer",
) -> UserOrganization:
    """Ensure user has membership in organization, creating if needed."""
    result = await db.execute(
        select(UserOrganization).where(
            UserOrganization.user_id == user_id,
            UserOrganization.organization_id == org_id,
        )
    )
    membership = result.scalar_one_or_none()

    if not membership:
        membership = UserOrganization(
            user_id=user_id,
            organization_id=org_id,
            role=role,
            status="active",
        )
        db.add(membership)
        await db.flush()

    return membership


def build_token_response(
    user: User,
    org: Organization,
    role: str,
) -> TokenVerifyResponse:
    """Build access + refresh token response."""
    access_token = create_access_token(
        user_id=user.id,
        organization_id=org.id,
        role=role,
        email=user.email,
    )
    refresh_token = create_refresh_token(user.id, org.id)

    return TokenVerifyResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserBrief(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            avatar_url=user.avatar_url,
            role=role,
            organization_id=org.id,
            organization_name=org.name,
        ),
    )
