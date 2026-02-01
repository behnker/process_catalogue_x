-- Process Catalogue — Database Initialization
-- Run once when PostgreSQL container starts.

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ──────────────────────────────────────────────────────────
-- Row-Level Security (RLS) Configuration
-- Blueprint §6.1: Complete tenant data isolation
-- ──────────────────────────────────────────────────────────

-- Function to get current tenant from session variable
CREATE OR REPLACE FUNCTION current_org_id()
RETURNS UUID AS $$
BEGIN
  RETURN NULLIF(current_setting('app.current_organization_id', true), '')::UUID;
END;
$$ LANGUAGE plpgsql STABLE;

-- Apply RLS after tables are created by Alembic.
-- This is a template — enable on each tenant-scoped table:
--
--   ALTER TABLE processes ENABLE ROW LEVEL SECURITY;
--   CREATE POLICY tenant_isolation ON processes
--     USING (organization_id = current_org_id());
--
-- For development, RLS is enforced via application-level filtering.

-- ──────────────────────────────────────────────────────────
-- Seed Data: Default organization for development
-- ──────────────────────────────────────────────────────────

-- This will be populated by Alembic migrations + seed script.
-- See packages/api/src/utils/seed.py
