"""KPI CRUD endpoints — relational rows in process_kpi."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.process import Process
from src.models.operating_model import ProcessKpi
from src.schemas.kpi import (
    ProcessKpiCreate,
    ProcessKpiResponse,
    ProcessKpiUpdate,
)

router = APIRouter()


async def _verify_process(
    process_id: str, user: CurrentUser, db: AsyncSession
) -> None:
    result = await db.execute(
        select(Process).where(
            Process.id == process_id,
            Process.organization_id == user.organization_id,
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Process not found")


@router.get(
    "/{process_id}/operating-model/kpis",
    response_model=list[ProcessKpiResponse],
)
async def list_kpis(
    process_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List all KPIs for a process."""
    result = await db.execute(
        select(ProcessKpi).where(
            ProcessKpi.process_id == process_id,
            ProcessKpi.organization_id == user.organization_id,
        )
    )
    return [ProcessKpiResponse.model_validate(r) for r in result.scalars().all()]


@router.post(
    "/{process_id}/operating-model/kpis",
    response_model=ProcessKpiResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_kpi(
    process_id: str,
    body: ProcessKpiCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a KPI for a process."""
    await _verify_process(process_id, user, db)

    row = ProcessKpi(
        id=str(uuid4()),
        organization_id=user.organization_id,
        process_id=process_id,
        **body.model_dump(),
    )
    db.add(row)
    await db.flush()
    await db.refresh(row)
    return ProcessKpiResponse.model_validate(row)


@router.patch(
    "/{process_id}/operating-model/kpis/{item_id}",
    response_model=ProcessKpiResponse,
)
async def update_kpi(
    process_id: str,
    item_id: str,
    body: ProcessKpiUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a KPI."""
    result = await db.execute(
        select(ProcessKpi).where(
            ProcessKpi.id == item_id,
            ProcessKpi.process_id == process_id,
            ProcessKpi.organization_id == user.organization_id,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="KPI not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(row, field, value)
    await db.flush()
    await db.refresh(row)
    return ProcessKpiResponse.model_validate(row)


@router.delete(
    "/{process_id}/operating-model/kpis/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_kpi(
    process_id: str,
    item_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a KPI."""
    result = await db.execute(
        select(ProcessKpi).where(
            ProcessKpi.id == item_id,
            ProcessKpi.process_id == process_id,
            ProcessKpi.organization_id == user.organization_id,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="KPI not found")
    await db.delete(row)
    await db.flush()
