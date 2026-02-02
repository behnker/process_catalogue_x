"""Seed System Catalogue with Surity's 8 systems and process linkages.

Revision ID: 006
Revises: 005
Create Date: 2026-02-02

Blueprint §9.6.9: Surity system register (8 systems)
Operating Model Systems & Tools sheet (9 process-system linkages)
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from uuid import uuid4

# revision identifiers, used by Alembic.
revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None

# Pre-generated UUIDs for systems (allows linkages)
SYSTEM_IDS = {
    "erp": str(uuid4()),
    "m365": str(uuid4()),
    "audit_app": str(uuid4()),
    "fangcloud": str(uuid4()),
    "contract_mgmt": str(uuid4()),
    "share_drive": str(uuid4()),
    "kingdee": str(uuid4()),
    "dingtalk": str(uuid4()),
}


def upgrade() -> None:
    conn = op.get_bind()

    # Get the first organization (Surity) for seeding
    org_result = conn.execute(
        sa.text("SELECT id FROM organizations LIMIT 1")
    )
    org_row = org_result.fetchone()
    if not org_row:
        # No org exists yet; skip seeding (will be run after org is created)
        return

    org_id = org_row[0]

    # ── Insert 8 Systems ──────────────────────────────────────
    systems_data = [
        # 1. ERP System
        (SYSTEM_IDS["erp"], org_id, "ERP System",
         "Customized ERP by Fumasoft",
         "End-to-end: supplier/factory/customer management, project/quotation/product, factory audit job, ordering & shipment, reporting",
         "erp", "Fumasoft", "custom_developed",
         "All", '["web_browser"]', False, "on_premise", "china_only",
         "critical", "custom_contract", "optimize"),

        # 2. Email & OneDrive (M365)
        (SYSTEM_IDS["m365"], org_id, "Email & OneDrive (M365)",
         "Microsoft 365 Business Standard",
         "Email communication and file storage",
         "communication", "Microsoft", "commercial_saas",
         "All", '["desktop_app","mobile_app","web_browser"]', True, "cloud_global", "global",
         "high", "subscription", "maintain"),

        # 3. Factory Audit App
        (SYSTEM_IDS["audit_app"], org_id, "Factory Audit App",
         "Developed by Chongqing Yida",
         "Audit questionnaire with rate calculation and report generation",
         "quality", "Chongqing Yida", "custom_developed",
         "QA", '["mobile_app"]', False, "on_premise", "china_only",
         "medium", "custom_contract", "evaluate"),

        # 4. FangCloud
        (SYSTEM_IDS["fangcloud"], org_id, "FangCloud",
         "yifangyun cloud storage",
         "Key quality files: Framework docs, Factory Audit Reports, Technical Files",
         "collaboration", "yifangyun", "commercial_saas",
         "QA", '["desktop_app","mobile_app","web_browser"]', True, "cloud_china", "multi_region",
         "medium", "subscription", "maintain"),

        # 5. Contract Management System
        (SYSTEM_IDS["contract_mgmt"], org_id, "Contract Management System",
         "zhenling contract platform",
         "Contract lifecycle: buying agreements, office rent, QA 3rd party contracts",
         "contract_mgmt", "zhenling", "commercial_saas",
         "Sourcing", '["web_browser"]', True, "cloud_china", "china_only",
         "medium", "subscription", "maintain"),

        # 6. Internal Share Drive
        (SYSTEM_IDS["share_drive"], org_id, "Internal Share Drive",
         "Windows Server file share",
         "Internal document storage",
         "file_storage", "Microsoft", "internal",
         "All", '["file_browser"]', False, "on_premise", "china_only",
         "medium", "internal", "retire"),

        # 7. Kingdee Finance Software
        (SYSTEM_IDS["kingdee"], org_id, "Internal Finance Software (Kingdee)",
         "Kingdee accounting platform",
         "Accounting and financial management",
         "finance", "Kingdee", "commercial_onprem",
         "Finance", '["desktop_app"]', False, "on_premise", "china_only",
         "high", "perpetual", "maintain"),

        # 8. Ding Talk
        (SYSTEM_IDS["dingtalk"], org_id, "Ding Talk",
         "Alibaba workplace platform (free tier)",
         "Leave and trip approval workflows",
         "workflow", "Alibaba", "commercial_saas",
         "All", '["desktop_app","mobile_app"]', True, "cloud_china", "china_only",
         "low", "free", "maintain"),
    ]

    for sys in systems_data:
        conn.execute(
            sa.text("""
                INSERT INTO system_catalogue
                    (id, organization_id, name, description, scope_description,
                     system_type, provider_name, provider_type, primary_users,
                     access_methods, is_saas, hosting_model, operating_region,
                     criticality, license_model, status)
                VALUES
                    (:id, :org_id, :name, :desc, :scope, :sys_type, :provider,
                     :prov_type, :users, :access::jsonb, :saas, :hosting, :region,
                     :crit, :license, :status)
                ON CONFLICT DO NOTHING
            """),
            {
                "id": sys[0], "org_id": sys[1], "name": sys[2], "desc": sys[3],
                "scope": sys[4], "sys_type": sys[5], "provider": sys[6],
                "prov_type": sys[7], "users": sys[8], "access": sys[9],
                "saas": sys[10], "hosting": sys[11], "region": sys[12],
                "crit": sys[13], "license": sys[14], "status": sys[15],
            }
        )

    # ── Get Process IDs by code ───────────────────────────────
    process_codes = ["L2-05", "L2-10", "L2-20", "L2-28", "L2-37", "L2-39", "L2-44", "L2-47"]
    process_ids = {}

    for code in process_codes:
        result = conn.execute(
            sa.text("SELECT id FROM processes WHERE organization_id = :org AND code = :code"),
            {"org": org_id, "code": code}
        )
        row = result.fetchone()
        if row:
            process_ids[code] = row[0]

    # ── Insert 9 Process-System Linkages ──────────────────────
    linkages = [
        # L2-05 Data Management -> ERP
        ("L2-05", "erp", "Product master data repository, order management",
         "primary", "central_hub", "critical", "All staff"),
        # L2-05 Data Management -> M365
        ("L2-05", "m365", "Document management, file storage, collaboration",
         "secondary", "manual_entry", "high", "All staff"),
        # L2-10 Brief -> M365
        ("L2-10", "m365", "Client communication, brief receipt",
         "primary", "manual_entry", "high", "Account team"),
        # L2-20 Surity Audit -> ERP
        ("L2-20", "erp", "Audit scheduling, findings documentation, grading",
         "primary", "manual_export", "medium", "Quality team"),
        # L2-28 Test Specification -> ERP
        ("L2-28", "erp", "Test tracking and certificate management",
         "secondary", "manual_entry", "high", "Quality team"),
        # L2-37 Order Management -> ERP
        ("L2-37", "erp", "PO creation, production tracking",
         "primary", "central_hub", "critical", "Sourcing team"),
        # L2-39 Inspection -> ERP
        ("L2-39", "erp", "Inspection scheduling, results tracking, defect logging",
         "primary", "manual_export", "high", "QC team"),
        # L2-44 Shipment Booking -> ERP
        ("L2-44", "erp", "Shipment data and documentation",
         "secondary", "manual_entry", "high", "Logistics team"),
        # L2-47 Documentation & Payment -> Kingdee
        ("L2-47", "kingdee", "Invoice processing, payment tracking, reconciliation",
         "primary", "api", "critical", "Finance team"),
    ]

    for link in linkages:
        proc_code, sys_key, purpose, role, method, crit, scope = link
        proc_id = process_ids.get(proc_code)
        sys_id = SYSTEM_IDS.get(sys_key)

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
                    "id": str(uuid4()), "org_id": org_id, "proc_id": proc_id,
                    "sys_id": sys_id, "purpose": purpose, "role": role,
                    "method": method, "crit": crit, "scope": scope,
                }
            )


def downgrade() -> None:
    conn = op.get_bind()

    # Remove seeded linkages
    for sys_id in SYSTEM_IDS.values():
        conn.execute(
            sa.text("DELETE FROM process_system WHERE system_id = :sys_id"),
            {"sys_id": sys_id}
        )

    # Remove seeded systems
    for sys_id in SYSTEM_IDS.values():
        conn.execute(
            sa.text("DELETE FROM system_catalogue WHERE id = :id"),
            {"id": sys_id}
        )
