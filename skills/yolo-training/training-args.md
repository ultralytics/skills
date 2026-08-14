# Base training argument reference (default.yaml, v8.4.119)

`yolo cfg` prints the installed base schema and defaults. Effective values can also come
from a task trainer, loaded checkpoint, or explicit argument; inspect the run's
`args.yaml`. Names are identical in CLI and Python.

## Train settings

| Arg                             | Default         | Meaning                                                                            |
| ------------------------------- | --------------- | ---------------------------------------------------------------------------------- |
| `model`                         | None            | .pt weights (fine-tune) or .yaml architecture (scratch)                            |
| `data`                          | None            | dataset yaml, or folder for classify                                               |
| `epochs`                        | 100             | training epochs                                                                    |
| `time`                          | None            | max hours; overrides epochs                                                        |
| `patience`                      | 100             | early-stop epochs without val improvement                                          |
| `batch`                         | 16              | int; `-1` AutoBatch; float 0–1 = VRAM fraction                                     |
| `imgsz`                         | 640             | global default; classify uses 224 when unset; checkpoints retain their saved value |
| `save` / `save_period`          | True / -1       | checkpointing; save_period=N saves every N epochs                                  |
| `cache`                         | False           | `True` (RAM) / `"disk"` image caching                                              |
| `device`                        | None            | `0`, `[0,1]`, `cpu`, `mps`, `npu:0`, `xpu:0`, `-1` auto-idle                       |
| `workers`                       | 8               | dataloader workers (per DDP rank)                                                  |
| `project` / `name` / `exist_ok` | None/None/False | output dir control                                                                 |
| `pretrained`                    | True            | load pretrained weights                                                            |
| `cls_remap`                     | True            | remap pretrained cls-head rows by matching class names                             |
| `optimizer`                     | auto            | SGD, MuSGD, Adam, Adamax, AdamW, NAdam, RAdam, RMSprop, auto (case-insensitive)    |
| `seed` / `deterministic`        | 0 / True        | reproducibility                                                                    |
| `single_cls`                    | False           | treat all classes as one                                                           |
| `rect`                          | False           | rectangular batching                                                               |
| `cos_lr`                        | False           | cosine LR schedule                                                                 |
| `close_mosaic`                  | 10              | disable mosaic for final N epochs                                                  |
| `resume`                        | False           | resume from last.pt                                                                |
| `amp`                           | True            | mixed precision                                                                    |
| `fraction`                      | 1.0             | fraction of dataset to train on                                                    |
| `profile`                       | False           | profile ONNX/TensorRT speeds during training                                       |
| `freeze`                        | None            | int N (first N layers) or list of layer indices                                    |
| `multi_scale`                   | 0.0             | imgsz jitter fraction during training                                              |
| `compile`                       | False           | torch.compile: True/`"default"`/`"reduce-overhead"`/`"max-autotune-no-cudagraphs"` |
| `channels_last`                 | False           | channels-last memory format                                                        |
| `overlap_mask` / `mask_ratio`   | True / 4        | segment: merge overlapping masks; mask downsample                                  |
| `dropout`                       | 0.0             | classify only                                                                      |
| `val` / `plots`                 | True / True     | validate + plot during training                                                    |

## Hyperparameters (LR, loss weights)

| Arg                                                    | Default          | Meaning                                                                   |
| ------------------------------------------------------ | ---------------- | ------------------------------------------------------------------------- |
| `lr0` / `lrf`                                          | 0.01 / 0.01      | initial LR / final LR = lr0×lrf                                           |
| `momentum`                                             | 0.937            | SGD momentum / Adam beta1                                                 |
| `weight_decay`                                         | 0.0005           |                                                                           |
| `warmup_epochs` / `warmup_momentum` / `warmup_bias_lr` | 3.0 / 0.8 / 0.1  |                                                                           |
| `box` / `cls` / `dfl`                                  | 7.5 / 0.5 / 1.5  | detect loss weights                                                       |
| `cls_pw`                                               | 0.0              | class-weights power for class imbalance (0=off, 1=full inverse-frequency) |
| `pose` / `kobj` / `rle`                                | 12.0 / 1.0 / 1.0 | pose loss weights                                                         |
| `angle`                                                | 1.0              | OBB angle loss                                                            |
| `dlog` / `dgrad` / `dlam`                              | 1.0 / 0.5 / 1.0  | depth loss weights                                                        |
| `distill_model` / `dis`                                | None / 6.0       | knowledge-distillation teacher + weight                                   |
| `nbs`                                                  | 64               | nominal batch size for loss normalization                                 |

## Augmentation

| Arg                                             | Default               | Meaning / when to change                               |
| ----------------------------------------------- | --------------------- | ------------------------------------------------------ |
| `hsv_h` / `hsv_s` / `hsv_v`                     | 0.015 / 0.7 / 0.4     | color jitter; reduce `hsv_h` for color-defined classes |
| `degrees`                                       | 0.0                   | rotation; `degrees=180` for aerial/top-down            |
| `translate` / `scale` / `shear` / `perspective` | 0.1 / 0.5 / 0.0 / 0.0 | geometric; `scale` accepts (min,max) tuple             |
| `flipud` / `fliplr`                             | 0.0 / 0.5             | `flipud=0.5` for aerial; pose fliplr needs `flip_idx`  |
| `bgr`                                           | 0.0                   | channel-swap probability                               |
| `mosaic`                                        | 1.0                   | 4-image mosaic (off for last `close_mosaic` epochs)    |
| `mixup` / `cutmix`                              | 0.0 / 0.0             | try 0.1 for crowded scenes                             |
| `copy_paste` / `copy_paste_mode`                | 0.0 / flip            | segment only; try 0.3 for overlapping instances        |
| `auto_augment`                                  | randaugment           | classify: randaugment/autoaugment/augmix               |
| `erasing`                                       | 0.4                   | classify random erasing                                |

When to deviate: aerial/top-down (incl. OBB) → `degrees=180 flipud=0.5`;
orientation-meaningful content → keep `degrees=0`; never disable augmentation to make
training loss look better — that's overfitting on purpose.

Depth training automatically disables `mosaic`, `mixup`, `cutmix`, and `copy_paste`;
passing them has no effect because multi-image composition would invalidate depth maps.
