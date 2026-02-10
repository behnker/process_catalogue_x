"""Seed Issue & Opportunity Log from Surity V6 Register.

Revision ID: 018
Revises: 017
Create Date: 2026-02-10

Seeds 34 operational issues (I-001 through I-034) and their linked
opportunities from Surity_Issue_Opportunity_Register_V6.docx.

Sources: 6 interview transcripts (T1-T6) + AI Fluency Survey.
Each issue mapped to the most relevant V4 process code.

Replaces the 4 sample issues from migration 010 (which were deleted
by migration 015 during V4 reseed).
"""

from alembic import op
import sqlalchemy as sa
from datetime import date
from uuid import uuid4
import json

revision = "018"
down_revision = "017"
branch_labels = None
depends_on = None


# ── Issue data from V6 register ──────────────────────────────
# Each entry maps to a V4 process code for process_id lookup.
# Classifications: people, process, system, data
# Criticality/complexity: high, medium, low

V6_ISSUES = [
    {
        "ref": "I-001",
        "title": "Manual Data Entry Across Systems",
        "description": (
            "Same data entered into ERP/BSM/MDM/PIM/SAP/client systems. "
            "30-50+ fields/SKU, 5-10+ min each. Audit app separate. "
            "Different client templates (Maxeda, Bunnings, Pindom)."
        ),
        "classification": "system",
        "criticality": "high",
        "complexity": "high",
        "process_code": "2.8.5",  # Data Management
        "opp_flag": True,
        "opp_desc": "Intelligent Data Entry & System Sync: canonical data layer, mapping engine, Excel front-end+backend, audit-ERP sync",
        "opp_benefit": "60-70% entry reduction",
        "opp_roles": ["All ops"],
    },
    {
        "ref": "I-002",
        "title": "Artwork & AWCL Verification",
        "description": (
            "Excel AWCL not linked to artwork. 3-team review. Regression errors. "
            "No field-level diffs. Packaging engineers miss required icons/spec items."
        ),
        "classification": "process",
        "criticality": "high",
        "complexity": "high",
        "process_code": "4.2.2",  # Artwork Development
        "opp_flag": True,
        "opp_desc": "Automated Artwork Verification: PDF+AWCL comparison, OCR+layout, side-by-side overlay, version diff, icon recognition",
        "opp_benefit": "50%+ cycle reduction",
        "opp_roles": ["Artwork", "QA", "Sourcing", "Packaging"],
    },
    {
        "ref": "I-003",
        "title": "Data Inconsistency & LC Recalculation",
        "description": "Dimensions/CBM/freight change frequently. Repeated landed cost recalculation required.",
        "classification": "data",
        "criticality": "high",
        "complexity": "medium",
        "process_code": "1.2.5",  # Total Landed Cost Modeling
        "opp_flag": True,
        "opp_desc": "LC Auto-Recalculation: centralised FOB/carton/CBM/freight, auto-recalc, delta reports",
        "opp_benefit": "Real-time margin visibility",
        "opp_roles": ["Commercial", "Supply Chain"],
    },
    {
        "ref": "I-004",
        "title": "Report Generation & KPI Consolidation",
        "description": "Manual pivot consolidation. Different hierarchies/fiscal years across clients.",
        "classification": "system",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "2.5.2",  # Internal Budgeting & Forecasting
        "opp_flag": True,
        "opp_desc": "BI Dashboard & AI Reporting: Power BI, standardised datasets, AI narratives, KPI dictionary",
        "opp_benefit": "Eliminate manual pivots",
        "opp_roles": ["All depts"],
    },
    {
        "ref": "I-005",
        "title": "Order Amendment Friction",
        "description": "No automated interface for some clients. Manual processing of order changes.",
        "classification": "process",
        "criticality": "medium",
        "complexity": "low",
        "process_code": "5.1.1",  # Order Processing
        "opp_flag": True,
        "opp_desc": "Order Amendment Orchestration: parse reports, detect amendments, dashboard, push to systems",
        "opp_benefit": "Reduce error rate",
        "opp_roles": ["Supply Chain", "Commercial"],
    },
    {
        "ref": "I-006",
        "title": "Supplier Discovery Time",
        "description": "~1 week to find new suppliers. No automated shortlisting.",
        "classification": "process",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "3.3.1",  # Vendor Identification & Selection
        "opp_flag": True,
        "opp_desc": "AI Supplier Discovery: AI search, scoring, image matching",
        "opp_benefit": "1 week reduced to days",
        "opp_roles": ["Sourcing"],
    },
    {
        "ref": "I-007",
        "title": "Document Comparison & Validation",
        "description": "Manual Excel/spec comparison across documents.",
        "classification": "process",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "4.1.1",  # Technical File Completion
        "opp_flag": True,
        "opp_desc": "Automated Artwork Verification: PDF+AWCL comparison, OCR+layout, version diff",
        "opp_benefit": "Reduce manual cross-validation",
        "opp_roles": ["QA", "Sourcing", "Artwork"],
    },
    {
        "ref": "I-008",
        "title": "Multi-Language Translation",
        "description": (
            "Non-native checking. OCR issues. Google Translate used as fallback "
            "for marketing copy - quality risk."
        ),
        "classification": "process",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "4.3.1",  # Instruction Manual Development
        "opp_flag": True,
        "opp_desc": "Multi-Language Translation & Copy: context-aware translation, packaging workflow, AI-assisted copy generation",
        "opp_benefit": "Faster EU approval + faster go-to-market content",
        "opp_roles": ["Artwork", "QA", "Sourcing"],
    },
    {
        "ref": "I-009",
        "title": "Product Spec & Tech File Compilation",
        "description": "TPS/PIMDAM compiled from multiple sources. Blocks shipment.",
        "classification": "process",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "4.1.1",  # Technical File Completion
        "opp_flag": True,
        "opp_desc": "Tech File Auto-Population: AI from BOM/test reports to TPS/PIMDAM",
        "opp_benefit": "Faster tech files",
        "opp_roles": ["QA", "Technical"],
    },
    {
        "ref": "I-010",
        "title": "Spreadsheet Overhead & Duplicates",
        "description": "Multiple trackers with no single source of truth. Root systemic constraint.",
        "classification": "system",
        "criticality": "high",
        "complexity": "high",
        "process_code": "2.8.5",  # Data Management
        "opp_flag": True,
        "opp_desc": "Intelligent Data Entry & System Sync: canonical data layer, mapping engine, central master-data export",
        "opp_benefit": "Eliminate duplicate trackers",
        "opp_roles": ["All ops"],
    },
    {
        "ref": "I-011",
        "title": "RFQ Process Inefficiency",
        "description": "One-by-one dispatch of RFQs. No bulk processing.",
        "classification": "process",
        "criticality": "low",
        "complexity": "low",
        "process_code": "3.4.1",  # Tender & Quotation Management
        "opp_flag": True,
        "opp_desc": "Automated RFQ Dispatch: bulk dispatch, auto-validate, flag exceptions",
        "opp_benefit": "Faster quotation cycle",
        "opp_roles": ["Sourcing"],
    },
    {
        "ref": "I-012",
        "title": "Shipping & 3PL Data Manual Handling",
        "description": "Multiple 3PL formats. ~Half day per client per week for manual processing.",
        "classification": "system",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "5.4.1",  # Shipment Preparation & Delivery
        "opp_flag": True,
        "opp_desc": "3PL Shipping ETL & Upload: ETL 3PL formats to ERP, daily upload",
        "opp_benefit": "Half-day per client per week saved",
        "opp_roles": ["Supply Chain", "Logistics"],
    },
    {
        "ref": "I-013",
        "title": "Knowledge & Institutional Memory",
        "description": "No centralised knowledge base. Knowledge lost on staff departure. Repeated mistakes.",
        "classification": "people",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "2.8.2",  # Lessons Learned Repository
        "opp_flag": True,
        "opp_desc": "Surity Knowledge Base (RAG): AI KB for regulations, standards, past decisions, quotation history, vendor records",
        "opp_benefit": "Institutional memory preserved",
        "opp_roles": ["All teams"],
    },
    {
        "ref": "I-014",
        "title": "Product Master Data Fragmentation",
        "description": (
            "No central master. Category templates differ. GS codes inconsistent. "
            "Upload failures cascade downstream."
        ),
        "classification": "data",
        "criticality": "high",
        "complexity": "high",
        "process_code": "2.8.5",  # Data Management
        "opp_flag": True,
        "opp_desc": "Product Master & SKU Seeding: central master, PSR mapping, unit normalisation, seed similar SKU, GS codes",
        "opp_benefit": "Eliminate re-keying",
        "opp_roles": ["Commercial", "Sourcing", "Data"],
    },
    {
        "ref": "I-015",
        "title": "AI Tool Governance & Data Privacy",
        "description": "Multiple AI tools in use, no licensing or safeguards. Data security risk.",
        "classification": "process",
        "criticality": "medium",
        "complexity": "high",
        "process_code": "2.7.1",  # IT Infrastructure & Security
        "opp_flag": True,
        "opp_desc": "AI Tool Governance Framework: approved tools, substitutions, policy, prompts",
        "opp_benefit": "Secure AI adoption",
        "opp_roles": ["IT", "All"],
    },
    {
        "ref": "I-016",
        "title": "Image & Media Upload Failures",
        "description": (
            "Batch uploads fail with vague errors. Manual retry. "
            "Suppliers provide inconsistent/low-quality images. "
            "Professional photos outsourced. Many images per SKU slow to upload."
        ),
        "classification": "system",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "2.8.3",  # Document Library Management
        "opp_flag": True,
        "opp_desc": "Image Validation + Resilient Uploader: auto-validate size/DPI/format, per-file diagnosis, auto-resize, resumable batch, supplier photo brief",
        "opp_benefit": "Reduce rejections",
        "opp_roles": ["Data", "E-commerce", "Sourcing"],
    },
    {
        "ref": "I-017",
        "title": "Process Catalogue Needs Validation",
        "description": "L3 processes and RACI need confirmation by leadership. Blocks automation prioritisation.",
        "classification": "process",
        "criticality": "medium",
        "complexity": "low",
        "process_code": "2.2.2",  # Standard Operating Procedures
        "opp_flag": True,
        "opp_desc": "Process Catalogue Validation: finalise L3 and RACI, score automation potential",
        "opp_benefit": "Accurate targeting for automation",
        "opp_roles": ["Leadership"],
    },
    {
        "ref": "I-018",
        "title": "Inconsistent Client Systems & Email Workflows",
        "description": "Clients lack centralised system. Email-based approvals create traceability gap.",
        "classification": "system",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "1.1.2",  # Stakeholder Communication Plan
        "opp_flag": True,
        "opp_desc": "Unified POB / Artwork Platform: Surity-hosted POB, structured AWCL, POB-PIM/DAM-ERP integration, immutable audit logs",
        "opp_benefit": "Full traceability",
        "opp_roles": ["Artwork", "QA", "Client"],
    },
    {
        "ref": "I-019",
        "title": "Vendor Artwork Quality & Master Copy",
        "description": "Low-quality first drafts from vendors. Overstated marketing claims. Rework required.",
        "classification": "process",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "4.2.2",  # Artwork Development
        "opp_flag": True,
        "opp_desc": "AI Vendor Template Generation: master templates from brand manuals, icon libraries, locked templates",
        "opp_benefit": "Higher first-pass quality",
        "opp_roles": ["Artwork", "QA", "Vendors"],
    },
    {
        "ref": "I-020",
        "title": "No Visual QA Against Brand Manuals",
        "description": "Manual brand-rule checks. Missing icons not caught until late stage.",
        "classification": "process",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "4.2.2",  # Artwork Development
        "opp_flag": True,
        "opp_desc": "AI Visual QA / Brand Checks: computer vision for deviations, icon recognition for missing required elements",
        "opp_benefit": "Catch errors before print",
        "opp_roles": ["Artwork", "QA", "Packaging"],
    },
    {
        "ref": "I-021",
        "title": "Internal Tools Localisation & Complexity",
        "description": "Chinese audit app. Complex interface for external users. Slows reviews.",
        "classification": "system",
        "criticality": "low",
        "complexity": "medium",
        "process_code": "2.7.3",  # ERP/Audit Application Administration
        "opp_flag": True,
        "opp_desc": "Internal Tools Localisation & UX: UI improvements, translations, guided tours, performance",
        "opp_benefit": "Faster reviews",
        "opp_roles": ["QA", "Vendors"],
    },
    {
        "ref": "I-022",
        "title": "Audit App Not Integrated with ERP",
        "description": "Separate records in audit app and ERP. Manual re-entry required. Duplicate entry.",
        "classification": "system",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "2.7.3",  # ERP/Audit Application Administration
        "opp_flag": True,
        "opp_desc": "Intelligent Data Entry & System Sync: audit-ERP sync component",
        "opp_benefit": "Eliminate duplicate entry",
        "opp_roles": ["QA", "IT"],
    },
    {
        "ref": "I-023",
        "title": "Audit Evidence Management Burden",
        "description": "50-100+ photos/videos per audit. No indexing. Slow review.",
        "classification": "process",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "3.5.1",  # Factory Audit Execution
        "opp_flag": True,
        "opp_desc": "Audit Evidence AI Tagging: ML auto-tag photos/videos, gallery, clip previews",
        "opp_benefit": "Speed review",
        "opp_roles": ["QA Inspectors"],
    },
    {
        "ref": "I-024",
        "title": "Audit Follow-Up & CAPA Ad Hoc",
        "description": "Ad hoc escalation. Manual scheduling. Inconsistent follow-up.",
        "classification": "process",
        "criticality": "medium",
        "complexity": "low",
        "process_code": "2.2.3",  # CAPA System
        "opp_flag": True,
        "opp_desc": "CAPA Workflow Automation: assignment, deadlines, tracking, escalation, auto-schedule",
        "opp_benefit": "Consistent follow-up",
        "opp_roles": ["QA", "Sourcing"],
    },
    {
        "ref": "I-025",
        "title": "Cross-Category Audit Visibility Gap",
        "description": "Teams treat same factory differently across categories. Duplicate audit effort.",
        "classification": "process",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "3.5.1",  # Factory Audit Execution
        "opp_flag": True,
        "opp_desc": "Cross-Category Audit Visibility: standardised checklists, scorecards+rationale",
        "opp_benefit": "Eliminate duplicate audits",
        "opp_roles": ["All categories"],
    },
    {
        "ref": "I-026",
        "title": "AWCL Ownership & Accountability Gap",
        "description": "No single owner for AWCL. Late-stage changes cause regression errors.",
        "classification": "process",
        "criticality": "medium",
        "complexity": "low",
        "process_code": "4.2.2",  # Artwork Development
        "opp_flag": True,
        "opp_desc": "AWCL Ownership SLAs & Pre-Flight QA: single owner, vendor SLAs, pre-flight QA, role-based workflow",
        "opp_benefit": "Clear accountability",
        "opp_roles": ["Artwork", "Sourcing", "QA"],
    },
    {
        "ref": "I-027",
        "title": "Poor Vendor Data Quality & Back-and-Forth",
        "description": "Incomplete/incorrect specs from vendors. Multiple chase/correct/re-request cycles.",
        "classification": "data",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "2.1.1",  # Supplier Onboarding & Vetting
        "opp_flag": True,
        "opp_desc": "Vendor Data Portal: structured forms, validation rules, cert checks, onboarding/training",
        "opp_benefit": "80%+ first-time pass rate",
        "opp_roles": ["Sourcing", "QA", "Packaging"],
    },
    {
        "ref": "I-028",
        "title": "No Version Diff / Field-Level Change Trail",
        "description": "No field-level diff capability. Full re-reviews needed on every change. Wasted effort.",
        "classification": "system",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "2.8.3",  # Document Library Management
        "opp_flag": True,
        "opp_desc": "Automated Artwork Verification: version diff component with field-level change tracking",
        "opp_benefit": "Eliminate full re-reviews",
        "opp_roles": ["Artwork", "QA", "Sourcing"],
    },
    {
        "ref": "I-029",
        "title": "Complex Category Attributes & Specialist Validation",
        "description": "GS codes differ by family. dB, IP ratings need certs. Compliance risk.",
        "classification": "process",
        "criticality": "medium",
        "complexity": "high",
        "process_code": "4.1.2",  # Testing & Sealing
        "opp_flag": True,
        "opp_desc": "AI Cross-Check & Attribute Extraction: parse specs, extract attributes, flag inconsistencies, marketing claim guardrails",
        "opp_benefit": "Reduce manual cross-validation",
        "opp_roles": ["Sourcing", "QA", "Technical"],
    },
    {
        "ref": "I-030",
        "title": "Fragmented Vendor & Quotation Records",
        "description": "Quotations emailed/ad-hoc stored. Lost on departure. Knowledge loss.",
        "classification": "data",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "3.4.1",  # Tender & Quotation Management
        "opp_flag": True,
        "opp_desc": "Surity Knowledge Base (RAG): centralised quotation history + vendor records",
        "opp_benefit": "Institutional memory for quotations",
        "opp_roles": ["All sourcing"],
    },
    {
        "ref": "I-031",
        "title": "Marketing Copy & Content Creation Manual",
        "description": (
            "Writing product descriptions, marketing copy, and localised content is "
            "manual and time-consuming. Google Translate used as fallback. Error-prone. "
            "No reusable copy snippets."
        ),
        "classification": "process",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "4.3.1",  # Instruction Manual Development
        "opp_flag": True,
        "opp_desc": "AI Marketing Copy & Content Generation: AI-assisted product descriptions, controlled prompts + human review, templates per category, reusable copy snippet library, multi-language output",
        "opp_benefit": "Speed copy creation 5-10x, consistent quality",
        "opp_roles": ["Sourcing", "E-commerce", "Marketing"],
    },
    {
        "ref": "I-032",
        "title": "Poor / Incomplete Client Briefs",
        "description": (
            "Briefs from clients (esp. global sourcing teams) lack minimum requirements. "
            "Causes wasted early-stage sourcing work and rework when buyer direction changes."
        ),
        "classification": "process",
        "criticality": "medium",
        "complexity": "low",
        "process_code": "3.1.1",  # Project Brief Receipt & Alignment
        "opp_flag": True,
        "opp_desc": "Client Brief Gating Template: minimum-brief checklist with required fields + examples, intake form, gate early-stage sourcing work on brief completeness",
        "opp_benefit": "Eliminate wasted sourcing on incomplete briefs",
        "opp_roles": ["Sourcing", "Commercial"],
    },
    {
        "ref": "I-033",
        "title": "Competitor Benchmarking is Manual",
        "description": (
            "Market intelligence and competitor research done line-by-line manually. "
            "Very time consuming. No structured output format."
        ),
        "classification": "process",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "3.2.1",  # Private Label Benchmarking
        "opp_flag": True,
        "opp_desc": "AI Competitor Benchmarking: web-scraping + AI to extract competitor product attributes/prices/features, structured Excel/PPT summaries",
        "opp_benefit": "10x faster competitor analysis, structured reusable output",
        "opp_roles": ["Sourcing", "Commercial"],
    },
    {
        "ref": "I-034",
        "title": "Repeat SKU Asset Rework",
        "description": (
            "Even repeat items need new photos/packaging/marketing as client expectations evolve. "
            "No variant library or reusable asset packs."
        ),
        "classification": "process",
        "criticality": "medium",
        "complexity": "medium",
        "process_code": "2.8.1",  # Product & Category Knowledge Base
        "opp_flag": True,
        "opp_desc": "SKU Variant Library & Asset Reuse: maintain variant library per SKU, reusable asset packs, change log, quick adaptation for different clients",
        "opp_benefit": "Eliminate redundant work on known products, faster repeat-SKU turnaround",
        "opp_roles": ["Sourcing", "Artwork", "E-commerce"],
    },
]


