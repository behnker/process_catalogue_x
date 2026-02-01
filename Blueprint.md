# Process Catalogue - Product Specification Blueprint

## Document Information
- **Version:** 1.9
- **Last Updated:** January 31, 2026
- **Status:** Requirements Complete - UI Specification Added

---

## 1. Executive Summary

The Process Catalogue is a strategic business operations platform that enables organizations to translate business strategy into actionable operational reality. The platform connects seven integrated feature sets through a central **Process Spine**, providing end-to-end visibility from strategic intent through to measurable adoption outcomes.

The system answers the fundamental question: **"How does our strategy translate into operational change, and how do we know it's working?"**

---

## 2. Product Vision

### 2.1 Problem Statement
Organizations struggle to:
- Connect business strategy to operational execution
- Understand the full impact of strategic decisions across business dimensions
- Track dependencies between business model changes and operational requirements
- Monitor whether strategic changes are being adopted and delivering results
- Roll up impact analysis across multiple dimensions (sponsors, systems, processes, roles, markets, categories)

### 2.2 Target Users
[Awaiting requirements - likely includes: Strategy teams, Operations leaders, Program/Portfolio managers, Change managers, Business analysts, Executive sponsors]

### 2.3 Value Proposition
A unified platform that provides:
- Strategic-to-operational traceability
- Multi-dimensional impact analysis
- Integrated change governance
- Adoption monitoring and metrics tracking
- Single source of truth for business operations architecture

---

## 3. Core Architecture

### 3.1 The Process Spine
The **Process Spine** is the central integration layer that connects all seven feature components. It serves as the backbone through which all components interact, enabling:
- Cross-component traceability
- Multi-dimensional roll-up and drill-down
- Impact analysis across the entire value chain
- Consistent data model and relationships

### 3.2 Seven Feature Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           STRATEGIC LAYER                                    │
│  ┌─────────────────────┐                      ┌─────────────────────────┐   │
│  │  1. BUSINESS MODEL  │                      │  5. PORTFOLIO RESPONSE  │   │
│  │  Markets, Channels, │                      │  Projects, Governance,  │   │
│  │  Partners, Value    │                      │  Delivery               │   │
│  │  Proposition        │                      │                         │   │
│  └──────────┬──────────┘                      └────────────┬────────────┘   │
│             │                                              │                 │
│             ▼                                              ▼                 │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         PROCESS SPINE                                 │   │
│  │            (Central Integration & Traceability Layer)                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│             │                    │                         │                 │
│             ▼                    ▼                         ▼                 │
│  ┌─────────────────┐  ┌─────────────────────┐  ┌─────────────────────────┐  │
│  │ 2. PROCESS      │  │ 3. OPERATIONAL      │  │ 4. OPERATING MODEL      │  │
│  │    CATALOGUE    │  │    QUALITY LOGS     │  │    DESIGN               │  │
│  │ Roles, Processes│  │ Issues, Risks,      │  │ Future State            │  │
│  │ KPIs, Systems   │  │ Assumptions,        │  │ Operations              │  │
│  │                 │  │ Dependencies        │  │                         │  │
│  └─────────────────┘  └─────────────────────┘  └─────────────────────────┘  │
│                           OPERATIONAL LAYER                                  │
│                                                                              │
│  ┌──────────────────────────────┐  ┌────────────────────────────────────┐   │
│  │  6. CHANGE & ADOPTION        │  │  7. SURVEYS                        │   │
│  │  Lead Indicators, Adoption   │  │  AI Fluency, Operating Model,      │   │
│  │  Metrics, Benefits Tracking  │  │  Change Readiness, Adoption        │   │
│  └──────────────────────────────┘  └────────────────────────────────────┘   │
│                           MEASUREMENT LAYER                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Component Summary

| # | Component | Strategic Question Answered | Key Entities |
|---|-----------|----------------------------|--------------|
| 1 | **Business Model** | What is impacted in the business model? | Canvas Components (Markets, Channels, Partners, Clients, Categories, etc.), SWOT, RIADA at BM level, **Agentic Potential** |
| 2 | **Process Catalogue** | What is impacted in operations? | 6-Level Hierarchy (L0-L5), Resource Allocation (Sponsor→SME→RACI), Project Resources, **Agentic Opportunity Fields** |
| 3 | **Operational Quality Logs** | What is the operational risk environment? | **RIADA** (Risk, Issue, Action, Dependency, Assumption) × (People/Process/System/Data) × (Critical/High/Medium/Low) |
| 4 | **Operating Model Design** | What is current & future state? | RACI, KPIs, Policies, Governance, Systems, **Agent Catalogue**, Security, Data, Timing, Prompt Library, **Agentic Opportunity Register** |
| 5 | **Portfolio Response** | What projects deliver change? | Strategic Pillars, Programmes, Projects, Workstreams, Work Packages + **RIADA at every level** |
| 6 | **Change & Adoption Monitoring** | Are changes being adopted? | Lead Indicators, Lag Indicators, KPI Tracking, Benefits Realization |
| 7 | **Surveys** | What is our capability & readiness? | AI Fluency (AFI), Operating Model (SPRD), Change Readiness (ADKAR), Adoption Evidence |

### 3.4 Multi-Dimensional Roll-Up Capability

The platform must support impact analysis and roll-up across multiple dimensions:

| Dimension | Example Query |
|-----------|---------------|
| **Sponsor** | "What is the total impact to Sarah's portfolio?" |
| **System** | "What processes and projects are affected by the ERP upgrade?" |
| **Process** | "What risks and changes are associated with Order-to-Cash?" |
| **Role** | "What training and changes affect Customer Service Representatives?" |
| **Market** | "What is changing in our APAC operations?" |
| **Category** | "What is the status of all Digital Transformation initiatives?" |

---

## 4. Feature Components - Detailed Requirements

### 4.1 Component 1: Business Model

**Purpose:** Define and track what is impacted in the business model. Captures Business Model Canvas components with their specific values and enables Issues, Risks, and SWOT analysis at both group and individual entry levels.

#### 4.1.1 Business Model Canvas Components

The Business Model follows the Business Model Canvas framework with hierarchical values:

| Canvas Component | Description | Example Values (Surity) |
|-----------------|-------------|------------------------|
| **Customer Segments** | Who we serve | DIY Retailers |
| **Clients** | Specific customers | Selco, Bunnings, Maxeda |
| **Value Propositions** | What value we deliver | Sourcing expertise, Quality assurance, Compliance management |
| **Channels** | How we reach customers | Agent model |
| **Customer Relationships** | How we maintain relationships | Account management, Partnership |
| **Revenue Streams** | How we earn money | Agency margin (3-8%) |
| **Key Resources** | What we need to operate | Sourcing network, QA expertise, Vendor relationships |
| **Key Activities** | What we do | Source, Develop, Execute, Support |
| **Key Partners** | Who helps us | 3PL providers, Testing labs, Audit firms |
| **Key Suppliers** | Who supplies products | Vendor base (China, Vietnam) |
| **Cost Structure** | What it costs | Personnel, Travel, Testing, IT |
| **Trading Markets** | Where we sell | UK, Benelux, Australia |
| **Sourcing Markets** | Where we source | China (80-90%), Vietnam (10-20%) |
| **Product Categories** | What we source | Technical, Showroom, Seasonal, Home |

#### 4.1.2 Hierarchical Structure

```
Business Model (Top Level) - e.g., "Surity Business Model"
├── Canvas Component (Group Level) - e.g., "Clients"
│   ├── Entry (Individual Level) - e.g., "Bunnings"
│   ├── Entry - e.g., "Selco"
│   └── Entry - e.g., "Maxeda"
├── Canvas Component - e.g., "Trading Markets"
│   ├── Entry - e.g., "United Kingdom"
│   ├── Entry - e.g., "Benelux"
│   └── Entry - e.g., "Australia"
└── ... (other components)
```

#### 4.1.3 Issues, Risks & SWOT Attachment

Issues, Risks, and SWOT can be captured at:
- **Business Model Level** (highest aggregation)
- **Canvas Component Level** (e.g., all Clients)
- **Entry Level** (e.g., specific client like Bunnings)

**Aggregation Requirement:** All entries roll up automatically, enabling reports at any level showing aggregated Issues, Risks, SWOT from all child levels.

#### 4.1.4 Agentic Opportunity Fields (Business Model Level)

Each Canvas Entry (e.g., a specific market, client, or channel) can include agentic opportunity assessment:

| Field | Type | Description |
|-------|------|-------------|
| **agentic_potential** | ENUM | Automation/AI potential for this BM area | `None` / `Low` / `Medium` / `High` |
| **agentic_opportunity_description** | TEXT | Description of automation opportunity |
| **current_digital_maturity** | ENUM | Current digital/automation state | `Traditional` / `Digitizing` / `Digital` / `AI-Enabled` |
| **target_digital_maturity** | ENUM | Target future state | Same as above |

**Examples:**

| Canvas Entry | Agentic Potential | Opportunity Description |
|--------------|-------------------|------------------------|
| Channel: Agent Model | High | AI-assisted vendor matching, automated quotation generation |
| Client: Bunnings | Medium | Automated order intake via EDI, AI demand forecasting |
| Market: China Sourcing | High | AI-powered supplier discovery, automated compliance checking |
| Category: Technical | Medium | Automated test result interpretation, AI quality prediction |

#### 4.1.5 Excel Tab Mapping

| Excel Tab | Maps to Business Model |
|-----------|----------------------|
| Business Model Mapping | Process-to-BM linkage |
| Business Model Reference | BM component taxonomy |

---

### 4.2 Component 2: Process Catalogue

**Purpose:** Define and track what is impacted in operations through a 6-level process hierarchy with full traceability up and down. Supports both **Primary** (core value chain) and **Secondary** (support functions) process hierarchies.

#### 4.2.1 Primary vs Secondary Processes

A key feature of Operating Model design and Value Chain Analysis is the distinction between Primary and Secondary processes.

##### 4.2.1.1 Process Classification

| Classification | Description | Characteristics |
|----------------|-------------|-----------------|
| **Primary** | Core value chain processes | Directly create and deliver value to customers |
| **Secondary** | Support function processes | Enable and support the execution of primary processes |

##### 4.2.1.2 Primary Process Hierarchy (Core Value Chain)

All Primary processes share a common hierarchy structure:

```
PRIMARY PROCESSES (Core Value Chain)
├── L0: SUPPORT
│   └── L1 → L2 → L3 → L4 → L5
├── L0: SOURCE
│   └── L1 → L2 → L3 → L4 → L5
├── L0: DEVELOP
│   └── L1 → L2 → L3 → L4 → L5
└── L0: EXECUTE
    └── L1 → L2 → L3 → L4 → L5
```

##### 4.2.1.3 Secondary Process Hierarchies (Support Functions)

Each Secondary process domain has its **own distinct hierarchy** (L0 → L5):

```
SECONDARY PROCESSES (Support Functions)
│
├── IT (Information Technology)
│   ├── L0: IT Services
│   │   ├── L1: Infrastructure Management
│   │   ├── L1: Application Development
│   │   ├── L1: IT Support & Service Desk
│   │   └── L1: Cybersecurity
│   └── (each L1 → L2 → L3 → L4 → L5)
│
├── HR (Human Resources)
│   ├── L0: People Management
│   │   ├── L1: Talent Acquisition
│   │   ├── L1: Learning & Development
│   │   ├── L1: Performance Management
│   │   └── L1: Employee Relations
│   └── (each L1 → L2 → L3 → L4 → L5)
│
├── Legal
│   ├── L0: Legal Services
│   │   ├── L1: Contract Management
│   │   ├── L1: Compliance & Regulatory
│   │   ├── L1: Intellectual Property
│   │   └── L1: Dispute Resolution
│   └── (each L1 → L2 → L3 → L4 → L5)
│
├── Treasury / Finance
│   ├── L0: Financial Management
│   │   ├── L1: Accounts Payable
│   │   ├── L1: Accounts Receivable
│   │   ├── L1: Financial Planning & Analysis
│   │   └── L1: Treasury Operations
│   └── (each L1 → L2 → L3 → L4 → L5)
│
└── Portfolio Delivery
    ├── L0: Portfolio Management
    │   ├── L1: Strategic Planning
    │   ├── L1: Programme Management
    │   ├── L1: Project Delivery
    │   └── L1: Change Management
    └── (each L1 → L2 → L3 → L4 → L5)
```

##### 4.2.1.4 Process Entity Classification

| Field | Description | Values |
|-------|-------------|--------|
| **Process Type** | Primary or Secondary classification | `Primary` / `Secondary` |
| **Process Domain** | Domain for Secondary processes | `IT` / `HR` / `Legal` / `Treasury` / `Portfolio Delivery` / (extensible) |
| **Hierarchy Root** | The L0 this process belongs to | Reference to L0 process |

##### 4.2.1.5 Agentic Opportunity Fields

Each process includes fields to explicitly identify and track automation/AI opportunities:

| Field | Type | Description | Values |
|-------|------|-------------|--------|
| **agentic_potential** | ENUM | Assessment of automation/AI potential | `None` / `Low` / `Medium` / `High` |
| **agentic_opportunity_description** | TEXT | Description of the automation opportunity | Free text describing what could be automated and how |
| **current_automation_level** | ENUM | Current state of automation | `Manual` / `Assisted` / `Semi-Automated` / `Fully-Automated` |
| **target_automation_level** | ENUM | Desired future state | `Manual` / `Assisted` / `Semi-Automated` / `Fully-Automated` |
| **automation_gap** | DERIVED | Gap between current and target | Calculated: target - current |
| **linked_agent_id** | FK | Current agent (if any) | Reference to Agent Catalogue |
| **target_agent_id** | FK | Planned future agent (if any) | Reference to Agent Catalogue |
| **agentic_assessment_date** | DATE | When last assessed | Date of assessment |
| **agentic_assessed_by** | FK | Who assessed | Reference to User |

**Automation Level Definitions:**

| Level | Definition | Examples |
|-------|------------|----------|
| **Manual** | Process is entirely human-executed with no automation | Paper forms, verbal approvals, manual data entry |
| **Assisted** | Technology assists but human drives the process | Templates, calculators, reference lookups |
| **Semi-Automated** | Automation handles routine cases; humans handle exceptions | RPA for standard orders, AI suggestions with human approval |
| **Fully-Automated** | End-to-end automation with human oversight only | Straight-through processing, AI agents with exception escalation |

**Agentic Potential Assessment Criteria:**

| Potential | Criteria |
|-----------|----------|
| **High** | Repetitive, rule-based, high volume, low exception rate, data is digital and structured |
| **Medium** | Some repetition, moderate complexity, medium volume, data partially structured |
| **Low** | Complex judgment required, low volume, high variability, unstructured data |
| **None** | Requires human creativity, relationship, physical presence, or regulatory prohibition |

##### 4.2.1.6 Cross-Query Capability

Users can query across both Primary and Secondary processes:

| Query Example | Result |
|---------------|--------|
| "Show me all projects" | All projects from Portfolio (Primary) + Portfolio Delivery (Secondary) |
| "Show me all L2 processes" | All L2 processes across Primary + all Secondary domains |
| "Show me all IT-related issues" | Issues attached to IT Secondary processes |
| "Show me all processes for UK market" | Primary processes filtered by UK + Secondary processes supporting UK |
| "Show me all processes owned by John" | Processes across Primary + Secondary where John is Process Owner |

##### 4.2.1.7 Filtering Options

| Filter | Options |
|--------|---------|
| **Process Type** | All / Primary Only / Secondary Only |
| **Secondary Domain** | All / IT / HR / Legal / Treasury / Portfolio Delivery |
| **Combined View** | Unified list across selected types/domains |

##### 4.2.1.8 Primary-Secondary Linkage

Secondary processes can be linked to the Primary processes they support:

```
Primary Process: L2 - Order Management
├── Supported by (Secondary):
│   ├── IT: L3 - ERP Order Module Support
│   ├── IT: L3 - EDI Integration Maintenance
│   ├── HR: L3 - Order Team Training
│   └── Legal: L3 - Order Terms & Conditions Review
```

This enables impact analysis: "If we change Order Management, which support processes are affected?"

#### 4.2.2 Process Hierarchy (6 Levels)

| Level | Name | Description | Example (Primary) | Example (Secondary - IT) |
|-------|------|-------------|-------------------|--------------------------|
| **L0** | Value Stream / Domain | High-level process description | EXECUTE | IT Services |
| **L1** | Function/Capability | Function or capability description | Range Confirmation & Ordering | Application Development |
| **L2** | Process | Discrete process | Order Management | ERP Development |
| **L3** | Workflow | Workflow within a process | Order Entry Workflow | Change Request Workflow |
| **L4** | Workflow Variation | Variation by category, market, client | Order Entry - Technical (UK) | Change Request - Critical |
| **L5** | Workflow Steps | Steps to execute workflow | Create vendor PO | Code Review Step |

#### 4.2.3 Hierarchy Visualization

**Primary Process Example:**
```
L0: EXECUTE (Value Stream) [PRIMARY]
├── L1: Range Confirmation & Ordering (Function)
│   ├── L2: Order Management (Process)
│   │   ├── L3: Order Entry Workflow
│   │   │   ├── L4: Order Entry - Technical Products (UK)
│   │   │   │   ├── L5: Receive client PO
│   │   │   │   ├── L5: Validate order details
│   │   │   │   ├── L5: Create vendor PO
│   │   │   │   └── L5: Confirm with vendor
│   │   │   ├── L4: Order Entry - Seasonal Products (AU)
│   │   │   └── L4: Order Entry - Showroom (Benelux)
│   │   └── L3: Order Amendment Workflow
│   └── L2: Range Confirmation (Process)
└── L1: Shipment & Logistics (Function)
```

**Secondary Process Example (IT):**
```
L0: IT Services (Domain) [SECONDARY - IT]
├── L1: Application Development (Function)
│   ├── L2: ERP Development (Process)
│   │   ├── L3: Change Request Workflow
│   │   │   ├── L4: Change Request - Critical
│   │   │   │   ├── L5: Log change request
│   │   │   │   ├── L5: Impact assessment
│   │   │   │   ├── L5: Approval routing
│   │   │   │   └── L5: Implementation
│   │   │   └── L4: Change Request - Standard
│   │   └── L3: Release Management Workflow
│   └── L2: Portal Development (Process)
└── L1: IT Support & Service Desk (Function)
```

#### 4.2.4 Inheritance & Aggregation Rules

| Rule Type | Behavior |
|-----------|----------|
| **Issues Roll-Up** | An issue at L5 (e.g., "delete button doesn't work") aggregates to L0 reports |
| **Policy Inheritance** | A policy at L0 applies to all processes down to L5 |
| **KPI Aggregation** | KPIs can be aggregated up the hierarchy |
| **Risk Inheritance** | Risks cascade down; risk reports aggregate up |
| **Cross-Type Aggregation** | Reports can aggregate across Primary + Secondary (e.g., "all Critical issues") |

#### 4.2.5 Resource Allocation - Operational

| Role | Typical Level | Description |
|------|---------------|-------------|
| **Sponsor** | L0-L1 | Responsible for the outcome |
| **Stakeholder** | L1-L2 | Implicated in the outcome |
| **Process Owner** | L1-L3 | Designs that part of the solution |
| **Subject Matter Expert (SME)** | L3-L5 | Understands operational detail |
| **RACI Roles** | All levels | Everyone else allocated per RACI matrix |

#### 4.2.6 Resource Allocation - Project

| Role | Description |
|------|-------------|
| **Programme Manager** | Oversees multiple related projects |
| **Project Manager** | Manages specific project delivery |
| **Business Analyst** | Defines requirements and specifications |
| **Automation Engineer** | Implements automation solutions |
| **Developer** | Builds technical solutions |

#### 4.2.7 Excel Tab Mapping

| Excel Tab | Maps to Process Catalogue |
|-----------|--------------------------|
| Process Catalogue | Core process hierarchy (L0-L3 in example) |
| RAG Criteria | Rating definitions |
| SIPOC Mapping | L5 workflow steps |
| RACI Matrix | Role assignments |

---

### 4.3 Component 3: Operational Quality Logs

**Purpose:** Track the operational environment through RIADA logs (Risks, Issues, Actions, Dependencies, Assumptions) at any level of the hierarchy with severity classification.

#### 4.3.1 Log Types (RIADA)

| Log Type | Description | Example |
|----------|-------------|---------|
| **Risk** | Potential future problem requiring mitigation | "Vendor capacity may be insufficient for peak season" |
| **Issue** | Current problem requiring resolution | "Delete button not working in order entry screen" |
| **Action** | Task to address a risk, issue, or improvement | "Implement data validation rules by Q2" |
| **Dependency** | External factor that process/project relies on | "Requires ERP upgrade to be completed first" |
| **Assumption** | Believed condition taken as true for planning | "Assume freight rates remain stable" |

#### 4.3.2 RIADA Categories

All RIADA items are categorized across four dimensions (matching RAG assessment):

| Category | Description | Severity Levels |
|----------|-------------|-----------------|
| **People** | Skills, capacity, knowledge gaps | Critical, High, Medium, Low |
| **Process** | Workflow, procedure, methodology gaps | Critical, High, Medium, Low |
| **System** | Technology, tool, platform issues | Critical, High, Medium, Low |
| **Data** | Data quality, availability, governance issues | Critical, High, Medium, Low |

#### 4.3.3 Attachment Points

RIADA Logs can be attached to:
- **Business Model** components (any level)
- **Process Catalogue** entries (any level L0-L5)
- **Operating Model Design** components
- **Portfolio Response** items (pillars, programmes, projects, workstreams, work packages)

#### 4.3.4 Aggregation Behavior

```
Example: Issue logged at L5 Step "Create vendor PO"
├── Visible in L4: Order Entry - Technical Products (UK)
├── Visible in L3: Order Entry Workflow
├── Visible in L2: Order Management
├── Visible in L1: Range Confirmation & Ordering
└── Visible in L0: EXECUTE (in aggregated report)
```

#### 4.3.5 RIADA Entity Model

| Field | Description |
|-------|-------------|
| ID | Unique identifier |
| Type | Risk / Issue / Action / Dependency / Assumption |
| Title | Brief description |
| Description | Detailed description |
| Category | People / Process / System / Data |
| Severity | Critical / High / Medium / Low |
| Probability | (For Risks) High / Medium / Low |
| Impact | (For Risks) High / Medium / Low |
| Status | Open / In Progress / Resolved / Closed / Mitigated |
| Attached To | Reference to BM/Process/OM/Portfolio item |
| Attached Level | Level in hierarchy |
| Owner | Responsible person |
| Due Date | Target resolution/review date |
| Resolution | How it was resolved (if applicable) |
| Mitigation | Mitigation plan (for Risks) |
| Linked Items | Related RIADA items (e.g., Action linked to Issue) |
| Created Date | When logged |
| Updated Date | Last update |

#### 4.3.6 RIADA Relationships

RIADA items can be linked to each other:

```
Risk: "Vendor capacity may be insufficient"
├── Linked Action: "Identify backup vendors by March"
├── Linked Action: "Negotiate capacity guarantee with primary vendor"
└── Linked Assumption: "Assume 20% demand increase in Q4"

Issue: "Data entry errors causing order delays"
├── Linked Action: "Implement validation rules"
├── Linked Dependency: "Requires ERP upgrade"
└── Linked Risk: "Risk of continued errors until fix deployed"
```

---

### 4.4 Component 4: Operating Model Design

**Purpose:** Define current and future state operations through a comprehensive set of operating model components attached to processes, and host the **Standard Operating Model** documentation with publishing capabilities.

#### 4.4.1 Operating Model Components

| Component | Description | Excel Tab Reference |
|-----------|-------------|-------------------|
| **Process Definition** | What is the process | Process Catalogue |
| **RACI** | Who does what (Responsible, Accountable, Consulted, Informed) - may include Agents | RACI Matrix |
| **KPIs** | How we know the process is working | KPIs & Metrics |
| **Policies & Rules** | Guardrails for people, system, process | Policies & Rules |
| **Governance** | Key decision-making forums | Governance Framework |
| **Systems** | Technology supporting the process | Systems & Tools |
| **Timing & SLA** | Cycle times, service levels | Timing & SLA |
| **Agents** | AI/Automation agents in the process | *New - not in Excel* |
| **Security** | Data protection controls | *New - not in Excel* |
| **Data** | Data mastered in the process | *New - not in Excel* |

#### 4.4.2 Standard Operating Model Documentation

**Key Feature:** Each process level (L0-L5) can host rich text documentation that forms the "Standard Operating Model" - the authoritative source of how the organization operates.

##### 4.4.2.1 Documentation Content per Process Level

| Process Level | Documentation Content | Typical Length |
|---------------|----------------------|----------------|
| **L0 - Value Stream** | Strategic overview, value chain narrative, key objectives | 2-5 pages |
| **L1 - Function/Capability** | Function description, scope, interfaces, responsibilities | 3-8 pages |
| **L2 - Process** | Process description, inputs/outputs, key activities, ownership | 5-15 pages |
| **L3 - Workflow** | Detailed workflow steps, decision points, exceptions | 5-20 pages |
| **L4 - Workflow Variation** | Variation-specific instructions (by market/category/client) | 2-10 pages |
| **L5 - Workflow Steps** | Step-by-step instructions, screenshots, tips | 1-5 pages per step |

##### 4.4.2.2 Documentation Structure per Process

Each process level documentation includes:

```
Process: [L2-05] Data Management
├── Overview (Rich Text)
│   ├── Purpose & Objectives
│   ├── Scope & Boundaries
│   └── Key Stakeholders
│
├── Operating Model Summary (Auto-generated from components)
│   ├── RACI Summary Table
│   ├── KPIs Dashboard
│   ├── Policies & Rules List
│   ├── Governance Forums
│   ├── Systems & Tools Used
│   ├── Timing & SLA Targets
│   ├── Agents Involved
│   └── Data Mastered
│
├── Detailed Content (Rich Text)
│   ├── Process Narrative
│   ├── Step-by-Step Instructions
│   ├── Decision Trees / Flowcharts
│   ├── Examples & Scenarios
│   ├── Tips & Best Practices
│   └── Common Issues & Solutions
│
├── Related Content (Links)
│   ├── Child Processes (L3, L4, L5)
│   ├── Parent Processes (L1, L0)
│   ├── Related Processes (Siblings)
│   ├── Linked Projects (Portfolio)
│   └── Active RIADA Items
│
└── Appendices
    ├── Templates & Forms
    ├── Reference Documents
    └── Training Materials
```

##### 4.4.2.3 Rich Text Capabilities

| Feature | Description |
|---------|-------------|
| **Formatted Text** | Headings, bold, italic, lists, tables |
| **Images** | Screenshots, diagrams, photos |
| **Embedded Diagrams** | Flowcharts, process maps, swimlanes |
| **Links** | Internal (to other processes) and external URLs |
| **Tables** | Structured data presentation |
| **Code Blocks** | For technical documentation |
| **Callouts** | Tips, warnings, important notes |
| **Version History** | Track changes over time |

#### 4.4.3 Publishing & Report Generation

**Key Feature:** Generate professional PDF and HTML reports from the Standard Operating Model.

##### 4.4.3.1 Report Types

| Report Type | Description | Use Case |
|-------------|-------------|----------|
| **Single Process Report** | One process with full detail | Process owner reference |
| **Process Family Report** | Parent + all children (e.g., L2 + all L3/L4/L5) | Team training |
| **Value Stream Report** | Full L0 → L5 hierarchy | Executive overview |
| **Operating Model Summary** | All components for selected processes | Audit / compliance |
| **Custom Report** | User-selected processes and components | Ad-hoc needs |

##### 4.4.3.2 Report Formats

| Format | Features | Use Case |
|--------|----------|----------|
| **PDF** | Print-ready, paginated, table of contents, headers/footers, page numbers | Formal documentation, audits, training manuals |
| **HTML** | Web-viewable, responsive, interactive navigation, search | Intranet publishing, online reference |
| **Word (DOCX)** | Editable, track changes compatible | Draft review, collaborative editing |

##### 4.4.3.3 Report Customization Options

| Option | Description |
|--------|-------------|
| **Branding** | Organization logo, colors, fonts |
| **Cover Page** | Custom title, date, version, author |
| **Table of Contents** | Auto-generated with page numbers |
| **Component Selection** | Choose which OM components to include |
| **Depth Selection** | Choose how many levels to include (e.g., L2 only, or L2→L5) |
| **RIADA Inclusion** | Optionally include active risks/issues |
| **Confidentiality** | Watermarks, classification labels |
| **Appendix Options** | Include/exclude templates, references |

##### 4.4.3.4 Publishing Workflow

```
1. SELECT SCOPE
   ├── Choose process(es) to publish
   ├── Select hierarchy depth
   └── Select OM components to include

2. CONFIGURE REPORT
   ├── Choose format (PDF / HTML / DOCX)
   ├── Apply branding template
   ├── Set cover page details
   └── Configure options (TOC, RIADA, etc.)

3. PREVIEW
   ├── Review generated report
   └── Make adjustments if needed

4. PUBLISH
   ├── Generate final document
   ├── Save to document library
   ├── Share via link (HTML)
   └── Download (PDF/DOCX)

5. VERSION CONTROL
   ├── Version number assigned
   ├── Publish date recorded
   └── Previous versions archived
```

##### 4.4.3.5 Scheduled Publishing

| Feature | Description |
|---------|-------------|
| **Auto-Publish** | Schedule regular report generation (e.g., monthly SOP update) |
| **Change Detection** | Only republish if content has changed |
| **Distribution List** | Automatically notify stakeholders of new versions |
| **Expiry Alerts** | Notify when documents need review |

#### 4.4.4 Current vs Future State

Each Operating Model component supports:
- **Current State (As-Is):** How things work today
- **Future State (To-Be):** How things will work after transformation
- **Gap Analysis:** Differences between current and future
- **Transition Plan:** How to get from current to future

**Publishing Note:** Reports can be generated for Current State, Future State, or Comparison views.

#### 4.4.5 Agents Component (Detailed)

**Purpose:** The Agents component explicitly tracks AI and automation agents within processes, enabling systematic identification and management of agentic opportunities.

##### 4.4.5.1 Agent Catalogue

The Agent Catalogue is a reference catalogue of all AI/automation agents (current and planned):

| Field | Type | Description |
|-------|------|-------------|
| **agent_id** | UUID | Unique identifier |
| **name** | VARCHAR | Agent name (e.g., "Order Entry Bot", "Invoice Processor") |
| **description** | TEXT | What the agent does |
| **agent_type** | ENUM | Type of automation |
| **technology** | VARCHAR | Technology platform (e.g., "UiPath", "Power Automate", "Claude", "Custom Python") |
| **vendor** | VARCHAR | Vendor/provider |
| **status** | ENUM | Implementation status |
| **owner** | FK | Agent owner (User) |
| **created_date** | DATE | When agent was created/deployed |
| **review_date** | DATE | Next review date |

**Agent Types:**

| Type | Description | Examples |
|------|-------------|----------|
| **RPA** | Robotic Process Automation - mimics human UI interactions | Data entry bots, screen scraping, form filling |
| **AI_Assistant** | AI-powered assistant for human augmentation | Copilots, chatbots, recommendation engines |
| **AI_Agent** | Autonomous AI agent with decision-making capability | Agentic workflows, autonomous task completion |
| **Workflow** | Automated workflow orchestration | Approval routing, notification systems |
| **Integration** | System-to-system integration | API connectors, ETL processes, middleware |
| **Document_AI** | Document processing automation | OCR, document classification, extraction |
| **Predictive** | Predictive/analytical models | Demand forecasting, quality prediction |

**Agent Status:**

| Status | Description |
|--------|-------------|
| **Identified** | Opportunity identified, not yet evaluated |
| **Evaluating** | Under evaluation/POC |
| **Approved** | Approved for implementation |
| **Implementing** | Currently being built/deployed |
| **Live** | In production |
| **Optimizing** | Live and being improved |
| **Retiring** | Being phased out |
| **Retired** | No longer in use |

##### 4.4.5.2 Process-Agent Linkage

Each process can be linked to agents (current and planned):

| Field | Description |
|-------|-------------|
| **process_id** | The process |
| **agent_id** | The agent |
| **linkage_type** | `Current` (live today) or `Future` (planned) |
| **automation_scope** | What part of the process the agent handles |
| **automation_percentage** | Estimated % of process automated by this agent |
| **implementation_project_id** | Link to project implementing this agent |
| **go_live_date** | When agent went/will go live for this process |

##### 4.4.5.3 Automation Coverage View

For each process, display:

```
Process: L2-37 Order Management
├── Current Automation Level: Semi-Automated (40%)
├── Target Automation Level: Fully-Automated (85%)
├── Automation Gap: 45%
│
├── Current Agents (Live):
│   ├── Order Entry Bot (RPA) - 25% coverage
│   │   └── Handles: Standard order data entry
│   └── Order Validation Rules (Workflow) - 15% coverage
│       └── Handles: Basic validation checks
│
├── Future Agents (Planned):
│   ├── AI Order Processor (AI_Agent) - +30% coverage
│   │   └── Will handle: Complex order interpretation, exception handling
│   │   └── Project: PRJ-2026-042 Order Automation Phase 2
│   │   └── Go-Live: Q3 2026
│   └── Predictive Inventory Check (Predictive) - +15% coverage
│       └── Will handle: Proactive inventory verification
│       └── Project: PRJ-2026-055 Predictive Analytics
│       └── Go-Live: Q4 2026
│
└── Remaining Manual: 15%
    └── Exception escalation, vendor negotiation
```

##### 4.4.5.4 Agentic Opportunity Register

A dedicated view/report showing all identified agentic opportunities:

| Column | Description |
|--------|-------------|
| **Process** | Process name and code |
| **Level** | L0-L5 |
| **Current Automation** | Current level |
| **Target Automation** | Target level |
| **Gap** | Difference |
| **Agentic Potential** | None/Low/Medium/High |
| **Opportunity Description** | What could be automated |
| **Estimated Benefit** | Qualitative or quantitative benefit |
| **Complexity** | Low/Medium/High implementation complexity |
| **Priority Score** | Calculated: Potential × Benefit / Complexity |
| **Status** | Not Started / Evaluating / Project Created / In Progress / Complete |
| **Linked Project** | Project addressing this opportunity |

**Filtering Options:**

| Filter | Options |
|--------|---------|
| **Agentic Potential** | High only, High + Medium, All |
| **Current Automation Level** | Manual, Assisted, Semi-Auto, Fully-Auto |
| **Gap Size** | Large (>50%), Medium (25-50%), Small (<25%) |
| **Status** | Not Started, In Progress, Complete |
| **Process Level** | L0, L1, L2, L3, L4, L5 |
| **Process Area** | Filter by L0/L1 |
| **Owner** | Process Owner |

##### 4.4.5.5 Agentic Opportunity Workflow

```
1. IDENTIFY
   ├── Manual entry by Process Owner
   ├── Flagged from RIADA (System Issues indicating manual workarounds)
   ├── Flagged from Survey (Operating Model - System dimension RED)
   └── AI suggestion (from Prompt Library analysis)
         ↓
2. ASSESS
   ├── Set agentic_potential (None/Low/Medium/High)
   ├── Describe opportunity
   ├── Estimate benefit
   ├── Assess complexity
   └── Calculate priority score
         ↓
3. PRIORITIZE
   ├── Review in Agentic Opportunity Register
   ├── Compare with other opportunities
   └── Decide whether to pursue
         ↓
4. MOBILIZE (if approved)
   ├── Create Project in Portfolio
   ├── Link project to process
   ├── Link project to target agent
   └── Set go-live date
         ↓
5. IMPLEMENT
   ├── Track via Portfolio (standard project tracking)
   └── Agent status: Implementing
         ↓
6. DEPLOY
   ├── Agent goes live
   ├── Update process: current_automation_level
   ├── Link agent to process (linkage_type = Current)
   └── Agent status: Live
         ↓
7. MEASURE
   ├── Track adoption via Change & Adoption
   ├── Measure KPI improvement
   └── Update automation_percentage
```

#### 4.4.6 Prompt Library

**Purpose:** A comprehensive library of AI prompts that can be executed directly within the application, with results stored, personalized by context, and integrated with process data.

##### 4.4.6.1 Prompt Library Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           PROMPT LIBRARY ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                         PROMPT TEMPLATE                                  │    │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │    │
│  │  │  Base Prompt (per Process Level × Use Case)                      │   │    │
│  │  │  "Generate documentation for {process_name} at {level}..."       │   │    │
│  │  └─────────────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                      CONTEXT INJECTION                                   │    │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────────────────┐   │    │
│  │  │  UNIVERSAL    │  │ PERSONALI-    │  │  ADDITIONAL               │   │    │
│  │  │  CONTEXT      │  │ ZATION        │  │  CONTEXT                  │   │    │
│  │  │               │  │               │  │                           │   │    │
│  │  │ • Process     │  │ • User Role   │  │ • Recent Metric           │   │    │
│  │  │   hierarchy   │  │ • User Name   │  │ • Current Issue           │   │    │
│  │  │ • Business    │  │ • Team        │  │ • Goal/Objective          │   │    │
│  │  │   Model       │  │ • Expertise   │  │ • Time Period             │   │    │
│  │  │ • RACI        │  │   Level       │  │ • Custom input            │   │    │
│  │  │ • KPIs        │  │ • Preferences │  │ • Selected RIADA items    │   │    │
│  │  │ • Systems     │  │               │  │ • Project context         │   │    │
│  │  │ • Policies    │  │               │  │                           │   │    │
│  │  └───────────────┘  └───────────────┘  └───────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                         LLM EXECUTION                                    │    │
│  │                   (OpenAI / Anthropic / Qwen)                           │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                      RESULT STORAGE                                      │    │
│  │  • Stored in Prompt History                                              │    │
│  │  • Linked to Process, User, Timestamp                                    │    │
│  │  • Versioned results                                                     │    │
│  │  • Feedback/rating captured                                              │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

##### 4.4.6.2 Prompt Template Structure

**Prompts Organized By:**

| Dimension | Description | Example |
|-----------|-------------|---------|
| **Process Level** | Different prompts per level (L0-L5) | L2 strategic overview vs L5 step-by-step detail |
| **Use Case** | Purpose of the prompt | Documentation, Analysis, Training, Communication |
| **Component** | Operating Model component focus | RACI prompt, KPI prompt, Policy prompt |

**Prompt Template Hierarchy:**

