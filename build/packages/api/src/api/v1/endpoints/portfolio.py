"""
Portfolio API endpoints.
Full CRUD with hierarchy, WSVF scoring, and milestones.

Blueprint §4.5: 7-level hierarchy (Strategy → Epic → Task)
Blueprint §4.5.2: WSVF prioritization
Blueprint §4.5.4: Milestones, budget tracking
"""

from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.portfolio import PortfolioItem, PortfolioMilestone
from src.schemas.portfolio import (
    MilestoneCreate,
    MilestoneResponse,
    MilestoneUpdate,
    PortfolioItemCreate,
    PortfolioItemResponse,
    PortfolioItemUpdate,
    PortfolioListResponse,
    PortfolioTreeNode,
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


@router.get("/tree", response_model=list[PortfolioTreeNode])
async def get_portfolio_tree(
    root_level: str = Query("strategy", description="Starting level for tree"),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get portfolio hierarchy as a tree structure."""
    result = await db.execute(
        select(PortfolioItem)
        .where(PortfolioItem.organization_id == user.organization_id)
        .order_by(PortfolioItem.level, PortfolioItem.sort_order)
    )
    all_items = result.scalars().all()

    def build_children(parent_id: str) -> list[PortfolioTreeNode]:
        children = []
        for item in all_items:
            if item.parent_id == parent_id:
                node = PortfolioTreeNode(
                    id=item.id,
                    code=item.code,
                    name=item.name,
                    level=item.level,
                    status=item.status,
                    rag_status=item.rag_status,
                    wsvf_score=float(item.wsvf_score) if item.wsvf_score else None,
                    sort_order=item.sort_order,
                    children=build_children(item.id),
                )
                children.append(node)
        return sorted(children, key=lambda x: x.sort_order)

    tree = []
    for item in all_items:
        if item.level == root_level and not item.parent_id:
            node = PortfolioTreeNode(
                id=item.id,
                code=item.code,
                name=item.name,
                level=item.level,
                status=item.status,
                rag_status=item.rag_status,
                wsvf_score=float(item.wsvf_score) if item.wsvf_score else None,
                sort_order=item.sort_order,
                children=build_children(item.id),
            )
            tree.append(node)

    return sorted(tree, key=lambda x: x.sort_order)


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


# ── Milestones ────────────────────────────────────────


@router.get("/{item_id}/milestones", response_model=list[MilestoneResponse])
async def list_milestones(
    item_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get all milestones for a portfolio item."""
    result = await db.execute(
        select(PortfolioMilestone)
        .where(
            PortfolioMilestone.portfolio_item_id == item_id,
            PortfolioMilestone.organization_id == user.organization_id,
        )
        .order_by(PortfolioMilestone.sort_order, PortfolioMilestone.due_date)
    )
    milestones = result.scalars().all()
    return [MilestoneResponse.model_validate(m) for m in milestones]


@router.post(
    "/{item_id}/milestones",
    response_model=MilestoneResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_milestone(
    item_id: str,
    body: MilestoneCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a milestone for a portfolio item."""
    # Verify item exists
    result = await db.execute(
        select(PortfolioItem).where(
            PortfolioItem.id == item_id,
            PortfolioItem.organization_id == user.organization_id,
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Portfolio item not found")

    milestone = PortfolioMilestone(
        id=str(uuid4()),
        organization_id=user.organization_id,
        portfolio_item_id=item_id,
        **body.model_dump(),
    )
    db.add(milestone)
    await db.flush()
    await db.refresh(milestone)

    return MilestoneResponse.model_validate(milestone)


@router.patch("/{item_id}/milestones/{milestone_id}", response_model=MilestoneResponse)
async def update_milestone(
    item_id: str,
    milestone_id: str,
    body: MilestoneUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a milestone."""
    result = await db.execute(
        select(PortfolioMilestone).where(
            PortfolioMilestone.id == milestone_id,
            PortfolioMilestone.portfolio_item_id == item_id,
            PortfolioMilestone.organization_id == user.organization_id,
        )
    )
    milestone = result.scalar_one_or_none()

    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(milestone, field, value)

    await db.flush()
    await db.refresh(milestone)

    return MilestoneResponse.model_validate(milestone)


@router.delete(
    "/{item_id}/milestones/{milestone_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_milestone(
    item_id: str,
    milestone_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a milestone."""
    result = await db.execute(
        select(PortfolioMilestone).where(
            PortfolioMilestone.id == milestone_id,
            PortfolioMilestone.portfolio_item_id == item_id,
            PortfolioMilestone.organization_id == user.organization_id,
        )
    )
    milestone = result.scalar_one_or_none()

    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")

    await db.delete(milestone)
    await db.flush()
