---
name: yolo
description: >
  Core guide for Ultralytics YOLO — the yolo CLI and the ultralytics Python package:
  command grammar, tasks, modes, configuration, and how the full computer-vision
  lifecycle fits together (data → train → val → predict/track → export). Use for ANY
  task involving the ultralytics package, the yolo CLI, YOLO model weights (.pt),
  or the detect / segment / semantic / depth / classify / pose / OBB vision lifecycle.
---

# Ultralytics YOLO

One API, two surfaces. The CLI grammar is `yolo TASK MODE arg=value ...`; Python mirrors
it with the same argument names:

```bash
yolo detect train data=data.yaml model=yolo26n.pt epochs=100 imgsz=640
```

```python
from ultralytics import YOLO
model = YOLO("yolo26n.pt")
model.train(data="data.yaml", epochs=100, imgsz=640)
```

- TASK ∈ `detect` `segment` `semantic` `depth` `classify` `pose` `obb` — usually inferred
  from the weights, so it can be omitted.
- MODE ∈ `train` `val` `predict` `track` `export` `benchmark`.
- Install/upgrade: `pip install -U ultralytics`. Environment check: `yolo checks`.

## Whole lifecycle in five commands

```bash
yolo detect train data=data.yaml model=yolo26n.pt epochs=100   # → runs/detect/train/weights/best.pt
yolo val model=best.pt data=data.yaml                           # mAP, per-class metrics
yolo predict model=best.pt source=video.mp4 save=True           # any source: image/dir/URL/RTSP/webcam
yolo track model=best.pt source=video.mp4                       # + persistent object IDs
yolo export model=best.pt format=onnx                           # exported model loads back into YOLO()
```

## Route before coding

Read the skill for the stage you're working on BEFORE writing code — each contains exact
formats, argument tables with defaults, recipes, and symptom→fix tables. A request
spanning stages ("train and deploy") → read each relevant skill.

| Working on | Skill |
|---|---|
| choosing a model family/size/task, YOLO26 vs YOLO11, YOLO-World/YOLOE, SAM, RT-DETR | `yolo-models` |
| data.yaml, labels, annotation conversion, auto-labeling, dataset analysis/errors, splits | `yolo-datasets` |
| training, fine-tuning, hyperparameters, augmentation, OOM / NaN / low mAP, reading runs | `yolo-training` |
| hyperparameter tuning, Ray Tune, systematic model improvement, "autotraining" | `yolo-tuning` |
| predict on images/video/streams, Results API, tracking IDs, counting/heatmaps/Solutions | `yolo-inference` |
| ONNX / TensorRT / CoreML / OpenVINO / LiteRT / NCNN / NPUs, quantization, benchmarking | `yolo-export` |

## CLI specifics

Special commands (no TASK/MODE):

```bash
yolo help                 # full syntax reference
yolo checks               # env report: version, torch, CUDA, disk — run when anything is weird
yolo version
yolo settings             # view; `yolo settings key=value` to set; `yolo settings reset`
                          # keys incl. datasets_dir, runs_dir, wandb, mlflow, tensorboard, ...
yolo cfg                  # print every default argument (the ground truth for arg names)
yolo copy-cfg             # copy default.yaml → default_copy.yaml to customize, use with cfg=
yolo solutions help       # prebuilt apps: count, heatmap, speed, ... (see yolo-inference)
```

Parsing rules that matter:

- Args are `key=value`, no `--` flags. A leading `--` and trailing commas are stripped
  with a warning; spaces around `=` are merged.
- A bare boolean arg sets it True: `yolo predict ... show` ≡ `show=True`.
- `cfg=custom.yaml` replaces ALL defaults with your file (make one via `yolo copy-cfg`).
- Missing args are auto-filled with warnings (sample source, task-default data/model,
  `format=torchscript`).
- Model stem selects the architecture: `rtdetr-*` → RT-DETR, `sam_*`/`sam2*` → SAM,
  `FastSAM-*` → FastSAM, `yoloe-*`/`*-world*` → promptable YOLO (accepts
  `classes="person, bus"`), everything else → YOLO.

## Global directives

1. **Validate the dataset before training** — run the checks in `yolo-datasets`, then a
   1-epoch smoke test and eyeball `runs/<task>/train/train_batch0.jpg`: boxes must sit on
   objects. Bad labels are the #1 cause of "training worked, mAP is 0".
2. **Always fine-tune from pretrained `.pt`** — never `pretrained=False`, never a YAML
   architecture from scratch, unless the user is explicitly doing research.
3. **`stream=True` for videos/streams** in Python predict/track — the default list mode
   OOMs on long videos.
4. **Use `best.pt`** (not `last.pt`) from `runs/<task>/<name>/weights/` after training.
5. **After export, verify parity**: `yolo val` the exported artifact against the `.pt`
   baseline.
6. **Prefer built-ins over custom code**: dataset converters and checkers
   (`ultralytics.data`), trackers, and Solutions modules replace whole categories of
   hand-written glue.
7. **Trust the installed version over memory** — if an argument is rejected
   (`yolo checks` shows the version), the API moved: `yolo cfg` and the error text list
   valid arguments; prefer those over any table in these skills.
