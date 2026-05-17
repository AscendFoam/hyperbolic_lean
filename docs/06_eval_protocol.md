# 06 Eval Protocol

> 更新时间：2026-05-17
>
> 状态：T12 grouped protocol freeze、T13 hop bucket reporting、T14 smoke check、T31A query-level split、T31 minimal query-grouped loss 与 T32 GCN grouped baseline 均已通过 review。Smoke artifact 只证明输出链可落盘，不是正式 benchmark 结果。

## 1. 默认任务

正式 ancestor 任务默认采用：

```text
grouped multi-positive ancestor retrieval
```

查询单位：

```text
(src, relation)
```

正例集合：

```text
同一查询下全部真实 ancestor
```

禁止把旧单正例 `ancestor_ranking` 的 MRR 当作主结论。它只能作为历史对照或辅助指标。

## 2. 推荐任务族

| 任务 | 用途 | 当前地位 |
| --- | --- | --- |
| grouped ancestor retrieval | 默认正式协议 | 主任务 |
| typed parent retrieval | 区分 `extends` 与 `instance_of` | 辅助主任务 |
| parent prediction | 与旧结果保持可比 | 辅助任务 |
| typed link prediction | 检查 relation typing 信号 | 诊断任务 |
| proof-side utility | 连接 proving workflow | 后续 MVP |

## 3. 指标

grouped retrieval 必须报告：

- `Recall@1`
- `Recall@3`
- `Recall@5`
- `Recall@10`
- `MAP`
- `nDCG`
- `nDCG@10`
- `grouped-MRR`

必须补充 hop bucket：

- `hop_2`
- `hop_3`
- `hop_4_plus`

多 seed 正式结果默认报告：

```text
mean ± std over 5 seeds
```

## 3.1 当前代码入口与字段映射

当前执行仍保留旧任务键：

```text
task = ancestor_ranking
```

但在当前协议下，它默认映射到正式任务名：

```text
grouped multi-positive ancestor retrieval
```

当前代码入口：

1. 任务与 hop 构造：
   - `project_bootstrap/baseline_scaffold/src/relation_tasks.py`
2. grouped 指标计算与输出结构：
   - `project_bootstrap/baseline_scaffold/src/relation_baseline_common.py`
3. baseline runner：
   - `project_bootstrap/baseline_scaffold/src/run_relation_gcn_baseline.py`
   - `project_bootstrap/baseline_scaffold/src/run_relation_hyperbolic_baseline.py`
   - `project_bootstrap/baseline_scaffold/src/run_relation_grouped_retrieval_baseline.py`
4. sweep / report 汇总：
   - `project_bootstrap/baseline_scaffold/src/run_relation_seed_sweep.py`
   - `project_bootstrap/baseline_scaffold/src/_patch_sweep_reports.py`

当前冻结的关键配置字段：

- `task`
- `target_relation_types`
- `message_relation_types`
- `hierarchy_relation_types`
- `ancestor_label_mode`
- `ancestor_min_hops`
- `class_like_decl_kinds`
- `exclude_held_out_direct_edges`
- `negative_strategy`
- `negative_fallback_strategy`
- `model_type`
- `grouped_loss`
- `negative_ratio`

当前 grouped training 约定：

- T31 reviewed grouped runner path 使用 `(src_id, relation_type)` 作为训练、split 与 eval 的统一 query key。
- `grouped_loss = "sampled_softmax"` 是当前 reviewed 最小实现。
- `grouped_loss = "infonce"` 当前只是同一实现族的兼容配置名，不代表另一个独立 contrastive variant。
- grouped runner 的正式 sweep config 必须显式设置 `negative_ratio`，不得依赖 runner 默认值。
- best checkpoint 应由 grouped validation metric 驱动；T31 当前使用 grouped val MAP。

当前冻结的 grouped 输出字段：

- `metrics.json`:
  - `ranking.val.grouped`
  - `ranking.test.grouped`
  - `ranking.val.grouped.hop_buckets`
  - `ranking.test.grouped.hop_buckets`
