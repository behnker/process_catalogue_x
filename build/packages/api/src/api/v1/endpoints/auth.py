"""
Authentication API endpoints.

Blueprint §6.2.10 Authentication Endpoints:
  POST /api/v1/auth/magic-link     — Request magic link
  GET  /api/v1/auth/verify/{token} — Verify magic link and login
  POST /api/v1/auth/refresh        — Refresh access token
  POST /api/v1/auth/logout         — Invalidate session
  GET  /api/v1/auth/me             — Current user profile
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.core.auth import (
    CurrentUser,
    create_access_token,
    create_magic_link_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    verify_magic_link_token,
)
from src.core.database import get_db
from src.models.organization import (
    AllowedDomain,
    MagicLinkToken,
    Organization,
    User,
    UserOrganization,
)
from src.schemas.auth import (
    MagicLinkRequest,
    MagicLinkResponse,
    OrganizationBrief,
    TokenRefreshRequest,
    TokenVerifyResponse,
    UserBrief,
    UserProfile,
)

router = APIRouter()


@router.post("/magic-link", response_model=MagicLinkResponse)
async def request_magic_link(
    body: MagicLinkRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Step 1: User submits email → system sends magic link.
    Always returns success (prevents email enumeration).
    """
    email = body.email.lower().strip()
    domain = email.split("@")[1]

    # Check if domain is registered for any org
    result = await db.execute(
        select(AllowedDomain).where(
            AllowedDomain.domain == domain,
            AllowedDomain.is_verified == True,
        )
    )
    allowed = result.scalar_one_or_none()

    if allowed:
        # Generate magic link token
        full_token, token_hash, expires_at = create_magic_link_token(email)

        # Store token in DB
        magic_token = MagicLinkToken(
            email=email,
            token_hash=token_hash,
            expires_at=expires_at,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent", "")[:500],
        )
        db.add(magic_token)
        await db.flush()

        # Build magic link URL
        magic_link_url = f"{settings.FRONTEND_URL}/auth/verify?token={full_token}"

        # TODO: Send email via Resend/SendGrid
        # For development, log to console
        if settings.EMAIL_PROVIDER == "console":
            print(f"\n🔗 Magic Link for {email}: {magic_link_url}\n")
        else:
            # await send_magic_link_email(email, magic_link_url)
            pass

    # Always return same response (prevent enumeration)
    return MagicLinkResponse()


@router.get("/verify/{token}")
async def verify_magic_link(
    token: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Step 2: User clicks magic link → system validates and creates session.
    """
    # Find token in DB
    try:
        token_id = token.split(".")[0]
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid token format")

    result = await db.execute(
        select(MagicLinkToken).where(
            MagicLinkToken.id == token_id,
            MagicLinkToken.is_used == False,
        )
    )
    magic_token = result.scalar_one_or_none()

    if not magic_token:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Check expiry
    if magic_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Token has expired")

    # Verify HMAC
    if not verify_magic_link_token(token, magic_token.email, magic_token.token_hash):
        raise HTTPException(status_code=400, detail="Invalid token")

    # Mark as used
    magic_token.is_used = True
    magic_token.used_at = datetime.now(timezone.utc)

    # Find or create user
    email = magic_token.email
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        # Auto-create user on first login (self-registration)
        user = User(
            email=email,
            display_name=email.split("@")[0].replace(".", " ").title(),
        )
        db.add(user)
        await db.flush()

    # Find org membership
    domain = email.split("@")[1]
    result = await db.execute(
        select(AllowedDomain).where(AllowedDomain.domain == domain)
    )
    allowed_domain = result.scalar_one_or_none()

    if not allowed_domain:
        raise HTTPException(status_code=403, detail="Organization not found for this domain")

    org_id = allowed_domain.organization_id

    # Ensure user has membership
    result = await db.execute(
        select(UserOrganization).where(
            UserOrganization.user_id == user.id,
            UserOrganization.organization_id == org_id,
        )
    )
    membership = result.scalar_one_or_none()

    if not membership:
        membership = UserOrganization(
            user_id=user.id,
            organization_id=org_id,
            role="viewer",
            status="active",
        )
        db.add(membership)
        await db.flush()

    # Update last login
    user.last_login_at = datetime.now(timezone.utc)
    if not user.default_organization_id:
        user.default_organization_id = org_id

    # Get org name
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    org = result.scalar_one()

    # Create tokens
    access_token = create_access_token(
        user_id=user.id,
        organization_id=org_id,
        role=membership.role,
        email=user.email,
    )
    refresh_token = create_refresh_token(user.id, org_id)

    return TokenVerifyResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserBrief(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            avatar_url=user.avatar_url,
            role=membership.role,
            organization_id=org_id,
            organization_name=org.name,
        ),
    )


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
