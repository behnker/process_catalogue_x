"""Seed Governance data into process_operating_model.

Revision ID: 011
Revises: 010
Create Date: 2026-02-06

Seeds governance forums for key Surity processes.
Derived from Blueprint §4.5.10 and Surity operating context.
Idempotent: uses ON CONFLICT DO NOTHING.
"""

from alembic import op
import sqlalchemy as sa
from uuid import uuid4
import json

revision = "011"
down_revision = "010"
branch_labels = None
depends_on = None


# Governance data keyed by process code
GOVERNANCE_BY_PROCESS = {
    "L0-02": {  # SOURCE
        "forums": [
            {
                "name": "Sourcing Steering Committee",
                "cadence": "Monthly",
                "attendees": ["CEO", "COO", "VP Sourcing", "Head of Compliance"],
                "decision_authority": "Strategic sourcing decisions, supplier policy changes, budget approval",
                "chair": "COO",
            },
            {
                "name": "Supplier Review Board",
                "cadence": "Quarterly",
                "attendees": ["VP Sourcing", "Category Managers", "Quality Lead"],
                "decision_authority": "Supplier performance reviews, onboarding/offboarding decisions",
                "chair": "VP Sourcing",
            },
        ],
    },
    "L0-03": {  # DEVELOP
        "forums": [
            {
                "name": "Product Development Committee",
                "cadence": "Fortnightly",
                "attendees": ["Head of Product", "Design Lead", "Category Managers", "Sourcing Lead"],
                "decision_authority": "Product range decisions, new product approvals, specification changes",
                "chair": "Head of Product",
            },
        ],
    },
    "L0-04": {  # EXECUTE
        "forums": [
            {
                "name": "Operations Review",
                "cadence": "Weekly",
                "attendees": ["COO", "Logistics Manager", "Warehouse Lead", "IT Manager"],
                "decision_authority": "Operational escalations, capacity decisions, process change approval",
                "chair": "COO",
            },
        ],
    },
    "L0-05": {  # DELIVER
        "forums": [
            {
                "name": "Delivery Performance Review",
                "cadence": "Weekly",
                "attendees": ["Logistics Manager", "Customer Service Lead", "Warehouse Lead"],
                "decision_authority": "Delivery SLA exceptions, carrier performance, route optimisation",
                "chair": "Logistics Manager",
            },
        ],
    },
    "L0-01": {  # SUPPORT
        "forums": [
            {
                "name": "Executive Leadership Team",
                "cadence": "Monthly",
                "attendees": ["CEO", "COO", "CFO", "VP Sourcing", "Head of HR"],
                "decision_authority": "Strategic direction, investment decisions, policy approval, risk oversight",
                "chair": "CEO",
            },
            {
                "name": "IT Governance Board",
                "cadence": "Monthly",
                "attendees": ["IT Manager", "COO", "Security Lead", "Data Manager"],
                "decision_authority": "System changes, security policy, data governance, technology roadmap",
                "chair": "IT Manager",
            },
        ],
    },
}


def upgrade() -> None:
    conn = op.get_bind()

    org_result = conn.execute(sa.text("SELECT id FROM organizations LIMIT 1"))
    org_row = org_result.fetchone()
    if not org_row:
        print("  No organization found, skipping governance seeding")
        return

    org_id = str(org_row[0])
    inserted = 0

    for process_code, governance_data in GOVERNANCE_BY_PROCESS.items():
        # Look up process by code
        proc_result = conn.execute(
            sa.text(
                "SELECT id FROM processes WHERE code = :code AND organization_id = :org"
            ),
            {"code": process_code, "org": org_id},
        )
        proc_row = proc_result.fetchone()
        if not proc_row:
            print(f"  Process {process_code} not found, skipping")
            continue

        process_id = str(proc_row[0])
        row_id = str(uuid4())

        conn.execute(
            sa.text("""
                INSERT INTO process_operating_model
                    (id, organization_id, process_id, component_type, current_state, future_state, transition_notes, created_at, updated_at)
                VALUES
                    (:id, :org, :pid, 'governance', :current, '{}', NULL, NOW(), NOW())
                ON CONFLICT (process_id, component_type) DO NOTHING
            """),
            {
                "id": row_id,
                "org": org_id,
                "pid": process_id,
                "current": json.dumps(governance_data),
            },
        )
        inserted += 1

    print(f"  Seeded governance for {inserted} processes (ON CONFLICT DO NOTHING)")


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "DELETE FROM process_operating_model WHERE component_type = 'governance'"
        )
    )
    print("  Removed all governance operating model data")
