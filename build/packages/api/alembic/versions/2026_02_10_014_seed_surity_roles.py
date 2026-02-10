"""Seed role_catalogue with actual Surity Contact List roles.

Revision ID: 014
Revises: 013
Create Date: 2026-02-10

Replaces the 13 placeholder roles from migration 013 with
32 actual operational roles from Surity Contact List Dec 2025.
Idempotent: uses ON CONFLICT DO UPDATE to upsert.
"""

from alembic import op
import sqlalchemy as sa
from uuid import uuid4

revision = "014"
down_revision = "013"
branch_labels = None
depends_on = None

SURITY_ROLES = [
    {"name": "General Manager", "scope": "Leadership", "sort_order": 1},
    {"name": "Managing Director - Surity Europe", "scope": "Leadership", "sort_order": 2},
    {"name": "Executive Assistant", "scope": "Leadership", "sort_order": 3},
    {"name": "Sourcing Director", "scope": "Sourcing", "sort_order": 10},
    {"name": "Category Sourcing Director", "scope": "Sourcing", "sort_order": 11},
    {"name": "Category Sourcing Manager", "scope": "Sourcing", "sort_order": 12},
    {"name": "Product Sourcing Manager", "scope": "Sourcing", "sort_order": 13},
    {"name": "Senior Merchandiser", "scope": "Sourcing", "sort_order": 14},
    {"name": "Merchandiser", "scope": "Sourcing", "sort_order": 15},
    {"name": "Assistant Merchandiser", "scope": "Sourcing", "sort_order": 16},
    {"name": "Head of Operation", "scope": "Supply Chain", "sort_order": 20},
    {"name": "Category Supply Chain Manager", "scope": "Supply Chain", "sort_order": 21},
    {"name": "Logistics Manager", "scope": "Supply Chain", "sort_order": 22},
    {"name": "Logistics Analyst", "scope": "Supply Chain", "sort_order": 23},
    {"name": "Supply Chain Analyst", "scope": "Supply Chain", "sort_order": 24},
    {"name": "Head of Quality", "scope": "QA", "sort_order": 30},
    {"name": "Senior QA Manager", "scope": "QA", "sort_order": 31},
    {"name": "Category QA Manager", "scope": "QA", "sort_order": 32},
    {"name": "QA Technologist", "scope": "QA", "sort_order": 33},
    {"name": "Senior QA Technologist", "scope": "QA", "sort_order": 34},
    {"name": "QA Administrator", "scope": "QA", "sort_order": 35},
    {"name": "Packaging Manager", "scope": "Packaging", "sort_order": 40},
    {"name": "Senior Packaging Engineer", "scope": "Packaging", "sort_order": 41},
    {"name": "Senior Packaging Technologist", "scope": "Packaging", "sort_order": 42},
    {"name": "Packaging Technologist", "scope": "Packaging", "sort_order": 43},
    {"name": "Accounting Manager", "scope": "Finance", "sort_order": 50},
    {"name": "Assistant Accountant", "scope": "Finance", "sort_order": 51},
    {"name": "HR Manager", "scope": "HR & Admin", "sort_order": 60},
    {"name": "Receptionist", "scope": "HR & Admin", "sort_order": 61},
    {"name": "Driver", "scope": "HR & Admin", "sort_order": 62},
    {"name": "IT Manager", "scope": "IT", "sort_order": 70},
    {"name": "IT Support Officer", "scope": "IT", "sort_order": 71},
]


def upgrade() -> None:
    conn = op.get_bind()

    org_result = conn.execute(sa.text("SELECT id FROM organizations LIMIT 1"))
    org_row = org_result.fetchone()
    if not org_row:
        print("  No organization found, skipping role seeding")
        return

    org_id = str(org_row[0])

    # Remove old placeholder roles that don't exist in the contact list
    old_only = [
        "CEO", "COO", "CFO", "VP Sourcing", "Head of Product",
        "Category Manager", "Sourcing Lead", "Quality Lead",
        "Warehouse Lead", "Head of HR", "Customer Service Lead",
    ]
    for name in old_only:
        conn.execute(
            sa.text(
                "DELETE FROM role_catalogue WHERE organization_id = :org AND name = :name"
            ),
            {"org": org_id, "name": name},
        )

    # Upsert new roles (Logistics Manager and IT Manager already exist)
    for role in SURITY_ROLES:
        conn.execute(
            sa.text("""
                INSERT INTO role_catalogue
                    (id, organization_id, name, scope, sort_order, is_active, created_at, updated_at)
                VALUES
                    (:id, :org, :name, :scope, :sort_order, true, NOW(), NOW())
                ON CONFLICT (organization_id, name)
                DO UPDATE SET scope = EXCLUDED.scope, sort_order = EXCLUDED.sort_order, updated_at = NOW()
            """),
            {
                "id": str(uuid4()),
                "org": org_id,
                "name": role["name"],
                "scope": role["scope"],
                "sort_order": role["sort_order"],
            },
        )

    print(f"  Upserted {len(SURITY_ROLES)} roles, removed {len(old_only)} placeholders")


def downgrade() -> None:
    conn = op.get_bind()
    # Remove all contact-list roles; migration 013 will re-seed placeholders on downgrade
    org_result = conn.execute(sa.text("SELECT id FROM organizations LIMIT 1"))
    org_row = org_result.fetchone()
    if not org_row:
        return

    org_id = str(org_row[0])
    for role in SURITY_ROLES:
        conn.execute(
            sa.text(
                "DELETE FROM role_catalogue WHERE organization_id = :org AND name = :name"
            ),
            {"org": org_id, "name": role["name"]},
        )
    print(f"  Removed {len(SURITY_ROLES)} contact-list roles")
