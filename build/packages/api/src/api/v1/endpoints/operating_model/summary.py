"""Operating model list and summary endpoints.

Queries both JSONB components (resources, security, data) and
relational tables (raci, kpis, governance, policies, timing, sipoc)
to produce unified summary. Systems counted via process_system table.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.process import Process, ProcessOperatingModel
from src.models.operating_model import (
    ProcessGovernance,
    ProcessKpi,
    ProcessPolicy,
    ProcessRaci,
    ProcessSipoc,
    ProcessTiming,
)
from src.models.system_catalogue import ProcessSystem
from src.schemas.operating_model import (
    OperatingModelComponentResponse,
    OperatingModelSummary,
)

router = APIRouter()

# All 10 component types
ALL_COMPONENTS = {
    "sipoc", "raci", "kpis", "systems", "policies",
    "timing", "governance", "security", "data", "resources",
}

# Relational model → component type mapping
RELATIONAL_MODELS = {
    "raci": ProcessRaci,
    "kpis": ProcessKpi,
    "governance": ProcessGovernance,
    "policies": ProcessPolicy,
    "timing": ProcessTiming,
    "sipoc": ProcessSipoc,
}


@router.get("/{process_id}/operating-model", response_model=list[OperatingModelComponentResponse])
async def list_operating_model(
    process_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get all JSONB operating model components for a process."""
    result = await db.execute(
        select(Process).where(
            Process.id == process_id,
            Process.organization_id == user.organization_id,
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Process not found")

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
    """Get summary of operating model completeness — relational + JSONB."""
    org_id = user.organization_id

    # 1. JSONB components (resources, security, data, plus legacy governance/raci/etc if still present)
    result = await db.execute(
        select(ProcessOperatingModel).where(
            ProcessOperatingModel.process_id == process_id,
            ProcessOperatingModel.organization_id == org_id,
        )
    )
    jsonb_components = result.scalars().all()
    jsonb_defined = {c.component_type for c in jsonb_components}

    # Gaps from JSONB components
    gaps = []
    for c in jsonb_components:
        if c.future_state and c.current_state != c.future_state:
            gaps.append(c.component_type)

    # 2. Relational components — check for >=1 row each
    defined_components: set[str] = set()
    for comp_type, model in RELATIONAL_MODELS.items():
        result = await db.execute(
            select(func.count()).where(
                model.process_id == process_id,
                model.organization_id == org_id,
            )
        )
        if result.scalar() > 0:
            defined_components.add(comp_type)

    # 3. Systems — via process_system junction
    result = await db.execute(
        select(func.count()).where(
            ProcessSystem.process_id == process_id,
            ProcessSystem.organization_id == org_id,
        )
    )
    if result.scalar() > 0:
        defined_components.add("systems")

    # 4. Merge JSONB-only defined (resources, security, data)
    for comp_type in jsonb_defined:
        if comp_type in {"resources", "security", "data"}:
            defined_components.add(comp_type)

    missing = ALL_COMPONENTS - defined_components

    return OperatingModelSummary(
        process_id=process_id,
        total_components=len(ALL_COMPONENTS),
        defined_components=sorted(defined_components),
        missing_components=sorted(missing),
        components_with_gaps=gaps,
        completion_percentage=round(len(defined_components) / len(ALL_COMPONENTS) * 100),
    )
