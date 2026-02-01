# Implementation Guide
## Process Catalogue Platform

> **Authoritative context:** `CLAUDE.md` is the single source of truth for coding standards, conventions, and architectural decisions. This guide covers implementation phases and task breakdown only.

---

## Phase Overview

| Phase | Focus | Key Deliverables |
|-------|-------|------------------|
| **0** | Foundation | CI/CD, auth flow, RLS middleware, pytest/vitest fixtures |
| **1** | Core CRUD | Process Catalogue (L0–L5), RIADA, Business Model Canvas |
| **2** | Advanced | Operating Model, Portfolio, Surveys, Prompt Library, LLM integration |
| **3** | Hardening | E2E tests (Playwright), load testing (k6), China deployment, i18n |

**Current status:** Pre-Phase 0. Scaffold complete, specification finalised.

---

## Phase 0: Foundation

### Tasks

1. **CI/CD Pipeline**
   - GitHub Actions: lint, type-check, test on PR
   - Ruff + mypy (Python), ESLint + tsc (TypeScript)

2. **Database Setup**
   - Run Alembic migrations
   - Verify RLS policies on all tenant tables
   - Create seed data script

3. **Auth Flow**
   - Magic link request → email via Resend
   - Token verification → JWT issuance
   - Refresh token rotation
   - Protected route middleware (frontend)

4. **Test Fixtures**
   - pytest: async DB session, test organization, test user
   - vitest: mock API client, auth store

### Success Criteria
- [ ] `pnpm dev` starts both frontend and API
- [ ] User can request magic link, receive email, and log in
- [ ] Protected routes redirect unauthenticated users
- [ ] CI pipeline passes on all checks

---

## Phase 1: Core CRUD

### 1.1 Process Catalogue

**Models:** `Process`, `ProcessOperatingModel`

**API Endpoints:**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/processes` | List (paginated, filterable by level/status/owner) |
| GET | `/api/v1/processes/{id}` | Detail with children |
| POST | `/api/v1/processes` | Create |
| PATCH | `/api/v1/processes/{id}` | Update |
| DELETE | `/api/v1/processes/{id}` | Soft delete |

**Frontend:**
- Process Canvas (swimlane layout per Blueprint §10.2)
- Process List (table view with toggle)
- Process Detail (slide-over panel for L3/L4/L5)
- Process Form (create/edit)

### 1.2 RIADA (Quality Logs)

**Models:** `RiadaItem`

**API Endpoints:**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/riada` | List (filterable by type/severity/status/process) |
| GET | `/api/v1/riada/{id}` | Detail |
| POST | `/api/v1/riada` | Create |
| PATCH | `/api/v1/riada/{id}` | Update |
| DELETE | `/api/v1/riada/{id}` | Soft delete |

**Frontend:**
- RIADA List (table view, type-specific columns)
- RIADA Detail (slide-over panel)
- RIADA Form (context-dependent: modal for simple, panel for complex)

**Note:** Column headings vary by type (Issue/Risk/Dependency/Assumption) — see task list.

### 1.3 Business Model Canvas

**Models:** `BusinessModel`, `BusinessModelEntry`, `BusinessModelMapping`

