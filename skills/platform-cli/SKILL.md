---
name: platform-cli
description: >
  Use when operating Ultralytics Platform from a terminal or script with the ul CLI
  (ul cloud RESOURCE OPERATION key=value, PyPI package ultralytics-platform) — listing,
  creating, updating, cloning, or moving projects, datasets, and models, starting and
  monitoring cloud training runs, downloading weights, exports, deployments, uploads,
  trash and restore, and storage integrations. For the Platform web UI or local yolo
  commands, see yolo; for choosing what to train and how to improve it, see
  yolo-training and yolo-tuning.
---

# Platform CLI (`ul cloud`)

`ul` needs Python 3.11+ and comes with `pip install ultralytics` or
`pip install ultralytics-platform`. `ul cloud` calls the Platform API through the generated
SDK; `ul login`, `ul train`, `ul predict`, and the other local commands delegate to the
`ultralytics` package. This skill covers Platform operations, not model selection or
hyperparameter tuning.

```bash
pip install ultralytics                   # or `pip install ultralytics-platform`
export ULTRALYTICS_API_KEY="YOUR_API_KEY" # or `ul login API_KEY`
ul cloud --help                           # every resource and operation
ul cloud training start --help            # one operation's arguments, types, and choices
```

Endpoint semantics are documented in the
[Platform API reference](https://docs.ultralytics.com/platform/api).

## Canonical command shapes

```bash
ul cloud account summary # plan, credits, counts; `username` is your workspace
ul cloud datasets list   # omit owner= for your own workspace; owner=TEAM for a team
ul cloud projects create project=helmets name="Helmet Detection" visibility=private
ul cloud models create body='{"owner":"WS","project":"helmets","model":"exp1","name":"Experiment 1"}'
ul cloud training start model_id=MODEL_ID gpu_type=l4 \
  train_args='{"model":"yolo26n.pt","data":"ul://WS/datasets/helmets","epochs":50}'
ul cloud models training project=helmets model=exp1 # live status, epoch progress, metrics
ul cloud models files project=helmets model=exp1    # short-lived weights download URL
```

Argument rules:

- Arguments are SDK Python names as `key=value` (`gpu_type`, `project_id`), never
  `--key value`. A bare boolean means `true`. Quote JSON for the shell.
- An operation takes one `body=` JSON object exactly when its help lists
  `body (dict[str, Any])`. These are the operations whose API request is a union of
  shapes: `models create`, `deployments update`, `images update`, `lifecycle delete-trash`,
  `datasets ingest`, `upload signed-url`, `storage-integrations create`/`discover`, and
  `models predict`/`deployments predict`. Every other operation takes flat fields; nested
  objects such as `train_args`, `metadata`, and `args` are still JSON values.
- Object and array values accept `@file.json` or `@-` for stdin. Multipart binaries such as
  the predict `file` field accept `@path` only.
- Help shows only `body (dict[str, Any])` for union bodies. Read that request schema from the
  production contract instead of guessing or loading the whole file:

```bash
curl -s https://platform.ultralytics.com/openapi.json | python3 -c \
  "import json,sys; print(json.dumps(json.load(sys.stdin)['paths']['/api/models']['post']['requestBody'], indent=1))"
```

Behavior rules:

- Output is the complete API response on stdout, printed as JSON, text, or bytes according
  to its content type. Download operations return signed URLs, not bytes: `datasets export`,
  `datasets create-export`, `models files`, and a completed `exports retrieve` return URLs
  that expire. Preserve them verbatim and fetch them separately.
- Failures go to stderr: exit 1 for API/connection errors, 2 for argument/file errors, 130
  when interrupted. Interrupting does not cancel a submitted job; use its cancel operation
  (`models delete-training`, `exports delete`, `datasets delete-batch`).
- There is no `--json`, `--fields`, `--dry-run`, or automatic pagination. `list` operations
  take only `limit=` (raise it once to its maximum). Operations that page expose `page`,
  `offset`, `cursor`, or `page_token` in their help; the CLI never fetches the next page, so
  keep requesting until the response reports no more.
- An omitted path `owner` defaults to the logged-in username after one account lookup. Pass
  `owner=TEAM` for team workspaces. Account, billing, trash, storage-integration, and Roboflow
  commands act on the credential's own account, and `account summary` does not list teams
  for API keys.
- Display names, URL slugs, database IDs, and URIs are distinct. Training data is
  `ul://OWNER/datasets/DATASET`; starting weights are a checkpoint name or
  `ul://OWNER/PROJECT/MODEL`. Carry returned IDs and slugs into the next command; retrieve
  missing identifiers instead of inferring them from names or URLs.

## Working method

1. Resolve the requested outcome and target. Use exact supplied identifiers; otherwise list
   and pick one unambiguous match. For several matches, inspect distinguishing metadata and
   ask when the target or consequence stays ambiguous. A bounded listing does not prove
   absence; broaden discovery or report what was searched.
2. Read current state when it affects the change (visibility, status, existing children).
3. Execute the smallest requested change, then verify from the response. Retrieve again when
   the response omits needed state, the write is uncertain, or the job is asynchronous.
4. Report what actually changed, current status, warnings, and the resource link. Creating
   an entry, accepting a job, and completing it are separate outcomes.

Execute clearly requested actions without repeated confirmation. For spending, sharing, or
irreversible changes, resolve ambiguity about target or consequence first. A request for
advice is not authorization to act; "clean things up" is not permission for account-wide
deletion. Do not invent commands, flags, or status edits to simulate operations the CLI does
not expose; use the UI for those.

## Workflows

Commands omit the `ul cloud` prefix, the defaulted owner, and the `project=`/`model=`/
`dataset=` path identifiers that `--help` lists.

| Goal               | Commands                                                                                                                                                                                                                                                                                                              |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Inventory          | `projects list`, `datasets list`, `models list project=P`. `explore search q=... type=datasets` searches public content, which is not private inventory. Retrieve a dataset to check task, classes, splits, and readiness.                                                                                            |
| Create             | `projects create project=slug name="Display"`, `datasets create dataset=slug name="Display" task=detect`. Set `visibility=` deliberately.                                                                                                                                                                             |
| Copy               | `datasets clone`, `projects clone`, `models clone`: path `owner`/`project`/`model`/`dataset` name the source; `owner_body`, `project_body`, `model_body`, `dataset_body` name the destination. A model's destination project must already exist.                                                                      |
| Rename, edit, move | `<resource> update` with the changed fields only. Move a model with `models update project_id=DEST_ID` alone.                                                                                                                                                                                                         |
| Compare runs       | `projects retrieve` for model summaries, `models list`, or `datasets models` for runs on a dataset; `models retrieve` only for missing metrics. Tabulate status, dataset/version, configuration, and requested metrics with links. Missing metrics are unknown, not zero. There is no compare command.                |
| Weights            | `models files` returns a temporary checkpoint URL. No training or export is needed.                                                                                                                                                                                                                                   |
| Convert            | `exports create format=onnx`, then `exports retrieve export_id=ID` for progress and the download URL. `format=engine` needs `gpu_type`. Exporting does not deploy.                                                                                                                                                    |
| Dataset versions   | `datasets create-export` saves an immutable numbered snapshot and returns its signed NDJSON URL; `datasets export` (current data) or `datasets export v=N` (a saved version) returns a signed download URL; `datasets restore version=N` rolls the live dataset back in place.                                        |
| Deploy             | `deployments create project=P model=M deployment=slug name="Display" region=us-central1`. `deployments update deployment=D body='{"action":"replace","project":"P","model":"M"}'` swaps the model on the same URL; `body='{"action":"stop"}'` and `{"action":"start"}` pause and resume it. `health` warms it.        |
| Inference          | `models predict body='{"file":"@image.jpg"}'` or `deployments predict deployment=D body='{"file":"@image.jpg"}'`; `deployments logs`/`metrics` inspect a service. `images predict image_id=ID model_id=ul://...` predicts on a dataset image without saving labels.                                                   |
| Import data        | `datasets create`, then `upload signed-url body=` (`assetType`, `assetId`, `filename`, `contentType`, `totalBytes`), PUT the bytes with the returned headers, `upload complete session_id=S`, `datasets ingest body='{"sessionId":"S"}'` (or `{"sourceUrl":...}`), then retrieve until ready. Queued is not imported. |
| Trash              | `<resource> delete` moves to 30-day trash. `lifecycle trash` lists it, `lifecycle restore id=ID type=model` undeletes, `lifecycle delete-trash body='{"id":"ID","type":"model"}'` purges one item and `body='{"all":true}'` the whole account.                                                                        |

## Cloud training

1. Resolve the workspace, project, a ready dataset, starting weights, and requested settings.
   Check `training gpu-availability` before choosing `gpu_type`; cloud training spends
   credits. `data` must use the dataset's actual owner, which may differ from the model's.
2. `models create body=...` with `owner`, `project`, the `model` slug, and `name` for a new
   experiment. Reuse a pending entry from a failed start after checking its state.
3. `training start model_id=ID gpu_type=... train_args=...` with a fresh `train_args`
   holding `model`, `data`, and numeric `epochs` plus requested settings. Omit `device`.
   Do not copy stored worker arguments wholesale; saved data paths may be worker-local.
4. `models training` or `models retrieve` for progress. Return the run link and actual
   status without waiting for completion unless asked. `models delete-training` cancels a
   run and keeps its entry; never start an active run again.

## Recover

- **401**: check the credential source without exposing secrets. `ULTRALYTICS_API_KEY`
  overrides the saved login key, so logging in again does not replace a stale environment
  value. If the execution environment injects credentials, use its flow. Verify with a read
  afterwards.
- **403**: read the error for workspace access, permissions, or operation constraints; do
  not assume an expired login.
- Fix clear validation errors within the requested action. After a timeout or uncertain
  write, inspect state before retrying. Stop on unresolved inputs, permissions, or repeated
  failure; report partial results and remaining work instead of duplicating writes.

Resource links use `https://platform.ultralytics.com`: projects `/{owner}/{project}`,
datasets `/{owner}/datasets/{dataset}`, models and training `/{owner}/{project}/{model}`.
Use returned slugs after changes; retrieve missing slugs.

## Operation gotchas

Operation help already says what each command does. These are the side effects and
constraints it omits; `--help` and the error text still win when they disagree.

### Clone

- Project, dataset, and model clones need a different destination workspace. Cloning is
  not how to create a same-workspace experiment; use `models create`.
- Model sources need usable weights and must not be training. Project clones carry
  completed models with weights but not datasets, deployments, exports, or unfinished runs.

### Visibility

- Creation may default to public and clones may keep the source's visibility, so set
  `visibility=` explicitly. Public projects expose their models. Public visibility is not
  collaborator edit access.

### Update

- Arrays and `metadata` objects replace prior values. Send the full list for a partial edit.
- `starred` is handled by a separate branch that ignores other fields in the same call. Send
  it alone.
- Starting training again on an existing model clears its prior run metrics and results.
  Create a new model to keep them. Fine-tuning from existing weights does not resume the
  optimizer or epoch count.
- `capture_dataset_version=true` saves a new snapshot; it does not select an existing one.

### Delete, trash, restore

- `projects update archived=true` only organizes; it frees nothing.
- Deleting a project trashes its models and cancels their training.
- Restore a parent before its children; independently trashed children need their own
  restore. `datasets restore version=N` rolls the live dataset back in place and is not a
  trash restore. Stop active annotation before it.
- `images delete` and `images delete-bulk` are permanent and bypass trash.
- `datasets create-export` reuses an identical existing snapshot instead of creating a
  duplicate.

### Labels and auto-annotation

- `images update body='{"labels":[...]}'` replaces every label on the image, and
  `images predict` alone saves nothing. Retrieve first for a partial edit, and when the
  retrieve reports `labelsTruncated`, do not overwrite the labels you did not see.
- `datasets create-batch` persists labels and saves a version, normally on unlabeled images
  only. `include_annotated=true` also processes labeled images while retaining old labels.
  `delete-batch` cancels or dismisses a run without undoing labels already saved.
- Annotation prediction needs compatible tasks and classes or a `class_mapping`, and rejects
  connected, depth, and more-than-three-channel datasets.

### Classes, splits, task

- `class_names` replaces names by index; keep the order for a rename. Merging or deleting
  classes remaps or removes labels and shifts IDs.
- `redistribute-splits` reshuffles the whole dataset. `images update-bulk` moves selected IDs,
  and conflict policy `replace` may remove target images.
- `adopt-images` adds unlabeled public-image references to the train split, skipping
  existing images; it copies no labels or splits.
- Changing `task` converts no annotations. Switching to or from depth needs an empty dataset.

### Analysis

- `create-embeddings` starts analysis; `embeddings` and `clustering` read it;
  `delete-embeddings` cancels the analysis, not images.

### Connected storage

- Connected datasets are indexed in place, not copied. They cannot take appended uploads,
  versions, clones, or batch annotation.
- Disconnecting an integration leaves provider objects intact but breaks dataset access
  until the same account reconnects. Roboflow credentials are separate from Platform
  credentials.

### Compute

- Editing a model's `status` starts or stops nothing.
- Deployment `delete` is permanent; there is no trash for deployments.
- Export `delete` cancels a running conversion or removes the finished file; the source
  model is untouched.

The installed CLI is the authority: `ul version` shows the versions, `ul cloud <resource>
<operation> --help` lists valid arguments and choices, and error text beats any command
shape or caveat in this file. For endpoint semantics, the
[Platform API reference](https://docs.ultralytics.com/platform/api) and the live
`/openapi.json` win over memory.
