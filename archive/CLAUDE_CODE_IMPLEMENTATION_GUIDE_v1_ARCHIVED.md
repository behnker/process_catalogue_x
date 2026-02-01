# Claude Code Implementation Guide
## Process Catalogue Platform

---

## Executive Summary

This guide outlines how to structure the Process Catalogue project for optimal development using Claude Code. The key recommendations are:

1. **Break Blueprint.md into smaller, focused documents** (~320KB is too large for effective context)
2. **Create a clear folder structure** separating requirements, specs, and code
3. **Use a phased implementation approach** with clear milestones
4. **Provide Claude Code with focused context** per development task

---

## 1. Blueprint Decomposition Strategy

### Current State Analysis

| Metric | Value | Issue |
|--------|-------|-------|
| Total Lines | 5,662 | Too long for single context |
| File Size | ~320KB | Exceeds optimal context window usage |
| Sections | 16 major | Need topic-based separation |

### Recommended Document Structure

Break the monolithic Blueprint into **focused requirement documents**:

```
/docs/
├── 00_PROJECT_OVERVIEW.md           (~50 lines)   - Purpose, scope, tech stack summary
├── 01_ARCHITECTURE.md               (~300 lines)  - Technical architecture, deployment
├── 02_DATA_MODEL.md                 (~600 lines)  - Complete data model, ERD, all tables
├── 03_API_SPECIFICATION.md          (~400 lines)  - API endpoints, contracts
│
├── components/
│   ├── C1_BUSINESS_MODEL.md         (~200 lines)  - Component 1 requirements
│   ├── C2_PROCESS_CATALOGUE.md      (~300 lines)  - Component 2 requirements
│   ├── C3_QUALITY_LOGS.md           (~200 lines)  - Component 3 (RIADA) requirements
│   ├── C4_OPERATING_MODEL.md        (~400 lines)  - Component 4 requirements
│   ├── C5_PORTFOLIO.md              (~300 lines)  - Component 5 requirements
│   ├── C6_CHANGE_ADOPTION.md        (~200 lines)  - Component 6 requirements
│   └── C7_SURVEYS.md                (~300 lines)  - Component 7 requirements
│
├── features/
│   ├── F1_PROMPT_LIBRARY.md         (~300 lines)  - Prompt Library feature
│   ├── F2_LLM_INTEGRATION.md        (~300 lines)  - LLM connectivity
│   ├── F3_HEATMAPS_OVERLAYS.md      (~400 lines)  - Visualization features
│   ├── F4_AGENTIC_OPPORTUNITIES.md  (~300 lines)  - Agentic tracking
│   └── F5_REPORTING.md              (~200 lines)  - Reports & dashboards
│
├── ui/
│   ├── UI_DESIGN_SYSTEM.md          (~200 lines)  - Colors, typography, components
│   ├── UI_PROCESS_CANVAS.md         (~300 lines)  - Canvas visualization spec
│   ├── UI_NAVIGATION.md             (~150 lines)  - Navigation structure
│   └── UI_SCREENS.md                (~300 lines)  - Key screen specifications
│
├── infrastructure/
│   ├── INFRA_GLOBAL.md              (~200 lines)  - Vercel/Supabase setup
│   ├── INFRA_CHINA.md               (~200 lines)  - Alibaba Cloud setup
│   └── INFRA_SECURITY.md            (~150 lines)  - Security requirements
│
└── reference/
    ├── GLOSSARY.md                  (~100 lines)  - Terms and definitions
    ├── PERSONAS.md                  (~150 lines)  - 14 user personas
    └── NFR.md                       (~200 lines)  - Non-functional requirements
```

**Total: ~25 documents averaging ~250 lines each**

### Why This Structure Works Better

| Benefit | Explanation |
|---------|-------------|
| **Focused Context** | Claude Code can load only relevant docs for each task |
| **Parallel Development** | Different components can be built independently |
| **Easier Updates** | Change one component without touching others |
| **Clear Ownership** | Each doc has clear scope and purpose |
| **Better Prompting** | "Implement C2_PROCESS_CATALOGUE.md" is clearer than "implement processes from Blueprint" |

---

## 2. Project Folder Structure

### Recommended Repository Structure

