# T14 M1 Smoke Check And Cleanup

## Task ID
T14

## Goal
做 Milestone 1 收口 smoke check 与轻量清理，确认 grouped / hop bucket 协议字段在最小运行或静态样例中实际落盘。

## Why Now
T12/T13 已经通过 adversarial review，协议字段和 hop bucket 报告入口已收口。但 T13 review 明确指出没有端到端运行，且存在少量 helper duplication。进入 Milestone 2 诊断筛图前，应先用窄范围任务补上可复查的 smoke 证据，并在不扩大范围的前提下清理最明显的重复。

## Allowed Files
- relevant evaluation/reporting code under `project_bootstrap/baseline_scaffold/src`
- relevant small/smoke config files under `project_bootstrap/**/configs`
- smoke output under `artifacts/smoke/` or `artifacts/manual_checks/`
- `docs/06_eval_protocol.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不改训练目标
- 不新增模型架构
- 不跑大规模 seed sweep
- 不把 smoke output 写成正式 benchmark 结果
- 不修改 `docs/02_experiment_plan.md`

## Inputs to Read
- `docs/06_eval_protocol.md`
- `docs/review/T13_review.md`
- `project_bootstrap/baseline_scaffold/src/relation_baseline_common.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_gcn_baseline.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_hyperbolic_baseline.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_grouped_retrieval_baseline.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_seed_sweep.py`
- `project_bootstrap/baseline_scaffold/src/_patch_sweep_reports.py`

## Expected Output
- 一个可复查的最小 smoke check，确认 `grouped_test_ndcg_at_10` 与 `hop_2 / hop_3 / hop_4_plus` 字段能在输出链中出现；如果当前机器无法运行，明确记录依赖或数据 blocker。
- 在范围允许时，轻量减少 T13 review 指出的 helper duplication；如果清理会扩大范围，则只记录 deferred item。
- `docs/06_eval_protocol.md` 和 handoff 文档说明 smoke output 不是正式 benchmark 结果。

## Verification
```powershell
rg -n "grouped_test_ndcg_at_10|hop_2_map|hop_3_map|hop_4_plus_map|flatten_grouped_hop_bucket_summary" project_bootstrap\baseline_scaffold\src docs\06_eval_protocol.md
```

还应运行一个可行的最小 smoke 命令，或明确说明为什么当前机器无法运行。

## Docs to Update
- `docs/06_eval_protocol.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md` if smoke check is blocked or helper cleanup is deferred

## Reviewer Type
normal
