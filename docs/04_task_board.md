# 04 Task Board

> 更新时间：2026-05-18（T51 review 后更新）
>
> Captain 原则：每轮只推进一个 `Current Unique Task`。Worker 不自动领取下一任务。

## Project Status

- 2026-05-17 captain update: `T34` 已通过 milestone review，Milestone 3 收口完成。
- 状态：Continue
- 当前阶段：Milestone 5 已启动；`T50` 已通过 review 并收口，`T51` 已通过 review 并完成 MVP 选型，当前唯一任务切换为 `T52`
- 当前主线：`benchmark / protocol / diagnostics`
- 当前不主张：把“已经证明 HGCN 稳定优于 GCN”写成既成事实
- 当前证据等级：已有真实实验与工程原型，但尚未冻结成正式 benchmark artifact

## Milestone 0: Governance Bootstrap

- [x] T00: 创建根目录 `README.md`、`AGENTS.md`、`CLAUDE.md`，把项目定位、执行入口和 agent 规则写入仓库入口
- [x] T01: 审查并校正 `docs/00~08` 与 `docs/tasks` 的一致性，确保任务包可以直接交给 worker
- [x] T02: 建立 `docs/review/` 的 review 模板，并记录治理初始化 review（由 PM 裁决：现有 Claude review 文档已满足当前阶段需要）

## Milestone 1: Data And Protocol Freeze

- [x] T10: 生成版本锁定与数据资产 manifest，覆盖 Lean、Mathlib、LeanDojo、Python 依赖、关键 config 与现有 artifact
- [x] T11: 写出 data card，描述当前可用图、字段、relation provenance、coverage-aware 处理与 unresolved 语义
- [x] T12: 固化 grouped multi-positive ancestor retrieval 协议，确认代码入口、配置字段、指标名与输出格式
- [x] T13: 增加或校验 hop bucket 常规报告入口，确保 `hop_2 / hop_3 / hop_4_plus` 出现在正式结果中
- [x] T14: Milestone 1 收口 smoke check 与轻量清理，确认协议字段在最小运行或静态样例中实际落盘

## Milestone 2: Diagnostics And Candidate Graph Selection

- [x] T20: 复查 `real_graphs_v1`、`hierarchy_focus_v1`、`mathlib_order_focus_v1` 诊断产物，形成候选图优先级表
- [x] T21: 对 module-level candidate scan 输出做 data-quality 审计，标出更深、更连续、更适合双曲检验的图
- [x] T22: 为 shallow forest / star forest 判断写出可复用诊断阈值与报告模板

## Milestone 3: Grouped Retrieval Training Alignment

- [x] T30: 阅读现有 grouped retrieval training 代码，定位 binary edge classification 与 grouped retrieval 的错配点
- [x] T31A: 实现并校验 grouped ancestor retrieval 的 query-level split completeness
- [x] T31: 实现最小 query-grouped loss 方案，优先 `sampled softmax` 或 `InfoNCE`，只接一个现有 config
- [x] T32: 在 `Field.Subfield` 与 `Order.Ring` 上跑 GCN 5-seed grouped training 对照
- [x] T33: 在相同 split 与参数预算下跑 HGCN 5-seed grouped training 对照
- [x] T34: 汇总 grouped training 与旧 binary training 的差异，写入诊断报告

## Milestone 4: Relation Provenance Split

- [x] T40: 冻结 `explicit-only / synthesized-only / mixed` 三类图的生成配置与输出位置
- [x] T41: 生成三类 provenance 图并运行结构诊断，比较深度、叶子比例、连通性与 hyperbolicity proxy
- [x] T42: 对三类 provenance 图运行 grouped retrieval / parent prediction 的 GCN 与 HGCN seed sweep
- [x] T43: 汇总 provenance split 结果，回答 synthesized relation 是否削弱双曲优势

## Milestone 5: Paper And Proof-Side Bridge

- [x] T50: 整理论文贡献骨架，围绕 pipeline / protocol / diagnostics / conditional hyperbolic conclusion
- [x] T51: 选择一个 proof-side utility MVP，例如 ancestor explanation 或 relation-aware declaration recommendation
- [ ] T52: 为 proof-side utility 写最小 demo 任务包，不承诺端到端 theorem proving
- [ ] T53: 完成里程碑审查，判断项目进入 Continue / Narrow / Resume-ready

## Current Unique Task

