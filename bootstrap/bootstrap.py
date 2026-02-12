#!/usr/bin/env python3
"""
Claude Code Bootstrap Skill
Fast project creation from templates
"""

import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import json

# Try to import jinja2, provide helpful error if missing
try:
    from jinja2 import Template
except ImportError:
    print("❌ Error: jinja2 not installed")
    print("Install: pip install jinja2")
    sys.exit(1)

TEMPLATES_DIR = Path.home() / ".claude" / "templates"

# Available templates
TEMPLATES = {
    "python-data": "Data analysis project",
    "python-app": "Python application",
    "consulting": "Kearney consulting deliverable",
    "research": "Research memo",
    "generic": "Minimal Python project",
}


def get_git_config(key: str, default: str = "") -> str:
    """Get git config value"""
    try:
        result = subprocess.run(
            ["git", "config", "--global", key],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip() or default
    except Exception:
        return default


def render_template(template_str: str, context: Dict) -> str:
    """Render Jinja2 template"""
    return Template(template_str).render(**context)


def bootstrap_project(template_name: str, project_name: str):
    """Bootstrap a new project from template"""

    # Validate template
    if template_name not in TEMPLATES:
        print(f"❌ Template not found: {template_name}")
        print(f"\nAvailable templates:")
        for name, desc in TEMPLATES.items():
            print(f"  {name:15} - {desc}")
        sys.exit(1)

    template_path = TEMPLATES_DIR / template_name
    if not template_path.exists():
        print(f"❌ Template directory not found: {template_path}")
        print(f"Expected location: {TEMPLATES_DIR}")
        sys.exit(1)

    # Check if project directory already exists
    project_path = Path.cwd() / project_name
    if project_path.exists():
        print(f"❌ Directory already exists: {project_name}")
        print(f"Choose a different name or remove existing directory")
        sys.exit(1)

    print(f"🚀 Bootstrapping '{project_name}' from template '{template_name}'")
    print("")

    # Create project directory
    project_path.mkdir()
    print(f"✅ Created directory: {project_name}/")

    # Build template context
    context = {
        "project_name": project_name,
        "project_name_snake": project_name.replace("-", "_").replace(" ", "_"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "year": datetime.now().year,
        "author": get_git_config("user.name", "Your Name"),
        "email": get_git_config("user.email", "you@example.com"),
    }

    # Copy and render template files
    print("📋 Creating project structure...")
    files_created = 0
    for template_file in template_path.rglob("*"):
        if template_file.is_file() and not template_file.name.startswith('.'):
            # Calculate relative path
            relative = template_file.relative_to(template_path)

            # Render path with context (for dynamic directory names)
            relative_str = str(relative)
            if "{{" in relative_str:
                relative_str = render_template(relative_str, context)

            target = project_path / relative_str
            target.parent.mkdir(parents=True, exist_ok=True)

            # Render file content for text files
            if template_file.suffix in ['.md', '.py', '.txt', '.toml', '.yaml', '.yml', '.json', '.html', '.css', '.js', '.sh']:
                try:
                    content = template_file.read_text()
                    rendered = render_template(content, context)
                    target.write_text(rendered)
                    files_created += 1
                except Exception as e:
                    print(f"⚠️  Warning: Could not render {relative}: {e}")
                    # Copy as-is if rendering fails
                    target.write_bytes(template_file.read_bytes())
            else:
                # Copy binary files as-is
                target.write_bytes(template_file.read_bytes())
                files_created += 1

    print(f"✅ Created {files_created} files")

    # Initialize git
    print("🔧 Initializing git repository...")
    try:
        subprocess.run(
            ["git", "init"],
            cwd=project_path,
            check=True,
            capture_output=True,
        )
        print("✅ Git initialized")
    except subprocess.CalledProcessError:
        print("⚠️  Warning: Could not initialize git")
    except FileNotFoundError:
        print("⚠️  Warning: git not found")

    # Create virtual environment
    print("🐍 Creating Python virtual environment...")
    try:
        subprocess.run(
            [sys.executable, "-m", "venv", "venv"],
            cwd=project_path,
            check=True,
            capture_output=True,
        )
        print("✅ Virtual environment created")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create venv: {e}")
        print("Continue manually with: python3 -m venv venv")

    # Print success message and next steps
    print("")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"✅ Project '{project_name}' created successfully!")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")
    print("Next steps:")
    print(f"  cd {project_name}")

    # OS-specific activation command
    if os.name == 'nt':  # Windows
        print(f"  venv\\Scripts\\activate")
    else:  # Unix/Mac
        print(f"  source venv/bin/activate")

    print(f"  pip install -r requirements.txt")
    print("")

    # Template-specific next steps
    if template_name == "python-data":
        print("For data analysis:")
        print("  jupyter notebook  # Open notebooks/")
        print("  # Or use: /eda data/raw/your-data.csv")
    elif template_name == "python-app":
        print("For application development:")
        print("  make install  # Install dependencies")
        print("  make test     # Run tests")
    elif template_name == "consulting":
        print("For Kearney deliverable:")
        print("  # Add data to data/")
        print("  # Use /kearney-design skill for on-brand visuals")
        print("  # Read CLAUDE.md for brand rules")
    elif template_name == "research":
        print("For research memo:")
        print("  # Edit research/memo.md")
        print("  make pdf      # Build PDF")

    print("")
    print(f"Read: {project_name}/README.md")
    print("")


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: bootstrap.py <template> <project-name>")
        print("")
        print("Available templates:")
        for name, desc in TEMPLATES.items():
            print(f"  {name:15} - {desc}")
        print("")
        print("Example:")
        print("  bootstrap.py python-data customer-analysis")
        sys.exit(1)

    template_name = sys.argv[1]
    project_name = sys.argv[2]

    bootstrap_project(template_name, project_name)


if __name__ == "__main__":
    main()
