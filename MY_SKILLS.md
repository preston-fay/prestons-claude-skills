# Preston's Claude Skills Library

> **📢 IMPORTANT:** This file has been replaced by **[SKILLS_INDEX.md](./SKILLS_INDEX.md)**
>
> The new index is more comprehensive (34 skills vs 31), better organized, and includes:
> - Complete catalog of ALL skills in ~/.claude/skills
> - Improved search and navigation
> - Example invocations for every skill
> - Recommended workflows
> - Health status and validation
>
> **Please use:** [SKILLS_INDEX.md](./SKILLS_INDEX.md)
>
> _(This file is kept as a backup but may be out of date)_

---

## Legacy Content Below (May Be Outdated)

A comprehensive collection of **31 skills** for consulting, analytics, data visualization, document creation, and strategic problem-solving. These skills are available from any project.

---

## Quick Reference Table

| Skill | Command | Category | Description |
|-------|---------|----------|-------------|
| **Problem Solving & Strategy** |
| Hypothesis Tree | `/hypothesis-tree` | Strategy | Build MECE hypothesis trees with test criteria |
| Issue Tree | `/issue-tree` | Strategy | Decompose problems into structured issue trees |
| Market Sizing | `/market-sizing` | Strategy | TAM/SAM/SOM market sizing framework |
| Value Chain | `/value-chain` | Strategy | Analyze cost and margin by value chain stage |
| Growth Matrix | `/growth-matrix` | Strategy | 2x2 portfolio analysis (Stars, Cash Cows, etc.) |
| **Client Deliverables** |
| Deck Builder | `/deck-builder` | Presentation | Structure presentations with story arcs |
| Insight Synthesizer | `/insight-synth` | Analysis | Transform data into actionable insights |
| Exec Summary | `/exec-summary` | Writing | 1-page executive summaries using SCQA |
| Data Request | `/data-request` | Data | Precise data request specifications |
| Methods Guide | `/methods-guide` | Analytics | Select and execute analytical methods |
| **Data & Analytics** |
| EDA | `/eda` | Analytics | Exploratory data analysis pipeline |
| Analyze | `/analyze` | Analytics | Extract insights from EDA findings |
| **Data Acquisition** |
| Scrape | `/scrape` | Data | Web scraping and API data acquisition |
| Interview | `/interview` | Requirements | Structured requirements gathering |
| **Visualization & Storytelling** |
| Map | `/map` | Visualization | Geographic data visualization |
| Storytell | `/storytell` | Narrative | Data storytelling frameworks |
| Observable Framework | `/observable-framework` | Dashboards | Kearney-branded dashboards with 16:9 slides (light/dark themes) |
| **Documents** |
| PPTX | `/pptx` | Documents | PowerPoint creation and editing |
| XLSX | `/xlsx` | Documents | Excel with formulas and analysis |
| PDF | `/pdf` | Documents | PDF processing and forms |
| DOCX | `/docx` | Documents | Word documents with track changes |
| **Design** |
| Canvas Design | `/canvas-design` | Design | Visual art and poster creation |
| Kearney Design | `/kearney-design` | Design | Kearney brand design system |
| **Frontend Development** | | | |
| React Best Practices | `/react-best-practices` | Frontend | Vercel's 45 React/Next.js optimization rules |
| Frontend Design | `/frontend-design` | Frontend | Production-grade UI with distinctive aesthetics |
| Web Design Guidelines | `/web-design-guidelines` | Frontend | Web interface design principles |
| Web Artifacts Builder | `/web-artifacts-builder` | Frontend | React + Tailwind + shadcn/ui artifacts |
| Webapp Testing | `/webapp-testing` | Testing | Playwright-based web app testing |
| MCP Builder | `/mcp-builder` | Development | Build MCP servers for Claude integration |
| **Utilities** |
| Setup Workflow | `/setup-workflow` | Setup | Project setup automation |
| Create Skill | `/create-skill` | Meta | Create new custom skills |

---

## Problem Solving & Strategy Skills

### `/hypothesis-tree` - Hypothesis Tree Builder

**Purpose:** Build structured hypothesis trees with MECE sub-hypotheses, test criteria, data requirements, and kill criteria. The canonical consulting problem-solving tool.

**Best for:**
- Framing business questions for analysis
- Case structuring
- Building testable hypotheses
- M&A evaluation, market entry decisions

