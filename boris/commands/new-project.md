---
description: "Bootstrap new project with Boris Cherny's best practices defaults"
---

# /new-project - Setup Project with Quality Gates

This command creates `.claude/` configuration with Boris Cherny's best practices built-in: verification loops, CLAUDE.md learning system, quality gates, and tech-stack-aware tooling.

## Steps

### 1. Detect Project Type

Check for:
- `requirements.txt` + "flask" → **Flask**
- `requirements.txt` → **Python**
- `package.json` → **Node** (future)
- `project_state/spec.yaml` → **KIE**
- `.env` with "KIE" or "KEARNEY" → **Consulting**
- Default → **Generic**

User can override with `--type <python|flask|node|consulting>`

### 2. Create `.claude/` Directory Structure

```bash
mkdir -p .claude
```

### 3. Create Symlinks to Global Defaults

```bash
ln -s ~/.claude/defaults/commands .claude/commands
ln -s ~/.claude/defaults/agents .claude/agents
```

This makes all Boris commands (`/verify-app`, `/test-and-fix`, `/quick-commit`, etc.) available in this project.

### 4. Copy Appropriate CLAUDE.md Template

Based on detected project type:
- Flask → `flask-CLAUDE.md.template`
- Python → `python-CLAUDE.md.template`
- Consulting → `consulting-CLAUDE.md.template`
- Generic → `CLAUDE.md.template`

```bash
cp ~/.claude/defaults/templates/<TYPE>-CLAUDE.md.template ./CLAUDE.md
```

Replace template variables:
- `{{DATE}}` → Current date
- `{{PROJECT_TYPE}}` → Detected type
- `{{PROJECT_NAME}}` → Directory name

### 5. Setup Permissions

Copy recommended permissions for detected stack:
```bash
cp ~/.claude/defaults/permissions/recommended-<TYPE>.json .claude/settings.local.json
```

Permission tiers:
- `--permissions minimal` → Read-only
- `--permissions recommended` → Default (safe but convenient)
- `--permissions full` → Full access (trusted projects only)

### 6. Create Hooks Config (if formatters detected)

If `black`, `ruff`, `prettier`, or `eslint` found in project:
```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "<formatter> \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
        }
      ]
    }
  ]
}
```

Save to `.claude/hooks.json`

### 7. Report Success

```
✅ Project bootstrapped with Boris defaults!

📁 Structure created:
  .claude/commands/    → ~/.claude/defaults/commands/
  .claude/agents/      → ~/.claude/defaults/agents/
  .claude/settings.local.json
  .claude/hooks.json (if formatters detected)
  CLAUDE.md (from <TYPE> template)

🛠️  Available commands:
  /verify-app         - Run full quality gates
  /test-and-fix       - Test loop with auto-fix
  /review-changes     - Pre-commit review
  /quick-commit       - Fast commit with verification
  /commit-push-pr     - Full git workflow
  /add-rule           - Capture mistake in CLAUDE.md

📋 Next steps:
  1. Review CLAUDE.md and customize for this project
  2. Run /verify-app to validate initial state
  3. Start building with quality gates enabled!
```

## Example Usage

```bash
/new-project                          # Auto-detect
/new-project --type flask             # Force Flask
/new-project --permissions full       # Full access
/new-project --type consulting        # Kearney deliverable
```

## Notes

- Existing `.claude/` directories are backed up to `.claude.backup.<timestamp>`
- Symlinks can be replaced with actual files to override specific commands/agents
- This is additive - your 30 skills and 16 global commands still work
- Only affects THIS project, not global config
