"""Process CRUD endpoints."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.process import Process
from src.schemas.process import (
    ProcessCreate,
    ProcessDetailResponse,
    ProcessResponse,
    ProcessUpdate,
)
from src.services.process_numbering import (
    generate_process_code,
    get_next_sort_order,
    renumber_siblings,
)

router = APIRouter()


@router.get("/{process_id}", response_model=ProcessDetailResponse)
async def get_process(
    process_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get a single process with operating model components."""
    result = await db.execute(
        select(Process).where(
            Process.id == process_id,
            Process.organization_id == user.organization_id,
        )
    )
    process = result.scalar_one_or_none()

    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    return ProcessDetailResponse.model_validate(process)


@router.post("/", response_model=ProcessResponse, status_code=status.HTTP_201_CREATED)
async def create_process(
    body: ProcessCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new process with auto-generated hierarchical code."""
    # Determine sort_order if not provided
    sort_order = body.sort_order
    if sort_order is None:
        sort_order = await get_next_sort_order(db, user.organization_id, body.parent_id)

    # Auto-generate hierarchical code
    code = await generate_process_code(
        db, user.organization_id, body.parent_id, sort_order
    )

    # Create process with generated code
    process_data = body.model_dump(exclude={"sort_order"})
    process = Process(
        id=str(uuid4()),
        organization_id=user.organization_id,
        code=code,
        sort_order=sort_order,
        **process_data,
    )
    db.add(process)
    await db.flush()
    await db.refresh(process)

    return ProcessResponse.model_validate(process)


@router.patch("/{process_id}", response_model=ProcessResponse)
async def update_process(
    process_id: str,
    body: ProcessUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update an existing process."""
    result = await db.execute(
        select(Process).where(
            Process.id == process_id,
            Process.organization_id == user.organization_id,
        )
    )
    process = result.scalar_one_or_none()

    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(process, field, value)

    await db.flush()
    await db.refresh(process)

    return ProcessResponse.model_validate(process)


@router.delete("/{process_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_process(
    process_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a process (soft delete by setting status to archived)."""
    result = await db.execute(
        select(Process).where(
            Process.id == process_id,
            Process.organization_id == user.organization_id,
        )
    )
    process = result.scalar_one_or_none()

    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    process.status = "archived"
    await db.flush()

    # Renumber remaining siblings to close gaps
    await renumber_siblings(db, user.organization_id, process.parent_id)