```
process-catalogue/
│
├── .claude/                          # Claude Code configuration
│   ├── context.md                    # Default context for Claude Code
│   ├── coding-standards.md           # Coding conventions
│   └── prompts/                      # Reusable prompts for common tasks
│       ├── create-component.md
│       ├── create-api-endpoint.md
│       └── create-db-migration.md
│
├── docs/                             # Requirements & specifications (see above)
│   ├── 00_PROJECT_OVERVIEW.md
│   ├── 01_ARCHITECTURE.md
│   ├── ...
│   └── reference/
│
├── packages/                         # Monorepo packages
│   │
│   ├── web/                          # Next.js frontend
│   │   ├── src/
│   │   │   ├── app/                  # App router pages
│   │   │   │   ├── (auth)/           # Auth pages (login, register)
│   │   │   │   ├── (dashboard)/      # Dashboard layout
│   │   │   │   │   ├── processes/    # Process catalogue pages
│   │   │   │   │   ├── business-model/
│   │   │   │   │   ├── quality-logs/
│   │   │   │   │   ├── operating-model/
│   │   │   │   │   ├── portfolio/
│   │   │   │   │   ├── change-adoption/
│   │   │   │   │   ├── surveys/
│   │   │   │   │   ├── prompts/
│   │   │   │   │   ├── reports/
│   │   │   │   │   └── settings/
│   │   │   │   └── api/              # API routes (if using Next.js API)
│   │   │   │
│   │   │   ├── components/           # React components
│   │   │   │   ├── ui/               # Base UI components (shadcn)
│   │   │   │   ├── layout/           # Layout components
│   │   │   │   ├── process/          # Process-specific components
│   │   │   │   ├── canvas/           # Process Canvas components
│   │   │   │   ├── riada/            # RIADA components
│   │   │   │   ├── charts/           # Chart/visualization components
│   │   │   │   └── forms/            # Form components
│   │   │   │
│   │   │   ├── hooks/                # Custom React hooks
│   │   │   ├── lib/                  # Utility functions
│   │   │   ├── stores/               # Zustand stores
│   │   │   ├── types/                # TypeScript types
│   │   │   └── styles/               # Global styles
│   │   │
│   │   ├── public/                   # Static assets
│   │   ├── package.json
│   │   ├── tailwind.config.ts
│   │   ├── tsconfig.json
│   │   └── next.config.js
│   │
│   ├── api/                          # FastAPI backend (or separate repo)
│   │   ├── src/
│   │   │   ├── main.py               # FastAPI app entry
│   │   │   ├── config/               # Configuration
│   │   │   ├── api/
│   │   │   │   ├── v1/
│   │   │   │   │   ├── endpoints/    # API endpoints by domain
│   │   │   │   │   │   ├── processes.py
│   │   │   │   │   │   ├── business_model.py
│   │   │   │   │   │   ├── riada.py
│   │   │   │   │   │   ├── portfolio.py
│   │   │   │   │   │   ├── surveys.py
│   │   │   │   │   │   ├── prompts.py
│   │   │   │   │   │   └── llm.py
│   │   │   │   │   └── router.py
│   │   │   │   └── deps.py           # Dependencies (auth, db)
│   │   │   │
│   │   │   ├── models/               # SQLAlchemy/Pydantic models
│   │   │   │   ├── core.py           # Organization, User, Role
│   │   │   │   ├── business_model.py
│   │   │   │   ├── process.py
│   │   │   │   ├── riada.py
│   │   │   │   ├── portfolio.py
│   │   │   │   ├── survey.py
│   │   │   │   ├── agent.py
│   │   │   │   └── prompt.py
│   │   │   │
│   │   │   ├── schemas/              # Pydantic schemas (API contracts)
│   │   │   ├── services/             # Business logic
│   │   │   ├── repositories/         # Data access layer
│   │   │   └── utils/                # Utilities
│   │   │
│   │   ├── tests/                    # API tests
│   │   ├── alembic/                  # Database migrations
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   └── shared/                       # Shared types/utilities
│       ├── types/                    # TypeScript types shared between packages
│       └── constants/                # Shared constants
│
├── infrastructure/                   # Infrastructure as Code
│   ├── terraform/
│   │   ├── global/                   # Vercel, Supabase, R2
│   │   └── china/                    # Alibaba Cloud
│   └── docker/
│       └── docker-compose.yml        # Local development
│
├── scripts/                          # Build/deploy scripts
│   ├── setup.sh
│   ├── seed-data.sh
│   └── deploy.sh
│
├── .github/                          # GitHub Actions
│   └── workflows/
│       ├── ci.yml
│       ├── deploy-global.yml
│       └── deploy-china.yml
│
├── package.json                      # Root package.json (monorepo)
├── turbo.json                        # Turborepo config
├── pnpm-workspace.yaml               # PNPM workspace config
└── README.md
```

