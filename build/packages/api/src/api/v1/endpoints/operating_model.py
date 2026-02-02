"""
Operating Model API endpoints.
Manages ProcessOperatingModel components per process.

Blueprint §4.4.1: 10 components (SIPOC, RACI, KPIs, Policies, Systems, etc.)
Each component stores Current State and Future State for gap analysis.
"""

from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.process import Process, ProcessOperatingModel
from src.schemas.operating_model import (
    OperatingModelComponentCreate,
    OperatingModelComponentResponse,
    OperatingModelComponentUpdate,
    OperatingModelSummary,
)

router = APIRouter()

# Valid component types per Blueprint §4.4.1
VALID_COMPONENTS = {
    "sipoc",
    "raci",
    "kpis",
    "systems",
    "policies",
    "timing",
    "governance",
    "security",
    "data",
    "resources",
}


@router.get("/{process_id}/operating-model", response_model=list[OperatingModelComponentResponse])
async def list_operating_model(
    process_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get all operating model components for a process."""
    # Verify process exists and belongs to tenant
    result = await db.execute(
        select(Process).where(
            Process.id == process_id,
            Process.organization_id == user.organization_id,
        )
    )
    process = result.scalar_one_or_none()
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    # Get all components
    result = await db.execute(
        select(ProcessOperatingModel).where(
            ProcessOperatingModel.process_id == process_id,
            ProcessOperatingModel.organization_id == user.organization_id,
        )
    )
    components = result.scalars().all()

    return [OperatingModelComponentResponse.model_validate(c) for c in components]


@router.get("/{process_id}/operating-model/summary", response_model=OperatingModelSummary)
async def get_operating_model_summary(
    process_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get summary of operating model completeness and gaps."""
    result = await db.execute(
        select(ProcessOperatingModel).where(
            ProcessOperatingModel.process_id == process_id,
            ProcessOperatingModel.organization_id == user.organization_id,
        )
    )
    components = result.scalars().all()

    defined_components = {c.component_type for c in components}
    missing_components = VALID_COMPONENTS - defined_components

    # Count components with gaps (future_state differs from current_state)
    gaps = []
    for c in components:
        if c.future_state and c.current_state != c.future_state:
            gaps.append(c.component_type)

    return OperatingModelSummary(
        process_id=process_id,
        total_components=len(VALID_COMPONENTS),
        defined_components=list(defined_components),
        missing_components=list(missing_components),
        components_with_gaps=gaps,
        completion_percentage=round(len(defined_components) / len(VALID_COMPONENTS) * 100),
    )


@router.get(
    "/{process_id}/operating-model/{component_type}",
    response_model=OperatingModelComponentResponse,
)
async def get_operating_model_component(
    process_id: str,
    component_type: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get a specific operating model component."""
    if component_type not in VALID_COMPONENTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid component type. Must be one of: {', '.join(VALID_COMPONENTS)}",
        )

    result = await db.execute(
        select(ProcessOperatingModel).where(
            ProcessOperatingModel.process_id == process_id,
            ProcessOperatingModel.component_type == component_type,
            ProcessOperatingModel.organization_id == user.organization_id,
        )
    )
    component = result.scalar_one_or_none()

    if not component:
        raise HTTPException(status_code=404, detail=f"Component '{component_type}' not found")

    return OperatingModelComponentResponse.model_validate(component)


@router.post(
    "/{process_id}/operating-model",
    response_model=OperatingModelComponentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_operating_model_component(
    process_id: str,
    body: OperatingModelComponentCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new operating model component for a process."""
    if body.component_type not in VALID_COMPONENTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid component type. Must be one of: {', '.join(VALID_COMPONENTS)}",
        )

    # Verify process exists
    result = await db.execute(
        select(Process).where(
            Process.id == process_id,
            Process.organization_id == user.organization_id,
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Process not found")

    # Check if component already exists
    result = await db.execute(
        select(ProcessOperatingModel).where(
            ProcessOperatingModel.process_id == process_id,
            ProcessOperatingModel.component_type == body.component_type,
            ProcessOperatingModel.organization_id == user.organization_id,
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail=f"Component '{body.component_type}' already exists for this process",
        )

    component = ProcessOperatingModel(
        id=str(uuid4()),
        organization_id=user.organization_id,
        process_id=process_id,
        **body.model_dump(),
    )
    db.add(component)
    await db.flush()
    await db.refresh(component)

    return OperatingModelComponentResponse.model_validate(component)


@router.patch(
    "/{process_id}/operating-model/{component_type}",
    response_model=OperatingModelComponentResponse,
)
async def update_operating_model_component(
    process_id: str,
    component_type: str,
    body: OperatingModelComponentUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update an operating model component."""
    if component_type not in VALID_COMPONENTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid component type. Must be one of: {', '.join(VALID_COMPONENTS)}",
        )

    result = await db.execute(
        select(ProcessOperatingModel).where(
            ProcessOperatingModel.process_id == process_id,
            ProcessOperatingModel.component_type == component_type,
            ProcessOperatingModel.organization_id == user.organization_id,
        )
    )
    component = result.scalar_one_or_none()

    if not component:
        raise HTTPException(status_code=404, detail=f"Component '{component_type}' not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(component, field, value)

    await db.flush()
    await db.refresh(component)

    return OperatingModelComponentResponse.model_validate(component)


@router.delete(
    "/{process_id}/operating-model/{component_type}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_operating_model_component(
    process_id: str,
    component_type: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete an operating model component."""
    result = await db.execute(
        select(ProcessOperatingModel).where(
            ProcessOperatingModel.process_id == process_id,
            ProcessOperatingModel.component_type == component_type,
            ProcessOperatingModel.organization_id == user.organization_id,
        )
    )
    component = result.scalar_one_or_none()

    if not component:
        raise HTTPException(status_code=404, detail=f"Component '{component_type}' not found")

    await db.delete(component)
    await db.flush()
