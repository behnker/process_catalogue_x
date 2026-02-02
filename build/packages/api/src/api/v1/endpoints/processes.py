"""
Process Catalogue API endpoints.
Full CRUD with hierarchy traversal and tenant isolation.
"""

from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.process import Process, ProcessOperatingModel
from src.models.riada import RiadaItem
from src.schemas.process import (
    ProcessCreate,
    ProcessDetailResponse,
    ProcessListResponse,
    ProcessReorder,
    ProcessResponse,
    ProcessTreeNode,
    ProcessUpdate,
)
from src.services.process_numbering import (
    generate_process_code,
    get_next_sort_order,
    renumber_all_processes,
    renumber_siblings,
    renumber_subtree,
    calculate_level_from_parent,
)

router = APIRouter()


@router.get("/", response_model=ProcessListResponse)
async def list_processes(
    level: Optional[str] = Query(None, description="Filter by level (L0-L5)"),
    parent_id: Optional[str] = Query(None, description="Filter by parent"),
    status: Optional[str] = Query(None, description="Filter by status"),
    process_type: Optional[str] = Query(None, description="primary or secondary"),
    search: Optional[str] = Query(None, description="Search name/description"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """List processes with filters and pagination."""
    query = select(Process).where(
        Process.organization_id == user.organization_id
    )

    if level:
        query = query.where(Process.level == level)
    if parent_id:
        query = query.where(Process.parent_id == parent_id)
    if status:
        query = query.where(func.lower(Process.status) == status.lower())
    if process_type:
        query = query.where(Process.process_type == process_type)
    if search:
        query = query.where(
            Process.name.ilike(f"%{search}%")
            | Process.description.ilike(f"%{search}%")
        )

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Paginate
    query = query.order_by(Process.level, Process.sort_order, Process.code)
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    processes = result.scalars().all()

    return ProcessListResponse(
        items=[ProcessResponse.model_validate(p) for p in processes],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/tree", response_model=list[ProcessTreeNode])
async def get_process_tree(
    root_level: str = Query("L0", description="Starting level for tree"),
    user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Get the full process hierarchy as a tree structure.
    Used by the Process Canvas and Tree views.
    """
    # Get all non-archived processes for this org
    result = await db.execute(
        select(Process)
        .where(
            Process.organization_id == user.organization_id,
            Process.status != "archived",
        )
        .order_by(Process.level, Process.sort_order)
    )
    all_processes = result.scalars().all()

    # Build tree in memory
    by_id = {p.id: p for p in all_processes}
    roots = []

    for p in all_processes:
        node = ProcessTreeNode(
            id=p.id,
            code=p.code,
            name=p.name,
            level=p.level,
            process_type=p.process_type,
            status=p.status,
            current_automation=p.current_automation,
            sort_order=p.sort_order,
        )
        if p.parent_id and p.parent_id in by_id:
            # Attach to parent (we'll build this properly below)
            pass
        elif p.level == root_level:
            roots.append(node)

    # Simple tree builder
    def build_children(parent_id: str) -> list[ProcessTreeNode]:
        children = []
        for p in all_processes:
            if p.parent_id == parent_id:
                node = ProcessTreeNode(
                    id=p.id,
                    code=p.code,
                    name=p.name,
                    level=p.level,
                    process_type=p.process_type,
                    status=p.status,
                    current_automation=p.current_automation,
                    sort_order=p.sort_order,
                    children=build_children(p.id),
                )
                children.append(node)
        return sorted(children, key=lambda x: x.sort_order)

    tree = []
    for p in all_processes:
        if p.level == root_level and not p.parent_id:
            node = ProcessTreeNode(
                id=p.id,
                code=p.code,
                name=p.name,
                level=p.level,
                process_type=p.process_type,
                status=p.status,
                current_automation=p.current_automation,
                sort_order=p.sort_order,
                children=build_children(p.id),
            )
            tree.append(node)

    return sorted(tree, key=lambda x: x.sort_order)


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
