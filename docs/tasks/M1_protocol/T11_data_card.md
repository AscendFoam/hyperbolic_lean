# T11 Data Card

## Task ID
T11

## Goal
写出当前可用图和数据资产的 data card，说明字段、relation 类型、coverage-aware 处理、unresolved 语义和使用限制。

## Why Now
后续协议和模型任务必须知道哪些图能作为正式 benchmark，哪些只能作为历史探索产物。

## Allowed Files
- `docs/data_card.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不改数据文件
- 不重算 artifacts
- 不把 coverage 不可靠的数据写成可靠标签

## Inputs to Read
- `docs/data_manifest.md`
- `data/processed/**/README.md`
- `artifacts/diagnostics/*/report.md`
- `docs/02_experiment_plan.md`

## Expected Output
- `docs/data_card.md`，覆盖图列表、字段说明、relation provenance、known limitations、recommended usage。

## Verification
```powershell
rg -n "unresolved|coverage|relation|extends|instance_of|recommended usage" docs\data_card.md
git diff -- docs\data_card.md docs\04_task_board.md docs\07_handoff.md docs\08_risks_and_open_questions.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
normal
