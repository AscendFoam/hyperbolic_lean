# T01 Governance Consistency Review

## Task ID
T01

## Goal
审查并校正 `docs/00~08`、`docs/tasks`、根目录入口文档之间的一致性，确保后续 worker 可以按 `Current Unique Task` 直接开工。

## Why Now
T00 完成后，治理入口会从 docs 扩展到根目录。需要在进入数据和协议任务前消除冲突、过期描述和任务边界不清。

## Allowed Files
- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/reference/AI_coding_workflow.md`
- `docs/for_human/T00_explained.md`
- `docs/tasks/**`
- `README.md`
- `AGENTS.md`
- `CLAUDE.md`

## Forbidden Scope
- 不修改 `docs/02_experiment_plan.md`
- 不修改代码、configs 或 artifacts
- 不标记未 review 的任务为完成

## Inputs to Read
- `docs/reference/AI_coding_workflow.md`
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/tasks/M0_governance/T00_root_project_docs.md`
- `docs/review/T00_review.md`
- `docs/for_human/T00_explained.md`
- T00 worker final report and review, if available

## Expected Output
- 一致性修订后的治理文档。
- `docs/04_task_board.md` 中仅由 Captain 根据 review 标记 T00 状态。
- 若发现需暂缓的问题，写入 `docs/08_risks_and_open_questions.md`。

## Verification
```powershell
rg -n "证明双曲优于|已证明|Current Unique Task|Allowed files|Forbidden scope|docs/reference/AI_coding_workflow.md" docs README.md AGENTS.md CLAUDE.md
git diff -- docs README.md AGENTS.md CLAUDE.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/05_decision_log.md` if a governance decision changes

## Reviewer Type
normal
