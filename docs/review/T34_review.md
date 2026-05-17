# Review: T34

> Reviewer: Claude Code (milestone)
> Date: 2026-05-17
> Task package: `docs/tasks/M3_training/T34_grouped_training_summary.md`

## Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

1. **D024 条目中英混杂。** `docs/05_decision_log.md` 新增的 D024 使用英文撰写（`Date`、`Status`、`Basis`、`Decision`、`Consequence`），而表中其余条目（D001–D023）均为中文格式（日期、状态、依据、决策、后果）。此外 D024 的 `Status` 字段使用 `Drafted for review` 而非与其他条目一致的 `Accepted`。建议后续精修时统一为中文格式和 Accepted 状态。

2. **报告 Section 5 缺少 Recall@1/3/5/10 对比列。** T32 和 T33 原始报告中都记录了完整的 Recall@1/3/5/10，但 T34 汇总表只展示了 grouped MAP、nDCG、nDCG@10 和 delta。这不影响主要结论（MAP 和 nDCG 已经足够判断 GCN 领先），但遗漏了 Recall 维度的汇总信息。

3. **Section 6 历史数值来源未引用具体文件名。** 报告说 "The older phase summary dated 2026-05-02 reported..."，但没有给出具体文件路径。读者需要自行搜索才能找到 `docs/阶段总结（2026-05-02，grouped retrieval training）.md`。建议补充来源文件名或链接。

4. **08_risks_and_open_questions.md 底部的 T34 Worker Draft Note 使用全英文。** 其余治理文档中新增的 Worker Draft Note / Update 也使用英文，与文件主体语言不一致。不影响结论正确性，但降低了中文文档的可读性。

## Missing Tests

None. T34 是 summary-only 文档任务，不涉及代码变更。验证方式为文档字段检查和数值交叉核验，均已通过。

## Suspicious Implementation Details

None. 以下核验全部通过：

1. **Allowed files 合规**：worker 只修改了 `docs/04_task_board.md`、`docs/05_decision_log.md`、`docs/07_handoff.md`、`docs/08_risks_and_open_questions.md`，并新增了 `docs/experiment_reports/grouped_training_summary.md`。无源代码变更（`git diff HEAD -- project_bootstrap/baseline_scaffold/src/` 为空）。

2. **任务包要求的五项输出全部存在**：
   - Scope / comparability statement → Section 2
   - grouped vs binary protocol diff → Section 3
   - explicit GCN vs HGCN config diff table → Section 4
   - result summary 覆盖 Order.Ring 与 Field.Subfield → Section 5
   - conclusion buckets（accepted / inconclusive / deferred）→ Section 7

3. **数值交叉核验**：
   - T34 报告中的 GCN Field.Subfield grouped MAP `0.4839 ± 0.0783` 与 `gcn_grouped_training.md` 一致。
   - T34 报告中的 HGCN Field.Subfield grouped MAP `0.4458 ± 0.1150` 与 `hgcn_grouped_training.md` 一致。
   - T34 报告中的 GCN Order.Ring grouped MAP `0.5789 ± 0.0346` 与 `gcn_grouped_training.md` 一致。
   - T34 报告中的 HGCN Order.Ring grouped MAP `0.5616 ± 0.0312` 与 `hgcn_grouped_training.md` 一致。
   - 所有 nDCG、nDCG@10 数值也与原始报告逐字段匹配。
   - HGCN MRR 略高（`0.6123` vs `0.6101`）的观察与 T33 报告一致。

4. **历史数值可溯源**：Section 6 引用的 binary gMAP 和 grouped gMAP 数值（`0.144, 0.321, 0.104, 0.299, 0.208, 0.291, 0.148`）均可追溯至 `docs/阶段总结（2026-05-02，grouped retrieval training）.md`，且数值完全匹配。

5. **Config diff 表正确**：Section 4 列出的 HGCN 特有字段（`model_variant`、`distance_signal_mode`、`distance_stat_momentum`、`residual_gate_init`、`decoder_hidden_dim`、`curvature`、`grad_clip_norm`）与 T33 review 的逐字段 diff 核验一致。

6. **无 Forbidden scope 违规**：未新增实验、未修改 T32/T33 结果、未修改训练代码或协议实现、未修改 `docs/02_experiment_plan.md`。

7. **验证命令通过**：`rg -n "config diff|可比性|binary|grouped|GCN|HGCN|Order.Ring|Field.Subfield|accepted|inconclusive|deferred"` 在报告中命中所有关键词。

8. **可比性边界正确**：
   - T32 vs T33 被正确标记为"matched grouped protocol 下直接可比"。
   - 历史 grouped-vs-binary 被正确标记为"alignment evidence, not directly interchangeable baselines"。
   - 报告未出现任何跨协议直接优劣比较。

## Scope Compliance

| check | result |
| --- | --- |
| Only allowed files modified/created | PASS — 4 个治理文档更新 + 1 个新报告，均在 allowed 范围内 |
| No new experiments run | PASS — 无 sweep artifact 变更，无源代码变更 |
| No T32/T33 results rewritten | PASS — 所有数值与 reviewed 报告一致 |
| No code or protocol changes | PASS — `git diff HEAD -- project_bootstrap/` 为空 |
| No `docs/02_experiment_plan.md` edit | PASS — 该文件未变更 |

## Recommended Next Action

Captain 可将 T34 标记完成，Milestone 3 闭合。当前唯一任务可切换到 T40（冻结 `explicit-only / synthesized-only / mixed` 三类图的生成配置与输出位置），进入 Milestone 4 relation provenance split。

Non-blocking issues 可在后续文档精修中处理：D024 中英统一、Section 6 来源文件引用补充、Section 5 Recall 汇总补充。
