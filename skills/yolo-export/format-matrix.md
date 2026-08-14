# Export format matrix (v8.4.119)

From `ultralytics.engine.exporter.export_formats()` — the installed version's ground
truth: `from ultralytics.engine.exporter import export_formats; print(export_formats())`.

| `format=`               | Artifact             | Supported extra args                                                      |
| ----------------------- | -------------------- | ------------------------------------------------------------------------- |
| `torchscript`           | `.torchscript`       | batch, quantize, nms, dynamic                                             |
| `onnx`                  | `.onnx`              | batch, data, dynamic, quantize, opset, simplify, nms, fraction            |
| `openvino`              | `_openvino_model/`   | batch, data, dynamic, quantize, nms, fraction                             |
| `engine` (TensorRT)     | `.engine`            | batch, data, dynamic, quantize, opset, simplify, workspace, nms, fraction |
| `coreml`                | `.mlpackage`         | batch, dynamic, quantize, nms                                             |
| `saved_model` (TF)      | `_saved_model/`      | batch, data, fraction, quantize, opset, keras, nms                        |
| `pb` (TF GraphDef)      | `.pb`                | batch, opset                                                              |
| `litert` (was `tflite`) | `.tflite`            | batch, quantize, data, fraction                                           |
| `edgetpu`               | `_edgetpu.tflite`    | data, fraction, quantize, opset                                           |
| `paddle`                | `_paddle_model/`     | batch                                                                     |
| `mnn`                   | `.mnn`               | batch, dynamic, quantize, opset, simplify, nms                            |
| `ncnn`                  | `_ncnn_model/`       | batch, quantize                                                           |
| `executorch`            | `_executorch_model/` | batch                                                                     |
| `imx` (Sony IMX500)     | `_imx_model/`        | data, quantize, fraction, nms                                             |
| `rknn` (Rockchip)       | `_rknn_model/`       | batch, name, quantize, opset, simplify, data, fraction                    |
| `qnn` (Qualcomm)        | `_qnn.onnx`          | batch, name, quantize, opset, simplify, fraction, data                    |
| `hailo`                 | `_hailo_model/`      | name, quantize, data, fraction, simplify, conf, iou                       |
| `ascend` (Huawei)       | `_ascend_model/`     | batch, name, quantize, opset, simplify, nms                               |
| `axelera`               | `_axelera_model/`    | batch, quantize, fraction, data                                           |
| `deepx`                 | `_deepx_model/`      | data, quantize, opset, simplify, optimize                                 |

Notes:

- `name=` doubles as the hardware target selector for `rknn` (e.g. `name=rk3588`),
  `qnn`, `hailo`, `ascend`. For rknn/qnn/hailo the error message lists valid chip
  names; for ascend pass any CANN soc version like `Ascend310P3`.
- `quantize` aliases canonicalize `8`/`int8`/`w8a8` to `8`,
  `16`/`fp16`/`w16a16` to `16`, and `32`/`fp32`/`w32a32` to `32`; `w8a16` and `w8a32`
  remain mixed schemes. FP32 (`32`) is usually equivalent to unset, with format-specific
  exceptions.
- Precision support is format-specific. FP16: `torchscript` (GPU only), `onnx`,
  `openvino`, `engine`, `coreml`, `mnn`, `ncnn`, `rknn` (chip-dependent), `ascend`.
  INT8: `onnx`, `openvino`, `engine`, `coreml`, `saved_model`, `edgetpu`, `mnn`, `imx`,
  `rknn`, `axelera`, `deepx`, `hailo`, `litert`. `w8a16`: `coreml`, `imx`, `qnn`,
  `litert`; `w8a32`: `litert` only. Explicit unsupported precision requests fail;
  with `quantize` unset, some device formats select their required precision automatically.
- Calibration requirements vary by backend and scheme. Pass representative `data` when
  required; LiteRT `w8a32` needs no calibration.
- Some formats install their toolchains in isolated environments on first use (imx,
  rknn, axelera, deepx) — first export is slow; tell the user it isn't hung.
