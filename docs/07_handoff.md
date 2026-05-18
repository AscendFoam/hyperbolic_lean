# 07 Handoff

> 更新时间：2026-05-18（T52 review 后更新）
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

`T52a`: 实现 ancestor explanation proof-side demo CLI，直接加载 T42 reviewed embeddings，支持 single-query 与 `explicit_vs_mixed` provenance comparison。
任务包如下：

```text
docs/tasks/M5_paper/T52a_ancestor_explanation_demo.md
```

先读取 `docs/proof_side_mvp.md`、`docs/tasks/M5_paper/T52_proof_side_demo_package.md`、`docs/review/T52_review.md`、`docs/paper_outline.md`、`docs/06_eval_protocol.md` 与相关代码入口，再按 `T52a` 任务包实现 demo。必须保留 provenance-aware comparison mode、精确 artifact path、`declarations.csv` 精确 declaration 匹配，以及 node ordering sanity check。

## 8. 下一步

`T50` 已通过 `PASS_WITH_WARNINGS` review 并标记完成。已产出 `docs/paper_outline.md`，包含：

- Working title 与 one-paragraph positioning
- Central claim（provenance-conditional）与 5 条 non-claim 边界
- 5 条 paper contributions（C1–C5）
- Evidence ladder：Milestone 1~4 各自提供的证据与角色
- Figures/Tables plan（4 figures + 7 tables）
- Threats to validity（internal / external / construct）
- Venue fit（ITP / CPP / FM 优先级排序与适配分析）
- Proof-side bridge：说明 T51 为何需要从 paper story 延伸到 utility MVP
- Provenance-precision boundaries：R28/R29/R25/R04 的文稿约束
- Draft section outline（11 sections）

