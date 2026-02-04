"""System Catalogue write endpoints (create, update, delete)."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.system_catalogue import ProcessSystem, SystemCatalogue
from src.schemas.system_catalogue import (
    SystemCatalogueCreate,
    SystemCatalogueResponse,
    SystemCatalogueUpdate,
)

router = APIRouter()


async def _get_process_count(
    db: AsyncSession, system_id: str, org_id: str,
) -> int:
    """Get process link count for a system."""
    result = await db.execute(
        select(func.count())
        .select_from(ProcessSystem)
        .where(
            ProcessSystem.system_id == system_id,
            ProcessSystem.organization_id == org_id,
        )
    )
    return result.scalar() or 0


@router.post("/", response_model=SystemCatalogueResponse, status_code=status.HTTP_201_CREATED)
async def create_system(
    body: SystemCatalogueCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new system in the catalogue."""
    system = SystemCatalogue(
        id=str(uuid4()),
        organization_id=user.organization_id,
        created_by=user.id,
        updated_by=user.id,
        **body.model_dump(),
    )
    db.add(system)
    await db.flush()
    await db.refresh(system)

    response = SystemCatalogueResponse.model_validate(system)
    response.process_count = 0
    return response


@router.patch("/{system_id}", response_model=SystemCatalogueResponse)
async def update_system(
    system_id: str,
    body: SystemCatalogueUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a system."""
    result = await db.execute(
        select(SystemCatalogue).where(
            SystemCatalogue.id == system_id,
            SystemCatalogue.organization_id == user.organization_id,
        )
    )
    system = result.scalar_one_or_none()

    if not system:
        raise HTTPException(status_code=404, detail="System not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(system, field, value)

    system.updated_by = user.id
    await db.flush()
    await db.refresh(system)

    process_count = await _get_process_count(db, system.id, user.organization_id)
    response = SystemCatalogueResponse.model_validate(system)
    response.process_count = process_count
    return response


@router.delete("/{system_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system(
    system_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Soft delete a system (set status to 'retire')."""
    result = await db.execute(
        select(SystemCatalogue).where(
            SystemCatalogue.id == system_id,
            SystemCatalogue.organization_id == user.organization_id,
        )
    )
    system = result.scalar_one_or_none()

    if not system:
        raise HTTPException(status_code=404, detail="System not found")

    system.status = "retire"
    system.updated_by = user.id
    await db.flush()
