# Export format matrix (v8.4.174)

From `ultralytics.engine.exporter.export_formats()` — the installed version's ground truth: `from ultralytics.engine.exporter import export_formats; print(export_formats())`.

| `format=`                | Artifact             | Supported extra args                                                      |
| ------------------------ | -------------------- | ------------------------------------------------------------------------- |
| `torchscript`            | `.torchscript`       | batch, quantize, nms, dynamic                                             |
| `onnx`                   | `.onnx`              | batch, data, dynamic, quantize, opset, simplify, nms, fraction            |
| `openvino`               | `_openvino_model/`   | batch, data, dynamic, quantize, nms, fraction                             |
| `engine` (TensorRT)      | `.engine`            | batch, data, dynamic, quantize, opset, simplify, workspace, nms, fraction |
| `coreml`                 | `.mlpackage`         | batch, dynamic, quantize, nms                                             |
| `coreai` (Apple Core AI) | `.aimodel`           | batch, quantize                                                           |
| `saved_model` (TF)       | `_saved_model/`      | batch, data, fraction, quantize, opset, nms                               |
| `pb` (TF GraphDef)       | `.pb`                | batch, opset                                                              |
| `edgetpu`                | `_edgetpu.tflite`    | data, fraction, quantize, opset                                           |
| `litert` (was `tflite`)  | `.tflite`            | batch, quantize, data, fraction                                           |
| `paddle`                 | `_paddle_model/`     | batch                                                                     |
| `mnn`                    | `.mnn`               | batch, dynamic, quantize, opset, simplify, nms                            |
| `ncnn`                   | `_ncnn_model/`       | batch, quantize                                                           |
| `imx` (Sony IMX500)      | `_imx_model/`        | data, quantize, fraction, nms                                             |
| `rknn` (Rockchip)        | `_rknn_model/`       | batch, name, quantize, opset, simplify, data, fraction                    |
| `executorch`             | `_executorch_model/` | batch                                                                     |
| `axelera`                | `_axelera_model/`    | batch, quantize, fraction, data                                           |
| `deepx`                  | `_deepx_model/`      | data, quantize, opset, simplify, optimize                                 |
| `qnn` (Qualcomm)         | `_qnn.onnx`          | batch, name, quantize, opset, simplify, fraction, data                    |
| `hailo`                  | `_hailo_model/`      | name, quantize, data, fraction, simplify, conf, iou                       |
| `ascend` (Huawei)        | `_ascend_model/`     | batch, name, quantize, opset, simplify, nms                               |
| `xilinx` (AMD Xilinx)    | `_xilinx_model/`     | name, quantize, data, fraction, opset, simplify                           |

Notes:

- `name=` doubles as the hardware target selector for `rknn` (e.g. `name=rk3588`), `qnn` (Hexagon HTP arch, e.g. `name=73`), `hailo`, `ascend`, and `xilinx` (Vitis AI device). When omitted it falls back to `rk3588`, `73`, `hailo8l`, `Ascend310B4`, or `ve2-xc2ve3858`, so always set it. For rknn/qnn/hailo/xilinx the error message lists valid targets; for ascend pass a CANN SoC version whose kernels are installed, like `Ascend310P3`.
- `quantize` aliases canonicalize `8`/`int8`/`w8a8` to `8`, `16`/`fp16`/`w16a16` to `16`, and `32`/`fp32`/`w32a32` to `32`; `w8a16` and `w8a32` remain mixed schemes. FP32 (`32`) is usually equivalent to unset, with format-specific exceptions.
- Precision support is format-specific. FP16: `torchscript` (GPU only), `onnx`, `openvino`, `engine`, `coreml`, `mnn`, `ncnn`, `rknn` (chip-dependent), `ascend`, `coreai`. INT8: `onnx`, `openvino`, `engine`, `coreml`, `saved_model`, `edgetpu`, `mnn`, `imx`, `rknn` (detect only), `axelera`, `deepx`, `hailo`, `litert`, `xilinx`. `w8a16`: `coreml`, `qnn`, `litert`; `w8a32`: `litert` only. Explicit unsupported precision requests fail; with `quantize` unset, some device formats select their required precision automatically.
- `nms` in the table means `nms=True` can embed NMS; other formats warn and export raw outputs. `imx` always embeds NMS for detect, pose, and segment (any `nms` value becomes `True`). `nms=False` (YOLO26/YOLOv10 NMS-free head) falls back to raw outputs with a warning on `rknn`, `ncnn`, `executorch`, `paddle`, `edgetpu`, `qnn`, LiteRT INT8/`w8a16`, and TensorRT <8.5 or INT8 TensorRT 10.3 on JetPack 6.
- Calibration requirements vary by backend and scheme. Pass representative `data` when required; LiteRT `w8a32` needs no calibration.
- Some formats pip-install heavy, pinned toolchains into the active environment on first use (imx, rknn, axelera, deepx, xilinx). The first export is slow, so tell the user it isn't hung; the pins can downgrade shared packages, so prefer a dedicated virtual environment.
- Core AI export requires macOS 26+ on Apple silicon or x86_64 Linux (glibc 2.34+), torch>=2.8, and Python 3.11–3.14. The `.aimodel` runtime targets iOS 27+/macOS 27+; use CoreML for broader Apple support.
- Core AI accepts `quantize=16`, but some FP16 `.aimodel` assets can abort while loading their Apple Neural Engine program; fall back to FP32 if one does.
