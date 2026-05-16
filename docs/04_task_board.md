# 04 Task Board

> 更新时间：2026-05-16
>
> Captain 原则：每轮只推进一个 `Current Unique Task`。Worker 不自动领取下一任务。

## Project Status

- 状态：Continue
- 当前阶段：Milestone 3 grouped retrieval training alignment；T31 已通过 adversarial review，当前推荐 T32 运行 GCN grouped training 5-seed sweep
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
- [ ] T32: 在 `Field.Subfield` 与 `Order.Ring` 上跑 GCN 5-seed grouped training 对照
- [ ] T33: 在相同 split 与参数预算下跑 HGCN 5-seed grouped training 对照
- [ ] T34: 汇总 grouped training 与旧 binary training 的差异，写入诊断报告

## Milestone 4: Relation Provenance Split

- [ ] T40: 冻结 `explicit-only / synthesized-only / mixed` 三类图的生成配置与输出位置
- [ ] T41: 对三类 provenance 图运行结构诊断，比较深度、叶子比例、连通性与 hyperbolicity proxy
- [ ] T42: 对三类 provenance 图运行 grouped retrieval / parent prediction 的 GCN 与 HGCN seed sweep
- [ ] T43: 汇总 provenance split 结果，回答 synthesized relation 是否削弱双曲优势

## Milestone 5: Paper And Proof-Side Bridge

- [ ] T50: 整理论文贡献骨架，围绕 pipeline / protocol / diagnostics / conditional hyperbolic conclusion
- [ ] T51: 选择一个 proof-side utility MVP，例如 ancestor explanation 或 relation-aware declaration recommendation
- [ ] T52: 为 proof-side utility 写最小 demo 任务包，不承诺端到端 theorem proving
- [ ] T53: 完成里程碑审查，判断项目进入 Continue / Narrow / Resume-ready

## Current Unique Task

`T32`: 在 `Field.Subfield` 与 `Order.Ring` 上跑 GCN 5-seed grouped training 对照。

任务包位置：

`docs/tasks/M3_training/T32_gcn_grouped_training_sweep.md`

## Why Now

`T31` 已通过 adversarial review，确认 grouped retrieval runner 的训练 query、split 与 eval 均使用 `(src_id, relation_type)` key，且 best checkpoint 由 grouped val MAP 驱动。下一步需要先跑 GCN 5-seed grouped training sweep，建立欧氏 baseline，再进入 HGCN 对照。

## Worker Package Summary

- Task ID: `T32`
- Allowed files:
  - new artifacts under `artifacts/baselines/relation_seed_sweeps/`
  - related configs under `project_bootstrap/**/configs`
  - `docs/experiment_reports/gcn_grouped_training.md`
  - `docs/04_task_board.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Forbidden scope:
  - 不改 HGCN 代码
  - 不改变 T31 定义的 grouped training 协议
  - 不覆盖历史 artifact
  - 不改 grouped runner 训练目标，除非只是修复运行参数或配置引用
  - 不把 smoke 结果当作正式 benchmark 结论
- T32-specific notes:
  - 必须使用 T31 reviewed grouped retrieval runner / seed sweep path，不能退回旧 BCE runner。
  - 每个正式 sweep config 必须显式设置 `negative_ratio`，不要依赖 grouped runner 默认值。
  - 如果 `Field.Subfield` 或 `Order.Ring` 缺少可直接运行 config，worker 应先在 Allowed files 内补齐 config，并记录无法运行的具体阻塞。
- Verification:
  - `Get-ChildItem artifacts\baselines\relation_seed_sweeps`
  - `rg -n "mean|std|Recall|MAP|nDCG|grouped|hop|negative_ratio" docs\experiment_reports\gcn_grouped_training.md project_bootstrap\**\configs`

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

## After Completion

Worker 完成后需要 reviewer 只读审查。Captain 根据 review 结果更新：

- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/05_decision_log.md`（如果产生关键决策）
