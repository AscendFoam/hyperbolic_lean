# T32 GCN Grouped Training Sweep

## Task ID
T32

## Goal
在 `Field.Subfield` 与 `Order.Ring` 上运行 GCN 5-seed grouped training 对照。

## Why Now
先用强欧氏 baseline 验证 grouped training 入口稳定，再比较双曲模型。

## Allowed Files
- new artifacts under `artifacts/baselines/relation_seed_sweeps/`
- related configs under `project_bootstrap/**/configs`
- `docs/experiment_reports/gcn_grouped_training.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`

## Forbidden Scope
- 不改 HGCN 代码
- 不改变 T31 定义的协议
- 不覆盖历史 artifact

## Inputs to Read
- `docs/06_eval_protocol.md`
- T31 implementation and review
- candidate configs for Field.Subfield and Order.Ring

## Expected Output
- GCN 5-seed mean ± std 报告。
- grouped 指标与 hop bucket 结果。
- 运行命令与 artifact 路径。

## Verification
```powershell
Get-ChildItem artifacts\baselines\relation_seed_sweeps
rg -n "mean|std|Recall|MAP|nDCG|grouped|hop" docs\experiment_reports\gcn_grouped_training.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
adversarial
