# Training Alignment Audit

> 更新时间：2026-05-13
>
> 状态：T30 reviewed audit + T31A reviewed split fix + T31 reviewed minimal grouped-loss path。本文保留 T30 的只读错配审计，补充 T31A 对 query-level split completeness 的修复状态，并记录 T31 最小 grouped-loss 路径的实现边界；不把 smoke 结果写成正式 benchmark 结论。

## 1. Scope

本审计只覆盖当前 relation-aware GCN / HGCN 的训练与评测对齐情况。

已审计输入：

- `project_bootstrap/baseline_scaffold/src/relation_tasks.py`
- `project_bootstrap/baseline_scaffold/src/relation_baseline_common.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_gcn_baseline.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_hyperbolic_baseline.py`
- 现有 grouped retrieval summary / result artifacts

本审计不做的事：

- 不实现新 loss
- 不改 split
- 不改 negative sampling
- 不运行任何长训练或 seed sweep

## 2. Current Code Path

当前 `ancestor_ranking` 的代码路径实际上分成两段：

1. **训练数据构造仍是逐边 binary**
   - `build_ancestor_task_examples_with_hops(...)` 先生成 closure 正例边 `(src, dst, relation)`。
   - `stratified_split_relation_examples(...)` 再把这些正例边按 `relation_type` 分层切成 `train / val / test`。
   - `sample_negative_relation_examples(...)` 以“每条正例边”为中心采样负例。
   - `write_relation_split_csv(...)` 落盘的是边级二分类样本。

2. **评测已经是 grouped retrieval**
   - `build_grouped_ranking_queries(...)` 在评测阶段才把样本按 `(src, relation)` 聚成 grouped query。
   - `build_grouped_ranking_metrics(...)` 计算 `MAP / nDCG / nDCG@10 / grouped-MRR / Recall@k / hop buckets`。
   - GCN / HGCN runner 都会把 grouped test 指标写入 `metrics.json` 与 `result_summary.json`。

换句话说，当前实现是：

```text
edge-level BCE training -> binary AP/AUROC checkpoint selection -> post-hoc grouped retrieval evaluation
```

## 3. What Is Already Aligned

先说清楚当前已经做对的部分，避免把所有问题混在一起：

1. grouped retrieval 指标与 hop bucket 已经有稳定代码入口，且 GCN / HGCN runner 的输出字段已对齐。
2. `task = ancestor_ranking` 虽然是 legacy key，但当前协议下已经被明确映射为 grouped multi-positive ancestor retrieval。
3. 负采样时会用 `all_positive_examples` 排除所有已知正例，因此“另一 split 的真正例被显式采成负例”这件事当前代码已经避免。

因此，T30 的问题不在“没有 grouped eval”，而在“训练和模型选择仍没有按 grouped query 来组织”。

## 4. Confirmed Mismatch Points

## M1. Loss mismatch: training optimizes edge-wise BCE, not grouped retrieval

代码事实：

- `build_edge_tensors(...)` 把样本压成 `edge_index / relation_ids / labels` 三个张量。
- `run_relation_gcn_baseline.py` 与 `run_relation_hyperbolic_baseline.py` 都使用：
  - `criterion = torch.nn.BCEWithLogitsLoss()`
  - `loss = criterion(train_logits, train_labels)`

这意味着当前优化目标是：

```text
对每条 (src, dst, relation) 边独立做二分类
```

而正式 benchmark 目标是：

```text
对同一个 (src, relation) 查询下的全部真 ancestor 做 grouped ranking
```

影响：

- 训练阶段不要求“同查询内真祖先彼此一起靠前”。
- 模型只学到“这条边像不像正例”，没有学到“同一查询下候选排序应该怎样排”。

## M2. Query-unit mismatch: train rows are edges, eval units are `(src, relation)` queries

代码事实：

- 训练样本单位是 `(src, dst, relation, label)`。
- `build_grouped_ranking_queries(...)` 到评测时才把同一 `(src, relation)` 下多个 `dst` 合并。

影响：

- 训练阶段的权重按“正例边数”分配。
- 评测阶段的 grouped 指标按“query”平均。

这会带来两个偏差：

1. 正例多的 query 在训练里天然更重。
2. query 间没有统一的归一化；训练目标和报告口径不在同一层级。

## M3. Split mismatch: current split is edge-level, not query-level

这是本轮审计发现的最重要结构问题。

代码事实：

- `stratified_split_relation_examples(...)` 只按 `relation_type` 分桶。
- 它不会把同一 `(src, relation)` query 绑定在同一个 split。
- 对 `ancestor_ranking` 来说，closure 正例 `(src, dst_1, relation)`、`(src, dst_2, relation)`、`(src, dst_3, relation)` 很容易被拆到不同 split。

