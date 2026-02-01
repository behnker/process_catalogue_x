# Design Coherence Analysis
## Process Catalogue Platform - Blueprint v1.5

---

## Purpose Statement

> **"Design business and operating models with clear agentic opportunities identified, reported, projects mobilised and delivery tracked through to adoption with survey and assessment support for the key inputs to process, adoption, capability and readiness"**

---

## Purpose Decomposition

To test coherence, I've broken the purpose into **8 key capabilities**:

| # | Capability | Keywords |
|---|------------|----------|
| **P1** | Design business models | Business model design |
| **P2** | Design operating models | Operating model design |
| **P3** | Identify agentic opportunities | Agentic opportunities identified |
| **P4** | Report on opportunities | Reported |
| **P5** | Mobilise projects | Projects mobilised |
| **P6** | Track delivery | Delivery tracked |
| **P7** | Track adoption | Through to adoption |
| **P8** | Survey & assessment support | Survey and assessment support for process, adoption, capability, readiness |

---

## Feature-by-Feature Analysis

---

## Feature 1: Business Model

### Purpose Alignment Matrix

| Capability | Supported? | How? | Gap? |
|------------|------------|------|------|
| **P1: Design business models** | ✅ FULL | Business Model Canvas with 13 components (Markets, Clients, Categories, Partners, Channels, Value Propositions, Revenue, Cost, etc.) | None |
| **P2: Design operating models** | ⚪ INDIRECT | Links to processes via Business Model Mapping | Primary responsibility is Component 4 |
| **P3: Identify agentic opportunities** | ⚠️ PARTIAL | Can identify which BM components need improvement via RIADA | No explicit "agentic opportunity" flag or AI/automation potential indicator |
| **P4: Report on opportunities** | ✅ FULL | RIADA summary, heatmaps, dashboards at BM level | None |
| **P5: Mobilise projects** | ✅ FULL | Links to Portfolio; BM components can be scope of projects | None |
| **P6: Track delivery** | ⚪ INDIRECT | Via linked projects | Primary responsibility is Component 5 |
| **P7: Track adoption** | ⚪ INDIRECT | Via Change & Adoption | Primary responsibility is Component 6 |
| **P8: Survey support** | ⚪ INDIRECT | Operating Model Survey assesses BM-linked processes | Primary responsibility is Component 7 |

### Coherence Score: 7/10

### Analysis

**Strengths:**
- Complete Business Model Canvas implementation
- Strong linkage to Process Catalogue (process-to-BM-component mapping)
- RIADA at BM level captures strategic risks/issues
- Clear connection to Portfolio for project mobilisation

**Gaps Identified:**

| Gap ID | Gap Description | Severity | Recommendation |
|--------|-----------------|----------|----------------|
| BM-G1 | No explicit "Agentic Opportunity" identifier at BM level | Medium | Add field to CanvasEntry: `agentic_potential` (None/Low/Medium/High) with description of automation/AI opportunity |
| BM-G2 | No direct survey for Business Model health | Low | Consider "Strategic Alignment Survey" as 5th survey type, or include BM questions in Operating Model Survey |

---

## Feature 2: Process Catalogue

### Purpose Alignment Matrix

| Capability | Supported? | How? | Gap? |
|------------|------------|------|------|
| **P1: Design business models** | ⚪ INDIRECT | Links processes to BM components | Primary responsibility is Component 1 |
| **P2: Design operating models** | ✅ FULL | 6-level hierarchy (L0-L5), Primary/Secondary processes, comprehensive SOM content | None |
| **P3: Identify agentic opportunities** | ⚠️ PARTIAL | Agent Catalogue exists; processes can be linked to agents | No systematic way to flag "this process is a candidate for AI/automation" |
| **P4: Report on opportunities** | ✅ FULL | Process Canvas, heatmaps, overlays, RAG status reporting | None |
| **P5: Mobilise projects** | ✅ FULL | Project-Process linking shows which processes are in scope | None |
| **P6: Track delivery** | ⚪ INDIRECT | Via linked projects | Primary responsibility is Component 5 |
| **P7: Track adoption** | ⚪ INDIRECT | Via Change & Adoption, Adoption Evidence Survey | Primary responsibility is Component 6 |
| **P8: Survey support** | ✅ FULL | Operating Model Survey directly assesses processes (SPRD dimensions) | None |