所有内容均保持 provenance-conditional 口径。`T50` 已正式收口；当前唯一任务已继续切换到 `T52`。
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
54. `T32` 本轮已由 worker 补齐正式 grouped GCN configs：`grouped_gcn_field_subfield_anc_t32.json`、`grouped_gcn_field_subfield_sweep_t32.json`、`grouped_gcn_order_ring_anc_t32.json`、`grouped_gcn_order_ring_sweep_t32.json`；两份 base config 都显式设置 `grouped_loss = sampled_softmax` 与 `negative_ratio = 10.0`。
55. `T32` 已通过 reviewed grouped runner / seed sweep path 成功运行两组真实 5-seed GCN grouped training sweep；`Field.Subfield` 与 `Order.Ring` 两组 artifact 均无失败 seed。
56. `T32` 已新增 `docs/experiment_reports/gcn_grouped_training.md`，记录精确命令、config 路径、artifact 路径、seed 列表、grouped mean/std 指标和 hop bucket 聚合。
57. `T32` 已经过 adversarial reviewer 只读审查并判定为 PASS；Captain 已将 `T32` 标记完成。
58. T32 review 的 non-blocking issues 已分类：Section 5 hop bucket 表呈现精简为 accepted presentation choice；`grouped MAP` / `gMAP` 混用为 deferred wording cleanup；无 rejected warning。
59. 当前唯一任务已切换到 `T33`；本轮只推荐下一任务，不执行 T33。
60. `docs/review/T33_review.md` 结论为 `PASS`，无 blocking issues。
61. `T33` 已标记完成；当前唯一任务切换到 `T34`，用于汇总 grouped training 与旧 binary training 的差异，不新增实验。
62. `docs/review/T34_review.md` 结论为 `PASS`，无 blocking issues。
63. `T34` 已标记完成；当前唯一任务切换到 `T40`。
64. `docs/review/M3_review.md` 结论为 `PASS_WITH_WARNINGS`；Milestone 3 允许闭合并进入 Milestone 4，但 full clean-environment reproducibility 仍保留 warning。
65. `T40` 本轮已由 worker 完成 provenance split 配置冻结与协议文档草案：新增 `provenance_split_field_subfield_t40.json`、`provenance_split_order_ring_t40.json` 两份 frozen config，以及 `docs/provenance_split_protocol.md` 协议文档。协议冻结了 origin_map（`extends→explicit, instance_of→synthesized`）、三类 split（`explicit_only / synthesized_only / hierarchy_mixed`）、输出目录约定（`data/processed/declaration_graph/{source_name}_{split_name}/`）、生成命令和 T41/T42 usage guide。Worker 未运行 sweep，未修改数据语义，未覆盖历史配置。随后进入 adversarial reviewer 只读审查。
66. `docs/review/T40_review.md` 结论为 `PASS`。Captain 判定 `T40` 完成；reviewer 的 non-blocking notes 已转化为 `T41` 的执行要求：必须校验协议中的预期边数，并程序化验证当前两组候选图上的 `hierarchy_mixed = full source graph` identity。
67. 当前唯一任务切换为 `T41`；从治理状态看，允许提交当前阶段成果并继续派发下一轮 worker，但 staging 时仍应排除 `.claude/settings.json` 之类的越界本地权限变更。
68. `T41` 本轮已由 worker 完成执行。六个 provenance split 图目录已真实落盘于 `data/processed/declaration_graph/`，所有边数与协议预期一致；`hierarchy_mixed = full source graph` identity 已程序化验证（两组候选均确认）。六个 split 图的结构诊断已完成，artifact 位于 `artifacts/diagnostics/provenance_split_t41/`。报告 `docs/experiment_reports/provenance_diagnostics.md` 已产出，核心发现：`synthesized_only` 图在两组候选上均为 longest chain = 1、multi-parent = 0、cycle rank = 0 的浅层星状森林；所有层级深度来自 `explicit_only`；混合图从 synthesized 边继承叶子膨胀和碎片化。Worker 未运行模型训练，未覆盖已有 diagnostics，未改动 T40 冻结语义。随后进入 adversarial reviewer 只读审查。
69. docs/review/T41_review.md 结论为 PASS。Captain 判定 T41 完成并将当前唯一任务切换为 T42。reviewer 的非阻塞意见不要求返修，但已转成 T42 的执行约束：explicit_only 作为 primary split，synthesized_only 作为 controlled diagnostic，hierarchy_mixed 作为 T32/T33 reproducibility check；同时 T42 任务包已补入 tool-side config Allowed Files，避免再次越界写入。
70. T42 本轮已由 worker 完成执行。24 份 provenance sweep config 已创建（12 base + 12 sweep），60 次训练全部成功（零失败）。核心发现：(1) explicit_only 上 HGCN 首次在两组候选图上均超过 GCN（FS MAP +0.1247, OR MAP +0.0557），优势随 hop 深度单调增长；(2) synthesized_only 上 GCN 反超 HGCN；(3) hierarchy_mixed 与 T32/T33 完全一致。新增报告 docs/experiment_reports/provenance_seed_sweeps.md。Worker 未覆盖历史 artifact，未修改 T40/T41 语义。随后进入 adversarial reviewer 只读审查。
71. T43 本轮已由 worker 完成执行。已产出 `docs/experiment_reports/provenance_summary.md`，汇总 T41 结构诊断与 T42 provenance-aware seed sweeps 的核心发现。报告明确写入：(1) `explicit_only` 是 primary evidence，HGCN 在该 split 上稳定领先；(2) `synthesized_only` 是 controlled diagnostic；(3) `hierarchy_mixed` 是 full source graph reproducibility check；(4) synthesized 边的作用是结构性稀释；(5) 项目结论精化为 provenance-conditional。精度约束已满足：FS `hop_4_plus` 基于 4/5 seeds 已注明；`synthesized_only` aggregate/per-seed 口径差异已登记为待核清项（R28）。Worker 未新增训练，未修改 T40/T41/T42 冻结语义。随后进入 review。
72. `docs/review/T43_review.md` 结论为 `PASS`。Captain 已标记 `T43` 完成并闭环 Milestone 4，当前唯一任务切换为 `T50`。reviewer 的非阻塞问题已分类并写回治理：Section 5.1 中 Field.Subfield synthesized_only 的 GCN 表格值错误记为 deferred publication-precision fix（R29）；`.claude/settings.json` 继续 rejected/excluded from commit；R04 继续保留为 provenance-conditional `Mitigated` 口径。
73. `T50` 本轮已由 worker 完成 paper skeleton 草案：新增 `docs/paper_outline.md`，包含 working title、positioning、central claim 与 non-claim 边界、5 条 contributions（C1–C5）、evidence ladder、figures/tables plan、threats to validity、venue fit（ITP/CPP/FM）、proof-side bridge、provenance-precision boundaries 和 draft section outline。所有内容保持 provenance-conditional 口径，绕开 R28/R29。同步更新治理文档。Worker 未标记任务完成，等待 reviewer 只读审查。
74. `docs/review/T50_review.md` 已给出 `PASS_WITH_WARNINGS`。Captain 已完成 warning 分类：`docs/00_raw_idea.md`、`docs/01_feasibility_report.md`、`docs/03_architecture.md`、`docs/06_eval_protocol.md` 的治理状态同步越界编辑记为 accepted low-severity hygiene；worker 修改 `docs/tasks/**/*.md` 记为 rejected future precedent，不要求返修但后续不应再发生；`R30` 与 `R31` 记为 deferred 并继续保留在风险表中；`.claude/settings.json` 继续 excluded from commit。`T50` 已标记完成，当前唯一任务切换为 `T51`。
75. `T51` 本轮已由 worker 完成执行。已产出 `docs/proof_side_mvp.md`，比较了三个候选 MVP 方向（ancestor explanation / declaration recommendation / premise retrieval），选择 ancestor explanation 作为 proof-side utility MVP。核心理由：直接映射 C2 和 C4、零新依赖零新训练、把 provenance-conditional finding 变成可体验的 hierarchy navigation 工具、与 ITP/CPP venue fit 高度对齐。已正面回应 R31：ancestor explanation 不是简单"列出祖先"而是 provenance-aware quality comparison tool，满足 CPP tool demo 标准。已明确 MVP 的输入、输出、验收标准、失败标准和不做事项。同步更新治理文档。Worker 未标记任务完成，等待 reviewer 只读审查。
76. `T52` 本轮已由 worker 完成执行。已重写 `docs/tasks/M5_paper/T52a_ancestor_explanation_demo.md` 作为唯一下游 demo 实现任务包。该包明确：(1) 新建 `proof_side_ancestor_explanation.py` CLI 脚本；(2) 加载 T42 provenance sweep 的 `node_embeddings.npy`（不重训、不加载 checkpoint）；(3) 支持 single-query mode 和 `explicit_vs_mixed` provenance comparison mode；(4) 包含 critical implementation note 关于 node ordering alignment（必须复用 `common.load_declaration_graph()` 的节点顺序）；(5) 要求新建 demo report；(6) Allowed files 限定为 2 新文件 + 4 治理文档，禁止修改任何已有代码；(7) reviewer type 为 adversarial。同步更新治理文档。Worker 未标记任务完成，等待 reviewer 只读审查。