影响不止是“训练/评测不一致”，而是**grouped query 本身会被拆碎**：

1. 同一 query 的一部分正例可能进 train，另一部分进 val/test。
2. `build_grouped_ranking_queries(...)` 在 val/test 只会看到本 split 内的正例。
3. 因此，其他 split 里的同 query 真正例不会被标成 positive。
4. 它们仍然在 candidate pool 里，于是会在 grouped eval 中被当成 non-positive 候选。

结果：

- grouped val/test 指标可能把“真祖先”当成假负例处理。
- 即使未来换成 grouped loss，只要 split 仍是 edge-level，query-complete 评测仍然不可靠。

## 4.1 T31A Fix Status

`T31A` 已在代码路径上补入 grouped ancestor retrieval 的 query-level split completeness：

1. `relation_tasks.py`
   - 新增 `query_key_for_relation_example(...)`
   - 新增 `stratified_split_relation_examples_by_query(...)`
   - 新增 `summarize_query_level_split(...)`
   - 新增 `assert_query_level_split_disjoint(...)`

2. `relation_baseline_common.py`
   - 对 `task == "ancestor_ranking"` 改为走 `stratified_split_relation_examples_by_query(...)`
   - 在数据准备阶段立即运行 `assert_query_level_split_disjoint(...)`
   - 把 `query_split_summary` 写入 `run_manifest.json -> task_summary`

当前语义是：

```text
only ancestor_ranking uses query-level split;
other task families keep their current split path.
```

这符合 `T31A` 的任务边界，也避免在本轮误改 `parent_prediction` 等无关任务。

## 4.2 Post-Fix Interpretation

`T31A` 之后，M3 的结论需要改成更精确的版本：

1. 对 `ancestor_ranking` / grouped ancestor retrieval 路径，query-level split completeness 已被显式修复。
2. val/test grouped eval 现在应以“同一 `(src, relation)` query 不跨 split”为前提运行。
3. `T31` 因而可以把重点收缩到 grouped loss、query-aware negatives 和 grouped checkpoint selection。

仍然保留的边界：

- 这次修复没有把训练单位改成 query；那仍属于 `T31`。
- 这次修复没有把局部 sampled negatives 改成更强的 query-aware candidate competition；那也仍属于 `T31`。
- 这次修复没有给出任何新性能结论。

## M4. Negative-sampling mismatch: training negatives are local sampled edges, eval candidates are full query pools

代码事实：

- `sample_negative_relation_examples(...)` 以正例边为中心采负例。
- 当前默认是 `negative_ratio` 配合 `same_module` / `random` 策略。
- 评测阶段 `candidate_ids` 来自 `relation_candidate_pools` 的整池候选，而不是训练时那组局部负例。

影响：

- 训练看到的是“每条边附近的一小批 sampled negatives”。
- 评测要求的是“在整张 relation-specific candidate pool 上做排序”。

这会让模型在训练时主要学到局部 binary discrimination，而不是全候选排序。

## M5. Model-selection mismatch: early stopping uses binary AP, not grouped metric

代码事实：

- GCN / HGCN runner 都在训练过程中用 `evaluate_split(...)` 算 val binary 指标。
- 最优 checkpoint 依据是 `val_average_precision`。
- `build_ranking_task_metrics(...)` 只在训练结束后运行。

影响：

- 当前“最佳模型”是按 binary AP 选出来的，不是按 grouped MAP / nDCG / Recall@10 选出来的。
- 这意味着即使 grouped 指标更重要，训练过程也不会为了 grouped 指标去选模型。

## M6. Reporting mismatch: grouped benchmark exists, but historical single-positive field still留在 summary surface

代码事实：

- `result_summary.json` 仍同时保留 `ranking_test_mrr` 与 grouped 系列字段。
- 现有 seed sweep / artifact 已经普遍写出 `grouped_test_map`、`grouped_test_ndcg`、`grouped_test_recall_at_10`，但历史 `ranking_test_mrr` 仍保留。

影响：

- 这不是最核心的训练错配，但会增加阅读混淆。
- 如果后续只盯 `ranking_test_mrr`，容易把 binary-style历史口径重新抬回主结论。

## 5. Minimal T31 Change Boundary

如果后续进入 `T31`，最小改造边界建议如下：

1. **只对 grouped ancestor retrieval 路径新增 grouped training 分支**
   - 保留 `parent_prediction` 等任务现有 BCE 路径。
   - 不在同一轮重写所有任务。

