# Process Catalogue - Claude Code Context

> **IMPORTANT:** This file should be loaded at the start of every Claude Code session.
> It provides essential context that applies to all development tasks.

---

## Project Purpose

Build a **multi-tenant SaaS platform** for:
- Designing business and operating models
- Identifying and tracking agentic (automation/AI) opportunities
- Managing quality issues (RIADA framework)
- Tracking portfolio of change projects
- Monitoring adoption with survey support

**Target Users:** DIY retail sourcing companies (initial client: Surity)

---

## Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| **Next.js 14+** | React framework (App Router) |
| **TypeScript** | Type safety |
| **Tailwind CSS** | Styling |
| **shadcn/ui** | Component library |
| **Zustand** | State management |
| **React Query** | Server state |
| **Recharts** | Charts/visualizations |

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | Python API framework |
| **SQLAlchemy** | ORM |
| **Pydantic** | Validation & schemas |
| **Alembic** | Database migrations |
| **Python 3.11+** | Runtime |

### Database & Infrastructure
| Component | Global | China |
|-----------|--------|-------|
| **Database** | Supabase (PostgreSQL) | ApsaraDB (PostgreSQL) |
| **Auth** | Supabase Auth | Alibaba IDaaS |
| **Storage** | Cloudflare R2 | Alibaba OSS |
| **Hosting** | Vercel | Alibaba ECS |
| **LLM** | OpenAI / Anthropic | Alibaba Qwen |

---

## Key Architectural Decisions

### 1. Multi-Tenancy
- **Row-Level Security (RLS)** enforces tenant isolation
- Every table has `organization_id` column
- All queries automatically filtered by organization

### 2. Process Hierarchy
- Self-referential `Process` table with `parent_id`
- 6 levels: L0 (Value Stream) → L5 (Work Instruction)
- Primary (value chain) and Secondary (support) types

### 3. RIADA Polymorphic Attachment
- RIADA items can attach to ANY entity via `RiadaAttachment`
- Uses `entity_type` + `entity_id` pattern
- Enables issues/risks on processes, projects, BM components

### 4. Current vs Future State
- Operating Model components support both states
- Enables gap analysis and transition planning

### 5. Agentic Tracking
- Processes have `agentic_potential` and `automation_level` fields
- Agent Catalogue tracks all AI/automation agents
- ProcessAgent links agents to processes (current/future)

---

## Coding Conventions

### TypeScript / React

```typescript
// Components: PascalCase, functional with hooks
export function ProcessCard({ process, onClick }: ProcessCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  // ...
}

// Hooks: use{Name}
export function useProcesses(filters: ProcessFilters) {
  return useQuery(['processes', filters], () => fetchProcesses(filters));
}

// Types: PascalCase
interface Process {
  id: string;
  code: string;
  name: string;
  level: ProcessLevel;
  parentId: string | null;
}

// Enums: PascalCase with UPPER_CASE values
enum ProcessLevel {
  L0 = 'L0',
  L1 = 'L1',
  // ...
}
```

### Python / FastAPI

```python
# Models: PascalCase
class Process(Base):
    __tablename__ = "process"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organization.id"))
    code: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(255))

# Endpoints: snake_case paths
@router.get("/processes")
async def list_processes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ProcessResponse]:
    # ...

# Schemas: PascalCase
class ProcessCreate(BaseModel):
    code: str
    name: str
    parent_id: uuid.UUID | None = None
```

### File Naming

| Type | Convention | Example |
|------|------------|---------|
| React Components | `PascalCase.tsx` | `ProcessCanvas.tsx` |
| React Hooks | `use{Name}.ts` | `useProcesses.ts` |
| TypeScript Types | `{name}.types.ts` | `process.types.ts` |
| API Endpoints | `snake_case.py` | `process_catalogue.py` |
| SQLAlchemy Models | `snake_case.py` | `process.py` |
| Tests | `{name}.test.ts/py` | `process.test.ts` |

---

## API Conventions

### Endpoint Structure
```
/api/v1/{resource}           # Collection
/api/v1/{resource}/{id}      # Single item
/api/v1/{resource}/{id}/{sub} # Sub-resource
```

