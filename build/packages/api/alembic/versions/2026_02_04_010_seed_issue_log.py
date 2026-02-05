"""Seed Issue Log with sample operational issues.

Revision ID: 010
Revises: 009
Create Date: 2026-02-04

Seeds 4 sample issues mapped from spec examples AP-001 through AP-004.
After insert, the trg_issue_rag_sync trigger auto-updates process RAG.

Expected RAG state after seed:
- L2-05 Data Mgmt: rag_system=red, rag_people=amber, rag_data=amber
- L3-11 Prod Data: rag_data=amber
- L2-22 Audit CAP: rag_process=red
"""

from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from datetime import date

revision = "010"
down_revision = "009"
branch_labels = None
depends_on = None


# Sample issues from spec (mapped from AP- to OPS- prefix)
SAMPLE_ISSUES = [
    {
        "title": "ERP system frequently crashes during peak hours",
        "description": "The ERP system experiences crashes 2-3 times per week during peak processing hours (9am-11am), causing data loss and requiring manual recovery.",
        "classification": "system",
        "criticality": "high",
        "complexity": "high",
        "process_path": "SUPPORT|Data, Systems & Reporting|Data Management",
        "opportunity_flag": True,
        "opportunity_description": "Upgrade ERP infrastructure to cloud-hosted solution",
        "opportunity_expected_benefit": "99.9% uptime, automatic failover, reduced maintenance burden",
        "opportunity_beneficiary_roles": ["IT Team", "Operations", "All Staff"],
    },
    {
        "title": "Staff lack training on new data validation procedures",
        "description": "New data validation procedures were introduced but only 40% of staff have been trained. This leads to inconsistent data quality.",
        "classification": "people",
        "criticality": "medium",
        "complexity": "low",
        "process_path": "SUPPORT|Data, Systems & Reporting|Data Management",
        "opportunity_flag": True,
        "opportunity_description": "Create e-learning module for data validation",
        "opportunity_expected_benefit": "100% staff trained within 30 days, consistent application of procedures",
        "opportunity_beneficiary_roles": ["Training Team", "Operations"],
    },
    {
        "title": "Product master data has duplicate records",
        "description": "Approximately 15% of product records have duplicates due to lack of deduplication rules. This causes reporting inaccuracies.",
        "classification": "data",
        "criticality": "medium",
        "complexity": "medium",
        "process_path": "SUPPORT|Data, Systems & Reporting|Product Data Management",
        "opportunity_flag": False,
        "opportunity_description": None,
        "opportunity_expected_benefit": None,
        "opportunity_beneficiary_roles": [],
    },
    {
        "title": "Audit CAP process lacks documented escalation path",
        "description": "When audit findings require escalation, there is no documented process for who to escalate to and when. This leads to delays in addressing critical findings.",
        "classification": "process",
        "criticality": "high",
        "complexity": "low",
        "process_path": "SOURCE|Factory Audit Programs|Audit CAP Management",
        "opportunity_flag": True,
        "opportunity_description": "Create escalation matrix with automated alerts",
        "opportunity_expected_benefit": "Clear accountability, reduced resolution time by 50%",
        "opportunity_beneficiary_roles": ["Quality Team", "Management"],
    },
]


