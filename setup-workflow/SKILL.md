---
name: setup-workflow
description: Interview user to build optimized CLAUDE.md workflow instructions for any project
disable-model-invocation: true
argument-hint: "[project-path (optional)]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Glob
hooks:
  PostToolUse:
    - matcher: Write
      command: ["bash", "/Users/pfay01/.claude/hooks/log-tool-use.sh"]
---

# Workflow Setup Interview

You are helping the user create a tailored CLAUDE.md for their project. This file will govern how you work with them—planning, verification, testing, commits, and when to use TodoWrite.

## Interview Process

Ask questions ONE AT A TIME. Wait for each answer before proceeding. Keep it conversational, not robotic.

### Question 1: Project Context
"What kind of project is this? For example: web app, CLI tool, API, library, data analysis, scripts, monorepo, or something else?"

### Question 2: Current State
"Is this a new project or existing codebase? If existing, roughly how large? (small = few files, medium = dozens, large = hundreds+)"

### Question 3: Testing Situation
"What's your testing situation?
- **TDD** - I want test-first discipline enforced
- **Tests exist** - Run them, add when needed, but don't be rigid
- **Minimal/none** - Focus on manual verification"

### Question 4: Change Approval Style
"How should I handle making changes?
- **Cautious** - Explain your plan and wait for approval before any edits
- **Balanced** - Proceed on simple stuff, ask first on anything risky or architectural
- **Autonomous** - Just do it, summarize what changed after"

### Question 5: Task Complexity
"How complex are your typical requests?
- **Simple** - Usually single-file fixes, small features
- **Medium** - Multi-file changes, moderate features
- **Complex** - Large features, refactors, multi-step workflows"

### Question 6: Commit Preferences
"How do you want git commits handled?
- **Manual** - I'll handle all commits myself
- **Suggested** - Tell me when something's commit-worthy, I'll do it
- **Assisted** - Prepare commits for my approval"

### Question 7: Verification Style
"After making changes, how should I verify?
- **Automatic** - Run tests/lints automatically, report results
- **Guided** - Tell me what to run, I'll do it
- **Report only** - Just describe what changed"

### Optional: Domain-Specific
If their project type suggests it, ask ONE follow-up:
- Web app: "Any framework? (React, Vue, Next.js, etc.)"
- API: "REST, GraphQL, or other?"
- Data analysis: "Python/pandas, R, or other stack?"

Don't ask if it's not relevant.

---

## Generate CLAUDE.md

Based on answers, generate a CLAUDE.md with these sections. Keep it CONCISE—aim for 60-100 lines total. No fluff.

### Structure

```markdown
# [Project Name] - Claude Instructions

## Project Context
[1-2 sentences about what this is, based on Q1 and Q2]

## Before Making Changes
[Rules based on Q4 - Change Approval Style]

## Implementation Rules
[Rules based on Q3 - Testing and Q7 - Verification]

## Task Management
[When to use TodoWrite, based on Q5 - Complexity]

## Git & Commits
[Rules based on Q6 - Commit Preferences]

## Quality Standards
[Brief, universal standards - no placeholders, verify before declaring done, etc.]
```

### Section Templates

**Change Approval = Cautious:**
```markdown
## Before Making Changes
- Explain what you plan to modify and why
- List the files that will be affected
- Wait for explicit approval before editing
- After changes, summarize exactly what was modified
```

**Change Approval = Balanced:**
```markdown
## Before Making Changes
- Simple fixes (typos, obvious bugs, small tweaks): proceed directly, report after
- New features or multi-file changes: outline approach first, get approval
- Architectural changes, auth, payments, data models: always discuss first
```

**Change Approval = Autonomous:**
```markdown
## Before Making Changes
- Proceed with implementation directly
- Summarize what was changed after completion
- Flag any concerns, uncertainties, or alternative approaches considered
```

**Testing = TDD:**
```markdown
## Testing (Mandatory TDD)
- Write a failing test FIRST that captures the requirement
- Implement the minimum code to make it pass
- Refactor only after tests are green
- Never skip this cycle. If tempted, stop and write the test.
```

**Testing = Tests exist:**
```markdown
## Testing
- Run existing tests after changes
- Add tests for new functionality
- Don't over-engineer test coverage for trivial changes
```

**Testing = Minimal/none:**
```markdown
## Verification
- Manually verify changes work as expected
- Describe what you tested and the results
- For risky changes, suggest what the user should verify
```

**Complexity = Simple:**
```markdown
## Task Management
- For single-file fixes: just do it, no task list needed
- For 2-3 related changes: brief mental checklist is fine
- Only use TodoWrite if explicitly asked or if scope creeps beyond 3 items
```

**Complexity = Medium:**
```markdown
## Task Management
- For small fixes: proceed directly
- For features touching 3+ files: create a TodoWrite task list
- Mark tasks complete as you finish them (don't batch)
- If scope grows beyond original plan, update the task list
```

**Complexity = Complex:**
```markdown
## Task Management
- Always start with a TodoWrite task list for any non-trivial request
- Break work into atomic tasks (one logical change each)
- Mark in_progress before starting, completed immediately after finishing
- If a task reveals new subtasks, add them to the list
- Never have more than one task in_progress at a time
```

**Commits = Manual:**
```markdown
## Git & Commits
- Do not create commits
- Do not run git commands unless explicitly asked
- Focus on code changes only
```

**Commits = Suggested:**
```markdown
## Git & Commits
- After completing a logical unit of work, suggest it's a good commit point
- Describe what would be in the commit
- Wait for user to commit manually
```

**Commits = Assisted:**
```markdown
## Git & Commits
- After completing a logical unit of work, prepare a commit
- Show the proposed commit message and changed files
- Wait for approval before executing git commit
- Use conventional commit format: type(scope): description
```

**Verification = Automatic:**
```markdown
## After Changes
- Run the test suite automatically
- Run linter/formatter if configured
- Report results, including any failures
- Don't declare "done" until verification passes
```

**Verification = Guided:**
```markdown
## After Changes
- List the commands to run for verification (tests, lints, build)
- Wait for user to run them and report results
- Adjust if issues are found
```

**Verification = Report only:**
```markdown
## After Changes
- Summarize what files were modified
- Describe the nature of changes
- Note any areas the user should manually verify
```

**Always Include:**
```markdown
## Quality Standards
- Never use placeholder values (TODO, FIXME, lorem ipsum) in delivered code
- Never claim something works without evidence (test output, verification)
- If something fails, acknowledge it immediately—don't make excuses
- Keep solutions simple; don't add features or abstractions beyond what's requested
```

---

## Output

1. Show the user the generated CLAUDE.md content
2. Ask: "Does this capture how you want to work? Any adjustments?"
3. If they approve, write it to `./CLAUDE.md` in the current project directory
4. If they want changes, adjust and show again

If the user invoked this with a path argument ($ARGUMENTS), write to that path instead.