### Standard Response Format
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "per_page": 20,
  "has_more": true
}
```

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {"field": "name", "message": "Name is required"}
    ]
  }
}
```

### Common Query Parameters
| Param | Type | Description |
|-------|------|-------------|
| `page` | int | Page number (1-based) |
| `per_page` | int | Items per page (default: 20, max: 100) |
| `sort` | string | Sort field (prefix `-` for desc) |
| `search` | string | Search term |
| `filter[field]` | string | Field filter |

---

## Component Reference (7 Components)

| # | Component | Key Entity | API Prefix |
|---|-----------|------------|------------|
| 1 | Business Model | `BusinessModel`, `CanvasEntry` | `/api/v1/business-models` |
| 2 | Process Catalogue | `Process` | `/api/v1/processes` |
| 3 | Quality Logs | `RiadaItem` | `/api/v1/riada` |
| 4 | Operating Model | `OperatingModelComponent` | `/api/v1/operating-model` |
| 5 | Portfolio | `Portfolio`, `PortfolioItem` | `/api/v1/portfolio` |
| 6 | Change & Adoption | `ChangeIndicator` | `/api/v1/adoption` |
| 7 | Surveys | `SurveyTemplate`, `SurveyInstance` | `/api/v1/surveys` |

---

## Quick Reference: Key Tables

### Process (Core)
```sql
CREATE TABLE process (
  id UUID PRIMARY KEY,
  organization_id UUID REFERENCES organization(id),
  parent_id UUID REFERENCES process(id),
  process_type VARCHAR(20),  -- 'primary', 'secondary'
  level VARCHAR(5),          -- 'L0' to 'L5'
  code VARCHAR(50),
  name VARCHAR(255),
  agentic_potential VARCHAR(20),  -- 'none', 'low', 'medium', 'high'
  current_automation_level VARCHAR(20),
  target_automation_level VARCHAR(20),
  -- ... other fields
);
```

### RiadaItem (Quality Logs)
```sql
CREATE TABLE riada_item (
  id UUID PRIMARY KEY,
  organization_id UUID REFERENCES organization(id),
  riada_type VARCHAR(20),    -- 'risk', 'issue', 'action', 'dependency', 'assumption'
  category VARCHAR(20),      -- 'people', 'process', 'system', 'data'
  severity VARCHAR(20),      -- 'critical', 'high', 'medium', 'low'
  title VARCHAR(255),
  description TEXT,
  status VARCHAR(20),
  owner_id UUID REFERENCES user(id),
  -- ... other fields
);
```

---

## Before You Start a Task

1. **Identify relevant requirement docs** in `/docs/`
2. **Check the data model** in `/docs/02_DATA_MODEL.md`
3. **Follow UI patterns** in `/docs/ui/UI_DESIGN_SYSTEM.md`
4. **Write tests** alongside implementation

---

## Common Tasks Quick Reference

### Creating a New API Endpoint
1. Create/update SQLAlchemy model in `packages/api/src/models/`
2. Create Pydantic schema in `packages/api/src/schemas/`
3. Create repository in `packages/api/src/repositories/`
4. Create endpoint in `packages/api/src/api/v1/endpoints/`
5. Add to router in `packages/api/src/api/v1/router.py`
6. Write tests in `packages/api/tests/`

### Creating a New React Component
1. Create component in `packages/web/src/components/{domain}/`
2. Add types in `packages/web/src/types/`
3. Create hook if needed in `packages/web/src/hooks/`
4. Write tests in `packages/web/src/__tests__/`

### Creating a Database Migration
```bash
cd packages/api
alembic revision --autogenerate -m "description"
alembic upgrade head
```

---

## Links to Detailed Docs

| Topic | Document |
|-------|----------|
| Full Data Model | `/docs/02_DATA_MODEL.md` |
| Process Catalogue | `/docs/components/C2_PROCESS_CATALOGUE.md` |
| RIADA System | `/docs/components/C3_QUALITY_LOGS.md` |
| UI Design System | `/docs/ui/UI_DESIGN_SYSTEM.md` |
| Process Canvas | `/docs/ui/UI_PROCESS_CANVAS.md` |
| LLM Integration | `/docs/features/F2_LLM_INTEGRATION.md` |

---

*Context Version: 1.0 | Last Updated: January 2026*
