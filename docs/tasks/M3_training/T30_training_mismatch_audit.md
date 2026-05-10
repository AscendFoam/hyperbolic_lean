# T30 Training Mismatch Audit

## Task ID
T30

## Goal
读取现有 grouped retrieval training 代码，定位 binary edge classification 与 grouped retrieval 的错配点。

## Why Now
在实现新 loss 前，必须先知道当前训练和评测在哪里不一致，避免盲目大改。

## Allowed Files
- `docs/training_alignment_audit.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不修改训练代码
- 不运行长 sweep
- 不提出未验证性能结论

## Inputs to Read
- `project_bootstrap/baseline_scaffold/src/relation_tasks.py`
- `project_bootstrap/baseline_scaffold/src/relation_baseline_common.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_gcn_baseline.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_hyperbolic_baseline.py`
- existing grouped retrieval summaries

## Expected Output
- `docs/training_alignment_audit.md`，列出当前 loss、batch/query 结构、negative sampling、eval 入口和最小改造点。

## Verification
```powershell
rg -n "BCE|loss|grouped|query|negative|mismatch" docs\training_alignment_audit.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
normal
