# UI Design Specification - Questions & Decisions Needed

## What We Already Have in the Blueprint (v1.8)

Before listing gaps, here's what's already specified:

| Area | Coverage | Location |
|------|----------|----------|
| Process Canvas layout | Good (swimlane, L0→L5) | Section 10.1 |
| Canvas interactions | Good (click, expand, hover) | Section 10.1.3 |
| Canvas toolbar & overlays | Good (11 overlay types) | Section 10.6 |
| Alternative views (Tree, List, Card) | Basic structure | Section 10.2 |
| Process Detail view | Good (layout + 6 tabs) | Section 10.3 |
| Executive Dashboard | Good (wireframe) | Section 10.4.1 |
| RIADA/Portfolio/Survey dashboards | Summary only | Section 10.4 |
| Navigation sidebar | Basic structure | Section 10.7 |
| Color palette | Defined | Section 10.7.1 |
| Typography | Defined | Section 10.7.2 |
| Component library | Listed | Section 10.7.3 |
| Responsive breakpoints | Basic rules | Section 10.7.4 |
| Key screens list | 15 screens listed | Section 10.8 |
| Heatmap/Overlay controls | Detailed | Section 10.6.3 |
| Auth flow | Defined (v1.8) | Section 6.2 |

---

## What's Missing / Needs Your Input

I've grouped the questions into categories. For each, I've noted the priority and suggested a default if you'd prefer to move fast.

---

## 1. GLOBAL LAYOUT & SHELL

### Q1.1: Application Shell Layout
**What layout pattern do you want for the main app shell?**

```
Option A: Fixed Sidebar + Content          Option B: Top Nav + Content
┌──────┬──────────────────┐                ┌──────────────────────────┐
│ Nav  │                  │                │  Top Navigation Bar      │
│      │   Content Area   │                ├──────────────────────────┤
│      │                  │                │                          │
│      │                  │                │   Content Area           │
│      │                  │                │                          │
└──────┴──────────────────┘                └──────────────────────────┘

Option C: Collapsible Sidebar + Content
┌──┬──────────────────────┐    ┌──────┬──────────────────┐
│☰ │                      │ ↔  │ Nav  │                  │
│  │   Content Area       │    │      │  Content Area    │
│  │                      │    │      │                  │
└──┴──────────────────────┘    └──────┴──────────────────┘
(collapsed = icons only)       (expanded = icons + labels)
```

**Suggested default:** Option C (collapsible sidebar) — most common in modern SaaS tools, gives maximum canvas space when collapsed.

---

### Q1.2: Sidebar Width
When expanded, how wide should the sidebar be?
- Narrow: 220px (just fits labels)
- Standard: 260px (comfortable)
- Wide: 300px (room for nested items)

**Suggested default:** 260px expanded, 64px collapsed (icon-only)

---

### Q1.3: Header Bar Content
What should the persistent top header contain?

Typical options:
- Organization name / logo
- Current page title / breadcrumbs
- Global search
- Notifications bell
- User avatar + dropdown
- Quick-action button (e.g., "+ New")
- Environment indicator (e.g., "Surity - Production")

**Which of these do you want? Anything else?**

---

### Q1.4: Multi-Organization Switcher
Users could belong to multiple organizations (e.g., a consultant). Do you want an organization switcher?
- Yes, in header
- Yes, on login screen only
- No, users belong to one org

---

## 2. PROCESS CANVAS (Already partially specified — gap-filling)

### Q2.1: Canvas Background
What should the canvas background look like?
- Plain white
- Subtle dot grid (like Figma/Miro)
- Subtle line grid
- Light gradient

**Suggested default:** Subtle dot grid — signals "workspace" visually

---

### Q2.2: Canvas Zoom & Pan
The canvas could get very large (100+ L2 processes). Should users be able to:
- Zoom in/out (Ctrl+scroll or pinch)?
- Pan by dragging background?
- Mini-map navigator (like VS Code)?
- Fit-to-view button?

**Suggested default:** All of the above

---

### Q2.3: Process Card Size on Canvas
What size should L2 process cards be on the canvas?
- Small: ~120×60px (fits more, less detail)
- Medium: ~160×80px (shows name + RAG dots)
- Large: ~200×100px (shows name + RAG + issue count + owner avatar)

**Suggested default:** Medium (160×80) — shows enough at a glance without overcrowding

---

### Q2.4: L3/L4/L5 Expansion Behavior
Currently specified as "expandable nested menus." Should these:
- Expand inline (push other content down)?
- Open in a slide-over panel from the right?
- Open as a modal/dialog?
- Open in a dedicated "drill-down" view replacing the canvas?

**Suggested default:** Slide-over panel from the right — keeps canvas visible for context

---

### Q2.5: Process Canvas Empty State
What should users see when an organization has no processes yet?
- Illustration + "Create your first process" CTA?
- Template gallery ("Start from Surity template")?
- Guided setup wizard?

---

