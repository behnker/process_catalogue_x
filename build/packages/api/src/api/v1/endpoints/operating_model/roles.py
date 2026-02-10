"""Role Catalogue CRUD endpoints — reference data for UI dropdowns."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.operating_model import RoleCatalogue
from src.schemas.operating_model import (
    RoleCatalogueCreate,
    RoleCatalogueResponse,
    RoleCatalogueUpdate,
)

router = APIRouter()


@router.get(
    "/reference/roles",
    response_model=list[RoleCatalogueResponse],
)
async def list_roles(
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List all roles in the catalogue."""
    result = await db.execute(
        select(RoleCatalogue)
        .where(RoleCatalogue.organization_id == user.organization_id)
        .order_by(RoleCatalogue.sort_order)
    )
    return [RoleCatalogueResponse.model_validate(r) for r in result.scalars().all()]


@router.post(
    "/reference/roles",
    response_model=RoleCatalogueResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_role(
    body: RoleCatalogueCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a role in the catalogue."""
    # Check for duplicate name
    result = await db.execute(
        select(RoleCatalogue).where(
            RoleCatalogue.organization_id == user.organization_id,
            RoleCatalogue.name == body.name,
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=409, detail=f"Role '{body.name}' already exists"
        )

    row = RoleCatalogue(
        id=str(uuid4()),
        organization_id=user.organization_id,
        **body.model_dump(),
    )
    db.add(row)
    await db.flush()
    await db.refresh(row)
    return RoleCatalogueResponse.model_validate(row)


@router.patch(
    "/reference/roles/{role_id}",
    response_model=RoleCatalogueResponse,
)
async def update_role(
    role_id: str,
    body: RoleCatalogueUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a role."""
    result = await db.execute(
        select(RoleCatalogue).where(
            RoleCatalogue.id == role_id,
            RoleCatalogue.organization_id == user.organization_id,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Role not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(row, field, value)
    await db.flush()
    await db.refresh(row)
    return RoleCatalogueResponse.model_validate(row)


@router.delete(
    "/reference/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_role(
    role_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a role."""
    result = await db.execute(
        select(RoleCatalogue).where(
            RoleCatalogue.id == role_id,
            RoleCatalogue.organization_id == user.organization_id,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Role not found")
    await db.delete(row)
    await db.flush()
