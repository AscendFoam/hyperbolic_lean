# T32 GCN Grouped Training Sweep

## Task ID
T32

## Goal
在 `Field.Subfield` 与 `Order.Ring` 上运行 GCN 5-seed grouped training 对照，使用 T31 已 review 的 grouped retrieval runner / seed sweep path，产出可审查的 mean ± std 报告。

## Why Now
`T31` 已通过 adversarial review，最小 query-grouped loss、query-level split 和 grouped eval key 已对齐。进入 HGCN 对照前，需要先固定欧氏 GCN 在相同 grouped protocol 下的 5-seed baseline。

## Allowed Files
- new artifacts under `artifacts/baselines/relation_seed_sweeps/`
- new or updated grouped GCN configs under `project_bootstrap/**/configs`
- `docs/experiment_reports/gcn_grouped_training.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不改 HGCN 代码
- 不改变 T31 定义的 grouped training 协议、query key、loss semantics 或 model selection metric
- 不改旧 BCE GCN / HGCN runner 来伪造 grouped 结果
- 不覆盖历史 artifact
- 不把 T31 smoke artifact 或单 seed smoke 写成正式 5-seed benchmark
- 不改 `docs/02_experiment_plan.md`

## Inputs to Read
- `docs/06_eval_protocol.md`
- `docs/review/T31_review.md`
- `docs/training_alignment_audit.md`
- `docs/candidate_graph_audit.md`
- `docs/diagnostics_protocol.md`
- T31 grouped runner implementation:
  - `project_bootstrap/baseline_scaffold/src/run_relation_grouped_retrieval_baseline.py`
  - `project_bootstrap/baseline_scaffold/src/run_relation_seed_sweep.py`
- existing grouped / relation configs under `project_bootstrap/baseline_scaffold/configs`

## Expected Output
- Two GCN grouped 5-seed sweep artifacts where feasible:
  - one for `Field.Subfield`
  - one for `Order.Ring`
- Each formal sweep config must explicitly set:
  - `model_type` / sweep model type for grouped GCN
  - `grouped_loss = "sampled_softmax"` unless there is a documented reason otherwise
  - `negative_ratio` explicitly, not by relying on the grouped runner default
  - output path under `artifacts/baselines/relation_seed_sweeps/`
- `docs/experiment_reports/gcn_grouped_training.md` must include:
  - exact commands run
  - config paths
  - artifact paths
  - seed list
  - grouped `MAP`, `nDCG`, `nDCG@10`, `Recall@k`, `grouped-MRR`
  - hop bucket results where available
  - mean ± std over seeds
  - explicit note that this is GCN only; HGCN comparison remains T33
- If either target graph lacks a runnable config or data artifact, do not invent results. Record the blocker, the missing path/config, and the partial verified output.

## Verification
```powershell
Get-ChildItem artifacts\baselines\relation_seed_sweeps
rg -n "mean|std|Recall|MAP|nDCG|grouped|hop|negative_ratio|sampled_softmax" docs\experiment_reports\gcn_grouped_training.md project_bootstrap\baseline_scaffold\configs
```

If the environment supports it, run the actual 5-seed grouped GCN sweep command(s). If runtime, data, or dependency constraints prevent completion, report the exact command attempted, error, and which artifacts were or were not produced.

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
adversarial
