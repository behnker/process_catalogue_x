"""Portfolio milestone CRUD endpoints."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.portfolio import PortfolioItem, PortfolioMilestone
from src.schemas.portfolio import (
    MilestoneCreate,
    MilestoneResponse,
    MilestoneUpdate,
)

router = APIRouter()


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