2. **训练单位改成 query**
   - 对 `ancestor_ranking` 先从 train split 构造 `(src, relation)` grouped queries。
   - 每个 query 明确维护 `positive_ids` 与 sampled candidate set。

3. **loss 至少升级为 query-grouped objective**
   - 优先候选：`sampled softmax` 或 `InfoNCE`
   - 目标是让同 query 内真祖先相对 query-aware negatives 更靠前。

4. **checkpoint 选择改成 grouped val metric**
   - 首选 `val grouped nDCG@10`
   - 备选 `val grouped MAP`
   - binary AP 退回为辅助诊断。

5. **如果不先修 query-level split，就不要把 T31/T32 的 grouped 结果写成高置信 benchmark 结论**
   - 当前 edge-level split 会让 grouped query 不完整。
   - 这是 grouped training alignment 的前置风险，不应被忽略。

## 5.1 T31 Reviewed Status

`T31` 已通过 adversarial review。该任务在最小边界内落地到 grouped retrieval runner 路径，重点是把训练 query 语义和 `T31A` 已 review 的 split/eval 语义真正对齐。

代码层面已完成：

1. `run_relation_grouped_retrieval_baseline.py`
   - 训练 query 构造不再走临时 ad hoc 聚合，而是直接复用 `build_grouped_ranking_queries(...)`。
   - grouped training query key 与 split/eval 显式统一为 `(src_id, relation_type)`。
   - 每个 query 现在显式记录 `positive_ids`、sampled `negative_ids`、`candidate_pool_size`。
   - 训练统计补充 `grouped_loss_name`、`query_group_summary`，并把 grouped training 侧摘要单独写入 `grouped_training_summary.json`。
   - `training_stats.json` 与 `result_summary.json` 现在同时保留 grouped training 侧摘要与 `task_summary.query_split_summary`，便于核对 T31A -> T31 的语义连续性。

2. config / smoke
   - 新增 `project_bootstrap/baseline_scaffold/configs/relation_grouped_gcn_typeclass_precise_v2_ancestor_ranking_smoke_t31.json`。
   - 已完成单次 smoke，artifact 位于：
     `artifacts/smoke/relation_grouped_gcn_lean4_example_typeclass_precise_v2_ancestor_ranking_smoke_t31/`

当前可确认的实现口径：

```text
query-level split (T31A) -> grouped training queries keyed by (src_id, relation_type) -> grouped val/test reporting on the same key
```

本轮刻意没有做的事：

- 不回头重写 edge-level BCE 的 GCN / HGCN runner。
- 不运行长 seed sweep。
- 不把 smoke artifact 写成正式 benchmark 结果。

T31 review 确认：

- query key alignment is solid：T31A split、T31 training 与 T31 eval 均使用 `(src_id, relation_type)`。
- model selection uses grouped val MAP，而不是 binary AP。
- `sampled_softmax_loss` 是真实的 InfoNCE / sampled-softmax family objective，没有 mock、stub 或 hardcode。
- 旧 BCE runners 未在 T31 中改动；后续正式 grouped sweep 必须使用 grouped runner。

当前残留边界：

- 该 grouped-loss 路径目前只在 grouped retrieval runner 上 smoke 过，尚未额外 smoke HGCN config。
- `grouped_loss="infonce"` 当前只作为最小兼容配置入口接受，尚未引入与 `sampled_softmax` 明确区分的单独实现；T31 review 接受该行为作为当前最小实现。
- grouped runner 默认 `negative_ratio = 10.0`，但 T31 smoke config 显式设为 `1.0`。T32/T33 正式 sweep config 必须显式设置该字段。

## 6. Recommended Priority Order

基于当前代码事实，建议优先级如下：

1. **P0: query-level split completeness**
   - `T31A` 已完成代码修复；review 通过后，这一项可以从前置风险降级为已收口实现项。

2. **P1: grouped loss branch**
   - `T31` 已通过 adversarial review；grouped retrieval runner 已具备最小 query-grouped loss、grouped val MAP model selection 和可追踪 artifact 字段。

3. **P2: query-aware negative/candidate sampling**
   - 让训练看到的竞争集更接近 grouped eval candidate pool。

4. **P3: reporting cleanup**
   - 明确 binary AP / ranking MRR 只作为辅助诊断。

## 7. Bottom Line

当前实现不是“没有 grouped benchmark”，而是：

```text
我们已经有 grouped eval，
但训练、split、negative sampling 和 checkpoint selection 仍主要服务于 edge-level BCE。
```

因此，`T31` 的核心工作不该只是“换一个 loss 名字”，而应至少把：

- query unit
- grouped objective
- grouped model selection

这三件事拉到同一口径上；否则训练/评测错配只会从“显式”变成“半显式”。
