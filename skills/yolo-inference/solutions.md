# Solutions — prebuilt vision apps

Solutions wrap model + tracker + geometry + drawing into one callable. If the request
matches a module below, use it — don't hand-roll track-ID bookkeeping and line-crossing
math.

## Universal pattern

Construct once → call per frame → returns `SolutionResults` with `.plot_im` (annotated
frame) plus solution-specific fields.

```python
import cv2
from ultralytics import solutions

counter = solutions.ObjectCounter(
    model="yolo26n.pt",
    region=[(20, 400), (1080, 400)],  # 2 points = line (counts crossings, in/out);
    classes=[2, 3, 5, 7],  # 3+ points = polygon (counts entries/presence)
    show=False,
)
cap = cv2.VideoCapture("traffic.mp4")
while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break
    results = counter(frame)
    # results.plot_im, counter.in_count, counter.out_count, counter.classwise_count
```

Common constructor args (`SolutionConfig`): `model`, `region` (pixel coords in the
frame), `classes`, `conf`, `iou`, `tracker` (default `botsort.yaml` here), `device`,
`show`, `line_width`, `imgsz`, `quantize` (`half` is deprecated). Invalid keys raise
ValueError — the message lists valid ones.

## Catalog (CLI name → class)

| Need                                  | CLI         | Class                  | Notes                                                      |
| ------------------------------------- | ----------- | ---------------------- | ---------------------------------------------------------- |
| Count line-crossings / region entries | `count`     | `ObjectCounter`        | in/out + per-class                                         |
| Count per multiple named zones        | `region`    | `RegionCounter`        |                                                            |
| Track only inside a zone              | `trackzone` | `TrackZone`            |                                                            |
| Movement heatmap                      | `heatmap`   | `Heatmap`              | `colormap=cv2.COLORMAP_JET` etc.                           |
| Speed estimation                      | `speed`     | `SpeedEstimator`       | `meter_per_pixel` for physical units; estimate, not radar  |
| Queue length monitoring               | `queue`     | `QueueManager`         | polygon region                                             |
| Parking occupancy                     | `parking`   | `ParkingManagement`    | slots via `ParkingPtsSelection()` GUI → JSON               |
| Workout rep counting                  | `workout`   | `AIGym`                | pose model + `kpts=[6,8,10]` joint indices                 |
| Alert on detections                   | `security`  | `SecurityAlarm`        | `authenticate(from_email, password, to_email)` then emails |
| Privacy blur                          | `blur`      | `ObjectBlurrer`        | `blur_ratio`                                               |
| Crop detections to files              | `crop`      | `ObjectCropper`        | `crop_dir`                                                 |
| Segmentation overlay + tracking       | `isegment`  | `InstanceSegmentation` | needs `-seg` model                                         |
| Point-to-object mapping               | `visioneye` | `VisionEye`            | `vision_point`                                             |
| Live charts of counts                 | `analytics` | `Analytics`            | line/bar/pie; call takes `(im0, frame_number)`             |
| Distance between two tracks           | —           | `DistanceCalculation`  | interactive                                                |
| Semantic image search                 | —           | `VisualAISearch`       | natural-language search over a folder                      |
| Browser demo, zero code               | `inference` | `Inference`            | Streamlit UI                                               |

CLI: `yolo solutions SOLUTION arg=value...`, e.g.

```bash
yolo solutions count source=video.mp4 region="[(20,400),(1080,400)]"
yolo solutions heatmap source=video.mp4
yolo solutions inference # Streamlit app (note: `yolo streamlit-predict` does NOT exist)
yolo solutions help
```

Output video lands in `runs/solutions/exp/`. An invalid solution name falls back to
`count` (with a logged warning) — spell exactly.

## Notes

- Region coordinates are **pixels in the frame** — grab one frame, note the resolution,
  then define regions. Double counting on a line usually means it sits where objects
  jitter; move it perpendicular to travel direction.
- Solutions accept any custom-trained `best.pt` matching their task type.
- Read state from attributes (`in_count`, `classwise_count`, …), not by parsing the
  drawn frame; `dir(obj)` lists what a module exposes.
- Enumerate what the installed version ships:
  `python -c "from ultralytics import solutions; print([s for s in dir(solutions) if s[0].isupper()])"`
- **When NOT to use**: bespoke multi-stage pipelines (detect → classify crop → OCR),
  3D/homography geometry, event logic no module models — build on `model.track()` +
  Results API instead (see SKILL.md).
