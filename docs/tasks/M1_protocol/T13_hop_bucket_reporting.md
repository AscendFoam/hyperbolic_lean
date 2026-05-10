# T13 Hop Bucket Reporting

## Task ID
T13

## Goal
增加或校验 hop bucket 常规报告入口，确保 `hop_2 / hop_3 / hop_4_plus` 出现在正式 grouped retrieval 结果中。

## Why Now
双曲价值可能只出现在更深 hop bucket；没有 hop 分桶就无法验证条件性结论。

## Allowed Files
- relevant evaluation/reporting code under `project_bootstrap/baseline_scaffold/src`
- relevant configs under `project_bootstrap/**/configs`
- `docs/06_eval_protocol.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`

## Forbidden Scope
- 不改训练目标
- 不重跑大规模 sweep，除非任务包后续显式要求
- 不把单次 dry-run 写成正式结果

## Inputs to Read
- `docs/06_eval_protocol.md`
- `project_bootstrap/baseline_scaffold/src/relation_tasks.py`
- `project_bootstrap/baseline_scaffold/src/eval_utils.py`
- existing grouped retrieval artifact summaries

## Expected Output
- hop bucket 指标在报告中可见，或明确记录阻塞原因。
- 文档说明 hop bucket 的定义和边界。

## Verification
```powershell
rg -n "hop_2|hop_3|hop_4_plus|hop" project_bootstrap\baseline_scaffold\src docs\06_eval_protocol.md
```

## Docs to Update
- `docs/06_eval_protocol.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md` if blocked

## Reviewer Type
adversarial
