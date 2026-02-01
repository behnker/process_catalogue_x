#!/bin/bash
# create_project_structure.sh
# Creates the complete folder structure for the Process Catalogue project

set -e

PROJECT_NAME="${1:-process-catalogue}"

echo "Creating project structure for: $PROJECT_NAME"
echo "=================================================="

# Create root directory
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# ============================================
# .claude/ - Claude Code Configuration
# ============================================
echo "Creating .claude/ directory..."
mkdir -p .claude/prompts

cat > .claude/context.md << 'EOF'
# Process Catalogue - Claude Code Context
# See templates/.claude/context.md for full content
# Copy the content from there to here
EOF

cat > .claude/coding-standards.md << 'EOF'
# Coding Standards

## TypeScript
- Use strict mode
- Prefer interfaces over types for objects
- Use enums for fixed sets of values
- Always define return types

## React
- Functional components only
- Use hooks for state and side effects
- Prefer composition over inheritance
- Co-locate tests with components

## Python
- Follow PEP 8
- Use type hints everywhere
- Prefer async/await for I/O
- Use dependency injection

## Git
- Conventional commits (feat:, fix:, docs:, etc.)
- Feature branches from main
- Squash merge to main
EOF

cat > .claude/prompts/create-component.md << 'EOF'
# Prompt: Create React Component

Read the relevant requirement doc and create a React component.

## Template
```tsx
import { useState } from 'react';
import { cn } from '@/lib/utils';

interface {ComponentName}Props {
  // Define props
}

export function {ComponentName}({ ...props }: {ComponentName}Props) {
  return (
    <div className="">
      {/* Implementation */}
    </div>
  );
}
```

## Checklist
- [ ] TypeScript types defined
- [ ] Props documented
- [ ] Tailwind for styling
- [ ] Accessible (ARIA labels)
- [ ] Tests written
EOF

cat > .claude/prompts/create-api-endpoint.md << 'EOF'
# Prompt: Create API Endpoint

## Steps
1. Create/update model in models/
2. Create schema in schemas/
3. Create repository in repositories/
4. Create endpoint in api/v1/endpoints/
5. Register in router.py
6. Write tests

## Template
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.{resource} import {Resource}Create, {Resource}Response
from app.repositories.{resource} import {Resource}Repository

router = APIRouter()