**What You Get:**
- Primary hypothesis (H0)
- 2-4 MECE supporting hypotheses (H1, H2, H3...)
- Test criteria for each branch
- Data requirements
- Kill criteria (what disproves the hypothesis)
- Validation roadmap (quick wins vs. deep dives)

**Example:** "Should we acquire CompanyX?" → Full tree with revenue synergies, cost synergies, integration risk branches

---

### `/issue-tree` - Issue Tree Decomposer

**Purpose:** Decompose complex problems into clean MECE issue trees with 3-4 levels of structured breakdown.

**Best for:**
- Problem structuring
- Root cause analysis
- Workplan development
- Diagnostic frameworks

**What You Get:**
- Root problem statement (bounded, actionable)
- 3-5 Level 1 branches (MECE)
- Level 2-3 sub-issues
- MECE validation checklist
- Analysis mapping (what analysis for each branch)
- Prioritization guide

**Common Patterns Included:**
- Profitability problems (Revenue vs. Cost vs. Asset efficiency)
- Growth problems (Existing customers, New customers, New products, New geographies)
- Operational problems (People, Process, Technology, External)

---

### `/market-sizing` - TAM/SAM/SOM Market Sizing

**Purpose:** Size markets using Total Addressable Market (TAM), Serviceable Addressable Market (SAM), and Serviceable Obtainable Market (SOM) framework.

**Best for:**
- Market opportunity assessment
- Investor pitch preparation
- Strategic planning
- Business case development

**What You Get:**
- TAM calculation with assumptions
- SAM with filters applied
- SOM projections (Year 1, 3, 5)
- Top-down and bottom-up validation
- Sensitivity analysis
- Sanity checks (implied market share, comparable companies)

---

### `/value-chain` - Value Chain Diagnostic

**Purpose:** Analyze cost, revenue, and margin by value chain stage to identify where margin is leaking or where costs are concentrated.

**Best for:**
- Cost reduction initiatives
- Margin improvement
- Make vs. buy decisions
- Operational diagnostics

**What You Get:**
- Stage-by-stage cost and margin breakdown
- Benchmark comparison
- Margin leakage identification
- Root cause analysis
- Prioritized recommendations (quick wins vs. structural changes)

**Stages Analyzed:** R&D → Procurement → Manufacturing → Logistics → Sales → Service (customizable)

---

### `/growth-matrix` - Growth-Efficiency Matrix

**Purpose:** Classify business units, products, or segments into strategic quadrants for portfolio decisions.

**Quadrants:**
- **Stars** (High Growth, High Efficiency): Protect & Grow
- **Question Marks** (High Growth, Low Efficiency): Invest or Exit
- **Cash Cows** (Low Growth, High Efficiency): Harvest
- **Turnarounds** (Low Growth, Low Efficiency): Fix or Divest

**What You Get:**
- Portfolio classification table
- Quadrant-specific strategic actions
- Resource allocation recommendations
- Watch list (entities near quadrant borders)
- Sensitivity analysis

---

## Client Deliverables Skills

### `/deck-builder` - Slide Deck Builder

**Purpose:** Structure compelling presentations that tell a clear story and drive decisions.

**Story Arc Templates:**
1. **Situation-Complication-Resolution (SCR)**: Best for recommendations
2. **Question-Answer Structure**: Best for diagnostics
3. **Option Comparison**: Best for strategic choices
4. **Progress Update**: Best for steering committees

**What You Get:**
- Story arc selection
- Slide flow outline
- Action titles (not topic titles!)
- Slide count guidance
- Appendix structure
- Deck review checklist

**Key Rule:** Every slide needs an action title that states the "so what" — not just the topic.

---

### `/insight-synth` - Insight Synthesizer

**Purpose:** Transform raw analysis into meaningful, actionable insights. Master the "So What?" skill.

**The Insight Hierarchy:**
```
LEVEL 4: RECOMMENDATION    → "Therefore, we should..."
LEVEL 3: INSIGHT          → "This means that..."
LEVEL 2: INFORMATION      → "The data shows..."
LEVEL 1: DATA             → "We have 10,000 records..."
```

**Quality Rubric (score each insight):**
- Specific (names names)
- Quantified (has numbers)
- Causal (explains why)
- Actionable (someone can do something)
- Surprising (non-obvious)

**Templates Included:**
- Diagnostic findings
- Opportunity identification
- Risk identification
- Competitive insights

---

### `/exec-summary` - Executive Summary Writer

**Purpose:** Distill complex analysis into compelling 1-page summaries.

