# System Catalogue — Schema Enhancement Specification

> **Blueprint Section:** 9.6.9 (Reference Catalogues)
> **Version:** 1.9.1 | **Date:** 2026-02-02
> **Status:** Ready for implementation
> **Depends on:** Organization, User, Process tables (Phase 1)

---

## Summary

Extend `SystemCatalogue` from 7 → 25 columns and `ProcessSystem` from 6 → 14 columns.
Source: Surity system register (8 systems) + Operating Model Systems & Tools sheet.
Seed: 8 system records + 10 process-system linkages.

---

## 1. New Enum Types

Create these before altering tables.

```sql
-- Extend existing
ALTER TYPE system_type ADD VALUE IF NOT EXISTS 'collaboration';
ALTER TYPE system_type ADD VALUE IF NOT EXISTS 'communication';
ALTER TYPE system_type ADD VALUE IF NOT EXISTS 'finance';
ALTER TYPE system_type ADD VALUE IF NOT EXISTS 'quality';
ALTER TYPE system_type ADD VALUE IF NOT EXISTS 'contract_mgmt';
ALTER TYPE system_type ADD VALUE IF NOT EXISTS 'file_storage';
ALTER TYPE system_type ADD VALUE IF NOT EXISTS 'workflow';
ALTER TYPE system_type ADD VALUE IF NOT EXISTS 'operational_tool';

-- New types
CREATE TYPE provider_type AS ENUM (
  'internal',           -- Built/maintained in-house
  'commercial_saas',    -- SaaS subscription (M365, FangCloud, Ding Talk)
  'commercial_onprem',  -- On-premise license (Kingdee)
  'custom_developed',   -- Built by external vendor (Fumasoft ERP, Yida Audit App)
  'open_source'
);

CREATE TYPE hosting_model AS ENUM (
  'cloud_global',       -- AWS/Azure/GCP global regions
  'cloud_china',        -- Alibaba/Tencent/Huawei Cloud
  'on_premise',         -- Customer-hosted servers
  'hybrid'
);

CREATE TYPE operating_region AS ENUM (
  'global',             -- Accessible everywhere
  'china_only',         -- China mainland only
  'international_only', -- Not accessible from China
  'multi_region'        -- Available in China + international
);

CREATE TYPE system_criticality AS ENUM (
  'critical',   -- Business stops; no workaround
  'high',       -- Major disruption; limited workaround
  'medium',     -- Operational impact; manual workaround exists
  'low'         -- Minimal impact; easy workaround
);

CREATE TYPE license_model AS ENUM (
  'free',              -- No cost (Ding Talk free tier)
  'subscription',      -- Recurring SaaS (M365, FangCloud)
  'perpetual',         -- One-time license (Kingdee)
  'custom_contract',   -- Bespoke dev/maintenance (Fumasoft, Yida)
  'internal'           -- No external cost
);

CREATE TYPE system_role AS ENUM (
  'primary',              -- Main system for this process
  'secondary',            -- Supporting system
  'reference',            -- Read-only / lookup
  'integration_target'    -- Receives data from this process
);

CREATE TYPE integration_method AS ENUM (
  'api',            -- REST/GraphQL API
  'manual_entry',   -- Human data entry
  'manual_export',  -- Export file, import elsewhere
  'file_transfer',  -- Automated file exchange
  'webhook',        -- Event-driven push
  'central_hub'     -- System acts as central data hub
);
```

---

## 2. SystemCatalogue Table (Enhanced)

Replaces Blueprint §9.6.9 SystemCatalogue.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK, DEFAULT gen_random_uuid() | |
| `organization_id` | UUID | FK → organization(id), NOT NULL | RLS tenant key |
| `name` | VARCHAR(255) | NOT NULL | System name |
| `description` | TEXT | | General description |
| `scope_description` | TEXT | | **NEW** — Business functions covered |
| `system_type` | system_type | NOT NULL | Extended enum (see §1) |
| `provider_name` | VARCHAR(255) | | **RENAMED** from `vendor` — Provider company |
| `provider_type` | provider_type | | **NEW** — internal / saas / onprem / custom / oss |
| `primary_users` | VARCHAR(255) | | **NEW** — Department scope: 'All', 'QA', 'Finance' |
| `access_methods` | JSONB | DEFAULT '[]' | **NEW** — ["web_browser", "desktop_app", "mobile_app"] |
| `is_saas` | BOOLEAN | DEFAULT FALSE | **NEW** — SaaS-delivered? |
| `hosting_model` | hosting_model | | **NEW** — cloud_global / cloud_china / on_premise / hybrid |
| `operating_region` | operating_region | | **NEW** — global / china_only / international_only / multi_region |
| `integration_method` | VARCHAR(255) | | **NEW** — Primary integration approach |
| `criticality` | system_criticality | DEFAULT 'medium' | **NEW** |
| `owner_id` | UUID | FK → "user"(id) | **NEW** — IT owner |
| `license_model` | license_model | | **NEW** |
| `compliance_notes` | TEXT | | **NEW** — Data residency, regulatory notes |
| `url` | VARCHAR(500) | | **NEW** — System URL or endpoint |
| `status` | catalogue_status | NOT NULL | evaluate / maintain / optimize / retire |
| `metadata` | JSONB | DEFAULT '{}' | Extensible (version, contract dates, SLA) |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |
| `updated_at` | TIMESTAMPTZ | DEFAULT now() | |
| `created_by` | UUID | FK → "user"(id) | |
| `updated_by` | UUID | FK → "user"(id) | |