- `result_summary.json`:
  - `grouped_test_map`
  - `grouped_test_ndcg`
  - `grouped_test_ndcg_at_10`
  - `grouped_test_mrr`
  - `grouped_test_recall_at_1`
  - `grouped_test_recall_at_3`
  - `grouped_test_recall_at_5`
  - `grouped_test_recall_at_10`
  - `hop_2_map`
  - `hop_2_ndcg`
  - `hop_2_grouped_mrr`
  - `hop_2_recall_at_1`
  - `hop_2_recall_at_3`
  - `hop_2_recall_at_5`
  - `hop_2_recall_at_10`
  - `hop_3_map`
  - `hop_3_ndcg`
  - `hop_3_grouped_mrr`
  - `hop_3_recall_at_1`
  - `hop_3_recall_at_3`
  - `hop_3_recall_at_5`
  - `hop_3_recall_at_10`
  - `hop_4_plus_map`
  - `hop_4_plus_ndcg`
  - `hop_4_plus_grouped_mrr`
  - `hop_4_plus_recall_at_1`
  - `hop_4_plus_recall_at_3`
  - `hop_4_plus_recall_at_5`
  - `hop_4_plus_recall_at_10`
- seed sweep outputs:
  - `per_seed_results.csv`
  - `per_seed_results.json`
  - `aggregate.json`
  - `report.md`
- smoke outputs:
  - `artifacts/smoke/relation_gcn_lean4_example_typeclass_precise_v2_ancestor_ranking_smoke_t14/result_summary.json`
  - `artifacts/smoke/relation_gcn_lean4_example_typeclass_precise_v2_ancestor_ranking_smoke_t14/metrics.json`

当前 smoke 约定：

- 只用于确认字段实际落盘，不用于正式 benchmark 比较。
- 不替代后续真实 seed sweep。
- 允许使用单 seed、极少 epoch 和缩小维度的最小运行配置。

详细冻结说明见 `docs/grouped_retrieval_protocol.md`。

## 4. Split 原则

1. 同一 `(src, relation)` 查询下的正例不能泄漏到不同 split。
2. 查询级 split 优先于边级随机 split。
3. 模块级 split 优先于全图随机 split，用于检验泛化。
4. 所有 split 必须记录 seed、候选空间和负采样策略。
5. `unresolved` 或 coverage 不可靠的端点不能强行当高置信 negative。

## 5. Baseline 比较原则

所有模型比较必须满足：

1. 相同数据快照。
2. 相同 split。
3. 相同 seed sweep。
4. 相同候选集合。
5. 相同 grouped 指标。
6. 相近参数预算。
7. 报告训练目标是否与评测目标对齐。

默认 baseline 梯度：

1. 启发式 / 文本 baseline。
2. 欧氏图模型，如 GCN / GraphSAGE / GAT。
3. 双曲模型，如 Poincare / HGCN / Lorentz 变体。
4. 只有在前面三层结果明确后，再考虑复杂模型。

## 6. 结构诊断指标

每张正式图至少报告：

- nodes / edges
- relation nodes / relation edges
- largest component
- SCC 情况
- longest chain
- leaf ratio
- multi-parent count
- cycle rank
- diameter estimate
- approximate hyperbolicity proxy
- grouped retrieval difficulty

诊断报告必须明确判断：

1. 图是否是 shallow forest / star forest。
2. 是否存在更深、更连续、更有层级密度的候选子图。
3. 当前图是否适合继续检验双曲优势。

结构诊断的统一启发式门控见：

```text
docs/diagnostics_protocol.md
```

该协议把以下判断写成可复用模板，并明确标注为 `heuristic`：

- shallow forest / star forest 风险
- positive scale
- component ratio
- closure expansion / closure cost
- `default follow-up candidate` / `depth stress-test` / `controlled probe` / `diagnostic-only` 角色分层

当前经验阈值口径：

