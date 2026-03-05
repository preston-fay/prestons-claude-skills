---
description: "Full git workflow: commit, verify, push, create PR"
---

# /commit-push-pr - Complete Git Workflow

End-to-end workflow from uncommitted changes to GitHub PR. Includes all quality gates, verification, and conventional commit format.

## Prerequisites

- Changes are made and ready to commit
- Tests are written (if new features)
- On a feature branch (not main/master)
- GitHub CLI installed (`gh`)

## Process

### 1. Check Branch

```bash
git branch --show-current
```

If on `main` or `master`:
```
⚠️  You're on main branch!
Create feature branch first:
  git checkout -b feature/your-feature-name
```

### 2. Review Changes

```bash
git status
git diff
```

### 3. Pre-Commit Review

```bash
/review-changes
```

If blockers found → Stop, fix them first

### 4. Run Full Verification

```bash
/verify-app
```

**Must pass:**
- Type checking
- Linting
- All tests
- Build (if applicable)

If fails → Stop, run `/test-and-fix`

### 5. Commit with Verification

```bash
/quick-commit
```

Generates conventional commit message, stages, and commits.

### 6. Push to Remote

Check if remote branch exists:
```bash
git rev-parse --verify origin/$(git branch --show-current) 2>/dev/null
```

If doesn't exist (first push):
```bash
git push -u origin $(git branch --show-current)
```

If exists:
```bash
git push
```

### 7. Generate PR Description

Analyze commits since branched from main:
```bash
git log main..HEAD --oneline
git diff main...HEAD
```

Generate PR description with:
- **Summary**: What changed (bullet points)
- **Why**: Motivation for changes
- **Test Plan**: How to verify it works
- **Screenshots**: If UI changes
- **Related Issues**: Links to issues

Format:
```markdown
## Summary
- Add password reset endpoint
- Email verification with time-limited tokens
- Comprehensive error handling

## Why
Users need ability to reset forgotten passwords securely.

## Test Plan
- [ ] Existing tests pass
- [ ] New tests for password reset flow
- [ ] Manual test: Request reset email
- [ ] Manual test: Use reset token
- [ ] Manual test: Expired token rejected

## Related Issues
Closes #123

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### 8. Create PR

```bash
gh pr create \
  --title "feat(auth): add password reset functionality" \
  --body "$(cat <<'EOF'
[Generated PR description above]
EOF
)"
```

### 9. Return PR URL

```
✅ Pull Request created!
📝 https://github.com/user/repo/pull/456

Next steps:
1. Review the PR description
2. Request reviewers: gh pr edit 456 --add-reviewer username
3. Monitor CI checks
4. Address review comments
```

## Example Session

```
User: /commit-push-pr

Claude:
Current branch: feature/password-reset
✅ On feature branch (not main)

Current changes:
  M src/auth.py
  A src/auth/reset.py
  M tests/test_auth.py

Running pre-commit review...
✅ No blockers found

Running verification...
⏳ Type checking... ✅
⏳ Linting... ✅
⏳ Tests (32 passed)... ✅

All checks passed! Proceeding with commit...

Proposed commit message:
─────────────────────────────
feat(auth): add password reset functionality

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
─────────────────────────────

Commit? yes

✅ Committed: abc1234

Pushing to origin/feature/password-reset...
✅ Pushed

Creating pull request...

Title: feat(auth): add password reset functionality

Description:
## Summary
- Add password reset endpoint with email verification
- Time-limited tokens for security
- Comprehensive tests for success and error cases

## Test Plan
- [x] All existing tests pass
- [x] New tests for reset flow
- [x] Manual testing completed

Closes #123

🤖 Generated with Claude Code

✅ Pull Request created!
📝 https://github.com/user/repo/pull/456
```

## Quality Gates

This command enforces:
1. ✅ Not committing directly to main
2. ✅ Pre-commit code review
3. ✅ Full verification passes
4. ✅ Conventional commit format
5. ✅ Comprehensive PR description
6. ✅ Test plan documented

## When to Use

**Use for:**
- Completing features
- Ready for code review
- All tests passing locally

**Don't use for:**
- Work in progress (use `/quick-commit` instead)
- Draft PRs (create draft manually)
- Hotfixes to main (use manual process)

## Options

```bash
/commit-push-pr                           # Full workflow
/commit-push-pr --draft                   # Create draft PR
/commit-push-pr --no-verify               # Skip verification (not recommended)
```

## Failure Handling

**If verification fails:**
```
❌ Verification failed - tests not passing

Run /test-and-fix to resolve issues, then try again.
```

**If push fails:**
```
❌ Push rejected - remote has changes

Fetch and rebase:
  git fetch origin
  git rebase origin/main
Then try /commit-push-pr again
```

**If PR creation fails:**
```
❌ gh CLI not authenticated

Authenticate:
  gh auth login
Then try again
```

## Notes

- Requires GitHub CLI: `brew install gh`
- Follows same commit conventions as `/quick-commit`
- PR description is editable after creation
- This is the recommended way to complete features
- Enforces Boris's "verification loop" at every step