**RLS Policy:**
```sql
CREATE POLICY tenant_isolation ON system_catalogue
  USING (organization_id = current_setting('app.current_org')::uuid);
```

**Indexes:**
```sql
CREATE INDEX idx_system_cat_org ON system_catalogue(organization_id);
CREATE INDEX idx_system_cat_type ON system_catalogue(organization_id, system_type);
CREATE INDEX idx_system_cat_status ON system_catalogue(organization_id, status);
CREATE INDEX idx_system_cat_region ON system_catalogue(organization_id, operating_region);
```

---

## 3. ProcessSystem Junction Table (Enhanced)

Replaces Blueprint §9.6.8 ProcessSystem linkage.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK, DEFAULT gen_random_uuid() | |
| `organization_id` | UUID | FK → organization(id), NOT NULL | RLS tenant key |
| `process_id` | UUID | FK → process(id), NOT NULL | |
| `system_id` | UUID | FK → system_catalogue(id), NOT NULL | |
| `purpose` | TEXT | | **NEW** — What system does for this process |
| `system_role` | system_role | DEFAULT 'primary' | **NEW** — primary / secondary / reference / integration_target |
| `integration_method` | integration_method | | **NEW** — How data flows |
| `criticality` | system_criticality | DEFAULT 'medium' | **NEW** — Process-level criticality |
| `user_scope` | VARCHAR(255) | | **NEW** — Which team uses it here |
| `pain_points` | TEXT | | **NEW** — Known issues |
| `automation_potential` | agentic_potential | | **NEW** — Reuse existing enum: none / low / medium / high |
| `status` | VARCHAR(20) | DEFAULT 'active' | active / planned / deprecated |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |
| `updated_at` | TIMESTAMPTZ | DEFAULT now() | |

**Unique constraint:**
```sql
ALTER TABLE process_system ADD CONSTRAINT uq_process_system
  UNIQUE (organization_id, process_id, system_id);
```

---

## 4. Seed Data — SystemCatalogue (Surity)

Insert after org and user records exist.

```sql
INSERT INTO system_catalogue
  (organization_id, name, description, scope_description, system_type, provider_name, provider_type,
   primary_users, access_methods, is_saas, hosting_model, operating_region,
   criticality, license_model, status)
VALUES
  -- 1. ERP System
  (:org_id, 'ERP System',
   'Customized ERP by Fumasoft',
   'End-to-end: supplier/factory/customer management, project/quotation/product, factory audit job, ordering & shipment, reporting',
   'erp', 'Fumasoft', 'custom_developed',
   'All', '["web_browser"]', false, 'on_premise', 'china_only',
   'critical', 'custom_contract', 'optimize'),

  -- 2. Email & OneDrive (M365)
  (:org_id, 'Email & OneDrive (M365)',
   'Microsoft 365 Business Standard',
   'Email communication and file storage',
   'communication', 'Microsoft', 'commercial_saas',
   'All', '["desktop_app","mobile_app","web_browser"]', true, 'cloud_global', 'global',
   'high', 'subscription', 'maintain'),

  -- 3. Factory Audit App
  (:org_id, 'Factory Audit App',
   'Developed by Chongqing Yida',
   'Audit questionnaire with rate calculation and report generation',
   'quality', 'Chongqing Yida', 'custom_developed',
   'QA', '["mobile_app"]', false, 'on_premise', 'china_only',
   'medium', 'custom_contract', 'evaluate'),

  -- 4. FangCloud
  (:org_id, 'FangCloud',
   'yifangyun cloud storage',
   'Key quality files: Framework docs, Factory Audit Reports, Technical Files',
   'collaboration', 'yifangyun', 'commercial_saas',
   'QA', '["desktop_app","mobile_app","web_browser"]', true, 'cloud_china', 'multi_region',
   'medium', 'subscription', 'maintain'),

  -- 5. Contract Management System
  (:org_id, 'Contract Management System',
   'zhenling contract platform',
   'Contract lifecycle: buying agreements, office rent, QA 3rd party contracts',
   'contract_mgmt', 'zhenling', 'commercial_saas',
   'Sourcing', '["web_browser"]', true, 'cloud_china', 'china_only',
   'medium', 'subscription', 'maintain'),

  -- 6. Internal Share Drive
  (:org_id, 'Internal Share Drive',
   'Windows Server file share',
   'Internal document storage',
   'file_storage', 'Microsoft', 'internal',
   'All', '["file_browser"]', false, 'on_premise', 'china_only',
   'medium', 'internal', 'retire'),

  -- 7. Kingdee Finance Software
  (:org_id, 'Internal Finance Software (Kingdee)',
   'Kingdee accounting platform',
   'Accounting and financial management',
   'finance', 'Kingdee', 'commercial_onprem',
   'Finance', '["desktop_app"]', false, 'on_premise', 'china_only',
   'high', 'perpetual', 'maintain'),

  -- 8. Ding Talk
  (:org_id, 'Ding Talk',
   'Alibaba workplace platform (free tier)',
   'Leave and trip approval workflows',
   'workflow', 'Alibaba', 'commercial_saas',
   'All', '["desktop_app","mobile_app"]', true, 'cloud_china', 'china_only',
   'low', 'free', 'maintain');
```