---

## 3. Claude Code Context Strategy

### The Context Problem

Claude Code has a limited context window. Loading the entire 320KB Blueprint wastes context on irrelevant sections.

### Solution: Layered Context Approach

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           CLAUDE CODE CONTEXT LAYERS                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  LAYER 1: ALWAYS LOADED (~100 lines)                                            │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  .claude/context.md                                                      │   │
│  │  • Project purpose (1 paragraph)                                         │   │
│  │  • Tech stack summary                                                    │   │
│  │  • Coding conventions                                                    │   │
│  │  • File naming rules                                                     │   │
│  │  • Key architectural decisions                                           │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  LAYER 2: TASK-SPECIFIC (~200-400 lines)                                        │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  Load relevant requirement doc(s) for current task:                      │   │
│  │  • Building Process Catalogue? → Load C2_PROCESS_CATALOGUE.md           │   │
│  │  • Building Canvas? → Load UI_PROCESS_CANVAS.md                         │   │
│  │  • Building API? → Load 03_API_SPECIFICATION.md + relevant component    │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  LAYER 3: REFERENCE (Load as needed)                                            │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  • Data model (when creating DB schema)                                  │   │
│  │  • UI Design System (when building components)                           │   │
│  │  • Glossary (when naming is unclear)                                     │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Example: .claude/context.md

```markdown
# Process Catalogue - Claude Code Context

## Project Purpose
Build a multi-tenant SaaS platform for designing business/operating models, 
tracking quality issues (RIADA), managing portfolios, and monitoring adoption.

## Tech Stack
- **Frontend:** Next.js 14+ (App Router), TypeScript, Tailwind CSS, shadcn/ui
- **Backend:** FastAPI (Python 3.11+), SQLAlchemy, Pydantic
- **Database:** PostgreSQL (Supabase for global, ApsaraDB for China)
- **Auth:** Supabase Auth / Alibaba IDaaS
- **Storage:** Cloudflare R2 / Alibaba OSS
- **LLM:** OpenAI/Anthropic (global), Qwen (China)

## Coding Conventions
- Use TypeScript strict mode
- Prefer functional components with hooks
- Use Zustand for state management
- Follow REST API conventions
- Use snake_case for Python, camelCase for TypeScript
- All components in PascalCase
- All API endpoints prefixed with /api/v1/

## Key Architectural Decisions
1. Multi-tenancy via Row-Level Security (RLS)
2. All tables have organization_id for tenant isolation
3. Polymorphic RIADA attachment (links to any entity)
4. Process hierarchy is self-referential (parent_id)
5. Current vs Future state for Operating Model

## File Naming
- React components: PascalCase.tsx (e.g., ProcessCanvas.tsx)
- API endpoints: snake_case.py (e.g., process_catalogue.py)
- Types: PascalCase.ts (e.g., Process.ts)
- Hooks: use{Name}.ts (e.g., useProcesses.ts)

## When Building Features
1. Read the relevant requirement doc in /docs/
2. Check the data model in /docs/02_DATA_MODEL.md
3. Follow the UI patterns in /docs/ui/UI_DESIGN_SYSTEM.md
4. Write tests alongside code
```

---

## 4. Phased Implementation Plan

### Phase Overview

| Phase | Focus | Duration | Deliverables |
|-------|-------|----------|--------------|
| **Phase 0** | Setup & Foundation | 1 week | Project structure, CI/CD, auth |
| **Phase 1** | Core Data Model | 2 weeks | Database, migrations, base API |
| **Phase 2** | Process Catalogue | 3 weeks | Component 2 + Canvas UI |
| **Phase 3** | Business Model | 2 weeks | Component 1 + linkage |
| **Phase 4** | RIADA | 2 weeks | Component 3 + dashboards |
| **Phase 5** | Operating Model | 3 weeks | Component 4 + SOM publishing |
| **Phase 6** | Portfolio | 2 weeks | Component 5 + WSVF |
| **Phase 7** | Change & Surveys | 3 weeks | Components 6 & 7 |
| **Phase 8** | LLM & Prompts | 2 weeks | LLM integration, Prompt Library |
| **Phase 9** | Heatmaps & Reports | 2 weeks | Overlays, dashboards, exports |
| **Phase 10** | Polish & Launch | 2 weeks | Testing, optimization, docs |

