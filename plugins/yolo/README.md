# Ultralytics YOLO plugin

Agent skills for [Ultralytics YOLO](https://docs.ultralytics.com) and [Ultralytics Platform](https://docs.ultralytics.com/platform): model selection, datasets and annotation, training, tuning, inference, export, and deployment. One `skills/` folder serves both Claude Code (`.claude-plugin/plugin.json`) and Codex (`.codex-plugin/plugin.json`). The skill list, Codex installation, and design notes are in the [repository README](https://github.com/ultralytics/skills).

Install in Claude Code:

```
/plugin install yolo --marketplace ultralytics/skills
```

## What it runs, sends, and fetches

The plugin ships only Markdown and YAML instructions, with no hooks, MCP servers, or scripts. Following them, your agent runs the `yolo` and `ul` CLIs or the `ultralytics` Python package from your own environment. Those tools download model weights and datasets. `ul cloud` commands, `ul://` datasets, and training with `project=` while you're signed in call the Ultralytics Platform API with your Platform [API key](https://docs.ultralytics.com/platform/account/api-keys), which you set up yourself.
