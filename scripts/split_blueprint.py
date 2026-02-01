#!/usr/bin/env python3
"""
Blueprint Splitter Script
Splits the monolithic Blueprint.md into focused requirement documents.

Usage:
    python split_blueprint.py --input Blueprint.md --output docs/

This script parses the Blueprint.md file and extracts sections into
separate, focused documents suitable for Claude Code consumption.
"""

import os
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

# Define the mapping of Blueprint sections to output files
SECTION_MAPPING = {
    # Project Overview - extract key summary sections
    "00_PROJECT_OVERVIEW.md": {
        "sections": [
            ("## 1. Executive Summary", "## 2."),
            ("## 2. Business Context", "## 3."),
            ("## 3. Solution Overview", "## 4."),
        ],
        "header": """# Process Catalogue - Project Overview

## Purpose
Design business and operating models with clear agentic opportunities identified, 
reported, projects mobilised and delivery tracked through to adoption with survey 
and assessment support for the key inputs to process, adoption, capability and readiness.

---

"""
    },
    
    # Architecture
    "01_ARCHITECTURE.md": {
        "sections": [
            ("## 7. Technical Architecture", "## 8."),
            ("## 8. Deployment Architecture", "## 9."),
        ],
        "header": """# Process Catalogue - Technical Architecture

## Overview
This document defines the technical and deployment architecture for both 
Global (Vercel/Supabase) and China (Alibaba Cloud) deployments.

---

"""
    },
    
    # Data Model
    "02_DATA_MODEL.md": {
        "sections": [
            ("### 9.6 Data Model", "### 9.7"),
        ],
        "header": """# Process Catalogue - Data Model

## Overview
Complete data model specification with 45+ tables across 14 domains.

---

"""
    },
    
    # Component 1: Business Model
    "components/C1_BUSINESS_MODEL.md": {
        "sections": [
            ("### 4.1 Component 1: Business Model", "### 4.2"),
        ],
        "header": """# Component 1: Business Model

## Purpose
Define and track what is impacted in the business model. Captures Business Model 
Canvas components with their specific values and enables Issues, Risks, and SWOT 
analysis at both group and individual entry levels.

---

"""
    },
    
    # Component 2: Process Catalogue
    "components/C2_PROCESS_CATALOGUE.md": {
        "sections": [
            ("### 4.2 Component 2: Process Catalogue", "### 4.3"),
        ],
        "header": """# Component 2: Process Catalogue

## Purpose
Define and track what is impacted in operations through a 6-level process hierarchy 
with full traceability up and down. Supports both Primary (core value chain) and 
Secondary (support functions) process hierarchies.

---

"""
    },
    
    # Component 3: Quality Logs (RIADA)
    "components/C3_QUALITY_LOGS.md": {
        "sections": [
            ("### 4.3 Component 3: Operational Quality Logs", "### 4.4"),
        ],
        "header": """# Component 3: Quality Logs (RIADA)

## Purpose
Track the operational environment through RIADA logs (Risks, Issues, Actions, 
Dependencies, Assumptions) at any level of the hierarchy with severity classification.

---

"""
    },
    
    # Component 4: Operating Model
    "components/C4_OPERATING_MODEL.md": {
        "sections": [
            ("### 4.4 Component 4: Operating Model Design", "### 4.5"),
        ],
        "header": """# Component 4: Operating Model Design

## Purpose
Document current and future state operating models with 10 components: RACI, KPIs, 
Policies, Governance, Systems, Agents, Security, Data, Timing, and Prompt Library.

---

"""
    },
    
    # Component 5: Portfolio
    "components/C5_PORTFOLIO.md": {
        "sections": [
            ("### 4.5 Component 5: Portfolio Response", "### 4.6"),
        ],
        "header": """# Component 5: Portfolio Response

## Purpose
Track the portfolio of projects and programmes mobilised to address business model 
and process changes, with full hierarchy from Strategic Pillar to Work Package.

---

"""
    },
    
    # Component 6: Change & Adoption
    "components/C6_CHANGE_ADOPTION.md": {
        "sections": [
            ("### 4.6 Component 6: Change & Adoption", "### 4.7"),
        ],
        "header": """# Component 6: Change & Adoption Monitoring

## Purpose
Monitor whether changes delivered by projects are being adopted through lead 
indicators, lag indicators, KPI tracking, and benefits realization.

---

"""
    },
    
    # Component 7: Surveys
    "components/C7_SURVEYS.md": {
        "sections": [
            ("### 4.7 Component 7: Surveys", "## 5."),
        ],
        "header": """# Component 7: Surveys

## Purpose
Assess capability and readiness through four survey types: AI Fluency (AFI), 
Operating Model (SPRD), Change Readiness (ADKAR), and Adoption Evidence.

---

"""
    },
    
    # Feature: Prompt Library
    "features/F1_PROMPT_LIBRARY.md": {
        "sections": [
            ("#### 4.4.6 Prompt Library", "#### 4.4.7"),
        ],
        "header": """# Feature: Prompt Library

## Purpose
A comprehensive library of AI prompts that can be executed directly within the 
application, with results stored, personalized by context, and integrated with 
process data.

---

"""
    },
    
    # Feature: LLM Integration
    "features/F2_LLM_INTEGRATION.md": {
        "sections": [
            ("### 6.3 LLM Integration", "### 6.4"),
        ],
        "header": """# Feature: LLM Integration

## Purpose
Connect to Large Language Models (LLMs) to execute prompts against catalogue data, 
run prompts from the Prompt Library, and optionally save or discard responses.

---

"""
    },
    
    # Feature: Heatmaps & Overlays
    "features/F3_HEATMAPS_OVERLAYS.md": {
        "sections": [
            ("### 10.6 Heatmap & Overlay System", "### 10.7"),
        ],
        "header": """# Feature: Heatmaps & Overlays

## Purpose
Visual overlay system for the Process Canvas that enables color-coded views 
based on different dimensions (RIADA, Projects, Systems, Roles, etc.).

---

"""
    },
    
    # Feature: Agentic Opportunities
    "features/F4_AGENTIC_OPPORTUNITIES.md": {
        "sections": [
            ("#### 4.4.5 Agents Component", "#### 4.4.6"),
            ("##### 4.2.1.5 Agentic Opportunity Fields", "##### 4.2.1.6"),
        ],
        "header": """# Feature: Agentic Opportunities

## Purpose
Explicitly track automation and AI opportunities at the process and business 
model level, with agent catalogue, automation levels, and opportunity register.

---

"""
    },
    
    # Feature: Reporting
    "features/F5_REPORTING.md": {
        "sections": [
            ("### 10.4 Dashboards", "### 10.5"),
            ("### 10.5 Reports", "### 10.6"),
        ],
        "header": """# Feature: Reporting & Dashboards

## Purpose
Pre-built dashboards and reports for executives, RIADA management, portfolio 
tracking, and survey results, plus custom report builder.

---

"""
    },
    
    # UI: Design System
    "ui/UI_DESIGN_SYSTEM.md": {
        "sections": [
            ("### 10.8 Design System", "### 10.9"),
        ],
        "header": """# UI Specification: Design System

## Purpose
Define the visual language for the application including colors, typography, 
spacing, and component library.

---

"""
    },
    
    # UI: Process Canvas
    "ui/UI_PROCESS_CANVAS.md": {
        "sections": [
            ("### 10.1 Process Canvas", "### 10.2"),
            ("### 10.2 Alternative Views", "### 10.3"),
            ("### 10.3 Process Detail View", "### 10.4"),
        ],
        "header": """# UI Specification: Process Canvas

## Purpose
Define the swimlane-based Process Canvas visualization with L0 horizontal, 
L1 horizontal, L2 vertical columns, and L3/L4/L5 as nested expandable menus.

---

"""
    },
    
    # UI: Navigation
    "ui/UI_NAVIGATION.md": {
        "sections": [
            ("### 10.7 Navigation Structure", "### 10.8"),
        ],
        "header": """# UI Specification: Navigation

## Purpose
Define the main navigation structure including sidebar, contextual navigation, 
and breadcrumbs.

---

"""
    },
    
    # Infrastructure: Global
    "infrastructure/INFRA_GLOBAL.md": {
        "sections": [
            ("### 8.1 Global Deployment", "### 8.2"),
        ],
        "header": """# Infrastructure: Global Deployment

## Purpose
Define the global SaaS deployment on Vercel (frontend), Supabase (database, auth), 
and Cloudflare R2 (storage).

---

"""
    },
    
    # Infrastructure: China
    "infrastructure/INFRA_CHINA.md": {
        "sections": [
            ("### 8.2 China Deployment", "### 8.3"),
        ],
        "header": """# Infrastructure: China Deployment

## Purpose
Define the China single-tenant deployment on Alibaba Cloud (ECS, ApsaraDB, OSS).

---

"""
    },
    
    # Infrastructure: Security
    "infrastructure/INFRA_SECURITY.md": {
        "sections": [
            ("### 9.5 Security Requirements", "### 9.6"),
        ],
        "header": """# Infrastructure: Security Requirements

## Purpose
Define security requirements including authentication, authorization, 
data protection, and compliance.

---

"""
    },
    
    # Reference: Personas
    "reference/PERSONAS.md": {
        "sections": [
            ("## 5. User Personas", "## 6."),
        ],
        "header": """# Reference: User Personas

## Purpose
Define the 14 user personas who will interact with the system, their roles, 
and primary use cases.

---

"""
    },
    
    # Reference: NFR
    "reference/NFR.md": {
        "sections": [
            ("### 9.1 Performance", "### 9.2"),
            ("### 9.2 Scalability", "### 9.3"),
            ("### 9.3 Availability", "### 9.4"),
            ("### 9.4 Compliance", "### 9.5"),
        ],
        "header": """# Reference: Non-Functional Requirements

## Purpose
Define performance, scalability, availability, and compliance requirements.

---

"""
    },
}


