---
description: "Run tech-stack-aware verification (typecheck, lint, tests)"
---

# /verify-app - Quality Gate Verification

Runs verification based on detected project type. This is the core quality gate that prevents "done" claims when code is actually broken.

## Detection & Execution

### Python Projects
```bash
if [ -f "requirements.txt" ]; then
  echo "🐍 Python project detected"

  # Type checking
  if command -v mypy &> /dev/null; then
    mypy . || echo "⚠️  Type errors found"
  else
    echo "⚠️  mypy not installed (pip install mypy)"
  fi

  # Linting
  if command -v ruff &> /dev/null; then
    ruff check . || echo "⚠️  Lint errors found"
  else
    echo "⚠️  ruff not installed (pip install ruff)"
  fi

  # Tests (CRITICAL - must pass)
  if command -v pytest &> /dev/null; then
    pytest || { echo "❌ Tests failed - FIX BEFORE PROCEEDING"; exit 1; }
  else
    echo "❌ pytest not installed (pip install pytest)"
    exit 1
  fi

  echo "✅ Python verification passed"
fi
```

### Flask Projects
```bash
if [ -f "requirements.txt" ] && grep -q "flask" requirements.txt; then
  echo "🌶️  Flask project detected"

  # Run Python checks first (above)
  # Then Flask-specific:

  if command -v flask &> /dev/null; then
    flask routes 2>&1 | head -10 || echo "⚠️  Flask not initialized"
  fi

  echo "✅ Flask verification passed"
fi
```

### Node Projects (Future)
```bash
if [ -f "package.json" ]; then
  echo "📦 Node project detected"

  npm run typecheck 2>/dev/null || echo "⚠️  No typecheck script"
  npm run lint 2>/dev/null || echo "⚠️  No lint script"
  npm test || { echo "❌ Tests failed"; exit 1; }
  npm run build || { echo "❌ Build failed"; exit 1; }

  echo "✅ Node verification passed"
fi
```

### KIE Projects
```bash
if [ -f "project_state/spec.yaml" ]; then
  echo "🏗️  KIE project detected"

  python3 -m pytest tests/ || { echo "❌ KIE tests failed"; exit 1; }

  echo "✅ KIE verification passed"
fi
```

### Generic/Consulting Projects
```bash
# No tech stack detected - run basic checks
echo "📄 Generic project - running basic checks"

# Check for common issues
if [ -d ".git" ]; then
  git status
  echo "✅ Git repository valid"
fi

if [ -f "README.md" ]; then
  echo "✅ README.md exists"
fi

echo "⚠️  No tech stack detected - add requirements.txt or package.json for automated verification"
```

## Failure Handling

- **Type errors**: Show first 10 errors with file locations
- **Lint errors**: Suggest auto-fix command
- **Test failures**: Show last 30 lines of output
- **Build failures**: Show error summary

## When to Run

**Always run before:**
- Committing code
- Creating PR
- Declaring feature "complete"
- Deploying

**Integrated into:**
- `/quick-commit` - Runs automatically
- `/commit-push-pr` - Runs before push
- `/test-and-fix` - Runs after each fix

## Notes

- Exit code 0 = all checks pass
- Exit code 1 = critical failure (tests/build)
- Warnings don't fail the check, only errors do
- This enforces Boris's "2-3x quality improvement through verification loops"
