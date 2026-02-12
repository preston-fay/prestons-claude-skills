#!/usr/bin/env python3
"""
Minimal skill initializer - creates just what you need.

Usage:
    python init.py <skill-name> [--global]

Examples:
    python init.py my-skill           # Creates in current project
    python init.py my-skill --global  # Creates in ~/.claude/skills/
"""

import sys
from pathlib import Path

SKILL_TEMPLATE = '''---
name: {name}
description: {description}
---

# {title}

{body}
'''

def init_skill(name: str, global_scope: bool, description: str = "", body: str = ""):
    """Create a minimal skill with just SKILL.md."""

    if global_scope:
        base = Path.home() / ".claude" / "skills"
    else:
        base = Path.cwd() / ".claude" / "skills"

    skill_dir = base / name

    if skill_dir.exists():
        print(f"Error: {skill_dir} already exists")
        return False

    skill_dir.mkdir(parents=True)

    title = " ".join(word.capitalize() for word in name.split("-"))

    content = SKILL_TEMPLATE.format(
        name=name,
        description=description or f"[TODO: What this does and when to use it]",
        title=title,
        body=body or "[TODO: Instructions for Claude]"
    )

    (skill_dir / "SKILL.md").write_text(content)

    print(f"Created: {skill_dir / 'SKILL.md'}")
    print(f"\nInvoke with: /{name}")
    return True

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    name = sys.argv[1]
    global_scope = "--global" in sys.argv

    success = init_skill(name, global_scope)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
