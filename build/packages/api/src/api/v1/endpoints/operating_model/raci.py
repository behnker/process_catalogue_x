"""RACI CRUD endpoints — relational rows in process_raci."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.process import Process
from src.models.operating_model import ProcessRaci
from src.schemas.raci import (
    ProcessRaciCreate,
    ProcessRaciResponse,
    ProcessRaciUpdate,
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
    "/{process_id}/operating-model/raci",
    response_model=list[ProcessRaciResponse],
)
async def list_raci(
    process_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List all RACI entries for a process."""
    result = await db.execute(
        select(ProcessRaci).where(
            ProcessRaci.process_id == process_id,
            ProcessRaci.organization_id == user.organization_id,
        )
    )
    return [ProcessRaciResponse.model_validate(r) for r in result.scalars().all()]


@router.post(
    "/{process_id}/operating-model/raci",
    response_model=ProcessRaciResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_raci(
    process_id: str,
    body: ProcessRaciCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a RACI entry for a process."""
    await _verify_process(process_id, user, db)

    row = ProcessRaci(
        id=str(uuid4()),
        organization_id=user.organization_id,
        process_id=process_id,
        **body.model_dump(),
    )
    db.add(row)
    await db.flush()
    await db.refresh(row)
    return ProcessRaciResponse.model_validate(row)


@router.patch(
    "/{process_id}/operating-model/raci/{item_id}",
    response_model=ProcessRaciResponse,
)
async def update_raci(
    process_id: str,
    item_id: str,
    body: ProcessRaciUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a RACI entry."""
    result = await db.execute(
        select(ProcessRaci).where(
            ProcessRaci.id == item_id,
            ProcessRaci.process_id == process_id,
            ProcessRaci.organization_id == user.organization_id,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="RACI entry not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(row, field, value)
    await db.flush()
    await db.refresh(row)
    return ProcessRaciResponse.model_validate(row)


@router.delete(
    "/{process_id}/operating-model/raci/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_raci(
    process_id: str,
    item_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a RACI entry."""
    result = await db.execute(
        select(ProcessRaci).where(
            ProcessRaci.id == item_id,
            ProcessRaci.process_id == process_id,
            ProcessRaci.organization_id == user.organization_id,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="RACI entry not found")
    await db.delete(row)
    await db.flush()
