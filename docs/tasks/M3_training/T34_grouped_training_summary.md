# T34 Grouped Training Summary

## Task ID
T34

## Goal
汇总 grouped training 与旧 binary training 的差异，写入诊断报告。

## Why Now
训练目标对齐的价值需要被解释，而不是只留下分散 artifact。

## Allowed Files
- `docs/experiment_reports/grouped_training_summary.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不新增实验
- 不挑选单 seed 做结论
- 不夸大双曲收益

## Inputs to Read
- T30, T31, T32, T33 reports and reviews
- historical binary training summaries
- grouped retrieval artifacts

## Expected Output
- grouped vs binary training 对比报告。
- 明确 accepted / inconclusive / deferred 结论。

## Verification
```powershell
rg -n "binary|grouped|mean|std|conclusion|inconclusive|deferred" docs\experiment_reports\grouped_training_summary.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
milestone
