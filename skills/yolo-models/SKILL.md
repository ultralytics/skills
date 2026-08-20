---
name: yolo-models
description: >
  Use when choosing or comparing Ultralytics models in Platform or code — picking a
  model family (YOLO26/YOLO11/YOLOv8, YOLO-World, YOLOE, SAM/SAM2/FastSAM, RT-DETR,
  YOLO-NAS), size (n/s/m/l/x), task variant (-seg, -sem, -cls, -pose, -obb, -depth),
  pretrained checkpoint, open-vocabulary or promptable detection/segmentation, or custom
  architecture. Covers Platform Explore/model flows, weight names and availability,
  selection guidance, and family trade-offs.
---

# Choosing an Ultralytics model

**Default recommendation: YOLO26, pretrained.** Latest generation, NMS-free end-to-end
(fastest CPU inference, simplest deployment). Use YOLO11/YOLOv8 only to match an existing
codebase or a deployment target that doesn't support YOLO26 yet. Most official weights
auto-download on first use; `sam3.pt` requires manual access and download.

## Choose in Platform

For the quickest no-code start, open [Platform Explore](https://platform.ultralytics.com/explore),
select **Projects**, clone the official `@ultralytics` project for the model family, then
train one of its pretrained models on your dataset. The **New Model** dialog filters base
models to the selected dataset task and offers official models plus your own completed
checkpoints for further fine-tuning.

Use a Platform model page to inspect metrics, test it in **Predict**, export it, deploy it,
clone it into another project, or download its `.pt` weights for the Python/CLI workflows
below. See [Platform Models](https://docs.ultralytics.com/platform/train/models) and
[Explore](https://docs.ultralytics.com/platform/explore).

## Model = family + size + task suffix

`yolo26` + `n/s/m/l/x` + task suffix → `yolo26s-seg.pt`

| Size | COCO mAP50-95 | Params | T4 TensorRT | Pick for                                   |
| ---- | ------------- | ------ | ----------- | ------------------------------------------ |
| n    | 40.9          | 2.4M   | ~1.7 ms     | edge/mobile, CPU realtime, first prototype |
| s    | 48.6          | 9.5M   | ~2.5 ms     | balanced default for most projects         |
| m    | 53.1          | 20.4M  | ~4.7 ms     | GPU server, accuracy matters               |
| l    | 55.0          | 24.8M  | ~6.2 ms     | accuracy-critical, ample GPU               |
| x    | 57.5          | 55.7M  | ~11.8 ms    | max accuracy, offline/batch                |

Strategy: prototype on `n` to validate the pipeline cheaply, then scale up until accuracy
stops paying for the latency. A bigger model never fixes bad labels.

| Suffix   | Task                            | Output               |
| -------- | ------------------------------- | -------------------- |
| _(none)_ | detect                          | boxes                |
| `-seg`   | instance segmentation           | polygons + boxes     |
| `-sem`   | semantic segmentation (YOLO26+) | per-pixel class mask |
| `-depth` | monocular depth (YOLO26+)       | depth map            |
| `-cls`   | classification                  | class probabilities  |
| `-pose`  | pose/keypoints                  | keypoints + boxes    |
| `-obb`   | oriented boxes                  | rotated boxes        |

Notes on the newer tasks:

- **semantic** (`-sem`): dataset uses PNG masks via `masks_dir` (default `masks/`) or
  polygon labels; metric is mIoU.
- **depth** (`-depth`): labels are float32 `.npy` depth maps; metric is delta1. Exposes a
  unique `model.calibrate(data=...)` step that fits a metric-scale correction, then
  `model.save(...)` to persist it.

## Family cheat sheet

| Family                                | Class                           | When                                                                                                                                                                                                       |
| ------------------------------------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| YOLO26 / YOLO11 / YOLO12 / YOLOv8–v10 | `YOLO("yolo26n.pt")`            | standard closed-set tasks; default choice                                                                                                                                                                  |
| YOLO-World                            | `YOLOWorld("yolov8s-world.pt")` | zero-shot detection of arbitrary text classes; `model.set_classes(["person", "helmet"])`                                                                                                                   |
| YOLOE                                 | `YOLOE("yoloe-26s-seg.pt")`     | open-vocabulary detect+segment via text or visual prompts; `set_classes(names, embeddings)`, visual prompts via `predict(..., visual_prompts={"bboxes": ..., "cls": ...})`; `-pf` variants are prompt-free |
| SAM / SAM2 / SAM3 / MobileSAM         | `SAM("sam_b.pt")`               | promptable segmentation: `predict(source, bboxes=... / points=... / labels=...)`; SAM2/3 add video and semantic variants                                                                                   |
| FastSAM                               | `FastSAM("FastSAM-s.pt")`       | CNN-based segment-anything, much faster than SAM                                                                                                                                                           |
| RT-DETR                               | `RTDETR("rtdetr-l.pt")`         | transformer detector, strong accuracy on GPU                                                                                                                                                               |
| YOLO-NAS                              | `NAS("yolo_nas_s.pt")`          | inference/val only, no training                                                                                                                                                                            |

All classes share the same `Model` API (`train/val/predict/track/export/...`) —
everything in the other yolo-\* skills applies to them, with the exceptions noted above.

Open-vocabulary decision: need arbitrary classes at inference with no training →
YOLO-World (detect) or YOLOE (detect+segment, also visual prompts). Need pixel-precise
masks from clicks/boxes → SAM family. Need a trained model for a fixed class list →
plain YOLO26 fine-tune (faster and more accurate on that closed set).

## Architecture YAMLs (custom models)

`ultralytics/cfg/models/` ships editable architecture definitions (`yolo26.yaml`,
`yolo11.yaml`, `yolov8.yaml`, scale variants `-p2` for small objects, `-p6` for large
imgsz, `-ghost`, etc.). Loading `YOLO("yolo26n.yaml")` builds from scratch — scale is
picked from the letter in the stem. To customize the architecture but keep pretrained
weights where layers match:

```python
model = YOLO("yolo26n.yaml").load("yolo26n.pt")  # transfer matching weights
```

Only go here for research/unusual constraints; for normal work fine-tune the stock `.pt`.

## Related pages

- `weights-catalog.md` (this folder) — read for package-known weight patterns and
  specialized official assets. Do not guess weight names.

## Verify against the installed version

Model availability moves fast. This prints the installed package's known fast-path set;
read `weights-catalog.md` before treating an unlisted official asset as invalid:

```bash
python -c "from ultralytics.utils.downloads import GITHUB_ASSETS_NAMES; print(*sorted(GITHUB_ASSETS_NAMES), sep='\\n')"
```

If a weight 404s or a class import fails, check `yolo checks` and trust the
installed-version error.
