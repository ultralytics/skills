# AGENTS.md

Repository guidance for coding agents. `CLAUDE.md` is a symlink to this file.

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

## Commands and validation

```bash
python3 .github/scripts/lint_skills.py
claude --plugin-dir .
```

The validator checks skill format, metadata, and manifest agreement; it does not execute examples or establish factual correctness. Ground package facts against the version documented in the READMEs and companion headings; inspect `yolo checks`, `yolo cfg`, `export_formats()`, and the matching package source. Ground Platform instructions against live docs and installed `ul cloud <resource> <operation> --help`. Installed plugins are cached; `claude --plugin-dir .` exercises this checkout directly.

## Where to look

- Skill instructions and companion references → `skills/`.
- Validation rules → `.github/scripts/lint_skills.py`.
- Plugin packaging → `.claude-plugin/`, `.codex-plugin/`.
- Install and grounding version → `README.md`, `README.zh-CN.md`.
- Skill dropdowns → `.github/ISSUE_TEMPLATE/`.

## Conventions

- `SKILL.md` frontmatter is exactly two keys, `name` and `description`, and must be the very first bytes of the file. Do not add a license header or blank line above it, and do not add vendor keys (`license`, `metadata`, `allowed-tools`) — the linter rejects any third key. House style (not linted) writes `description` as a YAML folded scalar (`description: >` followed by indented lines) so it wraps in the file.
- Descriptions state when to use the skill (with trigger keywords), never summarize its workflow. Where two skills border each other, the description says which sibling to use instead (`yolo-export` ↔ `yolo-inference`, `yolo-training` ↔ `yolo-tuning`, `platform-cli` → `yolo`).
- Version-volatile catalogs (weight names, argument tables, export format matrix, Solutions list) live in flat companion `.md` files next to `SKILL.md` and are referenced from a `## Related pages` section as `` `file.md` (this folder) ``; keep them flat (no subdirectories). The three package-derived catalogs (`training-args.md`, `format-matrix.md`, `weights-catalog.md`) carry the grounded version in their `# Title (v8.4.138)` heading; `label-formats.md` and `solutions.md` do not.
- Facts are grounded against a pinned `ultralytics` version (currently v8.4.138, stated in `README.md`, `README.zh-CN.md`, this file, and the companion-file headings) and every skill ends by deferring to the installed version (`yolo checks`, `yolo cfg`, `ul version`, `ul cloud <resource> <operation> --help`, error messages) over its own tables. `platform-cli` is deliberately not pinned to an `ultralytics-platform` version; its facts defer to the installed CLI's help and the live `/openapi.json`. When a new ultralytics release changes defaults, update the companion catalog files rather than rewriting SKILL.md bodies.
- Stage skills cover both surfaces: `yolo-datasets`, `yolo-training`, `yolo-inference`, and `yolo-export` open with a `## Fastest route: ... in Platform` section, `yolo-models` with `## Choose in Platform`, and `yolo-tuning` puts `## Compare experiments in Platform` right after its playbook; the local `yolo`/Python path follows, and training, inference, and export end with a `## Troubleshooting` symptom→fix table. Follow the existing bodies for house style: `key=value` arguments (never `--flags`), YOLO26 as the default recommendation, no "v" in YOLO11/YOLO26 (only legacy YOLOv8/YOLOv10 keep it), `best.pt` for inference and `last.pt` only for `resume=True`, `stream=True` for video, `quantize=` rather than the deprecated `half=`/`int8=`.
- `agents/openai.yaml` and the lint script carry the `# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license` header; Markdown files carry no header.
- Links: use canonical Ultralytics URLs without trailing slashes (`https://docs.ultralytics.com/platform`, `https://www.ultralytics.com`) and follow redirects to their final target before committing; `format.yml` runs a Lychee link check on PRs, and #9 canonicalized redirected and trailing-slash URLs repo-wide.
- Ultralytics-owned PyPI packages use `MAJOR.MINOR.PATCH` versions only; no suffixes.

## Pitfalls

- Every directory under `skills/` is treated as a skill. Do not park drafts, shared assets, or `__pycache__` there.