**The SCQA Framework:**
| Component | Purpose | Length |
|-----------|---------|--------|
| Situation | Establish shared context | 1-2 sentences |
| Complication | Introduce the tension | 1-2 sentences |
| Question | Frame what needs answering | 1 sentence |
| Answer | Your recommendation | 2-4 sentences |

**Word Count Targets:**
- Email summary: 100-150 words
- Executive brief: 200-300 words
- Full exec summary: 400-500 words
- Board memo: 600-800 words max

**Golden Rule:** If it's longer than 1 page, it's not an executive summary.

---

### `/data-request` - Data Request Builder

**Purpose:** Create precise, complete data requests that get you the right data the first time.

**What You Get:**
- Complete request template
- Field-level specifications (format, examples, nulls)
- Scope definition (time, geography, exclusions)
- Delivery specs (format, naming, method)
- Data quality checklist for when you receive data
- Escalation language templates

**Timeline Expectations:**
| Complexity | Typical Timeline |
|------------|------------------|
| Simple extract | 2-3 business days |
| Multiple systems | 5-7 business days |
| Custom calculations | 7-10 business days |
| New pipeline | 2-4 weeks |

---

### `/methods-guide` - Analytical Methods Guide

**Purpose:** Select the right analytical method for your business question.

**Method Selection:**
| Business Question | Primary Method |
|-------------------|----------------|
| "What drives our [metric]?" | Regression Analysis |
| "How has [metric] changed over time?" | Time Series Analysis |
| "Which customers/products are similar?" | Cluster Analysis |
| "Did our intervention work?" | A/B Testing |
| "What's the optimal allocation?" | Optimization |

**For Each Method:**
- When to use
- Data requirements
- Execution steps
- Interpretation checklist
- How to communicate results
- Common pitfalls
- Visualization recommendations

---

## Data & Analytics Skills

### `/eda` - Exploratory Data Analysis

**Purpose:** Comprehensive EDA pipeline with pandas.

**Functions:**
- `dataset_overview(df)` - Shape, types, missing values
- `profile_columns(df)` - Column-level stats
- `analyze_numerics(df)` - Distributions, outliers
- `analyze_correlations(df)` - Relationships
- `assess_data_quality(df)` - Quality scoring
- `run_full_eda(filepath)` - Complete pipeline

**Output:** Markdown report with visualizations using Kearney colors

---

### `/analyze` - Insight Analysis

**Purpose:** Extract deeper insights beyond EDA.

**Capabilities:**
- Trend identification and anomaly detection
- Segment comparison and benchmarking
- Pareto analysis (80/20)
- Statistical hypothesis testing
- RFM customer segmentation
- Executive summary generation

**When to Use:** After EDA, when stakeholders need actionable recommendations

---

## Data Acquisition Skills

### `/scrape` - Web Scraper

**Purpose:** Web scraping and data acquisition from websites and APIs.

**Methods:**
- Static HTML: requests + BeautifulSoup
- JavaScript pages: Playwright
- REST APIs: Pagination and rate limiting

**Ethics:** Always respects robots.txt, ToS, and uses polite rate limits

---

### `/interview` - Requirements Interview

**Purpose:** Structured 18-question requirements gathering.

**5 Phases:**
1. Context & Objectives (4 questions)
2. Scope & Constraints (4 questions)
3. Domain Deep-Dive (4 questions)
4. Priorities & Risks (3 questions)
5. Confirmation & Next Steps (3 questions)

**Output:** Structured requirements document with MoSCoW prioritization

---

## Visualization & Storytelling Skills

### `/map` - Geographic Mapping

**Purpose:** Create geographic visualizations from location data.

**Map Types:**
- Point maps (markers, bubbles)
- Heatmaps
- Choropleth maps (regions)
- Clustered markers
- Route visualization

**Libraries:** Folium, Plotly
**Styling:** Kearney purple gradient

---

### `/storytell` - Data Storytelling

**Purpose:** Transform data analysis into compelling narratives.

**Story Structures:**
- Problem-Solution arc
- Journey structure
- Comparison frame
- "Here's What I Found" format

**Templates:**
- Executive summary
- One-pager
- Presentation outline
- Insight slides

---

## Document Skills

### `/pptx` - PowerPoint Builder
Create and edit presentations with html2pptx conversion, OOXML editing, and template workflows.

### `/xlsx` - Excel Workbook Builder
Create workbooks with formulas, formatting, financial models. Includes recalculation support.

