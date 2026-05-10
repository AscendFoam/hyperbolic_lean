# T43 Provenance Summary

## Task ID
T43

## Goal
汇总 provenance split 结果，回答 synthesized relation 是否削弱双曲优势。

## Why Now
Milestone 4 的研究价值在于结构性解释，而不是分散的诊断和 seed sweep。

## Allowed Files
- `docs/experiment_reports/provenance_summary.md`
- `docs/05_decision_log.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不新增实验
- 不把 inconclusive 写成 positive finding
- 不隐藏负结果

## Inputs to Read
- T40, T41, T42 outputs and reviews
- `docs/02_experiment_plan.md`
- `docs/08_risks_and_open_questions.md`

## Expected Output
- synthesized relation 影响的结论分类：supported / partially supported / inconclusive / rejected。
- 后续 Continue / Narrow 建议。

## Verification
```powershell
rg -n "supported|inconclusive|synthesized|explicit|mixed|Continue|Narrow" docs\experiment_reports\provenance_summary.md
```

## Docs to Update
- `docs/05_decision_log.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
milestone
