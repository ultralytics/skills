<a href="https://www.ultralytics.com"><img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320" alt="Ultralytics logo"></a>

[English](README.md) | [简体中文](README.zh-CN.md)

# 🧠 Ultralytics Agent Skills

面向 [Ultralytics Platform](https://platform.ultralytics.com)、[`ultralytics`](https://github.com/ultralytics/ultralytics) Python 包和 `yolo` CLI 的 Agent Skills。它们帮助 AI 编程智能体（Claude Code、Codex、Cursor，以及任何支持 [Agent Skills 格式](https://agentskills.io)的智能体）掌握完整的计算机视觉生命周期：数据/标注 → 训练 → 调优 → 推理/跟踪 → 导出/部署。

[![CI](https://github.com/ultralytics/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/ultralytics/skills/actions/workflows/ci.yml)
[![Ultralytics Actions](https://github.com/ultralytics/skills/actions/workflows/format.yml/badge.svg)](https://github.com/ultralytics/skills/actions/workflows/format.yml)

[![Ultralytics Discord](https://img.shields.io/discord/1089800235347353640?logo=discord&logoColor=white&label=Discord&color=blue)](https://discord.com/invite/ultralytics)
[![Ultralytics Forums](https://img.shields.io/discourse/users?server=https%3A%2F%2Fcommunity.ultralytics.com&logo=discourse&label=Forums&color=blue)](https://community.ultralytics.com)
[![Ultralytics Reddit](https://img.shields.io/reddit/subreddit-subscribers/ultralytics?style=flat&logo=reddit&logoColor=white&label=Reddit&color=blue)](https://www.reddit.com/r/ultralytics/)

## 🧩 Skills

| Skill                                              | 用途                                                                                        |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [`yolo`](skills/yolo/SKILL.md)                     | Platform 和本地工作流概览、核心 CLI/Python 语法，以及其他 Skills 的路由                     |
| [`yolo-models`](skills/yolo-models/SKILL.md)       | 选择模型系列、尺寸和任务变体：YOLO26/11/v8、YOLO-World、YOLOE、SAM、RT-DETR；准确的权重名称 |
| [`yolo-datasets`](skills/yolo-datasets/SKILL.md)   | Platform 上传/标注、data.yaml、格式、转换器、数据集拆分和验证                               |
| [`yolo-training`](skills/yolo-training/SKILL.md)   | Platform 云端/远程训练、本地训练/验证、参数、结果和故障排除                                 |
| [`yolo-tuning`](skills/yolo-tuning/SKILL.md)       | Platform 实验对比、系统化改进方法、`model.tune()` 和 Ray Tune                               |
| [`yolo-inference`](skills/yolo-inference/SKILL.md) | Platform Predict/端点、本地推理、Results API、跟踪和 Solutions                              |
| [`yolo-export`](skills/yolo-export/SKILL.md)       | Platform/本地 ONNX/TensorRT/CoreML/OpenVINO/LiteRT/NPU 导出、量化和基准测试                 |

每个 Skill 都包含一个 `SKILL.md`（操作步骤、决策表和注意事项）以及 Codex/ChatGPT 展示元数据；必要时还会包含配套参考文件，用于保存随版本变化的目录信息（权重名称、参数表、导出格式矩阵）。软件包信息基于 `ultralytics` v8.4.119；Platform 流程基于当前的 [Platform 文档](https://docs.ultralytics.com/platform)。

## 📦 安装

在 [**Python>=3.8**](https://www.python.org/) 环境中安装 `ultralytics` 包及其所有[依赖项](https://github.com/ultralytics/ultralytics/blob/main/pyproject.toml)，并确保安装 [**PyTorch>=1.8**](https://pytorch.org/get-started/locally/)。

[![PyPI - Version](https://img.shields.io/pypi/v/ultralytics?logo=pypi&logoColor=white)](https://pypi.org/project/ultralytics/) [![Ultralytics Downloads](https://static.pepy.tech/badge/ultralytics)](https://clickpy.clickhouse.com/dashboard/ultralytics) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ultralytics?logo=python&logoColor=gold)](https://pypi.org/project/ultralytics/)

```bash
pip install ultralytics
```

如需其他安装方式，包括 [Conda](https://anaconda.org/conda-forge/ultralytics)、[Docker](https://hub.docker.com/r/ultralytics/ultralytics) 和通过 Git 从源码构建，请参阅[快速入门指南](https://docs.ultralytics.com/quickstart)。

[![Conda Version](https://img.shields.io/conda/vn/conda-forge/ultralytics?logo=condaforge)](https://anaconda.org/conda-forge/ultralytics) [![Docker Image Version](https://img.shields.io/docker/v/ultralytics/ultralytics?sort=semver&logo=docker)](https://hub.docker.com/r/ultralytics/ultralytics) [![Ultralytics Docker Pulls](https://img.shields.io/docker/pulls/ultralytics/ultralytics?logo=docker)](https://hub.docker.com/r/ultralytics/ultralytics)

### Claude Code

```bash
claude plugin marketplace add ultralytics/skills
claude plugin install yolo@ultralytics
```

<details>
<summary>从本地克隆仓库进行开发</summary>

```bash
git clone https://github.com/ultralytics/skills
claude plugin marketplace add ./skills
claude plugin install yolo@ultralytics
```

</details>

<details>
<summary>无需安装即可试用</summary>

在仓库目录中启动加载该插件的会话，不影响已安装的插件：

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

重启 Codex 后即可使用已安装的 Skills。

<details>
<summary>从本地克隆仓库进行开发</summary>

```bash
git clone https://github.com/ultralytics/skills && cd skills
codex plugin marketplace add .
codex plugin add yolo@ultralytics
```

编辑后请重启 Codex。要拉取 GitHub 源的新版本，请运行
`codex plugin marketplace upgrade ultralytics`，然后运行 `codex plugin add yolo@ultralytics`。

</details>

### 其他智能体（Cursor、Gemini CLI 等）

```bash
npx skills add ultralytics/skills
```

<details>
<summary>安装单个 Skill、全局安装或手动复制</summary>

```bash
npx skills add ultralytics/skills --skill yolo-training # 仅安装一个 Skill
npx skills add ultralytics/skills -g                    # 全局安装到 ~/.claude/skills/，而非 ./.claude/skills/
```

也可以直接将 `skills/` 下的文件夹复制（或创建符号链接）到智能体的 Skills 目录中。

</details>

## 🛠️ 设计说明

- Skills 按生命周期阶段和用户意图划分，而不是按模型系列划分。
- Frontmatter 具有可移植性，仅包含 `name` 和 `description`。
- 每个生命周期 Skill 都会在适用时同时介绍 Platform UI 与本地 Python/CLI 路径。
- 每个 Skill 都以安装版本的运行时信息为准：`yolo checks`（版本）、`yolo cfg`（有效参数）和错误消息优先于这些文件中的任何表格。

## 💡 贡献

Ultralytics 因社区协作而不断发展，我们非常重视你的贡献！请参阅[贡献指南](https://docs.ultralytics.com/help/contributing)，了解如何参与。也欢迎你通过[问卷调查](https://www.ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey)分享反馈。衷心感谢所有贡献者！🙏

[![Ultralytics 开源贡献者](https://raw.githubusercontent.com/ultralytics/assets/main/im/image-contributors.png)](https://github.com/ultralytics/ultralytics/graphs/contributors)

## 📄 许可证

Ultralytics 提供两种许可证，以满足不同需求：

- **AGPL-3.0 许可证**：适合热衷于开放协作和知识共享的学生、研究人员及爱好者。该 [OSI 批准](https://opensource.org/license/agpl-3.0)的开源许可证倡导透明与社区协作。详情请参阅 [LICENSE](LICENSE) 文件。
- **企业许可证**：面向商业应用，允许在商业产品和服务中集成 Ultralytics 软件和 AI 模型，而无需遵守 AGPL-3.0 的 copyleft 要求。如需商业使用，请咨询 [Ultralytics 企业许可证](https://www.ultralytics.com/license)。

## 📮 联系方式

如需报告与这些 Skills 相关的错误或提出功能建议，请使用 [GitHub Issues](https://github.com/ultralytics/skills/issues)。如有一般问题、讨论或社区支持需求，请加入我们的 [Discord](https://discord.com/invite/ultralytics)！

<br>
<div align="center">
  <a href="https://github.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="3%" alt="Ultralytics GitHub"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="间隔">
  <a href="https://www.linkedin.com/company/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-linkedin.png" width="3%" alt="Ultralytics LinkedIn"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="间隔">
  <a href="https://twitter.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-twitter.png" width="3%" alt="Ultralytics Twitter"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="间隔">
  <a href="https://www.youtube.com/ultralytics?sub_confirmation=1"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-youtube.png" width="3%" alt="Ultralytics YouTube"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="间隔">
  <a href="https://www.tiktok.com/@ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-tiktok.png" width="3%" alt="Ultralytics TikTok"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="间隔">
  <a href="https://www.ultralytics.com/bilibili"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-bilibili.png" width="3%" alt="Ultralytics BiliBili"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="间隔">
  <a href="https://discord.com/invite/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="3%" alt="Ultralytics Discord"></a>
</div>
