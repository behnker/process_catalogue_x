"""
Multi-tenant middleware and context.
Extracts organization context from authenticated user and injects into
all database queries via RLS or application-level filtering.

Blueprint §6.1: Organization-based data isolation with shared infrastructure.
"""

from contextvars import ContextVar
from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db

# Context variable holding the current tenant ID for this request
_current_org_id: ContextVar[Optional[str]] = ContextVar("current_org_id", default=None)


def get_current_org_id() -> Optional[str]:
    """Get the current organization ID from context."""
    return _current_org_id.get()


def set_current_org_id(org_id: str) -> None:
    """Set the current organization ID in context."""
    _current_org_id.set(org_id)


async def get_tenant_db(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> AsyncSession:
    """
    FastAPI dependency that returns a tenant-scoped database session.
    Sets the PostgreSQL session variable for RLS policies.
    """
    org_id = getattr(request.state, "organization_id", None)

    if not org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization context required",
        )

    # Set PostgreSQL session variable for Row-Level Security
    # Note: SET doesn't support parameterized queries, so we use string formatting
    # The org_id is a UUID from our auth system, so it's safe to interpolate
    await db.execute(text(f"SET app.current_organization_id = '{org_id}'"))
    set_current_org_id(org_id)

    return db


def apply_tenant_filter(query, model_class, org_id: str):
    """
    Apply organization filter to any query.
    Use this as a fallback when RLS is not available (e.g., testing).
    """
    if hasattr(model_class, "organization_id"):
        return query.where(model_class.organization_id == org_id)
    return query
