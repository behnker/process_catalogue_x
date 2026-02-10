"""Reseed process catalogue with V4 data (301 processes + RACI + KPIs).

Revision ID: 015
Revises: 014
Create Date: 2026-02-10

Replaces the 137-process catalogue (migration 008) with the V4 spreadsheet:
- 5 L0: Strategy, Support, Source, Develop, Execute
- 26 L1, 70 L2, 200 L3 processes (301 total)
- 200 RACI entries (one per L3 process)
- 200 KPI entries (one per L3 process)

Structural changes from V3: DELIVER merged into Execute (Post-Execution),
new Strategy L0 added. Process-system linkages dropped (paths changed).
"""

from alembic import op
import sqlalchemy as sa
from uuid import uuid4
import json
import os

revision = "015"
down_revision = "014"
branch_labels = None
depends_on = None

# OM tables with FK → processes (delete all rows for org)
OM_CHILD_TABLES = [
    "process_raci",
    "process_kpi",
    "process_governance",
    "process_policy",
    "process_timing",
    "process_sipoc",
    "process_system",
    "process_operating_model",
]

# Other tables with non-nullable FK → processes (delete rows for org)
OTHER_FK_TABLES = [
    "issue_log",
    "business_model_mappings",
]

# Tables with nullable FK → processes (null out the reference)
NULLABLE_FK_TABLES = [
    ("riada_items", "process_id"),
]


def _load_seed_data() -> list[dict]:
    """Load the V4 seed JSON from the reference directory."""
    migration_dir = os.path.dirname(__file__)
    project_root = os.path.normpath(
        os.path.join(migration_dir, "..", "..", "..", "..", "..")
    )
    seed_file = os.path.join(project_root, "reference", "process_catalogue_v4_seed.json")

    if not os.path.exists(seed_file):
        raise FileNotFoundError(f"Seed file not found: {seed_file}")

    with open(seed_file, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_org_id(conn) -> str | None:
    """Get the first organization ID (Surity)."""
    result = conn.execute(sa.text("SELECT id FROM organizations LIMIT 1"))
    row = result.fetchone()
    return str(row[0]) if row else None


def _delete_process_data(conn, org_id: str) -> None:
    """Delete all process-related data for the organization in FK order."""
    # 1. OM child tables (full delete)
    for table in OM_CHILD_TABLES:
        conn.execute(
            sa.text(f"DELETE FROM {table} WHERE organization_id = :org"),
            {"org": org_id},
        )

    # 2. Other tables with non-nullable process FK (full delete for org)
    for table in OTHER_FK_TABLES:
        conn.execute(
            sa.text(f"DELETE FROM {table} WHERE organization_id = :org"),
            {"org": org_id},
        )

    # 3. Nullable FK tables — null out process references
    for table, col in NULLABLE_FK_TABLES:
        conn.execute(
            sa.text(f"UPDATE {table} SET {col} = NULL WHERE organization_id = :org"),
            {"org": org_id},
        )

    # 4. Self-referential FK: delete children before parents (L3, L2, L1, L0)
    for level in ("L3", "L2", "L1", "L0"):
        conn.execute(
            sa.text(
                "DELETE FROM processes WHERE organization_id = :org AND level = :level"
            ),
            {"org": org_id, "level": level},
        )


def upgrade() -> None:
    conn = op.get_bind()

    org_id = _get_org_id(conn)
    if not org_id:
        print("  No organization found, skipping V4 reseed")
        return

    seed_data = _load_seed_data()

    # 1. Delete existing process data
    _delete_process_data(conn, org_id)

    # 2. Seed 301 processes
    ref_to_id: dict[str, str] = {}  # "1.1.1" → UUID
    inserted = 0

    for entry in seed_data:
        ref = entry["ref"]
        level = entry["level"]
        name = entry["name"]
        description = entry.get("description")

        # Determine parent ref and parent_id
        if level == 0:
            parent_id = None
        else:
            parent_ref = ".".join(ref.split(".")[:-1])
            parent_id = ref_to_id.get(parent_ref)
            if parent_id is None:
                print(f"  WARNING: parent {parent_ref} not found for {ref}")
                continue

        # Process type: "Support" L0 → secondary, all others → primary
        process_type = "secondary" if level == 0 and name == "Support" else "primary"

        proc_id = str(uuid4())
        level_str = f"L{level}"

        conn.execute(
            sa.text("""
                INSERT INTO processes
                    (id, organization_id, code, name, description, level,
                     parent_id, process_type, status)
                VALUES
                    (:id, :org_id, :code, :name, :desc, :level,
                     :parent_id, :proc_type, 'active')
            """),
            {
                "id": proc_id,
                "org_id": org_id,
                "code": ref,
                "name": name,
                "desc": description,
                "level": level_str,
                "parent_id": parent_id,
                "proc_type": process_type,
            },
        )

        ref_to_id[ref] = proc_id
        inserted += 1

    print(f"  Inserted {inserted} V4 processes")

    # 3. Seed RACI entries for L3 processes
    raci_count = 0
    for entry in seed_data:
        if entry["level"] != 3:
            continue
        if "responsible" not in entry:
            continue

        proc_id = ref_to_id.get(entry["ref"])
        if not proc_id:
            continue

        conn.execute(
            sa.text("""
                INSERT INTO process_raci
                    (id, organization_id, process_id, activity,
                     responsible, accountable, consulted, informed)
                VALUES
                    (:id, :org_id, :proc_id, :activity,
                     :responsible, :accountable, :consulted, :informed)
            """),
            {
                "id": str(uuid4()),
                "org_id": org_id,
                "proc_id": proc_id,
                "activity": entry["name"],
                "responsible": entry.get("responsible"),
                "accountable": entry.get("accountable"),
                "consulted": entry.get("consulted"),
                "informed": entry.get("informed"),
            },
        )
        raci_count += 1

    print(f"  Inserted {raci_count} RACI entries")

    # 4. Seed KPI entries for L3 processes
    kpi_count = 0
    for entry in seed_data:
        if entry["level"] != 3:
            continue
        kpi_text = entry.get("kpi")
        if not kpi_text:
            continue

        proc_id = ref_to_id.get(entry["ref"])
        if not proc_id:
            continue

        conn.execute(
            sa.text("""
                INSERT INTO process_kpi
                    (id, organization_id, process_id, name)
                VALUES
                    (:id, :org_id, :proc_id, :name)
            """),
            {
                "id": str(uuid4()),
                "org_id": org_id,
                "proc_id": proc_id,
                "name": kpi_text,
            },
        )
        kpi_count += 1

    print(f"  Inserted {kpi_count} KPI entries")


def downgrade() -> None:
    conn = op.get_bind()

    org_id = _get_org_id(conn)
    if not org_id:
        return

    # Delete all V4 data — migration 008 downgrade will handle its own data
    _delete_process_data(conn, org_id)
    print("  Removed V4 process data")
