# 07 Handoff

> 更新时间：2026-05-23（T59 review PASS；T60 当前）
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

`T60` 是当前唯一任务：在不新增实验的前提下，对现有 submission-facing 文档集做 venue-formatting / final submission asset shaping。重点不是再改结论，而是把最后两处 submission-facing 收尾同步好：`paper_artifact_package.md` 中 `R30 page budget check` 的勾选状态，以及 `paper_outline.md` 中 Page Budget Note 对正文/appendix 取舍的自洽说明。

先读取 `docs/review/T59_review.md`、`docs/paper_artifact_package.md`、`docs/paper_outline.md`、`docs/paper_draft.md`、`docs/paper_figures_and_tables.md`、`docs/04_task_board.md`、`docs/05_decision_log.md`、`docs/07_handoff.md`、`docs/08_risks_and_open_questions.md`，确认 `T59` 已正式收口、当前状态仍为 **Narrow**，以及 `R25/R30/R08` 仍需保留。`T60` 不是新实验任务，而是把已稳定的 paper-facing 文本资产推进到更可直接提交的终态。

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
77. `T52a` 本轮已由 worker 完成执行。已新建 `proof_side_ancestor_explanation.py` CLI 脚本和 `ancestor_explanation_demo_report.md`。脚本加载 T42 reviewed node embeddings，支持 single-query mode（ranked ancestor list + per-query metrics + hop breakdown）和 `explicit_vs_mixed` comparison mode（side-by-side provenance quality comparison）。核心实现：(1) 通过 `common.load_declaration_graph()` 加载图数据并构建 `declaration_id → row_index` 映射对齐 embedding 行序；(2) 从 extends 边 BFS 构建祖先 ground truth；(3) cosine similarity 排序并计算 MAP/Recall@k；(4) comparison mode 自动在 explicit_only 和 hierarchy_mixed 两个图上运行并对比。已在 CommRing（FS）和 StrictOrderedCommRing（OR）上验证：OR 上 HGCN 的 provenance quality difference 尤为显著（MAP 0.6438 vs 0.1492）。同步更新治理文档。Worker 未标记任务完成，等待 adversarial reviewer 只读审查。
78. `T53` 本轮已由 worker 完成执行。已产出 `docs/review/T53_milestone_review.md`，verdict 为 **Narrow**。审查了 M1–M5 全部 reviewed 证据链（24 个 task，11 个 adversarial review），确认：(1) protocol/governance 已闭环；(2) grouped benchmark 已 reviewed；(3) provenance-conditional conclusion 已 reviewed；(4) proof-side bridge 已从 paper story 变成可运行 demo。活跃风险 R01/R03/R10/R25/R28/R29/R30 均按真实状态记录，未夸大 closure。推荐下一阶段为 paper-facing / packaging / cleanup，不跑新实验。同步更新治理文档。Worker 未标记任务完成，等待 reviewer 只读审查。

79. `docs/review/T53_review.md` 已给出 `PASS`。Captain 已将 `T53` 正式标记完成，并把 `D034` 从 `Pending Review` 更新为 `Accepted`。当前唯一任务已切换为 `T54`：先完成 `docs/paper_draft.md` 的首版正文草稿，严格继承 reviewed evidence 与 `docs/paper_outline.md` 的 claim boundary。

80. `T54` worker 已完成 paper-facing draft 首版产出。`docs/paper_draft.md` 包含 8 个一级章节（Title, Abstract, Introduction, Experimental Setup, Results, Discussion, Limitations, Conclusion）和附录（Evidence Chain + Numeric Anchors）。草稿严格继承 `docs/paper_outline.md` 的 claim boundary，保持 provenance-conditional 口径，显式保留 R28/R29/R30/R25 精度边界。Worker 未修改任何 forbidden scope 文件，未标记任务完成，等待 reviewer 只读审查。