**Total: ~24 weeks (~6 months)**

### Phase Details

#### Phase 0: Setup & Foundation (Week 1)

**Tasks:**
1. Initialize monorepo structure
2. Set up Next.js with TypeScript, Tailwind, shadcn/ui
3. Set up FastAPI with SQLAlchemy
4. Configure Supabase project (auth, database)
5. Set up CI/CD (GitHub Actions)
6. Implement basic auth flow
7. Create base layout components

**Claude Code Prompt:**
```
Read /docs/01_ARCHITECTURE.md and /docs/infrastructure/INFRA_GLOBAL.md.
Set up the project structure as defined in the implementation guide.
Initialize a Next.js 14 app with TypeScript, Tailwind, and shadcn/ui.
Configure Supabase for authentication.
Create the base layout with sidebar navigation.
```

**Success Criteria:**
- [ ] Monorepo builds and runs locally
- [ ] User can sign up and log in
- [ ] Base dashboard layout renders
- [ ] CI pipeline passes

---

#### Phase 1: Core Data Model (Weeks 2-3)

**Tasks:**
1. Create all database tables from data model
2. Implement Row-Level Security policies
3. Create base CRUD API endpoints
4. Set up Alembic migrations
5. Create seed data script

**Claude Code Prompt:**
```
Read /docs/02_DATA_MODEL.md.
Create SQLAlchemy models for all core tables:
- Organization, User, Role, UserRole
- Process (with self-referential hierarchy)
- RiadaItem, RiadaAttachment
- All reference catalogues

Implement RLS policies for multi-tenancy.
Create Alembic migrations.
Create a seed data script with sample organization and processes.
```

**Success Criteria:**
- [ ] All 45+ tables created
- [ ] RLS policies enforce tenant isolation
- [ ] Migrations run cleanly
- [ ] Seed data loads successfully

---

#### Phase 2: Process Catalogue (Weeks 4-6)

**Tasks:**
1. Process CRUD API endpoints
2. Process hierarchy navigation
3. Process Canvas visualization
4. Process detail view
5. RAG status display
6. Process filtering

**Claude Code Prompt:**
```
Read /docs/components/C2_PROCESS_CATALOGUE.md and /docs/ui/UI_PROCESS_CANVAS.md.

Build the Process Catalogue feature:

1. API endpoints (FastAPI):
   - GET /api/v1/processes (list with hierarchy)
   - GET /api/v1/processes/{id} (detail)
   - POST /api/v1/processes (create)
   - PUT /api/v1/processes/{id} (update)
   - DELETE /api/v1/processes/{id} (soft delete)

2. Frontend:
   - ProcessCanvas component (swimlane layout)
   - ProcessList component (table view)
   - ProcessDetail component (tabbed detail)
   - ProcessForm component (create/edit)

Follow the canvas layout: L0 horizontal, L1 horizontal, L2 vertical columns,
L3/L4/L5 as expandable nested menus.
```

**Success Criteria:**
- [ ] Process Canvas displays hierarchy correctly
- [ ] User can navigate L0 → L5
- [ ] User can create/edit processes
- [ ] RAG status displays correctly
- [ ] Filtering works (by level, owner, status)

---

### Implementation Ticket Template

For each feature, create a structured ticket:

```markdown
## Feature: [Feature Name]

### Requirements Document
/docs/[relevant-doc].md

### Data Model
Tables involved:
- Table1 (columns: x, y, z)
- Table2 (columns: a, b, c)

### API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/... | List all |
| POST | /api/v1/... | Create new |

### UI Components
- Component1: Description
- Component2: Description

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Test Cases
1. Test case 1
2. Test case 2
```

---

## 5. Claude Code Best Practices

### DO ✅

