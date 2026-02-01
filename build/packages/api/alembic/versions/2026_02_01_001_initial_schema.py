"""Initial schema with all tables.

Revision ID: 001
Revises:
Create Date: 2026-02-01

Creates all tables for:
- Organizations, Users, Auth (magic links, audit logs)
- Process Catalogue (processes, operating model)
- RIADA (risks, issues, actions, dependencies, assumptions)
- Business Model (canvas, entries, mappings)
- Portfolio (items, milestones)
- Surveys (surveys, questions, responses)
- Reference Data (catalogues, prompts, LLM config)
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── Organizations ───────────────────────────────────────
    op.create_table(
        "organizations",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(100), unique=True, nullable=False, index=True),
        sa.Column("subscription_tier", sa.String(20), server_default="free"),
        sa.Column("settings", postgresql.JSONB, server_default="{}"),
        sa.Column("branding", postgresql.JSONB, server_default="{}"),
        sa.Column("data_region", sa.String(20), server_default="global"),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Allowed Domains ─────────────────────────────────────
    op.create_table(
        "allowed_domains",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("domain", sa.String(255), nullable=False, index=True),
        sa.Column("is_verified", sa.Boolean, server_default="false"),
        sa.Column("verification_method", sa.String(20)),
        sa.Column("verification_token", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Users ───────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("display_name", sa.String(255)),
        sa.Column("avatar_url", sa.String(500)),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("last_login_at", sa.DateTime(timezone=True)),
        sa.Column("default_organization_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("organizations.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── User-Organization Membership ────────────────────────
    op.create_table(
        "user_organizations",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("role", sa.String(50), server_default="viewer"),
        sa.Column("status", sa.String(20), server_default="invited"),
        sa.Column("invited_by", postgresql.UUID(as_uuid=False)),
        sa.Column("invited_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_user_organizations_user_org", "user_organizations", ["user_id", "organization_id"], unique=True)

    # ── Magic Link Tokens ───────────────────────────────────
    op.create_table(
        "magic_link_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, index=True),
        sa.Column("token_hash", sa.String(255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_used", sa.Boolean, server_default="false"),
        sa.Column("used_at", sa.DateTime(timezone=True)),
        sa.Column("ip_address", sa.String(45)),
        sa.Column("user_agent", sa.String(500)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Audit Logs ──────────────────────────────────────────
    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("organizations.id"), nullable=False, index=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=False)),
        sa.Column("action", sa.String(20), nullable=False),
        sa.Column("entity_type", sa.String(50), nullable=False, index=True),
        sa.Column("entity_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("changes", postgresql.JSONB),
        sa.Column("ip_address", sa.String(45)),
        sa.Column("user_agent", sa.String(500)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Processes ───────────────────────────────────────────
    op.create_table(
        "processes",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("code", sa.String(20), nullable=False, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("level", sa.String(5), nullable=False, index=True),
        sa.Column("parent_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("processes.id")),
        sa.Column("sort_order", sa.Integer, server_default="0"),
        sa.Column("process_type", sa.String(20), server_default="primary"),
        sa.Column("status", sa.String(20), server_default="draft", index=True),
        sa.Column("current_automation", sa.String(30), server_default="manual"),
        sa.Column("target_automation", sa.String(30)),
        sa.Column("automation_notes", sa.Text),
        sa.Column("owner_id", postgresql.UUID(as_uuid=False)),
        sa.Column("sponsor_id", postgresql.UUID(as_uuid=False)),
        sa.Column("function_id", postgresql.UUID(as_uuid=False)),
        sa.Column("tags", postgresql.JSONB, server_default="[]"),
        sa.Column("metadata_extra", postgresql.JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_processes_org_code", "processes", ["organization_id", "code"], unique=True)

    # ── Process Operating Model ─────────────────────────────
    op.create_table(
        "process_operating_model",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("process_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("processes.id"), nullable=False, index=True),
        sa.Column("component_type", sa.String(30), nullable=False, index=True),
        sa.Column("current_state", postgresql.JSONB, server_default="{}"),
        sa.Column("future_state", postgresql.JSONB, server_default="{}"),
        sa.Column("transition_notes", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_pom_process_component", "process_operating_model", ["process_id", "component_type"], unique=True)

    # ── Business Models ─────────────────────────────────────
    op.create_table(
        "business_models",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("status", sa.String(20), server_default="active"),
        sa.Column("canvas_layout", postgresql.JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Business Model Entries ──────────────────────────────
    op.create_table(
        "business_model_entries",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("business_model_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("business_models.id"), nullable=False, index=True),
        sa.Column("component", sa.String(30), nullable=False, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("sort_order", sa.Integer, server_default="0"),
        sa.Column("agentic_opportunity", sa.Text),
        sa.Column("agentic_readiness", sa.String(20)),
        sa.Column("agentic_impact", sa.String(20)),
        sa.Column("agentic_notes", sa.Text),
        sa.Column("metadata_extra", postgresql.JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Business Model Mappings ─────────────────────────────
    op.create_table(
        "business_model_mappings",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("process_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("processes.id"), nullable=False, index=True),
        sa.Column("trading_markets", postgresql.JSONB, server_default="[]"),
        sa.Column("clients", postgresql.JSONB, server_default="[]"),
        sa.Column("sourcing_markets", postgresql.JSONB, server_default="[]"),
        sa.Column("product_categories", postgresql.JSONB, server_default="[]"),
        sa.Column("key_partners", postgresql.JSONB, server_default="[]"),
        sa.Column("key_suppliers", postgresql.JSONB, server_default="[]"),
        sa.Column("channel", sa.String(50)),
        sa.Column("revenue_line", sa.String(100)),
        sa.Column("cost_line", sa.String(100)),
        sa.Column("functions", postgresql.JSONB, server_default="[]"),
        sa.Column("value_proposition", sa.Text),
        sa.Column("customer_segment", sa.String(255)),
        sa.Column("notes", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Portfolio Items ─────────────────────────────────────
    op.create_table(
        "portfolio_items",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("code", sa.String(30), nullable=False, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("level", sa.String(20), nullable=False, index=True),
        sa.Column("parent_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("portfolio_items.id")),
        sa.Column("sort_order", sa.Integer, server_default="0"),
        sa.Column("status", sa.String(20), server_default="proposed", index=True),
        sa.Column("rag_status", sa.String(10)),
        sa.Column("rag_notes", sa.Text),
        sa.Column("business_value", sa.Integer),
        sa.Column("time_criticality", sa.Integer),
        sa.Column("risk_reduction", sa.Integer),
        sa.Column("job_size", sa.Integer),
        sa.Column("wsvf_score", sa.Numeric(10, 2)),
        sa.Column("planned_start", sa.Date),
        sa.Column("planned_end", sa.Date),
        sa.Column("actual_start", sa.Date),
        sa.Column("actual_end", sa.Date),
        sa.Column("budget_approved", sa.Numeric(14, 2)),
        sa.Column("budget_spent", sa.Numeric(14, 2)),
        sa.Column("budget_forecast", sa.Numeric(14, 2)),
        sa.Column("budget_currency", sa.String(3), server_default="USD"),
        sa.Column("owner_id", postgresql.UUID(as_uuid=False)),
        sa.Column("sponsor_id", postgresql.UUID(as_uuid=False)),
        sa.Column("linked_process_ids", postgresql.JSONB, server_default="[]"),
        sa.Column("tags", postgresql.JSONB, server_default="[]"),
        sa.Column("metadata_extra", postgresql.JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_portfolio_items_org_code", "portfolio_items", ["organization_id", "code"], unique=True)

    # ── Portfolio Milestones ────────────────────────────────
    op.create_table(
        "portfolio_milestones",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("portfolio_item_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("portfolio_items.id"), nullable=False, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("due_date", sa.Date),
        sa.Column("completed_date", sa.Date),
        sa.Column("status", sa.String(20), server_default="pending"),
        sa.Column("sort_order", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── RIADA Items ─────────────────────────────────────────
    op.create_table(
        "riada_items",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("code", sa.String(20), nullable=False, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("riada_type", sa.String(20), nullable=False, index=True),
        sa.Column("category", sa.String(20), nullable=False, index=True),
        sa.Column("severity", sa.String(20), server_default="medium", index=True),
        sa.Column("status", sa.String(20), server_default="open", index=True),
        sa.Column("probability", sa.Integer),
        sa.Column("impact", sa.Integer),
        sa.Column("risk_score", sa.Integer),
        sa.Column("mitigation_plan", sa.Text),
        sa.Column("due_date", sa.Date),
        sa.Column("assigned_to_id", postgresql.UUID(as_uuid=False)),
        sa.Column("raised_by_id", postgresql.UUID(as_uuid=False)),
        sa.Column("process_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("processes.id"), index=True),
        sa.Column("portfolio_item_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("portfolio_items.id"), index=True),
        sa.Column("business_model_entry_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("business_model_entries.id"), index=True),
        sa.Column("rag_status", sa.String(10)),
        sa.Column("resolution_notes", sa.Text),
        sa.Column("resolved_at", sa.Date),
        sa.Column("resolved_by_id", postgresql.UUID(as_uuid=False)),
        sa.Column("tags", postgresql.JSONB, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_riada_items_org_code", "riada_items", ["organization_id", "code"], unique=True)

    # ── Surveys ─────────────────────────────────────────────
    op.create_table(
        "surveys",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("mode", sa.String(30), nullable=False, index=True),
        sa.Column("status", sa.String(20), server_default="draft"),
        sa.Column("target_audience", postgresql.JSONB, server_default="{}"),
        sa.Column("start_date", sa.Date),
        sa.Column("end_date", sa.Date),
        sa.Column("is_anonymous", sa.Boolean, server_default="false"),
        sa.Column("linked_process_ids", postgresql.JSONB, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Survey Questions ────────────────────────────────────
    op.create_table(
        "survey_questions",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("survey_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("surveys.id"), nullable=False, index=True),
        sa.Column("question_text", sa.Text, nullable=False),
        sa.Column("question_type", sa.String(30), nullable=False),
        sa.Column("is_required", sa.Boolean, server_default="true"),
        sa.Column("sort_order", sa.Integer, server_default="0"),
        sa.Column("options", postgresql.JSONB, server_default="[]"),
        sa.Column("scoring_weight", sa.Float, server_default="1.0"),
        sa.Column("conditions", postgresql.JSONB),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Survey Responses ────────────────────────────────────
    op.create_table(
        "survey_responses",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("survey_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("surveys.id"), nullable=False, index=True),
        sa.Column("respondent_id", postgresql.UUID(as_uuid=False)),
        sa.Column("is_complete", sa.Boolean, server_default="false"),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("total_score", sa.Float),
        sa.Column("answers", postgresql.JSONB, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Reference Catalogues ────────────────────────────────
    op.create_table(
        "reference_catalogues",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("catalogue_type", sa.String(30), nullable=False, index=True),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("status", sa.String(20), server_default="active"),
        sa.Column("sort_order", sa.Integer, server_default="0"),
        sa.Column("parent_id", postgresql.UUID(as_uuid=False)),
        sa.Column("metadata_extra", postgresql.JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_reference_catalogues_org_type_code", "reference_catalogues", ["organization_id", "catalogue_type", "code"], unique=True)

    # ── Prompt Templates ────────────────────────────────────
    op.create_table(
        "prompt_templates",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("category", sa.String(50), nullable=False, index=True),
        sa.Column("system_prompt", sa.Text),
        sa.Column("user_prompt_template", sa.Text, nullable=False),
        sa.Column("context_type", sa.String(30), server_default="process"),
        sa.Column("include_riada", sa.Boolean, server_default="true"),
        sa.Column("include_kpis", sa.Boolean, server_default="false"),
        sa.Column("include_raci", sa.Boolean, server_default="false"),
        sa.Column("default_model", sa.String(100)),
        sa.Column("default_temperature", sa.Numeric(3, 2)),
        sa.Column("default_max_tokens", sa.Integer),
        sa.Column("is_system", sa.Boolean, server_default="false"),
        sa.Column("is_published", sa.Boolean, server_default="true"),
        sa.Column("usage_count", sa.Integer, server_default="0"),
        sa.Column("avg_rating", sa.Numeric(3, 2)),
        sa.Column("tags", postgresql.JSONB, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Prompt Executions ───────────────────────────────────
    op.create_table(
        "prompt_executions",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("template_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("prompt_templates.id"), index=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("target_entity_type", sa.String(30), nullable=False),
        sa.Column("target_entity_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("prompt_sent", sa.Text, nullable=False),
        sa.Column("response_received", sa.Text),
        sa.Column("model_used", sa.String(100), nullable=False),
        sa.Column("prompt_tokens", sa.Integer),
        sa.Column("completion_tokens", sa.Integer),
        sa.Column("total_tokens", sa.Integer),
        sa.Column("estimated_cost", sa.Numeric(10, 6)),
        sa.Column("rating", sa.Integer),
        sa.Column("feedback", sa.Text),
        sa.Column("is_saved", sa.Boolean, server_default="false"),
        sa.Column("execution_time_ms", sa.Integer),
        sa.Column("error_message", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── LLM Configurations ──────────────────────────────────
    op.create_table(
        "llm_configurations",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False, index=True),
        sa.Column("provider", sa.String(50), nullable=False),
        sa.Column("model", sa.String(100), nullable=False),
        sa.Column("api_key_encrypted", sa.Text),
        sa.Column("endpoint_url", sa.String(500)),
        sa.Column("default_temperature", sa.Numeric(3, 2), server_default="0.7"),
        sa.Column("default_max_tokens", sa.Integer, server_default="4000"),
        sa.Column("rate_limit_rpm", sa.Integer, server_default="60"),
        sa.Column("monthly_token_limit", sa.Integer),
        sa.Column("is_enabled", sa.Boolean, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_llm_configurations_org_provider", "llm_configurations", ["organization_id", "provider", "model"], unique=True)


def downgrade() -> None:
    # Drop in reverse order of creation (respecting foreign keys)
    op.drop_table("llm_configurations")
    op.drop_table("prompt_executions")
    op.drop_table("prompt_templates")
    op.drop_table("reference_catalogues")
    op.drop_table("survey_responses")
    op.drop_table("survey_questions")
    op.drop_table("surveys")
    op.drop_table("riada_items")
    op.drop_table("portfolio_milestones")
    op.drop_table("portfolio_items")
    op.drop_table("business_model_mappings")
    op.drop_table("business_model_entries")
    op.drop_table("business_models")
    op.drop_table("process_operating_model")
    op.drop_table("processes")
    op.drop_table("audit_logs")
    op.drop_table("magic_link_tokens")
    op.drop_table("user_organizations")
    op.drop_table("users")
    op.drop_table("allowed_domains")
    op.drop_table("organizations")
