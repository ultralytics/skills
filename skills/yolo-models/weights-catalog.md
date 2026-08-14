# Model asset names (v8.4.119)

`ultralytics.utils.downloads.GITHUB_ASSETS_NAMES` is the package-known fast-path set, not
an exhaustive release catalog. The downloader also queries configured live release assets
for other names. Use the exact names and patterns below and official model/task docs; do not
guess or interpolate them. SAM 3 is the noted gated exception.

## YOLO detectors and task variants

Sizes: `n s m l x` unless noted. Pattern: `{family}{size}{suffix}.pt`.

| Family                                   | Suffixes available                                                     |
| ---------------------------------------- | ---------------------------------------------------------------------- |
| `yolo26`                                 | _(detect)_, `-cls`, `-seg`, `-sem`, `-pose`, `-obb`, `-depth`          |
| `yolo26{size}-objv1`                     | `-150`, `-seg` (Objects365-pretrained)                                 |
| `yolo11`                                 | _(detect)_, `-cls`, `-seg`, `-pose`, `-obb` (+ `yolo11n-grayscale.pt`) |
| `yolo12`                                 | _(detect only)_                                                        |
| `yolov8`                                 | _(detect)_, `-cls`, `-seg`, `-pose`, `-obb`, `-oiv7`                   |
| `yolov5{size}u`, `yolov5{size}6u`        | detect (u = updated head)                                              |
| `yolov3u`, `yolov3-sppu`, `yolov3-tinyu` | detect                                                                 |
| `yolov9`                                 | sizes `t s m c e`, detect                                              |
| `yolov10`                                | sizes `n s m b l x`, detect                                            |

Examples: `yolo26s-seg.pt`, `yolo26n-depth.pt`, `yolo11m-pose.pt`, `yolov8x-oiv7.pt`.

## Specialized official assets outside the fast-path set

| Use                    | Names                              | Acquisition                       |
| ---------------------- | ---------------------------------- | --------------------------------- |
| ADE20K semantic models | `yolo26{n,s,m,l,x}-sem-ade20k.pt`  | auto-download from release assets |
| Tracking ReID encoders | `yolo26{n,s,m,l,x}-reid.{pt,onnx}` | auto-download when tracker loads  |

## Open-vocabulary and promptable

| Model            | Names                                                         |
| ---------------- | ------------------------------------------------------------- |
| YOLO-World       | `yolov8{s,m,l,x}-world.pt`, `yolov8{s,m,l,x}-worldv2.pt`      |
| YOLOE (v8-based) | `yoloe-v8{s,m,l}-seg.pt`, `yoloe-v8{s,m,l}-seg-pf.pt`         |
| YOLOE (11-based) | `yoloe-11{s,m,l}-seg.pt`, `yoloe-11{s,m,l}-seg-pf.pt`         |
| YOLOE (26-based) | `yoloe-26{n,s,m,l,x}-seg.pt`, `yoloe-26{n,s,m,l,x}-seg-pf.pt` |
| SAM              | `sam_b.pt`, `sam_l.pt`, `mobile_sam.pt`                       |
| SAM 2 / 2.1      | `sam2_{t,s,b,l}.pt`, `sam2.1_{t,s,b,l}.pt`                    |
| SAM 3            | `sam3.pt` (request access and download from Hugging Face)     |
| FastSAM          | `FastSAM-s.pt`, `FastSAM-x.pt` (capitalization matters)       |

`-pf` = prompt-free YOLOE (built-in large vocabulary, no prompts needed).

SAM 3 does not auto-download. Request access at
`https://huggingface.co/facebook/sam3`, download `sam3.pt` after approval, and pass its
local path to `SAM()`.

## Other detectors

| Model    | Names                                                                  |
| -------- | ---------------------------------------------------------------------- |
| RT-DETR  | `rtdetr-l.pt`, `rtdetr-x.pt`                                           |
| YOLO-NAS | `yolo_nas_s.pt`, `yolo_nas_m.pt`, `yolo_nas_l.pt` (inference/val only) |