`T52`: 为已选定的 ancestor explanation proof-side MVP 编写最小 demo 实现任务包，不承诺端到端 theorem proving。
任务包如下：

`docs/tasks/M5_paper/T52_proof_side_demo_package.md`

## Why Now

`T51` 已把 proof-side bridge 收束为 ancestor explanation MVP，并在 review 中证明它不是过轻的“列祖先列表”，而是 provenance-aware quality comparison tool。当前最缺的不是再讨论候选方向，而是把后续实现边界写成可直接派给 worker 的最小 demo 任务包，明确 CLI 入口、artifact 依赖、比较模式、验证命令与禁止事项，避免后续实现阶段发生 scope creep。
## Worker Package Summary

- Task ID: `T52`
- Allowed files:
  - `docs/tasks/M5_paper/T52a_ancestor_explanation_demo.md`
  - `docs/05_decision_log.md`
  - `docs/04_task_board.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Forbidden scope:
  - 不实现 demo，不新增实验，不修改代码
  - 不承诺端到端 theorem proving，不把 proof-side MVP 写成“已证明可提升完整证明成功率”
  - 不引入新的大型依赖，不把当前任务扩张成多条 proof-side 支线并行开发
  - 不改写 T50 已确认的 provenance-conditional 论文口径，不忽略 `R28`/`R29`/`R31`
- T51/T52 handoff notes:
  - Authoritative `T52` scope is `docs/tasks/M5_paper/T52_proof_side_demo_package.md` and downstream package `docs/tasks/M5_paper/T52a_ancestor_explanation_demo.md`.
  - 必须把 MVP 选择写成 paper bridge，而不是独立的新研究主线。
  - 必须比较至少 paper outline 中已经列出的候选方向，并解释为何最终选择更适合当前证据和 venue fit。
  - 若继续推荐 ancestor explanation，必须正面回应 `R31`：说明为何它不会轻到不足以支撑 CPP/工具演示叙事；否则应选择更强的 utility 方向。
  - 必须明确输入、输出、验收标准、失败标准与不做事项，以便 `T52` 能把它拆成最小 demo 任务包。
- Verification:
  - `rg -n "Task ID|Goal|Why now|Allowed files|Forbidden scope|Inputs to read|Expected output|Verification|Docs to update|Reviewer type" docs\tasks\M5_paper\T52a_ancestor_explanation_demo.md`
  - `rg -n "ancestor explanation|explicit_only|hierarchy_mixed|CLI|artifact|comparison|no new dependencies|no retraining" docs\tasks\M5_paper\T52a_ancestor_explanation_demo.md`
  - `rg -n "T52|T52a|Current Unique Task|proof-side|demo" docs\04_task_board.md docs\05_decision_log.md docs\07_handoff.md docs\08_risks_and_open_questions.md docs\tasks\M5_paper\T52a_ancestor_explanation_demo.md`

## Execution Note
- 2026-05-10：`T00` 已通过 review，根目录入口文档与相关 handoff 文档已收口。
- 2026-05-10：当前唯一任务切换为 `T01`，用于复查治理文档之间的一致性。
- 2026-05-10：`docs/reference/AI_coding_workflow.md` 中与 `T00` 无关的 reviewer prompt 微调，已并入 `T01` 的一致性复查范围，不再作为悬置改动单独跟踪。
- 2026-05-10：`T01` review 结论为 `PASS_WITH_WARNINGS`；warnings 已接受并闭合，当前唯一任务切换为 `T10`。
- 2026-05-10：未发现 `docs/review/T02_review.md`，因此 `T02` 不标记完成，仅暂缓。
- 2026-05-10：`T10` 已产出 `docs/data_manifest.md` 草稿，完成版本锚点、代表性 config 入口与 artifact 根目录清点；`lean4-example`、LeanDojo、Python 环境等未能从可复现实据锁定的字段继续保留为 `unknown / needs verification`。
- 2026-05-10：`T10` 已通过 review，标记完成；`unknown / needs verification` 字段作为后续补证项保留，不阻塞 T11。
- 2026-05-10：PM 裁决 T02 可视为当前阶段完成，因为 `docs/review` 中已有可信 Claude review 文档覆盖已完成 task。
- 2026-05-10：当前唯一任务切换为 `T11`。
- 2026-05-10：`T11` 已产出 `docs/data_card.md` 草稿，明确当前可用图、基础字段、`uses / extends / instance_of` relation 语义、coverage-aware 处理规则，以及哪些图只适合诊断或历史用途。
- 2026-05-10：`T11` review 结论为 `PASS`；`docs/data_card.md` 成为 reviewed data card，新增的 provenance schema 边界风险继续在 R11 / Open Question 9 中跟踪。
- 2026-05-10：当前唯一任务切换为 `T12`，用于冻结 grouped retrieval 协议、代码入口、配置字段、指标名与输出格式；后续 worker 不应自动执行 T12，需新会话按任务包领取。
- 2026-05-10：`T12` 已产出 `docs/grouped_retrieval_protocol.md` 草稿，并更新 `docs/06_eval_protocol.md`，明确 legacy `task = ancestor_ranking` 与正式 grouped multi-positive 协议之间的映射、关键配置字段、代码入口与标准输出字段。
- 2026-05-10：`T12` 对 `project_bootstrap/baseline_scaffold/src/run_relation_grouped_retrieval_baseline.py` 做了最小字段对齐，补齐 `grouped_test_ndcg_at_10` 到 `result_summary.json`。
- 2026-05-11：`docs/review/T12_review.md` 结论为 `PASS`，blocking issues、non-blocking issues 与 missing verification 均为 none；Captain 判定无需 warning 分类或返修。
- 2026-05-11：`T12` 标记完成，`docs/grouped_retrieval_protocol.md` 成为 reviewed grouped protocol freeze；当前唯一任务切换为 `T13`，但本轮不执行 T13。
- 2026-05-11：`T13` 本轮完成 worker 实现，向 `run_relation_gcn_baseline.py`、`run_relation_hyperbolic_baseline.py`、`run_relation_grouped_retrieval_baseline.py` 的 `result_summary.json` 补齐 `hop_2 / hop_3 / hop_4_plus` 平铺字段。
- 2026-05-11：`T13` 同步更新 `run_relation_seed_sweep.py` 与 `_patch_sweep_reports.py`，让 seed sweep `report.md` 显式展示 hop bucket 聚合与 per-seed 结果。
- 2026-05-11：`T13` 已运行任务包静态校验 `rg -n "hop_2|hop_3|hop_4_plus|hop" project_bootstrap\baseline_scaffold\src docs\06_eval_protocol.md`。
- 2026-05-11：`docs/review/T13_review.md` 结论为 `PASS`，blocking issues 为 none；Captain 判定可标记完成。
- 2026-05-11：T13 review 的非阻塞问题分类：helper duplication 与未来端到端 spot-check 记为 deferred；per-seed table 只展示 MAP/nDCG 记为 accepted presentation choice；doc status wording 由 Captain 收口修正。
- 2026-05-11：`T13` 标记完成，当前唯一任务切换为 `T14`；本轮不执行 T14。
- 2026-05-11：`T14` 本轮新增最小 smoke config `project_bootstrap/baseline_scaffold/configs/relation_gcn_typeclass_precise_v2_ancestor_ranking_smoke_t14.json`，输出到 `artifacts/smoke/`，不作为正式 benchmark 结果。
- 2026-05-11：`T14` 已用 `C:\ProgramData\anaconda3\envs\DLEnv\python.exe` 成功运行单次最小 GCN smoke，生成 `artifacts/smoke/relation_gcn_lean4_example_typeclass_precise_v2_ancestor_ranking_smoke_t14/{metrics,result_summary}.json`，确认 `grouped_test_ndcg_at_10` 与 `hop_2 / hop_3 / hop_4_plus` 字段真实落盘。
- 2026-05-11：`T14` 已把 `flatten_grouped_hop_bucket_summary` 去重到 `project_bootstrap/baseline_scaffold/src/relation_baseline_common.py`。
- 2026-05-12：`docs/review/T14_review.md` 结论为 `PASS`，blocking issues 为 none；Captain 判定可标记完成。
- 2026-05-12：T14 review 的非阻塞问题分类：`.claude/settings.json` 自动权限改动为 rejected/excluded from commit；`format_metric` duplication 为 deferred，继续由 D05 跟踪；只 smoke GCN runner 为 accepted low residual risk，因为三个 runner 已共享同一 helper。
- 2026-05-12：`T14` 标记完成，Milestone 1 闭合；当前唯一任务切换为 `T20`，但本轮不执行 T20。
- 2026-05-12：`T20` 已由 worker 完成现有 diagnostics 复查与候选图优先级摘要，产出 `docs/diagnostics_summary.md`，并同步更新 handoff 与风险文档。
- 2026-05-12：`docs/review/T20_review.md` 结论为 `PASS_WITH_WARNINGS`，blocking issues 为 none；Captain 判定可标记完成。
- 2026-05-12：T20 review 的 warning 分类：`n/a` 数值补全与单表混合指标来源标注均 deferred，写入 R13 / D07；不影响候选优先级或 T20 完成。
- 2026-05-12：`T20` 标记完成，当前唯一任务切换为 `T21`；本轮不执行 T21。
- 2026-05-12：`T21` 已由 worker 完成 module-level candidate scan data-quality audit，新增 `docs/candidate_graph_audit.md`，并同步更新 handoff 与风险文档；随后进入 reviewer 只读审查。
- 2026-05-12：`docs/review/T21_review.md` 结论为 `PASS`，blocking issues 为 none；Captain 判定可标记完成。
- 2026-05-12：T21 review 的 non-blocking issues 分类：`depth` 列名歧义、审计表选择范围说明不足、mathlib module scan standalone config traceability gap 均为 deferred，写入 R15 / R16 / D08；不影响 T21 完成。
- 2026-05-12：`T21` 标记完成，当前唯一任务切换为 `T22`；本轮不执行 T22。
- 2026-05-12：`T22` 已由 worker 产出 `docs/diagnostics_protocol.md` 草案，并同步更新 `docs/06_eval_protocol.md`、`docs/07_handoff.md` 与 `docs/08_risks_and_open_questions.md`；随后进入 reviewer 只读审查。
- 2026-05-13：`docs/review/T22_review.md` 结论为 `PASS`，blocking issues 为 none；Captain 判定可标记完成。
- 2026-05-13：T22 review 的 non-blocking issues 分类：shallow forest flag condition 3 语义可能误导、report template 缺少 `multi-parent count`、`ancestor_added_nodes` 缺少内联定义均为 deferred，写入 R18 / D09；不影响 T22 完成。
- 2026-05-13：`T22` 标记完成，Milestone 2 闭合；当前唯一任务切换为 `T30`，本轮不执行 T30。
- 2026-05-13：`T30` 已由 worker 产出 `docs/training_alignment_audit.md` 草案，并同步更新 `docs/07_handoff.md` 与 `docs/08_risks_and_open_questions.md`；随后进入 reviewer 只读审查。
- 2026-05-13：`docs/review/T30_review.md` 结论为 `PASS`，blocking issues 为 none；Captain 判定可标记完成。
- 2026-05-13：T30 review 的 non-blocking issues 分类：Section 4 heading nesting、M6 mixed-language title、M3 rough impact estimate 均为 deferred，写入 D11；不影响 T30 完成。
- 2026-05-13：`T30` 标记完成；由于 R19 是 grouped benchmark 前置风险，Captain 插入 `T31A` query-level split completeness 任务，当前唯一任务切换为 `T31A`，本轮不执行 T31A。
- 2026-05-13：`T31A` 已由 worker 完成代码与文档草案：`ancestor_ranking` 路径改为 query-level split，并把 split disjointness 摘要写入 `run_manifest.json -> task_summary`；随后进入 adversarial reviewer 只读审查。
- 2026-05-13：`docs/review/T31A_review.md` 结论为 `PASS`，blocking issues 为 none；Captain 判定可标记完成。
- 2026-05-13：T31A review 的 non-blocking issues 处理：`ancestor_label_mode` 与 query key 交互写入 T31 注意事项；R19 从 Active 更新为 Mitigated；Section numbering 继续由 D11 跟踪；rare relation type 的 split 覆盖率作为后续 grouped benchmark 注意事项保留，不阻塞 T31A。
- 2026-05-13：`T31A` 标记完成；当前唯一任务切换为 `T31`，本轮只推荐下一任务，不执行 T31。
- 2026-05-13：`T31` 已由 worker 完成最小 grouped training 实现：`run_relation_grouped_retrieval_baseline.py` 复用 `build_grouped_ranking_queries(...)` 构造训练 query，训练 key 与 T31A 已 review 的 split / eval key 显式对齐到 `(src_id, relation_type)`。
- 2026-05-13：`T31` 新增最小 smoke config `project_bootstrap/baseline_scaffold/configs/relation_grouped_gcn_typeclass_precise_v2_ancestor_ranking_smoke_t31.json`，并完成单次 smoke；artifact 落在 `artifacts/smoke/relation_grouped_gcn_lean4_example_typeclass_precise_v2_ancestor_ranking_smoke_t31/`。
- 2026-05-16：`docs/review/T31_review.md` 结论为 `PASS`，blocking issues 为 none；Captain 判定可标记完成。
- 2026-05-16：T31 review 的 non-blocking issues 处理：`infonce` 作为 `sampled_softmax` alias 为 accepted current behavior；`negative_ratio` 默认差异与 `total_loss` device 初始化清理为 deferred；Captain 级治理文档更新为 accepted scope distinction；`.claude/settings.json` 自动权限 diff 为 rejected/excluded from commit。
- 2026-05-16：`T31` 标记完成；当前唯一任务切换为 `T32`，本轮只推荐下一任务，不执行 T32。
- 2026-05-17：`T32` 本轮已由 worker 补齐正式 grouped GCN configs：`grouped_gcn_field_subfield_anc_t32.json`、`grouped_gcn_field_subfield_sweep_t32.json`、`grouped_gcn_order_ring_anc_t32.json`、`grouped_gcn_order_ring_sweep_t32.json`。两份 base config 均显式设置 `grouped_loss = "sampled_softmax"` 与 `negative_ratio = 10.0`。
- 2026-05-17：`T32` 已使用 reviewed grouped retrieval runner / seed sweep path 完成两组真实 5-seed GCN grouped training sweep；artifact 位于 `artifacts/baselines/relation_seed_sweeps/grouped_gcn_field_subfield_t32/` 与 `artifacts/baselines/relation_seed_sweeps/grouped_gcn_order_ring_t32/`，两组 sweep 均 `failed_runs = []`。
- 2026-05-17：`T32` 已新增 `docs/experiment_reports/gcn_grouped_training.md`，汇总精确命令、config 路径、artifact 路径、seed 列表、grouped mean/std 指标与 hop bucket 聚合。
- 2026-05-17：`docs/review/T32_review.md` 结论为 `PASS`，blocking issues 为 none；Captain 判定可标记完成。
- 2026-05-17：T32 review 的 non-blocking issues 处理：Section 5 hop bucket 表呈现精简为 accepted presentation choice；`grouped MAP` / `gMAP` 混用为 deferred wording cleanup；无 rejected warning。
- 2026-05-17：`T32` 标记完成；当前唯一任务切换为 `T33`，本轮只推荐下一任务，不执行 T33。
- 2026-05-17：`docs/review/T33_review.md` 结论为 `PASS`，无 blocking issues。
- 2026-05-17：`T33` 标记完成；当前唯一任务切换为 `T34`，本轮只推荐下一任务，不执行 T34。
- 2026-05-17：`docs/review/T34_review.md` 结论为 `PASS`，无 blocking issues。
- 2026-05-17：`T34` 标记完成；Milestone 3 闭合；当前唯一任务切换为 `T40`，本轮只推荐下一任务，不执行 T40。
- 2026-05-17：`docs/review/M3_review.md` 结论为 `PASS_WITH_WARNINGS`；允许进入 Milestone 4，但 clean-environment reproducibility 仍保留警告。
- 2026-05-17：`T40` 本轮已由 worker 完成配置冻结与协议文档草案。新增两份 provenance split config：`provenance_split_field_subfield_t40.json`、`provenance_split_order_ring_t40.json`；新增 `docs/provenance_split_protocol.md`，冻结三类 provenance 图的生成配置、输出目录约定、origin_map 与 split 语义，并为 T41/T42 提供直接可复用的协议入口。Worker 未运行 seed sweep，未修改数据语义，未覆盖历史配置。随后进入 adversarial reviewer 只读审查。
- 2026-05-17：`docs/review/T40_review.md` 结论为 `PASS`，无 blocking issues。Captain 判定 `T40` 完成并将当前唯一任务切换到 `T41`。reviewer 的 non-blocking notes 已转成 `T41` 执行要求：必须校验预期边数，并程序化验证 `hierarchy_mixed = full source graph` identity。
- 2026-05-17：`T41` 本轮已由 worker 完成执行。已运行 T40 冻结配置生成六个 provenance split 图目录，所有边数与协议预期一致；已程序化验证 `hierarchy_mixed = full source graph` identity（两组候选图均确认）；已对六个 split 图运行结构诊断，artifact 位于 `artifacts/diagnostics/provenance_split_t41/`；已产出 `docs/experiment_reports/provenance_diagnostics.md`。核心发现：`synthesized_only` 图在两组候选上均为 longest chain = 1、multi-parent = 0、cycle rank = 0 的浅层星状森林；所有层级深度和多父节点分支均来自 `explicit_only`（`extends`）边；混合图从 synthesized 边继承的是叶子膨胀和碎片化，不是深度。Worker 未运行模型训练，未覆盖已有 diagnostics，未改动 T40 冻结语义。随后进入 adversarial reviewer 只读审查。

- 2026-05-17：`docs/review/T41_review.md` 结论为 `PASS`，无 blocking issues。Captain 判定 `T41` 完成并将当前唯一任务切换到 `T42`；reviewer 的非阻塞意见不要求返修，但已转成 `T42` 执行约束：`explicit_only` 作为 primary split，`synthesized_only` 作为 controlled diagnostic，`hierarchy_mixed` 作为 T32/T33 reproducibility check，同时任务包补入 tool-side config Allowed Files。
- 2026-05-18：`T42` 本轮已由 worker 完成执行。已创建 24 份 provenance sweep config（12 base + 12 sweep），在两组候选图的三个 provenance split 上运行了 GCN 和 HGCN 各 5-seed grouped retrieval sweep（共 60 次训练，零失败）。核心发现：(1) `explicit_only` 上 HGCN 首次在两组候选图上均超过 GCN（Field.Subfield MAP +0.1247, Order.Ring MAP +0.0557），且优势随 hop 深度单调增长；(2) `synthesized_only` 上 GCN 反超 HGCN，确认 HGCN 的双曲归纳偏置在平坦结构上是劣势；(3) `hierarchy_mixed` 结果与 T32/T33 完全一致（精确匹配），验证了 reproducibility 和 `hierarchy_mixed = full source graph` identity。新增报告 `docs/experiment_reports/provenance_seed_sweeps.md`。Worker 未覆盖已有 sweep artifact，未修改 T40/T41 冻结语义。随后进入 adversarial reviewer 只读审查。
- 2026-05-18：`docs/review/T42_review.md` 结论为 `PASS`，无 blocking issues。Captain 判定 `T42` 完成并将当前唯一任务切换到 `T43`；reviewer 的精度提醒不要求返修，但已转成 `T43` 的文稿约束：必须注明 `Field.Subfield explicit_only` 的 `hop_4_plus` 均值仅基于 4/5 seeds，必须登记 `synthesized_only` 中 GCN aggregate 与 per-seed 记录的口径差异，且 `.claude/settings.json` 继续 rejected/excluded from commit。
- 2026-05-18：`T43` 本轮已由 worker 完成执行。已产出 `docs/experiment_reports/provenance_summary.md`，汇总 T41 结构诊断与 T42 provenance-aware seed sweeps 的核心发现。报告明确写入：(1) `explicit_only` 是 primary evidence，HGCN 在该 split 上稳定领先（FS MAP +0.1247, OR MAP +0.0557），优势随 hop 深度单调增长；(2) `synthesized_only` 是 controlled diagnostic，GCN 在该 split 上优于 HGCN，确认双曲归纳偏置在平坦结构上是劣势；(3) `hierarchy_mixed` 是 full source graph reproducibility check，结果与 T32/T33 完全一致；(4) synthesized 边的作用是结构性稀释，不贡献层级深度；(5) 项目结论精化为 provenance-conditional：GCN 在 mixed graph 上仍领先，HGCN 只在 explicit-only hierarchy 上显现优势。精度约束已满足：FS `hop_4_plus` 基于 4/5 seeds 已注明；`synthesized_only` aggregate/per-seed 口径差异已登记为待核清项。Worker 未新增训练或修改 T40/T41/T42 冻结语义。随后进入 review。
- 2026-05-18：`docs/review/T43_review.md` 结论为 `PASS`，无 blocking issues。Captain 判定 `T43` 完成并闭环 Milestone 4，将当前唯一任务切换到 `T50`。reviewer 的非阻塞问题分类为：Field.Subfield `synthesized_only` 在 `docs/experiment_reports/provenance_summary.md` Section 5.1 的 GCN MAP 表格值错误记为 deferred publication-precision fix（写入 `R29`）；`.claude/settings.json` 自动权限 diff 继续记为 rejected/excluded from commit；R04 继续保留为 provenance-conditional `Mitigated` 记为 accepted classification judgment。
- 2026-05-18：`T50` 本轮已由 worker 完成执行。已产出 `docs/paper_outline.md`，包含 working title、one-paragraph positioning、central claim 与 non-claim 边界、5 条 contributions、evidence ladder（Milestone 1~4）、figures/tables plan、threats to validity、venue fit（ITP/CPP/FM）、proof-side bridge 说明、provenance-precision boundaries 和 draft section outline。所有内容均保持 provenance-conditional 口径：`explicit_only` 为 primary evidence，`synthesized_only` 为 controlled diagnostic，`hierarchy_mixed` 为 reproducibility check；未新增实验、未改动 T40~T43 冻结语义、未将 mixed graph 结论改写为 HGCN 整体优势。已绕开 R28/R29 未闭环精度问题。同步更新治理文档。Worker 未标记任务完成，等待 reviewer 只读审查。
- 2026-05-18：`T51` 本轮已由 worker 完成执行。已产出 `docs/proof_side_mvp.md`，比较了三个候选 MVP 方向（ancestor explanation / declaration recommendation / premise retrieval），选择 ancestor explanation 作为 proof-side utility MVP。核心理由：(1) 直接映射 C2 和 C4；(2) 零新依赖、零新训练；(3) 把 provenance-conditional quality difference 变成可体验的 hierarchy navigation 工具；(4) 与 ITP/CPP venue fit 高度对齐。已正面回应 R31：ancestor explanation 是 provenance-aware quality comparison tool，不是简单的"列出祖先"。已明确输入、输出、验收标准、失败标准和不做事项。同步更新治理文档。Worker 未标记任务完成，等待 reviewer 只读审查。
- 2026-05-18：`docs/review/T51_review.md` 结论为 `PASS`。Captain 判定 `T51` 正式完成并将 `D031` 从 pending review 更新为 `Accepted`；当前唯一任务切换为 `T52`，目标是把 ancestor explanation MVP 进一步收敛成唯一的下游 worker demo package。`R31` 已在本轮审查中获得接受，但 `T52/T52a` 后续实现仍必须保留 provenance-aware comparison mode，不能退化成纯祖先列表。
## T33 Completion Update (2026-05-17)

- Worker 已在 `T32` 所使用的 reviewed grouped runner / split / seed path 下，完成 `Field.Subfield` 与 `Order.Ring` 两组正式 HGCN grouped 5-seed sweep。
- 新增正式配置：`grouped_hgcn_field_subfield_anc_t33.json`、`grouped_hgcn_field_subfield_sweep_t33.json`、`grouped_hgcn_order_ring_anc_t33.json`、`grouped_hgcn_order_ring_sweep_t33.json`。
- 新增 artifact 根目录：`artifacts/baselines/relation_seed_sweeps/grouped_hgcn_field_subfield_t33/` 与 `artifacts/baselines/relation_seed_sweeps/grouped_hgcn_order_ring_t33/`；两组 sweep 均 `failed_runs = []`。
- 新增报告：`docs/experiment_reports/hgcn_grouped_training.md`。
- 结果摘要：在 matched grouped protocol 下，HGCN 没有在任一目标图上超过 reviewed 的 T32 GCN grouped baseline。
- Review 结论：`PASS`。`T34` 可作为 summary-only 后续任务推进，但不应重新打开 T33 实现范围。

## After Completion

Worker 完成后需要 reviewer 只读审查。Captain 根据 review 结果更新：

- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/05_decision_log.md`（如果产生关键决策）
## T34 Completion Update (2026-05-17)

- Worker 已完成 `docs/experiment_reports/grouped_training_summary.md`，作为 summary-only 后续收口报告。
- 报告明确区分了 matched grouped `T32`/`T33` 的直接可比性，与历史 grouped-vs-binary 证据之间的边界。
- 报告明确写出：`T32` 与 `T33` 可直接比较，而早期 grouped-vs-binary gain 仅作为 alignment evidence，不可直接与 formal matched sweep 数值混排。
- Worker 未改动任何 sweep artifact，也未重新打开 `T32` 或 `T33`。
- Review 结论：`PASS`。Milestone 3 可以闭合，项目可切换到 `T40`。
