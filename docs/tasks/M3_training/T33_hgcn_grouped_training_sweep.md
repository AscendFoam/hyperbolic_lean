# T33 HGCN Grouped Training Sweep

## Task ID
T33

## Goal
在相同 split 和参数预算下运行 HGCN 5-seed grouped training 对照。

## Why Now
只有在 GCN grouped training 站稳后，HGCN 对照才有解释价值。

## Allowed Files
- new artifacts under `artifacts/baselines/relation_seed_sweeps/`
- related configs under `project_bootstrap/**/configs`
- `docs/experiment_reports/hgcn_grouped_training.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`

## Forbidden Scope
- 不修改 GCN 结果
- 不调参到不可比
- 不把局部偶然收益写成稳定结论

## Inputs to Read
- T32 report and review
- `docs/06_eval_protocol.md`
- HGCN grouped configs

## Expected Output
- HGCN 5-seed mean ± std 报告。
- 与 T32 使用相同数据、split、候选和指标。

## Verification
```powershell
rg -n "mean|std|Recall|MAP|nDCG|grouped|hop|GCN|HGCN" docs\experiment_reports\hgcn_grouped_training.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
adversarial
