"""Seed Business Model Canvas — Markets, Clients & Services.

Revision ID: 012
Revises: 011
Create Date: 2026-02-08

Seeds Surity's BMC with customer segments (client portfolio),
value propositions (product categories), and key activities (service scope).
Idempotent: SELECT-before-INSERT guards prevent duplicates.
"""

from alembic import op
import sqlalchemy as sa
from uuid import uuid4

revision = "012"
down_revision = "011"
branch_labels = None
depends_on = None


CUSTOMER_SEGMENTS = [
    {
        "title": "UK Market — Selco Builders Warehouse",
        "description": "Trade-focused builders merchant. Transformed import supply chains with Surity. Strong Own Brands. Direct sourcing critical to commercial goals.",
        "sort_order": 1,
    },
    {
        "title": "EU Market — Maxeda DIY Group",
        "description": "Praxis and Brico brands (Netherlands/Belgium). Transformed import supply chains with Surity. Strong Own Brands. Direct sourcing critical to commercial goals.",
        "sort_order": 2,
    },
    {
        "title": "AU — Bunnings",
        "description": "Australia's largest home improvement retailer. Transformed import supply chains with Surity. Strong Own Brands. Direct sourcing critical to commercial goals.",
        "sort_order": 3,
    },
    {
        "title": "NZ — Fletcher Building",
        "description": "NZ-based building products. Transformed import supply chains with Surity. Strong Own Brands. Direct sourcing critical to commercial goals.",
        "sort_order": 4,
    },
    {
        "title": "AU — Tradelink",
        "description": "Plumbing and bathroom supplies. Transformed import supply chains with Surity. Strong Own Brands. Direct sourcing critical to commercial goals.",
        "sort_order": 5,
    },
    {
        "title": "AU — Oliveri",
        "description": "Kitchen and laundry products. Transformed import supply chains with Surity. Strong Own Brands. Direct sourcing critical to commercial goals.",
        "sort_order": 6,
    },
]

VALUE_PROPOSITIONS = [
    {
        "title": "Technical (DIY & Trade)",
        "description": "Hand tools, power tools, fixings, hardware, workshop equipment, lighting, building materials, electrical, plumbing.",
        "sort_order": 1,
    },
    {
        "title": "Showroom (Bathroom & Kitchen)",
        "description": "Faucets, showering, sanitary ware, bathroom furniture, kitchen sinks, tiling & flooring, bathroom accessories, kitchen accessories.",
        "sort_order": 2,
    },
    {
        "title": "Seasonal (Garden & Outdoor)",
        "description": "Outdoor living furniture, outdoor dining, maintenance equipment, garden tools, watering, propagation, landscape & décor, bird care, pools & leisure.",
        "sort_order": 3,
    },
    {
        "title": "Home (Interior)",
        "description": "Furniture, storage solutions, soft furnishings, home comfort, decorative lighting, décor items, Christmas/seasonal décor, cleaning products, home accessories.",
        "sort_order": 4,
    },
]

KEY_ACTIVITIES = [
    {
        "title": "Source",
        "description": "Supplier identification and vetting, quotation management, contract negotiation, vendor engagement.",
        "sort_order": 1,
    },
    {
        "title": "Develop",
        "description": "Technical & CSR factory audits, product specification, testing & sealing (Gold Seal), artwork & packaging development.",
        "sort_order": 2,
    },
    {
        "title": "Execute",
        "description": "Order management, production management, quality inspection, freight coordination (to origin port).",
        "sort_order": 3,
    },
    {
        "title": "Support",
        "description": "Document library maintenance, data management, KPI reporting, payment & finance facilitation.",
        "sort_order": 4,
    },
]

BMC_ENTRIES = [
    ("customer_segments", CUSTOMER_SEGMENTS),
    ("value_propositions", VALUE_PROPOSITIONS),
    ("key_activities", KEY_ACTIVITIES),
]


def upgrade() -> None:
    conn = op.get_bind()

    # Get org
    org_row = conn.execute(sa.text("SELECT id FROM organizations LIMIT 1")).fetchone()
    if not org_row:
        print("  No organization found, skipping BMC seeding")
        return

    org_id = str(org_row[0])

    # Get or create default business model
    bm_row = conn.execute(
        sa.text(
            "SELECT id FROM business_models WHERE organization_id = :org LIMIT 1"
        ),
        {"org": org_id},
    ).fetchone()

    if bm_row:
        bm_id = str(bm_row[0])
    else:
        bm_id = str(uuid4())
        conn.execute(
            sa.text("""
                INSERT INTO business_models (id, organization_id, name, description, status, created_at, updated_at)
                VALUES (:id, :org, 'Surity Business Model', 'Surity sourcing agent BMC — markets, clients & services', 'active', NOW(), NOW())
            """),
            {"id": bm_id, "org": org_id},
        )
        print(f"  Created business model {bm_id}")

    inserted = 0

    for component, entries in BMC_ENTRIES:
        for entry in entries:
            # Idempotent: skip if title already exists for this component
            existing = conn.execute(
                sa.text("""
                    SELECT id FROM business_model_entries
                    WHERE business_model_id = :bm AND component = :comp AND title = :title
                """),
                {"bm": bm_id, "comp": component, "title": entry["title"]},
            ).fetchone()

            if existing:
                continue

            conn.execute(
                sa.text("""
                    INSERT INTO business_model_entries
                        (id, organization_id, business_model_id, component, title, description, sort_order, created_at, updated_at)
                    VALUES
                        (:id, :org, :bm, :comp, :title, :desc, :sort, NOW(), NOW())
                """),
                {
                    "id": str(uuid4()),
                    "org": org_id,
                    "bm": bm_id,
                    "comp": component,
                    "title": entry["title"],
                    "desc": entry["description"],
                    "sort": entry["sort_order"],
                },
            )
            inserted += 1

    print(f"  Seeded {inserted} BMC entries across 3 components (idempotent)")


def downgrade() -> None:
    conn = op.get_bind()

    # Delete entries seeded by this migration (by matching the business model)
    org_row = conn.execute(sa.text("SELECT id FROM organizations LIMIT 1")).fetchone()
    if not org_row:
        return

    org_id = str(org_row[0])

    bm_row = conn.execute(
        sa.text(
            "SELECT id FROM business_models WHERE organization_id = :org LIMIT 1"
        ),
        {"org": org_id},
    ).fetchone()

    if not bm_row:
        return

    bm_id = str(bm_row[0])

    # Delete entries for the three seeded components
    result = conn.execute(
        sa.text("""
            DELETE FROM business_model_entries
            WHERE business_model_id = :bm
              AND component IN ('customer_segments', 'value_propositions', 'key_activities')
        """),
        {"bm": bm_id},
    )
    print(f"  Removed {result.rowcount} BMC entries")
