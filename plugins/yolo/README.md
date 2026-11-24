# Ultralytics YOLO plugin

Agent skills for [Ultralytics YOLO](https://docs.ultralytics.com) and [Ultralytics Platform](https://docs.ultralytics.com/platform): model selection, datasets and annotation, training, tuning, inference, export, and deployment. The same skills serve Claude Code and Codex. The skill list, Codex installation, and design notes are in the [repository README](https://github.com/ultralytics/skills).

Install in Claude Code:

```
/plugin install yolo --marketplace ultralytics/skills
```

## What it runs, sends, and fetches

The plugin ships only Markdown and YAML instructions, with no hooks, MCP servers, or scripts, so nothing runs when it loads. Following the skills, your agent runs the `yolo` and `ul` CLIs or the `ultralytics` Python package in your own environment. Those commands can:

- **Download** Python packages, model weights, datasets, and the public Platform API schema.
- **Upload to [Ultralytics Platform](https://platform.ultralytics.com)** with the Platform [API key](https://docs.ultralytics.com/platform/account/api-keys) you set up yourself: the files you pass to `ul cloud` commands, and the metrics and weights of training runs started with `project=` while you're signed in.
- **Send images to your own deployment** when you call a Platform endpoint's `/predict`.
- **Log to experiment trackers** such as Weights & Biases, MLflow, Comet, or ClearML, only when you have installed or enabled them.
- **Send telemetry**: the `ultralytics` package sends anonymous usage analytics, and crash reports when `sentry_sdk` is installed. `yolo settings sync=False` turns both off.
