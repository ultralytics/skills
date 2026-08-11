---
name: yolo-export
description: >
  Use when exporting or deploying Ultralytics YOLO models — yolo export /
  model.export() to ONNX, TensorRT engine, CoreML, OpenVINO, LiteRT/TFLite, NCNN,
  ExecuTorch or NPU formats (RKNN, QNN, Hailo, Ascend, IMX, Axelera, DeepX), FP16/INT8
  quantization, benchmarking formats, and consuming exports outside Python. For plain
  Python/CLI inference with .pt weights, see yolo-inference.
---

# Export, quantization & deployment

## Quickstart

```python
from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")
path = model.export(format="onnx")  # returns the exported file/dir path
```

```bash
yolo export model=best.pt format=onnx
```

Exports load straight back into `YOLO()` for predict/val — same API:

```python
model = YOLO("best.onnx")  # or best.engine, best_openvino_model/, ...
```

## Choose format by target hardware

| Target                                                   | `format=`                                                         | Why                                                                                                       |
| -------------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| NVIDIA GPU / Jetson                                      | `engine` (TensorRT)                                               | fastest on NVIDIA; **build on the deployment device** — engines are not portable across GPUs/TRT versions |
| Intel CPU/iGPU/NPU                                       | `openvino`                                                        | ~3× CPU speedup                                                                                           |
| Apple iOS/macOS                                          | `coreml`                                                          | Neural Engine                                                                                             |
| Android                                                  | `litert` (renamed from `tflite`) or `ncnn`                        | NCNN strong on ARM                                                                                        |
| Raspberry Pi                                             | `ncnn`                                                            | best ARM CPU latency                                                                                      |
| PyTorch Edge                                             | `executorch`                                                      |                                                                                                           |
| Cross-platform / unsure                                  | `onnx`                                                            | runs everywhere; start here, specialize when latency demands                                              |
| NPUs (Rockchip/Qualcomm/Hailo/Huawei/Sony/Axelera/DeepX) | `rknn` / `qnn` / `hailo` / `ascend` / `imx` / `axelera` / `deepx` | `name=` selects the exact chip for rknn/qnn/hailo/ascend                                                  |

Full 20-format matrix with per-format supported args: `format-matrix.md` (this folder).

## Key arguments

| Arg         | Default | Notes                                                                                                                                                                                                                   |
| ----------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `imgsz`     | 640     | baked into most formats — match what you'll feed it                                                                                                                                                                     |
| `quantize`  | None    | **the** precision arg (replaces deprecated `half`/`int8`): `16`/`fp16` FP16 (~2× smaller/faster, free lunch on GPU/NPU); `8`/`int8`/`w8a8` INT8 (~4× smaller, costs ~1–3 mAP, needs calibration); also `w8a16`, `w8a32` |
| `data`      | None    | calibration dataset for INT8 — a few hundred varied val images; defaults to the task's calibration set (coco128 etc.) if omitted                                                                                        |
| `dynamic`   | False   | variable input size/batch (ONNX/TensorRT) — costs some speed                                                                                                                                                            |
| `batch`     | 1       | max batch baked into the export                                                                                                                                                                                         |
| `simplify`  | True    | simplify ONNX graph                                                                                                                                                                                                     |
| `opset`     | newest  | pin lower if the consumer runtime complains                                                                                                                                                                             |
| `nms`       | False   | bake NMS into the graph — irrelevant for YOLO26 (NMS-free end-to-end); needed for YOLO11/v8 in non-Python runtimes                                                                                                      |
| `workspace` | None    | TensorRT builder GiB — lower if the build OOMs                                                                                                                                                                          |
| `device`    | None    | `device=0` required for TensorRT; also speeds INT8 calibration                                                                                                                                                          |
| `fraction`  | 1.0     | fraction of calibration data used                                                                                                                                                                                       |

## Verify parity after export (always)

```bash
yolo val model=best.pt data=data.yaml   # baseline
yolo val model=best.onnx data=data.yaml # FP16 within ~0.1–0.3 mAP; INT8 ~1–3
```

Large gaps mean a broken export (imgsz mismatch, missing NMS handling, bad calibration
data) — not "expected quantization noise". Also eyeball one prediction against the .pt.

## Benchmark all formats empirically

```bash
yolo benchmark model=best.pt data=data.yaml imgsz=640 # add quantize=16 to test FP16
```

Produces mAP + latency per exportable format **on this machine** — benchmark on the
deployment hardware, not your dev box.

## Consuming exports outside Python

- In raw runtimes (C++, mobile, JS) **you** own preprocessing (letterbox resize,
  BGR→RGB, /255) and output decoding.
- Output layout differs: YOLO26 is end-to-end (final `[x1,y1,x2,y2,conf,cls]` rows);
  YOLO11/v8 raw heads emit `[4+nc, anchors]` needing decode + NMS — check the output
  tensor shape first. This is the main reason to prefer YOLO26 for edge deployment.
- Class names travel in export metadata where supported; otherwise ship the `names`
  map alongside the model.
- Serving: `ultralytics.utils.triton.TritonRemoteModel` for Triton;
  `examples/` in the ultralytics repo has ONNXRuntime C++/Rust/Python references.

## Troubleshooting

| Symptom                                         | Fix                                                                                                                                             |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Export crashes on missing package               | most backends auto-install on first export; rerun. TensorRT must match your CUDA — install per NVIDIA docs                                      |
| `Unsupported ONNX opset` downstream             | export with lower `opset=`, or upgrade the runtime                                                                                              |
| TensorRT build OOM/slow                         | lower `workspace`, `batch=1`, `dynamic=False`                                                                                                   |
| Export much less accurate                       | imgsz mismatch; INT8 calibration data too small/unrepresentative (fix `data=`, or fall back to `quantize=16`); wrong custom pre/post-processing |
| Engine fails on another machine                 | TensorRT engines are device+version specific — rebuild on target                                                                                |
| CoreML export fails on Linux                    | OS-bound converter — export on macOS or vendor container                                                                                        |
| Deprecation warnings for `half`/`int8`/`tflite` | auto-forwarded (`half→quantize=16`, `int8→quantize=8`, `tflite→litert`) — switch to the new names                                               |

## Related pages

- `format-matrix.md` — all 20 formats, artifacts produced, and which args each format
  supports. Read when using any format beyond onnx/engine/openvino/coreml.

If the installed version rejects an argument, trust the error text (it lists valid
values) and `yolo cfg` over this file.
