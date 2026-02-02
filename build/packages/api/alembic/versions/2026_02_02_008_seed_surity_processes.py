"""Seed Surity Process Catalogue from Excel data.

Revision ID: 008
Revises: 007
Create Date: 2026-02-02

Seeds 137 processes (L0-L3) from Surity_Process_Catalogue_COMPLETE_Populated.xlsx
- 5 L0: SUPPORT, SOURCE, DEVELOP, EXECUTE, DELIVER
- 18 L1, 50 L2, 64 L3 processes
"""

from alembic import op
import sqlalchemy as sa
from uuid import uuid4
import json
import os

revision = "008"
down_revision = "007"
branch_labels = None
depends_on = None

# Process types: SUPPORT is secondary, others are primary (value chain)
SUPPORT_TYPE = "secondary"
PRIMARY_TYPE = "primary"


def upgrade() -> None:
    conn = op.get_bind()

    # Get the first organization (Surity)
    org_result = conn.execute(sa.text("SELECT id FROM organizations LIMIT 1"))
    org_row = org_result.fetchone()
    if not org_row:
        print("  No organization found, skipping process seeding")
        return

    org_id = str(org_row[0])

    # Load seed data from JSON - find project root
    # Migration file is at: build/packages/api/alembic/versions/
    # Seed file is at: reference/
    migration_dir = os.path.dirname(__file__)
    # Go up: versions -> alembic -> api -> packages -> build -> project_root
    project_root = os.path.normpath(os.path.join(migration_dir, "..", "..", "..", "..", ".."))
    seed_file = os.path.join(project_root, "reference", "process_catalogue_seed.json")

    if not os.path.exists(seed_file):
        print(f"  Seed file not found: {seed_file}")
        return

    with open(seed_file, "r", encoding="utf-8") as f:
        rows = json.load(f)

    # Clear existing processes for this org (fresh seed)
    # Must delete in FK order: child tables first
    conn.execute(
        sa.text("DELETE FROM process_system WHERE organization_id = :org"),
        {"org": org_id}
    )
    conn.execute(
        sa.text("DELETE FROM process_operating_model WHERE organization_id = :org"),
        {"org": org_id}
    )
    # Delete processes in reverse hierarchy order (children before parents)
    conn.execute(
        sa.text("DELETE FROM processes WHERE organization_id = :org"),
        {"org": org_id}
    )

    # Track created processes by their full path for parent lookup
    # Key: "L0|L1|L2|L3" -> UUID
    process_map = {}
    l0_counter = {}  # L0 name -> sequential number
    l1_counter = {}  # L0 name -> L1 name -> sequential number
    l2_counter = {}  # (L0, L1) -> L2 name -> sequential number
    l3_counter = {}  # (L0, L1, L2) -> L3 name -> sequential number

    inserted = 0

    for row in rows:
        l0 = row.get("l0")
        l1 = row.get("l1")
        l2 = row.get("l2")
        l3 = row.get("l3")
        owner = row.get("owner")
        desc = row.get("desc")

        # Determine the level of this row
        if l3:
            level = "L3"
            name = l3
            parent_path = f"{l0}|{l1}|{l2}"
        elif l2:
            level = "L2"
            name = l2
            parent_path = f"{l0}|{l1}"
        elif l1:
            level = "L1"
            name = l1
            parent_path = f"{l0}"
        else:
            level = "L0"
            name = l0
            parent_path = None

        if not name:
            continue

        # Build the full path key for this process
        if level == "L0":
            path_key = f"{l0}"
        elif level == "L1":
            path_key = f"{l0}|{l1}"
        elif level == "L2":
            path_key = f"{l0}|{l1}|{l2}"
        else:
            path_key = f"{l0}|{l1}|{l2}|{l3}"

        # Skip if already created (handles duplicate rows)
        if path_key in process_map:
            continue

        # Get parent ID
        parent_id = process_map.get(parent_path) if parent_path else None

        # Generate hierarchical code
        if level == "L0":
            if l0 not in l0_counter:
                l0_counter[l0] = len(l0_counter) + 1
            code = str(l0_counter[l0])
        elif level == "L1":
            if l0 not in l1_counter:
                l1_counter[l0] = {}
            if l1 not in l1_counter[l0]:
                l1_counter[l0][l1] = len(l1_counter[l0]) + 1
            parent_code = str(l0_counter[l0])
            code = f"{parent_code}.{l1_counter[l0][l1]}"
        elif level == "L2":
            key = (l0, l1)
            if key not in l2_counter:
                l2_counter[key] = {}
            if l2 not in l2_counter[key]:
                l2_counter[key][l2] = len(l2_counter[key]) + 1
            parent_code = f"{l0_counter[l0]}.{l1_counter[l0][l1]}"
            code = f"{parent_code}.{l2_counter[key][l2]}"
        else:  # L3
            key2 = (l0, l1)
            key3 = (l0, l1, l2)
            if key3 not in l3_counter:
                l3_counter[key3] = {}
            if l3 not in l3_counter[key3]:
                l3_counter[key3][l3] = len(l3_counter[key3]) + 1
            parent_code = f"{l0_counter[l0]}.{l1_counter[l0][l1]}.{l2_counter[key2][l2]}"
            code = f"{parent_code}.{l3_counter[key3][l3]}"

        # Determine process type
        process_type = SUPPORT_TYPE if l0 == "SUPPORT" else PRIMARY_TYPE

        # Generate UUID
        proc_id = str(uuid4())

        # Store owner in metadata_extra (no user records yet)
        metadata = {"owner_name": owner} if owner else {}

        # Insert process
        conn.execute(
            sa.text("""
                INSERT INTO processes
                    (id, organization_id, code, name, description, level,
                     parent_id, process_type, metadata_extra, status)
                VALUES
                    (:id, :org_id, :code, :name, :desc, :level,
                     :parent_id, :proc_type, CAST(:metadata AS jsonb), 'active')
            """),
            {
                "id": proc_id,
                "org_id": org_id,
                "code": code,
                "name": name,
                "desc": desc,
                "level": level,
                "parent_id": parent_id,
                "proc_type": process_type,
                "metadata": json.dumps(metadata),
            }
        )

        process_map[path_key] = proc_id
        inserted += 1

    print(f"  Inserted {inserted} Surity processes")

    # Now create process-system linkages for key processes
    _create_system_linkages(conn, org_id, process_map)


