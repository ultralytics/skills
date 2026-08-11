# Downloadable weight names (v8.4.117)

Exact `.pt` names that auto-download from `ultralytics/assets`. Use these exact strings —
do not guess or interpolate names; a wrong name raises a download error. The installed
version's authoritative list is `ultralytics.utils.downloads.GITHUB_ASSETS_NAMES`.

## YOLO detectors and task variants

Sizes: `n s m l x` unless noted. Pattern: `{family}{size}{suffix}.pt`.

| Family | Suffixes available |
|---|---|
| `yolo26` | *(detect)*, `-cls`, `-seg`, `-sem`, `-pose`, `-obb`, `-depth` |
| `yolo26{size}-objv1` | `-150`, `-seg` (Objects365-pretrained) |
| `yolo11` | *(detect)*, `-cls`, `-seg`, `-pose`, `-obb` (+ `yolo11n-grayscale.pt`) |
| `yolo12` | *(detect only)* |
| `yolov8` | *(detect)*, `-cls`, `-seg`, `-pose`, `-obb`, `-oiv7` |
| `yolov5{size}u`, `yolov5{size}6u` | detect (u = updated head) |
| `yolov3u`, `yolov3-sppu`, `yolov3-tinyu` | detect |
| `yolov9` | sizes `t s m c e`, detect |
| `yolov10` | sizes `n s m b l x`, detect |

Examples: `yolo26s-seg.pt`, `yolo26n-depth.pt`, `yolo11m-pose.pt`, `yolov8x-oiv7.pt`.

## Open-vocabulary and promptable

| Model | Names |
|---|---|
| YOLO-World | `yolov8{s,m,l,x}-world.pt`, `yolov8{s,m,l,x}-worldv2.pt` |
| YOLOE (v8-based) | `yoloe-v8{s,m,l}-seg.pt`, `yoloe-v8{s,m,l}-seg-pf.pt` |
| YOLOE (11-based) | `yoloe-11{s,m,l}-seg.pt`, `yoloe-11{s,m,l}-seg-pf.pt` |
| YOLOE (26-based) | `yoloe-26{n,s,m,l,x}-seg.pt`, `yoloe-26{n,s,m,l,x}-seg-pf.pt` |
| SAM | `sam_b.pt`, `sam_l.pt`, `mobile_sam.pt` |
| SAM 2 / 2.1 | `sam2_{t,s,b,l}.pt`, `sam2.1_{t,s,b,l}.pt` |
| FastSAM | `FastSAM-s.pt`, `FastSAM-x.pt` (capitalization matters) |

`-pf` = prompt-free YOLOE (built-in large vocabulary, no prompts needed).

## Other detectors

| Model | Names |
|---|---|
| RT-DETR | `rtdetr-l.pt`, `rtdetr-x.pt` |
| YOLO-NAS | `yolo_nas_s.pt`, `yolo_nas_m.pt`, `yolo_nas_l.pt` (inference/val only) |
