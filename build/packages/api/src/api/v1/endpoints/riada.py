"""
RIADA (Quality Logs) API endpoints.
Full CRUD with filtering by type, category, severity, status.
"""

from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.riada import RiadaItem
from src.schemas.riada import (
    RiadaCreate,
    RiadaListResponse,
    RiadaResponse,
    RiadaSummary,
    RiadaUpdate,
)

router = APIRouter()


def _generate_riada_code(riada_type: str, sequence: int) -> str:
    """Generate a RIADA code like RSK-001, ISS-001, ACT-001."""
    prefix_map = {
        "risk": "RSK",
        "issue": "ISS",
        "action": "ACT",
        "dependency": "DEP",
        "assumption": "ASM",
    }
    prefix = prefix_map.get(riada_type, "RDA")
    return f"{prefix}-{sequence:03d}"


@router.get("/", response_model=RiadaListResponse)
async def list_riada_items(
    riada_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    riada_status: Optional[str] = Query(None, alias="status"),
    process_id: Optional[str] = Query(None),
    portfolio_item_id: Optional[str] = Query(None),
    assigned_to_id: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List RIADA items with comprehensive filtering."""
    query = select(RiadaItem).where(
        RiadaItem.organization_id == user.organization_id
    )

    if riada_type:
        query = query.where(RiadaItem.riada_type == riada_type)
    if category:
        query = query.where(RiadaItem.category == category)
    if severity:
        query = query.where(RiadaItem.severity == severity)
    if riada_status:
        query = query.where(RiadaItem.status == riada_status)
    if process_id:
        query = query.where(RiadaItem.process_id == process_id)
    if portfolio_item_id:
        query = query.where(RiadaItem.portfolio_item_id == portfolio_item_id)
    if assigned_to_id:
        query = query.where(RiadaItem.assigned_to_id == assigned_to_id)
    if search:
        query = query.where(
            RiadaItem.title.ilike(f"%{search}%")
            | RiadaItem.description.ilike(f"%{search}%")
        )

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(RiadaItem.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    items = result.scalars().all()

    return RiadaListResponse(
        items=[RiadaResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/summary", response_model=RiadaSummary)
async def get_riada_summary(
    process_id: Optional[str] = Query(None),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get aggregated RIADA summary for dashboards and heatmaps."""
    base_query = select(RiadaItem).where(
        RiadaItem.organization_id == user.organization_id
    )
    if process_id:
        base_query = base_query.where(RiadaItem.process_id == process_id)

    result = await db.execute(base_query)
    items = result.scalars().all()

    summary = RiadaSummary(total=len(items))
    for item in items:
        summary.by_type[item.riada_type] = summary.by_type.get(item.riada_type, 0) + 1
        summary.by_severity[item.severity] = summary.by_severity.get(item.severity, 0) + 1
        summary.by_status[item.status] = summary.by_status.get(item.status, 0) + 1
        summary.by_category[item.category] = summary.by_category.get(item.category, 0) + 1

    return summary


@router.get("/{riada_id}", response_model=RiadaResponse)
async def get_riada_item(
    riada_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get a single RIADA item."""
    result = await db.execute(
        select(RiadaItem).where(
            RiadaItem.id == riada_id,
            RiadaItem.organization_id == user.organization_id,
        )
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="RIADA item not found")

    return RiadaResponse.model_validate(item)


@router.post("/", response_model=RiadaResponse, status_code=status.HTTP_201_CREATED)
async def create_riada_item(
    body: RiadaCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new RIADA item."""
    # Generate sequential code
    count_result = await db.execute(
        select(func.count())
        .select_from(RiadaItem)
        .where(
            RiadaItem.organization_id == user.organization_id,
            RiadaItem.riada_type == body.riada_type,
        )
    )
    sequence = (count_result.scalar() or 0) + 1
    code = _generate_riada_code(body.riada_type, sequence)

    # Calculate risk score if applicable
    risk_score = None
    if body.probability and body.impact:
        risk_score = body.probability * body.impact

    item = RiadaItem(
        id=str(uuid4()),
        organization_id=user.organization_id,
        code=code,
        raised_by_id=user.id,
        risk_score=risk_score,
        **body.model_dump(),
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)

    return RiadaResponse.model_validate(item)


@router.patch("/{riada_id}", response_model=RiadaResponse)
async def update_riada_item(
    riada_id: str,
    body: RiadaUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a RIADA item."""
    result = await db.execute(
        select(RiadaItem).where(
            RiadaItem.id == riada_id,
            RiadaItem.organization_id == user.organization_id,
        )
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="RIADA item not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    # Recalculate risk score
    if item.probability and item.impact:
        item.risk_score = item.probability * item.impact

    await db.flush()
    await db.refresh(item)

    return RiadaResponse.model_validate(item)


@router.delete("/{riada_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_riada_item(
    riada_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a RIADA item."""
    result = await db.execute(
        select(RiadaItem).where(
            RiadaItem.id == riada_id,
            RiadaItem.organization_id == user.organization_id,
        )
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="RIADA item not found")

    await db.delete(item)
    await db.flush()
