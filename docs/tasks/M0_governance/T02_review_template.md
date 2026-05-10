# T02 Review Template

## Task ID
T02

## Goal
建立 `docs/review/` 的 review 模板，并记录治理初始化 review 的文件命名规则。

## Why Now
后续每个 worker 任务都需要可审查、可归档的 reviewer 输出。先固化模板可以减少后续 review 格式漂移。

## Allowed Files
- `docs/review/README.md`
- `docs/review/TEMPLATE_review.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`

## Forbidden Scope
- 不修改代码
- 不新增真实 review 结论，除非已有 reviewer 报告
- 不修改 `docs/02_experiment_plan.md`

## Inputs to Read
- `docs/reference/AI_coding_workflow.md`
- `docs/04_task_board.md`
- `CLAUDE.md`

## Expected Output
- `docs/review/README.md` 说明 review 文件命名、verdict 和归档规则。
- `docs/review/TEMPLATE_review.md` 包含 Verdict、Blocking issues、Non-blocking issues、Missing tests、Suspicious details、Recommended next action。

## Verification
```powershell
Get-ChildItem docs\review
git diff -- docs\review docs\04_task_board.md docs\07_handoff.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`

## Reviewer Type
normal
