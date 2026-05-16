# 07 Handoff

> 更新时间：2026-05-16
>
> 给下一位 Captain / Worker / Reviewer 的接手说明。

## 1. 当前项目状态

你接手的是一个围绕 traced Lean / Mathlib hierarchy graph 的工程化研究仓库。当前主线已经从“证明 HGCN 优于 GCN”收束为：

> 构建真实 traced formal-math hierarchy graph 的可复现 pipeline、标准化 grouped retrieval 协议与结构诊断框架，并系统分析双曲归纳偏置在什么结构条件下才可能有效。

不要把项目重新带回“继续调 HGCN 直到赢”的旧路线。

## 2. 必读文件

按顺序读：

1. `docs/reference/AI_coding_workflow.md`
2. `docs/02_experiment_plan.md`
3. `docs/04_task_board.md`
4. `docs/06_eval_protocol.md`
5. `docs/08_risks_and_open_questions.md`

如果要理解历史证据，再读：

- `docs/项目交接Prompt（给后续AI）.md`
- `docs/阶段总结（2026-05-01，grouped ancestor retrieval）.md`
- `docs/阶段总结（2026-05-02，grouped retrieval training）.md`
- `docs/双曲优势假设的诊断分析与替代方向.md`

## 3. 当前唯一任务

`T32`: 在 `Field.Subfield` 与 `Order.Ring` 上跑 GCN 5-seed grouped training 对照。

任务包：

```text
docs/tasks/M3_training/T32_gcn_grouped_training_sweep.md
```

不要改 HGCN 代码，不要改变 T31 reviewed grouped training 协议，不要覆盖历史 artifact。当前只运行 GCN grouped training sweep，并产出可审查的 mean/std 报告。

当前状态补充：

- `T31A` 已通过 adversarial review，query-level split completeness 前置风险已收口。
- `T31` 已通过 adversarial review，最小 grouped training 路径已收口：`run_relation_grouped_retrieval_baseline.py` 复用 `build_grouped_ranking_queries(...)` 构造训练 query，确保 grouped loss、split 与 eval 共用同一 `(src_id, relation_type)` key。
- T31 smoke artifact 位于 `artifacts/smoke/relation_grouped_gcn_lean4_example_typeclass_precise_v2_ancestor_ranking_smoke_t31/`，其中 `grouped_training_summary.json`、`training_stats.json` 与 `result_summary.json` 均记录 `query_key_fields = [src_id, relation_type]` 与 `training_loss = sampled_softmax`。
- T32 worker 必须使用 reviewed grouped retrieval runner / seed sweep path，不能退回旧 BCE runner。
- T32 的正式 sweep config 必须显式设置 `negative_ratio`，不要依赖 grouped runner 默认值。
- `.claude/settings.json` 有自动权限 diff，review 已要求排除提交；不要把它作为 T31/T32 产物提交。

## 4. 当前已知事实

1. 目前没有稳定证据证明 HGCN 在真实 traced Lean hierarchy 图上优于 GCN。
2. 旧版单正例 `ancestor_ranking` 协议不合理，默认口径已经升级为 grouped multi-positive ancestor retrieval。
3. 真实 relation layer 往往偏浅、碎片化，常呈现 forest / star-forest 形态。
4. relation-aware GCN 仍是当前更强、更稳的 baseline。
5. full Mathlib trace 成本高，不作为当前前置条件。
6. 仓库已经有 `project_bootstrap/` 原型和 `artifacts/` 下的诊断 / baseline 产物。

## 5. 重要路径

工程入口：

- `project_bootstrap/leandojo_graph_scaffold/src`
- `project_bootstrap/baseline_scaffold/src`
- `project_bootstrap/graph_diagnostics_package`
- `project_bootstrap/next_traced_target_selection_package`

关键产物：

- `artifacts/diagnostics/real_graphs_v1/report.md`
- `artifacts/diagnostics/hierarchy_focus_v1/report.md`
- `artifacts/diagnostics/mathlib_order_focus_v1/report.md`
- `artifacts/baselines/relation_seed_sweeps/`

治理入口：

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `docs/04_task_board.md`
- `docs/tasks/`
- `docs/review/`

## 6. Worker 执行纪律

Worker 必须：

