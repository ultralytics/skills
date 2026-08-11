---
name: yolo-inference
description: >
  Use when running Ultralytics YOLO models on images, video, webcams, or streams —
  model.predict() / yolo predict, extracting boxes/masks/keypoints from the Results
  API, object tracking with persistent IDs (model.track), writing annotated video, and
  prebuilt Solutions (object counting, heatmaps, speed estimation, queues, parking).
  For making inference faster via ONNX/TensorRT/quantization, see yolo-export.
---

# Inference, Results API & tracking

## Quickstart

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")  # or your runs/detect/train/weights/best.pt
results = model("image.jpg")  # list[Results], one per image
results[0].show()
```

```bash
yolo predict model=yolo26n.pt source="image.jpg" save=True
```

**The one rule for video/streams: `stream=True`.** The default builds a list of ALL
results in RAM — OOM on long videos. `stream=True` returns a generator:

```python
for r in model("video.mp4", stream=True):
    ...
```

## Sources

Accepted directly: image/video path, directory, glob, URL, webcam index (`0`),
RTSP/RTMP/HTTP streams, YouTube URL (needs `pytubefix`), PIL image, numpy array (assumed
BGR), torch tensor, or a list of these. `vid_stride=N` processes every Nth frame.

## Arguments that matter

| Arg            | Default | Notes                                                       |
| -------------- | ------- | ----------------------------------------------------------- |
| `conf`         | 0.25    | lower → more recall + more false positives                  |
| `iou`          | 0.7     | NMS threshold; lower to remove duplicate boxes              |
| `imgsz`        | 640     | match training imgsz for best accuracy                      |
| `classes`      | None    | keep only these ids, e.g. `classes=[0]`                     |
| `max_det`      | 300     | raise for dense scenes                                      |
| `quantize`     | None    | `16` = FP16 on GPU ≈ 2× faster (replaces deprecated `half`) |
| `batch`        | 1       | >1 speeds up folders/videos with `stream=True`              |
| `retina_masks` | False   | full-resolution masks (slower, crisper)                     |
| `augment`      | False   | test-time augmentation: +accuracy, ~3× slower               |
| `verbose`      | True    | False in loops to silence per-frame logs                    |

Saving/drawing: `save`, `save_txt`, `save_conf`, `save_crop`, `show`, `line_width` →
`runs/<task>/predict*/`.

## Results API

Each `Results` has the task's payload — `.boxes`, `.masks`, `.keypoints`, `.probs`
(classify), `.obb`, `.semantic_mask`, `.depth` — plus `.names` (id→name), `.orig_img`
(BGR), `.speed`, and methods `.plot()`, `.show()`, `.save()`, `.save_txt()`,
`.save_crop()`, `.summary()`, and exports `to_df()` / `to_csv()` / `to_json()` (these
three only).

```python
r = results[0]
r.boxes.xyxy / .xywh / .xyxyn / .xywhn   # (N,4) boxes, pixel / normalized
r.boxes.conf, r.boxes.cls, r.boxes.id    # confidence, class ids, track ids (track mode)
r.masks.xy                                # list of (K,2) pixel polygons per instance
r.keypoints.xy, r.keypoints.conf          # (N,K,2), (N,K)
r.probs.top1, r.probs.top1conf            # classify; r.names[r.probs.top1] → label
r.obb.xyxyxyxy, r.obb.xywhr               # oriented boxes

from collections import Counter
counts = Counter(r.names[int(c)] for c in r.boxes.cls)   # count per class
```

`model.embed("image.jpg")` returns feature vectors (similarity search, clustering).

## Tracking (persistent IDs across frames)

```python
for r in model.track("video.mp4", stream=True):
    ids = r.boxes.id  # tensor of track ids, or None

# Frame-by-frame loop with your own capture: persist=True is REQUIRED
r = model.track(frame, persist=True)[0]  # else the tracker resets every frame
```

- Six trackers, selected with `tracker=`: **`tracktrack.yaml` (default)**,
  `botsort.yaml`, `bytetrack.yaml`, `ocsort.yaml`, `deepocsort.yaml`,
  `fasttrack.yaml`. ByteTrack is lightest; BoT-SORT/TrackTrack/DeepOCSORT support
  ReID (`with_reid: True`) and camera-motion compensation (`gmc_method`).
- Custom behavior: copy the YAML from `ultralytics/cfg/trackers/`, tweak
  (`track_buffer` = frames a lost track survives, `track_high_thresh`), pass your path.
- Tracking accepts all predict args. Always guard `r.boxes.id is not None`.

## Annotated-video writing pattern

```python
import cv2

cap = cv2.VideoCapture("in.mp4")
w, h, fps = (int(cap.get(p)) for p in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
out = cv2.VideoWriter("out.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
for r in model.track("in.mp4", stream=True):
    out.write(r.plot())  # .plot() returns annotated BGR frame
cap.release()
out.release()
```

## Performance checklist (in payoff order)

1. GPU + `quantize=16`.
2. Export to TensorRT/OpenVINO/CoreML — 2–5× (see yolo-export; exports load straight
   back into `YOLO()`).
3. Use a smaller model or `imgsz`.
4. Set `batch>1` for offline folders; use `vid_stride` when every frame isn't needed.
5. Set `verbose=False`; skip `.plot()` when only coordinates are needed.
6. Use one `YOLO()` instance per thread — never share across threads.

## Troubleshooting

| Symptom                          | Cause / fix                                                                   |
| -------------------------------- | ----------------------------------------------------------------------------- |
| No detections on visible objects | `conf` too high; wrong weights; imgsz far from training size                  |
| Boxes offset                     | you pre-resized manually — pass the raw image, preprocessing is internal      |
| Wrong colors in saved crops      | Results arrays are BGR; `cv2.cvtColor(..., COLOR_BGR2RGB)` for PIL/matplotlib |
| RAM climbs on video              | missing `stream=True`                                                         |
| `boxes.id is None` crash         | guard for None; `persist=True` in manual loops                                |
| Duplicate boxes                  | lower `iou`; `agnostic_nms=True` for cross-class dupes                        |
| Caps at 300 objects              | raise `max_det`                                                               |
| Slow first inference             | warmup — benchmark from the second call                                       |

## Related pages

- `solutions.md` (this folder) — read BEFORE hand-rolling counting, heatmaps, speed
  estimation, zone logic, queues, parking, workout counting, or privacy blurring: a
  prebuilt Solution almost certainly exists.

If the installed version rejects an argument, trust the error text and `yolo cfg` over
this file.
