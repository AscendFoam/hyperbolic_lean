# T34 Grouped Training Summary

## Task ID
T34

## Goal
基于已完成的 `T32`/`T33` grouped 5-seed sweep 与历史 binary training 材料，形成一份可审查的诊断总结，明确：

- grouped protocol 相对旧 binary protocol 的关键变化；
- matched grouped protocol 下 `GCN` 与 `HGCN` 的对照结果；
- 结论中哪些是 accepted、哪些是 inconclusive、哪些应 deferred。

## Why Now
`T32` 与 `T33` 都已通过 review，matched grouped protocol 下的 GCN/HGCN 对照已经收口。下一步不是继续跑实验，而是把 grouped-vs-binary 的协议差异、可比性边界和诊断结论收束成正式报告，作为 Milestone 3 的总结入口。

## Allowed files
- `docs/experiment_reports/grouped_training_summary.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden scope
- 不新增实验，不重跑任何 seed sweep，不生成新 artifact。
- 不修改 `T32` / `T33` / 历史 binary 报告中的既有数值。
- 不改训练代码、runner、config、seed、split 或协议实现。
- 不把跨协议绝对数值直接写成优劣判断。
- 不修改 `docs/02_experiment_plan.md`。

## Inputs to Read
- `docs/reference/AI_coding_workflow.md`
- `docs/02_experiment_plan.md`
- `docs/06_eval_protocol.md`
- `docs/review/T32_review.md`
- `docs/review/T33_review.md`
- `docs/experiment_reports/gcn_grouped_training.md`
- `docs/experiment_reports/hgcn_grouped_training.md`
- 历史 binary training 相关报告与汇总文档
- 相关 `T32` / `T33` config 文件，用于核对显式 diff 表

## Expected Output
在 `docs/experiment_reports/grouped_training_summary.md` 中至少包含：

1. Scope / comparability statement  
   明确写出：`T32` 与 `T33` 只在 matched grouped protocol 下可比较；grouped 与旧 binary 仅能做 protocol-level 对比，不能用绝对数值直接判断模型优劣。

2. grouped vs binary protocol diff  
   总结旧 binary edge classification 与 grouped multi-positive ancestor retrieval 的关键差异。

3. explicit GCN vs HGCN config diff table  
   明确列出 `T33 review` 点名的差异项，并说明除模型身份字段与 HGCN 特有字段外，其余配置保持一致。

4. result summary  
   同时覆盖 `Order.Ring` 与 `Field.Subfield`，并保留 controlled probe / primary candidate 的解释边界。

5. conclusion buckets  
   用 `accepted` / `inconclusive` / `deferred` 标记主要结论或后续事项。

## Verification
```powershell
rg -n "config diff|可比性|binary|grouped|GCN|HGCN|Order.Ring|Field.Subfield|accepted|inconclusive|deferred" docs\experiment_reports\grouped_training_summary.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
milestone