### Coherence Score: 8/10

### Analysis

**Strengths:**
- Comprehensive 6-level hierarchy captures all operational detail
- Strong Business Model linkage (Market, Client, Category tagging)
- RAG status (System, People, Process, Data) aligns with improvement identification
- Excellent visualization (Canvas, overlays, heatmaps)
- Clear ownership model (Sponsor → Owner → SME)

**Gaps Identified:**

| Gap ID | Gap Description | Severity | Recommendation |
|--------|-----------------|----------|----------------|
| PC-G1 | No explicit "Agentic Opportunity" or "Automation Candidate" flag on processes | Medium | Add to Process entity: `agentic_potential` (None/Low/Medium/High), `agentic_opportunity_description`, `current_agent_id` (FK to Agent Catalogue) |
| PC-G2 | Agent Catalogue exists but linkage to processes is weak | Medium | Strengthen Operating Model "Agents" component to explicitly map which processes have agents today vs. could have agents |

---

## Feature 3: Quality Logs (RIADA)

### Purpose Alignment Matrix

| Capability | Supported? | How? | Gap? |
|------------|------------|------|------|
| **P1: Design business models** | ⚪ INDIRECT | RIADA items can be linked to BM components | Primary responsibility is Component 1 |
| **P2: Design operating models** | ⚪ INDIRECT | RIADA items linked to processes inform OM design | Primary responsibility is Component 4 |
| **P3: Identify agentic opportunities** | ✅ FULL | Issues categorized by System dimension often indicate automation opportunities; manual workarounds logged as issues | None - this is where opportunities surface |
| **P4: Report on opportunities** | ✅ FULL | RIADA dashboards, severity reporting, category breakdowns, heatmaps | None |
| **P5: Mobilise projects** | ✅ FULL | RIADA items link to projects; issues drive project creation | None |
| **P6: Track delivery** | ✅ FULL | RIADA at project level tracks delivery risks/issues | None |
| **P7: Track adoption** | ⚠️ PARTIAL | Adoption issues can be logged | No specific RIADA type for "Adoption Blocker" |
| **P8: Survey support** | ✅ FULL | Operating Model Survey populates RIADA (RED ratings → Issues); Survey results feed issue identification | None |

### Coherence Score: 9/10

### Analysis

**Strengths:**
- RIADA framework is comprehensive (Risk, Issue, Action, Dependency, Assumption)
- 4-dimensional categorization (People, Process, System, Data) aligns perfectly with opportunity identification
- Severity levels enable prioritization
- Strong linkage to all other components (Process, Project, BM)
- Auto-creation from Survey results (RED → Issue)

**Gaps Identified:**

| Gap ID | Gap Description | Severity | Recommendation |
|--------|-----------------|----------|----------------|
| QL-G1 | No specific RIADA category for "Agentic/Automation Opportunity" | Low | Consider adding RIADA type "Opportunity" (O) to make RIADAO, or add tag `is_agentic_opportunity` to existing types |
| QL-G2 | No specific tracking for adoption-related issues during change | Low | Add RIADA category "Adoption" alongside People/Process/System/Data, OR add tag for adoption-phase issues |

---

## Feature 4: Operating Model Design

### Purpose Alignment Matrix

| Capability | Supported? | How? | Gap? |
|------------|------------|------|------|
| **P1: Design business models** | ⚪ INDIRECT | OM supports BM execution | Primary responsibility is Component 1 |
| **P2: Design operating models** | ✅ FULL | 10 comprehensive components: RACI, KPIs, Policies, Governance, Systems, Agents, Security, Data, Timing, Prompt Library | None |
| **P3: Identify agentic opportunities** | ✅ FULL | **Agents component** explicitly designed for this; Current vs Future state comparison shows where agents can be added | None |
| **P4: Report on opportunities** | ✅ FULL | Current vs Future state reporting; Agent coverage reporting | None |
| **P5: Mobilise projects** | ✅ FULL | Future state designs become project scope | None |
| **P6: Track delivery** | ⚪ INDIRECT | Via linked projects | Primary responsibility is Component 5 |
| **P7: Track adoption** | ⚠️ PARTIAL | Future state defines "what adoption looks like" | No direct adoption measurement in OM |
| **P8: Survey support** | ✅ FULL | Operating Model Survey directly assesses all OM dimensions | None |

