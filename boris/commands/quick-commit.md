---
description: "Fast commit with verification and conventional format"
---

# /quick-commit - Verified Commit Workflow

Stages changes, runs verification, and commits with conventional commit format. This is the everyday commit command with quality gates built-in.

## Process

### 1. Review Current State

```bash
git status
```

Show what will be committed.

### 2. Show Diff

```bash
git diff
```

Let user see exactly what's changing before staging.

### 3. Stage All Changes

```bash
git add -A
```

Stages:
- Modified files
- New files
- Deleted files

### 4. Run Verification (Optional but Recommended)

Ask user: "Run /verify-app before committing? (recommended)"

If yes:
```bash
/verify-app
```

If verification fails → Stop, don't commit

### 5. Analyze Changes for Commit Message

Read the diff and determine:
- What changed? (feat, fix, refactor, docs, test, chore)
- What's the scope? (auth, api, ui, config, etc.)
- Brief description (imperative mood)

### 6. Generate Conventional Commit Message

Format:
```
<type>(<scope>): <description>

[optional body]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code restructuring (no behavior change)
- `docs:` - Documentation only
- `test:` - Test additions/changes
- `chore:` - Maintenance (deps, config, etc.)
- `style:` - Formatting, whitespace
- `perf:` - Performance improvement

**Scope examples:**
- `feat(auth): add password reset functionality`
- `fix(api): handle null response in user endpoint`
- `refactor(utils): extract validation logic to helper`
- `docs(readme): add installation instructions`
- `test(auth): add edge cases for login flow`

### 7. Show Proposed Commit Message

```
Proposed commit message:
─────────────────────────────
feat(auth): add password reset functionality

- Add /api/auth/reset-password endpoint
- Email verification with token
- Tests cover success and error cases

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
─────────────────────────────

Proceed with commit? (yes/no)
```

### 8. Commit

If approved:
```bash
git commit -m "$(cat <<'EOF'
feat(auth): add password reset functionality

- Add /api/auth/reset-password endpoint
- Email verification with token
- Tests cover success and error cases

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### 9. Confirm Success

```bash
git log -1 --oneline
```

Show the commit that was just created.

```
✅ Committed: feat(auth): add password reset functionality
   SHA: abc1234
```

## Example Session

```
User: /quick-commit

Claude:
Current changes:
  M auth.py
  M tests/test_auth.py
  A config/email.py

Showing diff...
[shows git diff]

Run /verify-app before committing? (recommended)

User: yes

Claude:
Running verification...
✅ All tests pass
✅ Type checking clean
✅ Lint clean

Analyzing changes for commit message...

Proposed commit message:
─────────────────────────────
feat(auth): add password reset endpoint

Implements password reset via email with time-limited tokens.
Includes validation and comprehensive tests.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
─────────────────────────────

Proceed? (yes/no)

User: yes

Claude:
✅ Committed: feat(auth): add password reset endpoint
   SHA: 7f3a9b2
```

## Guidelines

### Commit Message Quality
- **Start with type**: Always use conventional format
- **Be specific**: "fix user login" not "fix bug"
- **Imperative mood**: "add feature" not "added feature"
- **50 char limit on title**: Keep it scannable
- **Body if needed**: Explain why, not what (diff shows what)

### When to Skip Verification
- Documentation-only changes
- Trivial changes (typos, comments)
- When verification already run recently
- But default should be YES, skip verification intentionally

### Staging Strategy
- This command stages ALL changes
- For partial commits, use manual `git add <files>` first
- Then `/quick-commit` will commit only staged files

## When to Use

**Use for:**
- Everyday commits
- After completing a logical unit of work
- When you want verification + commit in one step

**Don't use for:**
- Partial commits (stage manually first)
- When you need custom commit message (use git commit directly)
- When creating PR (use `/commit-push-pr` instead)

## Integration

- Can be chained: `/test-and-fix && /quick-commit`
- Used within `/commit-push-pr` workflow
- Respects project CLAUDE.md commit conventions

## Notes

- Always includes Co-Authored-By attribution
- Follows conventional commits spec
- Enables semantic versioning
- Makes git history readable
- Supports automated changelog generation
