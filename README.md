# Process Catalogue — Project Files

**Version:** Blueprint v1.9 (auth-reconciled)
**Date:** 2026-02-01
**Readiness:** 76% — Ready for Development

---

## Directory Structure

```
process_catalogue_x/
│
├── Blueprint.md                          ← PRIMARY SPEC (7,282 lines, v1.9)
│                                           Complete software requirements document.
│                                           This is the single source of truth.
│
├── CLAUDE_CODE_IMPLEMENTATION_GUIDE.md   ← Build instructions for Claude Code
│                                           Phase-by-phase implementation roadmap,
│                                           file structure, dependency lists.
│
├── build/                                ← SCAFFOLDED CODEBASE (monorepo)
│   ├── package.json                        Root monorepo config (pnpm workspaces)
│   ├── pnpm-workspace.yaml                 Workspace definition
│   ├── turbo.json                          Turborepo pipeline config
│   ├── .env.example                        Environment variable template
│   ├── .gitignore                          Git ignore rules
│   │
│   ├── packages/
│   │   ├── api/                            FastAPI backend (Python 3.11+)
│   │   │   ├── src/
│   │   │   │   ├── main.py                 App entrypoint
│   │   │   │   ├── api/v1/endpoints/       Route handlers (auth, processes, riada, etc.)
│   │   │   │   ├── core/                   Auth, database, multi-tenancy middleware
│   │   │   │   ├── models/                 SQLAlchemy ORM models (45+ tables)
│   │   │   │   ├── schemas/                Pydantic request/response schemas
│   │   │   │   ├── services/               Business logic layer
│   │   │   │   └── utils/                  Shared utilities
│   │   │   ├── tests/                      Unit + integration tests
│   │   │   ├── alembic/                    Database migrations
│   │   │   ├── requirements.txt            Python dependencies
│   │   │   └── Dockerfile                  Container build
│   │   │
│   │   ├── web/                            Next.js 14+ frontend (TypeScript)
│   │   │   ├── src/
│   │   │   │   ├── app/                    App Router pages
│   │   │   │   │   ├── auth/               Login + magic link verify
│   │   │   │   │   └── (authenticated)/    All protected routes
│   │   │   │   │       ├── dashboard/
│   │   │   │   │       ├── processes/      List + canvas views
│   │   │   │   │       ├── riada/          RIADA list + create
│   │   │   │   │       ├── business-model/
│   │   │   │   │       ├── portfolio/      List + create
│   │   │   │   │       ├── surveys/
│   │   │   │   │       ├── prompts/
│   │   │   │   │       ├── reports/
│   │   │   │   │       ├── reference-data/
│   │   │   │   │       └── settings/       General, Users, Integrations
│   │   │   │   ├── components/layout/      Sidebar, Header (app shell)
│   │   │   │   ├── lib/                    API client, utilities
│   │   │   │   └── stores/                 Zustand state management
│   │   │   ├── tailwind.config.ts          Surity theme (grey + yellow)
│   │   │   ├── package.json                Frontend dependencies
│   │   │   └── tsconfig.json               TypeScript config
│   │   │
│   │   └── shared/                         Shared types and constants
│   │
│   ├── infrastructure/
│   │   ├── docker/                         Docker Compose (local dev)
│   │   │   ├── docker-compose.yml          PostgreSQL + Redis + API + Web
│   │   │   └── init-db.sql                 Database initialization
│   │   └── terraform/                      IaC for cloud deployment
│   │
│   └── scripts/                            Build/deploy automation
│
├── scripts/
│   ├── create_project_structure.sh         Bash script to scaffold from scratch
│   └── split_blueprint.py                  Utility to split Blueprint into sections
│
├── templates/
│   └── .claude/context.md                  Claude Code project context file
│
├── docs/
│   └── Development_Readiness_Report.docx   Professional handoff report (76% score)
│
├── reference/                              SOURCE DATA (read-only reference)
│   ├── Business_Model_Integration_Guide.md Surity business model documentation
│   └── Surity_Process_Catalogue_Operating_Model.xlsx
│                                           14-sheet Excel with live Surity data
│                                           (Process Catalogue, RACI, KPIs, SIPOC, etc.)
│
└── process-catalogue-template.zip          Alternate pre-packaged template
```

---

## Quick Start

### For Claude Code

1. Open this folder as a Claude Code project
2. Copy `templates/.claude/context.md` → `.claude/context.md` at project root
3. Point Claude Code at `Blueprint.md` as the primary specification
4. Follow `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` for phased build instructions

### For Manual Development

1. `cd build/`
2. Copy `.env.example` → `.env` and fill in values
3. `pnpm install` (requires pnpm 8+)
4. `docker compose -f infrastructure/docker/docker-compose.yml up -d`
5. `pnpm dev` (starts both API and Web in parallel)

---

## Authentication Architecture

**Primary:** Passwordless magic links (email-only, no passwords)
**Enterprise add-on:** OAuth 2.0 / OIDC / SAML 2.0 SSO via Clerk (Global) or Keycloak (China)

All auth references across Sections 6.2, 8.2, 9.3, 9.8, 9.9, 9.10, and 14 are reconciled.
Section 6.2 is the authoritative specification.

---

## Tech Stack

| Layer | Global SaaS | China |
|-------|-------------|-------|
| Frontend | Next.js 14+ on Vercel | Next.js 14+ on Alibaba ECS |
| Backend | FastAPI on Railway | FastAPI on Alibaba ECS |
| Database | Supabase (PostgreSQL) | Alibaba RDS PostgreSQL |
| Auth | Supabase Auth (magic links) | Alibaba IDaaS |
| Storage | Cloudflare R2 | Alibaba OSS |
| Cache | Upstash Redis | Alibaba Redis |
| LLM | Anthropic Claude / OpenAI | Alibaba Qwen / Baidu ERNIE |

---

## Key Documents

| Document | Purpose |
|----------|---------|
| `Blueprint.md` | Complete software requirements (7,282 lines) |
| `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` | Phase-by-phase build instructions |
| `docs/Development_Readiness_Report.docx` | Formal readiness assessment |
| `Design_Coherence_Analysis.md` | UI/UX design consistency analysis |
| `UI_DESIGN_QUESTIONS.md` | Detailed UI specification questionnaire |
| `reference/Surity_Process_Catalogue_Operating_Model.xlsx` | Source data (14 sheets) |
| `reference/Business_Model_Integration_Guide.md` | Business model documentation |
