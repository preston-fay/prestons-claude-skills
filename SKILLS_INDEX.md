# Skills Index - Complete Reference
**Last Updated:** 2026-03-01 | **Location:** `~/.claude/skills` | **Total Skills:** 37

Complete catalog of all available skills for Claude Code and Cowork. This index replaces `MY_SKILLS.md` with a more comprehensive, searchable reference.

---

## Quick Navigation
- [Problem Solving & Strategy](#problem-solving--strategy) (5 skills)
- [Client Deliverables](#client-deliverables) (5 skills)
- [Data & Analytics](#data--analytics) (2 skills)
- [Data Acquisition](#data-acquisition) (2 skills)
- [Visualization & Storytelling](#visualization--storytelling) (3 skills)
- [Documents](#documents) (4 skills)
- [Design](#design) (3 skills)
- [Frontend Development](#frontend-development) (6 skills)
- [Utilities & Development](#utilities--development) (7 skills)

---

## Problem Solving & Strategy

### Hypothesis Tree → `/hypothesis-tree`
**When:** Framing business questions, case structuring, M&A evaluation
**Output:** Structured hypothesis tree with MECE sub-hypotheses, test criteria, data requirements, kill criteria
**Example:** `/hypothesis-tree Should we enter the European market?`

### Issue Tree → `/issue-tree`
**When:** Problem structuring, root cause analysis, workplan development
**Output:** MECE issue tree with 3-4 levels, analysis mapping, prioritization
**Example:** `/issue-tree Why are our margins declining?`

### Market Sizing → `/market-sizing`
**When:** TAM/SAM/SOM calculations, market opportunity assessment, investor pitches
**Output:** Bottoms-up and top-down market size estimates, sensitivity analysis
**Example:** `/market-sizing enterprise AI software market`

### Value Chain → `/value-chain`
**When:** Cost reduction, margin improvement, make vs buy decisions, operational diagnostics
**Output:** Stage-by-stage cost/margin breakdown, benchmarks, margin leakage identification
**Example:** `/value-chain automotive manufacturing process`

### Growth Matrix → `/growth-matrix`
**When:** Portfolio classification, resource allocation, investment prioritization
**Output:** 2x2 matrix (Stars, Cash Cows, Question Marks, Dogs) with strategic recommendations
**Example:** `/growth-matrix classify our product portfolio`

---

## Client Deliverables

### Deck Builder → `/deck-builder`
**When:** Building client presentations, organizing findings into narrative, structuring slides
**Output:** Presentation structure with story arcs, slide types, action titles, deck flow
**Example:** `/deck-builder create presentation structure for market entry recommendation`

### Insight Synthesizer → `/insight-synth`
**When:** Transforming data into actionable insights, mastering the "So What?" skill
**Output:** Insights using Insight Hierarchy, SCQA, Pyramid Principle
**Example:** `/insight-synth synthesize findings from revenue analysis`

### Exec Summary → `/exec-summary`
**When:** Writing 1-page summaries for executives, distilling complex analysis
**Output:** SCQA-structured executive summary with key findings and recommendations
**Example:** `/exec-summary summarize cost reduction opportunities`

### Data Request → `/data-request`
**When:** Requesting data from clients/teams, defining data specifications
**Output:** Precise data request with fields, formats, timeframes, quality criteria
**Example:** `/data-request build specification for customer transaction data`

### Methods Guide → `/methods-guide`
**When:** Selecting analytical methods for business questions, determining how to analyze data
**Output:** Method selection (regression, segmentation, optimization), execution guidance
**Example:** `/methods-guide what analysis for customer churn problem?`

---

## Data & Analytics

### EDA → `/eda`
**When:** Starting data analysis, understanding dataset structure, quality checks
**Output:** Statistical summaries, distributions, correlations, anomalies, visualizations
**Example:** `/eda analyze sales_data.csv`
**Note:** Uses context fork for isolated execution

### Analyze → `/analyze`
**When:** Going beyond EDA to extract insights and recommendations
**Output:** Key patterns, business implications, actionable recommendations, executive summary
**Example:** `/analyze extract insights from customer behavior data`
**Note:** Uses context fork for isolated execution

---

## Data Acquisition

### Scrape → `/scrape`
**When:** Web scraping, extracting data from websites/APIs, building datasets
**Output:** Structured data from web pages, pagination handling, rate limiting
**Example:** `/scrape extract product prices from ecommerce site`
**Note:** Uses context fork for isolated execution

### Interview → `/interview`
**When:** Structured requirements gathering at project start, scoping engagements
**Output:** Complete requirements documentation, success criteria, scope definition
**Example:** `/interview gather requirements for analytics project`

---

## Visualization & Storytelling

### Map → `/map`
**When:** Geographic data visualization, mapping points/regions/routes, spatial analysis
**Output:** Interactive maps with markers, choropleth maps, route visualization
**Example:** `/map visualize store locations by revenue`
**Note:** Uses context fork for isolated execution

### Storytell → `/storytell`
**When:** Communicating insights to stakeholders, creating data-driven narratives
**Output:** Compelling narratives that persuade and inform, storytelling frameworks
**Example:** `/storytell create narrative for quarterly business review`

### Observable Framework → `/observable-framework`
**When:** Building interactive dashboards, data-driven presentations, analytical reports
**Output:** Kearney-branded Observable Framework dashboards with 16:9 slide presentations
**Example:** `/observable-framework create dashboard for market analysis`
**Note:** Uses context fork for isolated execution

---

## Documents

### PPTX → `/pptx`
**When:** Creating or editing PowerPoint presentations programmatically
**Output:** .pptx files with slides, formatting, charts, tables
**Example:** `/pptx create presentation from analysis results`
**Note:** Has write logging for audit trail

### XLSX → `/xlsx`
**When:** Creating/editing Excel spreadsheets with formulas and analysis
**Output:** .xlsx files with formulas, formatting, data validation, charts
**Example:** `/xlsx create financial model spreadsheet`
**Note:** Has write logging for audit trail

### PDF → `/pdf`
**When:** Processing PDFs, filling forms, extracting text/tables
**Output:** PDF manipulation, form filling, text extraction, document merging
**Example:** `/pdf fill form fields in contract template`
**Note:** Has write logging for audit trail

### DOCX → `/docx`
**When:** Creating/editing Word documents with track changes, comments
**Output:** .docx files with formatting, tracked changes, comments
**Example:** `/docx create report with tracked changes`
**Note:** Has write logging for audit trail

---

## Design

### Canvas Design → `/canvas-design`
**When:** Creating visual art, posters, designs, static pieces
**Output:** Beautiful .png and .pdf documents with design philosophy
**Example:** `/canvas-design create poster for conference`

### KDS Design → `kds-design` (auto-applies)
**When:** Auto-applies to ALL visual generation tasks — UI, dashboards, visualizations, slides, layouts, components
**Output:** UDPE-enforced output: 8px grid, Major Third type scale, WCAG AA contrast, token discipline, spatial rhythm
**Note:** Non-invocable — auto-applies via description matching. Supersedes kearney-design with Layers 0-3 structural enforcement. Backed by TypeScript reference implementation at `/Users/pfay01/Projects/kds-design/src/`

### Kearney Design → `/kearney-design` *(superseded by kds-design)*
**When:** Creating ANY visual element - charts, slides, dashboards, reports
**Output:** Kearney brand compliance - colors, typography, chart formatting, layout
**Example:** `/kearney-design apply brand standards to dashboard`
**Note:** Retained for backward compatibility. kds-design absorbs all Layer 0 tokens and adds Layers 1-3 enforcement.

---

## Frontend Development

### React Best Practices → `/react-best-practices`
**When:** Writing/reviewing/refactoring React or Next.js code for optimal performance
**Output:** Vercel's 45 optimization rules applied to code
**Example:** `/react-best-practices review component performance`

### Frontend Design → `/frontend-design`
**When:** Building web components, pages, dashboards, React components, HTML/CSS layouts
**Output:** Distinctive, production-grade UI that avoids generic AI aesthetics
**Example:** `/frontend-design create landing page for product launch`

### Web Design Guidelines → `/web-design-guidelines`
**When:** Reviewing UI code for compliance, accessibility audits, UX review
**Output:** Design compliance report, accessibility issues, UX recommendations
**Example:** `/web-design-guidelines audit design of checkout flow`

### Web Artifacts Builder → `/web-artifacts-builder`
**When:** Creating complex artifacts with React + Tailwind + shadcn/ui components
**Output:** Multi-component artifacts with state management, routing
**Example:** `/web-artifacts-builder build interactive calculator`

### Webapp Testing → `/webapp-testing`
**When:** Testing local web applications, verifying frontend functionality
**Output:** Playwright-based tests, screenshots, browser logs
**Example:** `/webapp-testing test user login flow`

### MCP Builder → `/mcp-builder`
**When:** Building MCP servers to integrate external services with Claude
**Output:** MCP server implementation (Python FastMCP or Node/TypeScript)
**Example:** `/mcp-builder create MCP server for Slack integration`

---

## Utilities & Development

### Skills → `/skills` 🆕
**When:** Need to see what skills are available, can't remember a command name
**Output:** Complete skills catalog (this document) with all categories and commands
**Example:** `/skills` (then ask follow-up questions like "show me data skills")
**Note:** Meta-skill that displays this index - your quickest way to browse all capabilities

### Commands → `/commands` 🆕
**When:** Need to see workflow commands (Boris + custom), can't remember command names
**Output:** Complete command catalog - Boris workflow (7) + custom commands (16)
**Example:** `/commands` (then ask "what does /verify-app do?")
**Note:** Commands = project workflow; Skills = individual tasks

### Setup Workflow → `/setup-workflow`
**When:** Starting new coding project, configuring AI workflow preferences
**Output:** CLAUDE.md or AI_INSTRUCTIONS.md with testing, commits, task management rules
**Example:** `/setup-workflow configure project workflow preferences`

### Create Skill → `/create-skill`
**When:** Creating new custom skills, building workflow automations
**Output:** Skill directory with SKILL.md, documentation, template structure
**Example:** `/create-skill build custom analysis skill`

### Bootstrap → `/bootstrap`
**When:** Starting new project from templates (python-data, python-app, consulting, research)
**Output:** Complete project structure with venv, git, testing, tooling, documentation
**Example:** `/bootstrap python-data new-analysis-project`

### Remotion → `/remotion`
**When:** Creating videos, motion graphics, animated explainers, product demos
**Output:** Complete Remotion project with scenes, assets, animations
**Example:** `/remotion create product demo video`
**Note:** End-to-end pipeline from interview to rendered video

### Kearney (Utilities) → `kearney/`
**Note:** Directory present but no SKILL.md - likely contains reference materials or utilities

---

## Recommended Workflows (Skill Chaining)

### New Engagement
```
/interview → /hypothesis-tree → /issue-tree → /data-request
```
Gather requirements, frame hypotheses, structure problems, specify data needs

### Data Analysis Pipeline
```
/eda → /methods-guide → /analyze → /insight-synth
```
Explore data, select methods, extract insights, synthesize findings

### Dashboard Creation
```
/eda → /analyze → /observable-framework → /kearney-design
```
Analyze data, extract insights, build dashboard, apply branding

### Deliverable Creation
```
/exec-summary → /deck-builder → /storytell → /pptx → /kearney-design
```
Summarize findings, structure presentation, craft narrative, create slides, apply brand

### Market/Strategy Analysis
```
/market-sizing → /value-chain → /growth-matrix → /hypothesis-tree
```
Size opportunity, analyze margins, classify portfolio, test hypotheses

---

## How to Use

### In Claude Code CLI
Invoke any skill using its command:
```bash
/eda analyze sales_data.csv
/hypothesis-tree Should we acquire CompanyX?
/deck-builder create presentation for market entry
```

### In Cowork
Load skills via `skills-index.yaml`, then invoke by command name:
```
Load skills from ~/.claude/skills/skills-index.yaml
Use /eda to analyze the dataset
```

### Search Skills
Find skills by keyword:
```bash
grep -i "data analysis" ~/.claude/skills/SKILLS_INDEX.md
grep -i "presentation" ~/.claude/skills/SKILLS_INDEX.md
```

### Browse by Category
Open this file and use Quick Navigation links to jump to categories

---

## Advanced Features

### Context Fork Skills
These skills run in isolated sub-agents to avoid cluttering main context:
- `/eda` - Data analysis
- `/analyze` - Insight extraction
- `/scrape` - Web scraping
- `/map` - Geographic visualization
- `/observable-framework` - Dashboard building

### Write Logging Skills
These skills log tool usage for audit trails:
- `/pptx` - PowerPoint creation
- `/xlsx` - Excel creation
- `/pdf` - PDF processing
- `/docx` - Word processing
- Data & analytics skills (eda, analyze, scrape)

View logs: `tail ~/.claude/logs/skill-usage.log`

---

## Health Status
**Skills with SKILL.md:** 33/34 ✓
**Skills without SKILL.md:** 1 (kearney directory)

Run health check: `~/.claude/skills/.skillsrc --check` (coming soon)

---

## Maintenance

**Adding New Skills:**
1. Create directory in `~/.claude/skills/<skill-name>/`
2. Add `SKILL.md` file with required sections
3. Update this index manually or regenerate

**Updating This Index:**
This file can be regenerated from the skills directory. Keep manual edits minimal.

**Reporting Issues:**
If a skill doesn't work as documented, check:
1. SKILL.md file exists in skill directory
2. Command name matches documented name
3. Required dependencies installed (for data skills: pandas, numpy, etc.)

---

## Key Principles

1. **Always start with the problem** - Use `/hypothesis-tree` or `/issue-tree` before diving into analysis
2. **Data quality first** - Run `/eda` before any analysis to understand your data
3. **Brand compliance** - `kds-design` auto-applies to all visual output (supersedes `/kearney-design`)
4. **Insight hierarchy** - Push from data → information → insight → recommendation
5. **Action titles** - Every slide title states the "so what," not just the topic
6. **MECE everything** - Issue trees, hypotheses, and recommendations should be MECE

---

**Need help?** Open a skill's SKILL.md file for detailed documentation:
```bash
cat ~/.claude/skills/hypothesis-tree/SKILL.md
```
