"""Fix process-system linkages using name-based lookup.

Revision ID: 007
Revises: 006
Create Date: 2026-02-02

Migration 006 used old L2-xx codes which were converted to hierarchical
format by migration 003. This migration inserts the linkages using
process names instead.
"""

from alembic import op
import sqlalchemy as sa
from uuid import uuid4

revision = "007"
down_revision = "006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    # Get the first organization (Surity) for seeding
    org_result = conn.execute(
        sa.text("SELECT id FROM organizations LIMIT 1")
    )
    org_row = org_result.fetchone()
    if not org_row:
        return

    org_id = org_row[0]

    # Get system IDs by name
    system_ids = {}
    system_names = {
        "erp": "ERP System",
        "m365": "Email & OneDrive (M365)",
        "kingdee": "Internal Finance Software (Kingdee)",
    }

    for key, name in system_names.items():
        result = conn.execute(
            sa.text("SELECT id FROM system_catalogue WHERE organization_id = :org AND name = :name"),
            {"org": org_id, "name": name}
        )
        row = result.fetchone()
        if row:
            system_ids[key] = row[0]

    # Get process IDs by name
    process_name_map = {
        "Data Management": "data_mgmt",
        "Brief": "brief",
        "Surity Audit": "surity_audit",
        "Test Specification": "test_spec",
        "Order Management": "order_mgmt",
        "Inspection": "inspection",
        "Shipment Booking": "shipment",
        "Documentation & Payment": "doc_payment",
    }
    process_ids = {}

    for name, key in process_name_map.items():
        result = conn.execute(
            sa.text("SELECT id FROM processes WHERE organization_id = :org AND name = :name"),
            {"org": org_id, "name": name}
        )
        row = result.fetchone()
        if row:
            process_ids[key] = row[0]

    # Insert linkages (skip if already exist)
    linkages = [
        ("data_mgmt", "erp", "Product master data repository, order management",
         "primary", "central_hub", "critical", "All staff"),
        ("data_mgmt", "m365", "Document management, file storage, collaboration",
         "secondary", "manual_entry", "high", "All staff"),
        ("brief", "m365", "Client communication, brief receipt",
         "primary", "manual_entry", "high", "Account team"),
        ("surity_audit", "erp", "Audit scheduling, findings documentation, grading",
         "primary", "manual_export", "medium", "Quality team"),
        ("test_spec", "erp", "Test tracking and certificate management",
         "secondary", "manual_entry", "high", "Quality team"),
        ("order_mgmt", "erp", "PO creation, production tracking",
         "primary", "central_hub", "critical", "Sourcing team"),
        ("inspection", "erp", "Inspection scheduling, results tracking, defect logging",
         "primary", "manual_export", "high", "QC team"),
        ("shipment", "erp", "Shipment data and documentation",
         "secondary", "manual_entry", "high", "Logistics team"),
        ("doc_payment", "kingdee", "Invoice processing, payment tracking, reconciliation",
         "primary", "api", "critical", "Finance team"),
    ]

    inserted = 0
    for link in linkages:
        proc_key, sys_key, purpose, role, method, crit, scope = link
        proc_id = process_ids.get(proc_key)
        sys_id = system_ids.get(sys_key)

        if proc_id and sys_id:
            # Check if link already exists
            exists = conn.execute(
                sa.text("""
                    SELECT 1 FROM process_system
                    WHERE organization_id = :org AND process_id = :proc AND system_id = :sys
                """),
                {"org": org_id, "proc": proc_id, "sys": sys_id}
            ).fetchone()

            if not exists:
                conn.execute(
                    sa.text("""
                        INSERT INTO process_system
                            (id, organization_id, process_id, system_id, purpose,
                             system_role, integration_method, criticality, user_scope)
                        VALUES
                            (:id, :org_id, :proc_id, :sys_id, :purpose,
                             :role, :method, :crit, :scope)
                    """),
                    {
                        "id": str(uuid4()), "org_id": org_id, "proc_id": proc_id,
                        "sys_id": sys_id, "purpose": purpose, "role": role,
                        "method": method, "crit": crit, "scope": scope,
                    }
                )
                inserted += 1

    print(f"  Inserted {inserted} process-system linkages")


def downgrade() -> None:
    # Linkages will be removed by 006 downgrade if needed
    pass
