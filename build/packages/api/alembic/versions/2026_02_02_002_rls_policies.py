"""Add Row Level Security (RLS) policies for multi-tenancy.

Revision ID: 002
Revises: 001
Create Date: 2026-02-02

Enables RLS on all tenant tables and creates policies that restrict
access based on organization_id. This ensures complete tenant isolation.

Blueprint §6.1: Multi-tenancy is a security boundary, not a feature.
"""

from alembic import op

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None

# Tables with organization_id that need RLS
TENANT_TABLES = [
    "allowed_domains",
    "audit_logs",
    "business_model_entries",
    "business_model_mappings",
    "business_models",
    "llm_configurations",
    "portfolio_items",
    "portfolio_milestones",
    "process_operating_model",
    "processes",
    "prompt_executions",
    "prompt_templates",
    "reference_catalogues",
    "riada_items",
    "survey_questions",
    "survey_responses",
    "surveys",
    "user_organizations",
]


def upgrade() -> None:
    # Enable RLS on all tenant tables
    for table in TENANT_TABLES:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")

        # Create policy for SELECT - users can only see their org's data
        op.execute(f"""
            CREATE POLICY {table}_select_policy ON {table}
            FOR SELECT
            USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
        """)

        # Create policy for INSERT - users can only insert into their org
        op.execute(f"""
            CREATE POLICY {table}_insert_policy ON {table}
            FOR INSERT
            WITH CHECK (organization_id = current_setting('app.current_organization_id', true)::uuid)
        """)

        # Create policy for UPDATE - users can only update their org's data
        op.execute(f"""
            CREATE POLICY {table}_update_policy ON {table}
            FOR UPDATE
            USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
            WITH CHECK (organization_id = current_setting('app.current_organization_id', true)::uuid)
        """)

        # Create policy for DELETE - users can only delete their org's data
        op.execute(f"""
            CREATE POLICY {table}_delete_policy ON {table}
            FOR DELETE
            USING (organization_id = current_setting('app.current_organization_id', true)::uuid)
        """)

    # Organizations table - users can only see orgs they belong to
    op.execute("ALTER TABLE organizations ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE organizations FORCE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY organizations_select_policy ON organizations
        FOR SELECT
        USING (
            id = current_setting('app.current_organization_id', true)::uuid
            OR id IN (
                SELECT organization_id FROM user_organizations
                WHERE user_id = current_setting('app.current_user_id', true)::uuid
            )
        )
    """)

    # Users table - users can see themselves and users in their orgs
    op.execute("ALTER TABLE users ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE users FORCE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY users_select_policy ON users
        FOR SELECT
        USING (
            id = current_setting('app.current_user_id', true)::uuid
            OR id IN (
                SELECT uo.user_id FROM user_organizations uo
                WHERE uo.organization_id = current_setting('app.current_organization_id', true)::uuid
            )
        )
    """)
    op.execute("""
        CREATE POLICY users_update_own_policy ON users
        FOR UPDATE
        USING (id = current_setting('app.current_user_id', true)::uuid)
        WITH CHECK (id = current_setting('app.current_user_id', true)::uuid)
    """)

    # Magic link tokens - no RLS needed (checked by application)
    # But we still enable it with a permissive policy for service role
    op.execute("ALTER TABLE magic_link_tokens ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY magic_link_tokens_service_policy ON magic_link_tokens
        FOR ALL
        USING (true)
        WITH CHECK (true)
    """)


def downgrade() -> None:
    # Drop all policies and disable RLS
    for table in TENANT_TABLES:
        op.execute(f"DROP POLICY IF EXISTS {table}_select_policy ON {table}")
        op.execute(f"DROP POLICY IF EXISTS {table}_insert_policy ON {table}")
        op.execute(f"DROP POLICY IF EXISTS {table}_update_policy ON {table}")
        op.execute(f"DROP POLICY IF EXISTS {table}_delete_policy ON {table}")
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")

    # Organizations
    op.execute("DROP POLICY IF EXISTS organizations_select_policy ON organizations")
    op.execute("ALTER TABLE organizations DISABLE ROW LEVEL SECURITY")

    # Users
    op.execute("DROP POLICY IF EXISTS users_select_policy ON users")
    op.execute("DROP POLICY IF EXISTS users_update_own_policy ON users")
    op.execute("ALTER TABLE users DISABLE ROW LEVEL SECURITY")

    # Magic link tokens
    op.execute("DROP POLICY IF EXISTS magic_link_tokens_service_policy ON magic_link_tokens")
    op.execute("ALTER TABLE magic_link_tokens DISABLE ROW LEVEL SECURITY")
