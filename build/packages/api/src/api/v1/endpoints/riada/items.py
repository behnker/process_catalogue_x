"""RIADA item CRUD endpoints."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.riada import RiadaItem
from src.schemas.riada import (
    RiadaCreate,
    RiadaResponse,
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
