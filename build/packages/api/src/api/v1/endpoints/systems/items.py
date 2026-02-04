"""System Catalogue read endpoints (list, get)."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.system_catalogue import ProcessSystem, SystemCatalogue
from src.schemas.system_catalogue import (
    SystemCatalogueListResponse,
    SystemCatalogueResponse,
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

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    offset = (page - 1) * per_page
    query = query.order_by(SystemCatalogue.name).offset(offset).limit(per_page)
    result = await db.execute(query)
    systems = result.scalars().all()

    items = []
    for sys in systems:
        process_count = await _get_process_count(db, sys.id, user.organization_id)
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

    process_count = await _get_process_count(db, system.id, user.organization_id)
    response = SystemCatalogueResponse.model_validate(system)
    response.process_count = process_count
    return response
