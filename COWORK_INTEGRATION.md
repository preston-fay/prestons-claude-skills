# Cowork Integration Guide

This guide explains how Cowork agents can discover and use skills from the `~/.claude/skills` directory.

---

## Overview

**Skills Location:** `~/.claude/skills`
**Machine-Readable Index:** `skills-index.yaml`
**Human-Readable Catalog:** `SKILLS_INDEX.md`
**Total Skills:** 34

Skills are organized into 9 categories and can be invoked by command name (e.g., `/eda`, `/hypothesis-tree`).

---

## How Cowork Discovers Skills

### Option 1: Load Index Explicitly

Cowork can load the complete skills catalog from the YAML index:

```
Load skills from ~/.claude/skills/skills-index.yaml
```

This gives Cowork access to:
- All skill IDs and names
- Command invocation patterns
- "When to use" triggers
- Categories and tags
- Example invocations

### Option 2: Reference SKILLS_INDEX.md

For human-readable reference, Cowork can read:

```
Read ~/.claude/skills/SKILLS_INDEX.md for available skills
```

This provides:
- Category-organized catalog
- Quick navigation
- Recommended workflows
- Usage examples

### Option 3: Direct Skill Access

For a specific skill, Cowork can read the SKILL.md file directly:

```
Read ~/.claude/skills/hypothesis-tree/SKILL.md
```

---

## Skill Invocation Patterns

### Basic Invocation

```
Use /eda to analyze the dataset
Run /hypothesis-tree to frame the business question
Apply /kearney-design to the dashboard
```

### Invocation with Arguments

```
/market-sizing for enterprise AI software
/hypothesis-tree Should we acquire CompanyX?
/issue-tree Why are margins declining?
```

### Chained Skills (Workflows)

```
First run /eda on the data, then use /analyze to extract insights, and finally create a /pptx presentation
```

Recommended workflows:
- **Data Analysis:** `/eda` → `/methods-guide` → `/analyze` → `/insight-synth`
- **New Engagement:** `/interview` → `/hypothesis-tree` → `/issue-tree` → `/data-request`
- **Dashboard Creation:** `/eda` → `/analyze` → `/observable-framework` → `/kearney-design`

---

## Skills by Category

### Problem Solving & Strategy (5)
- `/hypothesis-tree` - Build hypothesis trees with MECE sub-hypotheses
- `/issue-tree` - Decompose problems into structured issue trees
- `/market-sizing` - TAM/SAM/SOM framework
- `/value-chain` - Analyze costs and margins by value chain stage
- `/growth-matrix` - 2x2 portfolio analysis

### Client Deliverables (5)
- `/deck-builder` - Structure presentations
- `/insight-synth` - Transform data into insights
- `/exec-summary` - 1-page executive summaries
- `/data-request` - Precise data specifications
- `/methods-guide` - Select analytical methods

### Data & Analytics (2)
- `/eda` - Exploratory data analysis
- `/analyze` - Extract insights and recommendations

### Data Acquisition (2)
- `/scrape` - Web scraping and APIs
- `/interview` - Requirements gathering

### Visualization & Storytelling (3)
- `/map` - Geographic visualization
- `/storytell` - Data storytelling
- `/observable-framework` - Kearney-branded dashboards

### Documents (4)
- `/pptx` - PowerPoint creation
- `/xlsx` - Excel with formulas
- `/pdf` - PDF processing
- `/docx` - Word documents

### Design (2)
- `/canvas-design` - Visual art creation
- `/kearney-design` - Kearney brand system

### Frontend Development (6)
- `/react-best-practices` - React/Next.js optimization
- `/frontend-design` - Production-grade UI
- `/web-design-guidelines` - Design compliance
- `/web-artifacts-builder` - React + Tailwind + shadcn/ui
- `/webapp-testing` - Playwright testing
- `/mcp-builder` - MCP server development

### Utilities & Development (5)
- `/setup-workflow` - Project setup automation
- `/create-skill` - Create new skills
- `/bootstrap` - Project templates
- `/remotion` - Video production

---

## Search and Discovery

### By Category

```
Show me all skills in the "Data & Analytics" category
List skills for "Client Deliverables"
```

### By Keyword

```
Find skills related to "presentations"
What skills help with "data analysis"?
Show skills for "strategic frameworks"
```

### By Use Case

```
What skill should I use for:
- Framing a business question? → /hypothesis-tree
- Analyzing a dataset? → /eda
- Creating a presentation? → /deck-builder or /pptx
- Building a dashboard? → /observable-framework
```

---

## Example Cowork Queries

### Skill Discovery

**User:** "What skills are available for strategy work?"

**Cowork Response:**
```
I have 5 strategy skills available:
1. /hypothesis-tree - Build hypothesis trees for business questions
2. /issue-tree - Structure problems with MECE decomposition
3. /market-sizing - Calculate TAM/SAM/SOM
4. /value-chain - Analyze costs and margins
5. /growth-matrix - Portfolio classification (2x2)

Would you like me to use one of these?
```