## 3. SCREENS NOT YET WIREFRAMED

These screens are listed in Section 10.8 but don't have wireframes or detailed specifications. For each, I need to know the key information and layout priorities.

### Q3.1: Business Model Canvas Screen
How should the Business Model Canvas be displayed?
- Traditional BMC grid layout (9 boxes)?
- List view by component?
- Both, with toggle?

What interactions should be available?
- Click a box to see entries?
- Drag-and-drop entries between components?
- Inline editing?

---

### Q3.2: RIADA List Screen
What's the primary view for the RIADA register?
- Table/grid (like a spreadsheet)?
- Kanban board (columns by status)?
- Both, with toggle?

What filters matter most?
- Type (Risk, Issue, Action, Dependency, Assumption)?
- Severity (Critical, High, Medium, Low)?
- Status (Open, In Progress, Resolved)?
- Owner?
- Linked process?

---

### Q3.3: RIADA Detail Screen
What layout for an individual RIADA item?
- Full-page detail view?
- Side panel (like Jira/Linear)?
- Modal dialog?

What information needs to be visible at a glance?
- Title, description, severity, status?
- Linked process(es)?
- Owner + assignee?
- History/comments?
- Related RIADA items?

---

### Q3.4: Portfolio View
How should the portfolio hierarchy be displayed?
- Tree view (Strategic Pillar → Programme → Project → Work Package)?
- Gantt chart?
- Kanban by status?
- Table/list?

What's the most important information per project?
- Status (RAG)?
- Timeline (start/end dates)?
- Budget?
- Process linkage?
- WSVF priority score?

---

### Q3.5: Survey Builder Screen
How complex should the survey builder be?
- Simple form builder (like Google Forms)?
- More structured (section-based with scoring)?
- Template-based only (select from 4 survey types, customize questions)?

Should survey preview be:
- Live preview next to editor (side-by-side)?
- Separate preview tab?

---

### Q3.6: Survey Response Screen
What should the respondent experience look like?
- One question per page (wizard-style)?
- All questions on one scrollable page?
- Section-by-section with progress bar?

---

### Q3.7: Prompt Library Screen
How should prompts be browsed?
- Card grid (like an app store)?
- Table/list?
- Categorized sections?

What should the prompt execution experience look like?
- Full-page with context panel + input + output?
- Side panel?
- Chat-like interface?

---

### Q3.8: Reference Data Management
How should reference catalogues (Roles, Systems, Suppliers, etc.) be managed?
- One unified screen with tabs per catalogue?
- Separate page per catalogue?
- Single settings page with nested sections?

---

### Q3.9: Settings Screens
What settings pages are needed?

Likely:
- Organization settings (name, branding, domains)
- User management (invite, roles, deactivate)
- Domain management (add, verify, remove)
- Integration settings (GitHub, LLM providers)
- Notification preferences
- Data export/import

Anything else?

---

### Q3.10: Login / Registration Screens
What should the login experience feel like?
- Minimal (email field + submit, branded background)?
- Branded landing page with login embedded?
- Separate marketing page and login page?

Should there be an organization-branded login (e.g., surity.processcatalogue.com)?

---

## 4. COMPONENT BEHAVIOR & PATTERNS

### Q4.1: Data Table Standard
For all list/table views, what features are expected?

| Feature | Include? |
|---------|----------|
| Column sorting | ? |
| Column filtering | ? |
| Column resizing | ? |
| Column reordering | ? |
| Row selection (checkbox) | ? |
| Bulk actions (on selected rows) | ? |
| Inline editing | ? |
| Pagination vs. infinite scroll | ? |
| Row click → detail view | ? |
| Export (CSV, Excel) | ? |
| Saved views/filters | ? |

**Suggested default:** Sorting ✓, Filtering ✓, Pagination ✓, Row click ✓, Export ✓, rest optional.

---

### Q4.2: Form Patterns
How should create/edit forms work?
- Full-page form?
- Slide-over panel?
- Modal dialog?
- Inline editing (click to edit)?

Should forms auto-save or require explicit save?

---

### Q4.3: Notification System
What notifications should the system send?

| Event | In-App | Email |
|-------|--------|-------|
| RIADA item assigned to you | ? | ? |
| RIADA item escalated | ? | ? |
| Project status changed | ? | ? |
| Survey assigned to you | ? | ? |
| New user registered | ? | ? |
| Process status changed | ? | ? |
| Comment/mention | ? | ? |
| Magic link login | N/A | ✓ |

**Do you want a notification center (bell icon with dropdown)?**

---

### Q4.4: Search
What type of search do you want?
- Global search (searches everything)?
- Scoped search (search within current view)?
- Both with keyboard shortcut (Cmd+K)?

Should search include:
- Processes?
- RIADA items?
- Projects?
- People?
- Prompts?
- Reference data?

**Suggested default:** Global search (Cmd+K) covering all entities.

---

### Q4.5: Dark Mode
Do you want dark mode support?
- Yes, system-preference aware
- Yes, manual toggle
- No, light only

