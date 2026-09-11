# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, etc.) when working with code in this repository. CLAUDE.md is a symlink to this file.

`ultralytics/skills` (AGPL-3.0) is a pack of agent skills in the [Agent Skills format](https://agentskills.io) for Ultralytics Platform, the `ultralytics` Python package, the `yolo` CLI, and the `ul` Platform CLI (`ultralytics-platform`). There is no runtime code to build or import: the repo is Markdown skill content under `skills/`, one Python validator (`.github/scripts/lint_skills.py`), and four manifests that package the same `skills/` tree as a Claude Code and Codex plugin; `npx skills add ultralytics/skills` and manual copies read the skill directories directly. The plugin is named `yolo` and the marketplace `ultralytics`, so users install `yolo@ultralytics`; the plugin version lives in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` (currently `0.3.0`, and the two must match).

## Core Principles (CRITICAL)

**Less is more. The simplest solution is the best solution.** The action hierarchy for every change: **Delete > Replace > Add**.

1. **Solve at the owner**: Put behavior in the code path that owns or observes it. For fixes, never guard a symptom with a staleness check, initialization flag, skip-first-call branch, or `try/except` around broken logic; relocate the trigger and delete the wrong path. For features, extend the existing owner rather than creating a parallel abstraction.
2. **Search and reuse first**: Search the whole repository before creating a feature, component, helper, workflow, or utility. Reuse or adapt what exists, consolidate in-scope duplication in the shared owner, and delete duplicate paths. Three similar lines beat a helper nobody else calls.
3. **Delete and modify existing code before creating new code**: Bugfixes are net-negative by default unless deletion and relocation are demonstrably impossible. A new file must first prove it cannot fit cleanly in an existing owner.
4. **Keep scope minimal**: Implement only the simplest complete solution. Avoid impossible-state handling, speculative flags, compatibility shims, policy scaffolding, and unrelated cleanup. Tests are out of scope by default — rely on existing coverage and focused validation; only an uncovered, high-risk regression path justifies minimal new test code.
5. **Ship zero-regression, production-ready changes**: Understand what you remove instead of retaining broken code as insurance. Remove unused imports, functions, types, files, and comments; run relevant cleanup checks; and thoroughly debug and validate the changed owner. Do not break existing features or workflows unless the PR intentionally removes them with evidence.

**Review gate:** for every addition, the reviewer decides whether deleting or changing existing code would have fixed the problem instead — if it would, that is a blocking finding. A missing or thin PR description is never itself a finding.

NEVER push to `main`. NEVER force push. Always start work in a new git worktree (`git worktree add`) on a feature branch and open a PR — never edit the primary checkout directly, it may hold in-flight work.

## PR Workflow

After opening a PR:

1. Wait for the automated PR review and auto-format commit from Ultralytics Actions (`format.yml`), then pull and address every finding.
2. Review the full diff in-session against the Core Principles, performance, and the review gate above, then batch the fixes into one commit and push. After each round of bot or human commits, pull and resume the same reviewer on `<last-reviewed-sha>..HEAD` plus anything that delta could have invalidated. Repeat until the local head matches the live head.
3. Hand off or merge only on a clean final pass: one cold full-diff review returning LGTM with no findings, on a head that is still live at merge time.
4. Never fight other commits: Ultralytics Actions may push commits, and multiple users may work on the same PR. `git pull --rebase` before pushing; never reset or revert commits you did not author.
5. After the PR merges, clean up: remove local worktrees and branches for it, then `git checkout main && git pull`.

## Commands

```bash
python .github/scripts/lint_skills.py # the sole CI job: skill frontmatter, size limits, openai.yaml, manifest JSON (stdlib only, no install)
claude plugin validate .              # optional: validates .claude-plugin/marketplace.json (Claude Code CLI)

# Try the skills from this checkout without installing anything
claude --plugin-dir .

# Install the local clone as a plugin (Claude Code / Codex); restart Codex after edits
claude plugin marketplace add . && claude plugin install yolo@ultralytics
codex plugin marketplace add . && codex plugin add yolo@ultralytics

# Ground a fact against the pinned package version (see Conventions) before writing it into a skill
pip install ultralytics==8.4.138 && yolo checks && yolo cfg
python -c "from ultralytics.engine.exporter import export_formats; print(export_formats())"
python -c "from ultralytics.utils.downloads import GITHUB_ASSETS_NAMES; print(*sorted(GITHUB_ASSETS_NAMES), sep='\n')"
```

- The lint script exits 1 with one `ERROR:` line per problem and otherwise prints `OK: <n> skills, <n> OpenAI metadata files, and 4 manifests validated`. It has no dependencies beyond the standard library; CI runs it on Python 3.13.
- Read grounding output through the matching companion file: `yolo cfg` prints base defaults that task trainers, checkpoints, and explicit arguments can override (`skills/yolo-training/training-args.md` says to inspect a run's `args.yaml` for effective values); `GITHUB_ASSETS_NAMES` is the package-known fast-path set, not an exhaustive catalog, so an unlisted official asset is not automatically invalid (`skills/yolo-models/weights-catalog.md`); `export_formats()` rows key `skills/yolo-export/format-matrix.md` by `format=` value.
- There is no formatter config in this repo (no `pyproject.toml`, no Prettier or codespell config). Formatting is applied by the Ultralytics Actions bot on the PR branch, which pushes an `Auto-format by https://ultralytics.com/actions` commit when it produces changes, so `git pull --rebase` before pushing again.
- Running `yolo` commands from the repo root is mostly safe for git: `.gitignore` covers `runs/`, `weights/`, `datasets/`, `*.pt`, and the export suffixes and `*_<fmt>_model/` directories, but not Core AI `.aimodel` files.

## Where to look

- **Wrong fact in a skill** (argument name, default, weight name, export format, CLI shape) → verify against `ultralytics==8.4.138` (`yolo cfg`, `export_formats()`, `GITHUB_ASSETS_NAMES`) or `ul cloud ... --help` / `/openapi.json`, then fix the owner: version-volatile tables in the companion `.md`, procedures and gotchas in `SKILL.md`. If the fact appears in the router (`skills/yolo/SKILL.md`) or a README description, fix those too.
- **Adding a stage skill** → `skills/<name>/SKILL.md` (frontmatter + body) and `skills/<name>/agents/openai.yaml`; add a row to `## Route before coding` in `skills/yolo/SKILL.md` and to the skill tables in `README.md` and `README.zh-CN.md`; add the name to the `Skill` dropdowns in `.github/ISSUE_TEMPLATE/bug-report.yml` and `feature-request.yml` (both still lack `platform-cli`); update `description` and bump `version` in both `plugin.json` files (the linter requires them to match) and `interface.longDescription` in `.codex-plugin/plugin.json`; update the skill count and list in this file; run the lint script. CI checks only the manifest agreement; the router, README, issue-template, and description wiring is manual.
- **New ultralytics release** → confirm the changed defaults from the installed version, update the `(v8.4.x)` headings and tables in `training-args.md`, `format-matrix.md`, `weights-catalog.md`, review `label-formats.md` and `solutions.md` (no version in their headings, so a search for the old version misses them), any body text that quotes a default, and the pinned-version sentence in both READMEs and this file. #11 (8.4.119 → 8.4.138) is the reference diff: 15 files, mostly companion tables.
- **Skill not triggering / triggering too often** → the `description` frontmatter of that skill (trigger keywords, sibling hand-offs). The router's `## Route before coding` table is prose the agent follows after `yolo` loads, not executable dispatch, and stage skills can be selected directly by their own descriptions or by name.
- **Install/packaging problem** (`yolo@ultralytics` not found, wrong version shown, Codex picker text) → the four manifests plus `README.md` install sections; `claude plugin validate .` checks the Claude marketplace manifest, the lint script checks cross-manifest consistency.
- **Formatter or link-check failures on a PR** → let the Actions bot commit Prettier/Ruff/codespell fixes and pull them; fix Lychee failures by hand (canonical URL, no trailing slash, follow the redirect).
- **Changing the validation contract** → `.github/scripts/lint_skills.py` (and `ci.yml` only if the Python version or trigger changes).

## Architecture

Paths below are relative to the repo root.

**How a skill reaches an agent.** Claude Code reads `.claude-plugin/marketplace.json` (`"source": "./"`) and Codex reads `.agents/plugins/marketplace.json` (`"source": {"source": "local", "path": "./"}`); each exposes exactly one plugin, `yolo`, resolving to the repo root. The matching `.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` then points at the tree with `"skills": "./skills/"`. Each `skills/<name>/` directory is one skill: the agent indexes `SKILL.md` frontmatter (`name` + `description`) to decide when to load it, reads the body when triggered, and opens companion files only when the body tells it to. `npx skills add ultralytics/skills` and manual copies bypass the manifests and read `skills/` directly, which is why frontmatter stays portable (no vendor keys). `skills/<name>/agents/openai.yaml` is Codex/ChatGPT presentation metadata (display name, short description, default prompt) and is not read by other agents. Nothing in the repo is executed at install time.

- `skills/yolo/SKILL.md` — the overview and router. Its description ("Use for ANY task involving Ultralytics Platform, the ultralytics Python package, yolo CLI, ...") is deliberately broad; the body carries the three surfaces (Platform UI, `yolo`/Python, `ul` CLI), the `yolo TASK MODE key=value` grammar, the five-command lifecycle, `## Route before coding` (a table mapping "Working on ..." → the seven stage skills), `## CLI specifics` (parsing rules: bare booleans, `cfg=` reset semantics, model-stem → architecture dispatch), and `## Global directives` (validate data first, always fine-tune from pretrained, `stream=True`, `best.pt`, verify export parity, prefer built-ins, trust the installed version). A new stage skill must be added to that routing table.
- `skills/yolo-models/` — family/size/task-suffix selection, Platform Explore flow, architecture YAMLs; `weights-catalog.md` is the model-asset reference covering the package-known `GITHUB_ASSETS_NAMES` fast-path set and specialized official assets outside it, and the body ends with the one-liner that prints the installed set.
- `skills/yolo-datasets/` — Platform upload/annotation, `images` → `labels` mirror rule, `data.yaml` anatomy per task (detect/segment/semantic/depth/classify/pose/obb), built-in converters, splitting, a pre-training validation checklist, the `coco8`-style smoke datasets; `label-formats.md` holds exact per-task label line formats and a symptom→cause table.
- `skills/yolo-training/` — Platform cloud training and the `ul://owner/datasets/slug` + `project=username/project-slug` remote-metrics recipe (`ultralytics>=8.4.120`), local quickstart, base arguments, recipes, reading `runs/<task>/<name>/`, troubleshooting; `training-args.md` is the pinned `default.yaml` argument/augmentation/loss-weight table.
- `skills/yolo-tuning/` — the ordered improvement playbook (tuning is the last step), Platform experiment comparison, `model.tune()` genetic tuner, Ray Tune, evolution budget rules.
- `skills/yolo-inference/` — Platform Predict and dedicated endpoints, `predict`/`track` quickstart, sources, arguments, Results API, tracking with `persist=True`, annotated-video pattern, performance checklist; `solutions.md` lists the prebuilt Solutions to use instead of hand-rolled counting/heatmap/speed logic.
- `skills/yolo-export/` — Platform Export tab, `yolo export`, format-by-hardware table, key arguments (`quantize`, `dynamic`, ...), parity verification, benchmarking, consuming exports outside Python; `format-matrix.md` is the pinned `export_formats()` table (21 targets).
- `skills/platform-cli/` — the `ul cloud RESOURCE OPERATION key=value` CLI: canonical command shapes, argument and behavior rules (`body=` JSON for union-shaped requests, `@file.json`/`@-` inputs, exit codes 1/2/130, no automatic pagination, owner defaulting), a working method, a goal→commands workflow table, cloud training, recovery (trash/restore), and per-operation gotchas. No companion file; it defers to `ul cloud ... --help`, the [Platform API reference](https://docs.ultralytics.com/platform/api), and `https://platform.ultralytics.com/openapi.json`.
- `.github/scripts/lint_skills.py` — the single validator and the de-facto schema: a top-level script with no functions, arguments, or main guard; `ROOT` is derived from its own location, so run it from anywhere. Per immediate child directory of `skills/` (any directory counts, so a stray folder fails CI): `SKILL.md` exists, frontmatter matches `^---\n(.*?)\n---\n` at offset 0, keys are exactly `{name, description}`, `name == dirname`, name matches `[a-z0-9]+(-[a-z0-9]+)*` and ≤64 chars, description non-empty and ≤1024 after whitespace collapsing, ≤500 newlines in the whole file, `agents/openai.yaml` exists with `interface:` and the three quoted fields (`short_description` 25–64 chars, `default_prompt` containing `$<dirname>`). Then it parses the four `MANIFESTS` as JSON, requires `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` to agree on `name`, `version`, and `skills`, requires `skills == "./skills/"`, and requires each marketplace to list exactly one plugin whose `name` equals the plugin's. Everything is regex, not a YAML parser: the description is whatever follows the first `description:` in the frontmatter, so keep `name` first and the folded `description` last; `openai.yaml` values must be double-quoted on one line with exactly two-space indentation (`^  key: "(.+)"$`). It does not open companion files, resolve `## Related pages` references, compare the README/router/issue-template skill lists, check version pins, or validate marketplace `source` objects or other vendor fields. Edit this script to change the format contract; there is no other schema.
- `.claude-plugin/plugin.json` also carries `displayName`, `description`, `keywords`, `license`, `repository`; `.codex-plugin/plugin.json` adds an `interface` block (`shortDescription`, `longDescription`, `defaultPrompt` list, `brandColor`, legal URLs) that Codex renders in its marketplace and the linter does not check.
- `README.md` / `README.zh-CN.md` — the public skill table (one row per skill, kept in the same order as the router table), install commands per agent, design notes, and the sentence pinning the grounded `ultralytics` version. Both files change together.
- `.github/ISSUE_TEMPLATE/` — `bug-report.yml` and `feature-request.yml` have a `Skill` dropdown enumerating skill names; `config.yml` redirects package bugs to `ultralytics/ultralytics`. `.github/PULL_REQUEST_TEMPLATE.md` restates the skill content checklist and CLA sentence.

## Conventions

- `SKILL.md` frontmatter is exactly two keys, `name` and `description`, and must be the very first bytes of the file. Do not add a license header or blank line above it, and do not add vendor keys (`license`, `metadata`, `allowed-tools`) — the linter rejects any third key. House style (not linted) writes `description` as a YAML folded scalar (`description: >` followed by indented lines) so it wraps in the file.
- Descriptions state when to use the skill (with trigger keywords), never summarize its workflow. Where two skills border each other, the description says which sibling to use instead (`yolo-export` ↔ `yolo-inference`, `yolo-training` ↔ `yolo-tuning`, `platform-cli` → `yolo`).
- Version-volatile catalogs (weight names, argument tables, export format matrix, Solutions list) live in flat companion `.md` files next to `SKILL.md` and are referenced from a `## Related pages` section as `` `file.md` (this folder) ``; keep them flat (no subdirectories). The three package-derived catalogs (`training-args.md`, `format-matrix.md`, `weights-catalog.md`) carry the grounded version in their `# Title (v8.4.138)` heading; `label-formats.md` and `solutions.md` do not.
- Facts are grounded against a pinned `ultralytics` version (currently v8.4.138, stated in `README.md`, `README.zh-CN.md`, this file, and the companion-file headings) and every skill ends by deferring to the installed version (`yolo checks`, `yolo cfg`, `ul version`, `ul cloud <resource> <operation> --help`, error messages) over its own tables. `platform-cli` is deliberately not pinned to an `ultralytics-platform` version; its facts defer to the installed CLI's help and the live `/openapi.json`. When a new ultralytics release changes defaults, update the companion catalog files rather than rewriting SKILL.md bodies.
- Stage skills cover both surfaces: `yolo-datasets`, `yolo-training`, `yolo-inference`, and `yolo-export` open with a `## Fastest route: ... in Platform` section, `yolo-models` with `## Choose in Platform`, and `yolo-tuning` puts `## Compare experiments in Platform` right after its playbook; the local `yolo`/Python path follows, and training, inference, and export end with a `## Troubleshooting` symptom→fix table. Follow the existing bodies for house style: `key=value` arguments (never `--flags`), YOLO26 as the default recommendation, no "v" in YOLO11/YOLO26 (only legacy YOLOv8/YOLOv10 keep it), `best.pt` for inference and `last.pt` only for `resume=True`, `stream=True` for video, `quantize=` rather than the deprecated `half=`/`int8=`.
- `agents/openai.yaml` and the lint script carry the `# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license` header; Markdown files carry no header.
- Links: use canonical Ultralytics URLs without trailing slashes (`https://docs.ultralytics.com/platform`, `https://www.ultralytics.com`) and follow redirects to their final target before committing; `format.yml` runs a Lychee link check on PRs, and #9 canonicalized redirected and trailing-slash URLs repo-wide.
- Ultralytics-owned PyPI packages use `MAJOR.MINOR.PATCH` versions only; no suffixes.

## Workflows

- `.github/workflows/ci.yml` (CI) — one `Lint` job on pushes to `main` and PRs targeting `main`: `actions/checkout`, `actions/setup-python` (3.13), `python .github/scripts/lint_skills.py`. It never installs `ultralytics`, so skill content is not executed or fact-checked automatically.
- `.github/workflows/format.yml` (Ultralytics Actions) — on PR open/sync/close/review-request and on new issues. Runs Ruff on the lint script (`python: true`), Prettier on YAML/JSON/Markdown (including every `SKILL.md`, companion `.md`, README, and manifest), codespell (`spelling: true`), Lychee broken-link checks (`links: true`), AI labels and PR summaries. It commits fixes back to the PR branch when there are any.
- `.github/workflows/cla.yml` (CLA) — on `pull_request_target` and issue comments; external contributors sign by commenting `I have read the CLA Document and I sign the CLA` (also `recheck`). Uses `ultralytics/actions/cla@main`.
- `.github/dependabot.yml` — weekly `github-actions` version bumps, labeled `dependencies`.

There is no publish or release workflow: the plugin is consumed straight from the GitHub repo (`claude plugin marketplace add ultralytics/skills`, `codex plugin marketplace add ultralytics/skills`, `npx skills add ultralytics/skills`), so whatever is on `main` is live for new installs. Bump the plugin `version` in both `plugin.json` files when skill content changes in a way users should re-install for (#12 went `0.2.0` → `0.3.0` when adding `platform-cli`).

## Gotchas

- Every directory under `skills/` is treated as a skill. Do not park drafts, shared assets, or `__pycache__` there.
- CI never executes the skills or installs `ultralytics`; a green check proves format, not correctness. Run the grounding commands above before changing any argument, default, weight name, or export format.
- Prettier runs on every Markdown, YAML, and JSON file on the PR branch and realigns tables; do not hand-tune table column widths or fight the bot commit.
- The Platform-facing content (Platform UI flows, `ul cloud` operations, `/openapi.json` shapes) is grounded against the live product and docs, not a package version, so it can drift without any version bump — re-check `ul cloud <resource> <operation> --help` when touching `platform-cli`.
- Codex reads installed plugins at startup: restart Codex after editing a locally installed clone, and for the GitHub-sourced install run `codex plugin marketplace upgrade ultralytics` then `codex plugin add yolo@ultralytics` to pull a new version (README install section).

## Tests

There is no test suite. The sole job in `ci.yml` runs `python .github/scripts/lint_skills.py` (structure and manifests) on Python 3.13; `format.yml` adds Prettier, Ruff, codespell, and Lychee link checks on PRs. Content correctness is verified manually: load this checkout with `claude --plugin-dir .`, run a representative prompt against the edited skill, confirm the agent reads the skill and any companion it needs, and paste the prompt and response into the PR as the template asks. For a `description` change, also try a natural-language prompt that does not name the skill plus a neighboring task that should select its sibling — invoking a skill by name checks the guidance but not the trigger.
