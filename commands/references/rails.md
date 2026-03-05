<!--
installed_from_repo: preston-fay/kie-v3
installed_at: 2026-01-18T14:37:53.092158
source_commit: 5806a3e3
-->

---
name: rails
description: Show Rails workflow progress and suggest next command
---

```bash
# Check for KIE workspace
if [ ! -f "project_state/spec.yaml" ] && [ ! -d "project_state" ]; then
  echo "❌ Not in a KIE workspace"
  echo "Run /startkie to bootstrap first"
  exit 1
fi
```

You are in a KIE workspace with Rails workflow tracking.

**IMPORTANT:** This command shows status only. DO NOT auto-run the suggested next command.

Run these commands and report the output:

```bash
python3 -m kie.cli status
```

After showing the status output, STOP.