@router.get("/", response_model=list[{Resource}Response])
async def list_{resources}(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = {Resource}Repository(db)
    return repo.list_by_organization(current_user.organization_id)
```
EOF

# ============================================
# docs/ - Requirements & Specifications
# ============================================
echo "Creating docs/ directory..."
mkdir -p docs/{components,features,ui,infrastructure,reference}

# Create placeholder docs
cat > docs/00_PROJECT_OVERVIEW.md << 'EOF'
# Process Catalogue - Project Overview

## Purpose
[Extract from Blueprint.md Section 1-3]

## Scope
[Define what's in and out of scope]

## Success Criteria
[Define how we measure success]
EOF

cat > docs/01_ARCHITECTURE.md << 'EOF'
# Process Catalogue - Technical Architecture

## Overview
[Extract from Blueprint.md Section 7-8]

## Tech Stack
[List all technologies]

## Deployment
[Describe deployment architecture]
EOF

cat > docs/02_DATA_MODEL.md << 'EOF'
# Process Catalogue - Data Model

## Overview
[Extract from Blueprint.md Section 9.6]

## Entity Relationship Diagram
[Include ERD]

## Table Definitions
[List all tables with columns]
EOF

cat > docs/03_API_SPECIFICATION.md << 'EOF'
# Process Catalogue - API Specification

## Overview
All APIs follow RESTful conventions and are versioned under /api/v1/

## Authentication
Bearer token in Authorization header

## Endpoints
[List all endpoints by resource]
EOF

# Component docs
for comp in C1_BUSINESS_MODEL C2_PROCESS_CATALOGUE C3_QUALITY_LOGS C4_OPERATING_MODEL C5_PORTFOLIO C6_CHANGE_ADOPTION C7_SURVEYS; do
  cat > "docs/components/${comp}.md" << EOF
# ${comp//_/ }

## Purpose
[Extract from Blueprint.md]

## Requirements
[List requirements]

## Data Model
[Relevant tables]

## API Endpoints
[List endpoints]

## UI Components
[List components needed]
EOF
done

# Feature docs
for feat in F1_PROMPT_LIBRARY F2_LLM_INTEGRATION F3_HEATMAPS_OVERLAYS F4_AGENTIC_OPPORTUNITIES F5_REPORTING; do
  cat > "docs/features/${feat}.md" << EOF
# ${feat//_/ }

## Purpose
[Extract from Blueprint.md]

## Requirements
[List requirements]

## Implementation
[Implementation details]
EOF
done

# UI docs
for ui in UI_DESIGN_SYSTEM UI_PROCESS_CANVAS UI_NAVIGATION UI_SCREENS; do
  cat > "docs/ui/${ui}.md" << EOF
# ${ui//_/ }

## Overview
[Extract from Blueprint.md Section 10]

## Specifications
[Detailed specs]
EOF
done

# Infrastructure docs
for infra in INFRA_GLOBAL INFRA_CHINA INFRA_SECURITY; do
  cat > "docs/infrastructure/${infra}.md" << EOF
# ${infra//_/ }

## Overview
[Extract from Blueprint.md]

## Configuration
[Configuration details]

## Deployment
[Deployment steps]
EOF
done

# Reference docs
cat > docs/reference/GLOSSARY.md << 'EOF'
# Glossary

| Term | Definition |
|------|------------|
| AFI | AI Fluency Index |
| RIADA | Risk, Issue, Action, Dependency, Assumption |
| RACI | Responsible, Accountable, Consulted, Informed |
| RLS | Row-Level Security |
| WSVF | Weighted Shortest Value First |
EOF

cat > docs/reference/PERSONAS.md << 'EOF'
# User Personas

## 1. Executive (CEO, COO)
- Views dashboards and summaries
- Tracks strategic initiatives

## 2. Process Owner
- Manages process definitions
- Reviews RIADA items

[Add remaining personas]
EOF

cat > docs/reference/NFR.md << 'EOF'
# Non-Functional Requirements

## Performance
- Page load < 2s
- API response < 500ms

## Scalability
- Support 100+ concurrent users
- Handle 10,000+ processes

## Availability
- 99.9% uptime

## Security
- SOC 2 compliance
- Data encryption at rest and in transit
EOF

# ============================================
# packages/web/ - Next.js Frontend
# ============================================
echo "Creating packages/web/ directory..."
mkdir -p packages/web/src/{app,components,hooks,lib,stores,types,styles}
mkdir -p packages/web/src/app/\(auth\)/{login,register}
mkdir -p packages/web/src/app/\(dashboard\)/{processes,business-model,quality-logs,operating-model,portfolio,change-adoption,surveys,prompts,reports,settings}
mkdir -p packages/web/src/components/{ui,layout,process,canvas,riada,charts,forms}
mkdir -p packages/web/public

cat > packages/web/package.json << 'EOF'
{
  "name": "@process-catalogue/web",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "vitest"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@tanstack/react-query": "^5.0.0",
    "zustand": "^4.4.0",
    "recharts": "^2.10.0",
    "lucide-react": "^0.300.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "vitest": "^1.0.0",
    "@testing-library/react": "^14.0.0"
  }
}
EOF

cat > packages/web/tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
EOF

cat > packages/web/tailwind.config.ts << 'EOF'
import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ["class"],
  content: [
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2563EB',
        secondary: '#64748B',
        success: '#22C55E',
        warning: '#F59E0B',
        danger: '#EF4444',
      },
    },
  },
  plugins: [],
}
export default config
EOF

cat > packages/web/next.config.js << 'EOF'
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

module.exports = nextConfig
EOF

# Create placeholder components
cat > packages/web/src/app/layout.tsx << 'EOF'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Process Catalogue',
  description: 'Design and manage your operating model',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
EOF

cat > packages/web/src/app/page.tsx << 'EOF'
export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold">Process Catalogue</h1>
      <p className="mt-4 text-gray-600">Coming soon...</p>
    </main>
  )
}
EOF

cat > packages/web/src/app/globals.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF

# ============================================
# packages/api/ - FastAPI Backend
# ============================================
echo "Creating packages/api/ directory..."
mkdir -p packages/api/src/{api/v1/endpoints,config,models,schemas,services,repositories,utils}
mkdir -p packages/api/{tests,alembic/versions}

cat > packages/api/requirements.txt << 'EOF'
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.0
alembic>=1.13.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
httpx>=0.26.0
pytest>=7.4.0
pytest-asyncio>=0.23.0
EOF

cat > packages/api/src/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.config.settings import settings

app = FastAPI(
    title="Process Catalogue API",
    description="API for Process Catalogue platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
EOF

cat > packages/api/src/config/settings.py << 'EOF'
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://localhost/process_catalogue"
    SECRET_KEY: str = "change-me-in-production"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"


settings = Settings()
EOF

cat > packages/api/src/api/v1/router.py << 'EOF'
from fastapi import APIRouter

from app.api.v1.endpoints import processes, riada, portfolio

api_router = APIRouter()

api_router.include_router(processes.router, prefix="/processes", tags=["processes"])
api_router.include_router(riada.router, prefix="/riada", tags=["riada"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
EOF

cat > packages/api/src/api/v1/endpoints/processes.py << 'EOF'
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_processes():
    """List all processes."""
    return {"items": [], "total": 0}


@router.get("/{process_id}")
async def get_process(process_id: str):
    """Get a single process by ID."""
    return {"id": process_id}
EOF

cat > packages/api/src/api/v1/endpoints/riada.py << 'EOF'
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_riada_items():
    """List all RIADA items."""
    return {"items": [], "total": 0}
EOF

cat > packages/api/src/api/v1/endpoints/portfolio.py << 'EOF'
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_portfolios():
    """List all portfolios."""
    return {"items": [], "total": 0}
EOF

cat > packages/api/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# ============================================
# packages/shared/ - Shared Types
# ============================================
echo "Creating packages/shared/ directory..."
mkdir -p packages/shared/{types,constants}

cat > packages/shared/types/process.ts << 'EOF'
export type ProcessLevel = 'L0' | 'L1' | 'L2' | 'L3' | 'L4' | 'L5';
export type ProcessType = 'primary' | 'secondary';
export type AgenticPotential = 'none' | 'low' | 'medium' | 'high';
export type AutomationLevel = 'manual' | 'assisted' | 'semi_automated' | 'fully_automated';
export type RagStatus = 'green' | 'amber' | 'red';

export interface Process {
  id: string;
  organizationId: string;
  parentId: string | null;
  processType: ProcessType;
  level: ProcessLevel;
  code: string;
  name: string;
  description?: string;
  agenticPotential?: AgenticPotential;
  currentAutomationLevel?: AutomationLevel;
  targetAutomationLevel?: AutomationLevel;
  ragPeople?: RagStatus;
  ragProcess?: RagStatus;
  ragSystem?: RagStatus;
  ragData?: RagStatus;
  createdAt: string;
  updatedAt: string;
}
EOF

cat > packages/shared/constants/index.ts << 'EOF'
export const PROCESS_LEVELS = ['L0', 'L1', 'L2', 'L3', 'L4', 'L5'] as const;

export const RIADA_TYPES = ['risk', 'issue', 'action', 'dependency', 'assumption'] as const;

export const RIADA_CATEGORIES = ['people', 'process', 'system', 'data'] as const;

export const SEVERITY_LEVELS = ['critical', 'high', 'medium', 'low'] as const;
EOF

# ============================================
# infrastructure/ - IaC
# ============================================
echo "Creating infrastructure/ directory..."
mkdir -p infrastructure/{terraform/{global,china},docker}

cat > infrastructure/docker/docker-compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: process_catalogue
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: ../../packages/api
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db/process_catalogue
    depends_on:
      - db

volumes:
  postgres_data:
EOF

# ============================================
# scripts/
# ============================================
echo "Creating scripts/ directory..."
mkdir -p scripts

cat > scripts/setup.sh << 'EOF'
#!/bin/bash
# Initial project setup

echo "Installing dependencies..."
pnpm install

echo "Setting up database..."
cd packages/api
alembic upgrade head
cd ../..

echo "Setup complete!"
EOF

cat > scripts/seed-data.sh << 'EOF'
#!/bin/bash
# Seed the database with sample data

echo "Seeding database..."
cd packages/api
python -m app.scripts.seed
cd ../..

echo "Seeding complete!"
EOF

chmod +x scripts/*.sh

# ============================================
# Root files
# ============================================
echo "Creating root configuration files..."

cat > package.json << 'EOF'
{
  "name": "process-catalogue",
  "private": true,
  "scripts": {
    "dev": "turbo dev",
    "build": "turbo build",
    "lint": "turbo lint",
    "test": "turbo test",
    "clean": "turbo clean"
  },
  "devDependencies": {
    "turbo": "^1.11.0"
  },
  "packageManager": "pnpm@8.14.0"
}
EOF

cat > turbo.json << 'EOF'
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {},
    "test": {}
  }
}
EOF

cat > pnpm-workspace.yaml << 'EOF'
packages:
  - 'packages/*'
EOF

cat > .gitignore << 'EOF'
# Dependencies
node_modules/
.pnpm-store/

# Build outputs
.next/
dist/
.turbo/

# Environment
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
.venv/
venv/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
coverage/
.pytest_cache/

# Misc
*.log
EOF

cat > README.md << 'EOF'
# Process Catalogue

A multi-tenant SaaS platform for designing business and operating models.

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- pnpm 8+
- Docker (for local database)

### Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pnpm install
   ```
3. Start the database:
   ```bash
   docker-compose -f infrastructure/docker/docker-compose.yml up -d db
   ```
4. Run migrations:
   ```bash
   cd packages/api
   alembic upgrade head
   ```
5. Start development servers:
   ```bash
   pnpm dev
   ```

## Project Structure

```
process-catalogue/
├── .claude/          # Claude Code configuration
├── docs/             # Requirements & specifications
├── packages/
│   ├── web/          # Next.js frontend
│   ├── api/          # FastAPI backend
│   └── shared/       # Shared types
├── infrastructure/   # Docker, Terraform
└── scripts/          # Build scripts
```

## Documentation

See `/docs` for detailed requirements and specifications.
EOF

# ============================================
# GitHub Actions
# ============================================
echo "Creating .github/ directory..."
mkdir -p .github/workflows

cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: pnpm/action-setup@v2
        with:
          version: 8
          
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'pnpm'
          
      - run: pnpm install
      - run: pnpm lint
      - run: pnpm test
      - run: pnpm build
EOF

# ============================================
# Done
# ============================================
echo ""
echo "=================================================="
echo "Project structure created successfully!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. cd $PROJECT_NAME"
echo "2. Copy content from Blueprint.md into docs/ files"
echo "3. Copy .claude/context.md from templates"
echo "4. Run: pnpm install"
echo "5. Run: docker-compose -f infrastructure/docker/docker-compose.yml up -d"
echo "6. Start developing!"
echo ""
echo "Directory structure:"
find . -type d | head -40