def upgrade() -> None:
    conn = op.get_bind()

    # Get the first organization (Surity)
    org_result = conn.execute(sa.text("SELECT id FROM organizations LIMIT 1"))
    org_row = org_result.fetchone()
    if not org_row:
        print("  No organization found, skipping issue seeding")
        return

    org_id = str(org_row[0])

    # Get the first user (for raised_by and created_by)
    user_result = conn.execute(sa.text("SELECT id FROM users LIMIT 1"))
    user_row = user_result.fetchone()
    if not user_row:
        print("  No user found, skipping issue seeding")
        return

    user_id = str(user_row[0])

    # Build process path lookup
    process_map = _build_process_map(conn, org_id)

    inserted = 0
    for issue_data in SAMPLE_ISSUES:
        process_path = issue_data["process_path"]
        process_info = process_map.get(process_path)

        if not process_info:
            print(f"  Process not found for path: {process_path}")
            continue

        process_id, process_code, process_name, process_level = process_info

        # Convert level string to int
        level_int = int(process_level[1]) if process_level.startswith("L") else 0

        # Build beneficiary roles as JSONB
        import json
        roles_json = json.dumps(issue_data["opportunity_beneficiary_roles"])

        # Insert issue (trigger will assign issue_number)
        conn.execute(
            sa.text("""
                INSERT INTO issue_log (
                    id, organization_id, title, description,
                    issue_classification, issue_criticality, issue_complexity,
                    issue_status, process_id, process_level, process_ref, process_name,
                    raised_by_id, date_raised,
                    opportunity_flag, opportunity_status, opportunity_description,
                    opportunity_expected_benefit, opportunity_beneficiary_roles,
                    created_by
                ) VALUES (
                    :id, :org_id, :title, :description,
                    :classification, :criticality, :complexity,
                    'open', :process_id, :process_level, :process_ref, :process_name,
                    :user_id, :date_raised,
                    :opp_flag, :opp_status, :opp_desc,
                    :opp_benefit, CAST(:opp_roles AS jsonb),
                    :user_id
                )
            """),
            {
                "id": str(uuid4()),
                "org_id": org_id,
                "title": issue_data["title"],
                "description": issue_data["description"],
                "classification": issue_data["classification"],
                "criticality": issue_data["criticality"],
                "complexity": issue_data["complexity"],
                "process_id": process_id,
                "process_level": level_int,
                "process_ref": process_code,
                "process_name": process_name,
                "user_id": user_id,
                "date_raised": date.today(),
                "opp_flag": issue_data["opportunity_flag"],
                "opp_status": "identified" if issue_data["opportunity_flag"] else None,
                "opp_desc": issue_data["opportunity_description"],
                "opp_benefit": issue_data["opportunity_expected_benefit"],
                "opp_roles": roles_json,
            },
        )
        inserted += 1

    print(f"  Inserted {inserted} sample issues (OPS-001 through OPS-{inserted:03d})")

    # Verify RAG sync worked
    _verify_rag_sync(conn, org_id)


def _build_process_map(conn, org_id: str) -> dict:
    """Build mapping of process paths to (id, code, name, level)."""
    result = conn.execute(
        sa.text("""
            WITH RECURSIVE process_tree AS (
                SELECT id, code, name, level, parent_id,
                       CAST(name AS TEXT) AS path
                FROM processes
                WHERE parent_id IS NULL AND organization_id = :org_id
                UNION ALL
                SELECT p.id, p.code, p.name, p.level, p.parent_id,
                       CAST(pt.path || '|' || p.name AS TEXT)
                FROM processes p
                JOIN process_tree pt ON p.parent_id = pt.id
                WHERE p.organization_id = :org_id
            )
            SELECT id, code, name, level, path FROM process_tree
        """),
        {"org_id": org_id},
    )

    return {
        row.path: (str(row.id), row.code, row.name, row.level)
        for row in result.fetchall()
    }


def _verify_rag_sync(conn, org_id: str) -> None:
    """Verify that RAG sync trigger updated process RAG columns."""
    result = conn.execute(
        sa.text("""
            SELECT code, name, rag_process, rag_system, rag_people, rag_data, rag_overall
            FROM processes
            WHERE organization_id = :org_id
              AND (rag_process != 'neutral' OR rag_system != 'neutral'
                   OR rag_people != 'neutral' OR rag_data != 'neutral')
        """),
        {"org_id": org_id},
    )

    rows = result.fetchall()
    if rows:
        print("  RAG sync results:")
        for row in rows:
            print(f"    {row.code} {row.name}: "
                  f"process={row.rag_process}, system={row.rag_system}, "
                  f"people={row.rag_people}, data={row.rag_data}, "
                  f"overall={row.rag_overall}")
    else:
        print("  Warning: No processes updated by RAG sync trigger")


def downgrade() -> None:
    conn = op.get_bind()

    # Get the first organization
    org_result = conn.execute(sa.text("SELECT id FROM organizations LIMIT 1"))
    org_row = org_result.fetchone()
    if not org_row:
        return

    org_id = str(org_row[0])

    # Delete seeded issues
    conn.execute(
        sa.text("DELETE FROM issue_log WHERE organization_id = :org_id"),
        {"org_id": org_id},
    )

    # Reset RAG columns on all processes
    conn.execute(
        sa.text("""
            UPDATE processes
            SET rag_process = 'neutral',
                rag_system = 'neutral',
                rag_people = 'neutral',
                rag_data = 'neutral'
            WHERE organization_id = :org_id
        """),
        {"org_id": org_id},
    )