```
Organization (Tenant)
├── Global Prompts (available to all processes)
│   ├── Documentation Generation
│   ├── Analysis & Insights
│   ├── Training Material
│   └── Communication Drafts
│
├── Level-Specific Prompts
│   ├── L0 (Value Stream) Prompts
│   │   ├── Strategic Overview
│   │   ├── Value Stream Analysis
│   │   └── Executive Summary
│   ├── L1 (Process Area) Prompts
│   │   ├── Process Area Documentation
│   │   ├── Capability Assessment
│   │   └── Stakeholder Briefing
│   ├── L2 (Process) Prompts
│   │   ├── Process Documentation
│   │   ├── Process Improvement Ideas
│   │   ├── RACI Generation
│   │   └── KPI Recommendations
│   ├── L3 (Workflow) Prompts
│   │   ├── Workflow Documentation
│   │   ├── Workflow Optimization
│   │   └── Training Guide
│   ├── L4 (Variation) Prompts
│   │   ├── Variation Comparison
│   │   ├── Market-Specific Guide
│   │   └── Category-Specific Guide
│   └── L5 (Step) Prompts
│       ├── Step-by-Step Instructions
│       ├── Work Instruction
│       ├── Troubleshooting Guide
│       └── Checklist Generation
│
└── Custom Prompts (user-created)
```

##### 4.4.6.3 Universal Context (Auto-Injected)

**Universal Context** is automatically injected into every prompt execution based on the current process context:

| Context Category | Data Injected | Source |
|------------------|---------------|--------|
| **Process Identity** | Process name, code, level, description | Process Catalogue |
| **Process Hierarchy** | Parent processes (L0→current), child processes | Process Catalogue |
| **Business Model** | Linked markets, clients, categories, partners | Business Model Mapping |
| **RACI** | Current RACI matrix for the process | Operating Model |
| **KPIs** | Current KPIs, targets, actuals | Operating Model |
| **Systems** | Systems used in this process | Operating Model |
| **Policies** | Applicable policies and rules | Operating Model |
| **Timing & SLA** | SLAs, cycle times, timing requirements | Operating Model |
| **RIADA Summary** | Open risks, issues count by severity | Quality Logs |
| **Recent Changes** | Recent updates to this process | Audit Log |
| **Related Projects** | Projects affecting this process | Portfolio |

**Universal Context Template (JSON):**

```json
{
  "process": {
    "id": "proc_123",
    "code": "L2-10",
    "name": "Brief",
    "level": "L2",
    "description": "Client requirements capture process",
    "type": "primary",
    "status": "active"
  },
  "hierarchy": {
    "l0": { "name": "Surity Agent Model", "code": "L0-01" },
    "l1": { "name": "SOURCE", "code": "L1-06" },
    "children_count": 5
  },
  "business_model": {
    "markets": ["UK", "Benelux", "Australia"],
    "clients": ["Bunnings", "Selco", "Maxeda"],
    "categories": ["Technical", "Showroom", "Seasonal", "Home"]
  },
  "operating_model": {
    "raci": {
      "responsible": "Account Manager",
      "accountable": "Account Director",
      "consulted": ["Client", "Merchandiser"],
      "informed": ["QA Manager"]
    },
    "kpis": [
      { "name": "Brief Accuracy", "target": "95%", "current": "89%" },
      { "name": "Brief Cycle Time", "target": "2 days", "current": "3.5 days" }
    ],
    "systems": ["Client Portal", "ERP", "SharePoint"],
    "policies": ["Client Confidentiality Policy", "Data Handling Policy"]
  },
  "riada_summary": {
    "open_risks": 2,
    "open_issues": 5,
    "overdue_actions": 1
  },
  "organization": {
    "name": "Surity",
    "industry": "Sourcing Agent"
  }
}
```

##### 4.4.6.4 User Personalization

**Personalization** adapts the prompt based on who is running it:

| Personalization | Description | Impact on Prompt |
|-----------------|-------------|------------------|
| **User Role** | User's role in the organization | Adjusts tone, detail level, focus |
| **User Name** | User's display name | Personalized addressing |
| **Process Role** | User's RACI role for this process | Focuses on responsibilities |
| **Expertise Level** | Beginner/Intermediate/Expert | Adjusts complexity |
| **Preferences** | User's saved preferences | Output format, length, style |
| **AFI Score** | User's AI Fluency level | Adjusts AI-related content |

**Personalization Examples:**

| User Role | Prompt Adaptation |
|-----------|-------------------|
| **CEO/COO** | Strategic summary, financial impact, executive language |
| **Process Owner** | Operational detail, improvement focus, accountability |
| **Business Analyst** | Documentation focus, gap analysis, detailed specifications |
| **SME** | Step-by-step detail, practical guidance, troubleshooting |
| **Project Manager** | Change impact, timeline, resource implications |
| **New Employee** | Foundational explanations, glossary inclusion, learning focus |

##### 4.4.6.5 Additional Context (User-Provided)

Users can inject **Additional Context** to make prompts more relevant:

| Context Type | Description | Example |
|--------------|-------------|---------|
| **Recent Metric** | Select a KPI to focus on | "Brief Accuracy dropped to 89% this month" |
| **Current Issue** | Select a RIADA item to address | "ISSUE-042: Client complaints about incomplete briefs" |
| **Goal/Objective** | Specify an objective | "Reduce brief cycle time by 30%" |
| **Time Period** | Focus on specific timeframe | "Q4 2025 performance" |
| **Audience** | Who will receive the output | "New team members joining next week" |
| **Project Context** | Link to a project | "Part of Order Management Automation project" |
| **Custom Input** | Free-text additional context | Any user-provided information |
| **Selected Items** | Multi-select RIADA, KPIs, etc. | "Focus on these 3 issues..." |

**Additional Context UI:**

```
┌─────────────────────────────────────────────────────────────────┐
│  ADDITIONAL CONTEXT (Optional)                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Focus Metric:    [ Select KPI...              ▼]               │
│                   ☑ Include current value and trend             │
│                                                                  │
│  Related Issue:   [ Select Issue...            ▼]               │
│                   ☐ ISSUE-042: Client complaints                │
│                   ☐ ISSUE-038: Data entry errors                │
│                   ☑ RISK-015: Staff turnover                    │
│                                                                  │
│  Goal/Objective:  [Reduce brief cycle time by 30%________]      │
│                                                                  │
│  Time Period:     [ Last Quarter              ▼]                │
│                                                                  │
│  Target Audience: [ New Team Members          ▼]                │
│                                                                  │
│  Custom Context:                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ We are onboarding 3 new account managers next week and  │    │
│  │ need to ensure they understand the brief process...     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  [Clear All]                              [Run Prompt →]        │
└─────────────────────────────────────────────────────────────────┘
```

##### 4.4.6.6 Prompt Execution

**Execution Flow:**

```
1. User selects prompt from library
   ↓
2. System loads Universal Context (auto)
   ↓
3. System applies User Personalization (auto)
   ↓
4. User adds Additional Context (optional)
   ↓
5. User previews assembled prompt (optional)
   ↓
6. User clicks "Run Prompt"
   ↓
7. System calls LLM API (OpenAI/Anthropic/Qwen)
   ↓
8. Result displayed in UI
   ↓
9. User can: Edit, Regenerate, Save, Export, Apply
   ↓
10. Result stored in Prompt History
```

**Execution Options:**

| Option | Description |
|--------|-------------|
| **Preview Prompt** | See the fully assembled prompt before execution |
| **Model Selection** | Choose LLM model (if multiple available) |
| **Temperature** | Adjust creativity (0.0 = deterministic, 1.0 = creative) |
| **Max Length** | Set output length limit |
| **Format** | Specify output format (Markdown, Plain text, HTML) |

##### 4.4.6.7 Prompt History & Results Storage

**Every prompt execution is stored:**

| Field | Description |
|-------|-------------|
| `id` | Unique execution ID |
| `prompt_template_id` | Which prompt template was used |
| `process_id` | Which process it was run against |
| `user_id` | Who ran the prompt |
| `universal_context` | Snapshot of context at execution time |
| `personalization` | User personalization applied |
| `additional_context` | User-provided additional context |
| `full_prompt` | Complete assembled prompt sent to LLM |
| `result` | LLM response |
| `model_used` | Which LLM model |
| `tokens_used` | Token count (input + output) |
| `execution_time` | How long it took |
| `rating` | User rating (1-5 stars) |
| `feedback` | User feedback text |
| `created_at` | Timestamp |

**History Features:**

| Feature | Description |
|---------|-------------|
| **View History** | See all past executions for a process |
| **Compare Results** | Compare multiple executions side-by-side |
| **Re-run** | Re-execute with same or modified context |
| **Export** | Export result to document (DOCX, PDF, MD) |
| **Apply to SOM** | Apply result to Standard Operating Model content |
| **Share** | Share result with colleagues |
| **Favorite** | Mark useful results for easy access |
| **Search** | Search across prompt history |

##### 4.4.6.8 Prompt Use Cases by Level

| Level | Use Case | Prompt Description |
|-------|----------|-------------------|
| **L0** | Strategic Overview | Generate executive summary of value stream health |
| **L0** | Business Impact | Analyze business model impact of changes |
| **L1** | Capability Assessment | Assess process area capability maturity |
| **L1** | Stakeholder Briefing | Generate stakeholder communication |
| **L2** | Process Documentation | Generate/update process documentation |
| **L2** | Improvement Analysis | Identify improvement opportunities |
| **L2** | RACI Generation | Suggest RACI based on process description |
| **L2** | KPI Recommendations | Recommend KPIs for this process |
| **L2** | Risk Analysis | Analyze risks based on RIADA data |
| **L3** | Workflow Documentation | Document workflow with decision points |
| **L3** | Training Guide | Create training material for workflow |
| **L3** | Optimization Ideas | Suggest workflow optimizations |
| **L4** | Variation Comparison | Compare variations across markets/categories |
| **L4** | Compliance Check | Check variation against policies |
| **L5** | Work Instruction | Generate detailed work instruction |
| **L5** | Checklist | Generate checklist for step execution |
| **L5** | Troubleshooting | Create troubleshooting guide |
| **All** | Issue Resolution | Suggest resolution for selected issue |
| **All** | Change Communication | Draft communication about process changes |
| **All** | Onboarding Guide | Create onboarding content for new team members |

##### 4.4.6.9 Prompt Template Management

**Template Administration:**

| Feature | Description |
|---------|-------------|
| **System Templates** | Pre-built templates (read-only) |
| **Organization Templates** | Custom templates for the tenant |
| **Personal Templates** | User's private templates |
| **Template Editor** | Create/edit templates with variables |
| **Variable Insertion** | Insert context variables (e.g., `{{process.name}}`) |
| **Testing** | Test template with sample data |
| **Versioning** | Track template changes |
| **Sharing** | Share templates with team |

**Template Variables:**

| Variable | Description |
|----------|-------------|
| `{{process.name}}` | Process name |
| `{{process.level}}` | Process level (L0-L5) |
| `{{process.description}}` | Process description |
| `{{hierarchy.l0.name}}` | Parent L0 name |
| `{{business_model.markets}}` | Linked markets |
| `{{operating_model.raci}}` | RACI matrix |
| `{{operating_model.kpis}}` | KPIs list |
| `{{riada_summary.open_issues}}` | Open issue count |
| `{{user.name}}` | Current user name |
| `{{user.role}}` | Current user role |
| `{{additional.goal}}` | User-provided goal |
| `{{additional.metric}}` | Selected metric |
| `{{additional.issue}}` | Selected issue |
| `{{additional.custom}}` | Custom context |

**Example Template:**

```markdown
# Prompt Template: Process Documentation

## System Instructions
You are an expert business analyst helping to document operational processes.

## Context
Process: {{process.name}} ({{process.code}})
Level: {{process.level}}
Part of: {{hierarchy.l1.name}} → {{hierarchy.l0.name}}

### Business Context
Markets: {{business_model.markets}}
Clients: {{business_model.clients}}
Categories: {{business_model.categories}}

### Current Operating Model
RACI:
{{operating_model.raci}}

KPIs:
{{operating_model.kpis}}

Systems Used:
{{operating_model.systems}}

### Current Issues
Open Issues: {{riada_summary.open_issues}}
Open Risks: {{riada_summary.open_risks}}

## User Context
User: {{user.name}} ({{user.role}})
{{#if additional.goal}}Goal: {{additional.goal}}{{/if}}
{{#if additional.custom}}Additional Context: {{additional.custom}}{{/if}}

## Task
Generate comprehensive process documentation for {{process.name}} that:
1. Explains the purpose and scope
2. Describes the workflow steps
3. Identifies inputs, outputs, and dependencies
4. Notes current challenges and improvement opportunities
5. Is appropriate for {{user.role}} audience
```

##### 4.4.6.10 Prompt Library Data Model

**PromptTemplate**

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier |
| `organization_id` | UUID | Tenant (NULL for system templates) |
| `user_id` | UUID | Creator (NULL for org/system) |
| `scope` | ENUM | 'system', 'organization', 'personal' |
| `name` | VARCHAR(255) | Template name |
| `description` | TEXT | Template description |
| `category` | VARCHAR(100) | Use case category |
| `applicable_levels` | ENUM[] | Which process levels (L0-L5) |
| `template_content` | TEXT | Prompt template with variables |
| `default_settings` | JSONB | Default model, temperature, etc. |
| `variables_schema` | JSONB | Expected variables |
| `version` | INTEGER | Template version |
| `status` | ENUM | 'draft', 'active', 'archived' |
| `created_at` | TIMESTAMP | |
| `updated_at` | TIMESTAMP | |

**PromptExecution**

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier |
| `template_id` | UUID | FK → PromptTemplate |
| `process_id` | UUID | FK → Process |
| `user_id` | UUID | FK → User |
| `universal_context` | JSONB | Context snapshot |
| `personalization` | JSONB | User personalization |
| `additional_context` | JSONB | User-provided context |
| `full_prompt` | TEXT | Assembled prompt |
| `result` | TEXT | LLM response |
| `model_used` | VARCHAR(100) | LLM model identifier |
| `tokens_input` | INTEGER | Input tokens |
| `tokens_output` | INTEGER | Output tokens |
| `execution_ms` | INTEGER | Execution time in ms |
| `rating` | INTEGER | User rating (1-5) |
| `feedback` | TEXT | User feedback |
| `is_favorite` | BOOLEAN | Favorited by user |
| `applied_to` | VARCHAR(50) | Where result was applied |
| `created_at` | TIMESTAMP | |

**PromptContextSnapshot**

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier |
| `execution_id` | UUID | FK → PromptExecution |
| `context_type` | VARCHAR(50) | 'process', 'business_model', 'operating_model', etc. |
| `context_data` | JSONB | Snapshot of context data |
| `created_at` | TIMESTAMP | |

##### 4.4.6.11 Integration Points

| Integration | Description |
|-------------|-------------|
| **Process Catalogue** | Run prompts from process detail view |
| **Operating Model** | Apply results to SOM content |
| **Quality Logs** | Select RIADA items as context; generate resolution suggestions |
| **Portfolio** | Include project context; generate project communications |
| **Surveys** | Generate survey analysis reports |
| **Reports** | Include AI-generated insights in published reports |

##### 4.4.6.12 Prompt Library UI Entry Points

| Location | Access Method |
|----------|---------------|
| **Process Detail Page** | "AI Assist" button → Prompt selector |
| **Operating Model Editor** | "Generate with AI" for each component |
| **RIADA Item View** | "Suggest Resolution" button |
| **Global Prompt Library** | Dedicated library page with search/browse |
| **Quick Access** | Recent prompts in sidebar |
| **Keyboard Shortcut** | Cmd/Ctrl + K → "Run Prompt..." |

#### 4.4.7 Excel Tab Mapping

| Excel Tab | Maps to Operating Model Design |
|-----------|-------------------------------|
| RACI Matrix | RACI component |
| KPIs & Metrics | KPIs component |
| Policies & Rules | Policies component |
| Governance Framework | Governance component |
| Systems & Tools | Systems component |
| Timing & SLA | Timing component |

---

### 4.5 Component 5: Portfolio Response (Portfolio Focus)

**Purpose:** Strategic portfolio management implementing hierarchical project organization with WSVF (Weighted Shortest Value First) prioritization, RIADA management at every level, and resource allocation to the Process Catalogue.

#### 4.5.1 Portfolio Hierarchy (7 Levels)

```
Organization (Tenant Level)
└── Portfolio
    └── Strategic Pillar
        └── Initiative / Programme
            └── Project
                └── Workstream (may be cross-project capability)
                    └── Work Package
```

| Level | Description | Example |
|-------|-------------|---------|
| **Organization** | Tenant/company level | Surity |
| **Portfolio** | Collection of strategic pillars | "2026 Strategic Portfolio" |
| **Pillar** | High-level strategic theme | "Digital Transformation", "Operational Excellence" |
| **Initiative/Programme** | Collection of related projects | "Process Automation Programme" |
| **Project** | Discrete delivery effort | "Order Management Automation" |
| **Workstream** | Sub-division; may be cross-project | "AI Bot Development", "Training" |
| **Work Package** | Specific deliverable | "Bot Training Data Preparation" |

#### 4.5.2 WSVF Prioritization Methodology

**Weighted Shortest Value First (WSVF)** is used to prioritize projects and initiatives:

```
Priority Score = (Project Value × Confidence Level) ÷ (Effort × Duration)
```

| Factor | Description | Scale |
|--------|-------------|-------|
| **Project Value** | Business value delivered | 1-10 (10 = highest value) |
| **Confidence Level** | Certainty of value realization | 0.1-1.0 (1.0 = highly confident) |
| **Effort** | Resource effort required | 1-10 (10 = highest effort) |
| **Duration** | Time to complete | Weeks/Months |

**WSVF Score Interpretation:**
- Higher score = Higher priority (more value per unit of effort/time)
- Enables objective comparison across different project types
- Supports portfolio optimization decisions

**Example Calculation:**
```
Project: "Order Management Automation"
- Project Value: 8 (high business impact)
- Confidence: 0.8 (proven technology)
- Effort: 5 (medium complexity)
- Duration: 3 months

Priority Score = (8 × 0.8) ÷ (5 × 3) = 6.4 ÷ 15 = 0.43
```

#### 4.5.3 Portfolio Entities

| Entity | Description | Key Attributes |
|--------|-------------|----------------|
| **Organization** | Tenant container | Name, settings, users |
| **Portfolio** | Strategic collection | Name, owner, time horizon, budget |
| **Pillar** | Strategic theme | Name, sponsor, objectives, KPIs |
| **Initiative/Programme** | Project collection | Name, PM, scope, timeline, budget |
| **Project** | Delivery effort | Name, PM, WSVF factors, status, resources |
| **Workstream** | Project subdivision | Name, lead, cross-project flag |
| **Work Package** | Deliverable | Name, owner, due date, status |

#### 4.5.4 Light Project Management Features

The Portfolio Response provides lightweight project management capabilities focused on tracking outcomes, scope, milestones, budget, and status without the overhead of full project management tools.

##### 4.5.4.1 Benefits & Outcomes

| Field | Description | Example |
|-------|-------------|---------|
| **Benefits Description** | Expected benefits from the project | "Reduce order processing time by 40%, eliminate manual data entry errors" |
| **Outcome Statement** | Measurable outcomes to be achieved | "Process 200 orders/day with <1% error rate by Q3 2026" |
| **Success Criteria** | How success will be measured | "Cycle time <4 hours, Error rate <1%, User satisfaction >4.5/5" |
| **Strategic Alignment** | Link to strategic objectives | "Supports Pillar: Operational Excellence" |

##### 4.5.4.2 Scope Statement

| Field | Description | Example |
|-------|-------------|---------|
| **In Scope** | What is included in the project | "Order entry automation, Validation rules, Integration with ERP, User training" |
| **Out of Scope** | What is explicitly excluded | "Legacy system retirement, Warehouse processes, Customer portal changes" |
| **Scope Notes** | Additional context or constraints | "Phase 1 covers UK only; Benelux and AU in Phase 2" |

**Scope Change Tracking:**

| Field | Description |
|-------|-------------|
| Change ID | Unique identifier |
| Change Description | What changed |
| Reason | Why the change was requested |
| Impact | Effect on timeline, budget, resources |
| Status | Requested / Approved / Rejected |
| Approved By | Who approved the change |
| Date | When approved/rejected |

##### 4.5.4.3 Key Milestones

Milestones are categorized by type for clear tracking and reporting:

| Milestone Type | Description | Examples |
|----------------|-------------|----------|
| **Project** | Internal project delivery milestones | "Design Complete", "UAT Start", "Go-Live" |
| **Customer** | Client-facing or external commitments | "Client Demo", "Pilot Launch", "Full Rollout" |
| **Financial** | Budget and financial gate milestones | "Business Case Approved", "Budget Release", "Final Invoice" |
| **Benefit** | Benefit realization milestones | "First Benefits Measured", "Target ROI Achieved", "Full Benefits Realized" |

**Milestone Entity Model:**

| Field | Description |
|-------|-------------|
| ID | Unique identifier |
| Name | Milestone name |
| Type | Project / Customer / Financial / Benefit |
| Description | Detailed description |
| Planned Date | Target completion date |
| Actual Date | Actual completion date (if complete) |
| Status | Not Started / In Progress / Complete / Delayed / At Risk |
| Owner | Responsible person |
| Dependencies | Other milestones this depends on |
| Deliverables | What must be delivered to achieve this milestone |
| Notes | Additional context |

**Milestone Dashboard View:**

```
Project: Order Management Automation
═══════════════════════════════════════════════════════════════════════════

PROJECT MILESTONES
  ✓ Requirements Sign-off          Planned: 15-Jan  Actual: 14-Jan   COMPLETE
  ✓ Design Complete                Planned: 01-Feb  Actual: 03-Feb   COMPLETE
  ● Development Complete           Planned: 15-Mar  Actual: --       IN PROGRESS
  ○ UAT Start                      Planned: 01-Apr  Actual: --       NOT STARTED
  ○ Go-Live                        Planned: 01-May  Actual: --       NOT STARTED

CUSTOMER MILESTONES
  ✓ Client Kick-off                Planned: 10-Jan  Actual: 10-Jan   COMPLETE
  ○ Client Demo                    Planned: 20-Mar  Actual: --       NOT STARTED
  ○ Pilot Launch (UK)              Planned: 15-Apr  Actual: --       NOT STARTED
  ○ Full Rollout                   Planned: 01-Jun  Actual: --       NOT STARTED

FINANCIAL MILESTONES
  ✓ Business Case Approved         Planned: 05-Jan  Actual: 05-Jan   COMPLETE
  ✓ Budget Released                Planned: 10-Jan  Actual: 10-Jan   COMPLETE
  ○ Mid-Project Review             Planned: 01-Mar  Actual: --       NOT STARTED
  ○ Final Invoice                  Planned: 30-Jun  Actual: --       NOT STARTED

BENEFIT MILESTONES
  ○ Baseline Metrics Captured      Planned: 31-Jan  Actual: --       NOT STARTED
  ○ First Benefits Measured        Planned: 01-Jun  Actual: --       NOT STARTED
  ○ Target ROI Achieved            Planned: 01-Sep  Actual: --       NOT STARTED
  ○ Full Benefits Realized         Planned: 31-Dec  Actual: --       NOT STARTED
```

##### 4.5.4.4 Budget & Financial Tracking

**Budget Status:**

| Status | Description |
|--------|-------------|
| **Draft** | Budget being prepared |
| **Pending Approval** | Submitted for approval |
| **Approved** | Budget approved and available |
| **On Hold** | Budget frozen pending review |
| **Closed** | Project complete, budget closed |

**Financial Tracking Fields:**

| Field | Description | Example |
|-------|-------------|---------|
| **Budgeted Spend** | Total approved budget | $250,000 |
| **Current Spend** | Actual spend to date | $85,000 |
| **Projected Spend** | Forecast total spend at completion | $240,000 |
| **Variance** | Difference (Budgeted - Projected) | $10,000 (4% under) |
| **Budget Status** | Current approval status | Approved |
| **Contingency** | Reserved contingency amount | $25,000 (10%) |
| **Contingency Used** | Contingency spent to date | $5,000 |

**Financial Summary View:**

```
Project: Order Management Automation
═══════════════════════════════════════════════════════════════════════════

BUDGET OVERVIEW
  Budget Status:     APPROVED
  Budgeted Spend:    $250,000
  Current Spend:     $85,000   (34% of budget)
  Projected Spend:   $240,000  (96% of budget)
  Variance:          $10,000   (4% UNDER budget) ✓

SPEND BREAKDOWN
  ├── Personnel:     $60,000  (71% of current spend)
  ├── Technology:    $15,000  (18%)
  ├── Training:      $5,000   (6%)
  └── Other:         $5,000   (5%)

CONTINGENCY
  Reserved:          $25,000
  Used:              $5,000   (20% of contingency)
  Remaining:         $20,000

FORECAST
  Month     Planned    Actual    Cumulative
  ─────────────────────────────────────────
  Jan       $30,000    $28,000   $28,000
  Feb       $40,000    $42,000   $70,000
  Mar       $50,000    $15,000*  $85,000    * Month in progress
  Apr       $50,000    --        --
  May       $40,000    --        --
  Jun       $40,000    --        --
```

##### 4.5.4.5 Benefits Tracking

| Field | Description | Example |
|-------|-------------|---------|
| **Target Benefits** | Expected benefits (quantified) | "$500K annual savings, 40% cycle time reduction" |
| **Current Benefits Accrued** | Benefits realized to date | "$125K savings (Q1), 25% cycle time improvement" |
| **Benefits Realization %** | Progress toward target | 25% of annual target |
| **Measurement Method** | How benefits are measured | "Monthly comparison vs. baseline metrics" |
| **Baseline Date** | When baseline was captured | January 15, 2026 |
| **Review Frequency** | How often benefits are reviewed | Monthly |

**Benefits Tracking View:**

```
Project: Order Management Automation
═══════════════════════════════════════════════════════════════════════════

BENEFITS SUMMARY
  Target Annual Benefits:    $500,000
  Current Benefits Accrued:  $125,000  (25% of target)
  On Track:                  YES ✓

BENEFIT BREAKDOWN
  Benefit                    Target      Current    Status
  ─────────────────────────────────────────────────────────
  Labor Cost Reduction       $300,000    $80,000    ✓ On Track
  Error Reduction Savings    $100,000    $25,000    ✓ On Track
  Cycle Time Improvement     $100,000    $20,000    ⚠ At Risk

BENEFIT TIMELINE
  Q1 2026:  $125,000 (Actual)     ✓ Achieved
  Q2 2026:  $125,000 (Forecast)
  Q3 2026:  $125,000 (Forecast)
  Q4 2026:  $125,000 (Forecast)
  ─────────────────────────────────
  Total:    $500,000
```

##### 4.5.4.6 Project Status (RAG)

Projects are assessed across five dimensions using RAG (Red/Amber/Green) status:

| Dimension | What It Measures | RAG Criteria |
|-----------|------------------|--------------|
| **Resource** | Team capacity and availability | 🟢 Fully staffed / 🟡 Minor gaps / 🔴 Critical gaps |
| **Quality** | Deliverable quality and defects | 🟢 Meeting standards / 🟡 Some issues / 🔴 Major quality concerns |
| **Scope** | Scope stability and changes | 🟢 Stable / 🟡 Minor changes / 🔴 Significant scope creep |
| **Benefits Delivery** | Progress toward benefits | 🟢 On track / 🟡 At risk / 🔴 Benefits unlikely |
| **Timeline** | Schedule adherence | 🟢 On schedule / 🟡 Minor delays / 🔴 Significant delays |

**RAG Status Entity Model:**

| Field | Description |
|-------|-------------|
| Dimension | Resource / Quality / Scope / Benefits Delivery / Timeline |
| Status | Green / Amber / Red |
| Trend | Improving (↑) / Stable (→) / Declining (↓) |
| Commentary | Explanation of current status |
| Actions | Mitigation actions if Amber/Red |
| Updated By | Who updated the status |
| Updated Date | When last updated |

**Project Status Dashboard:**

```
Project: Order Management Automation
═══════════════════════════════════════════════════════════════════════════

OVERALL STATUS: 🟡 AMBER

STATUS BY DIMENSION
  Dimension           Status    Trend    Commentary
  ─────────────────────────────────────────────────────────────────────────
  Resource            🟢 GREEN   →       Team fully staffed, no concerns
  Quality             🟢 GREEN   ↑       Defect rate improving, UAT prep on track
  Scope               🟡 AMBER   →       2 change requests pending approval
  Benefits Delivery   🟢 GREEN   →       Q1 benefits achieved as planned
  Timeline            🟡 AMBER   ↓       Development 3 days behind schedule

ACTIONS FOR AMBER/RED ITEMS
  • Scope: Review change requests in Thursday steering committee
  • Timeline: Adding 1 developer for 2 weeks to recover schedule

LAST UPDATED: March 15, 2026 by John Smith (Project Manager)
```

##### 4.5.4.7 Project Summary Card

Consolidated view of all project management data:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PROJECT: Order Management Automation                           Status: 🟡   │
├─────────────────────────────────────────────────────────────────────────────┤
│ OVERVIEW                                                                     │
│ Pillar: Operational Excellence    Programme: Process Automation             │
│ PM: John Smith                    Sponsor: Sarah Jones                      │
│ Start: Jan 2026                   End: Jun 2026                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ BENEFITS & OUTCOMES                                                          │
│ Target: $500K annual savings, 40% cycle time reduction                      │
│ Current: $125K accrued (25%)                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ SCOPE                                                                        │
│ In: Order entry automation, Validation rules, ERP integration, Training     │
│ Out: Legacy retirement, Warehouse processes, Customer portal                │
├─────────────────────────────────────────────────────────────────────────────┤
│ MILESTONES                              │ BUDGET                             │
│ Next: Development Complete (15-Mar)     │ Budgeted:  $250,000               │
│ Progress: 3 of 8 complete               │ Current:   $85,000 (34%)          │
│                                         │ Projected: $240,000 (96%)         │
├─────────────────────────────────────────────────────────────────────────────┤
│ STATUS (RAG)                                                                 │
│ Resource: 🟢  Quality: 🟢  Scope: 🟡  Benefits: 🟢  Timeline: 🟡            │
├─────────────────────────────────────────────────────────────────────────────┤
│ RIADA SUMMARY                                                                │
│ Risks: 2 (1 High, 1 Med)   Issues: 1 (Med)   Actions: 4 (2 overdue)        │
│ Dependencies: 3            Assumptions: 2                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 4.5.5 RIADA Management at Each Portfolio Level

**Key Feature:** RIADA (Risk, Issue, Action, Dependency, Assumption) tracking is available at every level of the portfolio hierarchy.

```
Organization: "Surity"
└── Portfolio: "2026 Strategic Portfolio"
    ├── RIADA: Portfolio-level tracking
    │
    └── Pillar: "Digital Transformation"
        ├── RIADA: Pillar-level tracking
        │
        └── Initiative: "Process Automation Programme"
            ├── RIADA: Programme-level tracking
            │
            └── Project: "Order Management Automation"
                ├── RIADA: Project-level tracking
                │
                └── Workstream: "AI Bot Development"
                    ├── RIADA: Workstream-level tracking
                    │
                    └── Work Package: "Bot Training Data Preparation"
                        └── RIADA: Work package-level tracking
```

#### 4.5.6 RIADA Aggregation in Portfolio

| Report Level | Shows |
|--------------|-------|
| **Work Package** | Only RIADA items for that work package |
| **Workstream** | Aggregated RIADA from all work packages + workstream-level items |
| **Project** | Aggregated RIADA from all workstreams + project-level items |
| **Initiative** | Aggregated RIADA from all projects + initiative-level items |
| **Pillar** | Aggregated RIADA from all initiatives + pillar-level items |
| **Portfolio** | Aggregated RIADA from all pillars + portfolio-level items |
| **Organization** | Aggregated RIADA across all portfolios |

#### 4.5.7 Real-time KPIs & Dashboard

Portfolio health metrics displayed in real-time:

| KPI Category | Metrics |
|--------------|---------|
| **Portfolio Health** | % on track, % at risk, % blocked |
| **WSVF Distribution** | Priority score distribution, top priorities |
| **RIADA Summary** | Open risks by severity, overdue actions, critical dependencies |
| **Resource Utilization** | Allocation %, capacity vs demand |
| **Timeline** | Milestones due, slippage trends |
| **Budget** | Spend vs budget, forecast accuracy |

#### 4.5.8 Cross-Project Capabilities

Some workstreams span multiple projects:
- **AI Automation** - Applied across multiple process improvement projects
- **Training & Change Management** - Supports all transformation projects
- **Data Migration** - Shared capability across system projects

**RIADA for Cross-Project Workstreams:** Issues/risks in shared capabilities can be linked to multiple projects and roll up to all affected initiatives.

#### 4.5.9 Project Resource Allocation

Projects allocate resources to Process Catalogue entries:

| Resource Role | Description |
|---------------|-------------|
| Programme Manager | Oversees programme of projects |
| Project Manager | Manages project delivery |
| Business Analyst | Defines requirements |
| Automation Engineer | Implements automation |
| Developer | Builds solutions |

**Linkage:** Project resources are linked to specific processes (L0-L5) they are transforming.

#### 4.5.10 Governance Integration

| Governance Element | Description |
|-------------------|-------------|
| Steering Committee | Strategic oversight |
| Project Board | Project-level decisions |
| Working Groups | Operational coordination |
| Decision Log | Record of key decisions |
| RIADA Log | Integrated with Quality Logs (Component 3) |

#### 4.5.11 Portfolio-to-Process Linkage

Each portfolio item can be linked to Process Catalogue entries:

```
Project: "Order Management Automation"
├── Linked Process: L2 - Order Management
├── Linked Process: L3 - Order Entry Workflow
├── Linked Process: L3 - Order Amendment Workflow
└── Linked Process: L5 - Create vendor PO (step being automated)

Impact: 
- RIADA items from project visible in Process Catalogue views
- Process issues visible in Project RIADA dashboard
- Enables "What projects are affecting this process?" queries
```

#### 4.5.12 Excel Tab Mapping

| Excel Tab | Maps to Portfolio Response |
|-----------|---------------------------|
| Action Plans | Improvement actions (basic project tracking) |
| Governance Framework | Governance forums |

---

### 4.6 Component 6: Change & Adoption Monitoring

**Purpose:** Measure whether changes are being adopted and delivering expected outcomes through surveys, lead indicators, and KPI tracking.

#### 4.6.1 Monitoring Components

| Component | Description |
|-----------|-------------|
| **Adoption Surveys** | Assess if lead indicators of adoption are present |
| **Lead Indicators** | Early signals that adoption is happening |
| **Lag Indicators** | Outcome measures showing results |
| **KPI Selection** | Specific KPIs selected from main KPI catalogue |
| **Benefits Realization** | Tracking whether expected benefits are achieved |

#### 4.6.2 Lead Indicators of Adoption

Example lead indicators (to be surveyed):
- Training completed
- System access provisioned
- Documentation read/acknowledged
- Process followed correctly (spot checks)
- Questions/support tickets reducing
- User confidence (self-reported)

#### 4.6.3 KPI Tracking

KPIs are selected from the main KPI Catalogue and tracked for specific changes:

| Metric | Baseline | Target | Current | Trend |
|--------|----------|--------|---------|-------|
| Process Cycle Time | 32 hrs | 24 hrs | 28 hrs | ↑ |
| Error Rate | 5% | 1% | 3% | ↑ |
| User Satisfaction | 3.2 | 4.5 | 3.8 | ↑ |

#### 4.6.4 Excel Tab Mapping

| Excel Tab | Maps to Change & Adoption |
|-----------|--------------------------|
| KPIs & Metrics | KPI selection source |
| Summary Dashboard | Aggregated metrics view |

---

### 4.7 Component 7: Surveys

**Purpose:** Create and administer surveys to capture organizational capability, process health, change readiness, and adoption evidence. Surveys feed data into other components (Process Catalogue, Portfolio, Change & Adoption).

#### 4.7.1 Survey Types (4 Modes)

The Surveys component supports 4 distinct survey modes, each serving a different purpose:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SURVEY COMPONENT                                       │
│                            4 Survey Modes                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  MODE 1: AI FLUENCY              MODE 2: OPERATING MODEL                        │
│  ══════════════════              ══════════════════════                         │
│  "What level of AI               "Which processes, systems,                     │
│   capability do we have?"         people, data need optimising?"                │
│                                                                                  │
│  • Captured by: Individual       • Captured by: Process                         │
│  • Viewed by: Role, Process      • Assessed: System, People,                    │
│  • Output: AFI Score (0-100)       Process, Data (SPRD)                         │
│  • Use: Training, Champions      • Output: RAG by dimension                     │
│                                  • Use: Improvement prioritization              │
│                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────  │
│                                                                                  │
│  MODE 3: CHANGE READINESS        MODE 4: ADOPTION EVIDENCE                      │
│  ════════════════════════        ═════════════════════════                      │
│  "Is the organization ready      "Is the change being adopted                   │
│   for this change?"               and working?"                                 │
│                                                                                  │
│  • Scope: Project / Programme    • Scope: Project / Programme                   │
│  • Timing: Pre-kickoff           • Timing: Post go-live                         │
│  • Output: Readiness Score       • Measures: Process compliance,                │
│  • Use: Go/No-go, Planning         Role behavior, KPI movement                  │
│                                  • Output: Adoption Score                       │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

| Mode | Purpose | Scope | Key Output |
|------|---------|-------|------------|
| **AI Fluency** | Measure AI capability | Individual → Role → Process | AFI Score (0-100) |
| **Operating Model** | Assess process health | Process (L0-L5) × 4 dimensions | RAG by SPRD |
| **Change Readiness** | Assess readiness for change | Project / Programme | Readiness Score % |
| **Adoption Evidence** | Measure change adoption | Project / Programme | Adoption Score % |

---

#### 4.7.2 Mode 1: AI Fluency Survey

**Purpose:** Measure individual AI capability to inform training strategy, identify champions, and assess transformation readiness.

##### 4.7.2.1 Capture & View Dimensions

| Dimension | Description |
|-----------|-------------|
| **Captured By** | Individual (each person completes survey) |
| **Viewed By Role** | Aggregate AFI by Role (e.g., "Account Managers avg AFI = 45") |
| **Viewed By Process** | Aggregate AFI by Process owners/participants (e.g., "Order Management team avg AFI = 62") |

##### 4.7.2.2 AI Competency Model (6 Levels)

| Level | Competency | Capability Description |
|-------|------------|------------------------|
| **L0** | No Experience | Haven't used AI tools |
| **L1** | Basic Prompting | Simple questions, basic answers |
| **L2** | Advanced Prompting | Multi-step prompts, context setting, iteration |
| **L3** | Deep Research | Complex analysis, synthesis, research tasks |
| **L4** | Process Automation | Workflow automation, batch processing |
| **L5** | Solution Building | Custom solutions, API integration, agent building |

##### 4.7.2.3 AI Fluency Index (AFI) Scoring

**Scale:** 0-100 points calculated from 5 components:

| Component | Points | What It Measures |
|-----------|--------|------------------|
| **Usage Frequency** | 20 pts | Work + Personal AI usage frequency |
| **Competency Level** | 30 pts | Self-assessed capability (L0-L5) |
| **Application Breadth** | 20 pts | Number of use cases applied |
| **Confidence Level** | 15 pts | Self-reported confidence |
| **Readiness** | 15 pts | Learning willingness + impact perception |

**Proficiency Bands:**

| Band | AFI Score | Classification | Action |
|------|-----------|----------------|--------|
| **Beginner** | 0-20 | Limited/no experience | Foundations training |
| **Novice** | 21-40 | Basic use, low confidence | Guided practice |
| **Intermediate** | 41-60 | Regular use, growing skills | Advanced training |
| **Advanced** | 61-80 | Confident power user | AI Champion candidate |
| **Expert** | 81-100 | AI champion, solution builder | Train others, lead initiatives |

##### 4.7.2.4 AI Fluency Survey Questions (15 Questions)

| # | Question Topic | Response Type | Points |
|---|----------------|---------------|--------|
| 1 | Work AI usage frequency | Scale (Never → Daily) | 0-12 |
| 2 | Personal AI usage frequency | Scale (Never → Daily) | 0-8 |
| 3 | Primary AI tools used | Multi-select | — |
| 4 | Use cases applied | Checklist (14 items) | 0-20 |
| 5 | Self-assessed competency level | Single (L0-L5) | 0-30 |
| 6 | Confidence level | Scale (1-5) | 0-15 |
| 7 | Biggest barriers to AI use | Multi-select | — |
| 8 | Training format preference | Single | — |
| 9 | Time available for training | Single | — |
| 10 | Interest in becoming AI Champion | Yes/No/Maybe | — |
| 11 | Interest in AI training | Scale | 0-8 |
| 12 | Best use cases for your role | Open text | — |
| 13 | Belief in AI impact | Scale | 0-7 |
| 14 | Current AI limitations | Open text | — |
| 15 | Support needed | Open text | — |

##### 4.7.2.5 AI Fluency Outputs

| Output | Description | View By |
|--------|-------------|---------|
| **Individual AFI Score** | Personal score 0-100 | User profile |
| **Role AFI Average** | Average by Role | Role Catalogue |
| **Process AFI Average** | Average by Process team | Process Catalogue |
| **Organization AFI** | Org-wide baseline | Dashboard |
| **Proficiency Distribution** | % in each band | Dashboard |
| **Champion List** | AFI ≥61 individuals | Reference Data |
| **Training Needs Matrix** | Gaps by role/team | Reports |

---

#### 4.7.3 Mode 2: Operating Model Survey

**Purpose:** Assess process health across 4 dimensions (System, People, Process, Data) using RAG methodology to identify optimization priorities.

##### 4.7.3.1 SPRD Assessment Framework (4 Dimensions)

| Dimension | Code | What It Assesses |
|-----------|------|------------------|
| **System** | S | Technology, automation, integration, reliability |
| **People** | P | Staffing levels, skills, turnover, roles, morale |
| **Process** | Pr | Documentation, standardization, efficiency, SLA performance |
| **Data** | D | Accuracy, completeness, timeliness, governance |

##### 4.7.3.2 RAG Rating Scale

| Rating | Status | Performance | Priority |
|--------|--------|-------------|----------|
| 🟢 **GREEN** | Well-functioning | >95% performance | Monitor |
| 🟡 **AMBER** | Needs improvement | 85-95% performance | Address 3-6 months |
| 🔴 **RED** | Critical issues | <85% performance | Address immediately |

##### 4.7.3.3 Survey Scope

**Linked To:** Process Catalogue (L0-L5)

**Respondent Assignment by Role Level:**

| Role Level | Processes Assessed | Items per Person |
|------------|-------------------|------------------|
| Director | L1 + selected L2 | 20-30 items |
| Manager | L2 processes | 8-12 items |
| Team Lead/Specialist | L3 processes | 10-20 items |

##### 4.7.3.4 Operating Model Survey Questions

**Per Dimension (SPRD):**

**SYSTEM Questions:**

| # | Question | Response |
|---|----------|----------|
| SYS-1 | Primary system/tool used | Select from System Catalogue |
| SYS-2 | System reliability (uptime) | RAG |
| SYS-3 | Level of automation | Scale (Manual → Fully automated) |
| SYS-4 | Integration with other systems | RAG |
| SYS-5 | System meets requirements | RAG |
| SYS-6 | System issues/pain points | Open text |
| SYS-7 | System improvement ideas | Open text |

**PEOPLE Questions:**

| # | Question | Response |
|---|----------|----------|
| PEO-1 | Current staffing vs. required | RAG |
| PEO-2 | Skill level adequacy | RAG |
| PEO-3 | Staff turnover impact | RAG |
| PEO-4 | Role clarity (RACI defined) | RAG |
| PEO-5 | Team morale | Scale |
| PEO-6 | Training adequacy | RAG |
| PEO-7 | People issues/pain points | Open text |

**PROCESS Questions:**

| # | Question | Response |
|---|----------|----------|
| PRC-1 | Process documentation status | RAG |
| PRC-2 | Process standardization | RAG |
| PRC-3 | SLA performance | RAG |
| PRC-4 | Process efficiency | RAG |
| PRC-5 | Handoff effectiveness | RAG |
| PRC-6 | Process issues/pain points | Open text |

**DATA Questions:**

| # | Question | Response |
|---|----------|----------|
| DAT-1 | Data accuracy | RAG |
| DAT-2 | Data completeness | RAG |
| DAT-3 | Data timeliness | RAG |
| DAT-4 | Single source of truth exists | Yes/No |
| DAT-5 | Data governance in place | RAG |
| DAT-6 | Data issues/pain points | Open text |

##### 4.7.3.5 Operating Model Survey Outputs

| Output | Description | Feeds Into |
|--------|-------------|------------|
| **Process RAG Matrix** | All processes × 4 dimensions | Process Catalogue (updates RAG status) |
| **RED Process List** | Priority intervention list | RIADA (auto-create Issues) |
| **Dimension Analysis** | Weakest/strongest dimension | Executive Dashboard |
| **Function Heatmap** | RAG by L0/L1 | Department planning |
| **Issue Register** | All captured issues | Quality Logs (RIADA) |
| **Improvement Backlog** | All suggestions | Portfolio (potential projects) |

---

#### 4.7.4 Mode 3: Change Readiness Survey

**Purpose:** Assess organizational and team readiness for a specific change initiative before project/programme kickoff.

##### 4.7.4.1 Survey Scope

**Linked To:** Portfolio Item (Project or Programme)

**Timing:** Before kickoff (Go/No-go decision input)

**Respondents:** Stakeholders affected by the change

| Stakeholder Type | Focus Areas |
|------------------|-------------|
| **Sponsors** | Vision clarity, commitment, resource availability |
| **Managers** | Team capacity, competing priorities, support capability |
| **End Users** | Understanding, willingness, concerns |
| **IT/Support** | Technical readiness, integration concerns |

##### 4.7.4.2 Readiness Dimensions (ADKAR-based)

| Dimension | Question Focus |
|-----------|----------------|
| **Awareness** | Do people understand why the change is needed? |
| **Desire** | Do they want to participate and support the change? |
| **Knowledge** | Do they know how to change? |
| **Ability** | Can they implement the required skills and behaviors? |
| **Reinforcement** | Are systems in place to sustain the change? |

##### 4.7.4.3 Change Readiness Survey Questions (16 Questions)

| # | Dimension | Question | Response |
|---|-----------|----------|----------|
| 1 | Awareness | I understand why this change is necessary | Scale 1-5 |
| 2 | Awareness | The business case is clear | Scale 1-5 |
| 3 | Awareness | I understand what will change for me/my team | Scale 1-5 |
| 4 | Desire | I support this change initiative | Scale 1-5 |
| 5 | Desire | I believe this change will improve things | Scale 1-5 |
| 6 | Desire | I am willing to adopt new ways of working | Scale 1-5 |
| 7 | Knowledge | I know what I need to do differently | Scale 1-5 |
| 8 | Knowledge | Training/resources are available | Scale 1-5 |
| 9 | Ability | I have capacity to learn new skills | Scale 1-5 |
| 10 | Ability | My team has capacity to implement | Scale 1-5 |
| 11 | Ability | There are no major blockers | Scale 1-5 |
| 12 | Reinforcement | Leadership is committed | Scale 1-5 |
| 13 | Reinforcement | Success will be recognized/rewarded | Scale 1-5 |
| 14 | Overall | I believe this change will succeed | Scale 1-5 |
| 15 | Open | My biggest concerns | Open text |
| 16 | Open | What would help me embrace this change | Open text |

##### 4.7.4.4 Change Readiness Scoring

**Readiness Score:** Average of scaled questions → Percentage

| Readiness Level | Score | Implication |
|-----------------|-------|-------------|
| **High Readiness** | ≥80% | Proceed with standard change management |
| **Moderate Readiness** | 60-79% | Enhanced communication and support needed |
| **Low Readiness** | 40-59% | Significant intervention required |
| **Not Ready** | <40% | Delay or redesign change approach |

##### 4.7.4.5 Change Readiness Outputs

| Output | Description | Feeds Into |
|--------|-------------|------------|
| **Overall Readiness Score** | Project/programme readiness % | Portfolio Item (status) |
| **Readiness by Dimension** | ADKAR breakdown | Change plan |
| **Readiness by Stakeholder Group** | Where resistance exists | Communication plan |
| **Concern Analysis** | Themes from open text | RIADA (Risks) |
| **Support Needs** | What people need | Project scope |

---

#### 4.7.5 Mode 4: Adoption Evidence Survey

**Purpose:** Measure whether a deployed change is being adopted through process compliance, role behavior, and KPI evidence.

##### 4.7.5.1 Survey Scope

**Linked To:** Portfolio Item (Project or Programme)

**Timing:** Post go-live (2 weeks, 1 month, 3 months, 6 months)

##### 4.7.5.2 Adoption Evidence Framework

| Evidence Type | What It Measures |
|---------------|------------------|
| **Process Evidence** | Is the new process being followed? |
| **Role Evidence** | Are people performing their new roles? |
| **KPI Evidence** | Are metrics improving as expected? |

##### 4.7.5.3 Process Evidence Questions

| # | Question | Response |
|---|----------|----------|
| PE-1 | I follow the new process as documented | Scale 1-5 |
| PE-2 | I use the new system/tool for this process | Scale 1-5 |
| PE-3 | The new process is followed consistently by my team | Scale 1-5 |
| PE-4 | I know where to find the process documentation | Yes/No |
| PE-5 | I have encountered issues following the new process | Yes/No + text |
| PE-6 | The new process is an improvement | Scale 1-5 |

##### 4.7.5.4 Role Evidence Questions

| # | Question | Response |
|---|----------|----------|
| RE-1 | I understand my responsibilities in the new process | Scale 1-5 |
| RE-2 | I have the skills to perform my new role effectively | Scale 1-5 |
| RE-3 | I feel confident performing my new responsibilities | Scale 1-5 |
| RE-4 | I have completed all required training | Yes/No |
| RE-5 | I have access to all systems/tools I need | Yes/No |
| RE-6 | I know who to escalate to when issues arise | Yes/No |

##### 4.7.5.5 KPI Evidence

| # | Evidence | Source |
|---|----------|--------|
| KE-1 | Baseline KPI value | System (from KPI Catalogue) |
| KE-2 | Current KPI value | System (measured) |
| KE-3 | Target KPI value | System (from Project) |
| KE-4 | KPI trend | Calculated (Improving/Stable/Declining) |
| KE-5 | Self-reported improvement | Survey question |
| KE-6 | Attribution to change | Survey question |

##### 4.7.5.6 Adoption Evidence Scoring

```
Adoption Score = (Process Evidence × 40%) + (Role Evidence × 30%) + (KPI Evidence × 30%)
```

| Adoption Level | Score | Implication |
|----------------|-------|-------------|
| **Full Adoption** | ≥85% | Change embedded, monitor |
| **Partial Adoption** | 60-84% | Targeted reinforcement needed |
| **Low Adoption** | 40-59% | Significant intervention required |
| **Failed Adoption** | <40% | Major remediation needed |

##### 4.7.5.7 Adoption Evidence Outputs

| Output | Description | Feeds Into |
|--------|-------------|------------|
| **Adoption Score** | Overall % | Portfolio Item (Benefits status) |
| **Adoption by Process** | Which processes adopted | Process Catalogue |
| **Adoption by Role** | Which roles struggling | Training plans |
| **KPI Movement** | Baseline → Current → Target | Change & Adoption (KPI tracking) |
| **Issue Log** | Adoption blockers | RIADA |

---

#### 4.7.6 Survey Builder Features

##### 4.7.6.1 Survey Configuration

| Feature | Description |
|---------|-------------|
| **Mode Selection** | Choose survey type (AI Fluency, OM, Readiness, Adoption) |
| **Template Library** | Pre-built templates for each mode |
| **Question Customization** | Add/modify/remove questions |
| **Branching Logic** | Show/hide questions based on answers |
| **Process Linking** | Link OM Survey to Process Catalogue entries |
| **Project Linking** | Link Readiness/Adoption to Portfolio Items |
| **Role Assignment** | Auto-assign based on role/process ownership |
| **Scoring Configuration** | Customize weights and thresholds |

##### 4.7.6.2 Survey Distribution

| Feature | Description |
|---------|-------------|
| **Email Invitations** | Personalized invitations with unique links |
| **Reminder Scheduling** | Automated reminders at configurable intervals |
| **Anonymous Option** | Anonymous responses for sensitive surveys |
| **Partial Save** | Save progress and resume later |
| **Mobile Responsive** | Complete on any device |
| **Bulk Import** | Import respondent lists |

##### 4.7.6.3 Survey Scheduling

| Survey Mode | Recommended Frequency |
|-------------|----------------------|
| **AI Fluency** | Annually + Post-training events |
| **Operating Model** | Annually + Pre-major transformation |
| **Change Readiness** | Per project/programme (before kickoff) |
| **Adoption Evidence** | Go-Live +2w, +1m, +3m, +6m |

---

#### 4.7.7 Survey Results & Integration

##### 4.7.7.1 Integration with Other Components

| Survey Mode | Updates Component | How |
|-------------|-------------------|-----|
| **AI Fluency** | Reference Data | Populates Champion list |
| **AI Fluency** | Process Catalogue | AFI by process team |
| **Operating Model** | Process Catalogue | Updates RAG status (S, P, Pr, D) |
| **Operating Model** | Quality Logs | Auto-creates Issues from RED ratings |
| **Change Readiness** | Portfolio | Updates project risk profile |
| **Change Readiness** | Quality Logs | Creates Risks from low readiness |
| **Adoption Evidence** | Change & Adoption | Updates KPI tracking, adoption metrics |
| **Adoption Evidence** | Quality Logs | Creates Issues from adoption blockers |

##### 4.7.7.2 Automated Actions

| Trigger | Action |
|---------|--------|
| Individual AFI ≥61 | Flag as AI Champion candidate |
| Process RED on any dimension | Auto-create RIADA Issue |
| Change Readiness <60% | Auto-create RIADA Risk on project |
| Adoption <60% at +3 months | Alert Change Manager, create Action |
| KPI not trending to target | Create Issue, notify Process Owner |

##### 4.7.7.3 Reporting & Dashboards

| Report | Description |
|--------|-------------|
| **AI Fluency Dashboard** | AFI distribution by role, process, trend |
| **Operating Model Heatmap** | RAG matrix by process × dimension |
| **Change Readiness Report** | ADKAR breakdown, stakeholder analysis |
| **Adoption Tracker** | Adoption scores over time, by process/role |
| **Survey Response Rates** | Completion tracking |
| **Trend Analysis** | Compare survey results over time |

---

#### 4.7.8 Survey Data Model

##### SurveyTemplate

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier |
| `organization_id` | UUID | Tenant reference |
| `mode` | ENUM | 'ai_fluency', 'operating_model', 'change_readiness', 'adoption_evidence' |
| `name` | VARCHAR(255) | Template name |
| `description` | TEXT | Description |
| `questions` | JSONB | Question definitions |
| `scoring_config` | JSONB | Scoring rules and weights |
| `status` | ENUM | 'draft', 'active', 'archived' |
| `created_at` | TIMESTAMP | |

##### SurveyInstance

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier |
| `template_id` | UUID | FK → SurveyTemplate |
| `name` | VARCHAR(255) | Instance name (e.g., "Q1 2026 AI Fluency") |
| `linked_entity_type` | VARCHAR(50) | 'process', 'portfolio_item', 'organization' |
| `linked_entity_id` | UUID | ID of linked entity |
| `status` | ENUM | 'draft', 'open', 'closed' |
| `open_date` | TIMESTAMP | When survey opens |
| `close_date` | TIMESTAMP | When survey closes |
| `created_at` | TIMESTAMP | |

##### SurveyRespondent

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier |
| `survey_instance_id` | UUID | FK → SurveyInstance |
| `user_id` | UUID | FK → User |
| `process_id` | UUID | FK → Process (for OM survey) |
| `status` | ENUM | 'pending', 'in_progress', 'completed' |
| `invited_at` | TIMESTAMP | |
| `completed_at` | TIMESTAMP | |

##### SurveyResponse

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier |
| `respondent_id` | UUID | FK → SurveyRespondent |
| `responses` | JSONB | Question ID → Answer |
| `scores` | JSONB | Calculated scores (AFI, Readiness, etc.) |
| `submitted_at` | TIMESTAMP | |

##### SurveyResult (Aggregated)

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier |
| `survey_instance_id` | UUID | FK → SurveyInstance |
| `dimension` | VARCHAR(50) | 'overall', 'system', 'people', 'process', 'data', 'role', etc. |
| `entity_type` | VARCHAR(50) | 'organization', 'process', 'role', 'user' |
| `entity_id` | UUID | ID of entity |
| `score` | DECIMAL | Calculated score |
| `rag_status` | ENUM | 'green', 'amber', 'red' (for OM) |
| `calculated_at` | TIMESTAMP | |

The system maintains reference data catalogues with lifecycle status tracking.

### 5.1 Lifecycle Status Values

All catalogue entries have a status:

| Status | Description |
|--------|-------------|
| **Evaluate** | Under assessment for adoption |
| **Maintain** | Active and stable |
| **Optimize** | Active but undergoing improvement |
| **Retire** | Being phased out |

### 5.2 Reference Catalogues

| Catalogue | Description | Example Entries |
|-----------|-------------|-----------------|
| **Role Catalogue** | Operational and project roles | Account Manager, QA Inspector, Data Analyst |
| **Agent Catalogue** | AI/Automation agents | Order Processing Bot, Data Validation Agent |
| **System Catalogue** | Technology platforms and tools | ERP, SharePoint, Client Portals |
| **KPI Catalogue** | All available metrics | Cycle Time, Error Rate, On-Time Delivery |
| **Supplier Catalogue** | Vendor base | Factory suppliers in China, Vietnam |
| **Client Catalogue** | Customer base | Bunnings, Selco, Maxeda |
| **Market Catalogue** | Trading and sourcing markets | UK, Benelux, Australia, China, Vietnam |
| **Category Catalogue** | Product categories | Technical, Showroom, Seasonal, Home |
| **Partner Catalogue** | Key partners | 3PL providers, Testing labs, Audit firms |

### 5.3 Catalogue Entity Model

| Field | Description |
|-------|-------------|
| ID | Unique identifier |
| Name | Display name |
| Description | Detailed description |
| Type | Catalogue type |
| Status | Evaluate / Maintain / Optimize / Retire |
| Owner | Responsible person |
| Created Date | When created |
| Updated Date | Last update |
| Linked Items | References to processes, projects, etc. |

---

## 6. Global Platform Requirements

These requirements apply across the entire platform, not specific to any single component.

### 6.1 Multi-Tenant Architecture

**Requirement:** Organization-based data isolation with shared infrastructure.

#### 6.1.1 Tenant Model

```
Platform Infrastructure (Shared)
├── Organization A (Tenant)
│   ├── Users & Roles
│   ├── Portfolios
│   ├── Business Models
│   ├── Process Catalogues
│   ├── Quality Logs
│   ├── Operating Model Designs
│   └── Change & Adoption Data
├── Organization B (Tenant)
│   └── ... (completely isolated data)
└── Organization C (Tenant)
    └── ... (completely isolated data)
```

#### 6.1.2 Data Isolation Requirements

| Requirement | Description |
|-------------|-------------|
| **Complete Isolation** | No data leakage between tenants |
| **Tenant-Scoped Queries** | All queries automatically filtered by organization |
| **Separate Encryption Keys** | Each tenant's data encrypted with unique keys |
| **Audit Logging** | Tenant-specific audit trails |
| **Backup & Recovery** | Per-tenant backup and restore capabilities |

#### 6.1.3 Shared Infrastructure Components

| Component | Shared | Tenant-Specific |
|-----------|--------|-----------------|
| Application Code | ✓ | |
| Database Schema | ✓ | |
| Data | | ✓ |
| User Accounts | | ✓ |
| Configuration | | ✓ |
| File Storage | ✓ (isolated containers) | ✓ (data) |
| API Endpoints | ✓ | |

#### 6.1.4 Organization Entity Model

| Field | Description |
|-------|-------------|
| ID | Unique identifier (UUID) |
| Name | Organization name |
| Slug | URL-friendly identifier |
| Subscription Tier | Free / Pro / Enterprise |
| Created Date | When onboarded |
| Settings | Organization-specific configuration |
| Branding | Logo, colors (if applicable) |
| Data Region | Geographic location of data storage |

### 6.2 Authentication & Authorization

**Requirement:** Passwordless email-based authentication with domain-restricted access per organization.

#### 6.2.1 Authentication Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         PASSWORDLESS AUTHENTICATION FLOW                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐                  │
│  │    User      │      │   System     │      │   Email      │                  │
│  │              │      │              │      │   Provider   │                  │
│  └──────┬───────┘      └──────┬───────┘      └──────┬───────┘                  │
│         │                     │                     │                           │
│         │  1. Enter email     │                     │                           │
│         │────────────────────►│                     │                           │
│         │                     │                     │                           │
│         │                     │  2. Validate domain │                           │
│         │                     │     against org     │                           │
│         │                     │                     │                           │
│         │                     │  3. Generate magic  │                           │
│         │                     │     link token      │                           │
│         │                     │                     │                           │
│         │                     │  4. Send email      │                           │
│         │                     │────────────────────►│                           │
│         │                     │                     │                           │
│         │  5. Receive email with login link         │                           │
│         │◄──────────────────────────────────────────│                           │
│         │                     │                     │                           │
│         │  6. Click link      │                     │                           │
│         │────────────────────►│                     │                           │
│         │                     │                     │                           │
│         │                     │  7. Validate token  │                           │
│         │                     │     (not expired,   │                           │
│         │                     │     not used)       │                           │
│         │                     │                     │                           │
│         │  8. Create session  │                     │                           │
│         │◄────────────────────│                     │                           │
│         │                     │                     │                           │
│         │  9. Redirect to     │                     │                           │
│         │     dashboard       │                     │                           │
│         │                     │                     │                           │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### 6.2.2 Passwordless (Magic Link) Authentication

**No passwords are stored or required.** Users authenticate via email-only magic links.

| Step | Action | Details |
|------|--------|---------|
| 1 | **User enters email** | On login page, user enters their work email |
| 2 | **Domain validation** | System checks email domain against registered organization domains |
| 3 | **Token generation** | System generates a secure, single-use magic link token |
| 4 | **Email sent** | System sends email with login link to user |
| 5 | **User clicks link** | User clicks link in email (valid for 15 minutes) |
| 6 | **Token validation** | System validates token is unused and not expired |
| 7 | **Session created** | System creates authenticated session |
| 8 | **Redirect** | User redirected to dashboard |

**Magic Link Characteristics:**

| Property | Value | Rationale |
|----------|-------|-----------|
| **Token Length** | 64 characters | Cryptographically secure |
| **Expiry** | 15 minutes | Balance security vs. convenience |
| **Single Use** | Yes | Prevent replay attacks |
| **Rate Limit** | 5 per hour per email | Prevent abuse |
| **Cooldown** | 60 seconds between requests | Prevent spam |

**Email Template:**

```
Subject: Your Process Catalogue Login Link

Hi {user_name},

Click the link below to sign in to Process Catalogue:

[Sign In to Process Catalogue]
{magic_link_url}

This link will expire in 15 minutes and can only be used once.

If you didn't request this link, you can safely ignore this email.

---
Process Catalogue
{organization_name}
```

#### 6.2.3 Domain-Restricted Access

**Key Principle:** Users can only access organizations that have registered their email domain.

##### Organization Domain Registration

Each organization registers one or more allowed email domains:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `organization_id` | UUID | Organization reference | `org_123` |
| `domain` | VARCHAR(255) | Email domain (lowercase) | `surity.co` |
| `is_primary` | BOOLEAN | Primary domain for org | `true` |
| `verification_status` | ENUM | Domain ownership verified | `verified`, `pending`, `failed` |
| `verified_at` | TIMESTAMP | When verified | `2026-01-15` |
| `created_at` | TIMESTAMP | When added | `2026-01-01` |

**Example Organization Setup:**

```
Organization: Surity
├── Primary Domain: surity.co
├── Additional Domains: surity.com, surity.com.au
│
├── Allowed Users:
│   ├── ralph.behnke@surity.co ✓
│   ├── jane.smith@surity.com ✓
│   └── tom.jones@surity.com.au ✓
│
└── Blocked Users:
    ├── ralph@gmail.com ✗ (personal email)
    ├── jane@outlook.com ✗ (personal email)
    └── attacker@malicious.com ✗ (unknown domain)
```

##### Domain Validation Rules

| Rule | Behavior |
|------|----------|
| **Exact match required** | `surity.co` does NOT match `notsurity.co` |
| **Case insensitive** | `Surity.CO` matches `surity.co` |
| **No subdomain matching** | `mail.surity.co` does NOT match `surity.co` (unless explicitly added) |
| **Multiple orgs per domain** | NOT allowed - each domain maps to exactly one org |
| **Multiple domains per org** | Allowed - org can have many domains |

##### Domain Verification Process

To prevent unauthorized domain claims, organizations must verify domain ownership:

| Method | Description | Use Case |
|--------|-------------|----------|
| **DNS TXT Record** | Add TXT record with verification code | Recommended |
| **Admin Email** | Send verification to admin@domain.com | Fallback |
| **Manual Verification** | Platform admin verifies (Enterprise only) | Special cases |

**DNS Verification Example:**

```
1. Organization requests domain: surity.co
2. System generates verification code: pc-verify=abc123xyz
3. Organization adds DNS TXT record:
   surity.co TXT "pc-verify=abc123xyz"
4. System checks DNS and marks domain as verified
```

#### 6.2.4 User Registration Flow

##### Self-Registration (if enabled)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           USER SELF-REGISTRATION FLOW                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  1. User visits: app.processcatalogue.com/register                              │
│                                                                                  │
│  2. User enters work email: ralph.behnke@surity.co                              │
│                                                                                  │
│  3. System extracts domain: surity.co                                           │
│                                                                                  │
│  4. System looks up domain:                                                      │
│     ├── Found: surity.co → Organization: Surity                                 │
│     └── Not Found: "Your organization is not registered. Contact admin."        │
│                                                                                  │
│  5. If found, check organization settings:                                       │
│     ├── self_registration_enabled: true → Continue                              │
│     └── self_registration_enabled: false → "Contact your admin for access."    │
│                                                                                  │
│  6. System sends magic link to email                                            │
│                                                                                  │
│  7. User clicks link, completes profile:                                        │
│     ├── Name (required)                                                         │
│     ├── Job Title (optional)                                                    │
│     └── Department (optional)                                                   │
│                                                                                  │
│  8. User assigned default role (e.g., "Viewer")                                 │
│                                                                                  │
│  9. Admin notified of new user registration                                     │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

##### Admin-Invited Registration

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          ADMIN-INVITED REGISTRATION FLOW                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  1. Admin navigates to: Settings → Users → Invite User                          │
│                                                                                  │
│  2. Admin enters:                                                                │
│     ├── Email: jane.smith@surity.co                                             │
│     ├── Role: Process Owner                                                     │
│     └── Send welcome email: ✓                                                   │
│                                                                                  │
│  3. System validates email domain matches organization                          │
│                                                                                  │
│  4. System creates user record (status: pending)                                │
│                                                                                  │
│  5. System sends invitation email with magic link                               │
│                                                                                  │
│  6. User clicks link, completes profile                                         │
│                                                                                  │
│  7. User status updated to: active                                              │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

##### Bulk User Import

For enterprise onboarding, admins can import users via CSV:

| Column | Required | Description |
|--------|----------|-------------|
| `email` | Yes | User's work email |
| `name` | Yes | Display name |
| `role` | No | Role to assign (default: Viewer) |
| `department` | No | Department name |
| `job_title` | No | Job title |
| `send_invite` | No | Send invitation email (default: true) |

**Import Validation:**
- All emails must match organization's registered domains
- Duplicate emails are skipped
- Invalid emails are flagged with errors
- Import summary shows success/failure counts

#### 6.2.5 Organization Registration Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `self_registration_enabled` | BOOLEAN | `false` | Allow users to self-register |
| `default_role_id` | UUID | Viewer | Role assigned to self-registered users |
| `require_admin_approval` | BOOLEAN | `true` | Require admin approval for self-registration |
| `allowed_domains` | ARRAY | [] | List of allowed email domains |
| `magic_link_expiry_minutes` | INTEGER | 15 | Magic link validity period |
| `session_timeout_hours` | INTEGER | 24 | Session duration |
| `max_sessions_per_user` | INTEGER | 5 | Maximum concurrent sessions |
| `require_mfa` | BOOLEAN | `false` | Require MFA (Enterprise only) |

#### 6.2.6 Authorization Model

##### Role-Based Access Control (RBAC)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AUTHORIZATION MODEL                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  User ─────► UserRole ─────► Role ─────► Permission                             │
│                │                                                                 │
│                │ (optional scope)                                               │
│                ▼                                                                 │
│           ScopeType: organization | process | project                           │
│           ScopeId:   {entity_id}                                                │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

##### Default Roles

| Role | Description | Typical Permissions |
|------|-------------|---------------------|
| **Super Admin** | Platform administrator | All permissions |
| **Organization Admin** | Organization administrator | Manage users, settings, all data |
| **Process Owner** | Owns and manages processes | Full control on owned processes |
| **Project Manager** | Manages portfolio items | Full control on assigned projects |
| **Contributor** | Can edit assigned items | Edit where assigned in RACI |
| **Viewer** | Read-only access | View all, edit nothing |

##### Permission Categories

| Category | Permissions |
|----------|-------------|
| **Process** | `process:view`, `process:create`, `process:edit`, `process:delete`, `process:publish` |
| **Business Model** | `bm:view`, `bm:create`, `bm:edit`, `bm:delete` |
| **RIADA** | `riada:view`, `riada:create`, `riada:edit`, `riada:delete`, `riada:assign` |
| **Portfolio** | `portfolio:view`, `portfolio:create`, `portfolio:edit`, `portfolio:delete` |
| **Survey** | `survey:view`, `survey:create`, `survey:respond`, `survey:view_results` |
| **Reports** | `report:view`, `report:create`, `report:export` |
| **Admin** | `admin:users`, `admin:roles`, `admin:settings`, `admin:audit` |
| **LLM** | `llm:use`, `llm:configure`, `llm:view_usage` |

##### Scoped Permissions

Permissions can be scoped to specific entities:

| Scope Type | Example | Effect |
|------------|---------|--------|
| **Organization** | User has `process:edit` at org level | Can edit ALL processes in org |
| **Process** | User has `process:edit` for L1-05 | Can edit L1-05 and all children |
| **Project** | User has `portfolio:edit` for PRJ-001 | Can edit PRJ-001 and children |

**Example Scoped Permission:**

```
User: jane.smith@surity.co
Roles:
├── Viewer (organization scope) - Can view everything
├── Process Owner (scoped to L1-05) - Full control on "Range Confirmation"
└── Project Manager (scoped to PRJ-2026-042) - Full control on "Order Automation"
```

#### 6.2.7 Session Management

| Feature | Description |
|---------|-------------|
| **Session Token** | JWT with 24-hour expiry (configurable) |
| **Refresh Token** | 30-day refresh token for seamless re-auth |
| **Session Storage** | HttpOnly, Secure, SameSite cookies |
| **Concurrent Sessions** | Default 5 per user (configurable) |
| **Session Termination** | Logout terminates current session |
| **Force Logout** | Admin can terminate all user sessions |
| **Activity Timeout** | Optional inactivity timeout (Enterprise) |

#### 6.2.8 Security Controls

| Control | Implementation |
|---------|----------------|
| **Rate Limiting** | 5 magic link requests per hour per email |
| **Brute Force Protection** | Exponential backoff on failed attempts |
| **IP Logging** | Log IP address of all auth attempts |
| **Suspicious Activity** | Alert admin on unusual login patterns |
| **Audit Trail** | Log all auth events (login, logout, failed) |
| **Token Revocation** | Ability to revoke all tokens for a user |

#### 6.2.9 Authentication Data Model

##### OrganizationDomain

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | Parent organization |
| `domain` | VARCHAR(255) | NOT NULL, UNIQUE | Email domain (lowercase) |
| `is_primary` | BOOLEAN | DEFAULT false | Primary domain flag |
| `verification_status` | ENUM | NOT NULL | 'pending', 'verified', 'failed' |
| `verification_code` | VARCHAR(100) | | DNS verification code |
| `verified_at` | TIMESTAMP | | When verified |
| `created_at` | TIMESTAMP | NOT NULL | |

##### MagicLinkToken

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `email` | VARCHAR(255) | NOT NULL | User email |
| `token_hash` | VARCHAR(255) | NOT NULL, UNIQUE | Hashed token (never store plaintext) |
| `expires_at` | TIMESTAMP | NOT NULL | Expiry time (15 min default) |
| `used_at` | TIMESTAMP | | When used (NULL if unused) |
| `ip_address` | VARCHAR(50) | | Request IP |
| `user_agent` | VARCHAR(500) | | Browser/client |
| `created_at` | TIMESTAMP | NOT NULL | |

##### UserSession

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `user_id` | UUID | FK → User | User reference |
| `token_hash` | VARCHAR(255) | NOT NULL, UNIQUE | Hashed session token |
| `refresh_token_hash` | VARCHAR(255) | UNIQUE | Hashed refresh token |
| `expires_at` | TIMESTAMP | NOT NULL | Session expiry |
| `refresh_expires_at` | TIMESTAMP | | Refresh token expiry |
| `ip_address` | VARCHAR(50) | | Session IP |
| `user_agent` | VARCHAR(500) | | Browser/client |
| `last_active_at` | TIMESTAMP | | Last activity |
| `created_at` | TIMESTAMP | NOT NULL | |

##### AuthAuditLog

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | Organization (if known) |
| `user_id` | UUID | FK → User | User (if known) |
| `email` | VARCHAR(255) | | Email attempted |
| `event_type` | ENUM | NOT NULL | See event types below |
| `success` | BOOLEAN | NOT NULL | Whether event succeeded |
| `ip_address` | VARCHAR(50) | | Request IP |
| `user_agent` | VARCHAR(500) | | Browser/client |
| `metadata` | JSONB | | Additional context |
| `created_at` | TIMESTAMP | NOT NULL | |

**Event Types:**
- `magic_link_requested`
- `magic_link_sent`
- `magic_link_clicked`
- `magic_link_expired`
- `magic_link_invalid`
- `login_success`
- `login_failed`
- `logout`
- `session_expired`
- `session_revoked`
- `user_registered`
- `user_invited`
- `password_not_applicable` (logged if someone tries password auth)

#### 6.2.10 API Endpoints

##### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/magic-link` | Request magic link | No |
| GET | `/api/v1/auth/verify/{token}` | Verify magic link and login | No |
| POST | `/api/v1/auth/refresh` | Refresh session token | Yes (refresh token) |
| POST | `/api/v1/auth/logout` | Logout current session | Yes |
| POST | `/api/v1/auth/logout-all` | Logout all sessions | Yes |
| GET | `/api/v1/auth/me` | Get current user info | Yes |
| GET | `/api/v1/auth/sessions` | List active sessions | Yes |
| DELETE | `/api/v1/auth/sessions/{id}` | Terminate specific session | Yes |

##### User Management Endpoints (Admin)

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/v1/users` | List users | `admin:users` |
| POST | `/api/v1/users/invite` | Invite user | `admin:users` |
| POST | `/api/v1/users/import` | Bulk import users | `admin:users` |
| GET | `/api/v1/users/{id}` | Get user details | `admin:users` |
| PUT | `/api/v1/users/{id}` | Update user | `admin:users` |
| DELETE | `/api/v1/users/{id}` | Deactivate user | `admin:users` |
| POST | `/api/v1/users/{id}/roles` | Assign role | `admin:users` |
| DELETE | `/api/v1/users/{id}/roles/{role_id}` | Remove role | `admin:users` |

##### Domain Management Endpoints (Admin)

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/v1/domains` | List organization domains | `admin:settings` |
| POST | `/api/v1/domains` | Add domain | `admin:settings` |
| GET | `/api/v1/domains/{id}/verify` | Get verification instructions | `admin:settings` |
| POST | `/api/v1/domains/{id}/verify` | Check domain verification | `admin:settings` |
| DELETE | `/api/v1/domains/{id}` | Remove domain | `admin:settings` |

#### 6.2.11 China Deployment Considerations

| Aspect | Global | China |
|--------|--------|-------|
| **Auth Provider** | Supabase Auth | Alibaba IDaaS |
| **Email Delivery** | SendGrid / Resend | Alibaba DirectMail |
| **Session Storage** | Supabase | ApsaraDB Redis |
| **MFA (Enterprise)** | Authenticator apps | Alibaba Cloud MFA |

**China-Specific Requirements:**
- All authentication data stored in China region
- Magic link emails sent via Alibaba DirectMail
- ICP compliance for domain verification
- SMS verification option (common in China)

### 6.3 GitHub Integration

**Requirement:** Repository connection with automated commits and sync capabilities for development workflow tracking.

#### 6.4.1 Integration Capabilities

| Capability | Description |
|------------|-------------|
| **Repository Connection** | Link GitHub repos to Projects/Workstreams |
| **Commit Tracking** | View commits associated with work packages |
| **Branch Management** | Track feature branches per work item |
| **Pull Request Sync** | Link PRs to RIADA items and work packages |
| **Automated Updates** | Sync status based on GitHub events |
| **Code Review Tracking** | Track review status and approvals |

#### 6.4.2 GitHub Entity Mappings

| Process Catalogue Entity | GitHub Entity |
|--------------------------|---------------|
| Project | Repository |
| Workstream | Branch prefix / Label |
| Work Package | Issue / PR |
| Action (RIADA) | Issue |
| Developer Resource | Contributor |

#### 6.2.3 Webhook Events

