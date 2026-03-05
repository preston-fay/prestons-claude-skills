<!--
installed_from_repo: preston-fay/kie-v3
installed_at: 2026-01-18T14:37:53.092587
source_commit: 5806a3e3
-->

---
name: doctor
description: Check workspace health and detect package collisions
---

```bash
# Check for KIE workspace
if [ ! -f "project_state/spec.yaml" ] && [ ! -d "project_state" ]; then
  echo "❌ Not in a KIE workspace"
  echo "Run /startkie to bootstrap first"
  exit 1
fi

# Route to project CLI
python3 -m kie.cli doctor
```
