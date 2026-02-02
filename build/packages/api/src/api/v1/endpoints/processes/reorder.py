"""Process reordering and code regeneration endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.process import Process
from src.schemas.process import ProcessReorder, ProcessResponse
from src.services.process_numbering import (
    calculate_level_from_parent,
    renumber_all_processes,
    renumber_siblings,
    renumber_subtree,
)

router = APIRouter()


@router.post("/reorder", response_model=ProcessResponse)
async def reorder_process(
    body: ProcessReorder,
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Move a process to a new position or parent with auto-renumbering."""
    result = await db.execute(
        select(Process).where(
            Process.id == body.process_id,
            Process.organization_id == user.organization_id,
        )
    )
    process = result.scalar_one_or_none()

    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    old_parent_id = process.parent_id
    is_reparenting = body.new_parent_id is not None and body.new_parent_id != old_parent_id

    # If reparenting, validate and update parent
    if is_reparenting:
        # Validate new parent exists
        if body.new_parent_id:
            parent_result = await db.execute(
                select(Process).where(
                    Process.id == body.new_parent_id,
                    Process.organization_id == user.organization_id,
                )
            )
            new_parent = parent_result.scalar_one_or_none()
            if not new_parent:
                raise HTTPException(status_code=400, detail="New parent process not found")

            # Update level based on new parent
            process.level = calculate_level_from_parent(new_parent.level)
        else:
            # Moving to root
            process.level = "L0"

        process.parent_id = body.new_parent_id

    # Update sort_order
    process.sort_order = body.new_sort_order
    await db.flush()

    # Renumber old siblings (close gap where process was removed)
    updated_ids = await renumber_siblings(db, user.organization_id, old_parent_id)

    # If reparenting, also renumber new siblings
    if is_reparenting:
        updated_ids.extend(
            await renumber_siblings(db, user.organization_id, body.new_parent_id)
        )

    # Cascade code changes to children if this process's code changed
    await renumber_subtree(db, user.organization_id, process.id)

    await db.refresh(process)
    return ProcessResponse.model_validate(process)


@router.post("/regenerate-codes")
async def regenerate_process_codes(
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Regenerate all process codes with hierarchical numbering (1, 1.1, 1.1.1, etc.)."""
    count = await renumber_all_processes(db, user.organization_id)
    await db.commit()
    return {"message": f"Regenerated codes for {count} processes"}
