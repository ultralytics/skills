<a href="https://www.ultralytics.com"><img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320" alt="Ultralytics logo"></a>

# 🧠 Ultralytics Agent Skills

Agent skills for the [`ultralytics`](https://github.com/ultralytics/ultralytics) Python package and `yolo` CLI. They teach AI coding agents (Claude Code, Codex, Cursor, and any agent that reads the [Agent Skills format](https://agentskills.io)) the full computer-vision lifecycle: datasets → training → tuning → inference/tracking → export.

[![CI](https://github.com/ultralytics/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/ultralytics/skills/actions/workflows/ci.yml)
[![Ultralytics Actions](https://github.com/ultralytics/skills/actions/workflows/format.yml/badge.svg)](https://github.com/ultralytics/skills/actions/workflows/format.yml)

[![Ultralytics Discord](https://img.shields.io/discord/1089800235347353640?logo=discord&logoColor=white&label=Discord&color=blue)](https://discord.com/invite/ultralytics)
[![Ultralytics Forums](https://img.shields.io/discourse/users?server=https%3A%2F%2Fcommunity.ultralytics.com&logo=discourse&label=Forums&color=blue)](https://community.ultralytics.com)
[![Ultralytics Reddit](https://img.shields.io/reddit/subreddit-subscribers/ultralytics?style=flat&logo=reddit&logoColor=white&label=Reddit&color=blue)](https://reddit.com/r/ultralytics)

## 🧩 Skills

| Skill                                              | Use it for                                                                                                               |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| [`yolo`](skills/yolo/SKILL.md)                     | Core grammar (`yolo TASK MODE arg=value`, Python mirror), lifecycle overview, CLI specifics, routing to the other skills |
| [`yolo-models`](skills/yolo-models/SKILL.md)       | Choosing family/size/task variant: YOLO26/11/v8, YOLO-World, YOLOE, SAM, RT-DETR; exact weight names                     |
| [`yolo-datasets`](skills/yolo-datasets/SKILL.md)   | data.yaml, label formats, converters, auto-labeling, splitting, validation                                               |
| [`yolo-training`](skills/yolo-training/SKILL.md)   | train/val, arguments, recipes, reading runs, troubleshooting                                                             |
| [`yolo-tuning`](skills/yolo-tuning/SKILL.md)       | Systematic improvement playbook, `model.tune()` genetic search, Ray Tune                                                 |
| [`yolo-inference`](skills/yolo-inference/SKILL.md) | predict, Results API, tracking, annotated video, prebuilt Solutions                                                      |
| [`yolo-export`](skills/yolo-export/SKILL.md)       | ONNX/TensorRT/CoreML/OpenVINO/LiteRT/NPU export, quantization, benchmarking                                              |

Each skill is a `SKILL.md` (procedures, decision tables, gotchas) plus, where needed, a companion reference file holding version-volatile catalogs (weight names, argument tables, format matrix). Content is grounded against `ultralytics` v8.4.117.

## 📦 Install

The skills document the [`ultralytics`](https://pypi.org/project/ultralytics/) package — install or upgrade it in the environment your agent works in:

```bash
pip install -U ultralytics
```

### Claude Code

```bash
claude plugin marketplace add ultralytics/skills
claude plugin install yolo
```

<details>
<summary>Develop from a local clone</summary>

```bash
git clone https://github.com/ultralytics/skills
claude plugin marketplace add ./skills
claude plugin install yolo
```

</details>

<details>
<summary>Try it without installing anything</summary>

Launch a session with the plugin loaded from the repo directory, leaving your installed plugins untouched:

```bash
git clone https://github.com/ultralytics/skills && cd skills
claude --plugin-dir .
```

</details>

### Codex

```bash
codex plugin marketplace add ultralytics/skills
codex plugin add yolo@ultralytics
```

Restart Codex to use the installed skills.

<details>
<summary>Develop from a local clone</summary>

```bash
git clone https://github.com/ultralytics/skills && cd skills
codex plugin marketplace add .
codex plugin add yolo@ultralytics
```

Restart Codex after edits. To pull new versions of the GitHub source, run
`codex plugin marketplace upgrade ultralytics`, then `codex plugin add yolo@ultralytics`.

</details>

### Other agents (Cursor, Gemini CLI, ...)

```bash
npx skills add ultralytics/skills
```

<details>
<summary>Single skills, global install, manual copy</summary>

```bash
npx skills add ultralytics/skills --skill yolo-training # one skill only
npx skills add ultralytics/skills -g                    # global (~/.claude/skills/) instead of ./.claude/skills/
```

Or simply copy (or symlink) the folders under `skills/` into your agent's skills directory.

</details>

## 🛠️ Design notes

- Skills are divided by lifecycle stage / user intent, not by model family.
- Frontmatter is portable: `name` + `description` only.
- Every skill defers to the installed version at runtime: `yolo checks` (version), `yolo cfg` (valid arguments), and error messages beat any table in these files.

## 💡 Contribute

Ultralytics thrives on community collaboration, and we deeply value your contributions! Please see our [Contributing Guide](https://docs.ultralytics.com/help/contributing) for details on how to get involved. We also invite you to share your feedback through our [Survey](https://www.ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey). A huge 🙏 thank you to all our contributors!

[![Ultralytics open-source contributors](https://raw.githubusercontent.com/ultralytics/assets/main/im/image-contributors.png)](https://github.com/ultralytics/ultralytics/graphs/contributors)

## 📄 License

Ultralytics offers two licensing options to accommodate diverse needs:

- **AGPL-3.0 License**: Ideal for students, researchers, and enthusiasts passionate about open collaboration and knowledge sharing. This [OSI-approved](https://opensource.org/license/agpl-3.0) open-source license promotes transparency and community involvement. See the [LICENSE](LICENSE) file for details.
- **Enterprise License**: Designed for commercial applications, this license permits the seamless integration of Ultralytics software and AI models into commercial products and services, bypassing the copyleft requirements of AGPL-3.0. For commercial use cases, please inquire about an [Ultralytics Enterprise License](https://www.ultralytics.com/license).

## 📮 Contact

For bug reports or feature suggestions related to these skills, please use [GitHub Issues](https://github.com/ultralytics/skills/issues). For general questions, discussions, and community support, join our [Discord](https://discord.com/invite/ultralytics) server!

<br>
<div align="center">
  <a href="https://github.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="3%" alt="Ultralytics GitHub"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.linkedin.com/company/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-linkedin.png" width="3%" alt="Ultralytics LinkedIn"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://twitter.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-twitter.png" width="3%" alt="Ultralytics Twitter"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.youtube.com/ultralytics?sub_confirmation=1"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-youtube.png" width="3%" alt="Ultralytics YouTube"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.tiktok.com/@ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-tiktok.png" width="3%" alt="Ultralytics TikTok"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://ultralytics.com/bilibili"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-bilibili.png" width="3%" alt="Ultralytics BiliBili"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://discord.com/invite/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="3%" alt="Ultralytics Discord"></a>
</div>