### Coherence Score: 9/10

### Analysis

**Strengths:**
- **Agents component is specifically designed for agentic opportunities** - this is a core strength
- Current vs Future state enables transformation planning
- Comprehensive coverage (RACI, KPIs, Policies, Governance, Systems, Agents, Security, Data, Timing)
- Prompt Library integration for AI-assisted design
- Strong survey integration (SPRD assessment)

**Gaps Identified:**

| Gap ID | Gap Description | Severity | Recommendation |
|--------|-----------------|----------|----------------|
| OM-G1 | Agents component could be more detailed | Low | Enhance Agents component to include: `agent_type` (RPA, AI Assistant, Workflow, Integration), `automation_level` (Assisted, Semi-Automated, Fully Automated), `implementation_status` (Identified, Evaluating, Implementing, Live, Retired) |
| OM-G2 | No explicit "Automation Readiness Score" per process | Low | Consider deriving score from: Data quality + Process standardization + System integration readiness |

---

## Feature 5: Portfolio Response

### Purpose Alignment Matrix

| Capability | Supported? | How? | Gap? |
|------------|------------|------|------|
| **P1: Design business models** | ⚪ INDIRECT | Projects can transform BM components | Primary responsibility is Component 1 |
| **P2: Design operating models** | ⚪ INDIRECT | Projects implement OM changes | Primary responsibility is Component 4 |
| **P3: Identify agentic opportunities** | ⚠️ PARTIAL | Projects can be tagged as "Automation" type | No systematic agentic opportunity intake from other components |
| **P4: Report on opportunities** | ✅ FULL | Portfolio dashboards, WSVF prioritization, status reporting | None |
| **P5: Mobilise projects** | ✅ FULL | **Core purpose** - Complete project hierarchy (Pillar → Programme → Project → Workstream → Work Package) | None |
| **P6: Track delivery** | ✅ FULL | **Core purpose** - Milestones, RAG status, budget tracking, RIADA at every level | None |
| **P7: Track adoption** | ⚠️ PARTIAL | Benefits tracking exists | Adoption measurement deferred to Component 6 |
| **P8: Survey support** | ✅ FULL | Change Readiness Survey, Adoption Evidence Survey both link to projects | None |

### Coherence Score: 9/10

### Analysis

**Strengths:**
- Complete project hierarchy (7 levels)
- WSVF prioritization framework for objective prioritization
- Comprehensive milestone tracking (Project, Customer, Financial, Benefit types)
- RIADA at every portfolio level
- Strong process linkage (which processes are transformed by which projects)
- Budget and financial tracking
- Benefits realization tracking

**Gaps Identified:**

| Gap ID | Gap Description | Severity | Recommendation |
|--------|-----------------|----------|----------------|
| PR-G1 | No automatic "opportunity to project" conversion workflow | Medium | Add feature: Convert RIADA Issue/Opportunity to Project with pre-populated scope from linked process |
| PR-G2 | No explicit "Agentic Project" classification | Low | Add project tag or type: `is_agentic_initiative` to filter/report on automation projects specifically |

---

## Feature 6: Change & Adoption Monitoring

### Purpose Alignment Matrix

| Capability | Supported? | How? | Gap? |
|------------|------------|------|------|
| **P1: Design business models** | ⚪ N/A | Not in scope | — |
| **P2: Design operating models** | ⚪ N/A | Not in scope | — |
| **P3: Identify agentic opportunities** | ⚪ N/A | Not in scope | — |
| **P4: Report on opportunities** | ⚪ INDIRECT | Reports on adoption gaps which may indicate opportunities | — |
| **P5: Mobilise projects** | ⚪ INDIRECT | Low adoption may trigger remediation projects | — |
| **P6: Track delivery** | ⚠️ PARTIAL | Tracks post-delivery adoption | Primary delivery tracking is Component 5 |
| **P7: Track adoption** | ✅ FULL | **Core purpose** - Lead indicators, lag indicators, KPI tracking, benefits realization | None |
| **P8: Survey support** | ✅ FULL | Adoption Evidence Survey directly measures adoption | None |

### Coherence Score: 8/10

### Analysis

