"""System Catalogue CRUD endpoints."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.system_catalogue import SystemCatalogue, ProcessSystem
from src.schemas.system_catalogue import (
    SystemCatalogueCreate,
    SystemCatalogueListResponse,
    SystemCatalogueResponse,
    SystemCatalogueUpdate,
)

router = APIRouter()


@router.get("/", response_model=SystemCatalogueListResponse)
async def list_systems(
    status: str | None = Query(None, description="Filter by status"),
    system_type: str | None = Query(None, description="Filter by system type"),
    hosting_model: str | None = Query(None, description="Filter by hosting model"),
    operating_region: str | None = Query(None, description="Filter by region"),
    criticality: str | None = Query(None, description="Filter by criticality"),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List systems with optional filters."""
    query = select(SystemCatalogue).where(
        SystemCatalogue.organization_id == user.organization_id
    )

    if status:
        query = query.where(SystemCatalogue.status == status)
    if system_type:
        query = query.where(SystemCatalogue.system_type == system_type)
    if hosting_model:
        query = query.where(SystemCatalogue.hosting_model == hosting_model)
    if operating_region:
        query = query.where(SystemCatalogue.operating_region == operating_region)
    if criticality:
        query = query.where(SystemCatalogue.criticality == criticality)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Paginate
    offset = (page - 1) * per_page
    query = query.order_by(SystemCatalogue.name).offset(offset).limit(per_page)
    result = await db.execute(query)
    systems = result.scalars().all()

    # Get process counts for each system
    items = []
    for sys in systems:
        count_result = await db.execute(
            select(func.count())
            .select_from(ProcessSystem)
            .where(
                ProcessSystem.system_id == sys.id,
                ProcessSystem.organization_id == user.organization_id,
            )
        )
        process_count = count_result.scalar() or 0
        response = SystemCatalogueResponse.model_validate(sys)
        response.process_count = process_count
        items.append(response)

    return SystemCatalogueListResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        has_more=(offset + len(systems)) < total,
    )


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


@router.get("/{system_id}", response_model=SystemCatalogueResponse)
async def get_system(
    system_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get a single system by ID."""
    result = await db.execute(
        select(SystemCatalogue).where(
            SystemCatalogue.id == system_id,
            SystemCatalogue.organization_id == user.organization_id,
        )
    )
    system = result.scalar_one_or_none()

    if not system:
        raise HTTPException(status_code=404, detail="System not found")

    count_result = await db.execute(
        select(func.count())
        .select_from(ProcessSystem)
        .where(
            ProcessSystem.system_id == system.id,
            ProcessSystem.organization_id == user.organization_id,
        )
    )
    process_count = count_result.scalar() or 0

    response = SystemCatalogueResponse.model_validate(system)
    response.process_count = process_count
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

    count_result = await db.execute(
        select(func.count())
        .select_from(ProcessSystem)
        .where(
            ProcessSystem.system_id == system.id,
            ProcessSystem.organization_id == user.organization_id,
        )
    )
    process_count = count_result.scalar() or 0

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
