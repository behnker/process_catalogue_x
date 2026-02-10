"""Policy CRUD endpoints — relational rows in process_policy."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.process import Process
from src.models.operating_model import ProcessPolicy
from src.schemas.policy import (
    ProcessPolicyCreate,
    ProcessPolicyResponse,
    ProcessPolicyUpdate,
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
    "/{process_id}/operating-model/policies",
    response_model=list[ProcessPolicyResponse],
)
async def list_policies(
    process_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List all policies for a process."""
    result = await db.execute(
        select(ProcessPolicy).where(
            ProcessPolicy.process_id == process_id,
            ProcessPolicy.organization_id == user.organization_id,
        )
    )
    return [ProcessPolicyResponse.model_validate(r) for r in result.scalars().all()]


@router.post(
    "/{process_id}/operating-model/policies",
    response_model=ProcessPolicyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_policy(
    process_id: str,
    body: ProcessPolicyCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a policy for a process."""
    await _verify_process(process_id, user, db)

    row = ProcessPolicy(
        id=str(uuid4()),
        organization_id=user.organization_id,
        process_id=process_id,
        **body.model_dump(),
    )
    db.add(row)
    await db.flush()
    await db.refresh(row)
    return ProcessPolicyResponse.model_validate(row)


@router.patch(
    "/{process_id}/operating-model/policies/{item_id}",
    response_model=ProcessPolicyResponse,
)
async def update_policy(
    process_id: str,
    item_id: str,
    body: ProcessPolicyUpdate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a policy."""
    result = await db.execute(
        select(ProcessPolicy).where(
            ProcessPolicy.id == item_id,
            ProcessPolicy.process_id == process_id,
            ProcessPolicy.organization_id == user.organization_id,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Policy not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(row, field, value)
    await db.flush()
    await db.refresh(row)
    return ProcessPolicyResponse.model_validate(row)


@router.delete(
    "/{process_id}/operating-model/policies/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_policy(
    process_id: str,
    item_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a policy."""
    result = await db.execute(
        select(ProcessPolicy).where(
            ProcessPolicy.id == item_id,
            ProcessPolicy.process_id == process_id,
            ProcessPolicy.organization_id == user.organization_id,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Policy not found")
    await db.delete(row)
    await db.flush()
