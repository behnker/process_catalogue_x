"""
Process hierarchical numbering service.

Generates auto-numbered hierarchical codes for processes:
- L0: "1", "2", "3"...
- L1: "1.1", "1.2", "2.1"...
- L2: "1.1.1", "1.1.2"...
- And so on through L5
"""

from typing import Optional

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.process import Process


async def get_next_sort_order(
    db: AsyncSession,
    organization_id: str,
    parent_id: Optional[str],
) -> int:
    """Get the next sort_order for a new sibling under the given parent."""
    query = select(func.coalesce(func.max(Process.sort_order), -1) + 1).where(
        Process.organization_id == organization_id
    )
    if parent_id:
        query = query.where(Process.parent_id == parent_id)
    else:
        query = query.where(Process.parent_id.is_(None))

    result = await db.execute(query)
    return result.scalar() or 0


async def generate_process_code(
    db: AsyncSession,
    organization_id: str,
    parent_id: Optional[str],
    sort_order: Optional[int] = None,
) -> str:
    """
    Generate hierarchical code based on parent and position.

    - L0 with no parent: "1", "2", "3"...
    - L1+ with parent: "{parent_code}.{position}"

    Position is 1-based for human readability.
    """
    if sort_order is None:
        sort_order = await get_next_sort_order(db, organization_id, parent_id)

    position = sort_order + 1  # 1-based for display

    if not parent_id:
        # L0 process - just the position number
        return str(position)

    # Get parent's code to build hierarchical code
    result = await db.execute(
        select(Process.code).where(Process.id == parent_id)
    )
    parent_code = result.scalar_one_or_none()

    if not parent_code:
        # Parent not found, fall back to simple number
        return str(position)

    return f"{parent_code}.{position}"


async def renumber_siblings(
    db: AsyncSession,
    organization_id: str,
    parent_id: Optional[str],
) -> list[str]:
    """
    Renumber all siblings under a parent based on sort_order.

    Returns list of process IDs that were renumbered (for cascading to children).
    """
    # Get all siblings ordered by sort_order
    query = select(Process).where(
        Process.organization_id == organization_id,
        Process.status != "archived",
    ).order_by(Process.sort_order)

    if parent_id:
        query = query.where(Process.parent_id == parent_id)
    else:
        query = query.where(Process.parent_id.is_(None))

    result = await db.execute(query)
    siblings = result.scalars().all()

    # Get parent code if exists
    parent_code = None
    if parent_id:
        parent_result = await db.execute(
            select(Process.code).where(Process.id == parent_id)
        )
        parent_code = parent_result.scalar_one_or_none()

    updated_ids = []
    for idx, process in enumerate(siblings):
        position = idx + 1  # 1-based
        new_code = f"{parent_code}.{position}" if parent_code else str(position)

        if process.code != new_code:
            process.code = new_code
            process.sort_order = idx
            updated_ids.append(process.id)
        elif process.sort_order != idx:
            process.sort_order = idx

    return updated_ids


async def renumber_subtree(
    db: AsyncSession,
    organization_id: str,
    process_id: str,
) -> None:
    """
    Recursively update codes for a process's children.

    Called when a process code changes to cascade the change to all descendants.
    """
    # Get this process's current code
    result = await db.execute(
        select(Process.code).where(Process.id == process_id)
    )
    parent_code = result.scalar_one_or_none()

    if not parent_code:
        return

    # Get all children ordered by sort_order
    result = await db.execute(
        select(Process).where(
            Process.parent_id == process_id,
            Process.status != "archived",
        ).order_by(Process.sort_order)
    )
    children = result.scalars().all()

    for idx, child in enumerate(children):
        position = idx + 1
        new_code = f"{parent_code}.{position}"

        if child.code != new_code:
            child.code = new_code

        if child.sort_order != idx:
            child.sort_order = idx

        # Recursively update this child's descendants
        await renumber_subtree(db, organization_id, child.id)


async def renumber_all_processes(
    db: AsyncSession,
    organization_id: str,
) -> int:
    """
    Renumber all processes in an organization with hierarchical codes.

    Used for migration/data repair. Returns count of updated processes.
    """
    count = 0

    # Start with L0 processes (no parent)
    result = await db.execute(
        select(Process).where(
            Process.organization_id == organization_id,
            Process.parent_id.is_(None),
            Process.status != "archived",
        ).order_by(Process.sort_order, Process.created_at)
    )
    roots = result.scalars().all()

    for idx, root in enumerate(roots):
        position = idx + 1
        new_code = str(position)

        if root.code != new_code or root.sort_order != idx:
            root.code = new_code
            root.sort_order = idx
            count += 1

        # Process descendants recursively
        count += await _renumber_children(db, organization_id, root.id, new_code)

    return count


async def _renumber_children(
    db: AsyncSession,
    organization_id: str,
    parent_id: str,
    parent_code: str,
) -> int:
    """Helper to recursively renumber children."""
    count = 0

    result = await db.execute(
        select(Process).where(
            Process.organization_id == organization_id,
            Process.parent_id == parent_id,
            Process.status != "archived",
        ).order_by(Process.sort_order, Process.created_at)
    )
    children = result.scalars().all()

    for idx, child in enumerate(children):
        position = idx + 1
        new_code = f"{parent_code}.{position}"

        if child.code != new_code or child.sort_order != idx:
            child.code = new_code
            child.sort_order = idx
            count += 1

        # Recurse to children
        count += await _renumber_children(db, organization_id, child.id, new_code)

    return count


def calculate_level_from_parent(parent_level: Optional[str]) -> str:
    """Calculate the level based on parent's level."""
    if not parent_level:
        return "L0"

    level_num = int(parent_level[1])  # Extract number from "L0", "L1", etc.
    next_level = min(level_num + 1, 5)  # Cap at L5
    return f"L{next_level}"
