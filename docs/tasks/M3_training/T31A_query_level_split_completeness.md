# T31A Query-Level Split Completeness

## Task ID
T31A

## Goal
实现并校验 `ancestor_ranking` / grouped ancestor retrieval 的 query-level split，使同一 `(src, relation)` query 的全部 positive ancestors 不跨 `train / val / test`。

## Why Now
`T30` 已确认当前 split 按正例边切分，而不是按 `(src, relation)` query 切分。只要这个问题存在，val/test grouped retrieval 可能缺少完整 positive set；直接进入 `T31` query-grouped loss 会把新训练目标接到不可靠的 split 上。

## Allowed Files
- `project_bootstrap/baseline_scaffold/src/relation_tasks.py`
- `project_bootstrap/baseline_scaffold/src/relation_baseline_common.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_gcn_baseline.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_hyperbolic_baseline.py`
- one new or updated smoke config under `project_bootstrap/baseline_scaffold/configs`
- `docs/training_alignment_audit.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不实现 query-grouped loss；该工作仍留给 `T31`
- 不运行长 seed sweep
- 不改 GCN / HGCN 架构
- 不把 smoke 结果写成正式 benchmark 结论
- 不重写 unrelated task families such as `parent_prediction`

## Inputs to Read
- `docs/training_alignment_audit.md`
- `docs/06_eval_protocol.md`
- `project_bootstrap/baseline_scaffold/src/relation_tasks.py`
- `project_bootstrap/baseline_scaffold/src/relation_baseline_common.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_gcn_baseline.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_hyperbolic_baseline.py`

## Expected Output
- A query-level split path for `ancestor_ranking` / grouped ancestor retrieval.
- A validation helper, assertion, or report field proving no `(src, relation)` query appears in more than one split for the grouped path.
- Minimal smoke or static verification showing the grouped split path is wired into at least one existing config / runner path.
- Documentation update explaining whether `T31` can now safely focus on grouped loss.

## Verification
```powershell
rg -n "query.*split|split.*query|src.*relation|ancestor_ranking|grouped" project_bootstrap\baseline_scaffold\src docs\training_alignment_audit.md
```

If the Python environment supports it, also run a minimal smoke command or targeted unit-style script that constructs the split and verifies disjoint `(src, relation)` query keys across `train / val / test`. If the environment does not support execution, state the blocker and provide static evidence.

## Docs to Update
- `docs/training_alignment_audit.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
adversarial