def read_blueprint(filepath: str) -> str:
    """Read the Blueprint.md file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def extract_section(content: str, start_marker: str, end_marker: str) -> str:
    """Extract a section from content between start and end markers."""
    # Find start position
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print(f"  WARNING: Start marker not found: {start_marker}")
        return ""
    
    # Find end position
    end_idx = content.find(end_marker, start_idx + len(start_marker))
    if end_idx == -1:
        # If end marker not found, go to end of content
        end_idx = len(content)
    
    return content[start_idx:end_idx].strip()


def create_document(output_path: str, header: str, sections: List[str]) -> None:
    """Create a document with header and extracted sections."""
    content = header
    
    for section in sections:
        if section:
            content += section + "\n\n---\n\n"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Count lines
    line_count = content.count('\n')
    print(f"  Created: {output_path} ({line_count} lines)")


def split_blueprint(input_path: str, output_dir: str) -> None:
    """Split the Blueprint into multiple focused documents."""
    print(f"Reading Blueprint from: {input_path}")
    content = read_blueprint(input_path)
    print(f"Blueprint size: {len(content):,} characters, {content.count(chr(10)):,} lines")
    print()
    
    print("Splitting into focused documents...")
    print("-" * 60)
    
    for output_file, config in SECTION_MAPPING.items():
        output_path = os.path.join(output_dir, output_file)
        
        # Extract all sections for this document
        extracted_sections = []
        for start_marker, end_marker in config["sections"]:
            section = extract_section(content, start_marker, end_marker)
            if section:
                extracted_sections.append(section)
        
        # Create the document
        create_document(output_path, config["header"], extracted_sections)
    
    print("-" * 60)
    print(f"\nDone! Created {len(SECTION_MAPPING)} documents in {output_dir}/")
    print("\nNext steps:")
    print("1. Review each document for completeness")
    print("2. Add any missing content manually")
    print("3. Create the .claude/context.md file")
    print("4. Initialize the repository structure")


def create_glossary(output_dir: str) -> None:
    """Create a glossary document."""
    glossary = """# Reference: Glossary

