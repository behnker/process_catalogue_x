"""Session management endpoints (refresh, logout, profile)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import (
    CurrentUser,
    create_access_token,
    decode_token,
    get_current_user,
)
from src.core.database import get_db
from src.models.organization import Organization, User, UserOrganization
from src.schemas.auth import (
    OrganizationBrief,
    TokenRefreshRequest,
    UserProfile,
)

router = APIRouter()


@router.post("/refresh")
async def refresh_token(body: TokenRefreshRequest):
    """Refresh an access token using a refresh token."""
    payload = decode_token(body.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=400, detail="Invalid token type")

    access_token = create_access_token(
        user_id=payload["sub"],
        organization_id=payload["org"],
        role="viewer",  # Re-fetch role in production
        email="",
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(user: CurrentUser = Depends(get_current_user)):
    """Invalidate the current session."""
    # In a JWT-based system, client deletes the token
    # For added security, add token to a denylist (Redis)
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserProfile)
async def get_me(
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user profile with all organization memberships."""
    result = await db.execute(select(User).where(User.id == user.id))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all memberships
    result = await db.execute(
        select(UserOrganization, Organization)
        .join(Organization, UserOrganization.organization_id == Organization.id)
        .where(UserOrganization.user_id == user.id)
    )
    memberships = result.all()

    orgs = [
        OrganizationBrief(
            id=org.id,
            name=org.name,
            slug=org.slug,
            role=membership.role,
        )
        for membership, org in memberships
    ]

    return UserProfile(
        id=db_user.id,
        email=db_user.email,
        display_name=db_user.display_name,
        avatar_url=db_user.avatar_url,
        organizations=orgs,
        default_organization_id=db_user.default_organization_id,
        last_login_at=db_user.last_login_at,
    )
