# Installation Guide

Get Preston's consolidated skills library running on your machine in under 5 minutes.

---

## Prerequisites

- **Claude Code** or **Claude Desktop** installed
- **Git** installed (`git --version`)
- **GitHub account** with SSH or HTTPS access configured

---

## Quick Install (Recommended)

### Option 1: Clone from Personal Account (preston-fay)

```bash
# Remove existing skills directory if present
rm -rf ~/.claude/skills

# Clone the repository
git clone https://github.com/preston-fay/claude-skills.git ~/.claude/skills

# Verify installation
cd ~/.claude/skills
ls -la | wc -l  # Should show 40+ items (37 skills + dotfiles)
```

### Option 2: Clone from Work Account (pfay01_kearney)

```bash
# Remove existing skills directory if present
rm -rf ~/.claude/skills

# Clone the repository
git clone git@github.com:pfay01_kearney/claude-skills.git ~/.claude/skills

# Verify installation
cd ~/.claude/skills
ls -la | wc -l  # Should show 40+ items (37 skills + dotfiles)
```

---

## Verify Installation

### 1. Check Directory Structure

```bash
cd ~/.claude/skills
ls -1d */ | head -10
```

**Expected output:**
```
analyze/
bayesian-causal-discovery/
bootstrap/
canvas-design/
commands/
create-skill/
data-request/
deck-builder/
docx/
eda/
...
```

### 2. Test Skills in Claude Code

Open Claude Code and run:
```
/skills
```

**Expected:** You should see a catalog of all 37 skills with descriptions.

### 3. Test a Specific Skill

```
/eda
```

**Expected:** The EDA (Exploratory Data Analysis) skill should load and show usage instructions.

---

## Dual-Remote Setup (Advanced)

If you want to push changes to BOTH GitHub accounts:

### 1. Clone from one account:
```bash
git clone https://github.com/preston-fay/claude-skills.git ~/.claude/skills
cd ~/.claude/skills
```

### 2. Add the second remote:
```bash
git remote add work git@github.com:pfay01_kearney/claude-skills.git
```

### 3. Verify both remotes:
```bash
git remote -v
```

**Expected output:**
```
origin    https://github.com/preston-fay/claude-skills.git (fetch)
origin    https://github.com/preston-fay/claude-skills.git (push)
work      git@github.com:pfay01_kearney/claude-skills.git (fetch)
work      git@github.com:pfay01_kearney/claude-skills.git (push)
```

### 4. Push to both when making changes:
```bash
git push origin main
git push work main
```

---

## Sync to Claude.ai (Web Interface)

### Method 1: GitHub Import (Recommended)

1. Go to https://claude.ai
2. Click Settings → Skills/Extensions
3. Import from GitHub: `https://github.com/preston-fay/claude-skills`
4. Wait for import to complete
5. Verify with `/skills` command in a conversation

### Method 2: Manual Upload (if GitHub import unavailable)

1. Download the repository as ZIP from GitHub
2. Extract to `~/.claude/skills`
3. Follow verification steps above

---

## Sync to Claude Desktop

Claude Desktop should automatically detect skills in `~/.claude/skills/`.

**Verify:**
1. Open Claude Desktop
2. Start a new conversation
3. Type `/skills`
4. You should see all 37 skills listed

**Troubleshooting:** If skills don't appear:
1. Restart Claude Desktop
2. Check that skills are in `~/.claude/skills/` (not a subdirectory)
3. Verify each skill has a `SKILL.md` file

---

## Updating Skills

### Pull Latest Changes

```bash
cd ~/.claude/skills
git pull origin main  # Or: git pull work main
```

### Sync Updates to Claude.ai

If you've set up GitHub import, claude.ai may auto-sync. If not:
1. Go to Settings → Skills
2. Re-import from GitHub
3. Wait for completion
4. Verify with `/skills`

---

## Troubleshooting

### Problem: "Skills directory not found"

**Solution:**
```bash
# Check if skills directory exists
ls -la ~/.claude/skills

# If not, clone again
git clone https://github.com/preston-fay/claude-skills.git ~/.claude/skills
```

### Problem: "Skills not showing in Claude Code"

**Causes:**
1. Skills not in correct directory
2. Missing SKILL.md files
3. Claude Code needs restart

**Solutions:**
```bash
# Verify location
cd ~/.claude/skills && pwd
# Should output: /Users/[your-username]/.claude/skills

# Check for SKILL.md files
find ~/.claude/skills -name "SKILL.md" | wc -l
# Should output: 37

# Restart Claude Code
# Quit and reopen the application
```

