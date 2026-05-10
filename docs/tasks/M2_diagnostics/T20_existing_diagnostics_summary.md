# T20 Existing Diagnostics Summary

## Task ID
T20

## Goal
复查现有 diagnostics 产物，形成候选图优先级表。

## Why Now
后续训练不应盲目扩图，应先知道哪些图过浅，哪些图值得检验双曲条件性价值。

## Allowed Files
- `docs/diagnostics_summary.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不重跑 diagnostics
- 不修改 artifacts
- 不把诊断估计写成精确定理

## Inputs to Read
- `artifacts/diagnostics/real_graphs_v1/report.md`
- `artifacts/diagnostics/hierarchy_focus_v1/report.md`
- `artifacts/diagnostics/mathlib_order_focus_v1/report.md` if present
- `docs/02_experiment_plan.md`

## Expected Output
- `docs/diagnostics_summary.md`，包含图列表、关键结构指标、浅层/更深判断、候选优先级。

## Verification
```powershell
rg -n "longest chain|leaf|candidate|priority|shallow|forest" docs\diagnostics_summary.md
git diff -- docs\diagnostics_summary.md docs\04_task_board.md docs\07_handoff.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
normal
