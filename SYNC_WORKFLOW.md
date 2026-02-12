# Skills Sync Workflow

This document explains how to keep your skills synchronized between:
- Local development (`~/.claude/skills`)
- GitHub repository (backup + version control)
- Personal Claude accounts (claude.ai + Claude Desktop)

---

## Architecture

```
~/.claude/skills (LOCAL MASTER)
       ↓ git push
GitHub private repo
       ↓ import URL
claude.ai + Claude Desktop
```

**Key Principle:** `~/.claude/skills` is the single source of truth. All changes happen here first, then sync outward.

---

## Quick Reference

### Push Local Changes to Both GitHub Accounts
```bash
cd ~/.claude/skills
git add .
git commit -m "Description of changes"
git push origin main     # Push to pfay01_kearney (work)
git push personal main   # Push to preston-fay (personal)
```

**Quick push to both:**
```bash
cd ~/.claude/skills
git add .
git commit -m "Description of changes"
git push --all  # Push to all remotes
```

### Pull Updates from GitHub
```bash
cd ~/.claude/skills
git pull origin main
```

### Sync to Personal Claude (claude.ai)
1. Go to claude.ai → Settings → Skills/Extensions
2. Import from GitHub: `https://github.com/pfay01_kearney/claude-skills`
3. Wait for import to complete
4. Verify: Run `/skills` command to see updated catalog

### Sync to Claude Desktop
- **Method 1 (Import):** Same as claude.ai - use GitHub import
- **Method 2 (Local):** Claude Desktop may already use `~/.claude/skills` directly

---

## Detailed Workflows

### Workflow 1: Adding a New Skill

**1. Create the skill locally:**
```bash
cd ~/.claude/skills
mkdir -p new-skill-name
cd new-skill-name
```

**2. Create SKILL.md:**
```markdown
---
name: new-skill-name
description: Brief description of what this skill does
---

# Skill Name

[Your skill content here...]

## Quick Start
[Examples of how to use it...]
```

**3. Test locally:**
```bash
# In Claude Code
/new-skill-name
```

**4. Commit and push:**
```bash
cd ~/.claude/skills
git add new-skill-name/
git commit -m "Add new-skill-name: [description]"
git push origin main
```

**5. Update indexes:**
- Add entry to `SKILLS_INDEX.md`
- Add entry to `skills-index.yaml`
- Commit index updates:
```bash
git add SKILLS_INDEX.md skills-index.yaml
git commit -m "Update indexes for new-skill-name"
git push origin main
```

**6. Sync to Personal Claude:**
- Re-import on claude.ai (if needed)
- Verify with `/skills`

---

### Workflow 2: Updating an Existing Skill

**1. Make changes locally:**
```bash
cd ~/.claude/skills/skill-name
# Edit SKILL.md or supporting files
```

**2. Test changes:**
```bash
# In Claude Code
/skill-name [test arguments]
```

**3. Commit and push:**
```bash
cd ~/.claude/skills
git add skill-name/
git commit -m "Update skill-name: [what changed]"
git push origin main
```

**4. Sync to Personal Claude:**
- Re-import on claude.ai (if auto-sync not enabled)

---

### Workflow 3: Removing a Skill