81. `docs/review/T54_review.md` 已给出 `PASS_WITH_WARNINGS`。Captain 已将 `T54` 正式标记完成；warning 分类为：`synthesized_only` 表格非对称呈现 accepted presentation choice，Allowed Files 越界同步模式与摘要长度、Background / Related Work 缺口均 deferred，并已写回风险治理。当前唯一任务已切换为 `T55`：只对 `docs/paper_draft.md` 做第二轮 refinement，不新增实验、不修改 experiment reports。

82. `docs/review/T55_review.md` 已给出 `PASS_WITH_WARNINGS`。Captain 已将 `T55` 正式标记完成；warning 分类为：Allowed Files 越界同步模式 deferred 并写回 `R08`，Background / Related Work 子节承接 accepted，abstract 压缩 accepted，`D19` 关闭 accepted。当前唯一任务已切换为 `T56`，目标是清理 `R28/R29` 的 publication-facing precision 问题。

83. T56 worker 已完成 precision cleanup。`R29` 已修正：`provenance_summary.md` Section 5.1 表格中 FS GCN synthesized_only MAP 从 HGCN copy-paste 值修正为 verified T42 value `1.0000 ± 0.0000`。`R28` 已解析并关闭：T56 重新审计 T42 artifact 三个输出文件，确认原始 "aggregate vs per-seed discrepancy" 是 metric naming confusion（`test_average_precision` vs `grouped_test_map`），两条指标均计算正确、内部一致。`paper_draft.md` Section 5.4 表格已补入 FS GCN verified row，Section 5.7/7.1.5/7.1.6 及 Numeric Anchors appendix 已同步。治理文档全部同步。Worker 未标记任务完成，等待 reviewer 只读审查。
84. `docs/review/T56_review.md` 已给出 `PASS`。Captain 已将 `T56` 正式标记完成；无 blocking issue。reviewer 留下的 non-blocking notes 已直接并入下一轮 `T57` 任务设计：统一 `provenance_summary.md` Section 5 summary table 粒度、压缩 `paper_draft.md` Section 5.4 长解释段、并在治理文档中显式写清 `R28` closure 满足 `T56` 任务包的例外条件。当前唯一任务已切换为 `T57`。
85. T57 worker 已完成 figure/table source rendering。新建 `docs/paper_figures_and_tables.md` 作为 publication-facing 图表源文档（4 core tables + 2 core figure specs + 1 summary table + 跨文档引用一致性记录）。同步压缩了 `paper_draft.md` Section 5.4 长解释段（~120 词 → ~60 词），统一了 `provenance_summary.md` Section 5 summary table 中 FS synthesized_only 的粒度，更新了 `paper_outline.md` 中 R28/R29 的状态。Worker 未标记任务完成，等待 adversarial reviewer 只读审查。
86. `docs/review/T57_review.md` 已给出 `PASS`。Captain 已将 `T57` 正式标记完成，并把当前唯一任务切换为 `T58`。`T57_review` 的非阻塞点不回头重开 `T57`：`paper_figures_and_tables.md` Section 4 的 stale “Pending sync” rows 与 `paper_draft.md` Section 5.4 的一句 mechanistic detail 取舍并入 `T58` artifact packaging；`.claude/settings.json` 继续排除出提交。
87. T58 worker 已完成 artifact packaging。新建 `docs/paper_artifact_package.md`，包含 source-to-claim 映射（C1–C5 + central claim）、table/figure-to-source 映射（5 core tables + 2 core figures）、已知排除项、活跃风险边界（R25/R30/R08）和提交检查清单。修正了 `paper_figures_and_tables.md` Section 4 的 stale “Pending sync” rows（改为 “Aligned (T57)”）。在 `paper_draft.md` Section 5.4 补回一句 mechanistic detail。未新增实验、未引入未 review 数值。
88. `docs/review/T58_review.md` 已给出 `PASS`。Captain 已将 `T58` 正式标记完成，并把当前唯一任务切换为 `T59`。`T58_review` 的两个 non-blocking notes 不回头重开 `T58`：`paper_artifact_package.md` 中 core-table 术语统一，以及 Table T1 的 HGCN source mapping 精度说明，统一并入 `T59` 的最终 paper editing / venue shaping。
89. T59 worker 已完成 final paper editing / venue shaping。Contribution-count decision: 保持 5 条（C1–C5），加入 page-budget-aware 措辞。`paper_artifact_package.md` core-table 术语统一为"4 core tables + 1 summary table"，Table T1 HGCN source mapping 已写成"T33 primary, T42 cross-check"。`paper_draft.md`、`paper_outline.md`、`paper_figures_and_tables.md` 已同步收束。治理文档全部更新。
90. `docs/review/T59_review.md` 已给出 `PASS`。Captain 已将 `T59` 正式标记完成，并把当前唯一任务切换为 `T60`。`T59_review` 的两个 non-blocking notes 不回头重开 `T59`：`paper_artifact_package.md` 中 `R30 page budget check` 的勾选同步，以及 `paper_outline.md` Page Budget Note 的自洽性补强，统一并入 `T60` 的 venue-formatting / final submission asset shaping。