**Strengths:**
- Lead and lag indicator framework
- KPI selection from central catalogue
- Benefits realization tracking
- Direct integration with Adoption Evidence Survey

**Gaps Identified:**

| Gap ID | Gap Description | Severity | Recommendation |
|--------|-----------------|----------|----------------|
| CA-G1 | Component feels lightweight compared to others | Medium | Expand to include: Adoption playbooks, intervention triggers, stakeholder sentiment tracking, training completion tracking |
| CA-G2 | No explicit link back to Process Catalogue to update process "adoption status" | Medium | Add workflow: When adoption hits threshold, update Process status or trigger notification to Process Owner |

---

## Feature 7: Surveys

### Purpose Alignment Matrix

| Capability | Supported? | How? | Gap? |
|------------|------------|------|------|
| **P1: Design business models** | ⚪ INDIRECT | Survey results may inform BM decisions | — |
| **P2: Design operating models** | ✅ FULL | Operating Model Survey directly assesses OM health (SPRD) | None |
| **P3: Identify agentic opportunities** | ✅ FULL | AI Fluency Survey identifies capability; OM Survey (System dimension) identifies automation gaps | None |
| **P4: Report on opportunities** | ✅ FULL | Survey dashboards, AFI distribution, SPRD heatmaps | None |
| **P5: Mobilise projects** | ⚠️ PARTIAL | Survey results inform project priorities | No direct "Survey Result → Project" conversion |
| **P6: Track delivery** | ⚪ INDIRECT | Change Readiness Survey pre-project; Adoption post-project | — |
| **P7: Track adoption** | ✅ FULL | Adoption Evidence Survey directly measures adoption (Process, Role, KPI evidence) | None |
| **P8: Survey support** | ✅ FULL | **Core purpose** - 4 survey types covering all dimensions | None |

### Coherence Score: 9/10

### Analysis

**Strengths:**
- 4 comprehensive survey types perfectly aligned to purpose:
  - **AI Fluency** → Capability assessment
  - **Operating Model** → Process health assessment
  - **Change Readiness** → Readiness assessment
  - **Adoption Evidence** → Adoption measurement
- AFI scoring (0-100) provides quantifiable capability metric
- SPRD framework (System, People, Process, Data) aligns with RIADA categories
- ADKAR-based readiness assessment
- Strong integration with other components (auto-create RIADA from RED ratings)

**Gaps Identified:**

| Gap ID | Gap Description | Severity | Recommendation |
|--------|-----------------|----------|----------------|
| SV-G1 | No "Agentic Readiness" survey or questions | Low | Add questions to AI Fluency or OM Survey: "Is this process a good candidate for automation?", "What barriers exist to automation?" |
| SV-G2 | No direct conversion of survey findings to projects | Low | Add feature: "Create Project from Survey Finding" to streamline mobilisation |

---

## Consolidated Gap Analysis

### All Identified Gaps

| Gap ID | Component | Description | Severity | Status |
|--------|-----------|-------------|----------|--------|
| BM-G1 | Business Model | No explicit "Agentic Opportunity" identifier | Medium | **RECOMMEND ADD** |
| BM-G2 | Business Model | No direct BM health survey | Low | Optional |
| PC-G1 | Process Catalogue | No "Automation Candidate" flag on processes | Medium | **RECOMMEND ADD** |
| PC-G2 | Process Catalogue | Weak Agent Catalogue linkage to processes | Medium | **RECOMMEND ADD** |
| QL-G1 | Quality Logs | No RIADA type for "Opportunity" | Low | Optional |
| QL-G2 | Quality Logs | No adoption-specific RIADA category | Low | Optional |
| OM-G1 | Operating Model | Agents component could be more detailed | Low | Optional |
| OM-G2 | Operating Model | No "Automation Readiness Score" | Low | Optional |
| PR-G1 | Portfolio | No "Opportunity to Project" conversion workflow | Medium | **RECOMMEND ADD** |
| PR-G2 | Portfolio | No "Agentic Project" classification | Low | Optional |
| CA-G1 | Change & Adoption | Component feels lightweight | Medium | **RECOMMEND EXPAND** |
| CA-G2 | Change & Adoption | No link back to Process to update status | Medium | **RECOMMEND ADD** |
| SV-G1 | Surveys | No "Agentic Readiness" questions | Low | Optional |
| SV-G2 | Surveys | No "Survey to Project" conversion | Low | Optional |