**1. Archive locally (don't delete immediately):**
```bash
cd ~/.claude/skills
git mv skill-name _archived-skill-name
git commit -m "Archive skill-name: [reason]"
git push origin main
```

**2. Update indexes:**
- Remove from `SKILLS_INDEX.md`
- Remove from `skills-index.yaml`
- Commit:
```bash
git add SKILLS_INDEX.md skills-index.yaml
git commit -m "Remove skill-name from indexes"
git push origin main
```

**3. Verify locally:**
```bash
/skills  # Should not show archived skill
```

**4. After 30 days (if confirmed not needed):**
```bash
git rm -r _archived-skill-name
git commit -m "Permanently remove archived skill-name"
git push origin main
```

---

### Workflow 4: Bulk Updates (Multiple Skills)

**1. Make all changes locally:**
```bash
cd ~/.claude/skills
# Edit multiple SKILL.md files
```

**2. Review changes:**
```bash
git status
git diff
```

**3. Commit related changes together:**
```bash
git add skill1/ skill2/ skill3/
git commit -m "Update multiple skills: improve documentation

- skill1: Add more examples
- skill2: Fix typo in description
- skill3: Update dependencies"
git push origin main
```

**4. Or commit separately:**
```bash
git add skill1/
git commit -m "skill1: Add more examples"
git add skill2/
git commit -m "skill2: Fix typo"
git add skill3/
git commit -m "skill3: Update dependencies"
git push origin main
```

---

## When to Sync

### Push to GitHub (Required)
- ✅ After adding a new skill
- ✅ After modifying skill documentation
- ✅ After updating indexes
- ✅ Before switching machines
- ✅ End of work session (if changes made)

### Sync to Personal Claude (Optional, as needed)
- When you need skills on claude.ai web interface
- When setting up Claude Desktop on new machine
- After major skill additions or updates
- **Note:** May not be necessary if Claude products auto-sync from GitHub

---

## Sync Frequency Recommendations

**Daily (if actively developing skills):**
```bash
# End of day
cd ~/.claude/skills
git add .
git commit -m "Daily update: [summary]"
git push origin main
```

**Weekly (if occasional skill updates):**
```bash
# Once a week
cd ~/.claude/skills
git status  # Check for uncommitted changes
git add .
git commit -m "Weekly sync: [what changed]"
git push origin main
```

**On-demand (if rarely updating):**
- Only push when you've made changes
- Run `git status` to check for uncommitted work

---

## Health Checks

### Verify Local Skills
```bash
cd ~/.claude/skills
./.skillsrc --check  # Run health check
```

### Verify Git Status
```bash
cd ~/.claude/skills
git status  # Should show "nothing to commit, working tree clean"
git log --oneline -5  # See recent commits
```

### Verify GitHub Sync
```bash
cd ~/.claude/skills
git fetch origin
git status  # Should show "Your branch is up to date with 'origin/main'"
```

### Verify Personal Claude
- Go to claude.ai
- Run `/skills` command
- Count should match local count (37 skills as of 2026-02-11)

---

## Troubleshooting

### Problem: "Your branch is behind 'origin/main'"
**Cause:** Someone else updated the repo, or you edited on another machine

**Solution:**
```bash
cd ~/.claude/skills
git pull origin main
# Resolve any conflicts if prompted
```

### Problem: "Your branch is ahead of 'origin/main'"
**Cause:** You have local commits not pushed to GitHub

**Solution:**
```bash
cd ~/.claude/skills
git push origin main
```

### Problem: Merge conflicts
**Cause:** Same file edited in two places

**Solution:**
```bash
cd ~/.claude/skills
git status  # See conflicted files
# Edit conflicted files to resolve
git add <resolved-file>
git commit -m "Resolve merge conflict in <file>"
git push origin main
```

### Problem: Skills not showing in claude.ai
**Cause:** Import may not have completed or auto-sync disabled

**Solution:**
1. Go to claude.ai → Settings → Skills
2. Re-import from GitHub URL
3. Wait for completion message
4. Test with `/skills` command

### Problem: Accidentally deleted a skill
**Cause:** `rm -rf` or accidental deletion

**Solution:**
```bash
cd ~/.claude/skills
git checkout HEAD -- skill-name/  # Restore from last commit
# Or
git log --oneline --all -- skill-name/  # Find when it existed
git checkout <commit-hash> -- skill-name/  # Restore from that commit
```

---

## Best Practices

### Commit Messages
Use conventional commit format:
- `feat(skill-name): Add new feature`
- `fix(skill-name): Fix bug in...`
- `docs(skill-name): Update documentation`
- `refactor(skill-name): Reorganize...`
- `chore: Update .gitignore`

### Branch Strategy
**Main branch only** (simple workflow):
- All changes go directly to `main`
- Suitable for personal projects with single developer

**Optional feature branches** (if needed):
```bash
git checkout -b feature/new-skill
# Make changes
git commit -m "Add new-skill"
git push origin feature/new-skill
# Create PR on GitHub, merge to main
```

### Backup Strategy
- ✅ GitHub serves as backup (automatic)
- ✅ Local `.git` history serves as version control
- ⚠️ Consider occasional manual backups:
```bash
cd ~
tar -czf claude-skills-backup-$(date +%Y%m%d).tar.gz .claude/skills/
```

---

## Advanced: Multi-Machine Workflow

### Setup on New Machine
1. Clone the repository:
```bash
cd ~/.claude
git clone https://github.com/pfay01_kearney/claude-skills.git skills
```

2. Verify:
```bash
cd ~/.claude/skills
ls -la  # Should see all 37 skill directories
```

3. Test:
```bash
# In Claude Code
/skills  # Should show all skills
```

### Syncing Between Machines

**Machine A (work):**
```bash
cd ~/.claude/skills
# Make changes
git add .
git commit -m "Update skill-name"
git push origin main
```

**Machine B (home):**
```bash
cd ~/.claude/skills
git pull origin main  # Pull changes from Machine A
# Now you have the latest skills
```

**Best Practice:** Always `git pull` before starting work on a new machine.

---

## Quick Commands Cheat Sheet

```bash
# Status check
cd ~/.claude/skills && git status

# Pull latest
cd ~/.claude/skills && git pull origin main

# Quick commit + push
cd ~/.claude/skills && git add . && git commit -m "Quick update" && git push origin main

# View recent commits
cd ~/.claude/skills && git log --oneline -10

# Health check
cd ~/.claude/skills && ./.skillsrc --check

# Count skills
cd ~/.claude/skills && ls -1d */ | wc -l
```

---

## Repository Information

**Dual-Remote Setup:** Skills are synced to BOTH GitHub accounts for redundancy and accessibility.

- **Primary (Work):** https://github.com/pfay01_kearney/claude-skills
  - Account: pfay01_kearney
  - Remote name: `origin`
  - Protocol: SSH (`git@github.com:pfay01_kearney/claude-skills.git`)

- **Secondary (Personal):** https://github.com/preston-fay/claude-skills
  - Account: preston-fay
  - Remote name: `personal`
  - Protocol: HTTPS (`https://github.com/preston-fay/claude-skills.git`)

- **Local Path:** `~/.claude/skills`
- **Visibility:** Private (both repos)
- **Total Skills:** 37 (as of 2026-02-11)

**Why Two Repos?**
- Work account (pfay01_kearney) for Kearney-related usage
- Personal account (preston-fay) for personal Claude.ai access
- Automatic redundancy and backup
- Both stay in perfect sync

---

*Last updated: 2026-02-11*