### Problem: "Git clone failed - permission denied"

**Cause:** SSH keys not configured or HTTPS credentials missing

**Solutions:**

**For SSH (recommended):**
```bash
# Generate SSH key if you don't have one
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub
# Add this to GitHub → Settings → SSH Keys
```

**For HTTPS:**
```bash
# Use HTTPS URL instead
git clone https://github.com/preston-fay/claude-skills.git ~/.claude/skills

# GitHub will prompt for username and Personal Access Token
# Create PAT at: GitHub → Settings → Developer Settings → Personal Access Tokens
```

### Problem: "/skills command not working"

**Solution:**
```bash
# Check if skills meta-skill exists
ls -la ~/.claude/skills/skills/

# Verify SKILL.md
cat ~/.claude/skills/skills/SKILL.md | head -10

# Restart Claude Code/Desktop
```

### Problem: "Merge conflicts when pulling updates"

**Solution:**
```bash
cd ~/.claude/skills

# See which files have conflicts
git status

# Option 1: Keep remote version (discard local changes)
git reset --hard origin/main

# Option 2: Keep local changes (stash and reapply)
git stash
git pull origin main
git stash pop
# Resolve conflicts manually if any
```

---

## Uninstall

To completely remove the skills library:

```bash
# Remove local directory
rm -rf ~/.claude/skills

# Verify removal
ls ~/.claude/
# Should NOT show 'skills' directory
```

**Note:** This only removes the local copy. GitHub repositories remain intact.

---

## File Locations Reference

| Item | Location | Purpose |
|------|----------|---------|
| Skills library | `~/.claude/skills/` | All 37 skill directories |
| Individual skill | `~/.claude/skills/<skill-name>/` | Single skill directory |
| Skill definition | `~/.claude/skills/<skill-name>/SKILL.md` | Skill instructions |
| Supporting files | `~/.claude/skills/<skill-name>/*` | Scripts, templates, data |
| Git repository | `~/.claude/skills/.git/` | Version control |
| Index | `~/.claude/skills/SKILLS_INDEX.md` | Catalog of all skills |
| Sync guide | `~/.claude/skills/SYNC_WORKFLOW.md` | How to keep skills synced |

---

## Next Steps

After installation:

1. ✅ **Read the skills catalog:**
   ```
   /skills
   ```

2. ✅ **Try a skill:**
   ```
   /hypothesis-tree Should we expand into European markets?
   ```

3. ✅ **Read sync workflow:**
   ```bash
   cat ~/.claude/skills/SYNC_WORKFLOW.md
   ```

4. ✅ **Browse skill documentation:**
   ```bash
   ls ~/.claude/skills/
   # Pick a skill directory
   cat ~/.claude/skills/eda/SKILL.md
   ```

5. ✅ **Set up dual-remote sync** (optional, see "Dual-Remote Setup" above)

---

## Getting Help

### Documentation

- **Sync workflow:** `SYNC_WORKFLOW.md`
- **Quality audit:** `QUALITY_AUDIT.md`
- **Skills index:** `SKILLS_INDEX.md`
- **Legacy reference:** `MY_SKILLS.md`

### Commands

```bash
# List all skills
ls -1 ~/.claude/skills/

# Count skills
ls -1d ~/.claude/skills/*/ | wc -l

# Search for a skill by keyword
ls ~/.claude/skills/ | grep -i "data"

# Read a skill's documentation
cat ~/.claude/skills/<skill-name>/SKILL.md

# Check git status
cd ~/.claude/skills && git status

# Pull latest updates
cd ~/.claude/skills && git pull origin main
```

---

## Architecture

```
~/.claude/skills/              # Skills library root
├── .git/                      # Git repository
├── .gitignore                 # Ignored files
├── README.md                  # Project overview
├── INSTALLATION.md            # This file
├── SYNC_WORKFLOW.md           # How to sync changes
├── QUALITY_AUDIT.md           # Skills quality assessment
├── SKILLS_INDEX.md            # Complete catalog
├── MY_SKILLS.md               # Legacy reference (backup)
├── skills-index.yaml          # Machine-readable catalog
├── analyze/                   # Skill: Insight analysis
│   └── SKILL.md
├── bayesian-causal-discovery/ # Skill: Causal discovery
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   └── scripts/
├── bootstrap/                 # Skill: Project templates
│   └── SKILL.md
├── ... (34 more skills)
└── write-as-preston/          # Skill: Personal writing voice
    └── SKILL.md
```

---

*Installation guide last updated: 2026-02-11*
*Total skills: 37*
*Supported platforms: macOS, Linux*
