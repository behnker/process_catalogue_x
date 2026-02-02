"""Process listing and tree endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import CurrentUser, get_current_user
from src.core.tenancy import get_tenant_db
from src.models.process import Process
from src.schemas.process import (
    ProcessListResponse,
    ProcessResponse,
    ProcessTreeNode,
)
from src.services.tree_builder import build_tree

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

    def node_factory(p: Process, children: list[ProcessTreeNode]) -> ProcessTreeNode:
        return ProcessTreeNode(
            id=p.id,
            code=p.code,
            name=p.name,
            level=p.level,
            process_type=p.process_type,
            status=p.status,
            current_automation=p.current_automation,
            sort_order=p.sort_order,
            children=children,
        )

    return build_tree(all_processes, node_factory, root_parent_id=None)
