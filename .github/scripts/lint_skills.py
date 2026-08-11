# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license
"""Validate skill format, OpenAI metadata, and plugin manifests."""

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
errors = []
manifests = {}
metadata_count = 0
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
    if len(keys) != 2 or set(keys) != {"name", "description"}:
        errors.append(
            f"{d.name}: frontmatter keys must be exactly name+description, got {keys}"
        )
    if name != d.name:
        errors.append(f"{d.name}: name '{name}' != directory name")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name or "") or len(name) > 64:
        errors.append(f"{d.name}: invalid name '{name}'")
    if not desc or len(desc) > 1024:
        errors.append(f"{d.name}: description empty or >1024 chars ({len(desc)})")
    if lines > 500:
        errors.append(f"{d.name}: SKILL.md is {lines} lines (max 500)")

    metadata = d / "agents" / "openai.yaml"
    if not metadata.is_file():
        errors.append(f"{d.name}: missing agents/openai.yaml")
        continue
    metadata_count += 1
    metadata_text = metadata.read_text(encoding="utf-8")
    values = {
        key: match.group(1)
        if (match := re.search(rf'^  {key}: "(.+)"$', metadata_text, re.MULTILINE))
        else ""
        for key in ("display_name", "short_description", "default_prompt")
    }
    if not re.search(r"^interface:\n", metadata_text, re.MULTILINE) or not all(
        values.values()
    ):
        errors.append(
            f"{d.name}: openai.yaml requires quoted display_name, short_description, and default_prompt"
        )
    if values["short_description"] and not 25 <= len(values["short_description"]) <= 64:
        errors.append(
            f"{d.name}: openai.yaml short_description must be 25-64 characters"
        )
    if values["default_prompt"] and f"${d.name}" not in values["default_prompt"]:
        errors.append(f"{d.name}: openai.yaml default_prompt must mention ${d.name}")

for rel in MANIFESTS:
    try:
        manifests[rel] = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        errors.append(f"{rel}: {e}")

claude = manifests.get(".claude-plugin/plugin.json", {})
codex = manifests.get(".codex-plugin/plugin.json", {})
for key in ("name", "version", "skills"):
    if claude.get(key) != codex.get(key):
        errors.append(
            f"plugin manifests disagree on {key}: {claude.get(key)!r} != {codex.get(key)!r}"
        )
if codex.get("skills") != "./skills/":
    errors.append("plugin manifests must point skills to './skills/'")

claude_plugins = manifests.get(".claude-plugin/marketplace.json", {}).get("plugins", [])
codex_plugins = manifests.get(".agents/plugins/marketplace.json", {}).get("plugins", [])
if len(claude_plugins) != 1 or claude_plugins[0].get("name") != codex.get("name"):
    errors.append("Claude marketplace must expose the packaged plugin")
if len(codex_plugins) != 1 or codex_plugins[0].get("name") != codex.get("name"):
    errors.append("Codex marketplace must expose the packaged plugin")

if errors:
    print("\n".join(f"ERROR: {e}" for e in errors))
    sys.exit(1)
print(
    f"OK: {len(skill_dirs)} skills, {metadata_count} OpenAI metadata files, and {len(MANIFESTS)} manifests validated"
)