1. 只做 `Current Unique Task`。
2. 只改任务包里的 `Allowed files`。
3. 不自动领取下一任务。
4. 完成后运行 `Verification`，或明确说明为什么无法运行。
5. 最后报告改动、验证和剩余风险。

Reviewer 默认只读。高风险任务使用 adversarial review。

## 7. 本轮状态更新

本轮 Captain 已完成：

1. 阅读 `docs/reference/AI_coding_workflow.md` 与 `docs/02_experiment_plan.md`。
2. 建立 `docs/00~08` 治理文档与 `docs/tasks/`、`docs/review/` 目录。
3. 将第一个 worker 任务设为 `T00`。

本轮 Worker 已完成且已通过 review 的内容：

1. 新建根目录入口文档 `README.md`、`AGENTS.md`、`CLAUDE.md`。
2. 更新 `docs/04_task_board.md`，补充本轮 `T00` 执行说明，但没有擅自勾选完成。
3. 更新本 handoff，说明根目录入口文档已补齐。

当前状态：

1. `T10` 已经过 reviewer 只读审查并判定为 PASS。
2. Captain 已将 `T10` 标记为完成，并把当前唯一任务切换到 `T11`。
3. PM 裁决 `T02` 可视为当前阶段完成，因为 `docs/review` 中已有可信 Claude review 文档覆盖已完成 task。
4. `docs/data_manifest.md` 只锁定了当前可从仓库与现有 config 直接核实的版本锚点；`lean4-example`、LeanDojo 精确版本、Python 精确环境仍明确保留为 `unknown / needs verification`。
5. `T11` 已经过 reviewer 只读审查并判定为 PASS；`docs/data_card.md` 成为 reviewed data card，补充了当前图资产的字段模式、relation 语义、coverage-aware 规则、recommended usage 与 unresolved 语义边界。
6. Captain 已将 `T11` 标记为完成，并把当前唯一任务切换到 `T12`。
7. `docs/tasks/**/*.md` 已检查，均包含 workflow 要求的任务包字段；GLM captain 后续可直接以 `docs/04_task_board.md` 的 Current Unique Task 为准分派 worker。
8. Worker 已产出 `docs/grouped_retrieval_protocol.md` 草稿，并更新 `docs/06_eval_protocol.md`，把 grouped 协议的代码入口、配置字段、指标名与输出字段写成显式映射。
9. Worker 已对 `run_relation_grouped_retrieval_baseline.py` 做最小代码修正，补齐 `grouped_test_ndcg_at_10` 到 `result_summary.json`，以匹配现有 seed sweep / report 汇总字段。
10. `T12` 已经过 adversarial reviewer 只读审查并判定为 PASS；Captain 已将 `T12` 标记完成。
11. 此前当前唯一任务已从 `T12` 切换到 `T13`。
12. `T13` 本轮已由 worker 完成实现与静态验证：单次 `result_summary.json` 已平铺导出 `hop_2 / hop_3 / hop_4_plus` 指标，seed sweep `report.md` 也已显式展示 hop bucket 聚合与 per-seed 结果。
13. `T13` 已经过 adversarial reviewer 只读审查并判定为 PASS；Captain 已将 `T13` 标记完成。
14. T13 review 的 helper duplication 与 end-to-end smoke gap 作为 deferred follow-up 跟踪；per-seed table 只展示 MAP/nDCG 被接受为展示选择，不视为阻塞。
15. 当前唯一任务已切换到 `T14`。
16. `T14` 本轮已由 worker 完成：新增最小 smoke config，成功运行单次 GCN `ancestor_ranking` smoke，并在 `artifacts/smoke/relation_gcn_lean4_example_typeclass_precise_v2_ancestor_ranking_smoke_t14/` 真实产出 `metrics.json` 与 `result_summary.json`。
17. 上述 smoke 已确认 `grouped_test_ndcg_at_10` 与 `hop_2 / hop_3 / hop_4_plus` 平铺字段实际落盘；该 artifact 仅用于 Milestone 1 spot-check，不是正式 benchmark 结果。
18. `T14` 还完成了轻量 cleanup：把 `flatten_grouped_hop_bucket_summary` 去重到 `relation_baseline_common.py`，消除了 T13 review 指出的 runner 间重复 helper。
19. `T14` 已经过 reviewer 只读审查并判定为 PASS；Captain 已将 `T14` 标记完成，Milestone 1 闭合。
20. T14 review 要求不要提交 `.claude/settings.json` 的自动权限 diff；该文件不属于 T14 Allowed Files。
21. 此前当前唯一任务已从 `T14` 切换到 `T20`。
22. `T20` 已由 worker 执行完成：基于 `real_graphs_v1`、`hierarchy_focus_v1`、`mathlib_order_focus_v1` 现有 artifacts 新增 `docs/diagnostics_summary.md`，给出“shallow diagnostic-only”与“candidate pool”的分层判断，并形成 provisional candidate priority。
23. `T20` 的核心结论是：大多数真实 relation layer 仍然偏浅，更多像 forest / star-forest；更值得继续跟进的是 `mathlib_algebra_order_d3` 与 `mathlib_algebra_order_ring_d4`，而 `ring_subring` / `field_subfield` 更适合作为小型受控 probe。
24. `T20` 已经过 reviewer 只读审查并判定为 `PASS_WITH_WARNINGS`；Captain 已将 `T20` 标记完成。
25. T20 review 的两个 warning 均 deferred：部分 `n/a` 表格数值可在后续文档精修中补全；单表混合指标来源可在后续修订中加来源标注。它们不影响候选优先级。
26. 当前唯一任务已切换到 `T21`。
27. `T21` 已由 worker 执行完成：基于 `module_hierarchy_scan_mathlib_algebra_order_index_v1` 与 `module_hierarchy_scan_batteries_v1` 现有 scan 产物新增 `docs/candidate_graph_audit.md`，把 depth、continuity、positive scale、ancestor closure cost 和结构风险拆开审计。
28. `T21` 的核心审计结论是：`Mathlib.Algebra.Order.Ring` 是当前最平衡的 follow-up 候选；`Mathlib.Algebra.Order` 更适合作为 depth stress-test；`Ring.Subring` / `Field.Subfield` 继续作为受控 probe；`Batteries` 模块扫描整体仍过浅，不适合作为下一轮 benchmark 来源。
29. `T21` 还指出 raw hierarchy score 不能直接当作 benchmark 排序依据，因为它会偏向小而紧凑的模块；后续若进入 T22，应把 positive scale、component ratio 与 closure cost 一起门控。
30. `T21` 已经过 reviewer 只读审查并判定为 PASS；Captain 已将 `T21` 标记完成。
31. T21 review 的三个 non-blocking issues 均 deferred：`depth` 列名歧义、审计表选择范围说明不足、mathlib module scan standalone config traceability gap。前两个作为 candidate audit 文档精修跟踪，第三个作为可复现 traceability 风险跟踪。
32. 当前唯一任务已切换到 `T22`；本轮只推荐下一任务，不执行 T22。
33. `T22` 已由 worker 执行完成文档草案：新增 `docs/diagnostics_protocol.md`，把 shallow forest / star forest 判断、positive scale、component ratio 与 closure expansion 门控写成显式 `heuristic` 模板，并把 `Mathlib.Algebra.Order.Ring` 校准为 default follow-up candidate、`Mathlib.Algebra.Order` 校准为 depth stress-test、`Ring.Subring` / `Field.Subfield` 校准为 controlled probe。
34. `T22` 同步把评测协议中的结构诊断部分链接到 `docs/diagnostics_protocol.md`，避免后续 worker 只引用 raw hierarchy score 就直接下 benchmark 结论。
35. `T22` 已经过 reviewer 只读审查并判定为 PASS；Captain 已将 `T22` 标记完成，Milestone 2 闭合。
36. T22 review 的三个 non-blocking issues 均 deferred：shallow forest flag condition 3 命名可能误导深层但碎片化图、report template 缺少 `multi-parent count` 行、`ancestor_added_nodes` 缺少内联定义。它们进入 R18 / D09，后续模板精修时处理。
37. 当前唯一任务已切换到 `T30`；本轮只推荐下一任务，不执行 T30。
38. `T30` 已由 worker 执行完成文档草案：新增 `docs/training_alignment_audit.md`，确认当前 GCN / HGCN 训练仍以 edge-level `BCEWithLogitsLoss` 为核心，而 grouped retrieval 只在训练后做 post-hoc 评测。
39. `T30` 审计还发现一个更强的结构风险：`stratified_split_relation_examples(...)` 当前按正例边而不是按 `(src, relation)` query 切分，因此同一 grouped query 可能跨 `train / val / test` 被拆碎，进而让 val/test grouped eval 缺少完整 positive set。
40. `T30` 已经过 reviewer 只读审查并判定为 PASS；Captain 已将 `T30` 标记完成。
41. T30 review 的三个 non-blocking issues 均 deferred：Section 4 heading nesting、M6 mixed-language title、M3 rough impact estimate。它们进入 D11，后续文档精修或 split analysis 时处理。
42. Captain 根据 T30 review 的 P0 建议插入 `T31A`，先修 query-level split completeness；当前唯一任务已切换到 `T31A`，本轮只推荐下一任务，不执行 T31A。
43. `T31A` 已由 worker 完成代码草案：`ancestor_ranking` / grouped ancestor retrieval 现在走 query-level split，不再按正例边切分同一 `(src, relation)` query。
44. `T31A` 还新增 split disjointness 摘要并在数据准备阶段做显式断言；当前设计是只影响 grouped ancestor retrieval 路径，不改 `parent_prediction` 等其他 task family。
45. `T31A` 已经过 adversarial reviewer 只读审查并判定为 PASS；Captain 已将 `T31A` 标记完成。
46. T31A review 的 non-blocking issues 已分类：query key 与 `ancestor_label_mode` 交互作为 T31 注意事项接受；R19 由 Active 改为 Mitigated；Section numbering 继续由 D11 跟踪；rare relation type 覆盖率留作后续 grouped benchmark 注意事项。
47. 当前唯一任务已切换到 `T31`；本轮只推荐下一任务，不执行 T31。
48. `T31` 本轮已由 worker 完成最小 grouped training 实现：`run_relation_grouped_retrieval_baseline.py` 现在直接复用 `build_grouped_ranking_queries(...)` 构造训练 query，训练 key 与 T31A 已 review 的 split / eval key 显式对齐到 `(src_id, relation_type)`。
49. `T31` 同步新增最小 smoke config `project_bootstrap/baseline_scaffold/configs/relation_grouped_gcn_typeclass_precise_v2_ancestor_ranking_smoke_t31.json`，并完成单次 smoke 运行；artifact 落在 `artifacts/smoke/relation_grouped_gcn_lean4_example_typeclass_precise_v2_ancestor_ranking_smoke_t31/`。
50. 上述 smoke 已确认 `grouped_training_summary.json`、`training_stats.json` 与 `result_summary.json` 写入 `training_loss = sampled_softmax`、`query_key_fields = [src_id, relation_type]`，且保留 `task_summary.query_split_summary` 作为 T31A split completeness 证据。
51. `T31` 已经过 adversarial reviewer 只读审查并判定为 PASS；Captain 已将 `T31` 标记完成。
52. T31 review 的 non-blocking issues 已分类：`grouped_loss="infonce"` 作为 `sampled_softmax` alias 为 accepted current behavior；grouped runner `negative_ratio` 默认值差异为 deferred 并写入 T32 明确配置要求；`total_loss` device 初始化清理为 deferred；Captain 级治理文档越界项为 accepted scope distinction；`.claude/settings.json` 自动权限 diff 为 rejected/excluded from commit。
53. 当前唯一任务已切换到 `T32`；本轮只推荐下一任务，不执行 T32。

## 8. 下一步

下一步把 `T32` 任务包交给 worker 执行。Worker 应运行 GCN 5-seed grouped training sweep，优先覆盖 `Field.Subfield` 与 `Order.Ring`，并产出 `docs/experiment_reports/gcn_grouped_training.md`。

T32 的关键执行点是：必须使用 T31 reviewed grouped runner / seed sweep path；正式 sweep config 必须显式设置 `negative_ratio`；如果 `Field.Subfield` 或 `Order.Ring` 缺少可运行 config，应在任务边界内补齐 config 并记录阻塞或产物路径。

不要把 `docs/data_manifest.md` 中的 `unknown / needs verification` 字段上升为既成版本事实。
不要把 `docs/data_card.md` 中的 `recommended usage` 误读为最终 benchmark 定稿；这仍然只是当前治理口径下的使用边界，后续还需要 T20+ diagnostics。
不要把 legacy `task = ancestor_ranking` 误读为旧单正例协议仍然有效；在 reviewed grouped protocol freeze 中，它只是 grouped multi-positive ancestor retrieval 的兼容执行键。
