# Ultralytics 🚀 AGPL-3.0 License - https://www.ultralytics.com/license
"""Validate skill format: SKILL.md frontmatter, size limits, and plugin manifest JSON."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFESTS = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
]
TRAILING_SLASH_URL = re.compile(
    r"https?://(?:[A-Za-z0-9-]+\.)*ultralytics\.com(?:/[^\s<>\"')\]?#]*)?/(?=[?#\s<>\"')\]]|$)"
)
APEX_URL = re.compile(r"https?://ultralytics\.com(?=[/:?#\s<>\"')\]]|$)")

errors = []
skill_dirs = sorted(d for d in (ROOT / "skills").iterdir() if d.is_dir())
if not skill_dirs:
    errors.append("no skill directories found under skills/")

for d in skill_dirs:
    sk = d / "SKILL.md"
    if not sk.is_file():
        errors.append(f"{d.name}: missing SKILL.md")
        continue
    text = sk.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        errors.append(f"{d.name}: no YAML frontmatter")
        continue
    fm = m.group(1)
    keys = re.findall(r"^([A-Za-z-]+):", fm, re.MULTILINE)
    name_match = re.search(r"^name: (\S+)", fm, re.MULTILINE)
    name = name_match.group(1) if name_match else ""
    desc = re.sub(r"\s+", " ", fm.split("description:", 1)[-1].replace(">", "")).strip()
    lines = text.count("\n")
    if set(keys) != {"name", "description"}:
        errors.append(f"{d.name}: frontmatter keys must be exactly name+description, got {keys}")
    if name != d.name:
        errors.append(f"{d.name}: name '{name}' != directory name")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name or "") or len(name) > 64:
        errors.append(f"{d.name}: invalid name '{name}'")
    if not desc or len(desc) > 1024:
        errors.append(f"{d.name}: description empty or >1024 chars ({len(desc)})")
    if lines > 500:
        errors.append(f"{d.name}: SKILL.md is {lines} lines (max 500)")

for rel in MANIFESTS:
    try:
        json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        errors.append(f"{rel}: {e}")

for path in ROOT.rglob("*"):
    if not path.is_file() or path.name == ".git":
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for lineno, line in enumerate(text.splitlines(), 1):
        if APEX_URL.search(line):
            errors.append(f"{path.relative_to(ROOT)}:{lineno}: use www.ultralytics.com, not ultralytics.com")
        if TRAILING_SLASH_URL.search(line):
            errors.append(f"{path.relative_to(ROOT)}:{lineno}: Ultralytics URLs must not end with /")

if errors:
    print("\n".join(f"ERROR: {e}" for e in errors))
    sys.exit(1)
print(f"OK: {len(skill_dirs)} skills and {len(MANIFESTS)} manifests validated")
