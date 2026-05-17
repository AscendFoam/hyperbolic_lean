# Review: T33

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

1. **报告未显式列出 HGCN 与 GCN 配置差异清单。** 任务包要求"明确列出 HGCN 配置与 GCN 配置之间的唯一差异"。报告中写了"using the same grouped protocol and seed list"和"HGCN did not overtake T32 GCN"，但未逐字段列出 HGCN 独有字段（`model_variant`、`distance_signal_mode`、`distance_stat_momentum`、`residual_gate_init`、`curvature`、`decoder_hidden_dim`、`grad_clip_norm`）以及它们与 T32 GCN config 的对应关系。经 review 逐字段 diff 验证，除上述 HGCN 模型字段和 `run_id`/`model_type`/`artifacts_root` 等身份字段外，两组 config 完全一致。因此不阻塞，但后续汇总报告（如 T34）可补入显式 diff 表。

2. **R24 条目中英混杂。** `docs/08_risks_and_open_questions.md` 新增的 R24 标题为英文（"T33 protocol mismatch risk closed after matched grouped HGCN sweep"），描述也以英文为主，而表中其余条目均为中文。建议后续精修时统一为中文标题和描述。

3. **报告未显式写出可比性约束声明。** 任务包要求"报告中应明确写出与 T32 的可比性约束，避免把局部绝对数值直接解读成优劣结论"。报告中通过 Scope 隐式传达了可比性（同 protocol、同 seed、同 loss），Notes 也正确写了"HGCN did not overtake T32 GCN"，但缺少一段显式的"本报告结果仅在 T32 matched protocol 下可比较，不可直接用绝对数值做跨协议优劣判断"式声明。不阻塞，因为结论正确且未出现过度声称。

## Missing Tests

None. 任务类型为实验 sweep 而非代码变更；验证方式为 artifact 产物检查与报告字段核验，均已通过。

## Suspicious Implementation Details

None. 以下要点已逐一验证：

1. **配置可比性**：逐字段 diff T32 GCN base config 与 T33 HGCN base config（两张图各一组），排除 HGCN 模型特有字段和身份字段后完全一致。
2. **artifact 完整性**：两组 sweep 各含 5 个 seed 子目录、`aggregate.json`、`per_seed_results.csv`、`per_seed_results.json`、`report.md`；`failed_runs = []`。
3. **报告数值**：Aggregate Metrics 和 Hop Buckets 中所有 mean ± std 值与 `aggregate.json` 逐字段核对一致。
4. **协议字段**：单 seed `result_summary.json` 包含 `training_loss = sampled_softmax`、`query_key_fields = [src_id, relation_type]`、`query_split_summary.is_query_level_disjoint = true`，与 T32 口径一致。
5. **Allowed files**：T33 worker 的所有变更均限于 Allowed files 范围内（4 个新 config、1 个新报告、3 个治理文档更新）。工作树中其余变更（`CLAUDE.md`、`docs/00_raw_idea.md`、`docs/05_decision_log.md` 等）属于 Captain 在 T32→T33 过渡期间的历史改动，非 T33 worker 所为。

## Recommended Next Action

Captain 可将 T33 标记完成，当前唯一任务切换到 T34（汇总 grouped training 与旧 binary training 的差异，写入诊断报告）。T34 可在此 review 的 Non-blocking issue 1 基础上补入显式 GCN vs HGCN config diff 表。
