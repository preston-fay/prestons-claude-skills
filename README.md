# Preston's Claude Skills Library

A world-class collection of **37 specialized skills** for consulting, analytics, data visualization, document creation, and strategic problem-solving — all available instantly in Claude Code, Claude Desktop, and claude.ai.

[![Skills](https://img.shields.io/badge/skills-37-purple)]() [![Quality](https://img.shields.io/badge/quality-world--class-green)]() [![License](https://img.shields.io/badge/license-Private-red)]()

---

## Quick Start

```bash
# Clone this repository
git clone https://github.com/preston-fay/claude-skills.git ~/.claude/skills

# Verify installation
ls ~/.claude/skills/ | wc -l  # Should show 37+ items

# Test in Claude Code
# Open Claude Code and type:
/skills
```

**Full installation guide:** [INSTALLATION.md](./INSTALLATION.md)

---

## What's Inside?

### 🎯 Strategy & Problem Solving (5 skills)
Build hypothesis trees, decompose problems with MECE frameworks, size markets, analyze value chains, and create growth matrices.

**Examples:**
- `/hypothesis-tree` - Build testable hypothesis trees for any business question
- `/issue-tree` - Decompose complex problems into MECE issue trees
- `/market-sizing` - TAM/SAM/SOM market sizing with sensitivity analysis
- `/value-chain` - Identify margin leakage by value chain stage
- `/growth-matrix` - Portfolio classification (Stars, Cash Cows, Question Marks)

### 📊 Data & Analytics (9 skills)
Exploratory data analysis, insight extraction, causal discovery, geographic mapping, web scraping, and more.

**Examples:**
- `/eda` - Comprehensive exploratory data analysis pipeline
- `/analyze` - Extract insights beyond EDA (trends, segments, anomalies)
- `/bayesian-causal-discovery` - Causal structure learning from tabular data
- `/map` - Create point maps, heatmaps, choropleths, routes
- `/scrape` - Web scraping with rate limiting and pagination

### 📝 Client Deliverables (5 skills)
Structure presentations, synthesize insights, write executive summaries, build data requests, and select analytical methods.

**Examples:**
- `/deck-builder` - Structure presentations with story arcs
- `/insight-synth` - Transform data into actionable insights
- `/exec-summary` - 1-page summaries using SCQA framework
- `/data-request` - Precise data request specifications
- `/methods-guide` - Select the right analytical method

### 📄 Documents (4 skills)
Create and edit PowerPoint, Excel, PDF, and Word documents programmatically.

**Examples:**
- `/pptx` - PowerPoint creation and editing
- `/xlsx` - Excel with formulas and analysis
- `/pdf` - PDF processing and form filling
- `/docx` - Word documents with track changes

### 📈 Visualization & Storytelling (3 skills)
Transform data into compelling narratives, create Kearney-branded dashboards, and build data stories.

**Examples:**
- `/observable-framework` - Kearney-branded dashboards with 16:9 presentations
- `/storytell` - Data storytelling frameworks and templates
- `/kearney-design` - Kearney brand design system (colors, typography, charts)

### 💻 Frontend Development (6 skills)
React best practices, production-grade UI design, web artifacts, accessibility auditing, and testing.

**Examples:**
- `/frontend-design` - Distinctive, production-grade UIs
- `/react-best-practices` - Vercel's 45 React/Next.js optimization rules
- `/web-artifacts-builder` - React + Tailwind + shadcn/ui artifacts
- `/webapp-testing` - Playwright-based web app testing
- `/web-design-guidelines` - UI/UX accessibility auditing
- `/mcp-builder` - Build MCP servers for Claude integration

### 🎨 Design & Creative (2 skills)
Visual art creation and brand design systems.

**Examples:**
- `/canvas-design` - Visual art and poster creation
- `/kearney-design` - Kearney brand compliance

### 🛠️ Utilities (3 skills)
Project setup, skill creation, requirements gathering, and personal writing.

**Examples:**
- `/setup-workflow` - Interview-driven CLAUDE.md generator
- `/create-skill` - Build new custom skills
- `/interview` - Structured requirements gathering
- `/write-as-preston` - Write in Preston's authentic voice

---

## Featured Skills

### `/hypothesis-tree` - MECE Hypothesis Trees

Build structured hypothesis trees with testable sub-hypotheses, data requirements, and kill criteria.

```
/hypothesis-tree Should we acquire CompanyX?
```

**Output:**
- Primary hypothesis (H0)
- 2-4 MECE supporting hypotheses
- Test criteria and data requirements
- Kill criteria (what disproves each hypothesis)
- Validation roadmap (quick wins vs. deep dives)

---

### `/eda` - Exploratory Data Analysis

Comprehensive EDA pipeline with pandas profiling, visualizations, and data quality assessment.

```
/eda data.csv
```

**Includes:**
- Dataset overview (shape, types, missing values)
- Column-level statistics
- Distribution analysis and outlier detection
- Correlation matrices
- Data quality scoring

---

### `/bayesian-causal-discovery` - Causal Structure Learning

Run Bayesian causal analysis on tabular data to discover causal relationships.

```
/bayesian-causal-discovery
```

**Delivers:**
- Directed Acyclic Graph (DAG) of causal relationships
- Bootstrap stability analysis
- Confidence-tiered edge findings
- Root-cause insights

---

### `/observable-framework` - Kearney-Branded Dashboards

Create interactive dashboards with 16:9 slide presentations, light/dark themes, and Kearney branding.

```
/observable-framework
```

**Features:**
- Data visualization with Plot
- Kearney purple color scheme
- Responsive layouts
- Executive-ready presentations

---

## Documentation

| Document | Purpose |
|----------|---------|
| **[INSTALLATION.md](./INSTALLATION.md)** | Complete installation guide with troubleshooting |
| **[SYNC_WORKFLOW.md](./SYNC_WORKFLOW.md)** | How to sync skills across GitHub, claude.ai, and Claude Desktop |
| **[SKILLS_INDEX.md](./SKILLS_INDEX.md)** | Complete catalog of all 37 skills with descriptions |
| **[QUALITY_AUDIT.md](./QUALITY_AUDIT.md)** | Quality assessment (7 world-class, 25 good, 3 acceptable, 2 needs work) |
| **[MY_SKILLS.md](./MY_SKILLS.md)** | Legacy reference (backup, may be outdated) |

---

## Example Workflows

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

---

## Quality

**Quality Distribution:**
- ⭐⭐⭐⭐⭐ **World-class (500+ lines):** 7 skills (19%)
- ⭐⭐⭐⭐ **Good (200-500 lines):** 25 skills (68%)
- ⭐⭐⭐ **Acceptable (100-200 lines):** 3 skills (8%)
- ⭐⭐ **Needs enhancement (<100 lines):** 2 skills (5%)

**All 37 skills have:**
- ✅ Proper SKILL.md files
- ✅ Clear documentation
- ✅ Example invocations
- ✅ Supporting files (where needed)

See [QUALITY_AUDIT.md](./QUALITY_AUDIT.md) for detailed assessment.

---

## GitHub Repositories

This library is synced to **two GitHub repositories** for redundancy:

| Account | URL | Remote | Purpose |
|---------|-----|--------|---------|
| **preston-fay** | https://github.com/preston-fay/claude-skills | `origin` | Personal Claude.ai access |
| **pfay01_kearney** | https://github.com/pfay01_kearney/claude-skills | `work` | Kearney-related usage |

**Both repos stay in perfect sync.** See [SYNC_WORKFLOW.md](./SYNC_WORKFLOW.md) for details.

---

## Stats

- **Total Skills:** 37
- **Lines of Documentation:** 10,000+
- **Categories:** 8
- **Supported Platforms:** macOS, Linux
- **Claude Versions:** Claude Code, Claude Desktop, claude.ai
- **Last Updated:** 2026-02-11

---

## Adding New Skills

```bash
# Create skill directory
mkdir -p ~/.claude/skills/new-skill-name
cd ~/.claude/skills/new-skill-name

# Create SKILL.md
cat > SKILL.md <<EOF
---
name: new-skill-name
description: Brief description
---

# Skill content here...
EOF

# Or use the skill creator
/create-skill
```

See [SYNC_WORKFLOW.md](./SYNC_WORKFLOW.md#workflow-1-adding-a-new-skill) for full instructions.

---

## Contributing

This is a personal skills library. To suggest improvements:

1. Create an issue describing the enhancement
2. Fork the repository
3. Make your changes
4. Submit a pull request

---

## License

**Private** - For personal use by Preston Fay.

---

## Quick Commands

```bash
# List all skills
ls -1 ~/.claude/skills/

# Count skills
ls -1d ~/.claude/skills/*/ | wc -l

# Search for skills by keyword
ls ~/.claude/skills/ | grep -i "data"

# Read a skill's documentation
cat ~/.claude/skills/eda/SKILL.md

# Pull latest updates
cd ~/.claude/skills && git pull origin main

# Push to both GitHub repos
cd ~/.claude/skills && git push origin main && git push work main
```

---

## Architecture

```
~/.claude/skills/
├── analyze/                      # Insight analysis beyond EDA
├── bayesian-causal-discovery/    # Causal discovery (NEW)
├── bootstrap/                    # Project templates
├── canvas-design/                # Visual art creation
├── create-skill/                 # Meta-skill for creating skills
├── data-request/                 # Data request builder
├── deck-builder/                 # Presentation structuring
├── docx/                         # Word document manipulation
├── eda/                          # Exploratory data analysis
├── exec-summary/                 # Executive summary writer
├── frontend-design/              # Production-grade UI creation
├── growth-matrix/                # Portfolio classification
├── hypothesis-tree/              # MECE hypothesis trees
├── insight-synth/                # Insight synthesizer
├── interview/                    # Requirements gathering
├── issue-tree/                   # Problem decomposition
├── kearney-design/               # Kearney brand system
├── map/                          # Geographic visualization
├── market-sizing/                # TAM/SAM/SOM framework
├── mcp-builder/                  # MCP server builder
├── methods-guide/                # Analytical method selector
├── observable-framework/         # Kearney dashboards
├── pdf/                          # PDF manipulation
├── pptx/                         # PowerPoint creation
├── react-best-practices/         # Vercel React optimization
├── remotion/                     # Video production
├── scrape/                       # Web scraping
├── setup-workflow/               # Project setup
├── storytell/                    # Data storytelling
├── value-chain/                  # Value chain analysis
├── web-artifacts-builder/        # React artifacts
├── web-design-guidelines/        # UI/UX auditing
├── webapp-testing/               # Playwright testing
├── write-as-preston/             # Personal writing voice (NEW)
├── xlsx/                         # Excel manipulation
├── .gitignore                    # Git ignore rules
├── INSTALLATION.md               # Installation guide
├── QUALITY_AUDIT.md              # Quality assessment
├── README.md                     # This file
├── SKILLS_INDEX.md               # Complete catalog
├── SYNC_WORKFLOW.md              # Sync instructions
└── skills-index.yaml             # Machine-readable index
```

---

**Built with ❤️ for consulting, analytics, and strategic problem-solving.**

*Last updated: 2026-02-11 | 37 skills | World-class quality*
