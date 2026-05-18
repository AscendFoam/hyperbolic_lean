# T52 Proof-Side Demo Package

## Task ID
T52

## Goal
基于 `T51` 已选定的 ancestor explanation MVP，写出一个可直接派发给后续 worker 的最小 demo 实现任务包；本任务只做任务分解与边界冻结，不实现 demo，也不承诺端到端 theorem proving。

## Why Now
`T51` 已完成候选比较、正式选定 ancestor explanation，并在 review 中关闭了“它是否过轻”的核心质疑。当前最需要的不是继续讨论方向，而是把后续 demo 的实现边界写窄、写实、写成可以直接执行的 worker task package，避免下一轮在代码实现前再次自行扩 scope。

## Allowed Files
- `docs/tasks/M5_paper/T52a_ancestor_explanation_demo.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不直接实现 demo
- 不修改代码
- 不新增实验，不重训练模型，不补跑 artifact
- 不引入 LeanDojo 或其他大型新依赖
- 不把 ancestor explanation 扩大成多个 proof-side 任务并行开发
- 不改写 `T50`/`T51` 已确认的 provenance-conditional 口径
- 不把 demo 写成“已证明可提升完整证明成功率”或端到端 theorem proving
- 不产出多个 competing downstream task packages；只产出一个主实现任务包

## Inputs to Read
- `docs/proof_side_mvp.md`
- `docs/review/T51_review.md`
- `docs/paper_outline.md`
- `docs/reference/AI_coding_workflow.md`
- `docs/06_eval_protocol.md`
- `docs/experiment_reports/provenance_seed_sweeps.md`
- `docs/experiment_reports/provenance_summary.md`
- `project_bootstrap/baseline_scaffold/src/relation_baseline_common.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_gcn_baseline.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_hyperbolic_baseline.py`

## Expected Output
- 新建 `docs/tasks/M5_paper/T52a_ancestor_explanation_demo.md`，作为后续真正实现 demo 的唯一下游 worker 任务包。
- 该任务包必须明确：
- 推荐代码入口和允许修改的精确文件范围
- 允许依赖的 reviewed artifacts / checkpoints / reports
- CLI 输入、输出格式、provenance-aware comparison mode 和最小可见验收场景
- 明确禁止 shortcut：不重训、不伪造 demo 数据、不把输出退化成纯祖先列表
- 可执行的 verification 命令和 reviewer type
- 同步更新治理文档，使 `T52` 处于“worker 已起草、等待 review”的一致状态，但不要自行标记 `T52` 完成。

## Verification
```powershell
rg -n "Task ID|Goal|Why now|Allowed files|Forbidden scope|Inputs to read|Expected output|Verification|Docs to update|Reviewer type" docs\tasks\M5_paper\T52a_ancestor_explanation_demo.md
rg -n "ancestor explanation|explicit_only|hierarchy_mixed|CLI|artifact|comparison|no new dependencies|no retraining" docs\tasks\M5_paper\T52a_ancestor_explanation_demo.md
rg -n "T52|T52a|Current Unique Task|proof-side|demo" docs\04_task_board.md docs\05_decision_log.md docs\07_handoff.md docs\08_risks_and_open_questions.md docs\tasks\M5_paper\T52a_ancestor_explanation_demo.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
normal
