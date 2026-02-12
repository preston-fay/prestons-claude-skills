# Commands - List All Available Commands

Quick reference to display all available commands (Boris workflow + custom commands).

---

## Purpose

Display a complete catalog of all slash commands available beyond the skills library. This includes Boris quality workflow commands and your custom project commands.

---

## When to Use

- You can't remember what commands are available
- You need to find a command for project workflow
- You want to see Boris quality commands
- You're exploring available project commands

**Triggers:** "show my commands", "list commands", "what commands do I have"

---

## Usage

### Basic Invocation
```
/commands
```

This displays all available commands organized by category.

### Follow-up Questions
```
/commands
[then ask:]
What does /verify-app do?
Show me the git workflow commands
Which command creates projects?
```

---

## What You Get

Complete command catalog showing:
- **Boris Workflow Commands** (7) - Project quality and git workflow
- **Custom Project Commands** (16) - Your KIE and analysis commands
- Command descriptions and when to use them

---

## Output Format

Commands organized by category:
1. **Boris Workflow** - Quality gates, testing, git workflow
2. **KIE Project** - KIE framework commands
3. **Analysis** - Data and analysis workflows

---

## Examples

### Example 1: Show All Commands
```
User: /commands
Assistant: [Displays complete command catalog]
```

### Example 2: Find Specific Command
```
User: /commands
Assistant: [Shows catalog]
User: Which command checks code quality?
Assistant: /verify-app - Runs full quality check (tests, linting, type checking)
```

---

## Quick Start

**Command:** `/commands`

**Common follow-ups:**
- "What does [command-name] do?"
- "Show me git workflow commands"
- "Which commands are for quality checks?"

---

## Commands Catalog

### Boris Workflow Commands (7)

**`/new-project`** - Bootstrap new project with best practices
- Creates CLAUDE.md, quality gates, git hooks
- Usage: `/new-project --type python`

**`/verify-app`** - Full quality check before commit
- Runs tests, linting, type checking
- Auto-detects project type

**`/test-and-fix`** - Auto-fix failing tests
- Test → fix → re-test cycle
- Repeats until passing

**`/review-changes`** - Pre-commit code review
- Reviews uncommitted changes
- Finds bugs, security issues

**`/quick-commit`** - Smart commit workflow
- Verify → stage → commit → push
- Enforces quality gates

**`/commit-push-pr`** - Full git workflow
- Everything quick-commit does + creates PR
- Automated PR description

**`/add-rule`** - Capture mistakes in CLAUDE.md
- Documents lessons learned
- Prevents recurrence

---

### Custom Project Commands (16)

#### KIE Framework (8)
- `/startkie` - Bootstrap new KIE project
- `/build` - Build KIE project
- `/validate` - Validate KIE structure
- `/spec` - Work with specifications
- `/status` - Check project status
- `/doctor` - Diagnose issues
- `/go` - Run KIE project
- `/rails` - Rails-specific operations

#### Analysis & Workflows (8)
- `/analyze` - Analysis workflows
- `/eda` - Exploratory data analysis
- `/intent` - Intent analysis
- `/sampledata` - Generate sample data
- `/preview` - Preview outputs
- `/theme` - Apply theming
- `/interview` - Interview workflows
- `/map` - Mapping operations

---

## Commands vs Skills

**Commands** = Project workflow and setup
- `/new-project`, `/verify-app`, `/quick-commit`
- Project-level operations
- Git workflow and quality gates

**Skills** = Individual capabilities (use `/skills`)
- `/eda`, `/hypothesis-tree`, `/pptx`
- Task-specific operations
- Reusable across any project

---

## Recommended Command Workflows

### Starting New Project
```
1. /new-project --type python
2. [Write code...]
3. /verify-app
4. /quick-commit
```

### KIE Project
```
1. /startkie
2. /build
3. /validate
4. /status
5. /doctor (if issues)
```

### Git Workflow
```
1. /review-changes (optional)
2. /verify-app
3. /quick-commit (or /commit-push-pr for PR)
```

---

## Technical Details

**Boris Commands Location:** `~/.claude/defaults/commands/`
**Custom Commands Location:** `~/.claude/commands/`

**Command Resolution Order:**
1. Project-specific `.claude/commands/` (if exists)
2. Global `~/.claude/commands/` (your 16 custom)
3. Global `~/.claude/defaults/commands/` (Boris 7)

---

## Related Skills

- `/skills` - List all 35 skills
- `/create-skill` - Create new custom skills
- `/setup-workflow` - Configure AI workflow

---

## Version

**Version:** 1.0
**Last Updated:** 2026-02-09
**Status:** Active