## 8. 下一步

`T52` 已通过 `PASS` review 并正式收口。已确认 `docs/tasks/M5_paper/T52a_ancestor_explanation_demo.md` 作为唯一下游 demo 实现任务包。

下一轮应推进 `T52a`：基于 `T52a` 任务包实现 ancestor explanation demo CLI 脚本，加载 T42 reviewed artifacts 的 node embeddings，提供 single-query 和 provenance comparison 两种模式，并新建 demo report 文档。实现中必须注意 node ordering alignment（复用 `common.load_declaration_graph()` 的节点顺序）、精确 artifact path、以及 `--declaration-name` 对 `declarations.csv` 的精确匹配；comparison mode 为硬边界而非可选增强。

T50/T51 继承的核心事实边界：
- `explicit_only` 是 primary evidence，HGCN 在该 split 上稳定领先（FS MAP +0.1247, OR MAP +0.0557）。
- `synthesized_only` 是 controlled diagnostic，GCN 在该 split 上优于 HGCN；它说明双曲偏置在平坦结构上是劣势，但不是主对比证据。
- `hierarchy_mixed` 是 full source graph reproducibility check，结果与 T32/T33 完全一致，且 mixed graph 上 GCN 仍领先。
- 项目主结论必须保持 provenance-conditional：GCN 在 mixed graph 上仍领先，HGCN 只在 explicit-only hierarchy 上显现优势。
- `R28` 仍然活跃：Field.Subfield synthesized_only 的 aggregate/per-seed 口径差异尚未核清。
- `R29` 仍然活跃：`docs/experiment_reports/provenance_summary.md` Section 5.1 中 Field.Subfield synthesized_only 的 GCN MAP 表格单元写错，外部发表前必须修正。
- `R30` 仍然活跃：5 条 contributions 可能对 ITP/CPP 页数预算过宽，后续 drafting 时可能需要合并。
- `R31` 已缓解并获 `T51_review` 接受：但 `T52` 及后续实现仍不得把 demo 退化成纯祖先列表，必须保留 provenance-aware comparison mode。
- commit 时继续排除 `.claude/settings.json`。
## T33 Completion Note

- HGCN grouped 5-seed sweeps 已在与 `T32` 相同的 grouped runner / split / seed path 下完成，覆盖 `Field.Subfield` 与 `Order.Ring`。
- 报告：`docs/experiment_reports/hgcn_grouped_training.md`
- Artifact 根目录：`artifacts/baselines/relation_seed_sweeps/grouped_hgcn_field_subfield_t33/` 与 `artifacts/baselines/relation_seed_sweeps/grouped_hgcn_order_ring_t33/`
- 两组 sweep 均 `failed_runs = []`。
- Review 结论：`PASS`。
## T34 Completion Note

- Worker 已完成 `docs/experiment_reports/grouped_training_summary.md`。
- 报告明确了三条边界：
  1. `T32` vs `T33` 是合法的 matched grouped comparison。
  2. grouped-vs-binary 首先是 protocol difference，旧数值只能作为 historical alignment evidence，而不是 formal matched sweep 的直接 baseline。
  3. 当前 reviewed 的 Milestone 3 结论仍然是“GCN overall ahead，HGCN not established as stronger”。
- `T34` 没有新跑实验；它始终是 summary-only 文档任务。
- Review 结论：`PASS`。

## M3 Review Note

- `docs/review/M3_review.md` 给 Milestone 3 的结论是 `PASS_WITH_WARNINGS`。
- 当前可安全闭合的结论：
  - grouped training alignment 已完成，
  - matched GCN-vs-HGCN formal sweeps 已通过 review，
  - Milestone 4 可以继续推进。
- 剩余 warning：
  - clean-environment reproducibility 仍未完全闭合，不应被夸大表述。
