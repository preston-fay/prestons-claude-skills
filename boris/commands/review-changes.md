---
description: "Pre-commit code review for bugs, security, and conventions"
---

# /review-changes - Pre-Commit Review

Analyzes uncommitted changes before commit to catch bugs, security issues, convention violations, and quality problems. This is your safety net before code enters git history.

## Live git state (pre-loaded)
- Branch:          !`git branch --show-current 2>/dev/null`
- Status:          !`git status --short 2>/dev/null`
- Unstaged diff:   !`git diff --stat 2>/dev/null`
- Staged diff:     !`git diff --cached --stat 2>/dev/null`
- Recent commits:  !`git log --oneline -5 2>/dev/null`

## Process

### 1. Check Git Status

```bash
git status
```

Show:
- Modified files
- Untracked files
- Staged vs unstaged
- Current branch

### 2. Get Full Diff

```bash
git diff        # Unstaged changes
git diff --cached   # Staged changes
```

### 3. Analyze Each Modified File

For each file, check:

#### **Correctness**
- Is the logic correct?
- Are there edge cases not handled?
- Off-by-one errors?
- Null/None handling?

#### **Bugs**
- Potential runtime errors?
- Type mismatches?
- Unhandled exceptions?
- Race conditions?
- Resource leaks?

#### **Security**
- SQL injection vulnerabilities?
- XSS vulnerabilities?
- Command injection?
- Exposed secrets or credentials?
- Insecure randomness?
- Missing input validation?

#### **Conventions**
- Follows project CLAUDE.md rules?
- Consistent naming with codebase?
- Proper error handling pattern?
- Comments where needed?

#### **Code Quality**
- Unnecessary complexity?
- Duplicate code?
- Magic numbers?
- Too long functions?
- Missing type hints (Python)?

### 4. Generate Report

```markdown
## Code Review Summary

### ✅ Good Changes
- Added proper error handling in auth.py:145
- Tests cover both success and error cases
- Clear variable names throughout

### ⚠️  Concerns

**auth.py:67** - Potential SQL Injection
```python
query = f"SELECT * FROM users WHERE id = {user_id}"  # UNSAFE
```
Should use parameterized query:
```python
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

**config.py:12** - Hardcoded Secret
```python
SECRET_KEY = "abc123"  # Don't commit this
```
Should use environment variable:
```python
SECRET_KEY = os.environ.get("SECRET_KEY")
```

**utils.py:89** - Bare Except Clause
Violates CLAUDE.md rule: "Don't use bare except clauses"
```python
except:  # Too broad
```
Should catch specific exception.

### 🔴 Blockers (Must Fix Before Commit)
1. SQL injection vulnerability (auth.py:67)
2. Hardcoded secret (config.py:12)

### 💡 Recommendations
- Consider extracting duplicate validation logic into helper function
- Add docstring to new `process_data()` function
- Test file `test_auth.py` could use more edge cases

## Next Steps
1. Fix blocker issues
2. Address concerns
3. Run /verify-app to ensure tests pass
4. Re-run /review-changes to verify fixes
5. Proceed with commit
```

### 5. Decision

**If blockers found:**
```
❌ Not ready to commit - fix blockers first
```

**If only concerns/recommendations:**
```
⚠️  Ready to commit, but consider addressing concerns
```

**If clean:**
```
✅ Looks good - ready to commit!
```

## Example Usage

```bash
User: /review-changes

Claude:
Let me check what's changed...
[runs git status and git diff]

Analyzing 3 modified files:
1. auth.py (45 lines changed)
2. tests/test_auth.py (12 lines added)
3. config.py (3 lines changed)

[Generates report above]

Found 2 blockers - shall I fix them before we commit?
```

## When to Use

**Always before:**
- Running /quick-commit
- Running /commit-push-pr
- Manual git commit

**Especially when:**
- Touching security-sensitive code
- Large refactoring
- Working in unfamiliar part of codebase
- Been working for hours (fresh eyes needed)

## Integration

- `/quick-commit` should call this first
- `/commit-push-pr` includes this step
- Can be called standalone anytime

## Notes

- Reviews follow project-specific CLAUDE.md rules
- Security checks prioritize OWASP Top 10
- Doesn't replace human code review, supplements it
- False positives possible - use judgment
- Updates project CLAUDE.md if new patterns found