**API Endpoints:**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/business-models` | List |
| GET | `/api/v1/business-models/{id}` | Detail with entries |
| POST | `/api/v1/business-models` | Create |
| PATCH | `/api/v1/business-models/{id}` | Update |
| POST | `/api/v1/business-models/{id}/entries` | Add entry |
| PATCH | `/api/v1/business-models/{id}/entries/{entry_id}` | Update entry |

**Frontend:**
- BMC Grid View (9-box canvas)
- BMC List View (table/accordion)
- Toggle between views
- Click-to-edit entries (inline)

### Success Criteria
- [ ] Process Canvas displays L0–L5 hierarchy
- [ ] L3/L4/L5 expand in slide-over panel
- [ ] RIADA items can be created and linked to processes
- [ ] Business Model Canvas displays all 9 components
- [ ] All CRUD operations enforce RLS

---

## Phase 2: Advanced Features

### 2.1 Operating Model

**Model:** `ProcessOperatingModel`

**Components per process:**
- SIPOC (Suppliers, Inputs, Process, Outputs, Customers)
- RACI Matrix
- KPIs
- Systems
- Policies
- Timing
- Governance
- Security
- Data

**UI:** Sub-tabs within Process Detail → Operating Model tab
- Current/Future state toggle
- Comparison mode
- Gap Analysis view

### 2.2 Portfolio

**Models:** `PortfolioItem`, `PortfolioMilestone`

**Hierarchy:** Strategic Pillar → Programme → Project → Workstream → Work Package → Epic → Task

**UI:**
- Tree view (primary)
- Table view (toggle)
- Gantt chart (toggle)
- WSVF prioritisation display

### 2.3 Surveys

**Models:** `Survey`, `SurveyQuestion`, `SurveyResponse`

**4 Survey Modes:**
1. AI Fluency (AFI score 0–100)
2. Operating Model (SPRD × RAG)
3. Change Readiness (ADKAR-based)
4. Adoption Evidence

**UI:**
- Survey builder (template-based)
- Survey response (section-by-section with progress)
- Results dashboard

### 2.4 Prompt Library

**Models:** `PromptTemplate`, `PromptExecution`, `LLMConfiguration`

**UI:**
- Prompt browser (card grid, categorised)
- Prompt execution (full page: context + input + output)
- Usage analytics

### Success Criteria
- [ ] Operating Model components editable per process
- [ ] Current/Future state comparison works
- [ ] Portfolio hierarchy navigable
- [ ] All 4 survey types functional
- [ ] Prompts executable with LLM integration

---

## Phase 3: Hardening

### Tasks

1. **E2E Tests**
   - Playwright: auth flow, process CRUD, canvas navigation
   - Critical path coverage

2. **Load Testing**
   - k6 scripts for API endpoints
   - Baseline performance metrics

3. **China Deployment**
   - Terraform for Alibaba Cloud
   - Provider abstraction verification
   - LLM swap (Qwen/ERNIE)

4. **i18n Completion**
   - All user-facing strings through `next-intl`
   - zh-CN translation
   - CI check for raw strings in TSX

5. **Security Audit**
   - OWASP Top 10 checklist
   - RLS policy review
   - Penetration testing (if required)

### Success Criteria
- [ ] E2E tests pass in CI
- [ ] API handles 100 concurrent users
- [ ] China deployment functional
- [ ] zh-CN translation complete
- [ ] No critical security findings

---

## Task Execution Protocol

When implementing any feature:

1. **Read** the relevant Blueprint section
2. **Plan** what files you'll create/modify
3. **Build** data layer → API layer → UI layer
4. **Test** alongside implementation
5. **Verify** RLS, schema parity, i18n compliance

See `CLAUDE.md` for detailed conventions and enforcement checkpoints.

---

## Key Files Reference

| Layer | Location |
|-------|----------|
| API endpoints | `build/packages/api/src/api/v1/endpoints/` |
| Models | `build/packages/api/src/models/` |
| Schemas | `build/packages/api/src/schemas/` |
| Services | `build/packages/api/src/services/` |
| Frontend pages | `build/packages/web/src/app/` |
| Components | `build/packages/web/src/components/` |
| Hooks | `build/packages/web/src/hooks/` |
| Stores | `build/packages/web/src/stores/` |

---

## UI Decisions Summary

Resolved decisions (see `CLAUDE.md` for details):

| Decision | Choice |
|----------|--------|
| App shell | Collapsible sidebar (64px/260px) |
| Header | Logo, breadcrumbs, search, notifications, avatar, "+ New" |
| L3/L4/L5 expansion | Slide-over panel from right |
| BMC screen | Grid + List toggle, click-to-edit |
| RIADA screen | Table only, type-specific columns |
| Portfolio screen | Tree primary, Table + Gantt toggles |
| Data tables | Sort, filter, select, bulk actions, paginate, export |
| Forms | Context-dependent, explicit save |
| Current/Future state | Toggle + comparison + gap analysis |
| Login | Split screen |
| Notifications | Bell icon with dropdown |

---

*Guide Version: 2.0 | Last Updated: February 2026*
