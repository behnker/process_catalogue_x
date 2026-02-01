"""
Business Model API endpoints.
"""

from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.business_model import BusinessModel, BusinessModelEntry
from src.schemas.common import (
    BusinessModelCanvasResponse,
    BusinessModelEntryCreate,
    BusinessModelEntryResponse,
)

router = APIRouter()


@router.get("/canvas", response_model=BusinessModelCanvasResponse)
async def get_business_model_canvas(
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Get the Business Model Canvas with all 9 component groups.
    Returns entries grouped by component for the canvas view.
    """
    result = await db.execute(
        select(BusinessModel).where(
            BusinessModel.organization_id == user.organization_id,
            BusinessModel.status == "active",
        )
    )
    bm = result.scalar_one_or_none()

    if not bm:
        # Create default canvas
        bm = BusinessModel(
            id=str(uuid4()),
            organization_id=user.organization_id,
            name="Business Model",
        )
        db.add(bm)
        await db.flush()

    # Get entries
    result = await db.execute(
        select(BusinessModelEntry)
        .where(BusinessModelEntry.business_model_id == bm.id)
        .order_by(BusinessModelEntry.sort_order)
    )
    entries = result.scalars().all()

    # Group by component
    components = [
        "key_partners", "key_activities", "key_resources",
        "value_propositions", "customer_relationships", "channels",
        "customer_segments", "cost_structure", "revenue_streams",
    ]
    grouped = {c: [] for c in components}
    for entry in entries:
        if entry.component in grouped:
            grouped[entry.component].append(
                BusinessModelEntryResponse.model_validate(entry)
            )

    return BusinessModelCanvasResponse(
        id=bm.id,
        name=bm.name,
        entries_by_component=grouped,
    )


@router.post("/entries", response_model=BusinessModelEntryResponse, status_code=201)
async def create_entry(
    body: BusinessModelEntryCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Add an entry to a BMC component."""
    # Get active BM
    result = await db.execute(
        select(BusinessModel).where(
            BusinessModel.organization_id == user.organization_id,
            BusinessModel.status == "active",
        )
    )
    bm = result.scalar_one_or_none()
    if not bm:
        raise HTTPException(status_code=404, detail="No active business model")

    entry = BusinessModelEntry(
        id=str(uuid4()),
        organization_id=user.organization_id,
        business_model_id=bm.id,
        **body.model_dump(),
    )
    db.add(entry)
    await db.flush()
    await db.refresh(entry)

    return BusinessModelEntryResponse.model_validate(entry)


@router.delete("/entries/{entry_id}", status_code=204)
async def delete_entry(
    entry_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a BMC entry."""
    result = await db.execute(
        select(BusinessModelEntry).where(
            BusinessModelEntry.id == entry_id,
            BusinessModelEntry.organization_id == user.organization_id,
        )
    )
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    await db.delete(entry)
    await db.flush()
