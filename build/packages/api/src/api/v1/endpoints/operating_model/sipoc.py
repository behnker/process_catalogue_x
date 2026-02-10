"""SIPOC CRUD endpoints — relational rows in process_sipoc."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.process import Process
from src.models.operating_model import ProcessSipoc
from src.schemas.sipoc import (
    ProcessSipocCreate,
    ProcessSipocResponse,
    ProcessSipocUpdate,
)

router = APIRouter()

VALID_ELEMENTS = {"supplier", "input", "output", "customer"}


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
    "/{process_id}/operating-model/sipoc",
    response_model=list[ProcessSipocResponse],
)
async def list_sipoc(
    process_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List all SIPOC elements for a process."""
    result = await db.execute(
        select(ProcessSipoc)
        .where(
            ProcessSipoc.process_id == process_id,
            ProcessSipoc.organization_id == user.organization_id,
        )
        .order_by(ProcessSipoc.element_type, ProcessSipoc.sort_order)
    )
    return [ProcessSipocResponse.model_validate(r) for r in result.scalars().all()]


@router.post(
    "/{process_id}/operating-model/sipoc",
    response_model=ProcessSipocResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_sipoc(
    process_id: str,
    body: ProcessSipocCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a SIPOC element for a process."""
    if body.element_type not in VALID_ELEMENTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid element_type. Must be one of: {', '.join(sorted(VALID_ELEMENTS))}",
        )
    await _verify_process(process_id, user, db)

    row = ProcessSipoc(
        id=str(uuid4()),
        organization_id=user.organization_id,
        process_id=process_id,
        **body.model_dump(),
    )
    db.add(row)
    await db.flush()
    await db.refresh(row)
    return ProcessSipocResponse.model_validate(row)


@router.patch(
    "/{process_id}/operating-model/sipoc/{item_id}",
    response_model=ProcessSipocResponse,
)
async def update_sipoc(
    process_id: str,
    item_id: str,
    body: ProcessSipocUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a SIPOC element."""
    if body.element_type and body.element_type not in VALID_ELEMENTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid element_type. Must be one of: {', '.join(sorted(VALID_ELEMENTS))}",
        )
    result = await db.execute(
        select(ProcessSipoc).where(
            ProcessSipoc.id == item_id,
            ProcessSipoc.process_id == process_id,
            ProcessSipoc.organization_id == user.organization_id,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="SIPOC element not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(row, field, value)
    await db.flush()
    await db.refresh(row)
    return ProcessSipocResponse.model_validate(row)


@router.delete(
    "/{process_id}/operating-model/sipoc/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_sipoc(
    process_id: str,
    item_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a SIPOC element."""
    result = await db.execute(
        select(ProcessSipoc).where(
            ProcessSipoc.id == item_id,
            ProcessSipoc.process_id == process_id,
            ProcessSipoc.organization_id == user.organization_id,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="SIPOC element not found")
    await db.delete(row)
    await db.flush()