def _create_system_linkages(conn, org_id: str, process_map: dict) -> None:
    """Create process-system linkages based on Operating Model spec."""

    # Get system IDs
    system_ids = {}
    for name, key in [
        ("ERP System", "erp"),
        ("Email & OneDrive (M365)", "m365"),
        ("Internal Finance Software (Kingdee)", "kingdee"),
    ]:
        result = conn.execute(
            sa.text("SELECT id FROM system_catalogue WHERE organization_id = :org AND name = :name"),
            {"org": org_id, "name": name}
        )
        row = result.fetchone()
        if row:
            system_ids[key] = str(row[0])

    if not system_ids:
        print("  No systems found, skipping linkages")
        return

    # Map process names to path keys for lookup
    # These are the key L2 processes that use systems
    process_lookups = {
        "data_mgmt": "SUPPORT|Data, Systems & Reporting|Data Management",
        "quotation": "EXECUTE|Order Management|Quotation",
        "surity_audit": "SOURCE|Factory Audit Programs|Surity Audit",
        "order_placement": "EXECUTE|Order Management|Order Placement",
        "fri": "EXECUTE|Quality Inspection|FRI (Final Random Inspection)",
        "container_booking": "EXECUTE|Container Loading & Delivery|Container Booking",
        "payment_release": "DELIVER|Payment Processing|Payment Release",
    }

    # Resolve process IDs
    process_ids = {}
    for key, path in process_lookups.items():
        proc_id = process_map.get(path)
        if proc_id:
            process_ids[key] = proc_id

    # Define linkages: (process_key, system_key, purpose, role, method, criticality, scope)
    linkages = [
        ("data_mgmt", "erp", "Product master data repository, order management",
         "primary", "central_hub", "critical", "All staff"),
        ("data_mgmt", "m365", "Document management, file storage, collaboration",
         "secondary", "manual_entry", "high", "All staff"),
        ("quotation", "erp", "Quotation creation and tracking",
         "primary", "central_hub", "high", "Account team"),
        ("surity_audit", "erp", "Audit scheduling, findings documentation, grading",
         "primary", "manual_export", "medium", "Quality team"),
        ("order_placement", "erp", "PO creation, order confirmation tracking",
         "primary", "central_hub", "critical", "Account team"),
        ("fri", "erp", "Inspection scheduling, results tracking, defect logging",
         "primary", "manual_export", "high", "QC team"),
        ("container_booking", "erp", "Shipment booking and documentation",
         "secondary", "manual_entry", "high", "Logistics team"),
        ("payment_release", "kingdee", "Invoice processing, payment authorization",
         "primary", "api", "critical", "Finance team"),
    ]

    linked = 0
    for link in linkages:
        proc_key, sys_key, purpose, role, method, crit, scope = link
        proc_id = process_ids.get(proc_key)
        sys_id = system_ids.get(sys_key)

        if proc_id and sys_id:
            conn.execute(
                sa.text("""
                    INSERT INTO process_system
                        (id, organization_id, process_id, system_id, purpose,
                         system_role, integration_method, criticality, user_scope)
                    VALUES
                        (:id, :org_id, :proc_id, :sys_id, :purpose,
                         :role, :method, :crit, :scope)
                    ON CONFLICT DO NOTHING
                """),
                {
                    "id": str(uuid4()),
                    "org_id": org_id,
                    "proc_id": proc_id,
                    "sys_id": sys_id,
                    "purpose": purpose,
                    "role": role,
                    "method": method,
                    "crit": crit,
                    "scope": scope,
                }
            )
            linked += 1

    print(f"  Created {linked} process-system linkages")


def downgrade() -> None:
    conn = op.get_bind()

    # Get the first organization
    org_result = conn.execute(sa.text("SELECT id FROM organizations LIMIT 1"))
    org_row = org_result.fetchone()
    if not org_row:
        return

    org_id = str(org_row[0])

    # Remove seeded data - delete in FK order
    conn.execute(
        sa.text("DELETE FROM process_system WHERE organization_id = :org"),
        {"org": org_id}
    )
    conn.execute(
        sa.text("DELETE FROM process_operating_model WHERE organization_id = :org"),
        {"org": org_id}
    )
    conn.execute(
        sa.text("DELETE FROM processes WHERE organization_id = :org"),
        {"org": org_id}
    )