### Priority Gaps to Address

| Priority | Gap ID | Recommendation |
|----------|--------|----------------|
| 1 | PC-G1 + BM-G1 | Add `agentic_potential` field to Process and CanvasEntry entities |
| 2 | PC-G2 | Strengthen Process ↔ Agent linkage in Operating Model |
| 3 | PR-G1 | Add "Convert to Project" workflow from RIADA/Survey findings |
| 4 | CA-G1 + CA-G2 | Expand Change & Adoption with intervention triggers and process status updates |

---

## Overall Coherence Assessment

### Scorecard

| Component | Coherence Score | Key Strength | Key Gap |
|-----------|-----------------|--------------|---------|
| 1. Business Model | 7/10 | Complete BMC implementation | No agentic opportunity flag |
| 2. Process Catalogue | 8/10 | Comprehensive hierarchy + visualization | Weak agent linkage |
| 3. Quality Logs (RIADA) | 9/10 | Perfect alignment with opportunity identification | Minor: No "Opportunity" type |
| 4. Operating Model | 9/10 | Agents component is core strength | Could be more detailed |
| 5. Portfolio Response | 9/10 | Complete project lifecycle | No opportunity-to-project workflow |
| 6. Change & Adoption | 8/10 | Good adoption measurement | Lightweight, needs expansion |
| 7. Surveys | 9/10 | 4 surveys cover all dimensions | Minor: No agentic readiness questions |

### Overall Score: **8.4 / 10**

### Verdict: **COHERENT WITH MINOR ENHANCEMENTS RECOMMENDED**

---

## Purpose Fulfilment Matrix

| Purpose Element | Fully Met? | Primary Component(s) | Supporting Component(s) |
|-----------------|------------|---------------------|------------------------|
| **Design business models** | ✅ Yes | Business Model | Process Catalogue |
| **Design operating models** | ✅ Yes | Operating Model, Process Catalogue | Quality Logs |
| **Identify agentic opportunities** | ⚠️ Partial | Operating Model (Agents), Quality Logs | Surveys (AI Fluency) |
| **Report on opportunities** | ✅ Yes | All (Dashboards, Heatmaps, Overlays) | — |
| **Mobilise projects** | ✅ Yes | Portfolio Response | Quality Logs (RIADA) |
| **Track delivery** | ✅ Yes | Portfolio Response | Quality Logs (RIADA) |
| **Track adoption** | ✅ Yes | Change & Adoption, Surveys | Portfolio (Benefits) |
| **Survey/Assessment support** | ✅ Yes | Surveys (4 types) | Operating Model Survey |

### The One Gap That Matters Most

**"Identify agentic opportunities"** is the weakest link. While the system can *surface* issues that *imply* automation opportunities (via RIADA System issues, OM Survey System RED ratings, AI Fluency low scores), there is no **explicit, first-class "Agentic Opportunity"** concept.

**Recommendation:** Add explicit agentic opportunity tracking:

```
Process Catalogue Enhancement:
├── agentic_potential: ENUM (None, Low, Medium, High)
├── agentic_opportunity_description: TEXT
├── current_automation_level: ENUM (Manual, Assisted, Semi-Auto, Fully-Auto)
├── target_automation_level: ENUM (same)
└── linked_agent_id: FK → Agent Catalogue

New Report:
├── "Agentic Opportunity Register"
├── Processes with High agentic potential
├── Gap: Current vs Target automation level
└── Linked projects addressing automation
```

---

## Conclusion

The Blueprint v1.5 design is **coherent and well-integrated**. The 7 components work together to deliver the stated purpose with clear handoffs:

```
Business Model → defines strategic context
       ↓
Process Catalogue → defines operational detail
       ↓
Quality Logs (RIADA) → captures issues and opportunities
       ↓
Operating Model → designs current and future state (including Agents)
       ↓
Portfolio Response → mobilises and tracks projects
       ↓
Change & Adoption → measures adoption
       ↓
Surveys → provides assessment inputs at each stage
```

**With the recommended enhancements**, the system will explicitly support agentic opportunity identification as a first-class concept, completing the alignment with the stated purpose.

---

*Analysis completed: January 31, 2026*
*Blueprint Version Analyzed: 1.5*
