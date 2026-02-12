#!/usr/bin/env python3
"""
Validate a generated Remotion project for common issues.
Usage: python3 validate.py <project-directory>

Checks:
1. Required files exist
2. Package.json dependencies & version consistency
3. No Math.random() or Date.now() (non-deterministic)
4. interpolate() calls have extrapolate clamping
5. staticFile() references resolve to public/ files
6. Video/Audio imported from @remotion/media
7. Transition presentations from correct subpaths
8. spring() calls include fps parameter
9. TransitionSeries alternation order
10. Composition has all required props
11. No 'any' types, no raw <img> tags
"""

import sys
import re
import json
from pathlib import Path
from typing import List


class ValidationResult:
    def __init__(self):
        self.passed: List[str] = []
        self.warnings: List[str] = []
        self.errors: List[str] = []

    def pass_check(self, msg: str):
        self.passed.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def error(self, msg: str):
        self.errors.append(msg)

    @property
    def ok(self):
        return len(self.errors) == 0

    def report(self):
        print("\n" + "=" * 60)
        print("REMOTION PROJECT VALIDATION REPORT")
        print("=" * 60)
        if self.passed:
            print(f"\n  PASSED ({len(self.passed)}):")
            for p in self.passed:
                print(f"    ✅ {p}")
        if self.warnings:
            print(f"\n  WARNINGS ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"    ⚠️  {w}")
        if self.errors:
            print(f"\n  ERRORS ({len(self.errors)}):")
            for e in self.errors:
                print(f"    ❌ {e}")
        print("\n" + "-" * 60)
        if self.ok:
            print(f"  RESULT: PASS — {len(self.passed)} passed, {len(self.warnings)} warnings")
        else:
            print(f"  RESULT: FAIL — {len(self.errors)} errors, {len(self.warnings)} warnings")
        print("-" * 60 + "\n")
        return self.ok


def find_ts_files(project_dir: Path) -> List[Path]:
    src = project_dir / "src"
    return (list(src.rglob("*.ts")) + list(src.rglob("*.tsx"))) if src.exists() else []


def check_required_files(d: Path, r: ValidationResult):
    for f in ["package.json", "tsconfig.json", "src/index.ts", "src/Root.tsx"]:
        (r.pass_check if (d / f).exists() else r.error)(f"Required file: {f}")
    for f in ["remotion.config.ts", "src/Video.tsx", "src/theme.ts"]:
        (r.pass_check if (d / f).exists() else r.warn)(f"Expected file: {f}")


def check_package_json(d: Path, r: ValidationResult):
    p = d / "package.json"
    if not p.exists():
        r.error("package.json not found"); return
    try:
        pkg = json.loads(p.read_text())
    except json.JSONDecodeError:
        r.error("package.json invalid JSON"); return

    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    for dep in ["remotion", "@remotion/cli"]:
        (r.pass_check if dep in deps else r.error)(f"Dependency: {dep}")

    versions = {}
    for name, ver in deps.items():
        if name == "remotion" or name.startswith("@remotion/"):
            versions[name] = ver.lstrip("^~")
    if len(set(versions.values())) <= 1:
        r.pass_check("Remotion package versions consistent")
    else:
        r.error(f"Version mismatch: {versions}")


def check_forbidden_patterns(files: List[Path], r: ValidationResult):
    found_random = found_date = False
    for f in files:
        c = f.read_text()
        if re.search(r'Math\.random\(\)', c):
            r.error(f"Math.random() in {f.name} — use random('seed') from 'remotion'")
            found_random = True
        if re.search(r'Date\.now\(\)', c):
            r.error(f"Date.now() in {f.name} — non-deterministic")
            found_date = True
        if re.search(r'console\.(log|warn|error)\(', c):
            r.warn(f"console statement in {f.name}")
    if not found_random: r.pass_check("No Math.random() usage")
    if not found_date: r.pass_check("No Date.now() usage")


def check_interpolate_clamping(files: List[Path], r: ValidationResult):
    unclamped = []
    for f in files:
        lines = f.read_text().split('\n')
        for i, line in enumerate(lines):
            if 'interpolate(' in line and 'interpolateColors(' not in line:
                ctx = '\n'.join(lines[max(0,i-1):min(len(lines),i+8)])
                if 'clamp' not in ctx:
                    unclamped.append(f"{f.name}:{i+1}")
    if unclamped:
        for loc in unclamped: r.warn(f"interpolate() possibly missing clamp at {loc}")
    else:
        r.pass_check("All interpolate() calls have clamping")


def check_media_imports(files: List[Path], r: ValidationResult):
    """Ensure Video/Audio come from @remotion/media, not 'remotion'."""
    found_wrong = False
    for f in files:
        content = f.read_text()
        # Find all import-from-remotion lines
        for line in content.split('\n'):
            # Only lines importing from exactly 'remotion' (not @remotion/*)
            if not re.search(r"""from\s+['"]remotion['"]""", line):
                continue
            if 'import' not in line:
                continue
            brace = re.search(r'\{([^}]+)\}', line)
            if not brace:
                continue
            imports = [s.strip().split(' as ')[0].strip() for s in brace.group(1).split(',')]
            for imp in imports:
                if imp == 'Video':
                    r.error(f"Video imported from 'remotion' in {f.name} — use '@remotion/media'")
                    found_wrong = True
                elif imp == 'Audio':
                    r.error(f"Audio imported from 'remotion' in {f.name} — use '@remotion/media'")
                    found_wrong = True

    if not found_wrong:
        r.pass_check("Video/Audio imports correct (from @remotion/media)")


def check_raw_img(files: List[Path], r: ValidationResult):
    for f in files:
        if re.search(r'<img\s', f.read_text()):
            r.warn(f"Raw <img> tag in {f.name} — use <Img> from 'remotion'")
            return
    r.pass_check("No raw <img> tags")


def check_static_files(d: Path, files: List[Path], r: ValidationResult):
    pub = d / "public"
    pat = re.compile(r"staticFile\(['\"]([^'\"]+)['\"]\)")
    refs = set()
    for f in files:
        for m in pat.finditer(f.read_text()):
            refs.add(m.group(1))
    if not refs:
        r.pass_check("No staticFile() references"); return
    missing = [ref for ref in sorted(refs) if not (pub / ref).exists()]
    if missing:
        for m in missing: r.error(f"Missing asset: public/{m}")
    else:
        r.pass_check(f"All {len(refs)} staticFile() references resolved")


def check_spring_fps(files: List[Path], r: ValidationResult):
    missing = []
    for f in files:
        lines = f.read_text().split('\n')
        for i, line in enumerate(lines):
            if re.search(r'spring\s*\(\s*\{', line):
                ctx = '\n'.join(lines[i:min(len(lines),i+6)])
                if 'fps' not in ctx:
                    missing.append(f"{f.name}:{i+1}")
    if missing:
        for loc in missing: r.error(f"spring() missing fps at {loc}")
    else:
        r.pass_check("All spring() calls include fps")


def check_transition_imports(files: List[Path], r: ValidationResult):
    pat = re.compile(
        r"import\s*\{[^}]*\b(fade|slide|wipe|flip|clockWipe|iris)\b[^}]*\}\s*from\s*['\"]@remotion/transitions['\"]"
    )
    for f in files:
        if pat.search(f.read_text()):
            r.error(f"Transition from '@remotion/transitions' in {f.name} — use subpath like '@remotion/transitions/fade'")
            return
    r.pass_check("Transition import paths correct")


def check_transition_series_order(files: List[Path], r: ValidationResult):
    tag_pat = re.compile(r'<TransitionSeries\.(Sequence|Transition)')
    for f in files:
        content = f.read_text()
        if 'TransitionSeries' not in content:
            continue
        tags = tag_pat.findall(content)
        if not tags:
            continue
        if tags[0] != 'Sequence':
            r.error(f"TransitionSeries must start with Sequence in {f.name}")
            return
        if tags[-1] != 'Sequence':
            r.error(f"TransitionSeries must end with Sequence in {f.name}")
            return
        for i in range(1, len(tags)):
            if tags[i] == tags[i-1]:
                r.error(f"Consecutive TransitionSeries.{tags[i]} in {f.name} — must alternate")
                return
    r.pass_check("TransitionSeries ordering correct")


def check_composition_props(d: Path, r: ValidationResult):
    root = d / "src" / "Root.tsx"
    if not root.exists():
        return
    content = root.read_text()
    for prop in ['durationInFrames', 'width', 'height', 'fps', 'component', 'id']:
        if prop not in content:
            r.error(f"Composition missing prop: {prop}")
            return
    r.pass_check("Composition has all required props")


def check_any_types(files: List[Path], r: ValidationResult):
    pat = re.compile(r':\s*any\b|as\s+any\b|<any>')
    found = []
    for f in files:
        for i, line in enumerate(f.read_text().split('\n'), 1):
            if pat.search(line):
                found.append(f"{f.name}:{i}")
    if found:
        for loc in found[:5]: r.warn(f"'any' type at {loc}")
        if len(found) > 5: r.warn(f"...and {len(found)-5} more")
    else:
        r.pass_check("No 'any' type usage")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate.py <project-directory>")
        sys.exit(1)

    d = Path(sys.argv[1]).resolve()
    if not d.exists():
        print(f"Error: Not found: {d}")
        sys.exit(1)

    print(f"\nValidating: {d}")
    r = ValidationResult()
    files = find_ts_files(d)

    if not files:
        r.error("No .ts/.tsx files in src/")
    else:
        r.pass_check(f"Found {len(files)} TypeScript files")

    check_required_files(d, r)
    check_package_json(d, r)
    check_forbidden_patterns(files, r)
    check_interpolate_clamping(files, r)
    check_media_imports(files, r)
    check_raw_img(files, r)
    check_static_files(d, files, r)
    check_spring_fps(files, r)
    check_transition_imports(files, r)
    check_transition_series_order(files, r)
    check_composition_props(d, r)
    check_any_types(files, r)

    ok = r.report()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
