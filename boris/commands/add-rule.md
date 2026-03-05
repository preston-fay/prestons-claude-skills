---
description: "Capture mistake in CLAUDE.md to prevent repeating it"
---

# /add-rule - Learning Loop

When Claude makes a mistake or you notice a pattern, use this to add it to CLAUDE.md so it NEVER happens again. This is the core of Boris's "continuous learning" philosophy.

## How It Works

1. Find CLAUDE.md (project root, current dir, or parent dir)
2. Determine rule category (Prohibited, Required, Testing, Naming, etc.)
3. Add formatted rule to appropriate section
4. Rule becomes permanent project memory

## Usage

```bash
/add-rule "Don't use bare except clauses"
/add-rule "Always use f-strings instead of .format()"
/add-rule "Test both success and error cases for API endpoints"
/add-rule "Kearney charts never have gridlines"
```

## Rule Categories

### Prohibited (❌ Don't...)
Things Claude should NEVER do in this project:
```markdown
## Prohibited
- ❌ Don't use bare except clauses
- ❌ Don't commit with debug=True in Flask
- ❌ Don't add gridlines to charts (Kearney standard)
```

### Required Practices (✅ Always...)
Things Claude MUST do:
```markdown
## Required Practices
- ✅ Always write test first (TDD)
- ✅ Always use type hints on functions
- ✅ Always run /verify-app before committing
```

### Testing Standards
Test-specific rules:
```markdown
## Testing Standards
- Test both success and error cases
- Mock external APIs in tests
- One assertion per test (usually)
```

### Naming Conventions
Project-specific naming:
```markdown
## Naming Conventions
- Use snake_case for Python functions
- Prefix test files with test_
- Use descriptive variable names (no abbreviations)
```

### Code Standards
Language-specific patterns:
```markdown
## Code Standards
- Prefer pathlib over os.path
- Use f-strings over .format()
- Docstrings for all public APIs
```

## Format

Each rule should be:
1. **Clear**: No ambiguity about what's prohibited/required
2. **Specific**: "Don't use X" not "Be careful with X"
3. **Actionable**: Claude can check for compliance
4. **Contextual**: Why this rule exists (optional)

**Good Rules:**
```markdown
- ❌ Don't use print() for logging (use logging module)
- ✅ Always validate user input before database queries
- Test files must start with test_ prefix
```

**Bad Rules:**
```markdown
- Be careful with error handling (too vague)
- Try to write clean code (not actionable)
- Think about security (not specific)
```

## Example Session

```
User: Claude, you keep using bare except clauses. Stop doing that.

Claude: You're right - that's catching all exceptions including KeyboardInterrupt.
Let me add this to CLAUDE.md:

/add-rule "Don't use bare except clauses - always specify exception types"

[Finds CLAUDE.md]
[Adds to ## Prohibited section]

✅ Rule added to CLAUDE.md

I've now captured this in project memory. I won't make this mistake again in this project.
```

## When to Use

**After mistakes:**
- Claude makes same error twice
- User corrects Claude's code
- Review catches repeated pattern

**Proactively:**
- Project-specific conventions
- Team standards
- Client requirements (like Kearney brand rules)

## Integration

Rules in CLAUDE.md are read on every Claude Code session start, so:
- New sessions won't repeat old mistakes
- Other developers using Claude Code see same rules
- Project accumulates institutional knowledge

## Notes

- Rules compound over time (Month 1: 5 rules, Month 3: 20 rules)
- More rules = fewer mistakes = higher quality
- This is "machine learning through documentation"
- Review CLAUDE.md monthly to consolidate similar rules