## Purpose
Define key terms and abbreviations used throughout the project.

---

## Terms

| Term | Definition |
|------|------------|
| **AFI** | AI Fluency Index - score (0-100) measuring AI capability |
| **ADKAR** | Awareness, Desire, Knowledge, Ability, Reinforcement - change model |
| **Canvas** | Business Model Canvas - strategic planning template |
| **L0-L5** | Process hierarchy levels (Value Stream to Work Instruction) |
| **PPSD** | People, Process, System, Data - RIADA categories |
| **RAG** | Red, Amber, Green - status indicators |
| **RACI** | Responsible, Accountable, Consulted, Informed - responsibility matrix |
| **RIADA** | Risk, Issue, Action, Dependency, Assumption - quality log types |
| **RLS** | Row-Level Security - database isolation mechanism |
| **SOM** | Standard Operating Model - documented operating model |
| **SPRD** | System, People, Process (Readiness), Data - survey dimensions |
| **WSVF** | Weighted Shortest Value First - prioritization method |

## Abbreviations

| Abbrev. | Meaning |
|---------|---------|
| **API** | Application Programming Interface |
| **BM** | Business Model |
| **CA** | Change & Adoption |
| **CRUD** | Create, Read, Update, Delete |
| **FK** | Foreign Key |
| **LLM** | Large Language Model |
| **OM** | Operating Model |
| **PC** | Process Catalogue |
| **PK** | Primary Key |
| **PR** | Portfolio Response |
| **QL** | Quality Logs |
| **RPA** | Robotic Process Automation |
| **UUID** | Universally Unique Identifier |

---

*Last Updated: January 2026*
"""
    output_path = os.path.join(output_dir, "reference/GLOSSARY.md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(glossary)
    print(f"  Created: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Split Blueprint.md into focused documents')
    parser.add_argument('--input', '-i', default='Blueprint.md', help='Input Blueprint file')
    parser.add_argument('--output', '-o', default='docs', help='Output directory')
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"ERROR: Input file not found: {args.input}")
        print("Make sure Blueprint.md is in the current directory.")
        return 1
    
    split_blueprint(args.input, args.output)
    create_glossary(args.output)
    
    return 0


if __name__ == "__main__":
    exit(main())
