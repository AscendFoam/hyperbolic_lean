# T33 HGCN Grouped Training Sweep

## Task ID
T33

## Goal
在相同 split、候选集合、seed 列表和参数预算下运行 HGCN 5-seed grouped training 对照，并与 T32 的 GCN grouped baseline 做可比比较。

## Why Now
`T32` 已通过 adversarial review，GCN grouped 5-seed baseline 已收口。现在进入 HGCN 对照，才能判断双曲模型在 reviewed grouped protocol 下是否有增益。

## Allowed Files
- new artifacts under `artifacts/baselines/relation_seed_sweeps/`
- related configs under `project_bootstrap/**/configs`
- `docs/experiment_reports/hgcn_grouped_training.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不修改 GCN 结果
- 不调参到不可比
- 不把局部偶然收益写成稳定结论
- 不改变 T32 采用的 grouped runner / split / candidate / metric 口径
- 不回头改 T31/T32 的协议或评价字段
- 不把 smoke 结果当作正式 benchmark 结论
- 不覆盖 T32 已有 artifact

## Inputs to Read
- `docs/06_eval_protocol.md`
- `docs/review/T32_review.md`
- `docs/experiment_reports/gcn_grouped_training.md`
- `docs/training_alignment_audit.md`
- `docs/diagnostics_protocol.md`
- `docs/candidate_graph_audit.md`
- `project_bootstrap/baseline_scaffold/configs` 中与 T32 对应的 grouped GCN configs
- `project_bootstrap/baseline_scaffold/src/run_relation_grouped_retrieval_baseline.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_seed_sweep.py`

## Expected Output
- HGCN 5-seed mean ± std 报告。
- 与 T32 使用相同数据、split、候选、seed 列表、参数预算和指标。
- 明确列出 HGCN 配置与 GCN 配置之间的唯一差异。
- 如果需要新 config，应当只做 HGCN 相关切换，不要改 grouped protocol。
- 报告中应明确写出与 T32 的可比性约束，避免把局部绝对数值直接解读成优劣结论。

## Verification
```powershell
rg -n "mean|std|Recall|MAP|nDCG|grouped|hop|GCN|HGCN" docs\experiment_reports\hgcn_grouped_training.md
```

如果环境支持，实际运行 5-seed grouped HGCN sweep，并记录 artifact 路径。若 runtime、依赖或配置不可比导致无法完成，必须说明具体 blocker，不能伪造结果。

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
adversarial
