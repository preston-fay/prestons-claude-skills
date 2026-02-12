# Enable All 37 Skills - Simple Instructions

**Goal:** Get all your skills working in Claude Code, Claude Desktop, and claude.ai (Cowork) from your personal GitHub repository.

**Time needed:** 5 minutes

---

## Part 1: Claude Code (Local - Already Done!)

Your skills are already working in Claude Code because they're in `~/.claude/skills/`

**Test it:**
1. Open Claude Code
2. Type: `/skills`
3. You should see all 37 skills listed

✅ **Claude Code is done!**

---

## Part 2: Claude Desktop (Local)

Claude Desktop automatically uses `~/.claude/skills/`

**Test it:**
1. Open Claude Desktop app
2. Start a new conversation
3. Type: `/skills`
4. You should see all 37 skills listed

If you don't see them:
1. Quit Claude Desktop completely
2. Reopen Claude Desktop
3. Try `/skills` again

✅ **Claude Desktop is done!**

---

## Part 3: claude.ai (Web / Cowork)

This is where you need to import from your personal GitHub repo.

### Step-by-Step Instructions:

**1. Go to claude.ai**
   - Open your browser
   - Go to https://claude.ai
   - Log in with your personal account

**2. Open Settings**
   - Click your profile icon (bottom left)
   - Click "Settings"

**3. Find the Skills/Extensions Section**
   - Look for "Skills", "Extensions", or "Integrations" tab
   - (The exact name might vary - it's where you manage custom content)

**4. Import from GitHub**
   - Click "Add Skills" or "Import from GitHub" button
   - Paste this URL:
     ```
     https://github.com/preston-fay/claude-skills
     ```
   - Click "Import" or "Connect"

**5. Wait for Import**
   - This might take 30-60 seconds
   - You'll see a progress indicator
   - Wait for "Import complete" or similar message

**6. Test It**
   - Go back to your conversations (or start a new one)
   - Type: `/skills`
   - You should see all 37 skills listed!

✅ **claude.ai is done!**

---

## Verification Checklist

Run `/skills` in each environment and verify you see **37 skills**:

- [ ] ✅ Claude Code (local CLI)
- [ ] ✅ Claude Desktop (local app)
- [ ] ✅ claude.ai (web / Cowork)

---

## Troubleshooting

### Problem: "Skills not showing in claude.ai"

**Solution 1: Check Import Status**
- Go to Settings → Skills
- Look for your imported repository
- Make sure import is "Complete" (not "In Progress" or "Failed")

**Solution 2: Re-import**
- Go to Settings → Skills
- Remove the old import (if it exists)
- Import again: `https://github.com/preston-fay/claude-skills`
- Wait for completion
- Refresh the page
- Try `/skills` again

**Solution 3: Use a New Conversation**
- Sometimes skills don't load in old conversations
- Start a brand new conversation
- Try `/skills`

---

### Problem: "GitHub import not available"

If claude.ai doesn't have GitHub import yet:

**Alternative: Wait for the feature**
- GitHub import may be rolling out gradually
- Check back in a few days
- Your local Claude Code and Desktop already work!

---

### Problem: "Import failed"

**Check Repository Visibility:**
1. Go to https://github.com/preston-fay/claude-skills
2. Make sure you can see it (you're logged in with preston-fay account)
3. Make sure it's not deleted or renamed

**Check GitHub Permissions:**
- claude.ai might need permission to access your GitHub
- Authorize the Claude app if prompted

---

## What Skills You'll Have

After setup, you'll have access to:

**Strategy (5):** hypothesis-tree, issue-tree, market-sizing, value-chain, growth-matrix

**Analytics (9):** eda, analyze, bayesian-causal-discovery, map, scrape, interview, methods-guide, data-request, insight-synth

**Deliverables (5):** deck-builder, exec-summary, storytell, observable-framework, kearney-design

**Documents (4):** pptx, xlsx, pdf, docx

**Frontend (6):** frontend-design, react-best-practices, web-artifacts-builder, webapp-testing, web-design-guidelines, mcp-builder

**Creative (2):** canvas-design, remotion

**Utilities (6):** bootstrap, setup-workflow, create-skill, write-as-preston, commands, skills

**Total: 37 skills**

---

## Quick Example Uses

Once enabled, try these:

```
/skills
→ See full catalog

/hypothesis-tree Should we expand into Europe?
→ Build a testable hypothesis tree

/eda data.csv
→ Run exploratory data analysis

/deck-builder
→ Structure a presentation

/write-as-preston
→ Write content in your voice
```

---

## Keeping Skills Updated

Your local skills (`~/.claude/skills/`) are always up-to-date because you're working directly with them.

For **claude.ai**, skills update automatically when you push to GitHub:

1. Make changes locally in `~/.claude/skills/`
2. Commit and push:
   ```bash
   cd ~/.claude/skills
   git add .
   git commit -m "Update skill"
   git push personal main
   ```
3. claude.ai will auto-sync (or you can re-import manually)

---

## Summary

**Already working:**
- ✅ Claude Code (uses `~/.claude/skills/` directly)
- ✅ Claude Desktop (uses `~/.claude/skills/` directly)

**Action needed:**
- ⚠️ claude.ai (import from `https://github.com/preston-fay/claude-skills`)

**Time:** 2 minutes to import on claude.ai

---

**Questions?**

If something doesn't work, check:
1. Is the GitHub repo accessible at https://github.com/preston-fay/claude-skills ?
2. Did you wait for the import to complete?
3. Did you try `/skills` in a new conversation?
4. Did you refresh the claude.ai page?

---

*Last updated: 2026-02-11*
*Total skills: 37*
*Personal GitHub: https://github.com/preston-fay/claude-skills*