| GitHub Event | Platform Action |
|--------------|-----------------|
| `push` | Update work package with commit reference |
| `pull_request.opened` | Create/link work package |
| `pull_request.merged` | Update work package status to Complete |
| `pull_request.closed` | Update work package status |
| `issues.opened` | Create linked Action in RIADA |
| `issues.closed` | Update Action status to Resolved |

#### 6.2.4 Bidirectional Sync

```
Process Catalogue                    GitHub
─────────────────                    ──────
Work Package Created    ──────►      Issue Created
                        ◄──────      Issue Closed
Action (RIADA) Created  ──────►      Issue Created (label: RIADA)
                        ◄──────      Commit pushed
Status Updated          ◄──────      PR Merged
```

#### 6.2.5 GitHub Integration Entity Model

| Field | Description |
|-------|-------------|
| ID | Internal reference |
| Organization ID | Tenant reference |
| GitHub Org | GitHub organization name |
| Repository | Repository name |
| Access Token | Encrypted OAuth token |
| Webhook Secret | Encrypted webhook secret |
| Linked Project | Project ID in Process Catalogue |
| Sync Enabled | Boolean |
| Last Sync | Timestamp |

### 6.4 LLM Integration

**Requirement:** Connect to Large Language Models (LLMs) to execute prompts against catalogue data, run prompts from the Prompt Library, and optionally save or discard responses.

#### 6.4.1 LLM Integration Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         LLM INTEGRATION ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                        PROCESS CATALOGUE DATA                            │    │
│  │  • Processes (L0-L5)           • RIADA Items                            │    │
│  │  • Operating Model (RACI, KPIs) • Portfolio/Projects                    │    │
│  │  • Business Model               • Survey Results                        │    │
│  │  • Reference Catalogues         • Audit History                         │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                         CONTEXT ASSEMBLY                                 │    │
│  │  • Universal Context (auto-populated from current process/entity)       │    │
│  │  • User Personalization (role, preferences)                             │    │
│  │  • Additional Context (user-selected data: metrics, issues, goals)      │    │
│  │  • Prompt Template (from Prompt Library or ad-hoc)                      │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                         LLM GATEWAY                                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │    │
│  │  │  OpenAI     │  │  Anthropic  │  │  Alibaba    │  │  Self-      │    │    │
│  │  │  GPT-4      │  │  Claude     │  │  Qwen       │  │  Hosted     │    │    │
│  │  │  (Global)   │  │  (Global)   │  │  (China)    │  │  (Optional) │    │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                         RESPONSE HANDLING                                │    │
│  │  ┌───────────────────┐     ┌───────────────────┐                        │    │
│  │  │  SAVE RESPONSE    │     │  DISCARD RESPONSE │                        │    │
│  │  │  • Store in DB    │     │  • View only      │                        │    │
│  │  │  • Link to entity │     │  • No persistence │                        │    │
│  │  │  • Version history│     │  • Regenerate     │                        │    │
│  │  │  • Rate & feedback│     │                   │                        │    │
│  │  └───────────────────┘     └───────────────────┘                        │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### 6.4.2 Supported LLM Providers

| Provider | Models | Region | Use Case |
|----------|--------|--------|----------|
| **OpenAI** | GPT-4, GPT-4-Turbo, GPT-3.5-Turbo | Global | Primary for non-China deployments |
| **Anthropic** | Claude 3 Opus, Sonnet, Haiku | Global | Alternative, strong reasoning |
| **Alibaba Cloud** | Qwen-Max, Qwen-Plus, Qwen-Turbo | China | Required for China deployment |
| **Azure OpenAI** | GPT-4, GPT-3.5 | Global/China | Enterprise compliance option |
| **Self-Hosted** | Llama, Mistral, custom | Any | Air-gapped/custom deployments |

#### 6.4.3 LLM Configuration (Per Tenant)

| Setting | Description | Options |
|---------|-------------|---------|
| **Primary Provider** | Default LLM provider | OpenAI, Anthropic, Qwen, Azure, Self-Hosted |
| **Primary Model** | Default model | Provider-specific model list |
| **Fallback Provider** | Backup if primary fails | Same options |
| **API Key** | Encrypted API credentials | Tenant-specific, encrypted at rest |
| **Endpoint URL** | Custom endpoint (self-hosted) | URL or null for cloud |
| **Default Temperature** | Creativity setting | 0.0 - 1.0 (default: 0.7) |
| **Max Tokens** | Response length limit | 1000 - 32000 |
| **Rate Limit** | Requests per minute | Configurable per tenant |
| **Cost Tracking** | Track token usage | Enabled/Disabled |
| **Data Retention** | How long to keep responses | 30/90/365 days / Forever |

#### 6.4.4 Prompt Execution Modes

**Mode 1: Ad-Hoc Query (Chat Interface)**

Users can ask questions directly against catalogue data:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  AI ASSISTANT                                                          [─][□][×]│
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  Context: L2-25 Silver Seal Process                              [Change ▼]    │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ User: What are the main issues with this process and how might we      │   │
│  │       improve it based on the RIADA data?                              │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ Assistant: Based on the RIADA data for the Silver Seal Process, I can  │   │
│  │ see 3 open issues:                                                      │   │
│  │                                                                          │   │
│  │ 1. **Sample submission delays** (High severity, System category)        │   │
│  │    - Root cause: Manual data entry into legacy system                   │   │
│  │    - Recommendation: Automate sample tracking with barcode scanning    │   │
│  │                                                                          │   │
│  │ 2. **Inconsistent review criteria** (Medium severity, Process category) │   │
│  │    - Root cause: Undocumented review standards                          │   │
│  │    - Recommendation: Create standardized review checklist               │   │
│  │ ...                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  [💾 Save Response]  [📋 Copy]  [🔄 Regenerate]  [👎 Discard]                   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ Ask a follow-up question...                                      [Send] │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Mode 2: Prompt Library Execution**

Run pre-defined prompts from the library:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  RUN PROMPT                                                            [─][□][×]│
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  Selected Prompt: [Generate Process Documentation        ▼]                     │
│  Target: L2-25 Silver Seal Process                                              │
│                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────  │
│  CONTEXT SUMMARY (Auto-populated)                                               │
│  ─────────────────────────────────────────────────────────────────────────────  │
│  Process: Silver Seal Process (L2-25)                                           │
│  Hierarchy: SOURCE → Product Development → Silver Seal                          │
│  RACI: R=QA Technician, A=QA Manager, C=Merchandiser, I=Account Manager        │
│  KPIs: Sample Pass Rate (Target: 95%, Current: 87%)                            │
│  Open Issues: 3 | Open Risks: 1                                                 │
│  Systems: QMS, Sample Tracking System                                           │
│                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────  │
│  ADDITIONAL CONTEXT (Optional)                                     [Expand ▼]  │
│  ─────────────────────────────────────────────────────────────────────────────  │
│                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────  │
│  OPTIONS                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────  │
│  Model: [GPT-4 ▼]  Temperature: [0.7]  Max Length: [2000 tokens]               │
│  ☑ Include RIADA details   ☑ Include KPI data   ☐ Include full RACI           │
│                                                                                  │
│  [Preview Full Prompt]           [▶ Run Prompt]           [Cancel]              │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Mode 3: Batch Execution**

Run prompts against multiple processes:

| Feature | Description |
|---------|-------------|
| **Select Multiple Processes** | Choose processes via canvas selection or filter |
| **Apply Same Prompt** | Run identical prompt against each |
| **Background Processing** | Queue for async execution |
| **Results Summary** | View all results in table format |
| **Bulk Save/Discard** | Save all, discard all, or selective |

#### 6.4.5 Data Access for LLM Context

The LLM can access the following data (respecting user permissions):

| Data Category | What's Included | Access Control |
|---------------|-----------------|----------------|
| **Process Data** | Name, description, level, hierarchy, type, status | User's viewable processes |
| **Operating Model** | RACI, KPIs, policies, systems, timing, governance | User's viewable processes |
| **RIADA** | Risks, issues, actions, dependencies, assumptions | User's viewable items |
| **Business Model** | Canvas components, mappings | User's org only |
| **Portfolio** | Projects, milestones, budget (summary) | User's viewable projects |
| **Survey Results** | Aggregated scores (not individual responses) | User's viewable surveys |
| **Reference Data** | Roles, systems, clients, markets, categories | User's org only |
| **Audit History** | Recent changes (sanitized) | User's viewable entities |

**Data NOT Accessible:**
- Other tenants' data (absolute isolation)
- Individual survey responses (privacy)
- API keys, passwords, secrets
- User PII beyond name/role
- Financial details beyond summary
- Data user doesn't have permission to view

#### 6.4.6 Response Handling

**Save Response:**

| Action | Description |
|--------|-------------|
| **Save to History** | Store in PromptExecution table |
| **Link to Entity** | Associate with process, project, or RIADA item |
| **Add Rating** | 1-5 star rating |
| **Add Feedback** | Text feedback for improvement |
| **Mark as Favorite** | Quick access later |
| **Apply to Content** | Use response to update process description, SOM, etc. |
| **Export** | Download as DOCX, PDF, Markdown |
| **Share** | Share link with colleagues |

**Discard Response:**

| Action | Description |
|--------|-------------|
| **View Only** | Response displayed but not persisted |
| **Regenerate** | Try again with same or modified parameters |
| **Modify & Retry** | Adjust prompt/context and re-run |
| **Close** | Dismiss without saving |

**Note:** Even discarded responses may be logged for usage tracking (token count, timestamp) without storing the actual content, for billing/quota purposes.

#### 6.4.7 Conversation Memory

For multi-turn conversations in ad-hoc mode:

| Feature | Description |
|---------|-------------|
| **Session Context** | Maintain context within a session |
| **Follow-up Questions** | Ask follow-ups without repeating context |
| **Context Window** | Last N messages included (configurable) |
| **Save Conversation** | Save entire conversation thread |
| **Resume Later** | Return to previous conversation |
| **Clear Context** | Start fresh within same session |

#### 6.4.8 LLM Entry Points (UI)

| Location | Access Method | Default Behavior |
|----------|---------------|------------------|
| **Global** | Cmd/Ctrl + K → "Ask AI..." | Ad-hoc query, no context |
| **Process Detail** | "AI Assist" button | Context = current process |
| **Process Canvas** | Right-click → "Ask AI about..." | Context = selected process |
| **RIADA Item** | "Suggest Resolution" button | Context = RIADA item + linked process |
| **Project Detail** | "AI Assist" button | Context = project + linked processes |
| **Operating Model Editor** | "Generate with AI" per section | Context = process + OM component |
| **Prompt Library** | "Run" button on any prompt | Context = selected target |
| **Report Builder** | "AI Summary" option | Context = report scope |
| **Sidebar** | Persistent AI chat panel (optional) | Maintains session |

#### 6.4.9 LLM Usage Controls

| Control | Description |
|---------|-------------|
| **Enable/Disable** | Tenant-level toggle for AI features |
| **Role Restrictions** | Limit AI access to specific roles |
| **Usage Quotas** | Monthly token/request limits per user or org |
| **Cost Alerts** | Notify admins when thresholds reached |
| **Audit Logging** | Log all AI interactions (prompt + response) |
| **Content Filtering** | Block sensitive data from being sent to LLM |
| **Approval Workflow** | Require approval before saving AI-generated content |

#### 6.4.10 China Deployment Considerations

| Requirement | Solution |
|-------------|----------|
| **Data Residency** | Use Alibaba Cloud Qwen; data stays in China |
| **API Compliance** | Qwen API compliant with China regulations |
| **No Cross-Border** | LLM calls don't leave China region |
| **Fallback** | If Qwen unavailable, queue for retry (no external fallback) |
| **Content Moderation** | Additional content filtering for compliance |

#### 6.4.11 LLM Integration Data Model

**LLMConfiguration (Per Tenant)**

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier |
| `organization_id` | UUID | FK → Organization |
| `provider` | ENUM | 'openai', 'anthropic', 'qwen', 'azure', 'self_hosted' |
| `model` | VARCHAR(100) | Model identifier |
| `api_key_encrypted` | TEXT | Encrypted API key |
| `endpoint_url` | VARCHAR(500) | Custom endpoint (nullable) |
| `default_temperature` | DECIMAL | Default temperature (0.0-1.0) |
| `default_max_tokens` | INTEGER | Default max tokens |
| `rate_limit_rpm` | INTEGER | Requests per minute limit |
| `monthly_token_limit` | BIGINT | Monthly token quota |
| `is_enabled` | BOOLEAN | Feature enabled |
| `created_at` | TIMESTAMP | |
| `updated_at` | TIMESTAMP | |

**LLMUsage (Tracking)**

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier |
| `organization_id` | UUID | FK → Organization |
| `user_id` | UUID | FK → User |
| `provider` | VARCHAR(50) | Provider used |
| `model` | VARCHAR(100) | Model used |
| `prompt_tokens` | INTEGER | Input tokens |
| `completion_tokens` | INTEGER | Output tokens |
| `total_tokens` | INTEGER | Total tokens |
| `estimated_cost` | DECIMAL | Estimated cost (USD) |
| `execution_id` | UUID | FK → PromptExecution (nullable) |
| `created_at` | TIMESTAMP | |

**Conversation (For Multi-Turn)**

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier |
| `organization_id` | UUID | FK → Organization |
| `user_id` | UUID | FK → User |
| `title` | VARCHAR(255) | Conversation title (auto-generated or user-set) |
| `context_entity_type` | VARCHAR(50) | 'process', 'project', 'riada_item', etc. |
| `context_entity_id` | UUID | ID of context entity |
| `status` | ENUM | 'active', 'archived' |
| `created_at` | TIMESTAMP | |
| `updated_at` | TIMESTAMP | |

**ConversationMessage**

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier |
| `conversation_id` | UUID | FK → Conversation |
| `role` | ENUM | 'user', 'assistant', 'system' |
| `content` | TEXT | Message content |
| `tokens` | INTEGER | Token count |
| `created_at` | TIMESTAMP | |

### 6.4 Role-Based Access Control (RBAC)

**Requirement:** Fine-grained permissions based on organizational role and component access.

#### 6.4.1 Permission Model

| Level | Description |
|-------|-------------|
| **Organization** | Access to tenant |
| **Component** | Access to specific component (BM, PC, QL, OM, PR, CA) |
| **Entity** | CRUD permissions on entities |
| **Field** | View/Edit permissions on specific fields |

#### 6.4.2 Standard Roles

| Role | Description | Typical Permissions |
|------|-------------|---------------------|
| **Admin** | Organization administrator | Full access to all components |
| **Portfolio Manager** | Manages portfolios and projects | Full Portfolio Response, Read others |
| **Process Owner** | Owns process definitions | Full Process Catalogue (owned), Read others |
| **Business Analyst** | Documents and analyzes | Edit Process Catalogue, Operating Model |
| **Project Manager** | Manages projects | Full Portfolio Response (owned projects) |
| **Viewer** | Read-only access | Read all components |
| **External** | Limited external access | Read specific shared items |

#### 6.4.3 Permission Matrix Example

| Role | Business Model | Process Catalogue | Quality Logs | Operating Model | Portfolio | Change & Adoption |
|------|---------------|-------------------|--------------|-----------------|-----------|-------------------|
| Admin | CRUD | CRUD | CRUD | CRUD | CRUD | CRUD |
| Portfolio Mgr | Read | Read | CRUD | Read | CRUD | CRUD |
| Process Owner | Read | CRUD (owned) | CRUD | CRUD | Read | Read |
| BA | Read | Edit | Create/Edit | Edit | Read | Read |
| PM | Read | Read | CRUD (project) | Read | CRUD (project) | Read |
| Viewer | Read | Read | Read | Read | Read | Read |

### 6.5 Core Platform Features

| Feature | Description |
|---------|-------------|
| **Hierarchical Navigation** | Navigate up/down through all hierarchies |
| **Multi-Dimensional Filtering** | Filter by any dimension (sponsor, system, market, etc.) |
| **Aggregated Reporting** | Roll up issues, risks, KPIs to any level |
| **Inheritance Engine** | Policies cascade down; issues roll up |
| **Cross-Linking** | Link any entity to any other (process ↔ project ↔ BM) |
| **Audit Trail** | Track all changes with who/when |
| **Version Control** | Maintain history of changes |
| **Prompt Library** | AI-assisted content generation |

### 6.6 User Stories

#### Business Model
- As a **Strategy Lead**, I want to view all issues affecting a specific market so I can prioritize interventions
- As a **COO**, I want to see aggregated SWOT at the Business Model level so I can report to the board

#### Process Catalogue  
- As a **Process Owner**, I want to see all issues in my process area (L1-L3) so I can plan improvements
- As a **SME**, I want to log an issue at L5 and have it visible to my Sponsor at L0

#### Quality Logs
- As a **Risk Manager**, I want to see all Critical risks across People, Process, System, Data dimensions
- As a **IT Director**, I want to filter issues by System category to plan remediation

#### Operating Model Design
- As a **Business Analyst**, I want to compare current vs future state RACI to identify role changes
- As a **Training Manager**, I want to see which roles are affected by process changes

#### Portfolio Response
- As a **Programme Manager**, I want to see which processes my projects are transforming
- As a **PMO Lead**, I want to see resource allocation across all active projects

#### Change & Adoption
- As a **Change Manager**, I want to survey users on adoption lead indicators
- As a **Sponsor**, I want to see if KPIs are improving post-implementation

### 7.3 Use Cases

[To be detailed in subsequent iterations]

---

## 7. User Personas & Workflows

### 7.1 User Personas

#### 7.1.1 Executive Personas

| Persona | Role | Primary Use Cases | Key Views |
|---------|------|-------------------|-----------|
| **CEO / COO** | Strategic oversight | Portfolio health, Business Model alignment, Executive dashboards | Portfolio summary, Strategic KPIs, RIADA heatmap |
| **CFO** | Financial governance | Budget tracking, Benefits realization, Cost analysis | Financial dashboards, Budget vs Actuals, ROI tracking |
| **CIO / CTO** | Technology strategy | System landscape, IT process health, Digital transformation | System catalogue, IT Secondary processes, Technology roadmap |

#### 7.1.2 Management Personas

| Persona | Role | Primary Use Cases | Key Views |
|---------|------|-------------------|-----------|
| **Portfolio Manager** | Portfolio oversight | Project prioritization (WSVF), Resource allocation, Cross-project dependencies | Portfolio dashboard, WSVF rankings, Resource heatmap |
| **Programme Manager** | Programme delivery | Multi-project coordination, Milestone tracking, RIADA management | Programme view, Gantt-style milestones, Risk register |
| **Process Owner** | Process governance | Process definition, Operating Model maintenance, Issue resolution | Process hierarchy, Operating Model components, RIADA log |
| **Department Head** | Functional leadership | Team processes, Departmental KPIs, Resource planning | Function view (L1), Team dashboards, Capacity planning |

#### 7.1.3 Operational Personas

| Persona | Role | Primary Use Cases | Key Views |
|---------|------|-------------------|-----------|
| **Project Manager** | Project delivery | Project tracking, Milestone management, Team coordination | Project card, Milestone tracker, Budget view |
| **Business Analyst** | Process documentation | Process mapping, Requirements capture, Operating Model design | Process editor, SIPOC mapping, RACI matrix |
| **Quality Manager** | Quality assurance | RIADA management, Audit tracking, Compliance monitoring | Quality dashboard, Audit log, Compliance checklist |
| **Change Manager** | Change adoption | Adoption surveys, Training tracking, Benefits measurement | Adoption dashboard, Survey results, KPI trends |

#### 7.1.4 Specialist Personas

| Persona | Role | Primary Use Cases | Key Views |
|---------|------|-------------------|-----------|
| **SME (Subject Matter Expert)** | Domain expertise | L3-L5 process detail, Issue logging, Knowledge contribution | Workflow detail, Step-by-step guides, Issue form |
| **IT Administrator** | System administration | User management, Integration configuration, System health | Admin console, User directory, Integration status |
| **External Auditor** | Compliance review | Read-only access to processes, Controls, Evidence | Audit view (filtered), Export functions |

### 7.2 Permission Matrix by Persona

| Persona | BM | PC | QL | OM | Portfolio | C&A | Admin |
|---------|----|----|----|----|-----------|-----|-------|
| CEO/COO | Read | Read | Read | Read | Read | Read | - |
| CFO | Read | Read | Read | Read | Read (Financial) | Read | - |
| CIO/CTO | Read | Read | Read | Read | Read | Read | - |
| Portfolio Mgr | Read | Read | CRUD | Read | CRUD | CRUD | - |
| Programme Mgr | Read | Read | CRUD | Read | CRUD (Programme) | Read | - |
| Process Owner | Read | CRUD (owned) | CRUD | CRUD (owned) | Read | Read | - |
| Dept Head | Read | Read (dept) | CRUD (dept) | Read | Read | Read | - |
| Project Mgr | Read | Read | CRUD (project) | Read | CRUD (project) | Read | - |
| Business Analyst | Read | Edit | Create/Edit | Edit | Read | Read | - |
| Quality Mgr | Read | Read | CRUD | Read | Read | Read | - |
| Change Mgr | Read | Read | Read | Read | Read | CRUD | - |
| SME | Read | Edit (L3-L5) | Create | Read | Read | Read | - |
| IT Admin | Read | Read | Read | Read | Read | Read | CRUD |
| External Auditor | Read | Read | Read | Read | Read | Read | - |
| Viewer | Read | Read | Read | Read | Read | Read | - |

### 7.3 Key Workflows

#### 7.3.1 Process Documentation Workflow

```
1. Process Owner initiates new process definition
   └── Creates L2 process with basic info
   
2. Business Analyst documents detail
   ├── Adds L3 workflows
   ├── Creates L4 variations (by market/category)
   └── Documents L5 steps (SIPOC)
   
3. SMEs review and enhance
   ├── Add operational detail
   ├── Upload supporting documents
   └── Flag issues/gaps
   
4. Process Owner approves
   ├── Reviews completeness
   ├── Assigns RACI
   └── Publishes to Standard Operating Model
   
5. Ongoing maintenance
   ├── SMEs log issues (RIADA)
   ├── Change requests trigger updates
   └── Periodic review cycles
```

#### 7.3.2 Project Delivery Workflow

```
1. Portfolio Manager creates project
   ├── Links to Strategic Pillar
   ├── Defines scope (in/out)
   └── Sets WSVF factors
   
2. Project Manager takes ownership
   ├── Defines milestones (Project, Customer, Financial, Benefit)
   ├── Links to affected processes
   ├── Sets up budget tracking
   └── Creates workstreams
   
3. Execution phase
   ├── Team logs progress
   ├── PM updates RAG status weekly
   ├── RIADA items managed
   └── Budget tracked
   
4. Go-live
   ├── Benefit milestones activated
   ├── Change Manager deploys adoption surveys
   └── KPI tracking begins
   
5. Benefits realization
   ├── Monthly benefits measurement
   ├── Variance analysis
   └── Lessons learned captured
```

#### 7.3.3 RIADA Management Workflow

```
1. Anyone logs RIADA item
   ├── Selects type (Risk/Issue/Action/Dependency/Assumption)
   ├── Attaches to entity (Process, Project, BM component)
   ├── Sets category (People/Process/System/Data)
   └── Assigns severity
   
2. Owner triages
   ├── Validates categorization
   ├── Assigns owner
   ├── Sets due date
   └── Links related items
   
3. Resolution cycle
   ├── Owner works item
   ├── Updates status
   ├── Logs actions taken
   └── Escalates if needed
   
4. Closure
   ├── Resolution documented
   ├── Status set to Resolved/Closed
   └── Linked items updated
   
5. Reporting
   ├── Auto-aggregation up hierarchy
   ├── Dashboard updates
   └── Trend analysis
```

---

## 8. Non-Functional Requirements

### 8.1 Performance

| Requirement | Target | Notes |
|-------------|--------|-------|
| **Page Load Time** | < 2 seconds | 90th percentile |
| **API Response Time** | < 500ms | Standard CRUD operations |
| **Search Response** | < 1 second | Full-text search across entities |
| **Report Generation** | < 30 seconds | PDF up to 100 pages |
| **Real-time Updates** | < 500ms | WebSocket latency |
| **Concurrent Users** | 500+ per tenant | Without degradation |

### 8.2 Security

| Requirement | Implementation |
|-------------|----------------|
| **Authentication** | Passwordless magic links (primary), OAuth 2.0 / OIDC (enterprise SSO add-on), SAML 2.0 (enterprise SSO add-on). See Section 6.2 for full specification |
| **Authorization** | Role-based access control (RBAC) with Row-Level Security |
| **Data Encryption** | AES-256 at rest, TLS 1.3 in transit |
| **MFA** | Required for admin roles, optional for others |
| **Session Management** | Configurable timeout, concurrent session limits |
| **Audit Logging** | All CRUD operations logged with user/timestamp |
| **Penetration Testing** | Annual third-party testing |
| **Vulnerability Scanning** | Automated weekly scans |

### 8.3 Scalability

| Dimension | Target | Approach |
|-----------|--------|----------|
| **Users per Tenant** | 10 - 1,000 | Horizontal scaling |
| **Tenants (SaaS)** | 100+ | Row-Level Security isolation |
| **Processes per Tenant** | 10,000+ | Efficient hierarchical queries |
| **RIADA Items** | 100,000+ per tenant | Indexed, partitioned |
| **Document Storage** | 100GB+ per tenant | Object storage (R2/OSS) |
| **API Requests** | 10,000/hour per tenant | Rate limiting, caching |

### 8.4 Availability

| Requirement | Target |
|-------------|--------|
| **Uptime SLA** | 99.9% (Global SaaS) |
| **Planned Maintenance** | < 4 hours/month, off-peak |
| **RTO (Recovery Time)** | < 4 hours |
| **RPO (Recovery Point)** | < 1 hour |
| **Backup Frequency** | Hourly incremental, daily full |
| **Disaster Recovery** | Multi-region failover (Global) |

### 8.5 Accessibility

| Requirement | Standard |
|-------------|----------|
| **WCAG Compliance** | Level AA (2.1) |
| **Keyboard Navigation** | Full support |
| **Screen Reader** | Compatible with JAWS, NVDA, VoiceOver |
| **Color Contrast** | Minimum 4.5:1 ratio |
| **Text Scaling** | Support up to 200% |

### 8.6 Localization

| Requirement | Support |
|-------------|---------|
| **Languages** | English (primary), Mandarin Chinese (China deployment) |
| **Date/Time** | Locale-aware formatting |
| **Currency** | Multi-currency display |
| **Time Zones** | User-configurable, UTC storage |

### 8.7 Data Retention

| Data Type | Retention | Notes |
|-----------|-----------|-------|
| **Active Data** | Indefinite | While tenant active |
| **Audit Logs** | 7 years | Compliance requirement |
| **Deleted Items** | 90 days soft delete | Recoverable |
| **Archived Projects** | 5 years | Read-only access |
| **Backups** | 30 days | Point-in-time recovery |

---

## 9. Technical Architecture

### 9.1 Deployment Models

The Process Catalogue supports two deployment models:

| Model | Description | Target Users |
|-------|-------------|--------------|
| **Multi-Tenant SaaS** | Shared infrastructure, organization-isolated data | Global customers |
| **Single-Tenant / On-Premise** | Dedicated deployment for specific client | Surity (China), Enterprise clients |

