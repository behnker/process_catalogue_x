"""Add RIADA links table for item-to-item relationships.

Revision ID: 004
Revises: 003
Create Date: 2026-02-02

Blueprint §5.3.6: RIADA-to-RIADA linking
- Risk → Linked Actions (mitigates)
- Issue → Linked Dependencies (caused_by, blocks)
- General relationships (related_to, depends_on, duplicates, parent_of)
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── RIADA Links (self-referential many-to-many) ─────────
    op.create_table(
        "riada_links",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column(
            "organization_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("organizations.id"),
            nullable=False,
        ),
        sa.Column(
            "source_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("riada_items.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "target_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("riada_items.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("link_type", sa.String(30), nullable=False, server_default="related_to"),
        sa.Column("notes", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Unique constraint: only one link between two items in the same direction
    op.create_index(
        "ix_riada_links_source_target",
        "riada_links",
        ["organization_id", "source_id", "target_id"],
        unique=True,
    )

    # Enable RLS
    op.execute("ALTER TABLE riada_links ENABLE ROW LEVEL SECURITY")

    # RLS policy for tenant isolation
    op.execute("""
        CREATE POLICY riada_links_tenant_isolation ON riada_links
        FOR ALL
        USING (organization_id = current_setting('app.current_organization_id')::uuid)
        WITH CHECK (organization_id = current_setting('app.current_organization_id')::uuid)
    """)


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS riada_links_tenant_isolation ON riada_links")
    op.drop_table("riada_links")