### `/pdf` - PDF Processor
Text extraction, PDF creation, merging/splitting, form filling, OCR.

### `/docx` - Word Document Builder
Create and edit documents with tracked changes, comments, formatting preservation.

---

## Design Skills

### `/canvas-design` - Visual Art Creator
Create beautiful visual art in PNG and PDF formats. Original designs for posters and creative assets.

### `/kearney-design` - Kearney Brand System

**Critical Rules:**
- **Primary:** Kearney Purple (#3A0069)
- **Chart colors:** Must follow prescribed order (1-10)
- **NO GRIDLINES** on any charts
- **Typography:** Inter (digital), Arial (print)
- **No pie charts** with >4 segments
- **No 3D effects** or dual y-axes

---

## Utility Skills

### `/setup-workflow` - Project Setup
Interview-driven CLAUDE.md generator for new projects.

### `/create-skill` - Skill Creator
Build new custom skills with proper structure and YAML frontmatter.

---

## Skill Chaining: Example Workflows

### New Engagement Workflow
```
1. /interview       → Gather requirements
2. /hypothesis-tree → Frame the problem
3. /issue-tree      → Decompose into workstreams
4. /data-request    → Specify data needs
```

### Data Analysis Workflow
```
1. /eda            → Explore the data
2. /methods-guide  → Select analytical approach
3. /analyze        → Extract insights
4. /insight-synth  → Synthesize findings
```

### Deliverable Creation Workflow
```
1. /exec-summary   → Write executive summary
2. /deck-builder   → Structure presentation
3. /storytell      → Craft the narrative
4. /pptx           → Create the slides
5. /kearney-design → Apply brand standards
```

### Market/Strategy Analysis Workflow
```
1. /market-sizing  → Size the opportunity
2. /value-chain    → Diagnose operations
3. /growth-matrix  → Prioritize portfolio
4. /hypothesis-tree → Build strategic hypotheses
```

---

## How to Use Skills

### Invoking a Skill
```
/eda
/hypothesis-tree
/deck-builder
```

### Passing Arguments
```
/market-sizing enterprise AI software
/hypothesis-tree Should we enter the European market?
/exec-summary [paste content to summarize]
```

### File Locations

| Type | Location | Scope |
|------|----------|-------|
| Personal skills | `~/.claude/skills/<name>/SKILL.md` | All projects |
| Project skills | `.claude/skills/<name>/SKILL.md` | That project only |

Project-level overrides personal-level for same name.

---

## Adding New Skills

```bash
# Create directory
mkdir -p ~/.claude/skills/<skill-name>

# Create SKILL.md with YAML frontmatter
```

```yaml
---
name: skill-name
description: Brief description
disable-model-invocation: true
argument-hint: "[optional argument hint]"
---

# Skill content here...
```

Or use `/create-skill` to scaffold automatically.

---

## Skill Summary by Category

| Category | Skills | Count |
|----------|--------|-------|
| Problem Solving | hypothesis-tree, issue-tree, market-sizing, value-chain, growth-matrix | 5 |
| Client Deliverables | deck-builder, insight-synth, exec-summary, data-request, methods-guide | 5 |
| Data & Analytics | eda, analyze | 2 |
| Data Acquisition | scrape, interview | 2 |
| Visualization | map, storytell, observable-framework | 3 |
| Documents | pptx, xlsx, pdf, docx | 4 |
| Design | canvas-design, kearney-design | 2 |
| Frontend Development | react-best-practices, frontend-design, web-design-guidelines, web-artifacts-builder, webapp-testing, mcp-builder | 6 |
| Utilities | setup-workflow, create-skill | 2 |
| **Total** | | **31** |

---

## Quick Tips

- **Always start with the problem:** Use `/hypothesis-tree` or `/issue-tree` before diving into analysis
- **Data quality first:** Run `/eda` before any analysis to understand your data
- **Brand compliance:** Use `/kearney-design` when creating any client-facing visuals
- **Insight hierarchy:** Push from data → information → insight → recommendation
- **One message per slide:** Use `/deck-builder` to structure before creating slides
- **MECE everything:** Issue trees, hypotheses, and recommendations should all be MECE
- **Action titles:** Every slide title should state the "so what," not just the topic
- **React apps:** Use `/react-best-practices` for Vercel's 45 optimization rules when building React/Next.js apps
- **UI testing:** Use `/webapp-testing` to verify frontend functionality with Playwright

---

*Last updated: 2026-02-04 | Total Skills: 31*
