# YOLO label formats per task

All coordinates **normalized to [0,1]** relative to image width/height, space-separated,
one object per line, 0-based integer class indices.

| Task     | Line format                                                                      | Tokens/line |
| -------- | -------------------------------------------------------------------------------- | ----------- |
| Detect   | `class cx cy w h`                                                                | 5           |
| Segment  | `class x1 y1 x2 y2 ... xn yn` (polygon, n ≥ 3)                                   | odd, ≥ 7    |
| Pose     | `class cx cy w h px1 py1 [v1] ... pxK pyK [vK]`                                  | 5 + K×dims  |
| OBB      | `class x1 y1 x2 y2 x3 y3 x4 y4` (4 corners in order around the box)              | 9           |
| Semantic | PNG index masks in `masks_dir` (or `masks/` at root); else polygon .txt fallback | —           |
| Depth    | no .txt — paired `depth/<split>/<stem>.npy` float32 meters                       | —           |
| Classify | no label files — folder structure is the label                                   | —           |

## Details that trip people up

- **Detect**: `cx cy` is the box **center**, not top-left. Converting from COCO
  (`x_min y_min w h` in pixels) needs both the center shift and normalization.
- **Segment**: one polygon per line; multi-part instances must be merged into a single
  polygon (`convert_coco` does this). Never mix box lines and polygon lines in one file —
  a `-seg` model needs polygons.
- **Pose**: keypoint count and dims must match `kpt_shape` exactly. With dims=3,
  visibility is `0` not labeled, `1` occluded, `2` visible; unlabeled keypoints get
  `0 0 0`. Without `flip_idx` in data.yaml, fliplr/flipud augmentations are silently
  disabled (warning) — supply it to keep them; its length must equal `kpt_shape[0]` or
  training errors.
- **OBB**: 4 corners in order around the box, normalized. DOTA-converted data can have
  values slightly outside [0,1]; clamp them.
- **Depth**: `.npy` arrays, float32, same H×W as the image, metric meters (invalid
  pixels: 0 or negative).

## Symptom → cause

| Symptom                                           | Likely cause                                                                                  |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `WARNING ... no labels found` / 0-loss "training" | labels dir not named `labels`, wrong mirror path, or stem mismatch                            |
| `Label class N exceeds dataset class count`       | indices not 0-based, or `names` missing entries                                               |
| `non-normalized or out of bounds coordinates`     | pixel coords written; divide by width/height                                                  |
| Boxes offset in `train_batch*.jpg`                | top-left corner used instead of center, or x/y swapped                                        |
| mAP ≈ 0 on a task model                           | wrong label format for the task (detect boxes fed to `-seg`)                                  |
| "Dataset not found, attempting download"          | relative `path` resolving against `datasets_dir` — use absolute `path` or fix `yolo settings` |
| Val mAP suspiciously high                         | train/val leakage (same-scene frames in both splits)                                          |
| Corrupt image warnings                            | truncated/CMYK/HEIC files — re-encode to RGB JPEG/PNG                                         |
