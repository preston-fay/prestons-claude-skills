<!--
installed_from_repo: preston-fay/kie-v3
installed_at: 2026-01-18T14:37:53.092976
source_commit: 5806a3e3
-->

---
name: sampledata
description: Manage sample/demo data - status, install, remove
---

```bash
# Check for KIE workspace
if [ ! -f "project_state/spec.yaml" ] && [ ! -d "project_state" ]; then
  echo "❌ Not in a KIE workspace"
  echo "Run /startkie to bootstrap first"
  exit 1
fi

# Parse subcommand (default: status)
SUBCOMMAND="${1:-status}"

# Route to project CLI
python3 -m kie.cli sampledata "$SUBCOMMAND"
```
