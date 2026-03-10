---
description: "Run tests and fix failures iteratively until all pass"
---

# /test-and-fix - Test Loop with Auto-Fix

Runs tests, analyzes failures, fixes them one at a time, and re-runs until all pass. This is the core TDD workflow command.

## Live project state (pre-loaded)
- Test framework: !`([ -f pytest.ini ] || [ -f pyproject.toml ] && grep -q pytest pyproject.toml) && echo "pytest" || ([ -f package.json ] && grep -q '"test"' package.json && echo "npm test") || echo "unknown"`
- Recent changes: !`git diff --name-only HEAD~1 2>/dev/null | head -10 || git status --short 2>/dev/null | head -10`
- Branch:         !`git branch --show-current 2>/dev/null`

## Process

### 1. Run Test Suite

Detect and run appropriate test command:
- Python: `pytest`
- Node: `npm test`
- KIE: `python3 -m pytest tests/`

### 2. Analyze Results

If all tests pass:
```
✅ All tests passing!
Total: X tests
Duration: Y seconds
```

If tests fail:
```
❌ X tests failed

Failed tests:
1. test_user_login (tests/test_auth.py:42)
   AssertionError: Expected 200, got 404

2. test_create_post (tests/test_posts.py:15)
   AttributeError: 'NoneType' object has no attribute 'title'

3. [more failures...]
```

### 3. Fix First Failure

**Focus on ONE test at a time:**

1. Read the test file
2. Understand what it's testing
3. Read the implementation being tested
4. Identify root cause
5. Fix the issue
6. Do NOT move to next failure yet

### 4. Re-run Tests

After fixing, immediately re-run:
```bash
pytest  # or appropriate command
```

### 5. Repeat Until All Pass

- If that test now passes → Move to next failure
- If that test still fails → Analyze why fix didn't work
- If NEW tests fail → You introduced a regression, fix it
- Keep going until 0 failures

## Example Session

```
User: /test-and-fix

Claude: Running tests...
❌ 3 tests failed

Failure 1: test_user_login
Expected 200 status code, got 404

Let me read tests/test_auth.py to understand this test...
[reads test]

The test expects POST /api/login to exist, but looking at routes.py:
[reads routes.py]

The route is registered as /login not /api/login. Fixing...
[edits routes.py to add /api/login]

Re-running tests...
✅ test_user_login now passes!

Failure 2: test_create_post
AttributeError: 'NoneType' object has no attribute 'title'

[continues until all pass]

✅ All tests passing! (3 fixes made)
```

## Guidelines

- **Be methodical**: Fix one test at a time, verify before moving on
- **Don't batch fixes**: Each fix → immediate re-run
- **Watch for regressions**: New failures mean your fix broke something else
- **Root cause, not symptoms**: Fix the underlying issue, not just the test
- **Ask if stuck**: If 3 attempts don't fix a test, ask user for clarification

## When to Use

- After implementing new feature
- After refactoring
- When CI shows test failures
- As part of TDD red-green-refactor cycle

## Integration

This command is used by:
- `/commit-push-pr` - Ensures tests pass before committing
- Post-implementation verification
- Part of the verification loop

## Notes

- Uses same test detection as `/verify-app`
- Stops at first critical error (import failures, syntax errors)
- Records fixes in context for learning
- Consider using `/add-rule` if same mistake keeps happening
