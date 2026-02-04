"""Magic link authentication endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.core.auth import create_magic_link_token, verify_magic_link_token
from src.core.database import get_db
from src.models.organization import AllowedDomain, MagicLinkToken, Organization
from src.schemas.auth import MagicLinkRequest, MagicLinkResponse
from src.services.auth_service import (
    build_token_response,
    create_dev_session,
    ensure_org_membership,
    find_or_create_user,
)

router = APIRouter()


@router.post("/dev-login")
async def dev_login(db: AsyncSession = Depends(get_db)):
    """
    Development-only: Auto-login as admin without magic link.
    Creates test org/user if they don't exist.
    """
    if settings.ENVIRONMENT not in ("development", "local", "test"):
        raise HTTPException(status_code=404, detail="Not found")

    return await create_dev_session(db)


@router.post("/magic-link", response_model=MagicLinkResponse)
async def request_magic_link(
    body: MagicLinkRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Step 1: User submits email -> system sends magic link.
    Always returns success (prevents email enumeration).
    """
    email = body.email.lower().strip()
    domain = email.split("@")[1]

    result = await db.execute(
        select(AllowedDomain).where(
            AllowedDomain.domain == domain,
            AllowedDomain.is_verified == True,
        )
    )
    allowed = result.scalar_one_or_none()

    if allowed:
        full_token, token_hash, expires_at = create_magic_link_token(email)

        magic_token = MagicLinkToken(
            email=email,
            token_hash=token_hash,
            expires_at=expires_at,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent", "")[:500],
        )
        db.add(magic_token)
        await db.flush()

        magic_link_url = f"{settings.FRONTEND_URL}/auth/verify?token={full_token}"

        from src.services.email import send_magic_link_email
        await send_magic_link_email(email, magic_link_url)

    return MagicLinkResponse()


@router.get("/verify/{token}")
async def verify_magic_link(
    token: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Step 2: User clicks magic link -> system validates and creates session.
    """
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

    if magic_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Token has expired")

    if not verify_magic_link_token(token, magic_token.email, magic_token.token_hash):
        raise HTTPException(status_code=400, detail="Invalid token")

    magic_token.is_used = True
    magic_token.used_at = datetime.now(timezone.utc)

    email = magic_token.email
    user = await find_or_create_user(db, email)

    # Resolve organization from domain
    domain = email.split("@")[1]
    result = await db.execute(
        select(AllowedDomain).where(AllowedDomain.domain == domain)
    )
    allowed_domain = result.scalar_one_or_none()

    if not allowed_domain:
        raise HTTPException(status_code=403, detail="Organization not found for this domain")

    org_id = allowed_domain.organization_id
    membership = await ensure_org_membership(db, user.id, org_id)

    user.last_login_at = datetime.now(timezone.utc)
    if not user.default_organization_id:
        user.default_organization_id = org_id

    result = await db.execute(select(Organization).where(Organization.id == org_id))
    org = result.scalar_one()

    return build_token_response(user, org, role=membership.role)
