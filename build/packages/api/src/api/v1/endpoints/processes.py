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
    ProcessResponse,
    ProcessTreeNode,
    ProcessUpdate,
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
        query = query.where(Process.status == status)
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
    # Get all processes for this org
    result = await db.execute(
        select(Process)
        .where(Process.organization_id == user.organization_id)
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
    """Create a new process."""
    process = Process(
        id=str(uuid4()),
        organization_id=user.organization_id,
        **body.model_dump(),
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
