"""Seed Timing & SLA data from Surity Operating Model Excel.

Revision ID: 017
Revises: 016
Create Date: 2026-02-10

Seeds 11 timing/SLA entries across 9 processes (7 L2 + 2 L3) from
Surity_Process_Catalogue_Operating_Model.xlsx → Timing & SLA sheet.

Processes are matched by V4 code (dot-notation) looked up at runtime.
"""

from alembic import op
import sqlalchemy as sa
from uuid import uuid4

revision = "017"
down_revision = "016"
branch_labels = None
depends_on = None


# ── Seed data ────────────────────────────────────────────────
# Mapped from Excel V3 IDs to V4 process codes by name match.

TIMING_ENTRIES = [
    {
        "process_code": "2.8.5",  # Data Management
        "name": "Data Entry Cycle Time",
        "frequency": "continuous",
        "volume_per_period": "500 SKUs/month",
        "cycle_time_target": "24 hours",
        "cycle_time_actual": "32 hours",
        "sla_commitment": "Data entered within 48 hours",
        "trigger_event": "New product/supplier onboarding",
        "dependencies": "Vendor data receipt",
        "peak_season": "Aug-Oct (new range launch)",
    },
    {
        "process_code": "2.8.5.1",  # Reference Data Management (was Product Data Maintenance L3-11)
        "name": "Product Data Update SLA",
        "frequency": "daily",
        "volume_per_period": "50 updates/day",
        "cycle_time_target": "4 hours",
        "cycle_time_actual": "6 hours",
        "sla_commitment": "Updates processed same day",
        "trigger_event": "Supplier sends updated specs",
        "dependencies": "Quality approval",
        "peak_season": "Jul-Sep (pre-season prep)",
    },
    {
        "process_code": "3.1.1",  # Project Brief Receipt & Alignment (was Brief L2-10)
        "name": "Brief Capture SLA",
        "frequency": "per_order",
        "volume_per_period": "8 briefs/month",
        "cycle_time_target": "3 days",
        "cycle_time_actual": "5 days",
        "sla_commitment": "Brief captured within 5 days",
        "trigger_event": "Client initiates project",
        "dependencies": "Client availability",
        "peak_season": "Jan-Mar (new season planning)",
    },
    {
        "process_code": "3.5.1",  # Factory Audit Execution (was Surity Audit L2-20)
        "name": "Audit Report Turnaround",
        "frequency": "per_order",
        "volume_per_period": "20 audits/month",
        "cycle_time_target": "7 days",
        "cycle_time_actual": "9 days",
        "sla_commitment": "Audit report within 10 days",
        "trigger_event": "New vendor onboarding",
        "dependencies": "Factory access, auditor availability",
        "peak_season": "Apr-Jun (new vendor season)",
    },
    {
        "process_code": "3.5.1.3",  # On-Site 5 Pillars Assessment
        "name": "On-Site Audit Duration",
        "frequency": "per_order",
        "volume_per_period": "20 audits/month",
        "cycle_time_target": "1 day",
        "cycle_time_actual": "1.5 days",
        "sla_commitment": "On-site audit completed in 1 day",
        "trigger_event": "Audit scheduled",
        "dependencies": "Travel to China",
        "peak_season": "Apr-Jun",
    },
    {
        "process_code": "4.1.2",  # Testing & Sealing (was Test Specification & Validation L2-28)
        "name": "Test Report Turnaround",
        "frequency": "per_order",
        "volume_per_period": "100 tests/month",
        "cycle_time_target": "14 days",
        "cycle_time_actual": "18 days",
        "sla_commitment": "Test reports received within 21 days",
        "trigger_event": "Silver Seal sample submitted",
        "dependencies": "Lab capacity, sample shipment",
        "peak_season": "May-Aug (GSS deadline push)",
    },
    {
        "process_code": "5.1.1",  # Order Processing (was Order Management L2-37)
        "name": "PO Confirmation SLA",
        "frequency": "continuous",
        "volume_per_period": "200 orders/month",
        "cycle_time_target": "1.5 days",
        "cycle_time_actual": "2 days",
        "sla_commitment": "PO confirmed within 3 days",
        "trigger_event": "Client places order",
        "dependencies": "Vendor confirmation",
        "peak_season": "Feb-Apr, Sep-Nov (pre-delivery windows)",
    },
    {
        "process_code": "5.1.1.7",  # Proforma Order Generation & Issuance (was Proforma Order Review L3-53)
        "name": "Proforma Review SLA",
        "frequency": "per_order",
        "volume_per_period": "200 orders/month",
        "cycle_time_target": "1 day",
        "cycle_time_actual": "1.5 days",
        "sla_commitment": "Proforma reviewed in 3 days",
        "trigger_event": "Vendor sends proforma",
        "dependencies": "Client approval if changes",
        "peak_season": "Feb-Apr, Sep-Nov",
    },
    {
        "process_code": "5.3.1",  # Pre-Shipment Inspection (was Inspection L2-39)
        "name": "Inspection Report SLA",
        "frequency": "per_order",
        "volume_per_period": "180 inspections/month",
        "cycle_time_target": "0.5 days",
        "cycle_time_actual": "0.75 days",
        "sla_commitment": "Report issued within 24 hours",
        "trigger_event": "100% production complete",
        "dependencies": "Vendor notification, inspector availability",
        "peak_season": "Mar-May, Oct-Dec (shipping windows)",
    },
    {
        "process_code": "5.4.1",  # Shipment Preparation & Delivery (was Shipment Booking L2-44)
        "name": "Booking Confirmation SLA",
        "frequency": "continuous",
        "volume_per_period": "160 shipments/month",
        "cycle_time_target": "1 day",
        "cycle_time_actual": "1.5 days",
        "sla_commitment": "Booking confirmed 15 days pre-shipment",
        "trigger_event": "Inspection passed",
        "dependencies": "3PL capacity, vessel schedule",
        "peak_season": "Apr-Jun, Nov-Jan (peak shipping)",
    },
    {
        "process_code": "5.5.2",  # Payment Processing (was Documentation & Payment L2-47)
        "name": "Payment Cycle Time",
        "frequency": "per_order",
        "volume_per_period": "160 shipments/month",
        "cycle_time_target": "30 days",
        "cycle_time_actual": "35 days",
        "sla_commitment": "Payment within 30 days of GR",
        "trigger_event": "Goods received at destination",
        "dependencies": "Document accuracy, client approval",
        "peak_season": "May-Jul, Dec-Feb (post-arrival)",
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
        print("  No organization found, skipping timing seed")
        return

    # Collect unique process codes needed
    codes = list({t["process_code"] for t in TIMING_ENTRIES})
    code_to_id = _get_process_ids(conn, org_id, codes)

    if not code_to_id:
        print(f"  WARNING: No processes found for codes {codes}")
        return

    inserted = 0
    skipped = 0
    for entry in TIMING_ENTRIES:
        process_id = code_to_id.get(entry["process_code"])
        if not process_id:
            print(f"  WARNING: Process {entry['process_code']} not found, skipping '{entry['name']}'")
            skipped += 1
            continue

        conn.execute(
            sa.text("""
                INSERT INTO process_timing
                    (id, organization_id, process_id, name, frequency,
                     volume_per_period, cycle_time_target, cycle_time_actual,
                     sla_commitment, trigger_event, dependencies, peak_season)
                VALUES
                    (:id, :org_id, :proc_id, :name, :frequency,
                     :volume, :target, :actual,
                     :sla, :trigger, :deps, :peak)
            """),
            {
                "id": str(uuid4()),
                "org_id": org_id,
                "proc_id": process_id,
                "name": entry["name"],
                "frequency": entry["frequency"],
                "volume": entry["volume_per_period"],
                "target": entry["cycle_time_target"],
                "actual": entry["cycle_time_actual"],
                "sla": entry["sla_commitment"],
                "trigger": entry["trigger_event"],
                "deps": entry["dependencies"],
                "peak": entry["peak_season"],
            },
        )
        inserted += 1

    print(f"  Inserted {inserted} timing entries ({skipped} skipped)")


def downgrade() -> None:
    conn = op.get_bind()
    org_id = _get_org_id(conn)
    if not org_id:
        return

    conn.execute(
        sa.text("DELETE FROM process_timing WHERE organization_id = :org"),
        {"org": org_id},
    )
    print("  Removed seeded timing entries")