1. `longest chain <= 4` 默认视为 shallow 风险。
2. `longest chain <= 3` 且 `leaf ratio >= 0.75` 默认视为 star-forest 风险。
3. `relation positive edges >= 250` 才有资格进入默认 follow-up 候选讨论。
4. `component ratio >= 0.65` 才能视为连续性较好。
5. `closure expansion ratio <= 0.60` 才能视为 closure 负担可接受。

这些阈值服务于当前 reviewed traced hierarchy diagnostics，不得直接写成理论结论或最终 benchmark 排名。

## 7. 数据资产要求

每次正式实验应绑定：

- Lean 版本
- Mathlib commit
- LeanDojo / tracing 工具版本
- Python 环境或依赖文件
- 图抽取脚本版本
- 评测脚本版本
- config 路径
- artifact 输出路径
- run id

T10 将负责把这些要求落成 version manifest。

## 8. 通过 / 失败判据

协议门通过条件：

1. grouped retrieval 已成为默认任务入口。
2. hop bucket 出现在常规报告中。
3. 5-seed mean ± std 可复现。
4. GCN / HGCN 同口径比较无明显数据泄漏。

双曲价值门通过条件，至少满足一项：

1. 低维下稳定优于欧氏模型。
2. 在更深 hop bucket 上形成稳定收益。
3. 在更纯层级图上显著优于欧氏 baseline。

若不满足，双曲保留为条件性 follow-up，不作为主论文承诺。

## 9. 当前治理状态

- `T00` 已通过 review，项目已有根目录入口文档。
- `T01` 已通过 review with warnings accepted，治理文档一致性复查已收口。
- `T02` 已按 PM 裁决视为当前阶段完成。
- `T10` 已通过 review，版本锁定与数据资产要求已落成 `docs/data_manifest.md`。
- `T11` 已通过 review，当前图资产、字段、relation provenance、coverage-aware 边界与 recommended usage 已落成 `docs/data_card.md`。
- `T12` 已通过 adversarial review，grouped 协议文档与 grouped retrieval runner 的最小输出字段对齐已收口。
- `T13` 已通过 adversarial review，已把 `hop_2 / hop_3 / hop_4_plus` 补入单次 `result_summary.json` 与 seed sweep `report.md` 的常规报告入口。
- `T14` 已通过 review，最小 GCN smoke 已确认 `grouped_test_ndcg_at_10` 与 hop bucket 平铺字段真实落盘。
- `T21` 已通过 review，module-level candidate scan audit 已确认 `Mathlib.Algebra.Order.Ring` 是当前最平衡的 follow-up 候选，`Mathlib.Algebra.Order` 更适合作为 depth stress-test。
- `T22` 已通过 review，`docs/diagnostics_protocol.md` 成为 reviewed heuristic diagnostics protocol；其中阈值仍只服务于当前 reviewed traced hierarchy diagnostics，不是理论证明或最终 benchmark 排名。
- `T30` 已通过 review，`docs/training_alignment_audit.md` 成为 reviewed training alignment audit；当前训练仍是 edge-level BCE，且现有 split 可能拆碎 grouped query。
- `T31A` 已通过 adversarial review，grouped ancestor retrieval 已改为 query-level split；run manifest 的 `query_split_summary` 记录 `split_strategy = query_level`、query overlap 为 0、`is_query_level_disjoint = true`。
- `T31` 已通过 adversarial review，grouped retrieval runner 已实现最小 query-grouped loss，训练、split 与 eval 共用 `(src_id, relation_type)` query key，并用 grouped val MAP 做模型选择。
- `T34` 已通过 milestone review，Milestone 3 的 grouped-vs-binary 诊断总结已收口。
- `T41` 已通过 adversarial review，六个 provenance split 图已真实生成并完成边数与 identity 校验；当前唯一任务为 `T42`，负责在 `explicit_only / synthesized_only / hierarchy_mixed` 三类图上运行 GCN/HGCN grouped seed sweeps，其中 `explicit_only` 为 primary split，`synthesized_only` 为 controlled diagnostic，`hierarchy_mixed` 为 reproducibility check。
- 不得把 T14 的 smoke output 写成正式 benchmark 结果。