| Practice | Reason |
|----------|--------|
| **Give focused tasks** | "Build the Process CRUD API" not "Build the whole backend" |
| **Reference specific docs** | "Read C2_PROCESS_CATALOGUE.md and implement..." |
| **Provide examples** | Include sample data, expected outputs |
| **Review incrementally** | Review each component before moving to next |
| **Use consistent naming** | Follow the conventions in context.md |
| **Write tests alongside code** | Ask Claude to generate tests with each feature |

### DON'T ❌

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| **Loading entire Blueprint** | Wastes context, causes hallucinations |
| **Vague requirements** | "Make it work" → inconsistent results |
| **Multiple features at once** | Context overload, mixed implementations |
| **Skipping data model** | Building UI without API causes rework |
| **No acceptance criteria** | Can't verify correct implementation |

### Effective Prompting Patterns

**Pattern 1: Incremental Build**
```
Step 1: Create the database model for Process table
Step 2: Create the Pydantic schemas for Process
Step 3: Create the CRUD repository for Process
Step 4: Create the API endpoints for Process
Step 5: Create the React components for Process list
Step 6: Add filtering and pagination
```

**Pattern 2: Reference + Task**
```
Read /docs/components/C2_PROCESS_CATALOGUE.md section 4.2.

Create the Process API endpoints with:
- Pagination (limit/offset)
- Filtering (by level, owner, status)
- Sorting (by name, code, updated_at)
- Include child count in response

Return JSON matching this schema:
{
  "items": [...],
  "total": 100,
  "page": 1,
  "per_page": 20
}
```

**Pattern 3: Example-Driven**
```
Create a ProcessCard component that displays:
- Process name and code (e.g., "L2-10 Brief")
- RAG status dots (🟢🟡🔴) for SPRD dimensions
- Issue count badge
- Owner avatar

Example usage:
<ProcessCard
  process={{
    code: "L2-10",
    name: "Brief",
    rag_people: "green",
    rag_process: "amber",
    rag_system: "green",
    rag_data: "green",
    issue_count: 3,
    owner: { name: "John", avatar: "..." }
  }}
  onClick={() => navigate(`/processes/${id}`)}
/>
```

---

## 6. Document Generation Script

Use this script to break down the Blueprint:

```bash
#!/bin/bash
# split-blueprint.sh

# Create docs directory structure
mkdir -p docs/components docs/features docs/ui docs/infrastructure docs/reference

# Function to extract section
extract_section() {
  local start_pattern="$1"
  local end_pattern="$2"
  local output_file="$3"
  
  sed -n "/${start_pattern}/,/${end_pattern}/p" Blueprint.md > "$output_file"
}

echo "Splitting Blueprint.md into focused documents..."

# Extract each section (patterns would need to be customized)
# This is a conceptual example - actual implementation would use
# more sophisticated parsing

echo "Done. Review docs/ directory for generated files."
```

---

## 7. Recommended Next Steps

### Immediate Actions

1. **Create the /docs folder structure** with empty files
2. **Extract content from Blueprint.md** into respective docs
3. **Create .claude/context.md** with project essentials
4. **Initialize the repository** with the folder structure
5. **Set up CI/CD** before any coding begins

### First Claude Code Session

```
I'm starting the Process Catalogue project.

Read: .claude/context.md

Task: Initialize the monorepo with:
1. Root package.json with pnpm workspaces and Turborepo
2. packages/web - Next.js 14 app with TypeScript and Tailwind
3. packages/api - FastAPI skeleton
4. Basic GitHub Actions CI workflow

Do NOT implement features yet - just the project skeleton.
```

### Verification Checklist

- [ ] Blueprint split into ~25 focused documents
- [ ] Each doc is <400 lines
- [ ] .claude/context.md created
- [ ] Folder structure matches the guide
- [ ] README.md documents how to run locally
- [ ] CI/CD pipeline configured

---

## 8. Summary

| Aspect | Recommendation |
|--------|----------------|
| **Blueprint Size** | Too large (320KB) - split into ~25 documents |
| **Context Strategy** | Layered approach - always load context.md, then task-specific docs |
| **Folder Structure** | Monorepo with packages/web, packages/api, docs/ |
| **Implementation** | Phased over ~24 weeks, data model first |
| **Prompting** | Focused, reference-specific, example-driven |
| **Testing** | Write alongside code, not after |

---

*Guide Version: 1.0*
*Last Updated: January 31, 2026*
