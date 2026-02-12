---
name: bootstrap
description: "Bootstrap new projects from templates (python-data, python-app, consulting, research, generic). Use when starting a new project or creating a new workspace."
user-invocable: true
argument-hint: "[template-name] [project-name]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash(python3 *)
  - Bash(mkdir *)
  - Bash(git *)
hooks:
  PostToolUse:
    - matcher: "*"
      command: ["bash", "/Users/pfay01/.claude/hooks/hook.logging.tool-use.sh"]
---

# Bootstrap Skill

Fast, opinionated project creation from production-ready templates.

## Overview

This skill creates complete project structures with best practices baked in:
- Python virtual environments
- Git initialization
- Testing infrastructure
- Quality tooling (black, ruff, mypy, pytest)
- Documentation templates
- Kearney Design System integration (for consulting projects)

## Templates Available

### `python-data` - Data Analysis Project

**Use when:** Starting a data analysis, research project, or exploratory work

**Structure:**
```
project-name/
├── src/                  # Custom code modules
├── notebooks/            # Jupyter notebooks (numbered)
│   └── 01_exploratory_analysis.ipynb
├── data/
│   ├── raw/             # Original data (immutable)
│   └── processed/       # Cleaned data
├── reports/             # Outputs, figures, PDFs
├── tests/               # pytest tests
├── requirements.txt     # Dependencies
├── pyproject.toml       # Tool config
├── CLAUDE.md            # AI instructions
├── README.md
└── .gitignore
```

**Dependencies:** pandas, matplotlib, seaborn, plotly, jupyter, pytest, black, ruff

### `python-app` - Python Application

**Use when:** Building a Flask/FastAPI app, CLI tool, or service

**Structure:**
```
project-name/
├── src/
│   └── project_name/    # Package directory
│       ├── __init__.py
│       ├── main.py
│       └── config.py
├── tests/               # pytest structure
├── requirements.txt
├── pyproject.toml
├── Makefile             # install, test, lint, run
├── CLAUDE.md
├── README.md
└── .gitignore
```

**Dependencies:** flask/fastapi, pytest, httpx, black, ruff, mypy

### `consulting` - Kearney Consulting Deliverable

**Use when:** Creating a Kearney-branded analysis, presentation, or report

**Structure:**
```
project-name/
├── data/                # Analysis inputs
├── analysis/            # Jupyter notebooks
├── deliverables/        # Final outputs
├── requirements.txt
├── kds-config.yaml      # Kearney Design System settings
├── CLAUDE.md            # Kearney brand rules
├── README.md
└── .gitignore
```

**Dependencies:** pandas, matplotlib, plotly, jupyterlab, kds tokens

**Special:** Enforces Kearney brand rules (no gridlines, logo must be image, etc.)

### `research` - Research Memo

**Use when:** Writing research memos, whitepapers, technical docs

**Structure:**
```
project-name/
├── research/            # Markdown files
├── references/          # PDFs, links, sources
├── build/               # Generated PDFs
├── requirements.txt
├── template.md          # SCQA structure
├── Makefile             # build PDF target
├── CLAUDE.md
├── README.md
└── .gitignore
```

**Dependencies:** pandoc, markdown, jupyter

### `generic` - Minimal Python Project

**Use when:** Starting a simple script or small project

**Structure:**
```
project-name/
├── src/
├── tests/
├── requirements.txt
├── pyproject.toml
├── CLAUDE.md
├── README.md
└── .gitignore
```

**Dependencies:** pytest, black, ruff (minimal)

## Usage

### From Claude Code

```
/bootstrap python-data customer-analysis
/bootstrap consulting market-entry-strategy
/bootstrap research ai-regulatory-landscape
/bootstrap python-app customer-api
/bootstrap generic quick-script
```

### What Happens

1. **Creates directory structure** based on template
2. **Renders templates** with project-specific variables (name, date, author)
3. **Initializes git** repository
4. **Creates virtual environment** (`python3 -m venv venv`)
5. **Installs dependencies** (via pip)
6. **Prints next steps** with activation command

### After Bootstrap

```bash
cd project-name
source venv/bin/activate  # Windows: venv\Scripts\activate
# Start working!
```

## Template Variables

All templates support Jinja2 variables:

- `{{ project_name }}` - Project directory name
- `{{ date }}` - Current date (YYYY-MM-DD)
- `{{ year }}` - Current year
- `{{ author }}` - From git config user.name

## Examples

### Create Data Analysis Project

```
/bootstrap python-data customer-segmentation
```

Creates a complete data science project with notebooks, data directories, and pytest.

### Create Consulting Deliverable

```
/bootstrap consulting q1-strategy-review
```

Creates a Kearney-branded project with KDS integration and brand compliance rules.

### Create Research Project

```
/bootstrap research generative-ai-landscape
```

Creates a research memo structure with Markdown → PDF build pipeline.

## Error Handling

- **Directory exists:** Will not overwrite. Choose a different name.
- **Template not found:** Lists available templates.
- **Python not found:** Error message with installation instructions.

## Customization

Templates are located in `~/.claude/templates/`. You can:
- Add custom templates
- Modify existing templates
- Add project-specific files

## Integration with Other Skills

After bootstrapping, use these skills:

- `/eda` - Run exploratory data analysis on data files
- `/analyze` - Deep analysis with insights
- `/deck-builder` - Turn analysis into presentation
- `/insight-synth` - Extract actionable insights

## Notes

- Always creates Python 3.9+ compatible projects
- Git initialized but no initial commit (you control first commit)
- Virtual environment created but not activated (manual activation)
- Dependencies installed only if pip is available