### Skill Usage

**User:** "Analyze this sales data and create insights"

**Cowork:**
```
I'll use the data analysis workflow:
1. First, /eda to explore the dataset structure and quality
2. Then /analyze to extract key insights
3. Finally /insight-synth to transform findings into recommendations

[Proceeds with analysis...]
```

### Workflow Recommendation

**User:** "We're starting a new market entry project"

**Cowork:**
```
For a new market entry project, I recommend this workflow:
1. /interview - Gather complete requirements
2. /hypothesis-tree - Frame key business questions
3. /market-sizing - Assess market opportunity
4. /issue-tree - Structure analysis workplan
5. /data-request - Specify needed data

Shall I start with /interview to gather requirements?
```

---

## Advanced Features

### Context Fork Skills

These skills run in isolated environments to avoid cluttering main context:
- `/eda` - Data analysis
- `/analyze` - Insight extraction
- `/scrape` - Web scraping
- `/map` - Geographic visualization
- `/observable-framework` - Dashboard building

When Cowork invokes these, they execute independently and return results.

### Write Logging Skills

These skills log usage for audit trails:
- `/pptx`, `/xlsx`, `/pdf`, `/docx` - Document creation
- `/eda`, `/analyze`, `/scrape` - Data operations

Logs are written to: `~/.claude/logs/skill-usage.log`

---

## Schema Reference

### skills-index.yaml Structure

```yaml
version: "1.0"
location: ~/.claude/skills
total_skills: 34

skills:
  - id: hypothesis-tree
    name: Hypothesis Tree Builder
    command: /hypothesis-tree
    category: Problem Solving & Strategy
    when_to_use: "Framing business questions, case structuring"
    output: "Structured hypothesis tree with MECE sub-hypotheses"
    examples:
      - "/hypothesis-tree Should we enter European market?"
    location: ~/.claude/skills/hypothesis-tree/
    files: [SKILL.md, README.md]
```

### Key Fields

- **id**: Unique skill identifier (kebab-case)
- **name**: Human-readable skill name
- **command**: Invocation command (e.g., `/eda`)
- **category**: One of 9 standard categories
- **when_to_use**: Trigger description for when to use this skill
- **output**: What the skill produces
- **examples**: Sample invocation patterns
- **location**: Full path to skill directory
- **files**: List of files in skill directory

---

## Health Check

Cowork can verify skill system health:

```
Run ~/.claude/skills/.skillsrc --check
```

This validates:
- All skill directories have SKILL.md files
- Required sections present
- No broken references
- System is healthy

Expected output:
```
✅ All skills are healthy!
Total skills: 34
Passed: 33
Missing SKILL.md: 1 (kearney - reference directory only)
```

---

## Best Practices for Cowork

1. **Load Skills Early**: Load skills-index.yaml at session start for full context

2. **Match Use Cases**: When user describes a need, match to "when_to_use" fields

3. **Recommend Workflows**: Suggest chained skills for complex tasks

4. **Show Examples**: Include example invocations when suggesting skills

5. **Validate Before Use**: Check that skill exists and is appropriate

6. **Handle Missing Skills Gracefully**: If a skill is referenced but not found, suggest alternatives

7. **Use Categories for Discovery**: When user asks "what can you do?", organize by category

8. **Chain Skills Intelligently**: For complex tasks, plan a skill sequence upfront

---

## Troubleshooting

### Skill Not Found

**Issue:** Cowork tries to use `/skill-name` but it doesn't exist

**Solution:**
1. Check skills-index.yaml for correct command name
2. Verify skill directory exists in ~/.claude/skills
3. Suggest similar skills from the same category

### Unclear When to Use

**Issue:** Multiple skills could apply to user's need

**Solution:**
1. List all matching skills with "when_to_use" descriptions
2. Ask user to clarify their specific goal
3. Recommend based on output type they need

### Missing Dependencies

**Issue:** Skill requires tools/libraries not installed

**Solution:**
1. Check skill's SKILL.md for dependencies
2. Inform user of requirements
3. Suggest alternative skills that don't require special setup

---

## Updates and Maintenance

### Adding New Skills

When new skills are added to ~/.claude/skills:
1. Skills are automatically discovered by directory scan
2. Regenerate skills-index.yaml if needed
3. skills-index.yaml can be recreated by scanning all SKILL.md files

### Keeping Index Current

The index can be regenerated:
```bash
cd ~/.claude/skills
python3 /tmp/scan_skills.py  # Regenerates skills-index.yaml
```

---

## Quick Reference Card

**Load Skills:**
```
Load skills from ~/.claude/skills/skills-index.yaml
```

**Find Skill:**
```
What skill helps with [use case]?
```

**Use Skill:**
```
/skill-name [arguments]
```

**List Categories:**
```
Show skills by category
```

**Workflow:**
```
Recommend workflow for [task]
```

**Health Check:**
```
~/.claude/skills/.skillsrc --check
```

---

For complete skill details, see: `~/.claude/skills/SKILLS_INDEX.md`
