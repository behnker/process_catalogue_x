"""Process-System linkage endpoints."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.process import Process
from src.models.system_catalogue import ProcessSystem, SystemCatalogue
from src.schemas.system_catalogue import (
    ProcessBrief,
    ProcessSystemResponse,
    ProcessSystemsResponse,
    SystemBrief,
    SystemProcessCreate,
)

router = APIRouter()


@router.get("/{system_id}/processes", response_model=ProcessSystemsResponse)
async def get_system_processes(
    system_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get all processes linked to a system."""
    # Verify system exists
    sys_result = await db.execute(
        select(SystemCatalogue).where(
            SystemCatalogue.id == system_id,
            SystemCatalogue.organization_id == user.organization_id,
        )
    )
    if not sys_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="System not found")

    result = await db.execute(
        select(ProcessSystem)
        .options(selectinload(ProcessSystem.process), selectinload(ProcessSystem.system))
        .where(
            ProcessSystem.system_id == system_id,
            ProcessSystem.organization_id == user.organization_id,
        )
    )
    links = result.scalars().all()

    items = []
    for link in links:
        response = ProcessSystemResponse.model_validate(link)
        if link.process:
            response.process = ProcessBrief.model_validate(link.process)
        if link.system:
            response.system = SystemBrief.model_validate(link.system)
        items.append(response)

    return ProcessSystemsResponse(items=items, total=len(items))


@router.post(
    "/{system_id}/processes",
    response_model=ProcessSystemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def link_process_to_system(
    system_id: str,
    body: SystemProcessCreate,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Link a process to a system (from system side)."""
    # Verify system exists
    sys_result = await db.execute(
        select(SystemCatalogue).where(
            SystemCatalogue.id == system_id,
            SystemCatalogue.organization_id == user.organization_id,
        )
    )
    system = sys_result.scalar_one_or_none()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")

    # Verify process exists
    proc_result = await db.execute(
        select(Process).where(
            Process.id == body.process_id,
            Process.organization_id == user.organization_id,
        )
    )
    process = proc_result.scalar_one_or_none()
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    # Check for existing link
    existing = await db.execute(
        select(ProcessSystem).where(
            ProcessSystem.organization_id == user.organization_id,
            ProcessSystem.process_id == body.process_id,
            ProcessSystem.system_id == system_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Link already exists")

    link = ProcessSystem(
        id=str(uuid4()),
        organization_id=user.organization_id,
        process_id=body.process_id,
        system_id=system_id,
        purpose=body.purpose,
        system_role=body.system_role,
        integration_method=body.integration_method,
        criticality=body.criticality,
        user_scope=body.user_scope,
        pain_points=body.pain_points,
        automation_potential=body.automation_potential,
        status=body.status,
    )
    db.add(link)
    await db.flush()
    await db.refresh(link)

    response = ProcessSystemResponse.model_validate(link)
    response.process = ProcessBrief.model_validate(process)
    response.system = SystemBrief.model_validate(system)
    return response


@router.delete("/{system_id}/processes/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_system_process_link(
    system_id: str,
    link_id: str,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Remove a process-system link."""
    result = await db.execute(
        select(ProcessSystem).where(
            ProcessSystem.id == link_id,
            ProcessSystem.system_id == system_id,
            ProcessSystem.organization_id == user.organization_id,
        )
    )
    link = result.scalar_one_or_none()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    await db.delete(link)
    await db.flush()