### 9.2 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PROCESS CATALOGUE                                   │
│                           Technical Architecture                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                         PRESENTATION LAYER                               │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │   │
│  │  │  Web App    │  │  Mobile     │  │  API        │  │  Webhooks   │    │   │
│  │  │  (React/    │  │  (PWA)      │  │  Consumers  │  │  (GitHub,   │    │   │
│  │  │   Next.js)  │  │             │  │             │  │   etc.)     │    │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                           API LAYER                                      │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐    │   │
│  │  │              FastAPI (Python) Backend                            │    │   │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │    │   │
│  │  │  │ Auth     │ │ REST API │ │ GraphQL  │ │ WebSocket│           │    │   │
│  │  │  │ (Magic  │ │ Endpoints│ │ (Optional│ │ (Real-   │           │    │   │
│  │  │  │  Links/ │ │          │ │          │ │  time)   │           │    │   │
│  │  │  │  SSO)   │ │          │ │          │ │          │           │    │   │
│  │  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │    │   │
│  │  └─────────────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                         SERVICE LAYER                                    │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │   │
│  │  │ Business │ │ Process  │ │ Portfolio│ │ Report   │ │ AI/LLM   │     │   │
│  │  │ Model    │ │ Catalogue│ │ Mgmt     │ │ Generator│ │ Services │     │   │
│  │  │ Service  │ │ Service  │ │ Service  │ │ Service  │ │          │     │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘     │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │   │
│  │  │ Quality  │ │ Operating│ │ Change & │ │ GitHub   │ │ Notifi-  │     │   │
│  │  │ Logs     │ │ Model    │ │ Adoption │ │ Integra- │ │ cation   │     │   │
│  │  │ Service  │ │ Service  │ │ Service  │ │ tion     │ │ Service  │     │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘     │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                          DATA LAYER                                      │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │   │
│  │  │   PostgreSQL    │  │  Object Storage │  │   Redis Cache   │         │   │
│  │  │   (Relational)  │  │  (Documents,    │  │   (Session,     │         │   │
│  │  │                 │  │   Reports, PDFs)│  │    Real-time)   │         │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 9.3 Technology Stack Recommendations

#### 9.3.1 Your Preferences vs Recommendations

| Layer | Your Preference | Recommendation | Rationale |
|-------|-----------------|----------------|-----------|
| **Hosting** | Vercel | ✅ Vercel (Global) / Alibaba Cloud (China) | Vercel excellent for Next.js; need China alternative |
| **Database** | Supabase | ⚠️ Supabase (Global) / Alibaba RDS (China) | Supabase doesn't operate in China |
| **Storage** | Cloudflare R2 | ✅ Cloudflare R2 (Global) / Alibaba OSS (China) | Good choice; need China alternative |
| **Backend** | Python | ✅ **FastAPI (Python)** | Excellent choice - modern, fast, async, great DX |

#### 9.3.2 Recommended Stack - Global (Multi-Tenant SaaS)

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Frontend Framework** | **Next.js 14+ (React)** | SSR/SSG, excellent DX, Vercel-optimized |
| **Frontend Hosting** | **Vercel** | Edge network, automatic scaling, preview deployments |
| **Backend Framework** | **FastAPI (Python 3.11+)** | Async, type hints, auto OpenAPI docs, excellent performance |
| **Backend Hosting** | **Vercel Serverless Functions** or **Railway/Render** | Serverless for simplicity; Railway for persistent connections |
| **Database** | **Supabase (PostgreSQL)** | Managed Postgres, real-time subscriptions, Row Level Security |
| **Object Storage** | **Cloudflare R2** | S3-compatible, no egress fees, global edge |
| **Cache** | **Upstash Redis** | Serverless Redis, global replication |
| **Search** | **Supabase Full-Text Search** or **Typesense** | Built-in FTS or dedicated search engine |
| **Auth** | **Supabase Auth** (magic links primary) + **Clerk** (enterprise SSO add-on) | Passwordless magic links for all users; OAuth/SAML SSO as optional enterprise tier. See Section 6.2 |
| **PDF Generation** | **WeasyPrint** or **Puppeteer** | Python-native or headless Chrome |
| **Background Jobs** | **Celery + Redis** or **Inngest** | Async task processing |
| **AI/LLM** | **OpenAI API** / **Anthropic Claude API** | Prompt library, content generation |
| **Monitoring** | **Sentry + Vercel Analytics** | Error tracking, performance monitoring |

#### 9.3.3 Recommended Stack - China (Single-Tenant)

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Frontend Framework** | **Next.js 14+ (React)** | Same as global for code parity |
| **Frontend Hosting** | **Alibaba Cloud ECS + CDN** | China-compliant hosting |
| **Backend Framework** | **FastAPI (Python 3.11+)** | Same as global |
| **Backend Hosting** | **Alibaba Cloud ECS** or **Function Compute** | China-compliant compute |
| **Database** | **Alibaba Cloud RDS (PostgreSQL)** | Managed Postgres, China-compliant |
| **Object Storage** | **Alibaba Cloud OSS** | S3-compatible, China-compliant |
| **Cache** | **Alibaba Cloud Redis** | Managed Redis |
| **Search** | **Alibaba OpenSearch** or **Self-hosted Typesense** | China-compliant search |
| **Auth** | **Alibaba IDaaS** (magic links primary) or **Self-hosted Keycloak** (enterprise SSO) | Passwordless magic links via Alibaba DirectMail; data residency compliance. See Section 6.2.11 |
| **PDF Generation** | **WeasyPrint** | Python-native, no external dependencies |
| **Background Jobs** | **Celery + Redis** | Self-hosted task processing |
| **AI/LLM** | **Alibaba Qwen** / **Baidu ERNIE** | China-accessible LLMs |
| **Monitoring** | **Alibaba Cloud ARMS** + **Self-hosted Sentry** | China-compliant monitoring |

#### 9.3.4 Why FastAPI + Python is the Right Choice

| Benefit | Description |
|---------|-------------|
| **Performance** | Async/await support, comparable to Node.js/Go for I/O-bound work |
| **Type Safety** | Pydantic models provide runtime validation + IDE support |
| **Auto Documentation** | OpenAPI (Swagger) docs generated automatically |
| **Ecosystem** | Rich libraries for PDF generation, data processing, AI/ML |
| **Developer Experience** | Clean, readable code; easy onboarding |
| **AI/LLM Ready** | Native support for OpenAI, LangChain, vector databases |

#### 9.3.5 Frontend: Why Next.js over Pure React

| Benefit | Description |
|---------|-------------|
| **SSR/SSG** | Server-side rendering for SEO and initial load performance |
| **API Routes** | Can host simple API endpoints alongside frontend |
| **Image Optimization** | Built-in image optimization |
| **Vercel Integration** | Seamless deployment, edge functions |
| **App Router** | Modern React Server Components support |

### 9.4 Architecture Patterns

#### 9.4.1 Multi-Tenancy Implementation

```
┌─────────────────────────────────────────────────────────────────┐
│                    MULTI-TENANCY APPROACH                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Option A: Row-Level Security (RECOMMENDED for SaaS)            │
│  ─────────────────────────────────────────────────              │
│  • Single database, single schema                                │
│  • Each table has `organization_id` column                       │
│  • PostgreSQL RLS policies enforce isolation                     │
│  • Supabase has built-in RLS support                            │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Table: processes                                        │    │
│  │  ┌────────────────┬─────────────┬──────────────────┐    │    │
│  │  │ organization_id│ process_id  │ name             │    │    │
│  │  ├────────────────┼─────────────┼──────────────────┤    │    │
│  │  │ org_001        │ proc_001    │ Order Management │    │    │
│  │  │ org_001        │ proc_002    │ Data Entry       │    │    │
│  │  │ org_002        │ proc_001    │ Sales Process    │    │    │
│  │  └────────────────┴─────────────┴──────────────────┘    │    │
│  │                                                          │    │
│  │  RLS Policy: organization_id = auth.jwt()->>'org_id'    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Option B: Schema-per-Tenant (For enterprise clients)           │
│  ─────────────────────────────────────────────────              │
│  • Single database, separate schema per tenant                   │
│  • Complete data isolation                                       │
│  • Easier compliance/audit                                       │
│  • More complex migrations                                       │
│                                                                  │
│  Option C: Database-per-Tenant (For China/On-Premise)          │
│  ─────────────────────────────────────────────────              │
│  • Separate database instance per client                         │
│  • Maximum isolation                                             │
│  • Required for data residency compliance                        │
│  • Higher operational overhead                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Recommendation:**
- **Global SaaS:** Row-Level Security (Option A)
- **China/Enterprise:** Database-per-Tenant (Option C)

#### 9.4.2 API Design Pattern

```python
# FastAPI Application Structure

app/
├── main.py                 # FastAPI app entry point
├── config.py               # Configuration management
├── dependencies.py         # Dependency injection
│
├── api/
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── business_model.py
│   │   ├── process_catalogue.py
│   │   ├── quality_logs.py
│   │   ├── operating_model.py
│   │   ├── portfolio.py
│   │   ├── change_adoption.py
│   │   └── reports.py
│   └── webhooks/
│       └── github.py
│
├── services/
│   ├── business_model_service.py
│   ├── process_service.py
│   ├── riada_service.py
│   ├── portfolio_service.py
│   ├── report_generator.py
│   ├── pdf_service.py
│   └── llm_service.py
│
├── models/
│   ├── database/          # SQLAlchemy/SQLModel ORM models
│   └── schemas/           # Pydantic request/response schemas
│
├── core/
│   ├── security.py        # Auth, JWT, permissions
│   ├── multi_tenancy.py   # Tenant context management
│   └── exceptions.py      # Custom exceptions
│
└── utils/
    ├── pdf_generator.py
    └── aggregation.py     # Roll-up calculations
```

#### 9.4.3 Real-Time Updates Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                    REAL-TIME ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Option A: Supabase Realtime (Global SaaS)                      │
│  ─────────────────────────────────────────                      │
│  • Built-in PostgreSQL LISTEN/NOTIFY                            │
│  • WebSocket subscriptions to table changes                     │
│  • Automatic filtering by RLS policies                          │
│                                                                  │
│  Client (React)                 Supabase                        │
│  ┌──────────────┐              ┌──────────────┐                 │
│  │ Subscribe to │──WebSocket──▶│ Realtime     │                 │
│  │ processes    │              │ Server       │                 │
│  │ table        │◀─────────────│              │                 │
│  └──────────────┘   Updates    └──────────────┘                 │
│                                       │                          │
│                                       ▼                          │
│                                ┌──────────────┐                 │
│                                │  PostgreSQL  │                 │
│                                │  (NOTIFY)    │                 │
│                                └──────────────┘                 │
│                                                                  │
│  Option B: Custom WebSocket (China/On-Premise)                  │
│  ─────────────────────────────────────────────                  │
│  • FastAPI WebSocket endpoints                                   │
│  • Redis Pub/Sub for message distribution                       │
│  • Custom event publishing on data changes                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 9.5 Infrastructure Diagram

#### 9.5.1 Global SaaS Deployment

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GLOBAL SAAS INFRASTRUCTURE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                              CLOUDFLARE                                      │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │  CDN + WAF + DDoS Protection + R2 Storage                          │     │
│  └────────────────────────────────────────────────────────────────────┘     │
│                                      │                                       │
│                                      ▼                                       │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │                            VERCEL                                   │     │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │     │
│  │  │  Next.js         │  │  Edge Functions  │  │  Serverless     │  │     │
│  │  │  Frontend        │  │  (Middleware)    │  │  API Routes     │  │     │
│  │  └──────────────────┘  └──────────────────┘  └─────────────────┘  │     │
│  └────────────────────────────────────────────────────────────────────┘     │
│                                      │                                       │
│          ┌───────────────────────────┼───────────────────────────┐          │
│          ▼                           ▼                           ▼          │
│  ┌──────────────────┐  ┌──────────────────────┐  ┌──────────────────┐      │
│  │    SUPABASE      │  │      RAILWAY         │  │    UPSTASH       │      │
│  │  ┌────────────┐  │  │  ┌────────────────┐  │  │  ┌────────────┐  │      │
│  │  │ PostgreSQL │  │  │  │ FastAPI Backend│  │  │  │   Redis    │  │      │
│  │  │ + Realtime │  │  │  │ (Long-running) │  │  │  │   Cache    │  │      │
│  │  │ + Auth     │  │  │  │                │  │  │  │            │  │      │
│  │  └────────────┘  │  │  │ • PDF Gen      │  │  │  └────────────┘  │      │
│  │  ┌────────────┐  │  │  │ • Background   │  │  └──────────────────┘      │
│  │  │  Storage   │  │  │  │   Jobs         │  │                             │
│  │  │ (Backups)  │  │  │  │ • WebSockets   │  │                             │
│  │  └────────────┘  │  │  └────────────────┘  │                             │
│  └──────────────────┘  └──────────────────────┘                             │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │                       EXTERNAL SERVICES                             │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │     │
│  │  │ OpenAI / │  │  GitHub  │  │  Sentry  │  │  Resend  │           │     │
│  │  │ Anthropic│  │   API    │  │(Monitoring│ │ (Email)  │           │     │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │     │
│  └────────────────────────────────────────────────────────────────────┘     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 9.5.2 China Single-Tenant Deployment

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CHINA SINGLE-TENANT INFRASTRUCTURE                        │
│                         (Alibaba Cloud China)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │                    ALIBABA CLOUD CDN + WAF                          │     │
│  │                   (China mainland nodes)                            │     │
│  └────────────────────────────────────────────────────────────────────┘     │
│                                      │                                       │
│                                      ▼                                       │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │                      ALIBABA CLOUD ECS                              │     │
│  │  ┌────────────────────────────────────────────────────────────┐    │     │
│  │  │                    Docker / Kubernetes                      │    │     │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │    │     │
│  │  │  │   Next.js    │  │   FastAPI    │  │   Celery Worker  │  │    │     │
│  │  │  │   Frontend   │  │   Backend    │  │   (Background)   │  │    │     │
│  │  │  │   Container  │  │   Container  │  │   Container      │  │    │     │
│  │  │  └──────────────┘  └──────────────┘  └──────────────────┘  │    │     │
│  │  └────────────────────────────────────────────────────────────┘    │     │
│  └────────────────────────────────────────────────────────────────────┘     │
│                                      │                                       │
│          ┌───────────────────────────┼───────────────────────────┐          │
│          ▼                           ▼                           ▼          │
│  ┌──────────────────┐  ┌──────────────────────┐  ┌──────────────────┐      │
│  │  ALIBABA RDS     │  │   ALIBABA OSS        │  │  ALIBABA REDIS   │      │
│  │  ┌────────────┐  │  │  ┌────────────────┐  │  │  ┌────────────┐  │      │
│  │  │ PostgreSQL │  │  │  │ Object Storage │  │  │  │   Cache    │  │      │
│  │  │            │  │  │  │ (Documents,    │  │  │  │   + Pub/Sub│  │      │
│  │  │            │  │  │  │  Reports, PDFs)│  │  │  │            │  │      │
│  │  └────────────┘  │  │  └────────────────┘  │  │  └────────────┘  │      │
│  └──────────────────┘  └──────────────────────┘  └──────────────────┘      │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │                    CHINA-ACCESSIBLE SERVICES                        │     │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │     │
│  │  │ Alibaba Qwen │  │  Gitee       │  │ Alibaba ARMS │              │     │
│  │  │ / Baidu ERNIE│  │  (Git host)  │  │ (Monitoring) │              │     │
│  │  │ (LLM)        │  │              │  │              │              │     │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │     │
│  └────────────────────────────────────────────────────────────────────┘     │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │                      COMPLIANCE & SECURITY                          │     │
│  │  • ICP License (required for China hosting)                         │     │
│  │  • Data residency within mainland China                             │     │
│  │  • China Cybersecurity Law compliance                               │     │
│  │  • Personal Information Protection Law (PIPL) compliance            │     │
│  └────────────────────────────────────────────────────────────────────┘     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.6 Data Model (Detailed)

#### 9.6.1 Data Model Summary

**Total Tables: 45+**

| Domain | Tables | Key Entities |
|--------|--------|--------------|
| **Core/Multi-Tenancy** | 4 | Organization, User, Role, UserRole |
| **Business Model** | 3 | BusinessModel, CanvasComponent, CanvasEntry |
| **Process Catalogue** | 4 | Process, ProcessTag, ProcessLink, ProcessBusinessModel |
| **Operating Model** | 4 | OperatingModelComponent, RaciEntry, KpiDefinition, ProcessKpi |
| **Quality Logs (RIADA)** | 3 | RiadaItem, RiadaAttachment, RiadaHistory |
| **Portfolio** | 4 | Portfolio, PortfolioItem, Milestone, ProjectProcess |
| **Change & Adoption** | 4 | ChangeIndicator, KpiTracking, AdoptionSurvey, AdoptionResponse |
| **Surveys** | 5 | SurveyTemplate, SurveyInstance, SurveyRespondent, SurveyResponse, SurveyResult |
| **Agentic/Agents** | 3 | Agent, ProcessAgent, AgenticOpportunity |
| **Reference Catalogues** | 8 | SystemCatalogue, RoleCatalogue, SupplierCatalogue, ClientCatalogue, MarketCatalogue, CategoryCatalogue, PartnerCatalogue |
| **Prompt Library** | 3 | PromptTemplate, PromptExecution, PromptContextSnapshot |
| **LLM Integration** | 4 | LLMConfiguration, LLMUsage, Conversation, ConversationMessage |
| **Audit & History** | 2 | AuditLog, EntityVersion |
| **Documents** | 2 | Document, PublishedReport |

#### 9.6.2 Entity Relationship Diagram Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              PROCESS CATALOGUE - ENTITY RELATIONSHIP DIAGRAM                      │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                    CORE / MULTI-TENANCY                                      │ │
│  │                                                                                              │ │
│  │    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐                      │ │
│  │    │ Organization │◄───────►│    User      │◄───────►│    Role      │                      │ │
│  │    │              │  1:N    │              │   N:M   │              │                      │ │
│  │    │ • id         │         │ • id         │         │ • id         │                      │ │
│  │    │ • name       │         │ • email      │         │ • name       │                      │ │
│  │    │ • slug       │         │ • name       │         │ • permissions│                      │ │
│  │    │ • tier       │         │ • status     │         │              │                      │ │
│  │    └──────┬───────┘         └──────────────┘         └──────────────┘                      │ │
│  │           │ (All entities reference Organization)                                           │ │
│  └───────────┼─────────────────────────────────────────────────────────────────────────────────┘ │
│              │                                                                                    │
│  ┌───────────┼─────────────────────────────────────────────────────────────────────────────────┐ │
│  │           ▼                     COMPONENT 1: BUSINESS MODEL                                  │ │
│  │                                                                                              │ │
│  │    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐                      │ │
│  │    │BusinessModel │────────►│CanvasComponent────────►│ CanvasEntry  │                      │ │
│  │    │              │   1:N   │              │   1:N   │              │                      │ │
│  │    │ • id         │         │ • type       │         │ • name       │                      │ │
│  │    │ • name       │         │ • name       │         │ • agentic_   │                      │ │
│  │    │ • version    │         │              │         │   potential  │                      │ │
│  │    └──────────────┘         └──────────────┘         └──────┬───────┘                      │ │
│  │                                                              │                              │ │
│  └──────────────────────────────────────────────────────────────┼──────────────────────────────┘ │
│                                                                 │                                 │
│  ┌──────────────────────────────────────────────────────────────┼──────────────────────────────┐ │
│  │                        COMPONENT 2: PROCESS CATALOGUE        │                               │ │
│  │                                                              ▼                               │ │
│  │    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐                      │ │
│  │    │   Process    │◄───────►│ ProcessTag   │◄───────►│ProcessBusModel                      │ │
│  │    │   (self)     │   1:N   │              │         │ (link to BM) │                      │ │
│  │    │ • id         │         │ • tag_type   │         │              │                      │ │
│  │    │ • parent_id  │         │ • tag_value  │         └──────────────┘                      │ │
│  │    │ • level      │         └──────────────┘                                               │ │
│  │    │ • code       │                                                                         │ │
│  │    │ • name       │◄────────┐                                                              │ │
│  │    │ • agentic_   │         │                                                              │ │
│  │    │   potential  │         │                                                              │ │
│  │    │ • automation │         │                                                              │ │
│  │    │   _level     │         │                                                              │ │
│  │    └──────┬───────┘         │                                                              │ │
│  │           │                 │                                                              │ │
│  └───────────┼─────────────────┼──────────────────────────────────────────────────────────────┘ │
│              │                 │                                                                 │
│  ┌───────────┼─────────────────┼──────────────────────────────────────────────────────────────┐ │
│  │           │                 │           COMPONENT 4: OPERATING MODEL                        │ │
│  │           │                 │                                                               │ │
│  │           ▼                 │    ┌──────────────┐         ┌──────────────┐                 │ │
│  │    ┌──────────────┐        │    │   OMComponent│         │  RaciEntry   │                 │ │
│  │    │ ProcessAgent │◄───────┼───►│              │────────►│              │                 │ │
│  │    │              │        │    │ • process_id │   1:N   │ • role_id    │                 │ │
│  │    │ • process_id │        │    │ • type       │         │ • raci_type  │                 │ │
│  │    │ • agent_id   │        │    │ • state      │         │              │                 │ │
│  │    │ • linkage    │        │    └──────────────┘         └──────────────┘                 │ │
│  │    │   _type      │        │                                                               │ │
│  │    └──────┬───────┘        │    ┌──────────────┐         ┌──────────────┐                 │ │
│  │           │                │    │KpiDefinition │────────►│  ProcessKpi  │                 │ │
│  │           ▼                │    │              │   1:N   │              │                 │ │
│  │    ┌──────────────┐        │    │ • name       │         │ • target     │                 │ │
│  │    │    Agent     │        │    │ • formula    │         │ • actual     │                 │ │
│  │    │              │        │    └──────────────┘         └──────────────┘                 │ │
│  │    │ • id         │        │                                                               │ │
│  │    │ • name       │        │                                                               │ │
│  │    │ • agent_type │        │                                                               │ │
│  │    │ • technology │        │                                                               │ │
│  │    │ • status     │        │                                                               │ │
│  │    └──────────────┘        │                                                               │ │
│  │                            │                                                               │ │
│  └────────────────────────────┼───────────────────────────────────────────────────────────────┘ │
│                               │                                                                  │
│  ┌────────────────────────────┼───────────────────────────────────────────────────────────────┐ │
│  │                            │      COMPONENT 3: QUALITY LOGS (RIADA)                         │ │
│  │                            │                                                                │ │
│  │                            ▼                                                                │ │
│  │    ┌───────────────────────────────────────────┐                                           │ │
│  │    │              RiadaItem                    │◄──────────┐                               │ │
│  │    │                                           │           │ (self-link                    │ │
│  │    │ • id            • category (PPSD)         │───────────┘  for related)                 │ │
│  │    │ • type (RIADA)  • severity                │                                           │ │
│  │    │ • title         • status                  │                                           │ │
│  │    │ • description   • owner_id                │                                           │ │
│  │    └───────────────────────┬───────────────────┘                                           │ │
│  │                            │                                                                │ │
│  │                            ▼                                                                │ │
│  │    ┌───────────────────────────────────────────┐                                           │ │
│  │    │           RiadaAttachment                 │ (Polymorphic - links to any entity)       │ │
│  │    │ • riada_item_id   • entity_type           │                                           │ │
│  │    │                   • entity_id             │                                           │ │
│  │    └───────────────────────────────────────────┘                                           │ │
│  │                                                                                             │ │
│  └─────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                            COMPONENT 5: PORTFOLIO RESPONSE                                   │ │
│  │                                                                                              │ │
│  │    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐                      │ │
│  │    │  Portfolio   │────────►│PortfolioItem │◄───────►│  Milestone   │                      │ │
│  │    │              │   1:N   │   (self)     │   1:N   │              │                      │ │
│  │    │ • id         │         │ • id         │         │ • type       │                      │ │
│  │    │ • name       │         │ • parent_id  │         │ • target_date│                      │ │
│  │    │ • year       │         │ • level      │         │ • status     │                      │ │
│  │    └──────────────┘         │ • type       │         └──────────────┘                      │ │
│  │                             │ • wsvf_score │                                               │ │
│  │                             └──────┬───────┘                                               │ │
│  │                                    │                                                        │ │
│  │                                    ▼                                                        │ │
│  │                             ┌──────────────┐                                               │ │
│  │                             │ProjectProcess│ (Links Projects ↔ Processes)                  │ │
│  │                             │              │                                               │ │
│  │                             │• project_id  │                                               │ │
│  │                             │• process_id  │                                               │ │
│  │                             │• impact_type │                                               │ │
│  │                             └──────────────┘                                               │ │
│  │                                                                                             │ │
│  └─────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                     COMPONENT 6 & 7: CHANGE & ADOPTION + SURVEYS                            │ │
│  │                                                                                              │ │
│  │    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐                      │ │
│  │    │ChangeIndicator────────►│ KpiTracking  │         │SurveyTemplate│                      │ │
│  │    │              │         │              │         │              │                      │ │
│  │    │ • project_id │         │ • baseline   │         │ • mode       │                      │ │
│  │    │ • indicator  │         │ • target     │         │ • questions  │                      │ │
│  │    │   _type      │         │ • actual     │         │              │                      │ │
│  │    └──────────────┘         └──────────────┘         └──────┬───────┘                      │ │
│  │                                                              │ 1:N                          │ │
│  │                                                              ▼                              │ │
│  │    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐                      │ │
│  │    │AdoptionSurvey│────────►│AdoptionResponse        │SurveyInstance│                      │ │
│  │    │              │   1:N   │              │         │              │                      │ │
│  │    │ • project_id │         │ • user_id    │         │ • process_id │                      │ │
│  │    │ • timing     │         │ • responses  │         │ • status     │                      │ │
│  │    └──────────────┘         └──────────────┘         └──────┬───────┘                      │ │
│  │                                                              │ 1:N                          │ │
│  │                                                              ▼                              │ │
│  │                                                       ┌──────────────┐                      │ │
│  │                                                       │SurveyResponse│                      │ │
│  │                                                       │              │                      │ │
│  │                                                       │ • user_id    │                      │ │
│  │                                                       │ • responses  │                      │ │
│  │                                                       │ • scores     │                      │ │
│  │                                                       └──────────────┘                      │ │
│  │                                                                                             │ │
│  └─────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                              SUPPORTING: LLM / PROMPTS / REFERENCE                           │ │
│  │                                                                                              │ │
│  │    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐                      │ │
│  │    │PromptTemplate│────────►│PromptExecution         │LLMConfiguration                     │ │
│  │    │              │   1:N   │              │         │              │                      │ │
│  │    │ • name       │         │ • user_id    │         │ • provider   │                      │ │
│  │    │ • template   │         │ • result     │         │ • model      │                      │ │
│  │    │ • variables  │         │ • rating     │         │ • api_key    │                      │ │
│  │    └──────────────┘         └──────────────┘         └──────────────┘                      │ │
│  │                                                                                              │ │
│  │    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐                      │ │
│  │    │ Conversation │────────►│ConversationMessage     │  LLMUsage    │                      │ │
│  │    │              │   1:N   │              │         │              │                      │ │
│  │    │ • user_id    │         │ • role       │         │ • tokens     │                      │ │
│  │    │ • context    │         │ • content    │         │ • cost       │                      │ │
│  │    └──────────────┘         └──────────────┘         └──────────────┘                      │ │
│  │                                                                                              │ │
│  │    REFERENCE CATALOGUES:                                                                    │ │
│  │    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │ │
│  │    │ System   │ │  Role    │ │ Supplier │ │  Client  │ │  Market  │ │ Category │          │ │
│  │    │ Catalogue│ │ Catalogue│ │ Catalogue│ │ Catalogue│ │ Catalogue│ │ Catalogue│          │ │
│  │    └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘          │ │
│  │                                                                                              │ │
│  └─────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 9.6.3 Core Tables - Multi-Tenancy & Users

##### Organization

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `name` | VARCHAR(255) | NOT NULL | Organization name |
| `slug` | VARCHAR(100) | UNIQUE, NOT NULL | URL-friendly identifier |
| `subscription_tier` | ENUM | NOT NULL | 'free', 'pro', 'enterprise' |
| `settings` | JSONB | | Organization settings |
| `branding` | JSONB | | Logo, colors, etc. |
| `data_region` | VARCHAR(50) | | 'global', 'china', 'eu' |
| `created_at` | TIMESTAMP | NOT NULL | Creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL | Last update timestamp |

##### User

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | Tenant reference |
| `email` | VARCHAR(255) | UNIQUE (per org) | User email |
| `name` | VARCHAR(255) | NOT NULL | Display name |
| `avatar_url` | VARCHAR(500) | | Profile picture |
| `auth_provider` | VARCHAR(50) | | 'email', 'google', 'saml' |
| `auth_provider_id` | VARCHAR(255) | | External auth ID |
| `status` | ENUM | NOT NULL | 'active', 'inactive', 'pending' |
| `last_login_at` | TIMESTAMP | | Last login time |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | NOT NULL | |

##### Role

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | Tenant reference (NULL for system roles) |
| `name` | VARCHAR(100) | NOT NULL | Role name |
| `description` | TEXT | | Role description |
| `permissions` | JSONB | NOT NULL | Permission definitions |
| `is_system` | BOOLEAN | DEFAULT FALSE | System-defined vs custom |
| `created_at` | TIMESTAMP | NOT NULL | |

##### UserRole (Join Table)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `user_id` | UUID | FK → User, PK | |
| `role_id` | UUID | FK → Role, PK | |
| `scope_type` | VARCHAR(50) | | 'organization', 'process', 'project' |
| `scope_id` | UUID | | Specific entity ID for scoped permissions |
| `granted_at` | TIMESTAMP | NOT NULL | |
| `granted_by` | UUID | FK → User | |

#### 9.6.4 Business Model Tables

##### BusinessModel

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | Tenant reference |
| `name` | VARCHAR(255) | NOT NULL | Business model name |
| `description` | TEXT | | Description |
| `version` | INTEGER | DEFAULT 1 | Version number |
| `status` | ENUM | NOT NULL | 'draft', 'active', 'archived' |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | NOT NULL | |
| `created_by` | UUID | FK → User | |

##### CanvasComponent

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `business_model_id` | UUID | FK → BusinessModel | Parent BM |
| `component_type` | ENUM | NOT NULL | See component types below |
| `name` | VARCHAR(255) | NOT NULL | Display name |
| `description` | TEXT | | Description |
| `sort_order` | INTEGER | DEFAULT 0 | Display order |
| `created_at` | TIMESTAMP | NOT NULL | |

**Component Types:** `customer_segments`, `clients`, `value_propositions`, `channels`, `revenue_streams`, `cost_structure`, `key_resources`, `key_activities`, `key_partners`, `key_suppliers`, `trading_markets`, `sourcing_markets`, `product_categories`

##### CanvasEntry

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `component_id` | UUID | FK → CanvasComponent | Parent component |
| `name` | VARCHAR(255) | NOT NULL | Entry name (e.g., "Bunnings", "UK") |
| `description` | TEXT | | Description |
| `metadata` | JSONB | | Additional structured data |
| `status` | ENUM | NOT NULL | 'active', 'inactive' |
| `sort_order` | INTEGER | DEFAULT 0 | Display order |
| `agentic_potential` | ENUM | | 'none', 'low', 'medium', 'high' |
| `agentic_opportunity_description` | TEXT | | Description of automation opportunity |
| `current_digital_maturity` | ENUM | | 'traditional', 'digitizing', 'digital', 'ai_enabled' |
| `target_digital_maturity` | ENUM | | 'traditional', 'digitizing', 'digital', 'ai_enabled' |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | NOT NULL | |

#### 9.6.5 Process Catalogue Tables

##### Process

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | Tenant reference |
| `parent_id` | UUID | FK → Process (self) | Parent process (NULL for L0) |
| `process_type` | ENUM | NOT NULL | 'primary', 'secondary' |
| `domain` | VARCHAR(50) | | For secondary: 'IT', 'HR', 'Legal', 'Treasury', 'Portfolio_Delivery' |
| `level` | ENUM | NOT NULL | 'L0', 'L1', 'L2', 'L3', 'L4', 'L5' |
| `code` | VARCHAR(50) | UNIQUE (per org) | Process code (e.g., "L2-10") |
| `name` | VARCHAR(255) | NOT NULL | Process name |
| `description` | TEXT | | Short description |
| `content` | TEXT | | Rich text documentation (Standard Operating Model) |
| `content_format` | ENUM | DEFAULT 'markdown' | 'markdown', 'html' |
| `status` | ENUM | NOT NULL | 'draft', 'active', 'deprecated', 'archived' |
| `version` | INTEGER | DEFAULT 1 | Version number |
| `owner_id` | UUID | FK → User | Process owner |
| `sponsor_id` | UUID | FK → User | Sponsor (typically L0-L1) |
| `rag_people` | ENUM | | 'green', 'amber', 'red' |
| `rag_process` | ENUM | | 'green', 'amber', 'red' |
| `rag_system` | ENUM | | 'green', 'amber', 'red' |
| `rag_data` | ENUM | | 'green', 'amber', 'red' |
| `agentic_potential` | ENUM | | 'none', 'low', 'medium', 'high' |
| `agentic_opportunity_description` | TEXT | | Description of automation opportunity |
| `current_automation_level` | ENUM | | 'manual', 'assisted', 'semi_automated', 'fully_automated' |
| `target_automation_level` | ENUM | | 'manual', 'assisted', 'semi_automated', 'fully_automated' |
| `current_agent_id` | UUID | FK → Agent | Current live agent |
| `target_agent_id` | UUID | FK → Agent | Planned future agent |
| `agentic_assessment_date` | DATE | | When last assessed |
| `agentic_assessed_by` | UUID | FK → User | Who assessed |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | NOT NULL | |
| `published_at` | TIMESTAMP | | When published to SOM |

##### ProcessTag (For L4 Variations)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `process_id` | UUID | FK → Process | Process being tagged |
| `tag_type` | ENUM | NOT NULL | 'market', 'category', 'client', 'custom' |
| `tag_value` | VARCHAR(255) | NOT NULL | Tag value (e.g., "UK", "Technical") |
| `canvas_entry_id` | UUID | FK → CanvasEntry | Link to BM entry if applicable |

##### ProcessLink (Cross-Linking)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `source_process_id` | UUID | FK → Process | Source process |
| `target_process_id` | UUID | FK → Process | Target process |
| `link_type` | ENUM | NOT NULL | 'supports', 'depends_on', 'related', 'primary_secondary' |
| `description` | TEXT | | Link description |
| `created_at` | TIMESTAMP | NOT NULL | |

#### 9.6.6 Operating Model Tables

##### OperatingModelComponent

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `process_id` | UUID | FK → Process | Parent process |
| `component_type` | ENUM | NOT NULL | See types below |
| `state` | ENUM | NOT NULL | 'current', 'future' |
| `content` | JSONB | NOT NULL | Component-specific data |
| `version` | INTEGER | DEFAULT 1 | |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | NOT NULL | |
| `updated_by` | UUID | FK → User | |

**Component Types:** `raci`, `kpis`, `policies`, `governance`, `systems`, `timing_sla`, `agents`, `security`, `data`

##### RaciEntry

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `om_component_id` | UUID | FK → OperatingModelComponent | Parent (type='raci') |
| `activity` | VARCHAR(255) | NOT NULL | Activity name |
| `responsible_id` | UUID | FK → Role/User | R - Does the work |
| `accountable_id` | UUID | FK → Role/User | A - Owns the outcome |
| `consulted_ids` | UUID[] | | C - Provides input |
| `informed_ids` | UUID[] | | I - Kept informed |
| `agent_id` | UUID | FK → Agent | If automated |
| `sort_order` | INTEGER | DEFAULT 0 | |

##### KpiDefinition (Reference Catalogue)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | Tenant reference |
| `name` | VARCHAR(255) | NOT NULL | KPI name |
| `description` | TEXT | | Description |
| `unit` | VARCHAR(50) | | 'hours', '%', '$', 'count' |
| `direction` | ENUM | | 'higher_better', 'lower_better' |
| `calculation` | TEXT | | Formula/calculation method |
| `frequency` | ENUM | | 'daily', 'weekly', 'monthly' |
| `status` | ENUM | NOT NULL | 'evaluate', 'maintain', 'optimize', 'retire' |
| `created_at` | TIMESTAMP | NOT NULL | |

##### ProcessKpi (KPIs assigned to process)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `process_id` | UUID | FK → Process | |
| `kpi_id` | UUID | FK → KpiDefinition | |
| `state` | ENUM | NOT NULL | 'current', 'future' |
| `target_value` | DECIMAL | | Target |
| `current_value` | DECIMAL | | Current value |
| `baseline_value` | DECIMAL | | Baseline before change |
| `last_measured_at` | TIMESTAMP | | |

#### 9.6.7 Quality Logs (RIADA) Tables

##### RiadaItem

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | Tenant reference |
| `type` | ENUM | NOT NULL | 'risk', 'issue', 'action', 'dependency', 'assumption' |
| `code` | VARCHAR(50) | UNIQUE (per org) | Auto-generated (e.g., "RISK-001") |
| `title` | VARCHAR(255) | NOT NULL | Short title |
| `description` | TEXT | NOT NULL | Full description |
| `category` | ENUM | NOT NULL | 'people', 'process', 'system', 'data' |
| `severity` | ENUM | NOT NULL | 'critical', 'high', 'medium', 'low' |
| `probability` | ENUM | | For risks: 'high', 'medium', 'low' |
| `impact` | ENUM | | For risks: 'high', 'medium', 'low' |
| `status` | ENUM | NOT NULL | See status values |
| `owner_id` | UUID | FK → User | Assigned owner |
| `reporter_id` | UUID | FK → User | Who logged it |
| `due_date` | DATE | | Target resolution date |
| `resolution` | TEXT | | Resolution details |
| `mitigation` | TEXT | | Mitigation plan (risks) |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | NOT NULL | |
| `resolved_at` | TIMESTAMP | | |

**Status Values:** `draft`, `open`, `in_progress`, `on_hold`, `resolved`, `closed`, `mitigated`, `cancelled`

##### RiadaAttachment (Polymorphic Link)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `riada_item_id` | UUID | FK → RiadaItem | |
| `attachable_type` | VARCHAR(50) | NOT NULL | 'process', 'portfolio_item', 'canvas_entry', 'project' |
| `attachable_id` | UUID | NOT NULL | ID of attached entity |
| `created_at` | TIMESTAMP | NOT NULL | |

##### RiadaLink (RIADA-to-RIADA Links)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `source_id` | UUID | FK → RiadaItem, PK | |
| `target_id` | UUID | FK → RiadaItem, PK | |
| `link_type` | ENUM | NOT NULL | 'causes', 'mitigates', 'blocks', 'related' |
| `created_at` | TIMESTAMP | NOT NULL | |

#### 9.6.8 Portfolio Tables

##### Portfolio

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | Tenant reference |
| `name` | VARCHAR(255) | NOT NULL | Portfolio name |
| `description` | TEXT | | Description |
| `time_horizon` | VARCHAR(50) | | "2026", "2026-2028" |
| `status` | ENUM | NOT NULL | 'planning', 'active', 'completed', 'archived' |
| `owner_id` | UUID | FK → User | Portfolio owner |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | NOT NULL | |

##### PortfolioItem

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `portfolio_id` | UUID | FK → Portfolio | |
| `parent_id` | UUID | FK → PortfolioItem (self) | Hierarchy |
| `item_type` | ENUM | NOT NULL | 'pillar', 'initiative', 'project', 'workstream', 'work_package' |
| `code` | VARCHAR(50) | UNIQUE (per portfolio) | Item code |
| `name` | VARCHAR(255) | NOT NULL | Item name |
| `description` | TEXT | | Description |
| `status` | ENUM | NOT NULL | 'planning', 'active', 'on_hold', 'completed', 'cancelled' |
| `owner_id` | UUID | FK → User | Owner |
| `sponsor_id` | UUID | FK → User | Sponsor (for projects) |
| `start_date` | DATE | | Planned start |
| `end_date` | DATE | | Planned end |
| `actual_start_date` | DATE | | Actual start |
| `actual_end_date` | DATE | | Actual end |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | NOT NULL | |

##### ProjectDetail (Extended Project Fields)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `portfolio_item_id` | UUID | PK, FK → PortfolioItem | 1:1 relationship |
| `benefits_description` | TEXT | | Expected benefits |
| `outcome_statement` | TEXT | | Measurable outcomes |
| `success_criteria` | TEXT | | How success is measured |
| `scope_in` | TEXT | | In scope items |
| `scope_out` | TEXT | | Out of scope items |
| `scope_notes` | TEXT | | Additional scope context |
| `wsvf_value` | INTEGER | | 1-10 |
| `wsvf_confidence` | DECIMAL | | 0.1-1.0 |
| `wsvf_effort` | INTEGER | | 1-10 |
| `wsvf_duration_weeks` | INTEGER | | Duration in weeks |
| `wsvf_score` | DECIMAL | | Calculated score |
| `budget_status` | ENUM | | 'draft', 'pending', 'approved', 'on_hold', 'closed' |
| `budgeted_spend` | DECIMAL | | Approved budget |
| `current_spend` | DECIMAL | | Actual to date |
| `projected_spend` | DECIMAL | | Forecast at completion |
| `contingency_amount` | DECIMAL | | Reserved contingency |
| `contingency_used` | DECIMAL | | Contingency spent |
| `target_benefits` | DECIMAL | | Target benefits value |
| `current_benefits` | DECIMAL | | Benefits accrued |
| `rag_resource` | ENUM | | 'green', 'amber', 'red' |
| `rag_quality` | ENUM | | |
| `rag_scope` | ENUM | | |
| `rag_benefits` | ENUM | | |
| `rag_timeline` | ENUM | | |
| `rag_overall` | ENUM | | |
| `rag_trend` | ENUM | | 'improving', 'stable', 'declining' |
| `rag_commentary` | TEXT | | Status commentary |
| `updated_at` | TIMESTAMP | NOT NULL | |

##### Milestone

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `portfolio_item_id` | UUID | FK → PortfolioItem | Parent project/workstream |
| `milestone_type` | ENUM | NOT NULL | 'project', 'customer', 'financial', 'benefit' |
| `name` | VARCHAR(255) | NOT NULL | Milestone name |
| `description` | TEXT | | Description |
| `planned_date` | DATE | NOT NULL | Target date |
| `actual_date` | DATE | | Actual completion date |
| `status` | ENUM | NOT NULL | 'not_started', 'in_progress', 'complete', 'delayed', 'at_risk' |
| `owner_id` | UUID | FK → User | Responsible person |
| `deliverables` | TEXT | | Required deliverables |
| `notes` | TEXT | | Additional notes |
| `sort_order` | INTEGER | DEFAULT 0 | |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | NOT NULL | |

##### MilestoneDependency

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `milestone_id` | UUID | FK → Milestone, PK | |
| `depends_on_id` | UUID | FK → Milestone, PK | |
| `dependency_type` | ENUM | | 'finish_to_start', 'start_to_start' |

##### ProjectProcessLink

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `portfolio_item_id` | UUID | FK → PortfolioItem, PK | Project/workstream |
| `process_id` | UUID | FK → Process, PK | Affected process |
| `impact_type` | ENUM | | 'transforms', 'replaces', 'enhances' |
| `description` | TEXT | | Impact description |

#### 9.6.9 Change & Adoption Tables

##### AdoptionSurvey

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | |
| `portfolio_item_id` | UUID | FK → PortfolioItem | Related project/change |
| `name` | VARCHAR(255) | NOT NULL | Survey name |
| `description` | TEXT | | Description |
| `status` | ENUM | NOT NULL | 'draft', 'active', 'closed' |
| `frequency` | ENUM | | 'once', 'weekly', 'monthly', 'milestone' |
| `start_date` | DATE | | Survey period start |
| `end_date` | DATE | | Survey period end |
| `created_at` | TIMESTAMP | NOT NULL | |

##### SurveyQuestion

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `survey_id` | UUID | FK → AdoptionSurvey | |
| `question_text` | TEXT | NOT NULL | Question |
| `question_type` | ENUM | NOT NULL | 'scale', 'yes_no', 'text', 'multiple_choice' |
| `options` | JSONB | | For multiple choice |
| `is_required` | BOOLEAN | DEFAULT TRUE | |
| `sort_order` | INTEGER | DEFAULT 0 | |

##### SurveyResponse

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `survey_id` | UUID | FK → AdoptionSurvey | |
| `user_id` | UUID | FK → User | Respondent |
| `responses` | JSONB | NOT NULL | Question ID → Answer |
| `submitted_at` | TIMESTAMP | NOT NULL | |

##### KpiTracking (For Change Measurement)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `portfolio_item_id` | UUID | FK → PortfolioItem | Related project |
| `kpi_id` | UUID | FK → KpiDefinition | |
| `baseline_value` | DECIMAL | | Pre-change baseline |
| `target_value` | DECIMAL | NOT NULL | Target after change |
| `measurement_date` | DATE | NOT NULL | When measured |
| `measured_value` | DECIMAL | NOT NULL | Actual value |
| `notes` | TEXT | | Measurement notes |
| `created_at` | TIMESTAMP | NOT NULL | |

#### 9.6.10 Reference Catalogues

##### SystemCatalogue

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | |
| `name` | VARCHAR(255) | NOT NULL | System name |
| `description` | TEXT | | Description |
| `system_type` | ENUM | | 'erp', 'crm', 'portal', 'database', 'tool', 'other' |
| `vendor` | VARCHAR(255) | | Vendor name |
| `status` | ENUM | NOT NULL | 'evaluate', 'maintain', 'optimize', 'retire' |
| `created_at` | TIMESTAMP | NOT NULL | |

##### Agent (Enhanced Agent Catalogue)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | Tenant reference |
| `name` | VARCHAR(255) | NOT NULL | Agent name (e.g., "Order Entry Bot") |
| `description` | TEXT | | What the agent does |
| `agent_type` | ENUM | NOT NULL | 'rpa', 'ai_assistant', 'ai_agent', 'workflow', 'integration', 'document_ai', 'predictive' |
| `technology` | VARCHAR(255) | | Technology platform (e.g., "UiPath", "Claude", "Power Automate") |
| `vendor` | VARCHAR(255) | | Vendor/provider |
| `status` | ENUM | NOT NULL | 'identified', 'evaluating', 'approved', 'implementing', 'live', 'optimizing', 'retiring', 'retired' |
| `owner_id` | UUID | FK → User | Agent owner |
| `go_live_date` | DATE | | When deployed to production |
| `review_date` | DATE | | Next review date |
| `documentation_url` | VARCHAR(500) | | Link to agent documentation |
| `metrics` | JSONB | | Performance metrics (transactions/day, error rate, etc.) |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | NOT NULL | |

**Agent Types:**
- `rpa`: Robotic Process Automation (UI mimicry)
- `ai_assistant`: AI-powered human augmentation
- `ai_agent`: Autonomous AI agent with decision-making
- `workflow`: Automated workflow orchestration
- `integration`: System-to-system integration
- `document_ai`: Document processing (OCR, extraction)
- `predictive`: Predictive/analytical models

##### ProcessAgent (Process-Agent Linkage)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `process_id` | UUID | FK → Process | The process |
| `agent_id` | UUID | FK → Agent | The agent |
| `linkage_type` | ENUM | NOT NULL | 'current', 'future' |
| `automation_scope` | TEXT | | What part of process the agent handles |
| `automation_percentage` | INTEGER | CHECK (0-100) | Estimated % automated by this agent |
| `implementation_project_id` | UUID | FK → PortfolioItem | Project implementing this |
| `planned_go_live` | DATE | | Planned go-live for future agents |
| `actual_go_live` | DATE | | Actual go-live date |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | NOT NULL | |

##### AgenticOpportunity (Opportunity Tracking)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | Tenant reference |
| `process_id` | UUID | FK → Process | Related process |
| `title` | VARCHAR(255) | NOT NULL | Opportunity title |
| `description` | TEXT | | Detailed description |
| `agentic_potential` | ENUM | NOT NULL | 'low', 'medium', 'high' |
| `current_automation_level` | ENUM | NOT NULL | 'manual', 'assisted', 'semi_automated', 'fully_automated' |
| `target_automation_level` | ENUM | NOT NULL | 'manual', 'assisted', 'semi_automated', 'fully_automated' |
| `estimated_benefit` | TEXT | | Qualitative/quantitative benefit |
| `estimated_effort` | ENUM | | 'low', 'medium', 'high' |
| `complexity` | ENUM | | 'low', 'medium', 'high' |
| `priority_score` | DECIMAL | | Calculated priority |
| `status` | ENUM | NOT NULL | 'identified', 'evaluating', 'approved', 'project_created', 'in_progress', 'complete', 'rejected' |
| `linked_project_id` | UUID | FK → PortfolioItem | Project addressing this |
| `identified_by` | UUID | FK → User | Who identified |
| `identified_date` | DATE | NOT NULL | When identified |
| `source` | ENUM | | 'manual', 'riada', 'survey', 'ai_suggestion' |
| `source_reference_id` | UUID | | Source entity ID (RIADA item, survey, etc.) |
| `created_at` | TIMESTAMP | NOT NULL | |
| `updated_at` | TIMESTAMP | NOT NULL | |

##### RoleCatalogue

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | |
| `name` | VARCHAR(255) | NOT NULL | Role name (e.g., "Account Manager") |
| `description` | TEXT | | Role description |
| `role_type` | ENUM | | 'operational', 'management', 'executive', 'external' |
| `department` | VARCHAR(100) | | Department |
| `is_agent` | BOOLEAN | DEFAULT FALSE | Is this an AI/automation agent role |
| `status` | ENUM | NOT NULL | 'active', 'inactive' |
| `created_at` | TIMESTAMP | NOT NULL | |

##### (Similar structure for: SupplierCatalogue, ClientCatalogue, MarketCatalogue, CategoryCatalogue, PartnerCatalogue)

#### 9.6.11 Audit & History Tables

##### AuditLog

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | |
| `user_id` | UUID | FK → User | Who made change |
| `entity_type` | VARCHAR(50) | NOT NULL | Table name |
| `entity_id` | UUID | NOT NULL | Record ID |
| `action` | ENUM | NOT NULL | 'create', 'update', 'delete', 'view' |
| `changes` | JSONB | | Before/after for updates |
| `ip_address` | VARCHAR(50) | | Client IP |
| `user_agent` | VARCHAR(500) | | Browser/client |
| `created_at` | TIMESTAMP | NOT NULL | |

##### EntityVersion (For version control)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `entity_type` | VARCHAR(50) | NOT NULL | Table name |
| `entity_id` | UUID | NOT NULL | Record ID |
| `version` | INTEGER | NOT NULL | Version number |
| `data` | JSONB | NOT NULL | Full entity snapshot |
| `created_by` | UUID | FK → User | |
| `created_at` | TIMESTAMP | NOT NULL | |

#### 9.6.12 Document & Report Tables

##### Document

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | |
| `name` | VARCHAR(255) | NOT NULL | Document name |
| `file_path` | VARCHAR(500) | NOT NULL | Storage path (R2/OSS) |
| `file_type` | VARCHAR(50) | | 'pdf', 'docx', 'xlsx', 'png' |
| `file_size` | INTEGER | | Bytes |
| `entity_type` | VARCHAR(50) | | Attached to entity type |
| `entity_id` | UUID | | Attached to entity ID |
| `uploaded_by` | UUID | FK → User | |
| `created_at` | TIMESTAMP | NOT NULL | |

##### PublishedReport

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | Unique identifier |
| `organization_id` | UUID | FK → Organization | |
| `report_type` | ENUM | NOT NULL | 'process', 'process_family', 'value_stream', 'om_summary', 'custom' |
| `format` | ENUM | NOT NULL | 'pdf', 'html', 'docx' |
| `name` | VARCHAR(255) | NOT NULL | Report title |
| `scope` | JSONB | NOT NULL | Processes/items included |
| `options` | JSONB | | Report configuration |
| `file_path` | VARCHAR(500) | | Storage path for generated file |
| `version` | INTEGER | DEFAULT 1 | |
| `generated_by` | UUID | FK → User | |
| `generated_at` | TIMESTAMP | NOT NULL | |

#### 9.6.13 Indexes & Constraints

```sql
-- Key indexes for performance

-- Organization-scoped queries (RLS support)
CREATE INDEX idx_process_org ON process(organization_id);
CREATE INDEX idx_riada_org ON riada_item(organization_id);
CREATE INDEX idx_portfolio_org ON portfolio(organization_id);

-- Hierarchical queries
CREATE INDEX idx_process_parent ON process(parent_id);
CREATE INDEX idx_process_level ON process(organization_id, level);
CREATE INDEX idx_portfolio_item_parent ON portfolio_item(parent_id);

-- RIADA queries
CREATE INDEX idx_riada_status ON riada_item(organization_id, status);
CREATE INDEX idx_riada_type_severity ON riada_item(organization_id, type, severity);
CREATE INDEX idx_riada_owner ON riada_item(owner_id, status);
CREATE INDEX idx_riada_attachment ON riada_attachment(attachable_type, attachable_id);

-- Full-text search
CREATE INDEX idx_process_search ON process USING gin(to_tsvector('english', name || ' ' || description));
CREATE INDEX idx_riada_search ON riada_item USING gin(to_tsvector('english', title || ' ' || description));

-- Row-Level Security (RLS) Policies
ALTER TABLE process ENABLE ROW LEVEL SECURITY;
CREATE POLICY process_tenant_isolation ON process
  USING (organization_id = current_setting('app.current_org')::uuid);
-- (Similar policies for all tenant-scoped tables)
```

### 9.7 API Design

#### 9.7.1 RESTful API Structure

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/organizations` | GET, POST | List/create organizations |
| `/api/v1/business-models` | GET, POST | List/create business models |
| `/api/v1/business-models/{id}/components` | GET, POST | Canvas components |
| `/api/v1/processes` | GET, POST | List/create processes |
| `/api/v1/processes/{id}` | GET, PUT, DELETE | Process CRUD |
| `/api/v1/processes/{id}/children` | GET | Get child processes |
| `/api/v1/processes/{id}/riada` | GET, POST | RIADA items for process |
| `/api/v1/riada` | GET, POST | All RIADA items |
| `/api/v1/riada/{id}` | GET, PUT, DELETE | RIADA item CRUD |
| `/api/v1/portfolios` | GET, POST | List/create portfolios |
| `/api/v1/portfolios/{id}/items` | GET, POST | Portfolio items (hierarchy) |
| `/api/v1/projects/{id}` | GET, PUT | Project details |
| `/api/v1/projects/{id}/milestones` | GET, POST | Project milestones |
| `/api/v1/projects/{id}/budget` | GET, PUT | Budget tracking |
| `/api/v1/reports/generate` | POST | Generate PDF/HTML report |
| `/api/v1/search` | GET | Cross-entity search |
| `/api/v1/aggregate` | POST | Roll-up queries |

#### 9.7.2 Query & Aggregation API

```python
# Example: Aggregate RIADA across dimensions
POST /api/v1/aggregate
{
  "entity": "riada",
  "group_by": ["severity", "category"],
  "filters": {
    "type": ["Risk", "Issue"],
    "status": ["Open", "In Progress"]
  },
  "scope": {
    "process_ids": ["proc_001", "proc_002"],  # Optional
    "project_ids": ["proj_001"],               # Optional
    "include_children": true                   # Roll-up
  }
}

# Response
{
  "results": [
    {"severity": "Critical", "category": "System", "count": 3},
    {"severity": "High", "category": "Process", "count": 7},
    ...
  ],
  "total": 45
}
```

### 9.8 Integration Points

| Integration | Protocol | Purpose |
|-------------|----------|---------|
| **GitHub** | REST API + Webhooks | Repo sync, commit tracking, issue sync |
| **SSO Providers** | SAML 2.0 / OIDC | Enterprise SSO add-on (optional); primary auth is passwordless magic links per Section 6.2 |
| **Email** | SMTP / Resend API | Notifications, report distribution |
| **LLM APIs** | REST | Content generation, prompt library |
| **Export** | File generation | PDF, DOCX, XLSX export |
| **Import** | File parsing | Excel import (existing data migration) |

### 9.9 Security Architecture

| Layer | Measures |
|-------|----------|
| **Network** | Cloudflare WAF, DDoS protection, TLS 1.3 |
| **Authentication** | Passwordless magic links (primary), OAuth 2.0 / OIDC (enterprise SSO add-on), MFA, Session management |
| **Authorization** | RBAC, Row-Level Security, API key scoping |
| **Data** | Encryption at rest (AES-256), in transit (TLS) |
| **Audit** | Comprehensive audit logging, tamper-evident |
| **Compliance** | SOC 2 (Global), China Cybersecurity Law (China) |

### 9.10 Technology Stack Summary

#### Global SaaS Stack

```
Frontend:        Next.js 14+ (React) on Vercel
Backend:         FastAPI (Python 3.11+) on Railway
Database:        Supabase (PostgreSQL 15+)
Cache:           Upstash Redis
Storage:         Cloudflare R2
Auth:            Supabase Auth (magic links primary) + Clerk (enterprise SSO add-on)
Search:          Supabase FTS / Typesense
PDF Generation:  WeasyPrint
Background Jobs: Celery + Redis / Inngest
LLM:             OpenAI GPT-4 / Anthropic Claude
Monitoring:      Sentry + Vercel Analytics
CI/CD:           GitHub Actions
```

#### China Stack

```
Frontend:        Next.js 14+ (React) on Alibaba ECS
Backend:         FastAPI (Python 3.11+) on Alibaba ECS
Database:        Alibaba RDS (PostgreSQL)
Cache:           Alibaba Redis
Storage:         Alibaba OSS
Auth:            Alibaba IDaaS (magic links primary) or Keycloak (enterprise SSO)
Search:          Alibaba OpenSearch / Self-hosted
PDF Generation:  WeasyPrint
Background Jobs: Celery + Redis
LLM:             Alibaba Qwen / Baidu ERNIE
Monitoring:      Alibaba ARMS + Self-hosted Sentry
CI/CD:           Gitee CI / Jenkins
```

---

## 10. User Interface Design

### 10.1 Application Shell & Global Layout

#### 10.1.1 Shell Layout

The application uses a **collapsible sidebar** layout with a persistent header bar.

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│  HEADER BAR (persistent, full width)                                                      │
│  ┌────────┬──────────────────┬─────────────┬───────┬───────┬────────┬──────┬──────────┐ │
│  │ Org    │ Page Title /     │  🔍 Global  │ + New │  🔔   │ v1.8.2 │ Org  │ 👤 User  │ │
│  │ Logo   │ Breadcrumbs      │  Search     │       │ Notif │        │ Swit │ Avatar   │ │
│  └────────┴──────────────────┴─────────────┴───────┴───────┴────────┴──────┴──────────┘ │
├──────┬───────────────────────────────────────────────────────────────────────────────────┤
│ NAV  │                                                                                    │
│      │                                                                                    │
│ 300px│                         CONTENT AREA                                              │
│  or  │                                                                                    │
│ 64px │                   (Changes per screen/route)                                      │
│      │                                                                                    │
│      │                                                                                    │
│      │                                                                                    │
│      │                                                                                    │
└──────┴───────────────────────────────────────────────────────────────────────────────────┘
```

#### 10.1.2 Sidebar Navigation

| Property | Value |
|----------|-------|
| **Expanded Width** | 300px |
| **Collapsed Width** | 64px (icon-only) |
| **Default State** | Expanded on desktop, collapsed on tablet |
| **Toggle** | Chevron button at bottom of sidebar |
| **Behavior** | Smooth animation (200ms ease-in-out) |

**Sidebar Structure (Expanded):**

```
┌─────────────────────────────────┐
│  ◀ Process Catalogue            │  ← Collapse button + app name
├─────────────────────────────────┤
│                                 │
│  🏠  Home / Dashboard           │
│                                 │
│  ── DESIGN ──────────────────── │
│  📊  Process Canvas             │
│  📋  Process List               │
│  🎯  Business Model             │
│                                 │
│  ── OPERATE ─────────────────── │
│  ⚠️  Quality Logs (RIADA)       │
│  📁  Portfolio                  │
│  📈  Change & Adoption          │
│  📝  Surveys                    │
│                                 │
│  ── INTELLIGENCE ────────────── │
│  🤖  Prompt Library             │
│  📄  Reports                    │
│                                 │
│  ── MANAGE ──────────────────── │
│  📚  Reference Data             │
│  ⚙️  Settings                   │
│                                 │
├─────────────────────────────────┤
│  ❓  Help                       │
│  👤  Ralph Behnke               │
│      ralph@surity.co            │
└─────────────────────────────────┘
```

**Sidebar Structure (Collapsed):**

```
┌────────┐
│   ▶    │  ← Expand button
├────────┤
│  🏠    │
├────────┤
│  📊    │
│  📋    │
│  🎯    │
├────────┤
│  ⚠️    │
│  📁    │
│  📈    │
│  📝    │
├────────┤
│  🤖    │
│  📄    │
├────────┤
│  📚    │
│  ⚙️    │
├────────┤
│  ❓    │
│  👤    │
└────────┘
```

**Collapsed Behavior:** Hovering over a collapsed icon shows a tooltip with the label. Clicking navigates directly.

#### 10.1.3 Header Bar

The header bar is persistent across all screens and contains:

| Element | Position | Description |
|---------|----------|-------------|
| **Organization Logo** | Left | Current org logo (uploaded by admin) |
| **Page Title / Breadcrumbs** | Left-center | Current page context (e.g., "SOURCE → Product Dev → Silver Seal") |
| **Global Search** | Center | Search bar (Cmd+K shortcut), searches all entities |
| **Quick Action** | Center-right | "+ New" dropdown (New Process, New RIADA, New Project, etc.) |
| **Notifications** | Right | Bell icon with unread count badge |
| **Version** | Right | Application version number (e.g., "v1.8.2") |
| **Org Switcher** | Right | Dropdown to switch between organizations |
| **User Avatar** | Far right | User photo/initials, dropdown for Profile, Preferences, Logout |

#### 10.1.4 Organization Switcher

Users who belong to multiple organizations see an org switcher in the header:

```
┌─────────────────────────────┐
│  ▼ Surity                   │
├─────────────────────────────┤
│  ✓ Surity           Active  │
│    Acme Corp                │
│    Demo Sandbox             │
├─────────────────────────────┤
│  + Join Organization        │
└─────────────────────────────┘
```

Switching organizations reloads all data for the selected org context. No logout required.

#### 10.1.5 Global Search (Cmd+K)

**Trigger:** Click search bar or press Cmd+K (Ctrl+K on Windows)

```
┌─────────────────────────────────────────────────────────────┐
│  🔍  Search processes, RIADA items, projects, people...     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RECENT                                                     │
│  📊 L2-10: Brief                              Process      │
│  ⚠️ ISS-042: Order delay issue                RIADA        │
│  📁 PRJ-2026-003: Order Automation            Project      │
│                                                             │
│  ── or type to search ──                                    │
│                                                             │
│  Results grouped by entity type:                            │
│  📊 Processes (3 results)                                   │
│  ⚠️ RIADA Items (7 results)                                │
│  📁 Projects (2 results)                                    │
│  👤 People (1 result)                                       │
│  🤖 Prompts (4 results)                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Search Coverage:** Processes, RIADA items, Projects, People/users, Prompts, Reference data, Business Model entries, Survey templates.

**Scoped Search:** Each list view also has its own search bar filtering within that view only.

#### 10.1.6 Notification Center

**Bell icon** in header with unread count badge:

```
┌─────────────────────────────────────────────────┐
│  🔔 Notifications                    Mark All   │
├─────────────────────────────────────────────────┤
│                                                  │
│  ● RIADA item assigned to you          2m ago   │
│    ISS-042: Order delay — assigned by Jane      │
│                                                  │
│  ● Survey assigned                     1h ago   │
│    AI Fluency Assessment — due Feb 14           │
│                                                  │
│  ○ Project status changed              3h ago   │
│    PRJ-003 moved to "In Progress"               │
│                                                  │
│  ○ @mention in comment                 1d ago   │
│    Ralph mentioned you on L2-37                 │
│                                                  │
├─────────────────────────────────────────────────┤
│  View All Notifications →                        │
└─────────────────────────────────────────────────┘
```

**User-Configurable:** Each notification event type can be set to In-App, Email, or Both. At least one channel must be enabled per event type.

| Event | Default |
|-------|---------|
| RIADA item assigned to you | Both |
| RIADA item escalated | Both |
| Project status changed | In-App |
| Survey assigned to you | Both |
| New user registered (admin) | Email |
| Process status changed | In-App |
| Comment or @mention | Both |
| Prompt execution completed | In-App |

#### 10.1.7 Quick Action Menu

"+ New" button in header opens a dropdown:

```
┌──────────────────────────────┐
│  + New                       │
├──────────────────────────────┤
│  📊 New Process              │
│  ⚠️ New RIADA Item           │
│  📁 New Project              │
│  📝 New Survey               │
│  🤖 Run Prompt               │
├──────────────────────────────┤
│  📥 Import Data              │
└──────────────────────────────┘
```

---

### 10.2 Process Canvas (Primary Navigation)

The **Process Canvas** is the primary visual interface for navigating the process hierarchy. It uses a swimlane layout that displays processes in a spatial hierarchy.

#### 10.2.1 Canvas Layout Structure

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    PROCESS CANVAS                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐    │
│  │ LEVEL 0: VALUE STREAM (Horizontal - Left to Right)                                       │    │
│  │                                                                                          │    │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐              │    │
│  │  │  SOURCE  │ → │ DEVELOP  │ → │ EXECUTE  │ → │ SUPPORT  │ → │ GOVERN   │              │    │
│  │  │   (L0)   │   │   (L0)   │   │   (L0)   │   │   (L0)   │   │   (L0)   │              │    │
│  │  └──────────┘   └────┬─────┘   └──────────┘   └──────────┘   └──────────┘              │    │
│  │                      │                                                                   │    │
│  └──────────────────────┼───────────────────────────────────────────────────────────────────┘    │
│                         │                                                                        │
│  ┌──────────────────────▼───────────────────────────────────────────────────────────────────┐   │
│  │ LEVEL 1: PROCESS AREAS (Horizontal - Aligned under selected L0)                          │   │
│  │                                                                                          │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │   │
│  │  │ PRODUCT DEV &   │  │ PACKAGING       │  │ INSTRUCTION     │  │ E-COMMERCE DATA │    │   │
│  │  │ APPROVAL (L1)   │  │ DEVELOPMENT (L1)│  │ MANUAL DEV (L1) │  │ & IMAGE (L1)    │    │   │
│  │  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘    │   │
│  │           │                    │                    │                    │              │   │
│  └───────────┼────────────────────┼────────────────────┼────────────────────┼──────────────┘   │
│              │                    │                    │                    │                   │
│  ┌───────────▼────────────────────▼────────────────────▼────────────────────▼──────────────┐   │
│  │ LEVEL 2: PROCESSES (Vertical columns - Aligned under each L1)                           │   │
│  │                                                                                          │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │   │
│  │  │ Silver Seal     │  │ Physical        │  │ IM Development  │  │ PIMDAM Process  │    │   │
│  │  │ Process      [▼]│  │ Packaging    [▼]│  │ & Translation[▼]│  │              [▼]│    │   │
│  │  ├─────────────────┤  ├─────────────────┤  └─────────────────┘  └─────────────────┘    │   │
│  │  │ • Sample Submit │  │ • Material Sel  │                                              │   │
│  │  │ • Silver Review │  │ • Packaging Test│   (L3 items shown                            │   │
│  │  │ • Pre-prod Test │  │ • Environmental │    when L2 expanded)                         │   │
│  │  └─────────────────┘  └─────────────────┘                                              │   │
│  │                                                                                          │   │
│  │  ┌─────────────────┐  ┌─────────────────┐                                              │   │
│  │  │ Technical File  │  │ Artwork Gen &   │                                              │   │
│  │  │ Compilation  [▼]│  │ Approval     [▼]│                                              │   │
│  │  ├─────────────────┤  ├─────────────────┤                                              │   │
│  │  │ • Test Reports  │  │ • AWCL Complete │                                              │   │
│  │  │ • Certificates  │  │ • Artwork Create│                                              │   │
│  │  │ • Declaration   │  │ • Die Cut Apprvl│                                              │   │
│  │  │ • REACH Check   │  │ • Barcode Verify│                                              │   │
│  │  └─────────────────┘  │ • Print Proof   │                                              │   │
│  │                       │ • Carton Marking│                                              │   │
│  │  ┌─────────────────┐  └─────────────────┘                                              │   │
│  │  │ Gold Seal       │                                                                    │   │
│  │  │ Process      [>]│  (Collapsed - click to expand)                                    │   │
│  │  └─────────────────┘                                                                    │   │
│  │                                                                                          │   │
│  │  ┌─────────────────┐                                                                    │   │
│  │  │ Testing &       │                                                                    │   │
│  │  │ Validation   [>]│                                                                    │   │
│  │  └─────────────────┘                                                                    │   │
│  │                                                                                          │   │
│  └──────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 10.2.2 Canvas Hierarchy Behavior

| Level | Display | Orientation | Behavior |
|-------|---------|-------------|----------|
| **L0** | Always visible | Horizontal (left → right) | Click to filter L1s below |
| **L1** | Below selected L0 | Horizontal (left → right) | Click to highlight L2 column |
| **L2** | Below L1s | Vertical columns (top → bottom) | Click to expand/collapse L3s |
| **L3** | Nested under L2 | Vertical list (expandable) | Click to expand L4s |
| **L4** | Nested under L3 | Nested menu/accordion | Click to expand L5s |
| **L5** | Nested under L4 | Nested menu/accordion | Click to open detail |

#### 10.2.3 Canvas Interaction Patterns

| Interaction | Action |
|-------------|--------|
| **Click L0** | Scrolls/filters to show L1s under that L0 |
| **Click L1** | Highlights the L2 column; shows breadcrumb |
| **Click L2** | Expands to show L3 items as nested list |
| **Click L3** | Expands to show L4 items (if any) |
| **Click L4** | Expands to show L5 items (if any) |
| **Click any item name** | Opens process detail panel/page |
| **Hover** | Shows tooltip with description, RAG status |
| **Right-click** | Context menu (Edit, View RIADA, Run Prompt, etc.) |
| **Drag & Drop** | Reorder processes within same parent (admin only) |

#### 10.2.4 Canvas Visual Indicators

| Indicator | Meaning |
|-----------|---------|
| **RAG dot** | Green/Amber/Red status indicator on process card |
| **Issue count badge** | Number of open issues (e.g., "3") |
| **Risk count badge** | Number of open risks |
| **Project link icon** | Process is linked to active project(s) |
| **Primary/Secondary icon** | Distinguish primary vs secondary processes |
| **Expand arrow [▼]** | Has children, currently expanded |
| **Collapse arrow [>]** | Has children, currently collapsed |
| **Info icon (i)** | Click to see quick info panel |

#### 10.2.5 Canvas Toolbar

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  [🔍 Search...]  [Filter ▼]  [View: Canvas ▼]  [Primary ○ Secondary ○ Both ●]          │
│                                                                                          │
│  Filters: [Market ▼] [Client ▼] [Category ▼] [Owner ▼] [RAG Status ▼] [Clear All]      │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

| Toolbar Feature | Description |
|-----------------|-------------|
| **Search** | Search processes by name, code, description |
| **Filter** | Filter by Business Model dimensions (Market, Client, Category) |
| **View Toggle** | Switch between Canvas, List, Tree views |
| **Primary/Secondary** | Show Primary, Secondary, or Both process types |
| **RAG Filter** | Show only Green, Amber, or Red processes |
| **Owner Filter** | Filter by Process Owner |

#### 10.2.6 Canvas Background & Navigation

**Background:** Plain white with subtle dot grid pattern (light grey dots at 20px intervals, opacity 0.15). Signals a workspace environment while remaining clean.

**Canvas Navigation Controls:**

| Control | Trigger | Description |
|---------|---------|-------------|
| **Zoom In/Out** | Ctrl+scroll / pinch | Zoom range: 25% — 200%, default 100% |
| **Pan** | Click-drag on background | Move the canvas viewport |
| **Mini-map** | Always visible (bottom-right) | Small overview showing viewport position |
| **Fit to View** | Button in toolbar | Zooms/pans to show all visible processes |
| **Zoom Indicator** | Toolbar display | Shows current zoom % with +/– buttons |

```
┌──────────────────────────────────────────────────────────┐
│  Canvas Toolbar (right side)                             │
│                                                          │
│  [Card Size: S ○ M ● L ○]  [🔍 75%  + −]  [⛶ Fit]     │
│                                                          │
│                                          ┌──────────┐   │
│                                          │ ░░▓▓░░░░ │   │
│                                          │ ░░▓▓░░░░ │   │
│                                          │ ░░░░░░░░ │   │
│                                          └──────────┘   │
│                                           Mini-map      │
└──────────────────────────────────────────────────────────┘
```

#### 10.2.7 Process Card Sizing

Users can select card size via a toggle in the canvas toolbar:

| Size | Dimensions | Content Shown |
|------|------------|---------------|
| **Small** | ~120×60px | Process code + name only |
| **Medium** | ~160×80px | Code, name, RAG dots (SPRD) |
| **Large** | ~200×100px | Code, name, RAG dots, issue count badge, owner avatar |

```
Small:                  Medium:                     Large:
┌──────────────┐       ┌───────────────────┐       ┌────────────────────────┐
│ L2-10: Brief │       │ L2-10: Brief      │       │ L2-10: Brief       👤 │
└──────────────┘       │ 🟢 🟡 🟢 🟢      │       │ 🟢 🟡 🟢 🟢     ⚠️3 │
                       └───────────────────┘       │ Sourcing Merch         │
                                                   └────────────────────────┘
```

Default: **Medium**. User preference persisted across sessions.

#### 10.2.8 L3/L4/L5 Inline Expansion

When a user clicks an L2 process card, its L3 children expand **inline** below the card, pushing canvas content down. L4/L5 nest further inline.

```
┌───────────────────┐
│ L2-10: Brief      │  ← Click to expand
│ 🟢 🟡 🟢 🟢      │
└───────┬───────────┘
        │
        ├── ┌─────────────────────┐
        │   │ L3-01: Brief Create │
        │   │ 🟢 🟢 🟡 🟢        │
        │   └─────────┬───────────┘
        │             │
        │             ├── L4-01: Template Selection
        │             ├── L4-02: Data Entry
        │             └── L4-03: Review & Submit
        │
        ├── ┌─────────────────────┐
        │   │ L3-02: Brief Review │
        │   │ 🟢 🟢 🟢 🟢        │
        │   └─────────────────────┘
        │
        └── ┌──────────────────────┐
            │ L3-03: Brief Approve │
            │ 🟡 🟢 🟢 🟢         │
            └──────────────────────┘
```

**Behavior:**
- Click L2 card → expand/collapse L3 children
- Click L3 item → expand/collapse L4 children
- Click L4 item → expand/collapse L5 children
- Indentation increases per level (20px per level)
- Smooth animation (150ms ease-out)
- Multiple L2 cards can be expanded simultaneously

#### 10.2.9 Canvas Empty State

When an organization has no processes, the canvas displays:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                                                                             │
│                     📊                                                      │
│                                                                             │
│              Your Process Canvas is empty                                   │
│                                                                             │
│     Start building your process hierarchy to map your                       │
│     operating model and identify opportunities.                             │
│                                                                             │
│     ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│     │ ✏️ Start from    │  │ 📋 Use a        │  │ 📥 Upload       │         │
│     │   Scratch        │  │   Template      │  │   Processes     │         │
│     │                 │  │                 │  │                 │         │
│     │ Create your     │  │ Choose from     │  │ Import from     │         │
│     │ first L0 value  │  │ pre-built       │  │ CSV, Excel, or  │         │
│     │ stream          │  │ templates       │  │ existing data   │         │
│     └─────────────────┘  └─────────────────┘  └─────────────────┘         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 10.3 Alternative Process Views

#### 10.3.1 Tree View

Hierarchical tree navigator (traditional folder structure):

```
▼ SOURCE (L0)
  ▼ Client Intake & Commercial Setup (L1)
    ▼ Brief (L2)
      ▼ Brief Creation (L3)
        > Brief Template Selection (L4)
        > Brief Data Entry (L5)
      > Brief Review (L3)
      > Brief Approval (L3)
    > Quote (L2)
    > Vendor Engagement (L2)
  > Range Development & Selection (L1)
▼ DEVELOP (L0)
  ...
```

#### 10.3.2 List View

Flat searchable/sortable table:

| Code | Name | Level | Parent | Owner | RAG | Issues | Type |
|------|------|-------|--------|-------|-----|--------|------|
| L0-02 | DEVELOP | L0 | — | Sarah | 🟡 | 5 | Primary |
| L1-08 | Product Development | L1 | DEVELOP | John | 🟢 | 0 | Primary |
| L2-25 | Silver Seal Process | L2 | Product Dev | Amy | 🔴 | 3 | Primary |
| L3-45 | Sample Submission | L3 | Silver Seal | Amy | 🟡 | 1 | Primary |

#### 10.3.3 Card View

Grid of process cards (useful for L2 level browsing):

```
┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
│ 🟢 L2-25          │  │ 🟡 L2-26          │  │ 🔴 L2-27          │
│ Silver Seal       │  │ Technical File    │  │ Gold Seal         │
│ Process           │  │ Compilation       │  │ Process           │
│                   │  │                   │  │                   │
│ Owner: Amy        │  │ Owner: John       │  │ Owner: Sarah      │
│ Issues: 0         │  │ Issues: 2         │  │ Issues: 5         │
│ [View] [Edit]     │  │ [View] [Edit]     │  │ [View] [Edit]     │
└───────────────────┘  └───────────────────┘  └───────────────────┘
```

---

### 10.4 Process Detail View

When a process is selected, display detailed information:

#### 10.4.1 Detail View Layout

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  ← Back to Canvas                                          [Edit] [AI Assist] [Export]  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  LEVEL 2                                                                    🟡 AMBER    │
│  ══════════════════════════════════════════════════════════════════════════════════     │
│  L2-25: Silver Seal Process                                                             │
│                                                                                          │
│  SOURCE → Product Development & Approval → Silver Seal Process                          │
│  (Breadcrumb showing L0 → L1 → L2)                                                      │
│                                                                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  [Overview] [Operating Model] [RIADA] [Projects] [History] [Prompts]                    │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │ OVERVIEW TAB                                                                     │   │
│  │                                                                                   │   │
│  │ Description:                                                                      │   │
│  │ The Silver Seal process validates product samples meet quality standards         │   │
│  │ before proceeding to full production testing...                                  │   │
│  │                                                                                   │   │
│  │ ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐                │   │
│  │ │ SYSTEM      🟢   │  │ PEOPLE      🟡   │  │ PROCESS     🟡   │                │   │
│  │ │ Good            │  │ Understaffed    │  │ Needs docs      │                │   │
│  │ └──────────────────┘  └──────────────────┘  └──────────────────┘                │   │
│  │                                                                                   │   │
│  │ ┌──────────────────┐                                                             │   │
│  │ │ DATA        🟢   │                                                             │   │
│  │ │ Accurate        │                                                             │   │
│  │ └──────────────────┘                                                             │   │
│  │                                                                                   │   │
│  │ Business Model Links:                                                            │   │
│  │ Markets: UK, Benelux, Australia                                                  │   │
│  │ Categories: Technical, Showroom                                                  │   │
│  │ Clients: Bunnings, Selco, Maxeda                                                │   │
│  │                                                                                   │   │
│  │ Child Processes (L3):                                                            │   │
│  │ • Sample Submission (3 issues)                                                   │   │
│  │ • Silver Seal Review                                                             │   │
│  │ • Pre-production Testing (1 risk)                                               │   │
│  │                                                                                   │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 10.4.2 Detail View Tabs

| Tab | Content |
|-----|---------|
| **Overview** | Description, RAG status (SPRD), Business Model links, Child processes |
| **Operating Model** | RACI, KPIs, Policies, Systems, Timing, Governance, Security, Data |
| **RIADA** | Risks, Issues, Actions, Dependencies, Assumptions for this process |
| **Projects** | Linked projects affecting this process |
| **History** | Audit log, version history |
| **Prompts** | Run prompts, view prompt history for this process |

---

### 10.5 Dashboard Views

#### 10.5.1 Executive Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  EXECUTIVE DASHBOARD                                                    [Export] [⚙️]   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐ │
│  │ PROCESS HEALTH          │  │ RIADA SUMMARY           │  │ PORTFOLIO STATUS        │ │
│  │                         │  │                         │  │                         │ │
│  │  🟢 65 Green            │  │  🔴 Critical: 3         │  │  Active Projects: 12    │ │
│  │  🟡 45 Amber            │  │  🟠 High: 12            │  │  On Track: 8            │ │
│  │  🔴 12 Red              │  │  🟡 Medium: 28          │  │  At Risk: 3             │ │
│  │                         │  │  🟢 Low: 45             │  │  Delayed: 1             │ │
│  │  [View Details]         │  │  [View Details]         │  │  [View Details]         │ │
│  └─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘ │
│                                                                                          │
│  ┌─────────────────────────────────────────────┐  ┌─────────────────────────────────┐   │
│  │ PROCESS RAG HEATMAP (L0 × Dimension)        │  │ TOP 10 RED PROCESSES            │   │
│  │                                              │  │                                 │   │
│  │         System People Process Data          │  │ 1. Gold Seal Process     🔴🔴🔴 │   │
│  │ SOURCE    🟢     🟢     🟡     🟢           │  │ 2. Order Confirmation    🔴🔴   │   │
│  │ DEVELOP   🟡     🟡     🔴     🟢           │  │ 3. Inspection Scheduling 🔴🟡   │   │
│  │ EXECUTE   🟢     🔴     🟡     🟡           │  │ 4. ...                          │   │
│  │ SUPPORT   🟢     🟢     🟢     🟡           │  │                                 │   │
│  │                                              │  │ [View All]                      │   │
│  └─────────────────────────────────────────────┘  └─────────────────────────────────┘   │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │ AI FLUENCY DISTRIBUTION                     │ ADOPTION SCORES (Active Changes)  │   │
│  │                                              │                                    │   │
│  │  Beginner ████░░░░░░░░░░░░░░░░░░░░░ 15%    │  Project A: ████████░░ 78%        │   │
│  │  Novice   ████████░░░░░░░░░░░░░░░░░ 25%    │  Project B: ██████████ 92%        │   │
│  │  Intermed ████████████░░░░░░░░░░░░░ 35%    │  Project C: ████░░░░░░ 45%        │   │
│  │  Advanced ██████░░░░░░░░░░░░░░░░░░░ 18%    │                                    │   │
│  │  Expert   ██░░░░░░░░░░░░░░░░░░░░░░░  7%    │  [View All]                        │   │
│  │                                              │                                    │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 10.5.2 RIADA Dashboard

| Widget | Content |
|--------|---------|
| **Summary Cards** | Count by type (Risk, Issue, Action, Dependency, Assumption) |
| **Severity Distribution** | Bar chart by Critical/High/Medium/Low |
| **Category Breakdown** | Pie chart by People/Process/System/Data |
| **Trend Chart** | Line chart of open items over time |
| **Overdue Actions** | List of overdue items |
| **By Process Area** | Heatmap of RIADA by L0/L1 |
| **By Owner** | Items grouped by assigned owner |

#### 10.5.3 Portfolio Dashboard

| Widget | Content |
|--------|---------|
| **Portfolio Summary** | Projects by status (Planning, Active, Complete) |
| **RAG Overview** | Projects by RAG status |
| **Timeline View** | Gantt-style view of project milestones |
| **Budget Summary** | Total budget, spend, forecast |
| **Benefits Tracker** | Target vs realized benefits |
| **WSVF Rankings** | Top priority projects by WSVF score |
| **Resource Allocation** | Resources assigned across projects |

#### 10.5.4 Survey Dashboard

| Widget | Content |
|--------|---------|
| **Active Surveys** | Currently open surveys with response rates |
| **AI Fluency Overview** | AFI distribution, trend over time |
| **Operating Model Health** | RAG summary from latest OM survey |
| **Change Readiness** | Readiness scores for upcoming changes |
| **Adoption Tracking** | Adoption scores for recent changes |
| **Response Rates** | Survey completion rates |

---

### 10.6 Report Types

#### 10.6.1 Standard Reports (Pre-Built)

| Report | Description | Output |
|--------|-------------|--------|
| **Process Catalogue Report** | Full process hierarchy with details | PDF, HTML |
| **Operating Model Report** | RACI, KPIs, Policies for selected processes | PDF, HTML |
| **RIADA Register** | All RIADA items with filters | PDF, Excel |
| **Portfolio Status Report** | Project status, milestones, RAG | PDF, HTML |
| **Executive Summary** | High-level health across all components | PDF |
| **AI Fluency Report** | AFI scores by role, team, process | PDF, Excel |
| **Change Readiness Report** | Readiness scores with breakdown | PDF |
| **Adoption Report** | Adoption evidence and scores | PDF |
| **Audit Trail Report** | Change history for compliance | PDF, Excel |
| **Agentic Opportunity Register** | All automation opportunities with prioritization | PDF, Excel |
| **Automation Coverage Report** | Current vs target automation levels by process | PDF, Excel |
| **Agent Catalogue Report** | All agents with status and linked processes | PDF, Excel |

#### 10.6.2 Custom Report Builder

| Feature | Description |
|---------|-------------|
| **Select Scope** | Choose processes, projects, date range |
| **Choose Sections** | Toggle which sections to include |
| **Add Filters** | Filter by market, client, category, owner |
| **Include Charts** | Select which visualizations to include |
| **Branding** | Add logo, set colors |
| **Schedule** | Set up recurring report generation |
| **Distribution** | Email to stakeholders automatically |

#### 10.6.3 Export Formats

| Format | Use Case |
|--------|----------|
| **PDF** | Professional documents, sharing, printing |
| **HTML** | Web viewing, embedding |
| **Excel** | Data analysis, further manipulation |
| **Word (DOCX)** | Editable documents |
| **Markdown** | Technical documentation |
| **JSON/CSV** | Data export, integration |

---

### 10.7 Heatmap & Overlay System

The Process Canvas supports **overlays** that color-code processes based on different dimensions, enabling powerful visual analysis.

#### 10.7.1 Display Modes

Users can toggle between two display modes when an overlay is active:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  DISPLAY MODE                                                                    │
│                                                                                  │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐              │
│  │  ○ SHOW ALL PROCESSES       │  │  ● SHOW MATCHING ONLY       │              │
│  │                             │  │                             │              │
│  │  All processes visible.     │  │  Only processes matching    │              │
│  │  Matching processes are     │  │  the filter are displayed.  │              │
│  │  color-coded; non-matching  │  │  Non-matching processes     │              │
│  │  shown in grey/neutral.     │  │  are hidden from view.      │              │
│  │                             │  │                             │              │
│  │  Use when: You want to see  │  │  Use when: You want to      │              │
│  │  context of where matches   │  │  focus only on relevant     │              │
│  │  sit within the full        │  │  processes without visual   │              │
│  │  process landscape.         │  │  clutter.                   │              │
│  └─────────────────────────────┘  └─────────────────────────────┘              │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

| Mode | Behavior | Use Case |
|------|----------|----------|
| **Show All Processes** | Full canvas visible; matching processes colored, non-matching greyed out | See context, understand where issues exist relative to full landscape |
| **Show Matching Only** | Canvas collapses to show only matching processes; non-matching hidden | Focus on specific subset, reduce visual noise, export filtered view |

**Visual Example - RIADA Overlay (RED Issues):**

**Show All Processes Mode:**
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  L0: SOURCE        DEVELOP         EXECUTE         SUPPORT         GOVERN      │
│      (grey)        (grey)          (grey)          (grey)          (grey)      │
│                                                                                  │
│  L1: ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                        │
│      │Product  │  │Packaging│  │Order    │  │Finance  │                        │
│      │Dev(grey)│  │Dev(grey)│  │Mgmt 🔴  │  │(grey)   │                        │
│      └─────────┘  └─────────┘  └─────────┘  └─────────┘                        │
│                                                                                  │
│  L2: ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                        │
│      │Silver   │  │Physical │  │Order 🔴 │  │Invoice  │                        │
│      │Seal     │  │Packaging│  │Confirm  │  │(grey)   │                        │
│      │(grey)   │  │(grey)   │  │         │  │         │                        │
│      └─────────┘  └─────────┘  └─────────┘  └─────────┘                        │
│      ┌─────────┐  ┌─────────┐  ┌─────────┐                                     │
│      │Tech File│  │Artwork  │  │Inspect  │                                     │
│      │(grey)   │  │(grey)   │  │🔴       │                                     │
│      └─────────┘  └─────────┘  └─────────┘                                     │
│                                                                                  │
│  Showing: 3 of 137 processes have RED Issues                                    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Show Matching Only Mode:**
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  L0: EXECUTE                                                                     │
│                                                                                  │
│  L1: ┌─────────────────┐                                                        │
│      │ Order Mgmt 🔴   │                                                        │
│      └─────────────────┘                                                        │
│                                                                                  │
│  L2: ┌─────────────────┐  ┌─────────────────┐                                  │
│      │ Order Confirm 🔴│  │ Inspection 🔴   │                                  │
│      │ 3 Critical      │  │ 2 Critical      │                                  │
│      └─────────────────┘  └─────────────────┘                                  │
│                                                                                  │
│  Showing: 3 processes with RED Issues (134 hidden)                              │
│  [Show All Processes] to see full context                                       │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### 10.7.2 Overlay Types

##### Overlay 1: RIADA (Issues, Risks, Actions, Dependencies, Assumptions)

**Purpose:** Show processes with quality/risk items using severity color coding

| Filter | Options |
|--------|---------|
| **RIADA Type** | Issues, Risks, Actions, Dependencies, Assumptions, All |
| **Category** | People, Process, System, Data, All |
| **Severity** | Critical, High, Medium, Low, All |
| **Status** | Open, In Progress, Overdue, All Open |

**Color Scheme:**

| Condition | Color | Meaning |
|-----------|-------|---------|
| Critical items present | 🔴 Red | Immediate attention |
| High items present | 🟠 Orange | Urgent |
| Medium items present | 🟡 Amber | Needs attention |
| Low items only | 🔵 Blue | Monitor |
| No matching items | ⬜ Grey (Show All) / Hidden (Matching Only) | Clean |

**Example Queries:**
- "Show all processes with **System Issues**" → Filter: Type=Issues, Category=System
- "Show only processes with **Critical or High Risks**" → Filter: Type=Risks, Severity=Critical+High, Mode=Matching Only
- "Show all processes with **Overdue Actions**" → Filter: Type=Actions, Status=Overdue
- "Show processes with **People Issues**" → Filter: Type=Issues, Category=People

---

##### Overlay 2: Project Scope

**Purpose:** Highlight processes impacted by a selected project

| Filter | Options |
|--------|---------|
| **Project** | Select from active projects |
| **Impact Type** | Transforms, Replaces, Enhances, All |
| **Change State** | In Progress, Planned, Completed |

**Color Scheme:**

| Condition | Color | Meaning |
|-----------|-------|---------|
| Directly impacted | 🟣 Purple (solid) | In scope - direct change |
| Indirectly impacted | 🟣 Purple (light) | In scope - downstream effect |
| Not impacted | ⬜ Grey / Hidden | Out of scope |

**Example Queries:**
- "Show scope of **Order Management Automation** project" → Full canvas with in-scope highlighted
- "Show ONLY processes in **Project X** scope" → Mode=Matching Only
- "Compare scope of **Project A** vs **Project B**" → Multi-select with different colors

---

##### Overlay 3: System

**Purpose:** Show which processes use a selected system

| Filter | Options |
|--------|---------|
| **System** | Select from System Catalogue |
| **Usage Type** | Primary System, Supporting System, All |
| **System Status** | Evaluate, Maintain, Optimize, Retire |

**Color Scheme:**

| Condition | Color | Meaning |
|-----------|-------|---------|
| Primary system | 🔵 Blue (solid) | Core dependency |
| Supporting system | 🔵 Blue (light) | Uses but not primary |
| Not using system | ⬜ Grey / Hidden | No relationship |

**Example Queries:**
- "Show all processes using **ERP**" → See ERP footprint across organization
- "Show ONLY processes supported by **ERP**" → Mode=Matching Only, focused view
- "Show processes using systems marked for **Retirement**" → Status=Retire

---

##### Overlay 4: Role (RACI)

**Purpose:** Show processes where a role is involved, filtered by RACI responsibility

| Filter | Options |
|--------|---------|
| **Role** | Select from Role Catalogue |
| **RACI** | Responsible, Accountable, Consulted, Informed, Any |
| **State** | Current, Future, Both |

**Color Scheme:**

| RACI | Color | Meaning |
|------|-------|---------|
| Responsible | 🟢 Green | Does the work |
| Accountable | 🔴 Red | Owns the outcome |
| Consulted | 🟡 Amber | Provides input |
| Informed | 🔵 Blue | Kept informed |
| Multiple RACI | 🟣 Purple | Multiple responsibilities |

**Example Queries:**
- "Show all processes where **Sourcing Manager** is **Accountable**" → Role=Sourcing Manager, RACI=A
- "Show ONLY processes where **QA Inspector** is **Responsible**" → Mode=Matching Only
- "Compare **Current** vs **Future** RACI for **Data Analyst**"

---

##### Overlay 5: Business Model

**Purpose:** Show processes linked to specific Business Model dimensions

| Filter | Options |
|--------|---------|
| **Dimension** | Market, Client, Category, Partner, Channel |
| **Value** | Select specific value(s) |

**Color Scheme:**

| Condition | Color |
|-----------|-------|
| Linked to selected value(s) | 🟢 Green (intensity by link count) |
| Not linked | ⬜ Grey / Hidden |

**Example Queries:**
- "Show all processes serving **UK Market**"
- "Show ONLY processes for **Bunnings** client" → Mode=Matching Only
- "Show processes handling **Technical** category products"

---

##### Overlay 6: Ownership

**Purpose:** Show processes by owner or sponsor

| Filter | Options |
|--------|---------|
| **Ownership Type** | Process Owner, Sponsor, Either |
| **Person** | Select user(s) |
| **Vacant** | Show processes with no owner assigned |

**Color Scheme:**

| Condition | Color |
|-----------|-------|
| Owned by selected person | 🟢 Green |
| Vacant/Unassigned | 🔴 Red |
| Different owner | ⬜ Grey / Hidden |

**Example Queries:**
- "Show all processes owned by **Sarah**"
- "Show ONLY processes with **no owner assigned**" → Vacant=true, Mode=Matching Only
- "Show ownership distribution across teams"

---

##### Overlay 7: Survey Results

**7a. Operating Model Survey (SPRD)**

| Filter | Options |
|--------|---------|
| **Dimension** | System, People, Process, Data, Overall |
| **Survey Instance** | Select survey |
| **RAG Filter** | Green, Amber, Red, All |

**Example Queries:**
- "Show **System** RAG from latest Operating Model survey"
- "Show ONLY processes that are **RED on People dimension**" → Mode=Matching Only

**7b. AI Fluency**

| Filter | Options |
|--------|---------|
| **Metric** | Average AFI, % Advanced+, % Beginner |
| **Threshold** | Custom threshold |

**Example:** "Show ONLY processes with teams having **AFI < 40**"

**7c. Adoption Evidence**

| Filter | Options |
|--------|---------|
| **Project** | Select project |
| **Metric** | Overall Adoption, Process/Role/KPI Evidence |
| **Threshold** | Adoption % threshold |

**Example:** "Show ONLY processes with **adoption < 60%**" for intervention

---

##### Overlay 8: Change Impact

**Purpose:** Compare current vs future state

| Filter | Options |
|--------|---------|
| **Comparison** | Current vs Future RACI, Systems, KPIs |
| **Change Type** | Added, Removed, Modified, Unchanged |

**Color Scheme:**

| Change | Color |
|--------|-------|
| Added (new) | 🟢 Green |
| Removed | 🔴 Red |
| Modified | 🟡 Amber |
| Unchanged | ⬜ Grey / Hidden |

**Example:** "Show ONLY processes with **RACI changes** planned" → Mode=Matching Only

---

##### Overlay 9: Dependency

**Purpose:** Show process dependencies and linkages

| Filter | Options |
|--------|---------|
| **Selected Process** | Choose starting process |
| **Direction** | Upstream, Downstream, Both |
| **Link Type** | Supports, Depends On, Related |

**Example:** "Show all processes **upstream** of Order Confirmation"

---

##### Overlay 10: Primary/Secondary

**Purpose:** Distinguish primary value chain from secondary support processes

| Filter | Options |
|--------|---------|
| **Process Type** | Primary, Secondary, Both |
| **Secondary Domain** | IT, HR, Legal, Treasury, Portfolio Delivery |

**Example:** "Show ONLY **Secondary - IT** processes" → Mode=Matching Only

---

##### Overlay 11: Agentic Opportunity

**Purpose:** Visualize automation potential and current automation levels across processes

| Filter | Options |
|--------|---------|
| **View Mode** | Potential, Current Level, Gap, Agent Coverage |
| **Agentic Potential** | High, Medium, Low, None |
| **Current Automation** | Manual, Assisted, Semi-Automated, Fully-Automated |
| **Target Automation** | Manual, Assisted, Semi-Automated, Fully-Automated |
| **Gap Size** | Large (>50%), Medium (25-50%), Small (<25%), None |
| **Has Agent** | Yes, No, Planned |
| **Opportunity Status** | Not Started, Evaluating, Project Created, In Progress, Complete |

**Color Schemes:**

*View Mode: Potential*
| Potential | Color |
|-----------|-------|
| High | 🟣 Purple (solid) |
| Medium | 🟣 Purple (light) |
| Low | 🔵 Blue |
| None | ⬜ Grey |

*View Mode: Current Automation Level*
| Level | Color |
|-------|-------|
| Fully-Automated | 🟢 Green |
| Semi-Automated | 🟡 Amber |
| Assisted | 🟠 Orange |
| Manual | 🔴 Red |

*View Mode: Gap (Current vs Target)*
| Gap | Color |
|-----|-------|
| Large (>50%) | 🔴 Red |
| Medium (25-50%) | 🟡 Amber |
| Small (<25%) | 🟢 Green |
| None (at target) | 🔵 Blue |

**Example Queries:**
- "Show all processes with **High agentic potential**"
- "Show ONLY **Manual** processes" → Mode=Matching Only
- "Show processes with **Large automation gap**"
- "Show processes with **no agent** but **High potential**"
- "Show processes where automation projects are **In Progress**"

---

##### Overlay 12: Custom/Combined

**Purpose:** User-defined combinations with AND/OR logic

| Feature | Description |
|---------|-------------|
| **Multiple Filters** | Combine any overlay filters |
| **Logic** | AND (all conditions) or OR (any condition) |
| **Save as View** | Save configuration for reuse |
| **Share View** | Share with colleagues |

**Example Complex Queries:**
- "Show processes where **Sourcing Manager is Accountable** AND **has System Issues**"
- "Show **UK Market** processes with **RED Operating Model** rating"
- "Show **Project X scope** filtered to only **Technical category**"

---

#### 10.7.3 Overlay UI Controls

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  OVERLAY CONTROLS                                                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  Overlay: [RIADA ▼]                              Display: [● All] [○ Matching]  │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ Type:     [☑ Issues] [☐ Risks] [☐ Actions]                              │   │
│  │ Category: [☐ People] [☐ Process] [☑ System] [☐ Data]                   │   │
│  │ Severity: [☑ Critical] [☑ High] [☐ Medium] [☐ Low]                     │   │
│  │ Status:   [● Open] [○ All]                                               │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  LEGEND:  🔴 Critical (2)  🟠 High (5)  🟡 Medium  🔵 Low  ⬜ None             │
│                                                                                  │
│  Results: 7 of 137 processes match    [View as List]                            │
│                                                                                  │
│  [Apply]  [Clear Overlay]  [Save View...]  [Export Filtered...]                 │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### 10.7.4 Overlay Interactions

| Interaction | Behavior |
|-------------|----------|
| **Hover on colored process** | Tooltip shows details (e.g., "3 Critical Issues, 2 High Issues") |
| **Click colored process** | Opens filtered detail (shows only matching RIADA items) |
| **Click legend item** | Toggle that color category on/off |
| **Toggle Display Mode** | Switch between Show All / Matching Only |
| **View as List** | Switch to table view with same filters applied |
| **Export Filtered** | Export matching processes as Excel/PDF |

#### 10.7.5 Heatmap Summary Views

In addition to canvas overlays, provide **summary heatmap matrices**:

**Process × Dimension Heatmap (Operating Model):**

```
                System  People  Process  Data   Overall
SOURCE            🟢      🟡       🟢      🟢      🟢
DEVELOP           🟡      🔴       🟡      🟢      🟡
EXECUTE           🟢      🟡       🔴      🟡      🟡
SUPPORT           🟢      🟢       🟢      🟡      🟢
GOVERN            🟡      🟢       🟢      🟢      🟢

[Click any cell to filter canvas to that L0 × Dimension]
```

**Process × RIADA Heatmap:**

```
                Issues  Risks  Actions  Deps  Assumptions  Total
SOURCE             3       2       5      1         2        13
DEVELOP            8       4       3      2         1        18
EXECUTE            5       6       4      3         0        18
SUPPORT            2       1       2      0         1         6
GOVERN             1       0       1      1         0         3

[Click any cell to filter canvas]
```

**Role × Process Heatmap (RACI Matrix):**

```
                Brief  Quote  Vendor  Order  Inspection
Account Mgr       R      R      C       R        I
Account Dir       A      A      A       A        C
Sourcing Mgr      C      C      R       C        C
QA Inspector      I      I      I       C        R

Legend: R=Responsible  A=Accountable  C=Consulted  I=Informed
[Click any cell to view process detail for that role]
```

---

### 10.8 Screen Specifications

#### 10.8.1 Login Screen

**Layout:** Minimal, centered, single URL for all organizations.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                         ░░░░░░░░░░░░░░░░░░░░░░                             │
│                         ░  Branded Background ░                             │
│                         ░░░░░░░░░░░░░░░░░░░░░░                             │
│                                                                             │
│                    ┌────────────────────────────┐                           │
│                    │                            │                           │
│                    │    📊 Process Catalogue    │                           │
│                    │                            │                           │
│                    │  Sign in with your work    │                           │
│                    │  email address             │                           │
│                    │                            │                           │
│                    │  ┌──────────────────────┐  │                           │
│                    │  │ ralph@surity.co      │  │                           │
│                    │  └──────────────────────┘  │                           │
│                    │                            │                           │
│                    │  ┌──────────────────────┐  │                           │
│                    │  │  Send Login Link →   │  │                           │
│                    │  └──────────────────────┘  │                           │
│                    │                            │                           │
│                    │  We'll email you a link    │                           │
│                    │  to sign in. No password   │                           │
│                    │  needed.                   │                           │
│                    │                            │                           │
│                    └────────────────────────────┘                           │
│                                                                             │
│                    v1.8.2                                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Magic Link Sent State:**

```
┌────────────────────────────┐
│                            │
│    ✉️ Check your email     │
│                            │
│  We sent a login link to   │
│  ralph@surity.co           │
│                            │
│  The link expires in 15    │
│  minutes.                  │
│                            │
│  [Resend Link]  (60s)      │
│                            │
│  Wrong email? [Try again]  │
│                            │
└────────────────────────────┘
```

**Organization Detection:** System extracts domain from email, matches to registered organization. If domain not found: "Your organization isn't registered yet. Contact your administrator."

#### 10.8.2 Business Model Canvas Screen

**Layout:** Toggle between traditional BMC grid and list view.

**Grid View (Default):**

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  Business Model: Surity Agent Model                     [Grid View ● | List View ○]     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌──────────────┬───────────────────┬──────────────┬───────────────────┬──────────────┐ │
│  │ KEY          │ KEY               │ VALUE        │ CUSTOMER          │ CUSTOMER     │ │
│  │ PARTNERS     │ ACTIVITIES        │ PROPOSITIONS │ RELATIONSHIPS     │ SEGMENTS     │ │
│  │              │                   │              │                   │              │ │
│  │ • 3PL        │ • Source          │ • Sourcing   │ • Account Mgmt   │ • Bunnings   │ │
│  │ • Test Labs  │ • Develop         │   expertise  │ • QA reporting   │ • Selco      │ │
│  │ • Audit      │ • Execute         │ • Quality    │ • Portal access  │ • Maxeda     │ │
│  │   firms      │ • Support         │   assurance  │                   │              │ │
│  │              │                   │ • Market     │                   │              │ │
│  │ [+ Add]      │ [+ Add]           │   access     │ [+ Add]           │ [+ Add]      │ │
│  │              │                   │              │                   │              │ │
│  │              │                   │ [+ Add]      │                   │              │ │
│  ├──────────────┼───────────────────┤              ├───────────────────┼──────────────┤ │
│  │ KEY          │                   │              │                   │ CHANNELS     │ │
│  │ RESOURCES    │                   │              │                   │              │ │
│  │              │                   │              │                   │ • Agent      │ │
│  │ • People     │                   │              │                   │   (always)   │ │
│  │ • Systems    │                   │              │                   │              │ │
│  │ • Vendor     │                   │              │                   │ [+ Add]      │ │
│  │   network    │                   │              │                   │              │ │
│  │ [+ Add]      │                   │              │                   │              │ │
│  ├──────────────┴───────────────────┴──────────────┴───────────────────┴──────────────┤ │
│  │ COST STRUCTURE                              │ REVENUE STREAMS                       │ │
│  │                                             │                                       │ │
│  │ • Personnel (fixed)                         │ • Agency margin: 3-8% commission      │ │
│  │ • Travel, Audits, Testing (variable)        │ • Non-inventory model                 │ │
│  │ [+ Add]                                     │ [+ Add]                               │ │
│  └─────────────────────────────────────────────┴───────────────────────────────────────┘ │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Interactions:**
- Click any entry to edit inline (auto-save)
- [+ Add] button within each box to add new entry
- Right-click entry for context menu (Edit, Delete, Link to Process, Add RIADA)
- Entries show RIADA count badges when issues exist

#### 10.8.3 RIADA List Screen

**Layout:** Toggle between table and kanban views. All 7 filters available.

**Table View:**

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  Quality Logs (RIADA)                        [Table View ● | Kanban ○]   [+ New Item]   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  Filters: [Type ▼] [Severity ▼] [Status ▼] [Owner ▼] [Process ▼] [Category ▼] [Date ▼]│
│                                                                                          │
│  🔍 Search RIADA items...                                              145 items         │
│                                                                                          │
│  ┌──┬────────┬──────────────────────────┬──────────┬──────────┬────────┬──────┬────────┐│
│  │☐ │ ID     │ Title                    │ Type     │ Severity │ Status │Owner │Process ││
│  ├──┼────────┼──────────────────────────┼──────────┼──────────┼────────┼──────┼────────┤│
│  │☐ │ISS-042 │ Order delay issue        │ 🔴 Issue │ 🔴 Crit  │ Open   │ JB   │ L2-37  ││
│  │☐ │RSK-018 │ Vendor capacity risk     │ 🟡 Risk  │ 🟠 High  │ Open   │ RS   │ L2-14  ││
│  │☐ │ACT-055 │ Update test spec docs    │ 🔵 Action│ 🟡 Med   │ In Prog│ TK   │ L2-28  ││
│  │☐ │DEP-003 │ ERP upgrade dependency   │ 🟣 Dep   │ 🟠 High  │ Open   │ ML   │ L2-05  ││
│  │☐ │ASM-012 │ China tariff stable      │ ⚪ Assum │ 🟡 Med   │ Open   │ RB   │ L1-13  ││
│  │  │        │                          │          │          │        │      │        ││
│  │  │        │         ∞ infinite scroll │          │          │        │      │        ││
│  └──┴────────┴──────────────────────────┴──────────┴──────────┴────────┴──────┴────────┘│
│                                                                                          │
│  Bulk Actions: [Assign ▼] [Change Status ▼] [Export ▼]                                  │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Kanban View:**

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  Columns by Status:                                                                      │
│                                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │ OPEN (12)    │  │ IN PROG (8)  │  │ RESOLVED (5) │  │ CLOSED (120) │               │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤               │
│  │ ┌──────────┐│  │ ┌──────────┐│  │ ┌──────────┐│  │ ┌──────────┐│               │
│  │ │ISS-042   ││  │ │ACT-055   ││  │ │ISS-038   ││  │ │ISS-001   ││               │
│  │ │Order del ││  │ │Update    ││  │ │Packaging ││  │ │Legacy    ││               │
│  │ │🔴 Crit   ││  │ │🟡 Med    ││  │ │🟡 Med    ││  │ │🟢 Low    ││               │
│  │ └──────────┘│  │ └──────────┘│  │ └──────────┘│  │ └──────────┘│               │
│  │ ┌──────────┐│  │ ┌──────────┐│  │              │  │              │               │
│  │ │RSK-018   ││  │ │ACT-061   ││  │              │  │              │               │
│  │ │Vendor cap││  │ │Audit sch ││  │              │  │              │               │
│  │ │🟠 High   ││  │ │🟡 Med    ││  │              │  │              │               │
│  │ └──────────┘│  │ └──────────┘│  │              │  │              │               │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                                          │
│  Drag cards between columns to change status                                            │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**RIADA Detail — Modal Dialog:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ISS-042: Order delay issue                                    [✕ Close]   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Type: 🔴 Issue          Severity: 🔴 Critical       Status: Open         │
│  Category: Process       Owner: Jane Brown            Due: Feb 15, 2026    │
│  Linked Process: L2-37 Order Management                                    │
│                                                                             │
│  ── Description ──────────────────────────────────────────────────────────  │
│  Orders from Bunnings are experiencing 3-5 day delays due to vendor         │
│  confirmation bottleneck. Affecting 40% of current orders.                  │
│                                                                             │
│  ── Impact ───────────────────────────────────────────────────────────────  │
│  Revenue at risk: $200K/month in delayed shipments                          │
│                                                                             │
│  ── Actions ──────────────────────────────────────────────────────────────  │
│  ☐ Review vendor SLAs for confirmation times           Due: Feb 10         │
│  ☑ Escalate to vendor management                       Done: Feb 1         │
│  ☐ Implement auto-reminder system                      Due: Feb 20         │
│                                                                             │
│  ── Related Items ────────────────────────────────────────────────────────  │
│  RSK-018: Vendor capacity risk                                             │
│  DEP-003: ERP upgrade dependency                                           │
│                                                                             │
│  ── Comments & History ───────────────────────────────────────────────────  │
│  💬 Jane: "Spoke with vendor, they're adding capacity"    2h ago           │
│  📝 Status changed: Draft → Open                         1d ago           │
│  📝 Created by Ralph Behnke                               2d ago           │
│                                                                             │
│  ┌─────────────────────────────────────────────────┐                       │
│  │ Add a comment...                                 │  [Send]              │
│  └─────────────────────────────────────────────────┘                       │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  [Delete]                                              [Save & Close]      │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 10.8.4 Portfolio View

**Layout:** Toggle between four views. Fields displayed in priority order.

**Tree View (Default):**

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  Portfolio                    [Tree ● | Gantt ○ | Kanban ○ | Table ○]   [+ New Item]    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ▼ 🎯 Digital Transformation (Strategic Pillar)            🟢 On Track    WSVF: 92     │
│    ▼ 📂 Process Automation Programme                       🟡 At Risk     WSVF: 88     │
│      ├── 📋 Order Automation (Project)          85%  👤 JB  🟢  Mar-Jun  $120K         │
│      │     ├── 📎 Phase 1: Requirements          ✅ Done                                │
│      │     ├── 📎 Phase 2: Build                 🔄 In Progress                         │
│      │     └── 📎 Phase 3: Rollout               ⏳ Planned                             │
│      ├── 📋 Data Entry Automation (Project)      60%  👤 TK  🟡  Apr-Jul  $50K          │
│      └── 📋 Inspection Scheduling (Project)      30%  👤 RS  🟢  May-Aug  $40K          │
│    ▼ 📂 Quality Uplift Programme                           🟢 On Track    WSVF: 75      │
│      ├── 📋 Test Lab Integration                 45%  👤 ML  🟢  Feb-May  $80K          │
│      └── 📋 Audit Digitization                   20%  👤 KW  🟢  Mar-Jun  $35K          │
│                                                                                          │
│  ▼ 🎯 Market Expansion (Strategic Pillar)                  🟡 At Risk     WSVF: 68     │
│    ▼ 📂 Germany Entry Programme                            🟡 At Risk     WSVF: 65      │
│      └── 📋 GS Mark Compliance (Project)         10%  👤 RB  🟡  Jun-Sep  $120K         │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Display Fields (Priority Order):**

| Priority | Field | Display |
|----------|-------|---------|
| 1 | Status (RAG) | Color dot |
| 2 | WSVF Priority | Score badge |
| 3 | % Complete | Progress bar/number |
| 4 | Owner | Avatar/initials |
| 5 | Timeline | Date range |
| 6 | Budget | Allocated amount |
| 7 | Process linkage | Available on detail view |

**Gantt View:** Horizontal timeline bars showing project duration, milestones as diamonds, dependencies as arrows.

**Kanban View:** Columns by status (Planned → In Progress → On Hold → Complete), cards draggable.

**Table View:** Sortable/filterable data grid with all fields, inline editing, infinite scroll.

#### 10.8.5 Survey Builder Screen

**Layout:** Template-based builder with separate preview tab.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  Survey Builder: AI Fluency Assessment               [Edit ● | Preview ○]   [Publish]   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  Template: [AI Fluency (AFI) ▼]                                                         │
│  Title:    [AI Fluency Assessment - Q1 2026        ]                                    │
│  Due Date: [Feb 28, 2026]     Respondents: [Select Teams/Users ▼]                       │
│                                                                                          │
│  ── Section 1: AI Awareness ──────────────────────────────────────────────────────────  │
│                                                                                          │
│  Q1. How familiar are you with AI concepts?              [Required ✓]                    │
│      [Scale: 1-5]   Labels: [Not at all → Expert]                                       │
│                                                                                          │
│  Q2. Have you used AI tools in your daily work?          [Required ✓]                    │
│      [Multiple Choice]                                                                   │
│      ○ Never   ○ Occasionally   ○ Regularly   ○ Daily                                   │
│                                                                                          │
│  [+ Add Question]                                                                        │
│                                                                                          │
│  ── Section 2: AI Application ────────────────────────────────────────────────────────  │
│                                                                                          │
│  Q3. Which AI tools have you used?                       [Optional]                      │
│      [Checkbox]                                                                          │
│      ☐ ChatGPT  ☐ Claude  ☐ Copilot  ☐ Other                                           │
│                                                                                          │
│  [+ Add Question]  [+ Add Section]                                                       │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Survey Response Screen (Respondent View):**

Section-by-section with progress bar:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  AI Fluency Assessment                                          Section 2 of 4          │
│  ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  50%                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  Section 2: AI Application                                                               │
│                                                                                          │
│  Q3. Which AI tools have you used in the past 6 months?                                 │
│                                                                                          │
│      ☑ ChatGPT                                                                          │
│      ☑ Claude                                                                           │
│      ☐ GitHub Copilot                                                                   │
│      ☐ Microsoft Copilot                                                                │
│      ☐ Other: [____________]                                                            │
│                                                                                          │
│  Q4. How confident are you applying AI to your daily tasks?                             │
│                                                                                          │
│      1 ──────●────────── 5                                                              │
│      Not at all    (3)    Very confident                                                │
│                                                                                          │
│                                                                                          │
│  [← Back]                                                              [Next Section →]  │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 10.8.6 Prompt Library Screen

**Browse View — Card Grid:**

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  Prompt Library                                    🔍 Search prompts...    [+ Create]    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  Categories: [All ●] [Process Analysis] [Risk Assessment] [Operating Model]             │
│              [Data Quality] [Strategic Planning] [Custom]                                │
│                                                                                          │
│  ── Process Analysis ──────────────────────────────────────────────────────────────────  │
│                                                                                          │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐             │
│  │ 🔍 Process Gap      │  │ ⚡ Automation       │  │ 📊 Bottleneck       │             │
│  │    Analysis          │  │    Opportunity      │  │    Detection        │             │
│  │                     │  │    Scan              │  │                     │             │
│  │ Analyze current vs  │  │ Identify where AI   │  │ Find process        │             │
│  │ future state gaps   │  │ or RPA could help    │  │ bottlenecks and     │             │
│  │ for any process     │  │ automate tasks       │  │ constraints         │             │
│  │                     │  │                     │  │                     │             │
│  │ 🏷️ Process, OM      │  │ 🏷️ Agentic, Process │  │ 🏷️ Process, KPI     │             │
│  │ ⚡ 42 runs          │  │ ⚡ 28 runs           │  │ ⚡ 15 runs           │             │
│  │                     │  │                     │  │                     │             │
│  │ [Run Prompt →]      │  │ [Run Prompt →]      │  │ [Run Prompt →]      │             │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘             │
│                                                                                          │
│  ── Risk Assessment ───────────────────────────────────────────────────────────────────  │
│  ...                                                                                     │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Prompt Execution — Full Page:**

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  ← Back to Library                               🔍 Process Gap Analysis                │
├────────────────────┬────────────────────────────────┬───────────────────────────────────┤
│                    │                                │                                    │
│  CONTEXT           │  INPUT                         │  OUTPUT                            │
│                    │                                │                                    │
│  Process:          │  Additional instructions:      │  (Waiting for execution)           │
│  [L2-10: Brief ▼]  │                                │                                    │
│                    │  ┌──────────────────────────┐  │  Click "Run" to generate          │
│  Include:          │  │ Focus on the gap between │  │  analysis.                         │
│  ☑ Process detail  │  │ current manual briefing  │  │                                    │
│  ☑ Operating Model │  │ and the target digital   │  │                                    │
│  ☑ RIADA items     │  │ process. Consider the    │  │                                    │
│  ☑ Child processes │  │ impact on downstream     │  │                                    │
│  ☐ KPI data        │  │ processes.               │  │                                    │
│  ☐ Business Model  │  │                          │  │                                    │
│                    │  └──────────────────────────┘  │                                    │
│  LLM Provider:     │                                │                                    │
│  [Claude Sonnet ▼]  │  [▶ Run Prompt]               │                                    │
│                    │                                │                                    │
│  Est. tokens: ~2K  │                                │                                    │
│                    │                                │                                    │
└────────────────────┴────────────────────────────────┴───────────────────────────────────┘
```

#### 10.8.7 Reference Data Management

**Layout:** Unified screen with tabs per catalogue.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  Reference Data                                                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  [Roles] [Systems] [Suppliers] [Clients] [Markets] [Categories] [Partners]              │
│   ^^^^                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  Roles                                           🔍 Search...        [+ Add Role]  │ │
│  │                                                                                     │ │
│  │  ┌────────────────────┬──────────────┬──────────────┬──────────┬──────────────────┐│ │
│  │  │ Name               │ Type         │ Department   │ Is Agent │ Status           ││ │
│  │  ├────────────────────┼──────────────┼──────────────┼──────────┼──────────────────┤│ │
│  │  │ Account Manager    │ Operational  │ Sourcing     │ No       │ 🟢 Active        ││ │
│  │  │ QC Inspector       │ Operational  │ QA & Tech    │ No       │ 🟢 Active        ││ │
│  │  │ Order Entry Bot    │ Operational  │ Sourcing     │ Yes 🤖   │ 🟢 Active        ││ │
│  │  │ Finance Controller │ Management   │ Finance      │ No       │ 🟢 Active        ││ │
│  │  └────────────────────┴──────────────┴──────────────┴──────────┴──────────────────┘│ │
│  │                                                                                     │ │
│  │  Click any cell to edit inline. Changes auto-save.                                 │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 10.8.8 Settings Screens

**Layout:** Settings page with left-side navigation tabs.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  Settings                                                                                │
├──────────────────────┬──────────────────────────────────────────────────────────────────┤
│                      │                                                                   │
│  Organization        │  Organization Settings                                           │
│  ● General           │                                                                   │
│  ○ Branding          │  Name:     [Surity                        ]                      │
│                      │  Slug:     [surity                        ]                      │
│  Users & Access      │  Logo:     [📷 Upload]  surity-logo.svg                          │
│  ○ User Management   │  Tier:     Enterprise                                            │
│  ○ Domain Mgmt       │  Region:   Asia-Pacific                                          │
│  ○ Roles & Perms     │                                                                   │
│                      │  Registration                                                     │
│  Integrations        │  Self-registration:  [On ●  Off ○]                               │
│  ○ GitHub            │  Default role:       [Viewer ▼]                                  │
│  ○ LLM Providers     │  Require approval:   [On ●  Off ○]                               │
│                      │                                                                   │
│  Data                │  Sessions                                                         │
│  ○ Export / Import   │  Magic link expiry:  [15] minutes                                │
│                      │  Session timeout:    [24] hours                                   │
│  System              │  Max sessions:       [5] per user                                │
│  ○ Notifications     │                                                                   │
│  ○ Audit Log         │                                                                   │
│  ○ API Keys          │  Changes auto-save ✓                                             │
│                      │                                                                   │
└──────────────────────┴──────────────────────────────────────────────────────────────────┘
```

**Settings Pages:**

| Page | Content |
|------|---------|
| **General** | Organization name, slug, logo, tier, region, registration settings, session settings |
| **Branding** | Logo upload |
| **User Management** | Invite users, list/search users, activate/deactivate, assign roles, bulk import |
| **Domain Management** | Add/remove domains, verification status, verify domain |
| **Roles & Permissions** | View/edit roles, assign permissions, create custom roles |
| **GitHub** | Connect repository, branch mapping, webhook settings |
| **LLM Providers** | Configure API keys, select default model, usage limits |
| **Export / Import** | Bulk export (processes, RIADA, portfolio), bulk import (CSV/Excel) |
| **Notifications** | Per-event notification preferences (in-app, email, both) |
| **Audit Log** | Searchable log of all system events with user, action, timestamp, detail |
| **API Keys** | Generate/revoke API keys for external integrations |

---

### 10.9 Operating Model UI Patterns

#### 10.9.1 Operating Model Tab (Accordion Layout)

Within the Process Detail view, the Operating Model tab uses accordion sections:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  L2-10: Brief → Operating Model                                  [Current ● | Future ○] │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ▼ RACI Matrix                                                              4 roles     │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Drag roles from the right panel onto activities to assign R/A/C/I                 ││
│  │                                                                                     ││
│  │  Grid View ● | List View ○                                                         ││
│  │                                                                                     ││
│  │                    │ Acct Mgr │ Sourcing Mgr │ QC Lead │ Designer │                ││
│  │  Brief Creation    │    R     │      A       │    C    │          │                ││
│  │  Brief Review      │    C     │      R       │    A    │    I     │                ││
│  │  Brief Approval    │    I     │      A       │    R    │          │                ││
│  │                                                                                     ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                          │
│  ▶ KPIs                                                                     3 KPIs      │
│                                                                                          │
│  ▶ Policies & Rules                                                         5 policies  │
│                                                                                          │
│  ▶ Governance                                                               2 forums    │
│                                                                                          │
│  ▼ Systems & Tools                                                          4 systems   │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       ││
│  │  │ 💻 SAP ERP    │  │ 📧 Outlook    │  │ 📊 Power BI   │  │ 🗂️ SharePoint │       ││
│  │  │ Primary       │  │ Communication │  │ Reporting     │  │ Documents     │       ││
│  │  │ ████████ 90%  │  │ ████████ 95%  │  │ ██████░░ 60%  │  │ █████░░░ 50%  │       ││
│  │  │ utilization   │  │ utilization   │  │ utilization   │  │ utilization   │       ││
│  │  └───────────────┘  └───────────────┘  └───────────────┘  └───────────────┘       ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                          │
│  ▶ Agents                                                                   1 agent     │
│                                                                                          │
│  ▶ Security & Access                                                        Confidential│
│                                                                                          │
│  ▶ Data                                                                     3 entities  │
│                                                                                          │
│  ▶ Timing & SLA                                                             2 SLAs      │
│                                                                                          │
│  ▶ Prompt Library                                                           5 prompts   │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 10.9.2 KPI Dashboard Cards

KPIs displayed as cards with sparklines:

```
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│ Brief Cycle Time    │  │ Brief Accuracy      │  │ Brief-to-Order      │
│                     │  │                     │  │ Conversion          │
│ Current: 3.2 days   │  │ Current: 92%        │  │ Current: 68%        │
│ Target:  2.0 days   │  │ Target:  98%        │  │ Target:  80%        │
│                     │  │                     │  │                     │
│  📈 ╱╲╱╲╱─╲        │  │  📈 ──╱──╱──        │  │  📉 ╲─╱╲──╲        │
│                     │  │                     │  │                     │
│ 🟡 Amber  ▲ +0.3d  │  │ 🟡 Amber  ▼ -2%    │  │ 🔴 Red    ▼ -5%    │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

#### 10.9.3 Current State / Future State Toggle

**Quick Toggle:** Switch in the Operating Model tab header

```
┌──────────────────────────────────────────────────────┐
│  Viewing:  [Current State ●]  [Future State ○]       │
│            [Compare / Gap Analysis]                   │
└──────────────────────────────────────────────────────┘
```

**Comparison View:**

```
┌────────────────────────────────┬────────────────────────────────┐
│  CURRENT STATE                 │  FUTURE STATE                  │
├────────────────────────────────┼────────────────────────────────┤
│                                │                                │
│  RACI: 4 roles                 │  RACI: 6 roles  (+2) 🟢       │
│  KPIs: 3 defined               │  KPIs: 5 defined (+2) 🟢      │
│  Systems: SAP, Outlook,        │  Systems: SAP, Outlook,        │
│    Power BI, SharePoint        │    Power BI, SharePoint,       │
│                                │    New CRM, AI Assistant 🟢    │
│  Agents: None                  │  Agents: Brief Bot 🟢          │
│  Automation: Manual            │  Automation: Semi-auto 🟢      │
│                                │                                │
├────────────────────────────────┴────────────────────────────────┤
│  GAP ANALYSIS                                                    │
│                                                                  │
│  🟢 4 improvements identified                                   │
│  🟡 2 require project initiation                                │
│  🔴 0 blockers                                                  │
│                                                                  │
│  Linked Projects:                                                │
│  📋 PRJ-2026-003: Brief Digitization (In Progress, 45%)        │
│  📋 PRJ-2026-008: AI Brief Assistant (Planned)                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

### 10.10 Global UI Patterns

#### 10.10.1 Data Table Standard

All table/list views across the application share these standard features:

| Feature | Behavior |
|---------|----------|
| **Column Sorting** | Click header to toggle asc/desc/none. Sort indicator arrow |
| **Column Filtering** | Filter icon per column, dropdown with type-appropriate filter |
| **Column Resizing** | Drag column border to resize |
| **Column Reordering** | Drag column header to reorder |
| **Row Selection** | Checkbox per row, select-all in header |
| **Bulk Actions** | Toolbar appears when rows selected (assign, status change, export, delete) |
| **Inline Editing** | Click any editable cell to edit in place. Auto-save on blur |
| **Infinite Scroll** | Load 50 rows initially, load more on scroll. Show loading indicator |
| **Row Click** | Click row (not checkbox) to open detail view |
| **Export** | Export current view (with active filters) to Excel or CSV |
| **Saved Views** | Save filter + sort + column configuration as named view. Share with team |

#### 10.10.2 Form Patterns

| Complexity | Pattern | Examples |
|------------|---------|----------|
| **Simple** | Inline editing — click to edit, auto-save on blur | Rename process, change status, edit description |
| **Complex** | Slide-over panel from right — form fields, auto-save | Create process, create RIADA item, create project, invite user |

**Slide-Over Panel:**

```
                                    ┌──────────────────────────────┐
                                    │  Create New Process    [✕]   │
  ┌──────────────────────────────┐  ├──────────────────────────────┤
  │                              │  │                              │
  │  (Main content visible       │  │  Code:   [L2-50         ]   │
  │   behind, dimmed)            │  │  Name:   [              ]   │
  │                              │  │  Level:  [L2 ▼]             │
  │                              │  │  Parent: [L1-05 ▼]          │
  │                              │  │  Type:   [Primary ▼]        │
  │                              │  │  Owner:  [Select ▼]         │
  │                              │  │                              │
  │                              │  │  Description:                │
  │                              │  │  ┌──────────────────────┐   │
  │                              │  │  │                      │   │
  │                              │  │  │                      │   │
  │                              │  │  └──────────────────────┘   │
  │                              │  │                              │
  │                              │  │  Auto-saving... ✓            │
  │                              │  │                              │
  │                              │  │              [Cancel] [Done] │
  └──────────────────────────────┘  └──────────────────────────────┘
```

**Auto-Save Behavior:**
- Save on blur (field loses focus)
- Debounce: 500ms after last keystroke
- Visual indicator: "Saving..." → "Saved ✓" (fade after 2s)
- Error: "Save failed — Retry" with retry button

#### 10.10.3 Empty States

All empty states include helpful copy and a quick-action button:

```
┌────────────────────────────────────────────┐
│                                            │
│  No RIADA items yet                        │
│                                            │
│  Quality logs help you track risks,        │
│  issues, and actions across your           │
│  processes. Start logging to build         │
│  visibility.                               │
│                                            │
│  [+ Create First RIADA Item]               │
│                                            │
└────────────────────────────────────────────┘
```

No illustrations. Friendly, helpful copy with a clear action.

#### 10.10.4 Report Viewing & Export

**In-App Report View:**

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  Report: Process Health Summary              [HTML View ● | PDF Preview ○]  [Export ▼]  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  (Rendered report content — charts, tables, narrative)                                  │
│                                                                                          │
│  Export options:                                                                         │
│  ┌──────────────┐                                                                       │
│  │ 📄 PDF       │                                                                       │
│  │ 📊 Excel     │                                                                       │
│  └──────────────┘                                                                       │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Report Builder:** Simple template-based. Select template → apply filters → generate.

```
┌──────────────────────────────────────────────────────────────┐
│  Generate Report                                              │
│                                                               │
│  Template:  [Process Health Summary ▼]                       │
│                                                               │
│  Filters:                                                     │
│  Scope:     [All Processes ▼]                                │
│  Market:    [All ▼]                                          │
│  Category:  [All ▼]                                          │
│  Period:    [Jan 2026 ▼] to [Mar 2026 ▼]                    │
│                                                               │
│  [Generate Report]                                            │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

### 10.11 Navigation Structure

#### 10.11.1 Contextual Navigation

| Context | Additional Navigation |
|---------|----------------------|
| **Process Detail** | Tabs (Overview, Operating Model, RIADA, Projects, History, Prompts) |
| **Project Detail** | Tabs (Overview, Scope, Milestones, Budget, RIADA, Team, Processes) |
| **Survey** | Tabs (Design, Respondents, Responses, Results, Reports) |
| **RIADA Item** | Modal with sections (Description, Impact, Actions, Related, History) |

---

### 10.12 Design System

#### 10.12.1 Color Palette

**Default Theme (Neutral):**

| Color | Use | Hex |
|-------|-----|-----|
| **Primary** | Buttons, links, active states | #2563EB (Blue) |
| **Secondary** | Secondary actions | #64748B (Slate) |
| **Success/Green** | RAG Green, success states | #22C55E |
| **Warning/Amber** | RAG Amber, warnings | #F59E0B |
| **Danger/Red** | RAG Red, errors, critical | #EF4444 |
| **Background** | Page background | #F8FAFC |
| **Surface** | Cards, panels | #FFFFFF |
| **Text Primary** | Main text | #1E293B |
| **Text Secondary** | Supporting text | #64748B |
| **Border** | Borders, dividers | #E2E8F0 |

**Surity Theme:**

| Color | Use | Hex |
|-------|-----|-----|
| **Primary** | Buttons, links, active states | #F59E0B (Yellow) |
| **Primary Hover** | Button hover states | #D97706 (Darker Yellow) |
| **Background** | Page background | #F9FAFB (Light Grey) |
| **Surface** | Cards, panels | #FFFFFF |
| **Sidebar** | Sidebar background | #F3F4F6 (Light Grey) |
| **Text Primary** | Main text | #1F2937 (Dark Grey) |

**Dark Mode (applies to both themes):**

| Color | Use | Hex |
|-------|-----|-----|
| **Background** | Page background | #0F172A |
| **Surface** | Cards, panels | #1E293B |
| **Text Primary** | Main text | #F1F5F9 |
| **Text Secondary** | Supporting text | #94A3B8 |
| **Border** | Borders, dividers | #334155 |

**Dark Mode Toggle:** Defaults to system preference, user can override in profile settings.

#### 10.12.2 Typography

| Element | Font | Size | Weight | Line Height |
|---------|------|------|--------|-------------|
| **H1** | Nunito | 30px | 700 (Bold) | 1.3 |
| **H2** | Nunito | 24px | 600 (SemiBold) | 1.3 |
| **H3** | Nunito | 20px | 600 (SemiBold) | 1.4 |
| **H4** | Nunito | 16px | 600 (SemiBold) | 1.4 |
| **Body** | Nunito | 14px | 400 (Regular) | 1.5 |
| **Body Small** | Nunito | 13px | 400 (Regular) | 1.5 |
| **Caption** | Nunito | 12px | 400 (Regular) | 1.4 |
| **Code** | JetBrains Mono | 13px | 400 (Regular) | 1.5 |

**Font Loading:** Nunito loaded via self-hosted files (not Google Fonts) for China compatibility.

#### 10.12.3 Spacing System

| Token | Value | Use |
|-------|-------|-----|
| **xs** | 4px | Tight internal spacing |
| **sm** | 8px | Small gaps, padding |
| **md** | 16px | Standard padding, margins |
| **lg** | 24px | Section spacing |
| **xl** | 32px | Large section gaps |
| **2xl** | 48px | Page-level spacing |

#### 10.12.4 Component Library

Built on **shadcn/ui** with Nunito font and custom theme tokens.

| Component | Usage | Variants |
|-----------|-------|----------|
| **Button** | Actions, CTAs | Primary, Secondary, Ghost, Destructive, Icon |
| **Card** | Process cards, dashboard widgets, KPI cards | Default, Elevated, Interactive |
| **Data Table** | All list views | With/without selection, inline edit |
| **Dialog / Modal** | RIADA detail, confirmations | Small, Medium, Large |
| **Slide-Over** | Complex forms, create/edit panels | Right-side, 400px wide |
| **Accordion** | Operating Model components | Single/multi expand |
| **Tabs** | View toggles, section navigation | Underline, Pill |
| **Badge** | Status indicators, counts, RAG | Green, Amber, Red, Blue, Grey |
| **Avatar** | User photos, initials | Small (24px), Medium (32px), Large (40px) |
| **Toast** | Auto-save confirmation, success/error messages | Success, Error, Info |
| **Tooltip** | Hover help, collapsed sidebar labels | Light, Dark |
| **Progress Bar** | Survey completion, project %, adoption | Default, RAG-colored |
| **Sparkline** | KPI trend charts | Up (green), Down (red), Flat (grey) |
| **Breadcrumbs** | Hierarchy navigation | Process path, Portfolio path |
| **Command Palette** | Global search (Cmd+K) | Full-screen overlay |
| **Dropdown Menu** | Quick actions, org switcher, export | Standard, Nested |
| **Toggle** | Current/Future state, view switches | Binary, Multi-option |

#### 10.12.5 Responsive Behavior

| Breakpoint | Width | Layout Adjustment |
|------------|-------|-------------------|
| **Desktop Large** | ≥1440px | Full layout, expanded sidebar default |
| **Desktop** | 1280-1439px | Full layout, collapsed sidebar default |
| **Tablet** | 768-1279px | Collapsed sidebar, simplified canvas |
| **Mobile** | <768px | Bottom navigation, list/tree views only, no canvas |

**Mobile Behavior:**
- Sidebar replaced by bottom tab bar (Home, Processes, RIADA, Portfolio, More)
- Canvas not available — use Tree or List view
- Slide-over panels become full-screen sheets
- Tables become card-based lists

#### 10.12.6 Accessibility (WCAG 2.1 AA)

| Requirement | Implementation |
|-------------|----------------|
| **Color Contrast** | Minimum 4.5:1 for body text, 3:1 for large text |
| **Keyboard Navigation** | Full tab navigation, focus indicators, skip links |
| **Screen Readers** | ARIA labels on all interactive elements |
| **Focus Management** | Visible focus ring, logical tab order |
| **Motion** | Respect `prefers-reduced-motion`, provide static alternatives |
| **RAG Colors** | Never use color alone — always pair with text/icon (🟢 Green, 🟡 Amber, 🔴 Red) |
| **Form Labels** | All inputs have visible labels, error messages linked to fields |
| **Alt Text** | All images have descriptive alt text |

#### 10.12.7 Tone of Voice

| Context | Tone | Example |
|---------|------|---------|
| **Success** | Friendly, brief | "Nice! Process updated ✓" |
| **Error** | Helpful, no blame | "Couldn't save — check your connection and try again" |
| **Empty State** | Encouraging, actionable | "No RIADA items yet. Start logging to build visibility." |
| **Confirmation** | Clear, specific | "Delete this RIADA item? This can't be undone." |
| **Loading** | Calm | "Loading your processes..." |
| **Notification** | Concise, informative | "Jane assigned you ISS-042: Order delay" |

#### 10.12.8 Internationalization (i18n)

| Aspect | Implementation |
|--------|----------------|
| **Framework** | next-intl or react-i18next |
| **Default Language** | English (en) |
| **Future Languages** | Simplified Chinese (zh-CN), others as needed |
| **String Storage** | JSON files per locale (e.g., en.json, zh-CN.json) |
| **Date/Number Formatting** | Locale-aware (Intl API) |
| **RTL Support** | Not required at launch |

All user-facing strings extracted to locale files from day one. No hardcoded strings in components.

---

### 10.13 Key Screens Summary

| Screen | Section | Primary Purpose |
|--------|---------|-----------------|
| **Login** | 10.8.1 | Passwordless email authentication |
| **Process Canvas** | 10.2 | Visual navigation of process hierarchy |
| **Process Detail** | 10.4 | View/edit process with Operating Model tabs |
| **Business Model Canvas** | 10.8.2 | BMC grid/list view with inline editing |
| **RIADA List** | 10.8.3 | Table/kanban view of quality logs |
| **RIADA Detail** | 10.8.3 | Modal dialog for individual RIADA items |
| **Portfolio View** | 10.8.4 | Tree/gantt/kanban/table for projects |
| **Survey Builder** | 10.8.5 | Template-based survey creation |
| **Survey Response** | 10.8.5 | Section-by-section respondent experience |
| **Prompt Library** | 10.8.6 | Card grid browse + full-page execution |
| **Reference Data** | 10.8.7 | Tabbed catalogue management |
| **Settings** | 10.8.8 | 11 settings pages |
| **Operating Model** | 10.9 | Accordion components with Current/Future/Gap |
| **Dashboards** | 10.5 | Executive, RIADA, Portfolio, Survey |
| **Reports** | 10.10.4 | Template-based generation, HTML/PDF view |

---

## 14. Open Questions

### Architecture Questions
1. ✅ ~~What is the primary purpose of the Process Catalogue?~~ *Answered: Strategic-to-operational traceability platform*
2. ✅ ~~What are the detailed entity models for each component?~~ *Answered: See Section 4*
3. ✅ ~~How does the Process Spine technically integrate the seven components?~~ *Answered: See Data Model Section 9.6*
4. ✅ ~~What is the data synchronization model between components?~~ *Answered: Real-time via database triggers + event sourcing*

### Business Model Questions
5. ✅ ~~Are there additional Business Model Canvas components beyond those listed?~~ *Answered: Standard BMC + custom components per tenant*
6. ✅ ~~How should SWOT be structured?~~ *Answered: SWOT is separate strategic analysis; RIADA is operational tracking*
7. ✅ ~~Can a single Business Model entry belong to multiple canvas components?~~ *Answered: Yes, via many-to-many relationship*

### Process Catalogue Questions
8. ✅ ~~How many levels in the process hierarchy?~~ *Answered: 6 levels (L0-L5)*
9. ✅ ~~Can processes have multiple parents?~~ *Answered: No - single parent hierarchy, but cross-linking supported*
10. ✅ ~~How are L4 variations structured?~~ *Answered: Flexible tagging (Category, Market, Client) not rigid matrix*
11. ✅ ~~What is the relationship between SIPOC and L5 steps?~~ *Answered: L5 steps ARE the SIPOC-detailed workflow steps*

### Quality Logs Questions
12. ✅ ~~Should Assumptions and Dependencies also be tracked?~~ *Answered: Yes - full RIADA*
13. ✅ ~~What workflow states should RIADA items have?~~ *Answered: Draft, Open, In Progress, On Hold, Resolved, Closed, Mitigated, Cancelled*
14. ✅ ~~How are Issues escalated between levels?~~ *Answered: Manual escalation with notification; auto-escalation rules configurable*

### Operating Model Design Questions
15. ✅ ~~How detailed should the Prompt Library be?~~ *Answered: Hierarchical - Organization → Component → Process Level → Use Case*
16. ✅ ~~What security classification levels are needed?~~ *Answered: Public, Internal, Confidential, Restricted*
17. ✅ ~~What data elements need to be tracked for "Data mastered in process"?~~ *Answered: Data entity, owner, source system, quality rules*

### Portfolio Response Questions
18. ✅ ~~Does Portfolio need RIADA tracking?~~ *Answered: Yes - RIADA at every portfolio level*
19. ✅ ~~What is the prioritization methodology?~~ *Answered: WSVF*
20. ✅ ~~What project management methodology is assumed?~~ *Answered: Methodology-agnostic; supports Agile, Waterfall, Hybrid*
21. ✅ ~~How are cross-project workstreams governed?~~ *Answered: Shared workstream with multiple project links; single owner*
22. ✅ ~~What financial tracking is needed?~~ *Answered: Budget, Current Spend, Projected Spend, Variance, Contingency*

### Change & Adoption Questions
23. ✅ ~~What survey tool integration is needed?~~ *Answered: Built-in simple surveys; integration with external tools optional*
24. ✅ ~~How frequently should adoption surveys run?~~ *Answered: Configurable per change initiative (weekly, monthly, milestone-based)*
25. ✅ ~~What is the benefits realization framework?~~ *Answered: Target → Baseline → Current → Variance with milestone tracking*

### Platform Questions
26. ✅ ~~What platform(s) should this run on?~~ *Answered: Web (primary), PWA for mobile, desktop via browser*
27. ✅ ~~Are there integration requirements with other systems?~~ *Answered: GitHub (required), ERP/PPM (optional via API)*
28. ✅ ~~What is the expected scale?~~ *Answered: 10-1000 users, 100-10,000 processes, 10-500 projects per tenant*
29. ✅ ~~What are the authentication and authorization requirements?~~ *Answered: Passwordless magic links (primary), OAuth2/OIDC & SAML 2.0 (enterprise SSO add-on), MFA support. See Section 6.2*
30. ✅ ~~What reporting and visualization capabilities are needed?~~ *Answered: Built-in dashboards, PDF/HTML export, chart library*
31. ✅ ~~Multi-tenancy requirements?~~ *Answered: Yes - Organization-based data isolation*

### Integration Questions
32. ✅ ~~Is GitHub integration required?~~ *Answered: Yes*
33. ✅ ~~What other source control systems need support?~~ *Answered: GitHub primary; GitLab/Bitbucket as future roadmap*
34. ✅ ~~What CI/CD pipeline integrations are needed?~~ *Answered: Webhook-based; GitHub Actions native support*

### User Questions
35. ✅ ~~Who are the primary user personas and their permissions?~~ *Answered: See Section 7.2*
36. ✅ ~~What are the key workflows for each user type?~~ *Answered: See Section 7.2*

---

## 15. Requirements Log

| Date | Requirement Added | Section Updated |
|------|-------------------|-----------------|
| 2026-01-31 | Initial blueprint created | All |
| 2026-01-31 | Core architecture defined: Process Spine + 6 Components | Sections 1, 2, 3 |
| 2026-01-31 | Multi-dimensional roll-up requirement added | Section 3.4 |
| 2026-01-31 | Strategic questions mapped to components | Section 3.3 |
| 2026-01-31 | **Business Model detailed:** Canvas components, hierarchy, SWOT/Issues attachment, aggregation | Section 4.1 |
| 2026-01-31 | **Process Catalogue detailed:** 6-level hierarchy (L0-L5), inheritance rules, resource allocation | Section 4.2 |
| 2026-01-31 | **Quality Logs detailed:** Issues/Risks with People/Process/System/Data categories, severity levels | Section 4.3 |
| 2026-01-31 | **Operating Model Design detailed:** 10 components, current/future state, Prompt Library | Section 4.4 |
| 2026-01-31 | **Portfolio Response detailed:** Hierarchy, cross-project capabilities, resource allocation | Section 4.5 |
| 2026-01-31 | **Change & Adoption detailed:** Surveys, lead/lag indicators, KPI tracking | Section 4.6 |
| 2026-01-31 | **Reference Data Catalogues added:** Role, Agent, System, KPI, Supplier, Client, etc. with lifecycle status | Section 5 |
| 2026-01-31 | Excel tab mapping completed for all components | Section 4.x |
| 2026-01-31 | **RIADA expanded:** Quality Logs now track Risk, Issue, Action, Dependency, Assumption (not just Issues/Risks) | Section 4.3 |
| 2026-01-31 | **Portfolio RIADA:** RIADA management added at every portfolio level (Pillar→Programme→Project→Workstream→Work Package) | Section 4.5 |
| 2026-01-31 | **RIADA relationships:** Added ability to link RIADA items to each other | Section 4.3.6 |
| 2026-01-31 | **Portfolio Focus:** Full Portfolio Response spec with WSVF prioritization, 7-level hierarchy | Section 4.5 |
| 2026-01-31 | **Multi-Tenant Architecture:** Organization-based data isolation with shared infrastructure | Section 6.1 |
| 2026-01-31 | **GitHub Integration:** Repository connection, automated commits, webhook sync | Section 6.2 |
| 2026-01-31 | **RBAC:** Role-based access control framework with permission matrix | Section 6.3 |
| 2026-01-31 | **Standard Operating Model:** Rich text documentation at each process level (L0-L5) | Section 4.4.2 |
| 2026-01-31 | **Publishing & Reports:** PDF, HTML, DOCX report generation with customization | Section 4.4.3 |
| 2026-01-31 | **Report Types:** Single process, process family, value stream, OM summary, custom reports | Section 4.4.3.1 |
| 2026-01-31 | **Publishing Workflow:** Scope selection, configuration, preview, publish, version control | Section 4.4.3.4 |
| 2026-01-31 | **Scheduled Publishing:** Auto-publish, change detection, distribution lists | Section 4.4.3.5 |
| 2026-01-31 | **Primary/Secondary Processes:** Classification for core value chain vs support functions | Section 4.2.1 |
| 2026-01-31 | **Secondary Domains:** IT, HR, Legal, Treasury, Portfolio Delivery with distinct hierarchies | Section 4.2.1.3 |
| 2026-01-31 | **Cross-Query Capability:** Query across Primary + Secondary processes | Section 4.2.1.5 |
| 2026-01-31 | **Primary-Secondary Linkage:** Link support processes to the primary processes they support | Section 4.2.1.7 |
| 2026-01-31 | **Light Project Management:** Benefits & Outcomes, Scope Statement, Key Milestones, Budget, Status | Section 4.5.4 |
| 2026-01-31 | **Milestone Types:** Project, Customer, Financial, Benefit milestone categorization | Section 4.5.4.3 |
| 2026-01-31 | **Budget Tracking:** Budgeted/Current/Projected spend, Budget Status, Contingency | Section 4.5.4.4 |
| 2026-01-31 | **Benefits Tracking:** Target benefits, Current benefits accrued, Realization % | Section 4.5.4.5 |
| 2026-01-31 | **RAG Status:** Resource, Quality, Scope, Benefits Delivery, Timeline dimensions | Section 4.5.4.6 |
| 2026-01-31 | **Project Summary Card:** Consolidated view of all project data | Section 4.5.4.7 |
| 2026-01-31 | **Technical Architecture:** Dual deployment model (Global SaaS + China Single-Tenant) | Section 9 |
| 2026-01-31 | **Global Stack:** Vercel + Supabase + Cloudflare R2 + FastAPI (Python) | Section 9.3.2 |
| 2026-01-31 | **China Stack:** Alibaba Cloud (ECS + RDS + OSS + Redis) + FastAPI | Section 9.3.3 |
| 2026-01-31 | **Multi-Tenancy Patterns:** RLS for SaaS, Database-per-tenant for China | Section 9.4.1 |
| 2026-01-31 | **API Design:** RESTful endpoints with aggregation support | Section 9.7 |
| 2026-01-31 | **Security Architecture:** Network, Auth, Data encryption, Compliance | Section 9.9 |
| 2026-01-31 | **User Personas:** 14 personas across Executive, Management, Operational, Specialist | Section 7.1 |
| 2026-01-31 | **Permission Matrix:** Detailed CRUD permissions per persona per component | Section 7.2 |
| 2026-01-31 | **Key Workflows:** Process Documentation, Project Delivery, RIADA Management | Section 7.3 |
| 2026-01-31 | **Non-Functional Requirements:** Performance, Security, Scalability, Availability, Accessibility | Section 8 |
| 2026-01-31 | **Detailed Data Model:** 30+ tables with columns, types, constraints, indexes | Section 9.6 |
| 2026-01-31 | **Open Questions:** All 36 questions answered with defaults/recommendations | Section 14 |
| 2026-01-31 | **Component 7: Surveys:** New 7th feature component for survey creation | Section 4.7 |
| 2026-01-31 | **4 Survey Modes:** AI Fluency, Operating Model, Change Readiness, Adoption Evidence | Section 4.7.1 |
| 2026-01-31 | **AI Fluency Survey:** 6-level competency model (L0-L5), AFI scoring (0-100), 15 questions | Section 4.7.2 |
| 2026-01-31 | **Operating Model Survey:** SPRD framework (System, People, Process, Data), RAG ratings | Section 4.7.3 |
| 2026-01-31 | **Change Readiness Survey:** ADKAR-based, readiness scoring, pre-kickoff timing | Section 4.7.4 |
| 2026-01-31 | **Adoption Evidence Survey:** Process/Role/KPI evidence, adoption scoring, post go-live | Section 4.7.5 |
| 2026-01-31 | **Survey Builder:** Templates, question customization, branching, scheduling | Section 4.7.6 |
| 2026-01-31 | **Survey Integration:** Auto-updates to Process Catalogue, RIADA, Portfolio, Change & Adoption | Section 4.7.7 |
| 2026-01-31 | **Prompt Library Enhanced:** Comprehensive AI prompt execution feature | Section 4.4.5 |
| 2026-01-31 | **Universal Context:** Auto-injected process, business model, operating model, RIADA context | Section 4.4.5.3 |
| 2026-01-31 | **User Personalization:** Role-based prompt adaptation, expertise level, preferences | Section 4.4.5.4 |
| 2026-01-31 | **Additional Context:** User-provided metrics, issues, goals, custom input | Section 4.4.5.5 |
| 2026-01-31 | **Prompt Execution:** In-app LLM execution with model selection, temperature, preview | Section 4.4.5.6 |
| 2026-01-31 | **Prompt History:** Stored results with versioning, rating, feedback, search | Section 4.4.5.7 |
| 2026-01-31 | **Level-Specific Prompts:** Different prompts per process level (L0-L5) | Section 4.4.5.8 |
| 2026-01-31 | **Template Management:** System, organization, personal templates with variables | Section 4.4.5.9 |
| 2026-01-31 | **Prompt Data Model:** PromptTemplate, PromptExecution, PromptContextSnapshot tables | Section 4.4.5.10 |
| 2026-01-31 | **Process Canvas:** Swimlane visualization with L0 horizontal, L1 horizontal, L2 vertical columns | Section 10.1 |
| 2026-01-31 | **Canvas Hierarchy:** L3/L4/L5 as expandable nested menus under L2 | Section 10.1.2 |
| 2026-01-31 | **Canvas Interactions:** Click, hover, right-click, drag-drop behaviors | Section 10.1.3 |
| 2026-01-31 | **Visual Indicators:** RAG dots, issue badges, project links, expand/collapse | Section 10.1.4 |
| 2026-01-31 | **Alternative Views:** Tree view, List view, Card view | Section 10.2 |
| 2026-01-31 | **Process Detail View:** Tabbed interface with Overview, Operating Model, RIADA, Projects | Section 10.3 |
| 2026-01-31 | **Executive Dashboard:** Process health, RIADA summary, portfolio status, heatmaps | Section 10.4.1 |
| 2026-01-31 | **RIADA Dashboard:** Severity, category, trend, owner breakdown widgets | Section 10.4.2 |
| 2026-01-31 | **Portfolio Dashboard:** RAG, timeline, budget, benefits, WSVF widgets | Section 10.4.3 |
| 2026-01-31 | **Survey Dashboard:** Response rates, AFI distribution, readiness, adoption | Section 10.4.4 |
| 2026-01-31 | **Standard Reports:** Process Catalogue, Operating Model, RIADA, Portfolio, Executive | Section 10.5.1 |
| 2026-01-31 | **Custom Report Builder:** Scope, sections, filters, charts, branding, scheduling | Section 10.5.2 |
| 2026-01-31 | **Export Formats:** PDF, HTML, Excel, Word, Markdown, JSON/CSV | Section 10.5.3 |
| 2026-01-31 | **Navigation Structure:** Sidebar navigation, contextual tabs | Section 10.7 |
| 2026-01-31 | **Design System:** Color palette, typography, component library, responsive behavior | Section 10.8 |
| 2026-01-31 | **Heatmap & Overlay System:** Comprehensive overlay framework for Process Canvas | Section 10.6 |
| 2026-01-31 | **Display Modes:** Show All Processes vs Show Matching Only toggle | Section 10.6.1 |
| 2026-01-31 | **RIADA Overlay:** Filter by type, category, severity, status with RAG colors | Section 10.6.2 |
| 2026-01-31 | **Project Scope Overlay:** Highlight processes impacted by selected project | Section 10.6.2 |
| 2026-01-31 | **System Overlay:** Show processes using selected system (primary/supporting) | Section 10.6.2 |
| 2026-01-31 | **Role/RACI Overlay:** Show processes by role involvement with RACI filter | Section 10.6.2 |
| 2026-01-31 | **Business Model Overlay:** Filter by Market, Client, Category, Partner | Section 10.6.2 |
| 2026-01-31 | **Ownership Overlay:** Show by Process Owner, Sponsor, or Vacant | Section 10.6.2 |
| 2026-01-31 | **Survey Results Overlay:** Operating Model RAG, AI Fluency, Adoption Evidence | Section 10.6.2 |
| 2026-01-31 | **Change Impact Overlay:** Current vs Future state comparison | Section 10.6.2 |
| 2026-01-31 | **Dependency Overlay:** Upstream/downstream process relationships | Section 10.6.2 |
| 2026-01-31 | **Primary/Secondary Overlay:** Process type and domain filtering | Section 10.6.2 |
| 2026-01-31 | **Custom/Combined Overlay:** User-defined filter combinations with AND/OR logic | Section 10.6.2 |
| 2026-01-31 | **Heatmap Summary Views:** Process×Dimension, Process×RIADA, Role×Process matrices | Section 10.6.5 |
| 2026-01-31 | **LLM Integration:** Connect to LLMs for prompt execution against catalogue data | Section 6.3 |
| 2026-01-31 | **LLM Providers:** OpenAI, Anthropic, Qwen (China), Azure OpenAI, Self-Hosted | Section 6.3.2 |
| 2026-01-31 | **LLM Configuration:** Per-tenant settings for provider, model, API keys, limits | Section 6.3.3 |
| 2026-01-31 | **Prompt Execution Modes:** Ad-hoc chat, Prompt Library execution, Batch execution | Section 6.3.4 |
| 2026-01-31 | **LLM Data Access:** Process, Operating Model, RIADA, Portfolio, Surveys (permission-controlled) | Section 6.3.5 |
| 2026-01-31 | **Response Handling:** Save (with rating, feedback, linking) or Discard responses | Section 6.3.6 |
| 2026-01-31 | **Conversation Memory:** Multi-turn conversations with session context | Section 6.3.7 |
| 2026-01-31 | **LLM Entry Points:** Global (Cmd+K), Process detail, Canvas, RIADA, Project, OM Editor | Section 6.3.8 |
| 2026-01-31 | **LLM Usage Controls:** Enable/disable, role restrictions, quotas, cost tracking, audit | Section 6.3.9 |
| 2026-01-31 | **China LLM Compliance:** Qwen for China deployment, data residency, no cross-border | Section 6.3.10 |
| 2026-01-31 | **LLM Data Model:** LLMConfiguration, LLMUsage, Conversation, ConversationMessage tables | Section 6.3.11 |
| 2026-01-31 | **Agentic Opportunity Fields (Process):** agentic_potential, automation levels, gap, linked agents | Section 4.2.1.5 |
| 2026-01-31 | **Automation Level Definitions:** Manual, Assisted, Semi-Automated, Fully-Automated | Section 4.2.1.5 |
| 2026-01-31 | **Agentic Potential Criteria:** High/Medium/Low/None assessment criteria | Section 4.2.1.5 |
| 2026-01-31 | **Agentic Opportunity Fields (Business Model):** agentic_potential, digital maturity at BM level | Section 4.1.4 |
| 2026-01-31 | **Agent Catalogue (Enhanced):** Agent types, status lifecycle, technology tracking | Section 4.4.5.1 |
| 2026-01-31 | **Process-Agent Linkage:** Current and future agent assignments per process | Section 4.4.5.2 |
| 2026-01-31 | **Automation Coverage View:** Visual display of current vs target automation | Section 4.4.5.3 |
| 2026-01-31 | **Agentic Opportunity Register:** Dedicated view/report for all opportunities | Section 4.4.5.4 |
| 2026-01-31 | **Agentic Opportunity Workflow:** Identify → Assess → Prioritize → Mobilize → Implement → Deploy → Measure | Section 4.4.5.5 |
| 2026-01-31 | **Agentic Opportunity Overlay:** Heatmap overlay for automation potential and gaps | Section 10.6.2 |
| 2026-01-31 | **Agentic Reports:** Agentic Opportunity Register, Automation Coverage, Agent Catalogue reports | Section 10.5.1 |
| 2026-01-31 | **Data Model Summary:** 45+ tables across 14 domains | Section 9.6.1 |
| 2026-01-31 | **Enhanced ERD:** Comprehensive entity relationship diagram | Section 9.6.2 |
| 2026-01-31 | **Process Table Enhanced:** Added 8 agentic opportunity fields | Section 9.6.5 |
| 2026-01-31 | **CanvasEntry Table Enhanced:** Added 4 agentic/digital maturity fields | Section 9.6.4 |
| 2026-01-31 | **Agent Table Enhanced:** Full agent lifecycle with 7 agent types | Section 9.6.10 |
| 2026-01-31 | **ProcessAgent Table:** Process-Agent linkage with current/future state | Section 9.6.10 |
| 2026-01-31 | **AgenticOpportunity Table:** Dedicated opportunity tracking table | Section 9.6.10 |
| 2026-01-31 | **RoleCatalogue Table:** Added is_agent flag for AI/automation roles | Section 9.6.10 |
| 2026-01-31 | **Authentication & Authorization:** Complete passwordless auth specification | Section 6.2 |
| 2026-01-31 | **Passwordless Magic Link:** Email-only authentication, no passwords | Section 6.2.2 |
| 2026-01-31 | **Domain-Restricted Access:** Organizations register allowed email domains | Section 6.2.3 |
| 2026-01-31 | **Domain Verification:** DNS TXT record verification for domain ownership | Section 6.2.3 |
| 2026-01-31 | **User Registration Flows:** Self-registration and admin-invited flows | Section 6.2.4 |
| 2026-01-31 | **Bulk User Import:** CSV import with domain validation | Section 6.2.4 |
| 2026-01-31 | **Organization Auth Settings:** Self-registration toggle, default roles, session config | Section 6.2.5 |
| 2026-01-31 | **RBAC Authorization:** Role-based access with scoped permissions | Section 6.2.6 |
| 2026-01-31 | **Default Roles:** Super Admin, Org Admin, Process Owner, Project Manager, Contributor, Viewer | Section 6.2.6 |
| 2026-01-31 | **Session Management:** JWT tokens, refresh tokens, concurrent session limits | Section 6.2.7 |
| 2026-01-31 | **Security Controls:** Rate limiting, brute force protection, audit logging | Section 6.2.8 |
| 2026-01-31 | **Auth Data Model:** OrganizationDomain, MagicLinkToken, UserSession, AuthAuditLog tables | Section 6.2.9 |
| 2026-01-31 | **Auth API Endpoints:** Magic link, verify, refresh, logout, user management | Section 6.2.10 |
| 2026-01-31 | **China Auth Deployment:** Alibaba IDaaS, DirectMail for China region | Section 6.2.11 |
| 2026-01-31 | **Application Shell:** Collapsible sidebar (300px/64px), persistent header bar | Section 10.1 |
| 2026-01-31 | **Header Bar:** Org logo, breadcrumbs, global search, notifications, version, org switcher, user avatar | Section 10.1.3 |
| 2026-01-31 | **Organization Switcher:** Multi-org support, switch without logout | Section 10.1.4 |
| 2026-01-31 | **Global Search (Cmd+K):** Searches all entity types, scoped search per view | Section 10.1.5 |
| 2026-01-31 | **Notification Center:** Bell icon, user-configurable per event, minimum one channel | Section 10.1.6 |
| 2026-01-31 | **Quick Action Menu:** "+ New" dropdown for common create actions | Section 10.1.7 |
| 2026-01-31 | **Canvas Background:** White with subtle dot grid | Section 10.2.6 |
| 2026-01-31 | **Canvas Navigation:** Zoom, pan, mini-map, fit-to-view, zoom indicator | Section 10.2.6 |
| 2026-01-31 | **Process Card Sizing:** User-selectable Small/Medium/Large toggle | Section 10.2.7 |
| 2026-01-31 | **L3/L4/L5 Inline Expansion:** Expand children inline on canvas | Section 10.2.8 |
| 2026-01-31 | **Canvas Empty State:** Start from scratch + template + upload options | Section 10.2.9 |
| 2026-01-31 | **Login Screen:** Minimal, single URL, org detected from email domain | Section 10.8.1 |
| 2026-01-31 | **Business Model Canvas Screen:** Grid/list toggle, inline editing, add buttons | Section 10.8.2 |
| 2026-01-31 | **RIADA List Screen:** Table/kanban toggle, all 7 filters, bulk actions | Section 10.8.3 |
| 2026-01-31 | **RIADA Detail:** Modal dialog with description, actions, related items, comments | Section 10.8.3 |
| 2026-01-31 | **Portfolio View:** Four views (tree, gantt, kanban, table), WSVF priority ranking | Section 10.8.4 |
| 2026-01-31 | **Survey Builder:** Template-based, separate preview tab | Section 10.8.5 |
| 2026-01-31 | **Survey Response:** Section-by-section with progress bar | Section 10.8.5 |
| 2026-01-31 | **Prompt Library:** Card grid browse, full-page execution with context/input/output | Section 10.8.6 |
| 2026-01-31 | **Reference Data:** Unified screen with tabs per catalogue | Section 10.8.7 |
| 2026-01-31 | **Settings Screens:** 11 settings pages (org, users, domains, integrations, audit) | Section 10.8.8 |
| 2026-01-31 | **Operating Model UI:** Accordion sections, drag-to-assign RACI, KPI sparkline cards | Section 10.9 |
| 2026-01-31 | **Current/Future State:** Toggle + side-by-side comparison + gap analysis view | Section 10.9.3 |
| 2026-01-31 | **Data Table Standard:** All 11 features (sort, filter, resize, reorder, select, bulk, inline edit, infinite scroll, click, export, saved views) | Section 10.10.1 |
| 2026-01-31 | **Form Patterns:** Inline editing (simple), slide-over panel (complex), auto-save | Section 10.10.2 |
| 2026-01-31 | **Empty States:** Helpful copy + quick-action buttons, no illustrations | Section 10.10.3 |
| 2026-01-31 | **Report Viewing:** In-app HTML + PDF preview, export to PDF/Excel | Section 10.10.4 |
| 2026-01-31 | **Surity Theme:** Light grey + yellow (#F59E0B) brand colors | Section 10.12.1 |
| 2026-01-31 | **Typography:** Nunito font (self-hosted for China compatibility) | Section 10.12.2 |
| 2026-01-31 | **Dark Mode:** System preference default + manual override | Section 10.12.1 |
| 2026-01-31 | **Component Library:** 16 shadcn/ui components specified | Section 10.12.4 |
| 2026-01-31 | **Accessibility:** WCAG 2.1 AA compliance, color-never-alone for RAG | Section 10.12.6 |
| 2026-01-31 | **Tone of Voice:** Friendly/conversational | Section 10.12.7 |
| 2026-01-31 | **Internationalization:** i18n framework from day one, English at launch | Section 10.12.8 |
| 2026-01-31 | **Responsive Behavior:** 4 breakpoints, mobile bottom nav, no canvas on mobile | Section 10.12.5 |
| 2026-01-31 | **Organization Branding:** Logo upload only | Section 10.12.1 |
| 2026-02-01 | **Auth Reconciliation:** Unified all auth references — passwordless magic links as primary, OAuth/SAML SSO as enterprise add-on. Reconciled Sections 8.2, 9.3.2, 9.3.3, 9.8, 9.9, 9.10, 14 to align with Section 6.2 specification | Sections 6.2, 8.2, 9.3–9.10, 14 |

---

## 16. Claude Code Implementation Notes

*This section contains specific guidance for Claude Code when building this application.*

### Build Instructions
[To be populated as requirements are finalized]

### File Structure
[To be populated as requirements are finalized]

### Dependencies
[To be populated as requirements are finalized]

### Testing Strategy
[To be populated as requirements are finalized]

---

*Document maintained collaboratively. Please provide requirements to populate each section.*
