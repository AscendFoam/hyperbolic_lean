# T52 Proof-Side Demo Package

## Task ID
T52

## Goal
为 proof-side utility 写最小 demo 任务包，不承诺端到端 theorem proving。

## Why Now
选定 MVP 后，需要把它拆成 worker 可实现的工程任务。

## Allowed Files
- `docs/tasks/M5_paper/T52a_*`
- `docs/proof_side_mvp.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`

## Forbidden Scope
- 不直接实现 demo
- 不修改代码
- 不扩大到多个 proof-side 任务

## Inputs to Read
- T51 output and review
- `docs/reference/AI_coding_workflow.md`
- `docs/06_eval_protocol.md`

## Expected Output
- 一个或多个后续 worker 任务包，包含 Allowed files、Verification、Reviewer type。

## Verification
```powershell
Get-ChildItem docs\tasks\M5_paper
rg -n "Task ID|Allowed Files|Verification|Reviewer Type" docs\tasks\M5_paper
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`

## Reviewer Type
normal