def _get_org_id(conn) -> str | None:
    result = conn.execute(sa.text("SELECT id FROM organizations LIMIT 1"))
    row = result.fetchone()
    return str(row[0]) if row else None


def _get_user_id(conn) -> str | None:
    result = conn.execute(sa.text("SELECT id FROM users LIMIT 1"))
    row = result.fetchone()
    return str(row[0]) if row else None


def _get_process_ids(conn, org_id: str, codes: list[str]) -> dict[str, tuple[str, str, str, str]]:
    """Look up process (id, code, name, level) by code for the given org."""
    result = conn.execute(
        sa.text(
            "SELECT code, id, name, level FROM processes "
            "WHERE organization_id = :org AND code = ANY(:codes)"
        ),
        {"org": org_id, "codes": codes},
    )
    return {
        row[0]: (str(row[1]), row[0], row[2], row[3])
        for row in result.fetchall()
    }


def upgrade() -> None:
    conn = op.get_bind()

    org_id = _get_org_id(conn)
    if not org_id:
        print("  No organization found, skipping V6 issue seed")
        return

    user_id = _get_user_id(conn)
    if not user_id:
        print("  No user found, skipping V6 issue seed")
        return

    # Collect unique process codes needed
    codes = list({issue["process_code"] for issue in V6_ISSUES})
    code_map = _get_process_ids(conn, org_id, codes)

    if not code_map:
        print(f"  WARNING: No processes found for codes {codes}")
        return

    inserted = 0
    skipped = 0
    for issue in V6_ISSUES:
        proc_info = code_map.get(issue["process_code"])
        if not proc_info:
            print(f"  WARNING: Process {issue['process_code']} not found, skipping {issue['ref']}")
            skipped += 1
            continue

        process_id, process_ref, process_name, process_level = proc_info
        level_int = int(process_level[1]) if process_level.startswith("L") else 0

        roles_json = json.dumps(issue["opp_roles"])

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
                "title": issue["title"],
                "description": issue["description"],
                "classification": issue["classification"],
                "criticality": issue["criticality"],
                "complexity": issue["complexity"],
                "process_id": process_id,
                "process_level": level_int,
                "process_ref": process_ref,
                "process_name": process_name,
                "user_id": user_id,
                "date_raised": date(2026, 2, 10),
                "opp_flag": issue["opp_flag"],
                "opp_status": "identified" if issue["opp_flag"] else None,
                "opp_desc": issue["opp_desc"],
                "opp_benefit": issue["opp_benefit"],
                "opp_roles": roles_json,
            },
        )
        inserted += 1

    print(f"  Inserted {inserted} V6 issues (OPS-001 through OPS-{inserted:03d}), {skipped} skipped")

    # Verify RAG sync
    _verify_rag_sync(conn, org_id)


def _verify_rag_sync(conn, org_id: str) -> None:
    """Verify that RAG sync trigger updated process RAG columns."""
    result = conn.execute(
        sa.text("""
            SELECT code, name, rag_process, rag_system, rag_people, rag_data, rag_overall
            FROM processes
            WHERE organization_id = :org_id
              AND (rag_process != 'neutral' OR rag_system != 'neutral'
                   OR rag_people != 'neutral' OR rag_data != 'neutral')
            ORDER BY code
        """),
        {"org_id": org_id},
    )

    rows = result.fetchall()
    if rows:
        print(f"  RAG sync: {len(rows)} processes updated")
        for row in rows:
            print(f"    {row[0]} {row[1]}: P={row[2]} S={row[3]} Ppl={row[4]} D={row[5]} => {row[6]}")
    else:
        print("  Warning: No processes updated by RAG sync trigger")


def downgrade() -> None:
    conn = op.get_bind()

    org_id = _get_org_id(conn)
    if not org_id:
        return

    # Delete all seeded issues
    conn.execute(
        sa.text("DELETE FROM issue_log WHERE organization_id = :org_id"),
        {"org_id": org_id},
    )

    # Reset RAG columns
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

    print("  Removed V6 issues and reset RAG columns")