---

## 5. Seed Data — ProcessSystem Linkages (Surity)

From Operating Model "Systems & Tools" sheet.

```sql
INSERT INTO process_system
  (organization_id, process_id, system_id, purpose, system_role, integration_method, criticality, user_scope)
VALUES
  -- L2-05 Data Management ↔ ERP
  (:org_id, :process_L2_05, :sys_erp,
   'Product master data repository, order management',
   'primary', 'central_hub', 'critical', 'All staff'),

  -- L2-05 Data Management ↔ SharePoint
  (:org_id, :process_L2_05, :sys_m365,
   'Document management, file storage, collaboration',
   'secondary', 'manual_entry', 'high', 'All staff'),

  -- L2-10 Brief ↔ Email (Outlook)
  (:org_id, :process_L2_10, :sys_m365,
   'Client communication, brief receipt',
   'primary', 'manual_entry', 'high', 'Account team'),

  -- L2-20 Surity Audit ↔ Audit Tracker
  (:org_id, :process_L2_20, :sys_erp,
   'Audit scheduling, findings documentation, grading',
   'primary', 'manual_export', 'medium', 'Quality team'),

  -- L2-28 Test Specification ↔ Testing Lab Portal
  -- Note: Testing Lab Portal not in Surity register — external system, add separately or as metadata
  (:org_id, :process_L2_28, :sys_erp,
   'Test tracking and certificate management',
   'secondary', 'manual_entry', 'high', 'Quality team'),

  -- L2-37 Order Management ↔ ERP
  (:org_id, :process_L2_37, :sys_erp,
   'PO creation, production tracking',
   'primary', 'central_hub', 'critical', 'Sourcing team'),

  -- L2-39 Inspection ↔ ERP
  (:org_id, :process_L2_39, :sys_erp,
   'Inspection scheduling, results tracking, defect logging',
   'primary', 'manual_export', 'high', 'QC team'),

  -- L2-44 Shipment Booking ↔ ERP
  (:org_id, :process_L2_44, :sys_erp,
   'Shipment data and documentation',
   'secondary', 'manual_entry', 'high', 'Logistics team'),

  -- L2-47 Documentation & Payment ↔ Kingdee
  (:org_id, :process_L2_47, :sys_kingdee,
   'Invoice processing, payment tracking, reconciliation',
   'primary', 'api', 'critical', 'Finance team');
```

---

## 6. API Endpoints

### GET /api/v1/systems
- Query params: `status`, `system_type`, `hosting_model`, `operating_region`, `criticality`
- Response includes `process_count` (aggregate from process_system)
- Paginated, sorted by name default

### GET /api/v1/systems/:id
- Full system record + linked processes (from process_system JOIN process)

### POST /api/v1/systems
- All fields from §2. Validate enums server-side.
- `access_methods` must be valid JSON array of strings.

### PATCH /api/v1/systems/:id
- Partial update. Status changes should log to audit_log.
- If status changes to 'retire', optionally create RIADA Action item.

### GET /api/v1/processes/:id/systems
- Returns systems linked to a process via process_system, with junction metadata.

### POST /api/v1/processes/:id/systems
- Create process-system linkage. Body: `{ system_id, purpose, system_role, integration_method, criticality, user_scope }`

---

## 7. UI Components

| Component | Location | Description |
|-----------|----------|-------------|
| SystemRegistryView | `/systems` | Table/card list with filters: status, type, hosting, region, criticality |
| SystemDetailPanel | `/systems/:id` | Full metadata + linked processes + RIADA items |
| ProcessSystemOverlay | Process canvas overlay | Badge processes by system criticality |
| StatusBadge | Shared component | Colour-coded: evaluate=blue, maintain=green, optimize=amber, retire=red |
| RegionIndicator | Shared component | Flag icon for operating_region |

---

## 8. Migration Checklist

- [ ] Create enum types (§1)
- [ ] ALTER system_catalogue — add 15 columns, rename vendor → provider_name
- [ ] ALTER process_system — add 7 columns, add unique constraint
- [ ] Create RLS policies on both tables
- [ ] Create indexes (§2)
- [ ] Seed 8 system records (§4)
- [ ] Seed 9 process-system linkages (§5)
- [ ] Extend API endpoints (§6)
- [ ] Build UI components (§7)
- [ ] Update CLAUDE.md component reference table
