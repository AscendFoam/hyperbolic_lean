# T43 Provenance Summary

## Task ID
T43

## Goal
汇总 T41 的 provenance 结构诊断与 T42 的 provenance-aware seed sweeps，正式回答 synthesized relation 是否削弱 hyperbolic advantage，并把 Milestone 4 结论收束成可进入后续论文/utility 规划的 reviewed summary。

## Why Now
T40/T41/T42 已经把 provenance split 的协议冻结、结构诊断和受约束模型对比全部做完。现在缺的不是更多训练，而是把这些结果统一成一个精确、可复述、不过度外推的结论：HGCN 的优势不是整体成立，而是只在 explicit hierarchy 层上成立；synthesized 边不会增加层级深度，但会在 mixed graph 中稀释这类优势。

## Allowed Files
- `docs/experiment_reports/provenance_summary.md`
- `docs/05_decision_log.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不要新增训练、seed sweep、split 生成或结构诊断运行
- 不要修改 T40/T41/T42 的 frozen protocol、graph semantics、artifact 数值或 config
- 不要把 `synthesized_only` 的结果写成 primary model-comparison evidence
- 不要把尚未核清的 aggregate / per-seed 口径差异写成“已解决事实”
- 不要重写 `docs/02_experiment_plan.md`

## Inputs to Read
- `docs/review/T41_review.md`
- `docs/review/T42_review.md`
- `docs/experiment_reports/provenance_diagnostics.md`
- `docs/experiment_reports/provenance_seed_sweeps.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/08_risks_and_open_questions.md`
- `docs/02_experiment_plan.md`

## Expected Output
- 新增 `docs/experiment_reports/provenance_summary.md`，至少明确写出：
  - `explicit_only` 是 primary evidence，且 HGCN 仅在该 split 上稳定领先
  - `synthesized_only` 是 trivial controlled diagnostic，不支持主模型结论
  - `hierarchy_mixed` 是 full source graph reproducibility check，而不是新的图族发现
  - synthesized relation 的作用是结构性稀释，而不是贡献层级深度
  - 项目结论应从“GCN overall ahead”精化为“GCN 在 mixed graph 上仍领先，HGCN 只在 explicit-only hierarchy 上显现优势”
- 同步更新风险/决策/任务板/handoff，使 T43 完成后项目可切换到 Milestone 5 的下一任务准备态

## Required Precision Notes
- 必须显式注明 `Field.Subfield explicit_only` 的 `hop_4_plus` 均值基于 4/5 seeds，而不是默认 5/5
- 必须把 `synthesized_only` 中 GCN aggregate 与 per-seed 记录的口径差异登记为待核清项
- 必须避免把上述精度问题写成 blocking 或推翻主结论；它们影响的是表述精度，不改变 provenance-conditional 结论

## Verification
```powershell
rg -n "explicit_only|synthesized_only|hierarchy_mixed|primary evidence|controlled diagnostic|reproducibility check|4/5 seeds|aggregate|per-seed|conditional" docs\experiment_reports\provenance_summary.md
rg -n "T43|provenance_summary|T42 已通过|Current Unique Task|R28|conditional" docs\04_task_board.md docs\05_decision_log.md docs\07_handoff.md docs\08_risks_and_open_questions.md
```

## Docs to Update
- `docs/05_decision_log.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
milestone
