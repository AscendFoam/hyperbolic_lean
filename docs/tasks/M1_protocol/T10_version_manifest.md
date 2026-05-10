# T10 Version Manifest

## Task ID
T10

## Goal
生成版本锁定与数据资产 manifest，列出当前正式实验依赖的 Lean、Mathlib、LeanDojo、Python 依赖、关键 config、脚本和 artifact 路径。

## Why Now
协议和数据不冻结，后续 seed sweep、诊断和论文结果无法复现。

## Allowed Files
- `docs/data_manifest.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不重新运行 trace 或训练
- 不修改 `project_bootstrap/`
- 不声称无法验证的版本已经锁定

## Inputs to Read
- `docs/02_experiment_plan.md`
- `project_bootstrap/**/README.md`
- `artifacts/README.md`
- existing configs under `project_bootstrap/**/configs`

## Expected Output
- `docs/data_manifest.md`，包含 version manifest、config index、artifact index 和 unknowns。
- 未知版本必须标为 `unknown / needs verification`，不能编造。

## Verification
```powershell
rg -n "unknown|needs verification|Lean|Mathlib|config|artifact" docs\data_manifest.md
git diff -- docs\data_manifest.md docs\04_task_board.md docs\07_handoff.md docs\08_risks_and_open_questions.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
normal
