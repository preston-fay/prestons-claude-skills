---
name: create-skill
description: Create a new Claude Code skill through conversation. Use when the user wants to create, build, or make a new skill, slash command, or workflow automation.
disable-model-invocation: true
argument-hint: "[skill-name (optional)]"
allowed-tools:
  - Read
  - Write
  - Glob
---

# Create Skill

Help users create effective Claude Code skills through conversation, not scaffolding.

## Philosophy

Skills are instructions that make Claude better at specific tasks. They should be:
- **Lean** - Context window is shared; every token costs
- **Focused** - One skill, one purpose
- **Practical** - Concrete examples over abstract explanations

Most personal skills need only a SKILL.md file. Scripts/references/assets are for complex, reusable skills.

## Process

### 1. Understand the Need

Ask ONE question at a time:

1. "What task do you want to automate or improve? Give me a concrete example of when you'd use this."

2. Based on their answer, ask ONE clarifying question if needed:
   - If unclear scope: "What's the trigger? When should this activate?"
   - If complex task: "Walk me through the steps you'd do manually."
   - If output-focused: "What should the result look like?"

Stop asking questions once you understand:
- What triggers the skill
- What Claude should do
- What the output looks like (if applicable)

### 2. Determine Complexity

**Simple skill** (most cases):
- Single SKILL.md file
- Text-based instructions
- No bundled resources needed

**Complex skill** (rare):
- Needs scripts for deterministic operations (PDF manipulation, data processing)
- Needs reference docs for large schemas or API docs
- Needs assets for templates or boilerplate

Default to simple. Only suggest complex if user describes:
- Repetitive code that should be a script
- Large reference material (>500 lines)
- Template files to copy

### 3. Determine 2.1 Features Needed

Ask these additional questions to determine the right 2.1 features:

**For isolation:**
"Does this skill do significant work (data processing, file generation, research) that shouldn't clutter the main conversation?"
- If YES → add `context: fork` and `agent: general-purpose`

**For tool restrictions:**
"What tools does this skill need? Should it be restricted to specific tools for safety?"
- Data/analytics skills: `Read, Glob, Grep, Bash(python *), Write`
- Document skills: `Read, Write, Glob, Bash(python *)`
- Reference skills: `Read` only
- Strategy/text skills: `Read, Write, Glob`

**For observability:**
"Should this skill log its tool usage for audit trails?"
- If skill creates files or runs code → add PostToolUse hook

### 4. Write the Skill

#### Frontmatter

```yaml
---
name: skill-name
description: What it does and WHEN to use it. Be specific about triggers.
disable-model-invocation: true  # For user-invoked only (optional)

# 2.1 Features - add based on skill type:
context: fork              # For isolated execution (data, research, generation)
agent: general-purpose     # Required when context: fork is set
allowed-tools:             # Restrict to necessary tools
  - Read
  - Write
  - Glob
  - Bash(python *)
hooks:                     # For observability
  PostToolUse:
    - matcher: Write
      command: ["bash", "/Users/pfay01/.claude/hooks/log-tool-use.sh"]
---
```

**Description is critical** - it's how Claude decides to load the skill. Include:
- What the skill does
- Specific triggers (file types, phrases, scenarios)

#### Body Patterns

**For workflows** (sequential steps):
```markdown
# Skill Name

## Process
1. First step
2. Second step
3. Final step

## Example
User: "example request"
Action: [what Claude does]
```

**For guidelines** (standards/rules):
```markdown
# Skill Name

## Rules
- Rule 1
- Rule 2

## Examples
Good: [example]
Bad: [example]
```

**For tools** (specific operations):
```markdown
# Skill Name

## When to Use
[Specific trigger conditions]

## How to Execute
[Concrete steps or script to run]

## Output Format
[What result looks like]
```

### 5. Place the Skill

Ask: "Should this skill be available everywhere, or just this project?"

| Answer | Location |
|--------|----------|
| Everywhere | `~/.claude/skills/<name>/SKILL.md` |
| This project | `.claude/skills/<name>/SKILL.md` |

### 6. Write and Verify

1. Create the skill directory and SKILL.md
2. Show the user what was created
3. Tell them how to test: "Try invoking it with `/<skill-name>` or describe a task that should trigger it."

## Anti-Patterns

**Don't:**
- Create README, CHANGELOG, or documentation files
- Add scripts unless user explicitly needs deterministic code
- Over-explain things Claude already knows
- Use placeholders like [TODO] in delivered skills
- Create deeply nested reference structures

**Do:**
- Keep SKILL.md under 200 lines for simple skills
- Use concrete examples over abstract rules
- Test by actually invoking the skill

## Quick Reference: Frontmatter Options

| Field | Purpose | Default |
|-------|---------|---------|
| `name` | Skill identifier | Directory name |
| `description` | What + when (triggers) | Required |
| `disable-model-invocation` | User-only, no auto-trigger | false |
| `user-invocable` | Hide from `/` menu (reference skills) | true |
| `allowed-tools` | Restrict available tools | All |
| `context: fork` | Run in isolated subagent | Main context |
| `agent` | Subagent type when forked | general-purpose |
| `hooks` | Lifecycle hooks for governance | None |

## 2.1 Feature Decision Guide

| Skill Type | context: fork | allowed-tools | hooks |
|------------|---------------|---------------|-------|
| Data/Analytics | YES | Read, Glob, Grep, Bash(python *), Write | YES - log all |
| Document Creation | NO | Read, Write, Glob, Bash(python *) | YES - log Write |
| Strategy/Text | NO | Read, Write, Glob | NO |
| Reference/Guidelines | NO | Read only | NO |
| Research/Exploration | YES | Read, Glob, Grep, WebSearch, WebFetch | YES - log all |
| Code Generation | Depends | Read, Write, Edit, Glob, Bash(*) | YES - log Write |

## Hook Template

Standard logging hook (use for skills that create files or run code):

```yaml
hooks:
  PostToolUse:
    - matcher: "*"           # Log all tools, or use "Write" for files only
      command: ["bash", "/Users/pfay01/.claude/hooks/log-tool-use.sh"]
```

## If User Provides a Name

If invoked with `$ARGUMENTS` (e.g., `/create-skill deploy-checker`):
- Use that as the skill name
- Still ask about purpose and triggers
- Skip asking about naming
