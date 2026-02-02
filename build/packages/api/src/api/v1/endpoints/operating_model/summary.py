"""Operating model list and summary endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.process import Process, ProcessOperatingModel
from src.schemas.operating_model import (
    OperatingModelComponentResponse,
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
