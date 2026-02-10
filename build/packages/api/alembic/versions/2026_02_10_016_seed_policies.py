"""Seed Policies & Business Rules from Surity Operating Model Excel.

Revision ID: 016
Revises: 015
Create Date: 2026-02-10

Seeds 10 policies/business rules across 7 L2 processes from
Surity_Process_Catalogue_Operating_Model.xlsx → Policies & Rules sheet.

Processes are matched by V4 code (dot-notation) looked up at runtime.
"""

from alembic import op
import sqlalchemy as sa
from datetime import date
from uuid import uuid4

revision = "016"
down_revision = "015"
branch_labels = None
depends_on = None


# ── Seed data ────────────────────────────────────────────────
# Mapped from Excel V3 IDs to V4 process codes by name match.

POLICIES = [
    {
        "process_code": "2.8.5",  # Data Management
        "name": "Single Source of Truth Policy",
        "description": "All product master data must be maintained in ERP system only. No shadow spreadsheets permitted.",
        "policy_type": "policy",
        "compliance_requirement": "Internal Governance",
        "owner_role": "Data Manager",
        "last_reviewed": date(2025, 11, 1),
    },
    {
        "process_code": "2.8.5",  # Data Management
        "name": "Data Validation Rule",
        "description": "Product dimensions must be in cm, weight in kg. Mandatory fields: SKU, description, supplier, FOB price.",
        "policy_type": "business_rule",
        "compliance_requirement": "Data Quality",
        "owner_role": "Data Manager",
        "last_reviewed": date(2025, 12, 1),
    },
    {
        "process_code": "3.5.1",  # Factory Audit Execution (was Surity Audit)
        "name": "Factory Approval Standards",
        "description": "Factories must achieve minimum 70% on 5 Pillars assessment. Zero tolerance for child labor or forced labor.",
        "policy_type": "policy",
        "compliance_requirement": "CSR / Ethical Sourcing",
        "owner_role": "Quality Director",
        "last_reviewed": date(2025, 1, 1),
    },
    {
        "process_code": "3.5.1",  # Factory Audit Execution (was Surity Audit)
        "name": "Audit Frequency Rule",
        "description": "Approved factories re-audited every 2-4 years based on grade. Failed factories ineligible for 12 months.",
        "policy_type": "business_rule",
        "compliance_requirement": "Quality Standards",
        "owner_role": "Quality Manager",
        "last_reviewed": date(2025, 1, 1),
    },
    {
        "process_code": "2.3.2",  # Product Safety & Certification Management (was Test Specification & Validation)
        "name": "Product Safety Standards",
        "description": "All products must meet CE/UKCA (UK), CE (Benelux), RCM (Australia) requirements before shipment.",
        "policy_type": "policy",
        "compliance_requirement": "Regulatory / Legal",
        "owner_role": "Quality Director",
        "last_reviewed": date(2024, 6, 1),
    },
    {
        "process_code": "2.3.2",  # Product Safety & Certification Management (was Test Specification & Validation)
        "name": "Lab Accreditation Rule",
        "description": "Testing labs must be ISO 17025 accredited. Reports older than 2 years not accepted.",
        "policy_type": "business_rule",
        "compliance_requirement": "Quality Standards",
        "owner_role": "Quality Manager",
        "last_reviewed": date(2024, 6, 1),
    },
    {
        "process_code": "5.1.1",  # Order Processing (was Order Management L2-37)
        "name": "Order Change Authorization",
        "description": "Order changes >$5K require client written approval. Changes <$5K approved by Account Manager.",
        "policy_type": "business_rule",
        "compliance_requirement": "Commercial Terms",
        "owner_role": "Commercial Director",
        "last_reviewed": date(2025, 9, 1),
    },
    {
        "process_code": "5.3.1",  # Pre-Shipment Inspection (was Inspection L2-39)
        "name": "AQL Sampling Standards",
        "description": "Final inspections use ISO 2859 AQL 2.5 sampling plan. Major defects: AQL 2.5, Minor: AQL 4.0, Critical: 0.",
        "policy_type": "policy",
        "compliance_requirement": "Quality Standards",
        "owner_role": "Quality Director",
        "last_reviewed": date(2024, 3, 1),
    },
    {
        "process_code": "5.4.1",  # Shipment Preparation & Delivery (was Shipment Booking L2-44)
        "name": "Booking Lead Time Rule",
        "description": "Shipment bookings must be made 15 days before ex-factory date. Rush bookings subject to surcharge.",
        "policy_type": "business_rule",
        "compliance_requirement": "Logistics SLA",
        "owner_role": "Logistics Manager",
        "last_reviewed": date(2024, 8, 1),
    },
    {
        "process_code": "5.5.2",  # Payment Processing (was Documentation & Payment L2-47)
        "name": "Payment Terms Policy",
        "description": "Standard terms: 30 days from goods receipt. Early payment discount: 2% if paid within 10 days.",
        "policy_type": "policy",
        "compliance_requirement": "Financial / Commercial",
        "owner_role": "Finance Director",
        "last_reviewed": date(2025, 1, 1),
    },
]


def _get_org_id(conn) -> str | None:
    result = conn.execute(sa.text("SELECT id FROM organizations LIMIT 1"))
    row = result.fetchone()
    return str(row[0]) if row else None


def _get_process_ids(conn, org_id: str, codes: list[str]) -> dict[str, str]:
    """Look up process UUIDs by code for the given org."""
    result = conn.execute(
        sa.text(
            "SELECT code, id FROM processes "
            "WHERE organization_id = :org AND code = ANY(:codes)"
        ),
        {"org": org_id, "codes": codes},
    )
    return {row[0]: str(row[1]) for row in result.fetchall()}


def upgrade() -> None:
    conn = op.get_bind()

    org_id = _get_org_id(conn)
    if not org_id:
        print("  No organization found, skipping policy seed")
        return

    # Collect unique process codes needed
    codes = list({p["process_code"] for p in POLICIES})
    code_to_id = _get_process_ids(conn, org_id, codes)

    if not code_to_id:
        print(f"  WARNING: No processes found for codes {codes}")
        return

    inserted = 0
    skipped = 0
    for policy in POLICIES:
        process_id = code_to_id.get(policy["process_code"])
        if not process_id:
            print(f"  WARNING: Process {policy['process_code']} not found, skipping '{policy['name']}'")
            skipped += 1
            continue

        conn.execute(
            sa.text("""
                INSERT INTO process_policy
                    (id, organization_id, process_id, name, policy_type,
                     description, compliance_requirement, owner_role,
                     last_reviewed, is_active)
                VALUES
                    (:id, :org_id, :proc_id, :name, :policy_type,
                     :description, :compliance, :owner_role,
                     :last_reviewed, true)
            """),
            {
                "id": str(uuid4()),
                "org_id": org_id,
                "proc_id": process_id,
                "name": policy["name"],
                "policy_type": policy["policy_type"],
                "description": policy["description"],
                "compliance": policy["compliance_requirement"],
                "owner_role": policy["owner_role"],
                "last_reviewed": policy["last_reviewed"],
            },
        )
        inserted += 1

    print(f"  Inserted {inserted} policies ({skipped} skipped)")


def downgrade() -> None:
    conn = op.get_bind()
    org_id = _get_org_id(conn)
    if not org_id:
        return

    conn.execute(
        sa.text("DELETE FROM process_policy WHERE organization_id = :org"),
        {"org": org_id},
    )
    print("  Removed seeded policies")
