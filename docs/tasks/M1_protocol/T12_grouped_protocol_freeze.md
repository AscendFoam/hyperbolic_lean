# T12 Grouped Protocol Freeze

## Task ID
T12

## Goal
固化 grouped multi-positive ancestor retrieval 协议，确认代码入口、配置字段、指标名和输出格式。

## Why Now
这是后续所有正式结果的任务口径。若协议仍只存在于文档，模型对照无法成为 benchmark。

## Allowed Files
- `docs/06_eval_protocol.md`
- `docs/grouped_retrieval_protocol.md`
- relevant config files under `project_bootstrap/**/configs`
- relevant evaluation/reporting code under `project_bootstrap/baseline_scaffold/src`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不大改模型架构
- 不新增 unrelated task
- 不删除旧结果

## Inputs to Read
- `docs/06_eval_protocol.md`
- `docs/阶段总结（2026-05-01，grouped ancestor retrieval）.md`
- `project_bootstrap/baseline_scaffold/src/relation_tasks.py`
- `project_bootstrap/baseline_scaffold/src/eval_utils.py`
- grouped retrieval configs and artifacts

## Expected Output
- 文档化 grouped protocol。
- 若代码字段不一致，做最小修正或记录 blocker。
- 输出格式能包含 Recall@k、MAP、nDCG、grouped-MRR。

## Verification
```powershell
rg -n "grouped|Recall@|MAP|nDCG|MRR|hop" project_bootstrap\baseline_scaffold\src docs\06_eval_protocol.md docs\grouped_retrieval_protocol.md
```

## Docs to Update
- `docs/06_eval_protocol.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
adversarial
