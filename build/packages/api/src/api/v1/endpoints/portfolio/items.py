"""Portfolio item CRUD endpoints."""

from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.portfolio import PortfolioItem
from src.schemas.portfolio import (
    PortfolioItemCreate,
    PortfolioItemResponse,
    PortfolioItemUpdate,
    PortfolioListResponse,
)

router = APIRouter()


@router.get("/", response_model=PortfolioListResponse)
async def list_portfolio_items(
    level: Optional[str] = Query(None),
    portfolio_status: Optional[str] = Query(None, alias="status"),
    parent_id: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List portfolio items with filtering."""
    query = select(PortfolioItem).where(
        PortfolioItem.organization_id == user.organization_id
    )

    if level:
        query = query.where(PortfolioItem.level == level)
    if portfolio_status:
        query = query.where(PortfolioItem.status == portfolio_status)
    if parent_id:
        query = query.where(PortfolioItem.parent_id == parent_id)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(PortfolioItem.sort_order)
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    items = result.scalars().all()

    return PortfolioListResponse(
        items=[PortfolioItemResponse.model_validate(i) for i in items],
        total=total,
    )


@router.post("/", response_model=PortfolioItemResponse, status_code=status.HTTP_201_CREATED)
async def create_portfolio_item(
    body: PortfolioItemCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new portfolio item."""
    # Calculate WSVF score
    wsvf_score = None
    if body.business_value and body.time_criticality and body.risk_reduction and body.job_size:
        wsvf_score = (body.business_value + body.time_criticality + body.risk_reduction) / body.job_size

    item = PortfolioItem(
        id=str(uuid4()),
        organization_id=user.organization_id,
        wsvf_score=wsvf_score,
        **body.model_dump(),
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)

    return PortfolioItemResponse.model_validate(item)


@router.get("/{item_id}", response_model=PortfolioItemResponse)
async def get_portfolio_item(
    item_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get a single portfolio item."""
    result = await db.execute(
        select(PortfolioItem).where(
            PortfolioItem.id == item_id,
            PortfolioItem.organization_id == user.organization_id,
        )
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")

    return PortfolioItemResponse.model_validate(item)


@router.patch("/{item_id}", response_model=PortfolioItemResponse)
async def update_portfolio_item(
    item_id: str,
    body: PortfolioItemUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a portfolio item."""
    result = await db.execute(
        select(PortfolioItem).where(
            PortfolioItem.id == item_id,
            PortfolioItem.organization_id == user.organization_id,
        )
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    # Recalculate WSVF score
    if item.business_value and item.time_criticality and item.risk_reduction and item.job_size:
        item.wsvf_score = (item.business_value + item.time_criticality + item.risk_reduction) / item.job_size

    await db.flush()
    await db.refresh(item)

    return PortfolioItemResponse.model_validate(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_portfolio_item(
    item_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a portfolio item (sets status to cancelled)."""
    result = await db.execute(
        select(PortfolioItem).where(
            PortfolioItem.id == item_id,
            PortfolioItem.organization_id == user.organization_id,
        )
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")

    item.status = "cancelled"
    await db.flush()
