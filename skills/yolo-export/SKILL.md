---
name: yolo-export
description: >
  Use when exporting or deploying Ultralytics YOLO models in Platform or code — the Platform Export tab and yolo export/model.export() for ONNX, TensorRT, CoreML, Core AI, OpenVINO, LiteRT, NCNN, ExecuTorch, and NPUs (RKNN, QNN, Hailo, Ascend, IMX, Axelera, DeepX, Xilinx), FP16/INT8 quantization, benchmarking, and non-Python runtimes. For inference with .pt weights or Platform endpoints, see yolo-inference.
---

# Export, quantization & deployment

## Fastest route: export in Platform

Open a completed model's **Export** tab, select a format, configure its arguments, and click **Start Export**. Platform runs CPU exports directly and asks for a target GPU where the format requires one (notably TensorRT); download the artifact when the job completes. For TensorRT, select the deployment device's GPU family or Jetson target; if its TensorRT/CUDA versions differ from the device's, export locally on that device instead.

Use Platform when you do not want to install each exporter toolchain locally. Use the Python/CLI path below for custom calibration, repeatable automation, local hardware builds, or immediate parity validation. See [Platform model export](https://docs.ultralytics.com/platform/train/models#export-model).

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

| Target                                                       | `format=`                                                                    | Why                                                                                                        |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| NVIDIA GPU / Jetson                                          | `engine` (TensorRT)                                                          | fastest on NVIDIA; **build on the deployment device** — engines are not portable across GPUs/TRT versions  |
| Intel CPU/iGPU/NPU                                           | `openvino`                                                                   | up to 3× CPU speedup on Intel                                                                              |
| Apple iOS/macOS                                              | `coreml`                                                                     | broad OS coverage, Vision/iOS/Flutter support                                                              |
| Apple iOS 27+/macOS 27+                                      | `coreai`                                                                     | native `.aimodel`; iOS/Flutter SDKs default to `coreml`; export on Apple silicon macOS 26+ or x86_64 Linux |
| Android                                                      | `litert` (renamed from `tflite`) or `ncnn`                                   | NCNN strong on ARM                                                                                         |
| Raspberry Pi                                                 | `ncnn`                                                                       | best ARM CPU latency                                                                                       |
| PyTorch Edge                                                 | `executorch`                                                                 |                                                                                                            |
| Cross-platform / unsure                                      | `onnx`                                                                       | runs everywhere; start here, specialize when latency demands                                               |
| NPUs (Rockchip/Qualcomm/Hailo/Huawei/Sony/Axelera/DeepX/AMD) | `rknn` / `qnn` / `hailo` / `ascend` / `imx` / `axelera` / `deepx` / `xilinx` | `name=` selects the exact chip for rknn/qnn/hailo/ascend/xilinx                                            |

Full 22-target local export matrix with per-format supported args: `format-matrix.md` (this folder).

## Key arguments

| Arg         | Default | Notes                                                                                                                                                                                           |
| ----------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `imgsz`     | model   | inherited from the loaded model; set explicitly to the deployment shape                                                                                                                         |
| `quantize`  | None    | precision request: `16`/`fp16`, `8`/`int8`/`w8a8`, `w8a16`, `w8a32`, or `32`/`fp32`; support, speed, size, and accuracy are backend-dependent — see `format-matrix.md` and benchmark the target |
| `data`      | None    | representative calibration data when required; use >300 images generally and 500+ for TensorRT. Omission selects a small task default, so pass deployment-representative data explicitly        |
| `dynamic`   | False   | variable input shape/batch where supported; check `format-matrix.md` and benchmark the target                                                                                                   |
| `batch`     | 1       | max batch baked into the export                                                                                                                                                                 |
| `simplify`  | True    | simplify ONNX graph                                                                                                                                                                             |
| `opset`     | None    | compatible ONNX opset selected automatically when unset; pin lower if the consumer runtime complains                                                                                            |
| `nms`       | None    | `None` exports raw outputs for external NMS (YOLO26 too); `True` embeds NMS where `format-matrix.md` lists `nms`; `False` selects the YOLO26/YOLOv10 NMS-free head, else raw outputs            |
| `workspace` | None    | TensorRT builder GiB — lower if the build OOMs                                                                                                                                                  |
| `device`    | None    | TensorRT needs a GPU (auto-set to `device=0` when unset); a GPU also speeds INT8 calibration                                                                                                    |
| `fraction`  | 1.0     | fraction of calibration data used                                                                                                                                                               |

## Verify parity after export (always)

```bash
yolo val model=best.pt data=data.yaml   # baseline
yolo val model=best.onnx data=data.yaml # compare the same task metric with the baseline
```

Acceptable differences depend on the task, model, backend, precision, and calibration data. Investigate unexpected gaps by matching `imgsz` and pre/post-processing and, where required, using representative calibration data. Also compare one prediction with `.pt`.

## Benchmark all formats empirically

```bash
yolo benchmark model=best.pt data=data.yaml imgsz=640                                    # all formats at default precision
yolo benchmark model=best.pt data=data.yaml format=engine quantize=16 device=0 imgsz=640 # targeted FP16
```

Produces the task metric + latency per exportable format **on this machine**. Repeat for each supported precision and benchmark on deployment hardware, not your dev box.

## Consuming exports outside Python

- In raw runtimes (C++, mobile, JS) **you** own preprocessing (letterbox resize, BGR→RGB, /255) and output decoding.
- Detect output layout follows `nms`: the default `nms=None` emits raw `[4+nc, anchors]` heads (xywh boxes + class scores) for every model, YOLO26 included, so you run NMS (`imx` instead always embeds NMS). `nms=False` on YOLO26/YOLOv10 emits NMS-free `[max_det, 6]` rows `[x1,y1,x2,y2,conf,cls]`, and `nms=True` embeds NMS with the same row layout where supported; some formats fall back to raw heads (`format-matrix.md`). Segment, pose, and OBB add task-specific outputs. Check export warnings and shapes.
- Class names travel in export metadata where supported; otherwise ship the `names` map alongside the model.
- Serving: `ultralytics.utils.triton.TritonRemoteModel` for Triton; `examples/` in the ultralytics repo has ONNXRuntime C++/Rust/Python references.

## Troubleshooting

| Symptom                                                   | Fix                                                                                                                                                                                                                                         |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Export crashes on missing package                         | most backends auto-install on first export; rerun. On Linux, TensorRT auto-installs as `tensorrt-cu<torch CUDA major>`; elsewhere install it per NVIDIA docs. Hailo (Dataflow Compiler) and Ascend (CANN `atc`) need their vendor SDK first |
| `Unsupported ONNX opset` downstream                       | export with lower `opset=`, or upgrade the runtime                                                                                                                                                                                          |
| TensorRT build OOM/slow                                   | lower `workspace`, `batch=1`, `dynamic=False`                                                                                                                                                                                               |
| Export much less accurate                                 | imgsz mismatch; too little/unrepresentative calibration data; wrong custom pre/post-processing; use a supported higher precision or backend                                                                                                 |
| Engine fails on another machine                           | TensorRT engines are device+version specific — rebuild on target                                                                                                                                                                            |
| CoreML export fails on Windows                            | export on macOS or Linux                                                                                                                                                                                                                    |
| Core AI export is unavailable                             | requires macOS 26+ on Apple silicon or x86_64 Linux (glibc 2.34+), torch>=2.8, and Python 3.11–3.14; use CoreML for broader production support                                                                                              |
| Deprecation warnings for `half`/`int8`/`end2end`/`tflite` | auto-forwarded (`half→quantize=16`, `int8→quantize=8`, `end2end=True→nms=False`, `end2end=False→nms=None` unless `nms=True` is also passed, `tflite→litert`) — switch to the new names                                                      |

## Related pages

- `format-matrix.md` — all 22 local export targets, artifacts produced, and supported args. Read when using any format beyond onnx/engine/openvino/coreml.

If the installed version rejects an argument, trust the error text (format and quantize errors list valid values) and `yolo cfg` over this file.
