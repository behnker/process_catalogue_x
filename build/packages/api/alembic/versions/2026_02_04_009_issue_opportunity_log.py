"""Issue & Opportunity Log with RAG Process Alignment.

Revision ID: 009
Revises: 008
Create Date: 2026-02-04

Implements:
- Issue Log table with OPS- prefix auto-numbering
- Issue history tracking with DB triggers
- 7 RAG columns on processes table
- Heatmap views for process-issue visualization
- RAG sync trigger (issue criticality -> process RAG)

Sources:
- Additional Design Documents/ISSUE_OPPORTUNITY_LOG_SPEC.docx
- Additional Design Documents/RAG_Issue_Alignment_Addendum.docx
- Additional Design Documents/Implementation_Amendments.docx (AMD-01, AMD-02)
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "009"
down_revision = "008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ═══════════════════════════════════════════════════════════════════════
    # PART 1: Create enum types
    # ═══════════════════════════════════════════════════════════════════════

    op.execute("""
        CREATE TYPE issue_classification AS ENUM ('people', 'process', 'system', 'data')
    """)

    op.execute("""
        CREATE TYPE issue_criticality AS ENUM ('high', 'medium', 'low')
    """)

    op.execute("""
        CREATE TYPE issue_complexity AS ENUM ('high', 'medium', 'low')
    """)

    op.execute("""
        CREATE TYPE issue_status AS ENUM (
            'open', 'in_progress', 'resolved', 'closed', 'deferred'
        )
    """)

    op.execute("""
        CREATE TYPE opportunity_status AS ENUM (
            'identified', 'evaluating', 'approved', 'in_delivery', 'delivered', 'rejected'
        )
    """)

    op.execute("""
        CREATE TYPE rag_status AS ENUM ('red', 'amber', 'green', 'neutral')
    """)

    # ═══════════════════════════════════════════════════════════════════════
    # PART 2: Create issue_log table
    # ═══════════════════════════════════════════════════════════════════════

    op.create_table(
        "issue_log",
        # Primary key and tenant
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("organizations.id"), nullable=False, index=True),

        # Auto-incrementing issue number (per org)
        sa.Column("issue_number", sa.Integer, nullable=False),

        # Core fields
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),

        # Classification (separate enum from RIADA - allows independent evolution)
        sa.Column("issue_classification",
                  postgresql.ENUM('people', 'process', 'system', 'data',
                                  name='issue_classification', create_type=False),
                  nullable=False),
        sa.Column("issue_criticality",
                  postgresql.ENUM('high', 'medium', 'low',
                                  name='issue_criticality', create_type=False),
                  nullable=False, server_default='medium'),
        sa.Column("issue_complexity",
                  postgresql.ENUM('high', 'medium', 'low',
                                  name='issue_complexity', create_type=False),
                  nullable=False, server_default='medium'),

        # Status workflow
        sa.Column("issue_status",
                  postgresql.ENUM('open', 'in_progress', 'resolved', 'closed', 'deferred',
                                  name='issue_status', create_type=False),
                  nullable=False, server_default='open'),

        # Process linkage (denormalized for heatmap performance)
        sa.Column("process_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("processes.id"), nullable=False, index=True),
        sa.Column("process_level", sa.SmallInteger, nullable=False),  # 0-5, converted from L0-L5
        sa.Column("process_ref", sa.String(20), nullable=False),      # Frozen process.code
        sa.Column("process_name", sa.String(255), nullable=False),    # Frozen process.name

        # Ownership
        sa.Column("raised_by_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("users.id"), nullable=False),
        sa.Column("assigned_to_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("users.id")),

        # Dates
        sa.Column("date_raised", sa.Date, nullable=False, server_default=sa.func.current_date()),
        sa.Column("target_resolution_date", sa.Date),
        sa.Column("actual_resolution_date", sa.Date),

        # Resolution
        sa.Column("resolution_summary", sa.Text),

        # Opportunity tracking (when issue resolution creates improvement opportunity)
        sa.Column("opportunity_flag", sa.Boolean, server_default='false'),
        sa.Column("opportunity_status",
                  postgresql.ENUM('identified', 'evaluating', 'approved',
                                  'in_delivery', 'delivered', 'rejected',
                                  name='opportunity_status', create_type=False)),
        sa.Column("opportunity_description", sa.Text),
        sa.Column("opportunity_expected_benefit", sa.Text),
        sa.Column("opportunity_beneficiary_roles", postgresql.JSONB, server_default='[]'),  # AMD-02: JSONB not TEXT[]

        # Audit trail columns
        sa.Column("created_by", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("users.id"), nullable=False),
        sa.Column("updated_by", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("users.id")),

        # Timestamps
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Unique constraint: one issue_number per organization
    op.create_index(
        "ix_issue_log_org_number",
        "issue_log",
        ["organization_id", "issue_number"],
        unique=True
    )

    # ═══════════════════════════════════════════════════════════════════════
    # PART 3: Auto-numbering trigger for issue_number
    # ═══════════════════════════════════════════════════════════════════════

    op.execute("""
        CREATE OR REPLACE FUNCTION next_issue_number()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Get next number for this organization
            SELECT COALESCE(MAX(issue_number), 0) + 1
            INTO NEW.issue_number
            FROM issue_log
            WHERE organization_id = NEW.organization_id;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql
    """)

    op.execute("""
        CREATE TRIGGER trg_issue_number
        BEFORE INSERT ON issue_log
        FOR EACH ROW
        EXECUTE FUNCTION next_issue_number()
    """)

    # ═══════════════════════════════════════════════════════════════════════
    # PART 4: updated_at trigger
    # ═══════════════════════════════════════════════════════════════════════

    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql
    """)

    op.execute("""
        CREATE TRIGGER trg_issue_log_updated_at
        BEFORE UPDATE ON issue_log
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column()
    """)

    # ═══════════════════════════════════════════════════════════════════════
    # PART 5: Create issue_log_history table
    # ═══════════════════════════════════════════════════════════════════════

    op.create_table(
        "issue_log_history",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("issue_id", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("issue_log.id", ondelete="CASCADE"), nullable=False, index=True),

        # What changed
        sa.Column("field_name", sa.String(50), nullable=False),
        sa.Column("old_value", sa.Text),
        sa.Column("new_value", sa.Text),

        # User note explaining the change
        sa.Column("change_note", sa.Text),

        # Who and when
        sa.Column("changed_by", postgresql.UUID(as_uuid=False),
                  sa.ForeignKey("users.id"), nullable=False),
        sa.Column("changed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_index(
        "ix_issue_log_history_issue_field",
        "issue_log_history",
        ["issue_id", "field_name", "changed_at"]
    )

    # ═══════════════════════════════════════════════════════════════════════
    # PART 6: Status change logging trigger
    # ═══════════════════════════════════════════════════════════════════════

    op.execute("""
        CREATE OR REPLACE FUNCTION log_issue_status_change()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Log status changes
            IF OLD.issue_status IS DISTINCT FROM NEW.issue_status THEN
                INSERT INTO issue_log_history
                    (organization_id, issue_id, field_name, old_value, new_value, changed_by)
                VALUES
                    (NEW.organization_id, NEW.id, 'issue_status',
                     OLD.issue_status::TEXT, NEW.issue_status::TEXT,
                     COALESCE(NEW.updated_by, NEW.created_by));
            END IF;

            -- Log criticality changes
            IF OLD.issue_criticality IS DISTINCT FROM NEW.issue_criticality THEN
                INSERT INTO issue_log_history
                    (organization_id, issue_id, field_name, old_value, new_value, changed_by)
                VALUES
                    (NEW.organization_id, NEW.id, 'issue_criticality',
                     OLD.issue_criticality::TEXT, NEW.issue_criticality::TEXT,
                     COALESCE(NEW.updated_by, NEW.created_by));
            END IF;

            -- Log assigned_to changes
            IF OLD.assigned_to_id IS DISTINCT FROM NEW.assigned_to_id THEN
                INSERT INTO issue_log_history
                    (organization_id, issue_id, field_name, old_value, new_value, changed_by)
                VALUES
                    (NEW.organization_id, NEW.id, 'assigned_to_id',
                     OLD.assigned_to_id::TEXT, NEW.assigned_to_id::TEXT,
                     COALESCE(NEW.updated_by, NEW.created_by));
            END IF;

            -- Log resolution date when set
            IF OLD.actual_resolution_date IS NULL AND NEW.actual_resolution_date IS NOT NULL THEN
                INSERT INTO issue_log_history
                    (organization_id, issue_id, field_name, old_value, new_value, changed_by)
                VALUES
                    (NEW.organization_id, NEW.id, 'actual_resolution_date',
                     NULL, NEW.actual_resolution_date::TEXT,
                     COALESCE(NEW.updated_by, NEW.created_by));
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql
    """)

    op.execute("""
        CREATE TRIGGER trg_issue_status_change
        AFTER UPDATE ON issue_log
        FOR EACH ROW
        EXECUTE FUNCTION log_issue_status_change()
    """)

    # ═══════════════════════════════════════════════════════════════════════
    # PART 7: RLS policies for issue_log and issue_log_history
    # ═══════════════════════════════════════════════════════════════════════

    for table in ["issue_log", "issue_log_history"]:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")

        op.execute(f"""
            CREATE POLICY {table}_select_policy ON {table}
            FOR SELECT
            USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
        """)

        op.execute(f"""
            CREATE POLICY {table}_insert_policy ON {table}
            FOR INSERT
            WITH CHECK (organization_id = current_setting('app.current_organization_id', true)::uuid)
        """)

        op.execute(f"""
            CREATE POLICY {table}_update_policy ON {table}
            FOR UPDATE
            USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
            WITH CHECK (organization_id = current_setting('app.current_organization_id', true)::uuid)
        """)

        op.execute(f"""
            CREATE POLICY {table}_delete_policy ON {table}
            FOR DELETE
            USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
        """)

    # ═══════════════════════════════════════════════════════════════════════
    # PART 8: Indexes for issue_log (performance per spec)
    # ═══════════════════════════════════════════════════════════════════════

    # Composite indexes for common query patterns
    op.create_index("ix_issue_log_org_status", "issue_log",
                    ["organization_id", "issue_status"])
    op.create_index("ix_issue_log_org_classification", "issue_log",
                    ["organization_id", "issue_classification"])
    op.create_index("ix_issue_log_org_criticality", "issue_log",
                    ["organization_id", "issue_criticality"])
    op.create_index("ix_issue_log_org_process_status", "issue_log",
                    ["organization_id", "process_id", "issue_status"])
    op.create_index("ix_issue_log_org_level_status", "issue_log",
                    ["organization_id", "process_level", "issue_status"])
    op.create_index("ix_issue_log_assigned", "issue_log",
                    ["assigned_to_id", "issue_status"])
    op.create_index("ix_issue_log_raised_by", "issue_log",
                    ["raised_by_id"])
    op.create_index("ix_issue_log_date_raised", "issue_log",
                    ["date_raised"])
    op.create_index("ix_issue_log_target_date", "issue_log",
                    ["target_resolution_date"])
    op.create_index("ix_issue_log_opportunity", "issue_log",
                    ["organization_id", "opportunity_flag", "opportunity_status"])

    # ═══════════════════════════════════════════════════════════════════════
    # PART 9: Add RAG columns to processes table
    # ═══════════════════════════════════════════════════════════════════════

    # RAG dimensions (4 columns matching issue_classification)
    op.add_column("processes", sa.Column(
        "rag_process",
        postgresql.ENUM('red', 'amber', 'green', 'neutral',
                        name='rag_status', create_type=False),
        server_default='neutral'
    ))
    op.add_column("processes", sa.Column(
        "rag_system",
        postgresql.ENUM('red', 'amber', 'green', 'neutral',
                        name='rag_status', create_type=False),
        server_default='neutral'
    ))
    op.add_column("processes", sa.Column(
        "rag_people",
        postgresql.ENUM('red', 'amber', 'green', 'neutral',
                        name='rag_status', create_type=False),
        server_default='neutral'
    ))
    op.add_column("processes", sa.Column(
        "rag_data",
        postgresql.ENUM('red', 'amber', 'green', 'neutral',
                        name='rag_status', create_type=False),
        server_default='neutral'
    ))

    # Review tracking
    op.add_column("processes", sa.Column(
        "rag_last_reviewed",
        sa.DateTime(timezone=True)
    ))
    op.add_column("processes", sa.Column(
        "rag_reviewed_by",
        postgresql.UUID(as_uuid=False)
    ))

    # Generated column for overall RAG (weakest-link rule)
    # Note: PostgreSQL GENERATED columns require specific syntax
    op.execute("""
        ALTER TABLE processes ADD COLUMN rag_overall rag_status
        GENERATED ALWAYS AS (
            CASE
                WHEN rag_process = 'red' OR rag_system = 'red'
                     OR rag_people = 'red' OR rag_data = 'red' THEN 'red'::rag_status
                WHEN rag_process = 'amber' OR rag_system = 'amber'
                     OR rag_people = 'amber' OR rag_data = 'amber' THEN 'amber'::rag_status
                WHEN rag_process = 'green' AND rag_system = 'green'
                     AND rag_people = 'green' AND rag_data = 'green' THEN 'green'::rag_status
                ELSE 'neutral'::rag_status
            END
        ) STORED
    """)

    # Indexes for RAG queries
    op.create_index("ix_processes_rag_overall", "processes",
                    ["organization_id", "rag_overall"])
    op.create_index("ix_processes_rag_dimensions", "processes",
                    ["organization_id", "rag_process", "rag_system", "rag_people", "rag_data"])

    # ═══════════════════════════════════════════════════════════════════════
    # PART 10: Heatmap view (direct issues only)
    # ═══════════════════════════════════════════════════════════════════════

    # Per RAG addendum: low=amber, no-issues=neutral (never green from issues alone)
    # Note: Use COUNT(il.id) not COUNT(*) to avoid counting NULL rows from LEFT JOIN
    op.execute("""
        CREATE OR REPLACE VIEW v_process_issue_heatmap AS
        SELECT
            p.organization_id,
            p.id AS process_id,
            p.code AS process_ref,
            p.name AS process_name,
            p.level,
            p.parent_id,
            -- Issue counts by classification (only open/in_progress)
            COUNT(il.id) FILTER (WHERE il.issue_classification = 'people') AS people_count,
            COUNT(il.id) FILTER (WHERE il.issue_classification = 'process') AS process_count,
            COUNT(il.id) FILTER (WHERE il.issue_classification = 'system') AS system_count,
            COUNT(il.id) FILTER (WHERE il.issue_classification = 'data') AS data_count,
            -- Max criticality by classification
            MAX(CASE WHEN il.issue_classification = 'people' THEN il.issue_criticality END) AS people_max_crit,
            MAX(CASE WHEN il.issue_classification = 'process' THEN il.issue_criticality END) AS process_max_crit,
            MAX(CASE WHEN il.issue_classification = 'system' THEN il.issue_criticality END) AS system_max_crit,
            MAX(CASE WHEN il.issue_classification = 'data' THEN il.issue_criticality END) AS data_max_crit,
            -- Heatmap colour per addendum: high=red, medium/low=amber, none=neutral
            CASE
                WHEN MAX(CASE WHEN il.issue_classification = 'people' THEN il.issue_criticality END) = 'high' THEN 'red'
                WHEN COUNT(il.id) FILTER (WHERE il.issue_classification = 'people') > 0 THEN 'amber'
                ELSE 'neutral'
            END AS people_colour,
            CASE
                WHEN MAX(CASE WHEN il.issue_classification = 'process' THEN il.issue_criticality END) = 'high' THEN 'red'
                WHEN COUNT(il.id) FILTER (WHERE il.issue_classification = 'process') > 0 THEN 'amber'
                ELSE 'neutral'
            END AS process_colour,
            CASE
                WHEN MAX(CASE WHEN il.issue_classification = 'system' THEN il.issue_criticality END) = 'high' THEN 'red'
                WHEN COUNT(il.id) FILTER (WHERE il.issue_classification = 'system') > 0 THEN 'amber'
                ELSE 'neutral'
            END AS system_colour,
            CASE
                WHEN MAX(CASE WHEN il.issue_classification = 'data' THEN il.issue_criticality END) = 'high' THEN 'red'
                WHEN COUNT(il.id) FILTER (WHERE il.issue_classification = 'data') > 0 THEN 'amber'
                ELSE 'neutral'
            END AS data_colour,
            -- Overall heatmap colour (worst of 4 dimensions)
            CASE
                WHEN MAX(il.issue_criticality) = 'high' THEN 'red'
                WHEN COUNT(il.id) > 0 THEN 'amber'
                ELSE 'neutral'
            END AS overall_colour,
            -- Total open issues (COUNT(il.id) not COUNT(*) to exclude NULL rows)
            COUNT(il.id) AS total_open_issues
        FROM processes p
        LEFT JOIN issue_log il ON il.process_id = p.id
            AND il.issue_status IN ('open', 'in_progress')
        WHERE p.status != 'archived'
        GROUP BY p.organization_id, p.id, p.code, p.name, p.level, p.parent_id
    """)

    # ═══════════════════════════════════════════════════════════════════════
    # PART 11: Rollup heatmap view (aggregates descendants)
    # ═══════════════════════════════════════════════════════════════════════

    # Corrected recursive CTE: walk UP from processes with issues to aggregate at ancestors
    op.execute("""
        CREATE OR REPLACE VIEW v_process_issue_heatmap_rollup AS
        WITH RECURSIVE process_tree AS (
            -- Base: all processes with their direct issue counts
            SELECT
                p.organization_id,
                p.id AS process_id,
                p.code AS process_ref,
                p.name AS process_name,
                p.level,
                p.parent_id,
                p.id AS source_process_id,  -- Track original source
                -- Direct counts
                COUNT(*) FILTER (WHERE il.issue_classification = 'people') AS people_count,
                COUNT(*) FILTER (WHERE il.issue_classification = 'process') AS process_count,
                COUNT(*) FILTER (WHERE il.issue_classification = 'system') AS system_count,
                COUNT(*) FILTER (WHERE il.issue_classification = 'data') AS data_count,
                -- Direct max criticality (for rollup we need worst-case)
                MAX(CASE WHEN il.issue_classification = 'people' AND il.issue_criticality = 'high' THEN 1
                         WHEN il.issue_classification = 'people' AND il.issue_criticality = 'medium' THEN 2
                         WHEN il.issue_classification = 'people' AND il.issue_criticality = 'low' THEN 3
                         ELSE 4 END) AS people_crit_rank,
                MAX(CASE WHEN il.issue_classification = 'process' AND il.issue_criticality = 'high' THEN 1
                         WHEN il.issue_classification = 'process' AND il.issue_criticality = 'medium' THEN 2
                         WHEN il.issue_classification = 'process' AND il.issue_criticality = 'low' THEN 3
                         ELSE 4 END) AS process_crit_rank,
                MAX(CASE WHEN il.issue_classification = 'system' AND il.issue_criticality = 'high' THEN 1
                         WHEN il.issue_classification = 'system' AND il.issue_criticality = 'medium' THEN 2
                         WHEN il.issue_classification = 'system' AND il.issue_criticality = 'low' THEN 3
                         ELSE 4 END) AS system_crit_rank,
                MAX(CASE WHEN il.issue_classification = 'data' AND il.issue_criticality = 'high' THEN 1
                         WHEN il.issue_classification = 'data' AND il.issue_criticality = 'medium' THEN 2
                         WHEN il.issue_classification = 'data' AND il.issue_criticality = 'low' THEN 3
                         ELSE 4 END) AS data_crit_rank
            FROM processes p
            LEFT JOIN issue_log il ON il.process_id = p.id
                AND il.issue_status IN ('open', 'in_progress')
            WHERE p.status != 'archived'
            GROUP BY p.organization_id, p.id, p.code, p.name, p.level, p.parent_id
        ),
        -- Aggregate: sum counts at each level, take worst criticality
        rollup_agg AS (
            SELECT
                pt.organization_id,
                pt.process_id,
                pt.process_ref,
                pt.process_name,
                pt.level,
                pt.parent_id,
                SUM(pt.people_count) AS people_count,
                SUM(pt.process_count) AS process_count,
                SUM(pt.system_count) AS system_count,
                SUM(pt.data_count) AS data_count,
                MIN(pt.people_crit_rank) AS people_crit_rank,
                MIN(pt.process_crit_rank) AS process_crit_rank,
                MIN(pt.system_crit_rank) AS system_crit_rank,
                MIN(pt.data_crit_rank) AS data_crit_rank
            FROM process_tree pt
            GROUP BY pt.organization_id, pt.process_id, pt.process_ref,
                     pt.process_name, pt.level, pt.parent_id
        ),
        -- Walk up to include child issues in parent counts
        ancestor_rollup AS (
            -- Start with leaf data
            SELECT * FROM rollup_agg
            UNION ALL
            -- Add child data to parents
            SELECT
                p.organization_id,
                p.id AS process_id,
                p.code AS process_ref,
                p.name AS process_name,
                p.level,
                p.parent_id,
                ar.people_count,
                ar.process_count,
                ar.system_count,
                ar.data_count,
                ar.people_crit_rank,
                ar.process_crit_rank,
                ar.system_crit_rank,
                ar.data_crit_rank
            FROM ancestor_rollup ar
            JOIN processes p ON p.id = ar.parent_id
            WHERE p.status != 'archived'
        ),
        final_agg AS (
            SELECT
                organization_id,
                process_id,
                MAX(process_ref) AS process_ref,
                MAX(process_name) AS process_name,
                MAX(level) AS level,
                MAX(parent_id::text)::uuid AS parent_id,
                SUM(people_count) AS people_count,
                SUM(process_count) AS process_count,
                SUM(system_count) AS system_count,
                SUM(data_count) AS data_count,
                MIN(people_crit_rank) AS people_crit_rank,
                MIN(process_crit_rank) AS process_crit_rank,
                MIN(system_crit_rank) AS system_crit_rank,
                MIN(data_crit_rank) AS data_crit_rank
            FROM ancestor_rollup
            GROUP BY organization_id, process_id
        )
        SELECT
            organization_id,
            process_id,
            process_ref,
            process_name,
            level,
            parent_id,
            people_count::INTEGER,
            process_count::INTEGER,
            system_count::INTEGER,
            data_count::INTEGER,
            (people_count + process_count + system_count + data_count)::INTEGER AS total_issues,
            -- Colour mapping per addendum
            CASE
                WHEN people_crit_rank = 1 THEN 'red'
                WHEN people_count > 0 THEN 'amber'
                ELSE 'neutral'
            END AS people_colour,
            CASE
                WHEN process_crit_rank = 1 THEN 'red'
                WHEN process_count > 0 THEN 'amber'
                ELSE 'neutral'
            END AS process_colour,
            CASE
                WHEN system_crit_rank = 1 THEN 'red'
                WHEN system_count > 0 THEN 'amber'
                ELSE 'neutral'
            END AS system_colour,
            CASE
                WHEN data_crit_rank = 1 THEN 'red'
                WHEN data_count > 0 THEN 'amber'
                ELSE 'neutral'
            END AS data_colour,
            CASE
                WHEN LEAST(people_crit_rank, process_crit_rank, system_crit_rank, data_crit_rank) = 1 THEN 'red'
                WHEN (people_count + process_count + system_count + data_count) > 0 THEN 'amber'
                ELSE 'neutral'
            END AS overall_colour
        FROM final_agg
    """)

    # ═══════════════════════════════════════════════════════════════════════
    # PART 12: RAG sync function (issue -> process RAG)
    # ═══════════════════════════════════════════════════════════════════════

    # Per addendum BR-11: high=red, medium/low=amber
    # Per addendum BR-15: resolving last issue reverts to neutral (not green)
    # GREEN requires explicit assessment (BR-12)
    op.execute("""
        CREATE OR REPLACE FUNCTION sync_process_rag_from_issues()
        RETURNS TRIGGER AS $$
        DECLARE
            v_process_id UUID;
            v_has_high_people BOOLEAN;
            v_has_high_process BOOLEAN;
            v_has_high_system BOOLEAN;
            v_has_high_data BOOLEAN;
            v_has_any_people BOOLEAN;
            v_has_any_process BOOLEAN;
            v_has_any_system BOOLEAN;
            v_has_any_data BOOLEAN;
            v_has_explicit_review BOOLEAN;
            v_new_rag_people rag_status;
            v_new_rag_process rag_status;
            v_new_rag_system rag_status;
            v_new_rag_data rag_status;
        BEGIN
            -- Determine which process to update
            IF TG_OP = 'DELETE' THEN
                v_process_id := OLD.process_id;
            ELSE
                v_process_id := NEW.process_id;
            END IF;

            -- Check for open issues by classification and criticality
            SELECT
                COALESCE(bool_or(issue_classification = 'people' AND issue_criticality = 'high'), false),
                COALESCE(bool_or(issue_classification = 'process' AND issue_criticality = 'high'), false),
                COALESCE(bool_or(issue_classification = 'system' AND issue_criticality = 'high'), false),
                COALESCE(bool_or(issue_classification = 'data' AND issue_criticality = 'high'), false),
                COALESCE(bool_or(issue_classification = 'people'), false),
                COALESCE(bool_or(issue_classification = 'process'), false),
                COALESCE(bool_or(issue_classification = 'system'), false),
                COALESCE(bool_or(issue_classification = 'data'), false)
            INTO
                v_has_high_people, v_has_high_process, v_has_high_system, v_has_high_data,
                v_has_any_people, v_has_any_process, v_has_any_system, v_has_any_data
            FROM issue_log
            WHERE process_id = v_process_id
              AND issue_status IN ('open', 'in_progress');

            -- Check if process has been explicitly reviewed
            SELECT (rag_last_reviewed IS NOT NULL)
            INTO v_has_explicit_review
            FROM processes
            WHERE id = v_process_id;

            -- Compute new RAG values per BR-11, BR-12, BR-15
            -- High criticality -> RED
            -- Any open issue (medium/low) -> AMBER
            -- No open issues + explicit review -> GREEN (per spec, but we allow explicit assessment to set this)
            -- No open issues + no review -> NEUTRAL

            -- People dimension
            IF v_has_high_people THEN
                v_new_rag_people := 'red';
            ELSIF v_has_any_people THEN
                v_new_rag_people := 'amber';
            ELSIF v_has_explicit_review THEN
                -- Keep existing green if set by explicit review, otherwise neutral
                SELECT CASE WHEN rag_people = 'green' THEN 'green' ELSE 'neutral' END
                INTO v_new_rag_people
                FROM processes WHERE id = v_process_id;
            ELSE
                v_new_rag_people := 'neutral';
            END IF;

            -- Process dimension
            IF v_has_high_process THEN
                v_new_rag_process := 'red';
            ELSIF v_has_any_process THEN
                v_new_rag_process := 'amber';
            ELSIF v_has_explicit_review THEN
                SELECT CASE WHEN rag_process = 'green' THEN 'green' ELSE 'neutral' END
                INTO v_new_rag_process
                FROM processes WHERE id = v_process_id;
            ELSE
                v_new_rag_process := 'neutral';
            END IF;

            -- System dimension
            IF v_has_high_system THEN
                v_new_rag_system := 'red';
            ELSIF v_has_any_system THEN
                v_new_rag_system := 'amber';
            ELSIF v_has_explicit_review THEN
                SELECT CASE WHEN rag_system = 'green' THEN 'green' ELSE 'neutral' END
                INTO v_new_rag_system
                FROM processes WHERE id = v_process_id;
            ELSE
                v_new_rag_system := 'neutral';
            END IF;

            -- Data dimension
            IF v_has_high_data THEN
                v_new_rag_data := 'red';
            ELSIF v_has_any_data THEN
                v_new_rag_data := 'amber';
            ELSIF v_has_explicit_review THEN
                SELECT CASE WHEN rag_data = 'green' THEN 'green' ELSE 'neutral' END
                INTO v_new_rag_data
                FROM processes WHERE id = v_process_id;
            ELSE
                v_new_rag_data := 'neutral';
            END IF;

            -- Update process RAG columns
            UPDATE processes
            SET
                rag_people = v_new_rag_people,
                rag_process = v_new_rag_process,
                rag_system = v_new_rag_system,
                rag_data = v_new_rag_data
            WHERE id = v_process_id;

            RETURN COALESCE(NEW, OLD);
        END;
        $$ LANGUAGE plpgsql
    """)

    op.execute("""
        CREATE TRIGGER trg_issue_rag_sync
        AFTER INSERT OR UPDATE OR DELETE ON issue_log
        FOR EACH ROW
        EXECUTE FUNCTION sync_process_rag_from_issues()
    """)


def downgrade() -> None:
    # Drop trigger and function
    op.execute("DROP TRIGGER IF EXISTS trg_issue_rag_sync ON issue_log")
    op.execute("DROP FUNCTION IF EXISTS sync_process_rag_from_issues()")

    # Drop views
    op.execute("DROP VIEW IF EXISTS v_process_issue_heatmap_rollup")
    op.execute("DROP VIEW IF EXISTS v_process_issue_heatmap")

    # Drop RAG columns from processes
    op.execute("ALTER TABLE processes DROP COLUMN IF EXISTS rag_overall")
    op.drop_column("processes", "rag_reviewed_by")
    op.drop_column("processes", "rag_last_reviewed")
    op.drop_column("processes", "rag_data")
    op.drop_column("processes", "rag_people")
    op.drop_column("processes", "rag_system")
    op.drop_column("processes", "rag_process")

    # Drop indexes on processes
    op.execute("DROP INDEX IF EXISTS ix_processes_rag_dimensions")
    op.execute("DROP INDEX IF EXISTS ix_processes_rag_overall")

    # Drop RLS policies
    for table in ["issue_log", "issue_log_history"]:
        op.execute(f"DROP POLICY IF EXISTS {table}_select_policy ON {table}")
        op.execute(f"DROP POLICY IF EXISTS {table}_insert_policy ON {table}")
        op.execute(f"DROP POLICY IF EXISTS {table}_update_policy ON {table}")
        op.execute(f"DROP POLICY IF EXISTS {table}_delete_policy ON {table}")
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")

    # Drop triggers and functions
    op.execute("DROP TRIGGER IF EXISTS trg_issue_status_change ON issue_log")
    op.execute("DROP FUNCTION IF EXISTS log_issue_status_change()")
    op.execute("DROP TRIGGER IF EXISTS trg_issue_log_updated_at ON issue_log")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")
    op.execute("DROP TRIGGER IF EXISTS trg_issue_number ON issue_log")
    op.execute("DROP FUNCTION IF EXISTS next_issue_number()")

    # Drop indexes on issue_log
    op.execute("DROP INDEX IF EXISTS ix_issue_log_opportunity")
    op.execute("DROP INDEX IF EXISTS ix_issue_log_target_date")
    op.execute("DROP INDEX IF EXISTS ix_issue_log_date_raised")
    op.execute("DROP INDEX IF EXISTS ix_issue_log_raised_by")
    op.execute("DROP INDEX IF EXISTS ix_issue_log_assigned")
    op.execute("DROP INDEX IF EXISTS ix_issue_log_org_level_status")
    op.execute("DROP INDEX IF EXISTS ix_issue_log_org_process_status")
    op.execute("DROP INDEX IF EXISTS ix_issue_log_org_criticality")
    op.execute("DROP INDEX IF EXISTS ix_issue_log_org_classification")
    op.execute("DROP INDEX IF EXISTS ix_issue_log_org_status")

    # Drop tables
    op.drop_table("issue_log_history")
    op.drop_table("issue_log")

    # Drop enums
    op.execute("DROP TYPE IF EXISTS rag_status")
    op.execute("DROP TYPE IF EXISTS opportunity_status")
    op.execute("DROP TYPE IF EXISTS issue_status")
    op.execute("DROP TYPE IF EXISTS issue_complexity")
    op.execute("DROP TYPE IF EXISTS issue_criticality")
    op.execute("DROP TYPE IF EXISTS issue_classification")
