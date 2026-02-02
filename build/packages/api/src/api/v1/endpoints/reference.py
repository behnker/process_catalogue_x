"""
Reference Catalogue API endpoints.
CRUD for departments, functions, roles, systems, and other reference data.
"""

from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.reference import ReferenceCatalogue
from src.schemas.reference import (
    CATALOGUE_TYPES,
    ReferenceCatalogueCreate,
    ReferenceCatalogueListResponse,
    ReferenceCatalogueResponse,
    ReferenceCatalogueUpdate,
)

router = APIRouter()


@router.get("/", response_model=ReferenceCatalogueListResponse)
async def list_reference_catalogues(
    catalogue_type: Optional[str] = Query(None, description="Filter by type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search code/name"),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List reference catalogue entries with optional filters."""
    query = select(ReferenceCatalogue).where(
        ReferenceCatalogue.organization_id == user.organization_id
    )

    if catalogue_type:
        query = query.where(ReferenceCatalogue.catalogue_type == catalogue_type)
    if status:
        query = query.where(ReferenceCatalogue.status == status)
    if search:
        query = query.where(
            ReferenceCatalogue.name.ilike(f"%{search}%")
            | ReferenceCatalogue.code.ilike(f"%{search}%")
        )

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Order by type, then sort_order
    query = query.order_by(
        ReferenceCatalogue.catalogue_type,
        ReferenceCatalogue.sort_order,
        ReferenceCatalogue.name,
    )

    result = await db.execute(query)
    items = result.scalars().all()

    return ReferenceCatalogueListResponse(
        items=[ReferenceCatalogueResponse.model_validate(item) for item in items],
        total=total,
    )


@router.get("/types")
async def list_catalogue_types():
    """List available catalogue types."""
    return {"types": CATALOGUE_TYPES}


@router.get("/{item_id}", response_model=ReferenceCatalogueResponse)
async def get_reference_catalogue(
    item_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get a single reference catalogue entry."""
    result = await db.execute(
        select(ReferenceCatalogue).where(
            ReferenceCatalogue.id == item_id,
            ReferenceCatalogue.organization_id == user.organization_id,
        )
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Reference item not found")

    return ReferenceCatalogueResponse.model_validate(item)


@router.post("/", response_model=ReferenceCatalogueResponse, status_code=status.HTTP_201_CREATED)
async def create_reference_catalogue(
    body: ReferenceCatalogueCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new reference catalogue entry."""
    # Validate catalogue type
    if body.catalogue_type not in CATALOGUE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid catalogue_type. Must be one of: {CATALOGUE_TYPES}",
        )

    # Check for duplicate code within same type
    existing = await db.execute(
        select(ReferenceCatalogue).where(
            ReferenceCatalogue.organization_id == user.organization_id,
            ReferenceCatalogue.catalogue_type == body.catalogue_type,
            ReferenceCatalogue.code == body.code,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail=f"Code '{body.code}' already exists for {body.catalogue_type}",
        )

    item = ReferenceCatalogue(
        id=str(uuid4()),
        organization_id=user.organization_id,
        **body.model_dump(),
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)

    return ReferenceCatalogueResponse.model_validate(item)


@router.patch("/{item_id}", response_model=ReferenceCatalogueResponse)
async def update_reference_catalogue(
    item_id: str,
    body: ReferenceCatalogueUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update an existing reference catalogue entry."""
    result = await db.execute(
        select(ReferenceCatalogue).where(
            ReferenceCatalogue.id == item_id,
            ReferenceCatalogue.organization_id == user.organization_id,
        )
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Reference item not found")

    update_data = body.model_dump(exclude_unset=True)

    # If updating code, check for duplicates
    if "code" in update_data and update_data["code"] != item.code:
        existing = await db.execute(
            select(ReferenceCatalogue).where(
                ReferenceCatalogue.organization_id == user.organization_id,
                ReferenceCatalogue.catalogue_type == item.catalogue_type,
                ReferenceCatalogue.code == update_data["code"],
                ReferenceCatalogue.id != item_id,
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail=f"Code '{update_data['code']}' already exists for {item.catalogue_type}",
            )

    for field, value in update_data.items():
        setattr(item, field, value)

    await db.flush()
    await db.refresh(item)

    return ReferenceCatalogueResponse.model_validate(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reference_catalogue(
    item_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a reference catalogue entry (soft delete)."""
    result = await db.execute(
        select(ReferenceCatalogue).where(
            ReferenceCatalogue.id == item_id,
            ReferenceCatalogue.organization_id == user.organization_id,
        )
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Reference item not found")

    item.status = "inactive"
    await db.flush()
