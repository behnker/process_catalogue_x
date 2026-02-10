"""Migrate Operating Model components from JSONB to relational tables.

Revision ID: 013
Revises: 012
Create Date: 2026-02-10

Creates 7 new tables: role_catalogue, process_raci, process_kpi,
process_governance, process_policy, process_timing, process_sipoc.

Adds agentic_potential column to processes table.
Migrates existing governance JSONB data to process_governance rows.
Seeds 13 operational roles for Surity organisation.

Blueprint §4.4.1: Operating Model components with dedicated relational tables.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from uuid import uuid4
import json

revision = "013"
down_revision = "012"
branch_labels = None
depends_on = None


# ── Enum values ──────────────────────────────────────────────

GOVERNANCE_CADENCE = (
    "governance_cadence",
    ["daily", "weekly", "fortnightly", "monthly", "quarterly", "annual", "ad_hoc"],
)
POLICY_TYPE = (
    "policy_type",
    ["policy", "business_rule", "regulatory", "standard", "guideline"],
)
TIMING_FREQUENCY = (
    "timing_frequency",
    ["continuous", "daily", "weekly", "monthly", "quarterly", "annual", "per_order", "on_demand"],
)
SIPOC_ELEMENT = (
    "sipoc_element",
    ["supplier", "input", "output", "customer"],
)
AGENTIC_POTENTIAL = (
    "agentic_potential",
    ["none", "low", "medium", "high"],
)

ALL_ENUMS = [GOVERNANCE_CADENCE, POLICY_TYPE, TIMING_FREQUENCY, SIPOC_ELEMENT, AGENTIC_POTENTIAL]

# ── Role seed data ───────────────────────────────────────────

SURITY_ROLES = [
    {"name": "CEO", "scope": "Internal - Executive", "sort_order": 1},
    {"name": "COO", "scope": "Internal - Executive", "sort_order": 2},
    {"name": "CFO", "scope": "Internal - Executive", "sort_order": 3},
    {"name": "VP Sourcing", "scope": "Internal - Sourcing", "sort_order": 4},
    {"name": "Head of Product", "scope": "Internal - Product", "sort_order": 5},
    {"name": "Category Manager", "scope": "Internal - Sourcing", "sort_order": 6},
    {"name": "Sourcing Lead", "scope": "Internal - Sourcing", "sort_order": 7},
    {"name": "Quality Lead", "scope": "Internal - Quality", "sort_order": 8},
    {"name": "Logistics Manager", "scope": "Internal - Operations", "sort_order": 9},
    {"name": "Warehouse Lead", "scope": "Internal - Operations", "sort_order": 10},
    {"name": "IT Manager", "scope": "Internal - Technology", "sort_order": 11},
    {"name": "Head of HR", "scope": "Internal - People", "sort_order": 12},
    {"name": "Customer Service Lead", "scope": "Internal - Operations", "sort_order": 13},
]


# ── RLS helper ───────────────────────────────────────────────

def create_rls_policies(table_name: str) -> None:
    """Enable RLS and create 4 CRUD policies for a table."""
    op.execute(f"ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY")
    op.execute(f"ALTER TABLE {table_name} FORCE ROW LEVEL SECURITY")

    op.execute(f"""
        CREATE POLICY {table_name}_select_policy ON {table_name}
        FOR SELECT
        USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
    """)
    op.execute(f"""
        CREATE POLICY {table_name}_insert_policy ON {table_name}
        FOR INSERT
        WITH CHECK (organization_id = current_setting('app.current_organization_id', true)::uuid)
    """)
    op.execute(f"""
        CREATE POLICY {table_name}_update_policy ON {table_name}
        FOR UPDATE
        USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
        WITH CHECK (organization_id = current_setting('app.current_organization_id', true)::uuid)
    """)
    op.execute(f"""
        CREATE POLICY {table_name}_delete_policy ON {table_name}
        FOR DELETE
        USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
    """)


def drop_rls_policies(table_name: str) -> None:
    """Drop all 4 RLS policies and disable RLS for a table."""
    for action in ("select", "insert", "update", "delete"):
        op.execute(f"DROP POLICY IF EXISTS {table_name}_{action}_policy ON {table_name}")
    op.execute(f"ALTER TABLE {table_name} DISABLE ROW LEVEL SECURITY")


# ── Upgrade ──────────────────────────────────────────────────

def upgrade() -> None:
    # ── Create enums ─────────────────────────────────────────
    for enum_name, values in ALL_ENUMS:
        op.execute(sa.text(
            f"CREATE TYPE {enum_name} AS ENUM ({', '.join(repr(v) for v in values)})"
        ))

    # ── Add agentic_potential to processes ────────────────────
    op.add_column(
        "processes",
        sa.Column("agentic_potential", sa.String(20), nullable=True),
    )

    # ── 1. role_catalogue ────────────────────────────────────
    op.create_table(
        "role_catalogue",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("scope", sa.String(50)),
        sa.Column("description", sa.Text),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("sort_order", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_role_catalogue_org", "role_catalogue", ["organization_id"])
    op.create_index(
        "uq_role_catalogue_org_name", "role_catalogue",
        ["organization_id", "name"], unique=True,
    )

    # ── 2. process_raci ──────────────────────────────────────
    op.create_table(
        "process_raci",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("process_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("processes.id"), nullable=False),
        sa.Column("activity", sa.String(255), nullable=False),
        sa.Column("responsible", sa.String(255)),
        sa.Column("accountable", sa.String(255)),
        sa.Column("consulted", sa.String(255)),
        sa.Column("informed", sa.String(255)),
        sa.Column("notes", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_process_raci_org_proc", "process_raci",
                    ["organization_id", "process_id"])

    # ── 3. process_kpi ───────────────────────────────────────
    op.create_table(
        "process_kpi",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("process_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("processes.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("unit", sa.String(50)),
        sa.Column("target_value", sa.String(100)),
        sa.Column("current_value", sa.String(100)),
        sa.Column("previous_value", sa.String(100)),
        sa.Column("trend", sa.String(10)),
        sa.Column("rag_status", sa.String(10)),
        sa.Column("frequency", sa.String(50)),
        sa.Column("data_source", sa.String(255)),
        sa.Column("owner_role", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_process_kpi_org_proc", "process_kpi",
                    ["organization_id", "process_id"])

    # ── 4. process_governance ────────────────────────────────
    op.create_table(
        "process_governance",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("process_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("processes.id"), nullable=False),
        sa.Column("forum_name", sa.String(255), nullable=False),
        sa.Column("cadence", sa.String(20)),
        sa.Column("chair", sa.String(255)),
        sa.Column("attendees", postgresql.JSONB, server_default="[]"),
        sa.Column("decision_authority", sa.Text),
        sa.Column("escalation_path", sa.Text),
        sa.Column("approval_threshold", sa.Text),
        sa.Column("documentation", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_process_governance_org_proc", "process_governance",
                    ["organization_id", "process_id"])

    # ── 5. process_policy ────────────────────────────────────
    op.create_table(
        "process_policy",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("process_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("processes.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("policy_type", sa.String(20), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("compliance_requirement", sa.String(255)),
        sa.Column("owner_role", sa.String(255)),
        sa.Column("last_reviewed", sa.Date),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_process_policy_org_proc", "process_policy",
                    ["organization_id", "process_id"])

    # ── 6. process_timing ────────────────────────────────────
    op.create_table(
        "process_timing",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("process_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("processes.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("frequency", sa.String(20)),
        sa.Column("volume_per_period", sa.String(100)),
        sa.Column("cycle_time_target", sa.String(100)),
        sa.Column("cycle_time_actual", sa.String(100)),
        sa.Column("sla_commitment", sa.Text),
        sa.Column("trigger_event", sa.Text),
        sa.Column("dependencies", sa.Text),
        sa.Column("peak_season", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_process_timing_org_proc", "process_timing",
                    ["organization_id", "process_id"])

    # ── 7. process_sipoc ─────────────────────────────────────
    op.create_table(
        "process_sipoc",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("process_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("processes.id"), nullable=False),
        sa.Column("element_type", sa.String(20), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("sort_order", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_process_sipoc_org_proc_type", "process_sipoc",
                    ["organization_id", "process_id", "element_type"])

    # ── Enable RLS on all 7 tables ───────────────────────────
    for table in (
        "role_catalogue", "process_raci", "process_kpi",
        "process_governance", "process_policy", "process_timing",
        "process_sipoc",
    ):
        create_rls_policies(table)

    # ── Migrate governance JSONB → relational ────────────────
    conn = op.get_bind()

    gov_rows = conn.execute(sa.text("""
        SELECT organization_id, process_id, current_state
        FROM process_operating_model
        WHERE component_type = 'governance'
          AND current_state IS NOT NULL
    """))

    migrated = 0
    for row in gov_rows:
        org_id = str(row[0])
        process_id = str(row[1])
        state = row[2] if isinstance(row[2], dict) else json.loads(row[2])

        forums = state.get("forums", [])
        for forum in forums:
            conn.execute(
                sa.text("""
                    INSERT INTO process_governance
                        (id, organization_id, process_id, forum_name, cadence,
                         chair, attendees, decision_authority, created_at, updated_at)
                    VALUES
                        (:id, :org, :pid, :forum_name, :cadence,
                         :chair, CAST(:attendees AS jsonb), :decision_authority, NOW(), NOW())
                """),
                {
                    "id": str(uuid4()),
                    "org": org_id,
                    "pid": process_id,
                    "forum_name": forum.get("name", "Unnamed"),
                    "cadence": (forum.get("cadence") or "").lower().replace(" ", "_") or None,
                    "chair": forum.get("chair"),
                    "attendees": json.dumps(forum.get("attendees", [])),
                    "decision_authority": forum.get("decision_authority"),
                },
            )
            migrated += 1

    print(f"  Migrated {migrated} governance forums to process_governance table")

    # ── Seed roles for Surity ────────────────────────────────
    org_result = conn.execute(sa.text("SELECT id FROM organizations LIMIT 1"))
    org_row = org_result.fetchone()
    if org_row:
        org_id = str(org_row[0])
        for role in SURITY_ROLES:
            conn.execute(
                sa.text("""
                    INSERT INTO role_catalogue (id, organization_id, name, scope, sort_order, created_at, updated_at)
                    VALUES (:id, :org, :name, :scope, :sort_order, NOW(), NOW())
                    ON CONFLICT (organization_id, name) DO NOTHING
                """),
                {
                    "id": str(uuid4()),
                    "org": org_id,
                    "name": role["name"],
                    "scope": role["scope"],
                    "sort_order": role["sort_order"],
                },
            )
        print(f"  Seeded {len(SURITY_ROLES)} roles into role_catalogue")
    else:
        print("  No organization found, skipping role seeding")


# ── Downgrade ────────────────────────────────────────────────

def downgrade() -> None:
    # Drop RLS policies
    for table in (
        "process_sipoc", "process_timing", "process_policy",
        "process_governance", "process_kpi", "process_raci",
        "role_catalogue",
    ):
        drop_rls_policies(table)

    # Drop tables
    op.drop_table("process_sipoc")
    op.drop_table("process_timing")
    op.drop_table("process_policy")
    op.drop_table("process_governance")
    op.drop_table("process_kpi")
    op.drop_table("process_raci")
    op.drop_table("role_catalogue")

    # Remove agentic_potential from processes
    op.drop_column("processes", "agentic_potential")

    # Drop enums
    for enum_name, _ in reversed(ALL_ENUMS):
        op.execute(sa.text(f"DROP TYPE IF EXISTS {enum_name}"))