## 8. 下一步

`T60` 是当前唯一任务，目标是 venue-formatting / final submission asset shaping。

T53 milestone review 的核心结论：
- **Verdict: Narrow**（收窄为 paper-facing / packaging / cleanup）
- 五个 Milestone 的 reviewed 证据链已闭合（24 个 task 通过 review，11 个 adversarial review）
- 核心 provenance-conditional finding 已确立：HGCN 仅在 `explicit_only` 上领先（FS MAP +0.1247, OR MAP +0.0557），`hierarchy_mixed` 上 GCN 仍领先
- Proof-side bridge 已变成可运行 CLI demo（T52a adversarial PASS）
- 当前不需要新实验、新模型、新数据源或新 demo
- 最紧迫的工作已从 artifact packaging / final paper editing 切换为 final submission asset shaping

T59 review 后：
- 当前状态：`T59` 已通过 review，当前唯一任务为 `T60`
- `docs/paper_artifact_package.md` 已建立为 submission-facing artifact package
- `docs/paper_figures_and_tables.md` 已建立为 publication-facing 图表 source-of-truth
- `R28` 已关闭：原始 "aggregate vs per-seed discrepancy" 经 T56 artifact 审计确认为 metric naming confusion（`test_average_precision` vs `grouped_test_map`），两条指标均计算正确、内部一致
- `R29` 已修正：`provenance_summary.md` Section 5.1 表格已修正为 verified T42 value `1.0000 ± 0.0000`；`paper_draft.md` 已同步
- 当前优先：venue-formatting / final submission asset shaping
- `T59_review` 的非阻塞点：同步 `paper_artifact_package.md` 中 `R30 page budget check` 的勾选状态；补强 `paper_outline.md` Page Budget Note 对正文/appendix 取舍的自洽说明
- 当前不推荐：新实验、新 demo、新模型、新数据源

T50/T51 继承的核心事实边界（保持不变）：
- `explicit_only` 是 primary evidence，HGCN 在该 split 上稳定领先（FS MAP +0.1247, OR MAP +0.0557）。
- `synthesized_only` 是 controlled diagnostic，GCN 在该 split 上优于 HGCN（FS +0.3143, OR +0.0893）。
- `hierarchy_mixed` 是 full source graph reproducibility check，结果与 T32/T33 完全一致，且 mixed graph 上 GCN 仍领先。
- 项目主结论必须保持 provenance-conditional。
- `R30` 仍然活跃：5 条 contributions 可能对 ITP/CPP 页数预算过宽，后续 drafting 时可能需要合并。
- `R31` 已缓解并获 `T51_review` 接受。
- `R25` 仍然活跃：clean-environment reproducibility 尚未完成。
- commit 时继续排除 `.claude/settings.json`。

T60 之后的候选方向：
- final repo packaging / handoff freeze（仅在 `T60` 收口并经 review 后再决定）
- 当前不推荐：新实验、新 demo、新模型、新数据源

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