**Suggested default:** Light only for v1, dark mode later.

---

## 5. OPERATING MODEL DESIGN

### Q5.1: Operating Model Component Editing
The Operating Model has 10 components per process. How should users edit these?

Option A: All on one scrollable page under the "Operating Model" tab
Option B: Sub-tabs within the Operating Model tab (RACI | KPIs | Policies | ...)
Option C: Accordion sections that expand/collapse

**Which pattern?**

---

### Q5.2: RACI Matrix Display
How should the RACI matrix be displayed?
- Grid/table (Roles across top, Activities down left)?
- List view (one row per role-activity pair)?
- Visual diagram?

Should users be able to:
- Click cells to toggle R/A/C/I?
- Drag roles to assign?
- Filter by role or activity?

---

### Q5.3: KPI Display
How should KPIs be displayed per process?
- Simple table (KPI, target, actual, trend)?
- Dashboard cards with sparklines?
- Both?

---

### Q5.4: Current State vs. Future State Toggle
The Operating Model supports current and future state. How should this be toggled?
- Toggle switch in header ("Viewing: Current / Future")?
- Side-by-side comparison mode?
- Tabs ("Current State" | "Future State" | "Gap Analysis")?

---

## 6. REPORTS & EXPORTS

### Q6.1: Report Viewing
How should reports be displayed?
- In-app rendered (HTML)?
- PDF preview?
- Both?

### Q6.2: Export Formats
Which export formats are priority?
- PDF (formatted report)?
- Excel (data export)?
- PowerPoint (presentation)?
- CSV (raw data)?
- Word document?

**Suggested default:** PDF + Excel as priority, others later.

---

### Q6.3: Custom Report Builder
How sophisticated should the report builder be?
- Simple: Pick template, select filters, generate
- Medium: Choose sections, arrange layout, add charts
- Advanced: Drag-and-drop report designer (like Tableau/Power BI)

**Suggested default:** Simple for v1 — template + filters.

---

## 7. BRANDING & THEME

### Q7.1: Organization Branding
Should organizations be able to customize:
- Logo in sidebar/header?
- Primary color (override blue)?
- Custom favicon?
- Login page background?

---

### Q7.2: Surity-Specific Branding
For the initial deployment, do you have:
- Surity logo (SVG preferred)?
- Surity brand colors?
- Surity brand fonts?
- Any existing style guides?

If so, should the default theme match Surity branding?

---

## 8. ACCESSIBILITY

### Q8.1: Accessibility Standard
What level of accessibility compliance do you need?
- WCAG 2.1 AA (recommended standard)?
- WCAG 2.1 AAA (maximum)?
- Basic (keyboard navigation + screen reader basics)?

**Suggested default:** WCAG 2.1 AA — industry standard, legally required in many markets.

---

## 9. CONTENT & COPY

### Q9.1: Tone of Voice
What tone should the application use?
- Professional/formal ("Your process has been updated")?
- Friendly/conversational ("Nice! Process updated")?
- Neutral/minimal ("Process updated")?

---

### Q9.2: Empty States
Should empty states include:
- Illustrations?
- Helpful copy explaining what goes here?
- Quick-action buttons?
- Links to documentation?

---

### Q9.3: Onboarding
Should there be a guided onboarding for new users?
- Step-by-step wizard?
- Tooltip tour?
- Sample data they can explore?
- Video walkthrough?
- None (assume trained users)?

---

## 10. CHINA-SPECIFIC UI

### Q10.1: Language Support
What languages are needed?
- English only?
- English + Simplified Chinese?
- Full i18n framework (add languages later)?

**Suggested default:** English only for v1, i18n framework in place for future.

---

### Q10.2: China UI Adjustments
Any specific adjustments for China deployment?
- Different fonts (system fonts vs. Inter)?
- Removed Google dependencies (fonts, maps, analytics)?
- WeChat integration (login, notifications)?

---

## Summary: Priority Decisions Needed

These are the decisions I need most to begin detailed wireframing:

| # | Question | Priority |
|---|----------|----------|
| Q1.1 | App shell layout (sidebar style) | **Critical** |
| Q1.3 | Header bar content | **Critical** |
| Q2.4 | L3/L4/L5 expansion behavior | **Critical** |
| Q3.1 | Business Model Canvas screen | **High** |
| Q3.2 | RIADA list screen pattern | **High** |
| Q3.4 | Portfolio view pattern | **High** |
| Q4.1 | Data table features standard | **High** |
| Q4.2 | Form patterns (modal vs panel vs page) | **High** |
| Q5.4 | Current/Future state toggle | **High** |
| Q3.10 | Login screen style | **Medium** |
| Q4.3 | Notification system | **Medium** |
| Q7.2 | Surity branding assets | **Medium** |

**You can answer all, some, or just the critical ones — and I'll use sensible defaults for the rest.**

---

*Prepared: January 31, 2026*
