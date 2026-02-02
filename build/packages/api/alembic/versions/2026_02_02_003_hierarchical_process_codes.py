"""Regenerate process codes with hierarchical numbering.

Revision ID: 003
Revises: 002
Create Date: 2026-02-02

Migrates existing process codes from manual format (e.g., "L2-10") to
hierarchical format (e.g., "1.2.3") based on parent-child relationships.

L0: "1", "2", "3"...
L1: "1.1", "1.2", "2.1"...
L2: "1.1.1", "1.1.2"...
And so on through L5.
"""

from alembic import op
from sqlalchemy import text

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Regenerate all process codes with hierarchical numbering."""
    # This migration uses a recursive CTE to renumber processes
    # Starting from L0 roots, it assigns sequential numbers and cascades to children

    conn = op.get_bind()

    # Check if already migrated - if codes are already hierarchical (contain dots), skip
    sample = conn.execute(
        text("SELECT code FROM processes WHERE code LIKE '%.%' LIMIT 1")
    ).fetchone()
    if sample:
        print("  Hierarchical codes already exist, skipping renumbering")
        return

    # Drop the unique constraint temporarily to allow code updates
    conn.execute(text("DROP INDEX IF EXISTS ix_processes_org_code"))

    # Get all organizations that have processes
    orgs = conn.execute(
        text("SELECT DISTINCT organization_id FROM processes WHERE status != 'archived'")
    ).fetchall()

    for (org_id,) in orgs:
        # Process L0 (root) processes first
        roots = conn.execute(
            text("""
                SELECT id FROM processes
                WHERE organization_id = :org_id
                  AND parent_id IS NULL
                  AND status != 'archived'
                ORDER BY sort_order, created_at
            """),
            {"org_id": org_id}
        ).fetchall()

        for idx, (root_id,) in enumerate(roots):
            position = idx + 1
            new_code = str(position)

            # Update root process
            conn.execute(
                text("UPDATE processes SET code = :code, sort_order = :sort_order WHERE id = :id"),
                {"code": new_code, "sort_order": idx, "id": root_id}
            )

            # Recursively update children
            _renumber_children(conn, org_id, root_id, new_code)

    # Recreate the unique constraint
    conn.execute(
        text("CREATE UNIQUE INDEX ix_processes_org_code ON processes (organization_id, code)")
    )


def _renumber_children(conn, org_id: str, parent_id: str, parent_code: str) -> None:
    """Recursively renumber children of a process."""
    children = conn.execute(
        text("""
            SELECT id FROM processes
            WHERE organization_id = :org_id
              AND parent_id = :parent_id
              AND status != 'archived'
            ORDER BY sort_order, created_at
        """),
        {"org_id": org_id, "parent_id": parent_id}
    ).fetchall()

    for idx, (child_id,) in enumerate(children):
        position = idx + 1
        new_code = f"{parent_code}.{position}"

        conn.execute(
            text("UPDATE processes SET code = :code, sort_order = :sort_order WHERE id = :id"),
            {"code": new_code, "sort_order": idx, "id": child_id}
        )

        # Recurse to grandchildren
        _renumber_children(conn, org_id, child_id, new_code)


def downgrade() -> None:
    """
    Downgrade is not fully reversible - original codes are lost.
    This sets codes back to a level-based format (e.g., "L2-001").
    """
    conn = op.get_bind()

    # Get all organizations
    orgs = conn.execute(
        text("SELECT DISTINCT organization_id FROM processes")
    ).fetchall()

    for (org_id,) in orgs:
        # For each level, renumber with level prefix
        for level_num in range(6):
            level = f"L{level_num}"
            processes = conn.execute(
                text("""
                    SELECT id FROM processes
                    WHERE organization_id = :org_id
                      AND level = :level
                    ORDER BY sort_order, created_at
                """),
                {"org_id": org_id, "level": level}
            ).fetchall()

            for idx, (proc_id,) in enumerate(processes):
                # Format: L2-001, L2-002, etc.
                old_code = f"{level}-{idx + 1:03d}"
                conn.execute(
                    text("UPDATE processes SET code = :code WHERE id = :id"),
                    {"code": old_code, "id": proc_id}
                )
