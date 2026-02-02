"""Add System Catalogue and ProcessSystem junction tables.

Revision ID: 005
Revises: 004
Create Date: 2026-02-02

Blueprint §9.6.9: System Catalogue with 25 columns
ProcessSystem junction table with 14 columns for process-to-system linkages.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "005"
down_revision = "004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── System Catalogue (25 columns) ─────────────────────────
    op.create_table(
        "system_catalogue",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column(
            "organization_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("organizations.id"),
            nullable=False,
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("scope_description", sa.Text),
        sa.Column("system_type", sa.String(30), nullable=False),
        sa.Column("provider_name", sa.String(255)),
        sa.Column("provider_type", sa.String(30)),
        sa.Column("primary_users", sa.String(255)),
        sa.Column("access_methods", postgresql.JSONB, server_default="[]"),
        sa.Column("is_saas", sa.Boolean, server_default="false"),
        sa.Column("hosting_model", sa.String(30)),
        sa.Column("operating_region", sa.String(30)),
        sa.Column("integration_method", sa.String(255)),
        sa.Column("criticality", sa.String(20), server_default="medium"),
        sa.Column(
            "owner_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("users.id"),
        ),
        sa.Column("license_model", sa.String(30)),
        sa.Column("compliance_notes", sa.Text),
        sa.Column("url", sa.String(500)),
        sa.Column("status", sa.String(20), nullable=False, server_default="evaluate"),
        sa.Column("metadata_extra", postgresql.JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column(
            "created_by",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("users.id"),
        ),
        sa.Column(
            "updated_by",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("users.id"),
        ),
    )

    # Indexes for system_catalogue
    op.create_index("ix_system_cat_org", "system_catalogue", ["organization_id"])
    op.create_index(
        "ix_system_cat_type", "system_catalogue", ["organization_id", "system_type"]
    )
    op.create_index(
        "ix_system_cat_status", "system_catalogue", ["organization_id", "status"]
    )
    op.create_index(
        "ix_system_cat_region", "system_catalogue", ["organization_id", "operating_region"]
    )

    # ── Process-System Junction (14 columns) ──────────────────
    op.create_table(
        "process_system",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column(
            "organization_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("organizations.id"),
            nullable=False,
        ),
        sa.Column(
            "process_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("processes.id"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "system_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("system_catalogue.id"),
            nullable=False,
            index=True,
        ),
        sa.Column("purpose", sa.Text),
        sa.Column("system_role", sa.String(30), server_default="primary"),
        sa.Column("integration_method", sa.String(30)),
        sa.Column("criticality", sa.String(20), server_default="medium"),
        sa.Column("user_scope", sa.String(255)),
        sa.Column("pain_points", sa.Text),
        sa.Column("automation_potential", sa.String(20)),
        sa.Column("status", sa.String(20), server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Unique constraint: one link per process-system pair per org
    op.create_index(
        "uq_process_system",
        "process_system",
        ["organization_id", "process_id", "system_id"],
        unique=True,
    )

    # ── Enable RLS ─────────────────────────────────────────────
    op.execute("ALTER TABLE system_catalogue ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE system_catalogue FORCE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE process_system ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE process_system FORCE ROW LEVEL SECURITY")

    # ── RLS Policies for system_catalogue ──────────────────────
    op.execute("""
        CREATE POLICY system_catalogue_select_policy ON system_catalogue
        FOR SELECT
        USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY system_catalogue_insert_policy ON system_catalogue
        FOR INSERT
        WITH CHECK (organization_id = current_setting('app.current_organization_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY system_catalogue_update_policy ON system_catalogue
        FOR UPDATE
        USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
        WITH CHECK (organization_id = current_setting('app.current_organization_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY system_catalogue_delete_policy ON system_catalogue
        FOR DELETE
        USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
    """)

    # ── RLS Policies for process_system ────────────────────────
    op.execute("""
        CREATE POLICY process_system_select_policy ON process_system
        FOR SELECT
        USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY process_system_insert_policy ON process_system
        FOR INSERT
        WITH CHECK (organization_id = current_setting('app.current_organization_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY process_system_update_policy ON process_system
        FOR UPDATE
        USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
        WITH CHECK (organization_id = current_setting('app.current_organization_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY process_system_delete_policy ON process_system
        FOR DELETE
        USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
    """)


def downgrade() -> None:
    # Drop process_system policies
    op.execute("DROP POLICY IF EXISTS process_system_select_policy ON process_system")
    op.execute("DROP POLICY IF EXISTS process_system_insert_policy ON process_system")
    op.execute("DROP POLICY IF EXISTS process_system_update_policy ON process_system")
    op.execute("DROP POLICY IF EXISTS process_system_delete_policy ON process_system")
    op.execute("ALTER TABLE process_system DISABLE ROW LEVEL SECURITY")

    # Drop system_catalogue policies
    op.execute("DROP POLICY IF EXISTS system_catalogue_select_policy ON system_catalogue")
    op.execute("DROP POLICY IF EXISTS system_catalogue_insert_policy ON system_catalogue")
    op.execute("DROP POLICY IF EXISTS system_catalogue_update_policy ON system_catalogue")
    op.execute("DROP POLICY IF EXISTS system_catalogue_delete_policy ON system_catalogue")
    op.execute("ALTER TABLE system_catalogue DISABLE ROW LEVEL SECURITY")

    # Drop tables
    op.drop_table("process_system")
    op.drop_table("system_catalogue")
