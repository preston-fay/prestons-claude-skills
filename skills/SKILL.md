# Skills - List All Available Skills

Quick reference to display all available skills in your library.

---

## Purpose

Display the complete skills catalog (`SKILLS_INDEX.md`) so you can quickly browse what's available and see command names and examples.

---

## When to Use

- You can't remember what skills are available
- You need to find a skill for a specific task
- You want to see command names and examples
- You're exploring available capabilities

**Triggers:** "show my skills", "list skills", "what skills do I have", "skills catalog"

---

## Usage

### Basic Invocation
```
/skills
```

This displays the complete `SKILLS_INDEX.md` with all 34 skills organized by category.

### Search for Specific Skills
After invoking `/skills`, you can ask follow-up questions:
```
/skills
[then follow up with:]
Show me just the data analysis skills
Which skills help with presentations?
Find skills related to strategy
```

---

## What You Get

The complete skills catalog showing:
- **9 categories** of skills
- **Command names** for each skill (e.g., `/eda`, `/hypothesis-tree`)
- **When to use** each skill
- **Example invocations**
- **Recommended workflows**
- **Health status**

---

## Output Format

The skill reads and displays:
- `~/.claude/skills/SKILLS_INDEX.md` (360 lines, organized by category)

**Categories shown:**
1. Problem Solving & Strategy (5 skills)
2. Client Deliverables (5 skills)
3. Data & Analytics (2 skills)
4. Data Acquisition (2 skills)
5. Visualization & Storytelling (3 skills)
6. Documents (4 skills)
7. Design (2 skills)
8. Frontend Development (6 skills)
9. Utilities & Development (5 skills)

---

## Examples

### Example 1: Show All Skills
```
User: /skills
Assistant: [Displays complete SKILLS_INDEX.md with all categories]
```

### Example 2: Find Specific Skills
```
User: /skills
Assistant: [Shows index]
User: Which ones help with data analysis?
Assistant: For data analysis, you have:
- /eda - Exploratory data analysis
- /analyze - Extract insights and recommendations
- /methods-guide - Select analytical methods
```

### Example 3: Quick Command Reference
```
User: /skills
Assistant: [Shows index]
User: What's the command for hypothesis trees?
Assistant: The command is /hypothesis-tree
Example: /hypothesis-tree Should we enter the European market?
```

---

## Quick Start

**Command:** `/skills`

**Common follow-ups:**
- "Show me just the [category] skills"
- "What does [skill-name] do?"
- "Which skill should I use for [task]?"

---

## Technical Details

**Reads:** `~/.claude/skills/SKILLS_INDEX.md`
**Format:** Markdown with categories and quick navigation
**Size:** 360 lines, 14 KB
**Update frequency:** Regenerate when new skills added

---

## Tips

1. **Browse by category** - Skills are organized into logical groups
2. **Look for "When" sections** - Shows when to use each skill
3. **Copy commands directly** - All commands shown with `/` prefix
4. **Check examples** - Every skill has invocation examples
5. **Use recommended workflows** - See skill chains for common tasks

---

## Related Skills

- `/create-skill` - Create new custom skills
- `~/.claude/skills/.skillsrc --check` - Validate skills health (run in terminal)

---

## Maintenance

This skill always reads the current `SKILLS_INDEX.md`, so it stays up to date automatically when the index is updated.

To update the index with new skills:
```bash
python3 /tmp/scan_skills.py
```

---

## Version

**Version:** 1.0
**Last Updated:** 2026-02-09
**Status:** Active
