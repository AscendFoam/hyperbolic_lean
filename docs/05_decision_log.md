# 05 Decision Log

> 更新时间：2026-05-23（T57 review PASS 后更新）
>
> 规则：只记录会影响后续任务选择、论文叙事、评测协议或项目状态的决策。

## D001: 主线从“证明双曲优于欧氏”收束为 benchmark / protocol / diagnostics

- 日期：2026-05-09
- 状态：Accepted
- 依据：`docs/02_experiment_plan.md`、现有 grouped retrieval 与 graph diagnostics 结果。
- 决策：不再把“稳定证明 HGCN 优于 GCN”作为默认目标；项目主线改为真实 traced formal-math hierarchy 图的可复现实验管线、标准化协议和结构诊断。
- 后果：任务板优先安排协议冻结、数据资产化、诊断筛图和训练目标对齐。

## D002: 默认 ancestor 任务口径改为 grouped multi-positive retrieval

- 日期：2026-05-09
- 状态：Accepted
- 依据：`docs/阶段总结（2026-05-01，grouped ancestor retrieval）.md` 与 `docs/02_experiment_plan.md`。
- 决策：旧单正例 `ancestor_ranking` 只保留为历史或辅助口径。正式结果默认使用 grouped `Recall@k`、`MAP`、`nDCG`、`grouped-MRR` 和 hop bucket。
- 后果：后续 worker 不应新增以单正例 MRR 为主指标的正式实验。

## D003: Full Mathlib trace 不作为当前前置条件

- 日期：2026-05-10
- 状态：Accepted
- 依据：`project_bootstrap/small_target_trace_package/README.md` 和历史执行经验。
- 决策：后续优先小仓库完整 trace、已有产物上的模块级子图、Mathlib hierarchy probe。除非 Captain 明确批准，不启动 full Mathlib tracing。
- 后果：降低工程风险，把资源投向更可控的数据快照和协议复验。

## D004: relation provenance split 升级为正式里程碑

- 日期：2026-05-10
- 状态：Accepted
- 依据：`docs/基于深度调研报告的项目定位与创新方向修订.md`、`docs/02_experiment_plan.md`。
- 决策：把 `explicit-only / synthesized-only / mixed` 三类关系图的诊断与 baseline 对照列为 Milestone 4。
- 后果：后续实验要回答 synthesized relation 是否削弱双曲几何最容易利用的层级信号。

## D005: 根目录治理入口作为第一个 worker 任务

- 日期：2026-05-10
- 状态：Accepted
- 依据：`docs/reference/AI_coding_workflow.md` 对 `README.md`、`AGENTS.md`、`CLAUDE.md` 的要求。
- 决策：Current Unique Task 设为 T00，先创建根目录入口文档，再推进协议或代码任务。
- 后果：后续 worker 会话能从仓库入口理解项目边界和任务纪律。

## D006: T00 通过 review 并切换到 T01

- 日期：2026-05-10
- 状态：Accepted
- 依据：`docs/review/T00_review.md`
- 决策：`T00` 判定为 PASS，标记完成；当前唯一任务切换到 `T01`，继续做治理文档一致性复查。
- 后果：后续 worker 可以在 `docs/tasks/M0_governance/T01_governance_consistency_review.md` 上继续推进，不需要回头修 T00。

## D007: 保留 `docs/reference/AI_coding_workflow.md` 中的 reviewer prompt 措辞微调

- 日期：2026-05-10
- 状态：Accepted
- 依据：`docs/review/T00_review.md`、`docs/tasks/M0_governance/T01_governance_consistency_review.md`
- 决策：将 `docs/reference/AI_coding_workflow.md` 中 reviewer prompt 的措辞微调视为正式 workflow 文案更新保留，不在 `T01` 中回滚。
- 后果：相关风险项与 deferred item 不再把这处改动视为待裁决状态；后续治理文档以当前 wording 为准。

## D008: T01 通过 review with warnings accepted

- 日期：2026-05-10
- 状态：Accepted
- 依据：`docs/review/T01_review.md`
- 决策：`T01` 判定为 `PASS_WITH_WARNINGS`。两个 warning 均接受：`README.md` 当前任务入口已更新为 `T10`；`CLAUDE.md` 的 T00 专用 review boundary 已泛化为当前任务通用边界。
- 后果：治理一致性复查完成，当前唯一任务切换到 `T10`。

## D009: T02 暂缓且不阻塞 T10

- 日期：2026-05-10
- 状态：Accepted
- 依据：当前 `docs/review/` 目录仅存在 `T00_review.md` 与 `T01_review.md`，未发现 `T02_review.md`
- 决策：不将 `T02` 标记为完成或已 review；将其暂缓，不作为进入 `T10` 的前置条件。
- 后果：优先推进版本锁定与数据资产 manifest；若后续 review 格式漂移，再回头补 `T02`。

## D010: PM 裁决 T02 当前阶段完成

- 日期：2026-05-10
- 状态：Accepted
- 依据：用户裁决；`docs/review/` 中已有由 Claude Code 编写的 `T00_review.md`、`T01_review.md`、`T10_review.md`
- 决策：虽然没有单独的 `T02_review.md`，但现有 Claude review 文档已经足以满足当前阶段对 review 文档格式与可信度的要求，因此 T02 标记为完成。
- 后果：Milestone 0 治理启动任务全部完成，不阻塞后续数据与协议任务。

## D011: T10 通过 review 并切换到 T11

- 日期：2026-05-10
- 状态：Accepted
- 依据：`docs/review/T10_review.md`
- 决策：`T10` 判定为 PASS，标记完成；当前唯一任务切换到 `T11`。
- 后果：`docs/data_manifest.md` 成为 reviewed manifest；其中 `unknown / needs verification` 字段继续作为后续补证项保留。

## D012: T11 通过 review 并切换到 T12

- 日期：2026-05-10
- 状态：Accepted
- 依据：`docs/review/T11_review.md`
- 决策：`T11` 判定为 PASS，标记完成；当前唯一任务切换到 `T12`。
- 后果：`docs/data_card.md` 成为 reviewed data card；其中的 recommended usage 仍不是最终 benchmark 定稿，provenance schema 边界继续作为 R11 / Open Question 9 跟踪，并由 Milestone 4 正式化。

## D013: T12 通过 adversarial review 并切换到 T13

- 日期：2026-05-11
- 状态：Accepted
- 依据：`docs/review/T12_review.md`
- 决策：`T12` 判定为 PASS，标记完成；当前唯一任务切换到 `T13`。
- 后果：`docs/grouped_retrieval_protocol.md` 成为 reviewed grouped protocol freeze；`task = ancestor_ranking` 继续只是 grouped multi-positive 协议的兼容执行键。hop bucket 常规报告入口仍由 `T13` 收口。

## D014: T13 通过 adversarial review 并切换到 T14

- 日期：2026-05-11
- 状态：Accepted
- 依据：`docs/review/T13_review.md`
- 决策：`T13` 判定为 PASS，标记完成；当前唯一任务切换到 `T14`。
- 后果：hop bucket 常规报告入口已成为 reviewed Milestone 1 协议能力。T13 review 的 helper duplication 与端到端 smoke gap 作为 deferred follow-up 进入风险/开放问题；T14 用窄范围 smoke check 与轻量 cleanup 收口，不执行大规模 sweep。

## D015: T14 通过 review 并切换到 T20

- 日期：2026-05-12
- 状态：Accepted
- 依据：`docs/review/T14_review.md`
- 决策：`T14` 判定为 PASS，标记完成；Milestone 1 数据与协议冻结闭合；当前唯一任务切换到 `T20`。
- 后果：后续 worker 应进入诊断与候选图选择，不再继续补协议字段。`.claude/settings.json` 的自动权限 diff 不纳入 T14 提交；`format_metric` 展示 helper 去重仍由 D05 延后跟踪。

## D016: T20 通过 review with warnings 并切换到 T21

- 日期：2026-05-12
- 状态：Accepted
- 依据：`docs/review/T20_review.md`
- 决策：`T20` 判定为 `PASS_WITH_WARNINGS`，标记完成；当前唯一任务切换到 `T21`。
- Warning 分类：`n/a` 表格项补全为 deferred；单表混合指标来源标注为 deferred；无 rejected warning。
- 后果：`docs/diagnostics_summary.md` 成为 reviewed provisional diagnostics summary。候选优先级可用于安排 T21，但表格精修和指标来源标注在后续文档修订中处理。

## D017: T21 通过 review 并切换到 T22

- 日期：2026-05-12
- 状态：Accepted
- 依据：`docs/review/T21_review.md`
- 决策：`T21` 判定为 PASS，标记完成；当前唯一任务切换到 `T22`。
- Warning 分类：`depth` 列名歧义为 deferred；审计表覆盖范围说明不足为 deferred；mathlib module scan standalone config traceability gap 为 deferred；无 accepted 或 rejected warning。
- 后果：`docs/candidate_graph_audit.md` 成为 reviewed module-level candidate scan audit。`Mathlib.Algebra.Order.Ring` 可作为下一轮默认候选的优先建议，但仍不是最终 benchmark 结论；T22 应把 shallow/star-forest 判断和 positive scale、component ratio、closure expansion 等门控写成 heuristic diagnostics protocol。

## D018: T22 通过 review 并切换到 T30

- 日期：2026-05-13
- 状态：Accepted
- 依据：`docs/review/T22_review.md`
- 决策：`T22` 判定为 PASS，标记完成；Milestone 2 诊断与候选图选择闭合；当前唯一任务切换到 `T30`。
- Warning 分类：shallow forest flag condition 3 对深层但碎片化图的命名可能误导，为 deferred；report template 缺少 `multi-parent count` 行，为 deferred；`ancestor_added_nodes` 缺少内联定义，为 deferred；无 accepted 或 rejected warning。
- 后果：`docs/diagnostics_protocol.md` 成为 reviewed heuristic diagnostics protocol。后续可以进入 training alignment，但必须先做 T30 只读错配审计，不直接修改 loss 或运行 seed sweep。

## D019: T30 通过 review 并插入 T31A split-completeness 前置任务

- 日期：2026-05-13
- 状态：Accepted
- 依据：`docs/review/T30_review.md`
- 决策：`T30` 判定为 PASS，标记完成；不直接进入原 `T31` loss 实现，而是先插入 `T31A` 修复 grouped ancestor retrieval 的 query-level split completeness。
- Warning 分类：Section 4 heading nesting 为 deferred；M6 mixed-language title 为 deferred；M3 rough impact estimate 为 deferred；无 accepted 或 rejected warning。
- 后果：`docs/training_alignment_audit.md` 成为 reviewed training alignment audit。`R19` 被视为 grouped benchmark 前置风险；`T31A` 必须先保证同一 `(src, relation)` query 不跨 split，再由 `T31` 实现 query-grouped loss。

## D020: T31A 通过 adversarial review 并切换到 T31

- 日期：2026-05-13
- 状态：Accepted
- 依据：`docs/review/T31A_review.md`
- 决策：`T31A` 判定为 PASS，标记完成；当前唯一任务切换到 `T31`。
- Warning 分类：`ancestor_label_mode` 与 query key 的交互作为 accepted follow-up note 写入 T31 注意事项；R19 状态更新为 Mitigated；Section numbering 延续 D11 deferred；rare relation type split 覆盖率作为后续 grouped benchmark 注意事项保留。
- 后果：grouped ancestor retrieval 的 split completeness 前置风险已关闭。`T31` 可以专注最小 query-grouped loss，但必须沿用 T31A 已 review 的 `(src_id, relation_type)` query key 语义，尤其注意 `source_kind` label 下的 `extends_ancestor` / `instance_ancestor`。

## D021: T31 通过 adversarial review 并切换到 T32

- 日期：2026-05-16
- 状态：Accepted
- 依据：`docs/review/T31_review.md`
- 决策：`T31` 判定为 PASS，标记完成；当前唯一任务切换到 `T32`。
- Non-blocking 分类：`grouped_loss="infonce"` 作为 `sampled_softmax` 别名为 accepted current behavior；grouped runner `negative_ratio` 默认值差异为 deferred 并写入 T32 明确配置要求；`total_loss` device 初始化清理为 deferred；Captain 级治理文档越界项为 accepted scope distinction；`.claude/settings.json` 自动权限 diff 为 rejected/excluded from commit。
- 后果：T32/T33 可以使用 reviewed grouped retrieval runner 进行同口径 seed sweep，但必须显式设置 `negative_ratio`，且不得退回旧 BCE runner。

## D022: T32 通过 adversarial review 并切换到 T33

- 日期：2026-05-17
- 状态：Accepted
- 依据：`docs/review/T32_review.md`
- 决策：`T32` 判定为 PASS，标记完成；当前唯一任务切换到 `T33`。
- Non-blocking 分类：Section 5 hop bucket 表呈现精简为 accepted presentation choice；`grouped MAP` / `gMAP` 混用为 deferred wording cleanup；无 rejected warning。
- 后果：T32 的 GCN grouped 5-seed baseline 已作为 reviewed 欧氏基线收口。`T33` 可以在相同 split、候选、seed 和参数预算下继续做 HGCN 对照。

## D023: T33 通过 adversarial review 并切换到 T34

- 日期：2026-05-17
- 状态：Accepted
- 依据：`docs/review/T33_review.md`
- 决策：`T33` 判定为 PASS，标记完成；当前唯一任务切换到 `T34`。
- Non-blocking 处理：显式 GCN-vs-HGCN config diff 表与可比性声明记入 `T34` summary 要求；R24 中英混杂问题直接在治理文档中收口为中文；无 blocking issue，无需返工 T33。
- 后果：Milestone 3 的 matched grouped GCN/HGCN 结果已收口。`T34` 作为 summary-only 任务负责补入显式 config diff、跨协议可比性声明，以及 grouped-vs-binary 诊断结论；不新增实验。
## D024: T34 通过 milestone review 并切换到 T40

- 日期：2026-05-17
- 状态：Accepted
- 依据：`docs/review/T34_review.md`
- 决策：`T34` 判定为 PASS，标记完成；当前唯一任务切换到 `T40`。
- Non-blocking 分类：D024 中英混杂问题直接在治理文档中收口为中文 accepted cleanup；Section 5 缺少 Recall 对比列为 deferred；Section 6 历史来源未写具体文件路径为 deferred；`08_risks_and_open_questions.md` 底部英文 draft note 为 accepted cleanup。
- 后果：Milestone 3 的 grouped-vs-binary 总结已收口，项目可进入 Milestone 4 provenance split，但不应把当前结果升级为“已证明 HGCN 整体优于 GCN”。

## D025: Milestone 3 综合审查通过，但保留可复现性警告

- 日期：2026-05-17
- 状态：Accepted
- 依据：`docs/review/M3_review.md`
- 决策：Milestone 3 判定为 `PASS_WITH_WARNINGS`；允许进入 `T40` / Milestone 4。
- Warning 分类：全新干净环境复现未闭合为 deferred；T34 报告 Recall 汇总与历史来源路径精修为 deferred；治理文档中英混杂主问题已由本轮 Captain 直接修正，记为 accepted cleanup。
- 后果：项目主线正式从 grouped training alignment 切换到 provenance split；对外叙事仍应保持“协议已修正、GCN 当前总体领先、双曲优势仍待条件化解释”的窄结论。

## D026: T40 通过 adversarial review 并切换到 T41

- 日期：2026-05-17
- 状态：Accepted
- 依据：`docs/review/T40_review.md`
- 决策：`T40` 判定为 `PASS`，标记完成；当前唯一任务切换到 `T41`。
- Non-blocking 处理：硬编码的预期边数快照记为 accepted frozen-protocol choice，但要求 `T41` 实测校验；`_t40_frozen` 仅是治理标记，记为 accepted；`hierarchy_mixed = full source graph` 只对当前候选图成立，记为 `T41/T42` 必须程序化验证的执行约束；`docs/05_decision_log.md` 的既有脏工作树变更记为非 T40 问题，不影响结论。
- 后果：项目可以从“配置冻结”推进到“实际 split 生成与结构诊断”；在 `T41` 完成前，仍不得把 provenance split 写成已经落盘验证完成的事实。
## D027: T41 通过 adversarial review 并切换到 T42

- 日期：2026-05-17
- 状态：Accepted
- 依据：`docs/review/T41_review.md`
- 决策：`T41` 判定为 `PASS`，标记完成；当前唯一任务切换到 `T42`。
- Non-blocking 处理：`relation_split_summary.json` 单文件覆盖记为 accepted script-output limitation，不回滚、不阻断；`graph_diagnostics_provenance_split_t41.json` 越出 T41 Allowed Files 记为 accepted low-severity packaging gap，并通过细化 `T42` 任务包补齐 tool-side config 边界；`synthesized_only` longest chain = 1 记为 active execution constraint，要求 `T42` 将其仅作为 controlled diagnostic。
- 后果：项目从“split 落盘与结构诊断”推进到“provenance-aware seed sweep”；下一轮只应执行 `T42`，并重点判断 HGCN 是否仅在 `explicit_only` 图上表现出结构性优势。

## D028: T42 通过 adversarial review 并切换到 T43

- 日期：2026-05-18
- 状态：Accepted
- 依据：`docs/review/T42_review.md`
- 决策：`T42` 判定为 `PASS`，标记完成；当前唯一任务切换到 `T43`。
- Non-blocking 处理：Field.Subfield `explicit_only` 的 `hop_4_plus` 均值仅基于 4/5 seeds，记为 accepted precision note，并要求 `T43` 在正式总结中显式注明；`synthesized_only` 中 GCN aggregate 与 per-seed 记录的口径差异记为 deferred follow-up，写入后续 summary/risk 约束，未核清前不得写成“全部 per-seed 均为 1.0”；`.claude/settings.json` 自动权限 diff 继续记为 rejected/excluded from commit；R04 的收口必须按 provenance-conditional 口径书写。
- 后果：项目从”provenance-aware seed sweep”推进到”Milestone 4 叙事收口”。`T43` 只做 summary/governance 收口，不新增实验；其输出将决定项目能否以精确口径进入 Milestone 5。

## D029: T43 通过 milestone review，Milestone 4 闭环并切换到 T50

- 日期：2026-05-18
- 状态：Accepted
- 依据：`docs/review/T43_review.md`、`docs/experiment_reports/provenance_summary.md`、T41/T42 reviewed outputs
- 决策：`T43` 判定为 `PASS`，标记完成；Milestone 4 的正式结论收束为 provenance-conditional：(1) `explicit_only` 是 primary evidence，HGCN 仅在该 split 上稳定领先；(2) `synthesized_only` 是 controlled diagnostic，不支持主模型对比主结论；(3) `hierarchy_mixed` 是 full source graph reproducibility check，而不是新的图族发现；(4) synthesized relation 的作用是结构性稀释，不贡献层级深度；(5) 项目结论从“GCN overall ahead”精化为“GCN 在 mixed graph 上仍领先，HGCN 只在 explicit-only hierarchy 上显现优势”。当前唯一任务切换到 `T50`。
- Non-blocking 分类：Field.Subfield `synthesized_only` 在 `docs/experiment_reports/provenance_summary.md` Section 5.1 的 GCN MAP 表格值错误记为 deferred publication-precision fix，并写入 `R29`；`.claude/settings.json` 自动权限 diff 记为 rejected/excluded from commit；R04 继续保持 `Mitigated` 但明确为 provenance-conditional mitigation，记为 accepted classification judgment。
- 精度边界：Field.Subfield `explicit_only` 的 `hop_4_plus` 均值基于 4/5 seeds（已注明）；`synthesized_only` GCN aggregate 与 per-seed 口径差异继续记为 `R28`；Section 5.1 的错误表格单元继续记为 `R29`，外部发表前必须修正。
- 后果：项目可以从 Milestone 4 推进到 Milestone 5 的论文骨架任务，但后续 paper-facing 文档必须保持 provenance-conditional 口径，并显式绕开 `R28`/`R29` 的未闭环精度问题。

## D030: T50 paper skeleton 保持 provenance-conditional 口径

- 日期：2026-05-18
- 状态：Accepted
- 依据：T50 任务包、T40~T43 reviewed outputs、venue 对照文档
- 决策：`docs/paper_outline.md` 采用 5 条 contributions 结构（pipeline / protocol / diagnostics / provenance-conditional finding / training alignment），venue 优先级为 ITP/CPP > FM > SEFM/ICFEM；proof-side bridge 暂把 ancestor explanation 作为默认候选起点，但最终 MVP 选择仍交由 `T51` 在比较 alternatives 后裁决。
- Non-blocking 分类：`docs/00_raw_idea.md`、`docs/01_feasibility_report.md`、`docs/03_architecture.md`、`docs/06_eval_protocol.md` 的治理状态同步越界编辑记为 accepted low-severity hygiene；worker 修改 `docs/tasks/M5_paper/T50_paper_skeleton.md` 记为 rejected future precedent，不要求返修但不构成后续 worker 的可复用先例；`R30`（贡献数过宽）与 `R31`（ancestor explanation 可能过轻）记为 deferred，并继续保留在风险表中；`.claude/settings.json` 继续 rejected/excluded from commit。
- 后果：`T50` 判定为 `PASS_WITH_WARNINGS` 并标记完成，当前唯一任务切换到 `T51`；paper outline 中的 numeric anchors 在 `R28`/`R29` 关闭前不得直接引用未核清的表格单元。

## D031: T51 选择 ancestor explanation 作为 proof-side MVP

- 日期：2026-05-18
- 状态：Accepted
- 依据：`docs/paper_outline.md` Section 9、T40~T43 reviewed outputs、R31 risk analysis
- 决策：选择 **ancestor explanation** 作为 proof-side utility MVP。比较了三个候选方向：(1) ancestor explanation（低复杂度，直接映射 C2/C4，零新依赖）；(2) relation-aware declaration recommendation（中复杂度，需要新任务定义）；(3) premise retrieval demo（高复杂度，需要 LeanDojo 桥接，违反 forbidden scope）。选择 ancestor explanation 的核心理由是它把 provenance-conditional finding 从表格数字变成用户可体验的 hierarchy navigation 质量差异，且与 ITP/CPP venue fit 高度对齐。
- R31 回应：ancestor explanation 不是"列出祖先"，而是 provenance-aware quality comparison tool——用户可直观看到同一 declaration 在 `explicit_only` vs `hierarchy_mixed` 上的 retrieval 质量差异和 hop-depth-dependent gradient。这满足 CPP tool demo 的 "artifact is functional and solves a real problem" 标准。
- 后果：`T52` 应基于此选择编写 ancestor explanation 的最小 demo 任务包，包括 CLI 入口、model artifact loading、provenance comparison mode 输出格式和验收命令。不引入新依赖、不重新训练模型、不修改已有 protocol。

## D032: T52 ancestor explanation demo 任务包设计决策

- 日期：2026-05-18
- 状态：Accepted
- 依据：`docs/proof_side_mvp.md`、`docs/paper_outline.md`、T42 reviewed artifacts 结构
- 决策：`T52_review` 判定为 `PASS`，`T52` 正式完成。`T52a` 任务包作为唯一下一任务被接受并冻结以下设计决策：(1) **artifact loading 策略**：直接加载 T42 provenance sweep 的 `node_embeddings.npy`，不重新 inference 或加载 checkpoint；(2) **代码入口**：新建独立脚本 `proof_side_ancestor_explanation.py`，不修改已有 runner；(3) **node ordering 对齐**：必须复用 `common.load_declaration_graph()` 的节点顺序，否则 embedding 行号会错位；(4) **comparison mode 为硬边界**：`explicit_vs_mixed` comparison mode 不是可选增强项而是验收条件的一部分；(5) **reviewer type 为 adversarial**：因为涉及 artifact 数据对齐和 provenance narrative 正确性；(6) **artifact path pattern 必须精确**：使用 `provenance_{model}_{candidate}_{provenance}_t42/provenance_{model}_{candidate}_{provenance}_t42_seed{seed}`；(7) **declaration-name 必须精确匹配**：按 `declarations.csv` 中的完整字符串匹配，不做模糊匹配。
- 后果：当前唯一任务切换为 `T52a`。后续 worker 按该任务包实现 demo，不引入新依赖、不重新训练、不修改已有代码；实现完成后进入 adversarial review。

## D033: T52a ancestor explanation demo 实现决策

- 日期：2026-05-19
- 状态：Accepted
- 依据：`docs/review/T52a_review.md`、T52a 任务包、T42 reviewed artifacts
- 决策：Captain 根据 `docs/review/T52a_review.md` 将 `T52a` 判定为 `PASS`。review 没有 blocking issues，只给出非阻塞的可选改进与 missing-tests 提醒，不要求 worker 返修。因此 `T52a` 正式标记完成，并将当前唯一任务切换到 `T53` milestone review。`T53` 只负责基于已 reviewed 的 protocol / benchmark / provenance / proof-side evidence 做阶段性裁决，不新增实验或代码开发。
- 后果：Milestone 5 当前状态从”proof-side demo 实现”推进到”milestone review 收口”。后续 worker 只应执行 `docs/tasks/M5_paper/T53_milestone_review.md`；git 提交仍需排除 `.claude/settings.json`。

## D034: T53 milestone review 裁决 Narrow

- 日期：2026-05-20
- 状态：Accepted
- 依据：`docs/review/T53_milestone_review.md`、M1–M5 全部 reviewed evidence、`docs/08_risks_and_open_questions.md` 当前风险状态
- 决策：T53 worker 已完成 milestone review，verdict 为 **Narrow**。核心理由：(1) 五个 Milestone 的 reviewed 证据链已闭合（24 个 task 通过 review，其中 11 个 adversarial review）；(2) 核心 provenance-conditional finding 已由 T42 的 60 次训练确立，经 T43 收口、T50 保持、T52a demo 验证；(3) proof-side bridge 已从 paper story 变成可运行 CLI demo 并通过 adversarial review；(4) 当前不需要新实验、新模型、新数据源或新 demo；(5) 最紧迫的工作是把已有证据整理成可投稿论文和 artifact package。活跃风险（R01/R03/R10/R25/R28/R29/R30）是 paper-facing 收窄工作中的待处理项。
- 后果：项目应从”继续开发实验“收窄为”paper-facing / packaging / cleanup“。下一任务形态应为 paper drafting、figure/table rendering、precision fixes (R28/R29)、artifact packaging。不跑新实验、不扩展 demo、不修改已冻结的 protocol 语义、不引入新模型或新依赖。

## D035: T53 review 通过并切换到 T54 paper draft

- 日期：2026-05-20
- 状态：Accepted
- 依据：`docs/review/T53_review.md`、`docs/review/T53_milestone_review.md`
- 决策：Captain 根据 `docs/review/T53_review.md` 将 `T53` 判定为 `PASS`。review 没有 blocking issues，也没有需要返工的 `PASS_WITH_WARNINGS` 分类项；仅指出了若干 captain 侧治理同步问题。Captain 已同步修正治理文档，并将当前唯一任务切换为 `T54`，目标是基于 `docs/paper_outline.md` 与全部 reviewed evidence 产出 paper-facing draft 首版。
- 后果：Milestone 5 正式收口，worker 可以继续推进下一任务，但只能执行 `T54`。git 可以提交当前 captain 同步结果与 reviewer 文档；提交时继续排除 `.claude/settings.json`。`T54` 之后再分拆 figure/table rendering、R28/R29 precision fixes 与 artifact packaging，保持单任务推进。

## D036: T54 paper draft 首版产出

- 日期：2026-05-20
- 状态：Accepted
- 依据：T54 任务包、`docs/paper_outline.md`、T32–T43/T50–T53 全部 reviewed evidence
- 决策：T54 worker 已产出 `docs/paper_draft.md` 首版，包含 8 个一级章节（Title, Abstract, Introduction, Experimental Setup, Results, Discussion, Limitations, Conclusion）和附录（Evidence Chain + Numeric Anchors）。草稿严格保持 provenance-conditional 口径：(1) `explicit_only` 是 primary evidence；(2) `synthesized_only` 是 controlled diagnostic；(3) `hierarchy_mixed` 是 reproducibility check，mixed graph 上 GCN 仍领先。草稿显式保留 R28（synthesized_only aggregate/per-seed 口径差异）、R29（provenance_summary.md 表格错误）、R30（contributions 过宽）、R25（clean-environment reproducibility 未闭合）的精度边界，未将任何活跃风险写成已关闭。所有数值来自 reviewed T32/T33/T42/T43 artifacts，未引入未 review 的新数字。
- 后果：`docs/paper_draft.md` 首版被接受为 Narrow 阶段的正式 paper-facing 基线文稿，可继续进入第二轮 paper refinement，而不需要回头重开实验链路。

## D037: T54 review 通过并切换到 T55 paper refinement

- 日期：2026-05-20
- 状态：Accepted
- 依据：`docs/review/T54_review.md`
- 决策：Captain 根据 `docs/review/T54_review.md` 将 `T54` 判定为 `PASS_WITH_WARNINGS`。warning 分类如下：(1) Allowed Files 范围外的治理同步编辑为 deferred governance-scope risk，写回 `R08`；(2) Section 5.4 中 `synthesized_only` 表格仅列 Order.Ring、Field.Subfield 仅以 prose note 说明，为 accepted presentation choice；(3) abstract 接近页数预算上界，为 deferred，并并入 `R30`；(4) 缺少 Related Work section，为 deferred；(5) 缺少 Background section，为 deferred；后两者并入新的 paper-structure risk `R33`。无 blocking issue，无 rejected warning。
- 后果：`T54` 正式标记完成，当前唯一任务切换为 `T55`。`T55` 只负责对 `docs/paper_draft.md` 做第二轮 refinement：压缩摘要、补齐 Background / Related Work 承接、让受控诊断表述更显式，同时保持 provenance-conditional 边界。不新增实验、不修改 experiment reports。当前治理状态允许 git 提交，并允许 worker 继续推进，但仅能执行 `docs/tasks/M5_paper/T55_paper_refinement.md`；提交时继续排除 `.claude/settings.json`。

## D038: T55 paper refinement 第二轮

- 日期：2026-05-20
- 状态：Accepted
- 依据：T55 任务包、`docs/review/T54_review.md` deferred warnings、`docs/paper_draft.md` T54 首版
- 决策：T55 worker 已完成第二轮 paper refinement，主要变更：(1) abstract 从 ~180 词压缩至 ~140 词，保留 C1-C5 核心信息与 provenance-conditional 主结论；(2) Introduction 新增 Section 3.2 Background 小节（Lean/Mathlib hierarchy semantics、hyperbolic GNN 理论动机、formal-math graph tooling 定位）；(3) Discussion 新增 Section 6.5 Related Work and Positioning 小节（hyperbolic embeddings 文献、formal-math graph 数据集与工具、proof assistant hierarchy navigation、本文差异化点）；(4) Section 5.4 `synthesized_only` 表格新增 Field.Subfield 占位行（`*see note below*`），并新增解释段说明省略原因（R28 精度边界），明确这不是为了隐藏反例；(5) Section 5.7 summary table 标注脚注引用 Section 5.4。所有 provenance-conditional 口径、R28/R29/R30/R25 精度边界和 8 个一级章节骨架保持不变。
- 后果：`docs/paper_draft.md` 已进入第二轮 refinement 状态，等待 reviewer 只读审查。T55 未新增实验、未修改 experiment reports、未修改 forbidden scope 文件。

## D039: T55 review 通过并切换到 T56 precision cleanup

- 日期：2026-05-22
- 状态：Accepted
- 依据：`docs/review/T55_review.md`
- 决策：`T55` 判定为 `PASS_WITH_WARNINGS`。warning 分类如下：(1) Allowed Files 越界同步模式为 deferred governance-risk，已写回 `R08`；(2) Background / Related Work 以子节承接为 accepted presentation choice；(3) abstract 压缩为 accepted；(4) `D19` 关闭为 accepted。
- 后果：`T55` 正式标记完成，当前唯一任务切换到 `T56`。`T56` 不新增实验，而是优先清理 `R28/R29` 的 publication-facing precision 问题，并为后续 figure/table rendering 与 artifact packaging 建立可引用、可核对的数值边界。提交时继续排除 `.claude/settings.json`。

## D040: T56 precision cleanup 完成 R28 关闭与 R29 修正

- 日期：2026-05-22
- 状态：Accepted
- 依据：T42 artifact 审计 (`provenance_gcn_field_subfield_synthesized_only_t42/` 的 aggregate.json、per_seed_results.json、per_seed_results.csv)
- 决策：
  1. `R29` 修正：`provenance_summary.md` Section 5.1 表格中 FS GCN synthesized_only MAP 从 HGCN copy-paste 值 `0.6857 ± 0.1140` 修正为 verified T42 value `1.0000 ± 0.0000`，delta 修正为 `GCN +0.3143`。
  2. `R28` 解析并关闭：原始 T43 报告中描述的 "aggregate vs per-seed discrepancy" 经重新审计确认是 metric naming confusion——被引用为 "per-seed MAP" 的 0.8100/0.9029 实为 `test_average_precision`（sklearn per-query metric），而非 `grouped_test_map`（grouped retrieval MAP across all queries）。`grouped_test_map` = 1.0 for all 5 seeds in aggregate.json、per_seed_results.json 和 per_seed_results.csv。`test_average_precision` aggregate (0.9426) 也正确反映 per-seed 值 (1.0, 1.0, 0.81, 0.9029, 1.0)。两条指标均计算正确、内部一致，不存在数据管线 bug。
- 后果：`provenance_summary.md` 和 `paper_draft.md` 均已同步更新 precision 信息；`R28`/`R29` 在 `docs/08_risks_and_open_questions.md` 中从 Active 更新为 Resolved；`D18` 关闭。`docs/review/T56_review.md` 已确认这次关闭满足 `T56` 任务包中“仅基于现有 reviewed artifact 严格解释根因时才可关闭 R28”的例外条件。所有修改均基于已有 reviewed T42 artifact，未引入新实验或未 review 数值。

## D041: T56 review 通过并切换到 T57 figure/table source rendering

- 日期：2026-05-22
- 状态：Accepted
- 依据：`docs/review/T56_review.md`
- 决策：`T56` 判定为 `PASS`。review 没有 blocking issue，也没有需要分类为 accepted/deferred/rejected 的 warning。reviewer 留下的三个 non-blocking notes 直接并入下一轮任务设计：`provenance_summary.md` Section 5 summary table 的粒度统一、`paper_draft.md` Section 5.4 长解释段的最终压缩、以及 `R28` closure 条件在治理文档中的显式可追溯性。
- 后果：`T56` 正式标记完成，当前唯一任务切换到 `T57`。`T57` 负责把已经稳定的 reviewed 数值边界转成 publication-facing 的 figure/table source rendering，并吸收上述非阻塞表达精修；`artifact packaging` 保持为后续单独任务。提交时继续排除 `.claude/settings.json`。

## D042: T57 figure/table source rendering 完成

- 日期：2026-05-23
- 状态：Accepted
- 依据：T56 reviewed artifacts、`docs/paper_outline.md` Section 6 figures/tables plan、`docs/paper_draft.md`、`docs/experiment_reports/provenance_summary.md`
- 决策：T57 worker 已完成 figure/table source rendering。核心产出：
  1. 新建 `docs/paper_figures_and_tables.md` 作为 publication-facing 图表源文档，包含 4 个 core tables（mixed baseline、provenance-aware comparison、hop-bucket delta、structural properties）、2 个 core figure specs（provenance split/structure、hop-depth delta）和 1 个 summary table。
  2. 压缩 `paper_draft.md` Section 5.4 长解释段（~120 词 → ~60 词），保留三要素事实：`grouped_test_map` 与 `test_average_precision` 是不同指标、两条指标均正确、R28 已由 T56 关闭。
  3. 统一 `provenance_summary.md` Section 5 summary table 中 FS synthesized_only 的粒度（从 "GCN wins" 改为 "GCN wins (+0.3143 MAP)"）。
  4. 更新 `paper_outline.md` 中 R28/R29 状态从 active 改为 resolved。
  Worker 未新增实验、未修改 artifact、未引入未 review 新数值。
- 后果：`docs/paper_figures_and_tables.md` 已成为 publication-facing 图表 source-of-truth；后续 artifact packaging 保持为单独任务。

## D043: T57 review 通过并切换到 T58 artifact packaging

- 日期：2026-05-23
- 状态：Accepted
- 依据：`docs/review/T57_review.md`
- 决策：`T57` 判定为 `PASS`。review 无 blocking issues，也无 `PASS_WITH_WARNINGS` 分类项。三个 non-blocking notes 的处理为：(1) `docs/paper_figures_and_tables.md` Section 4 中 stale “Pending sync” rows 不回头重开 `T57`，而是并入 `T58` artifact packaging 顺手修正；(2) `paper_draft.md` Section 5.4 压缩后少掉的一句 mechanistic detail 作为最终 paper-editing 取舍项，亦并入 `T58`；(3) `.claude/settings.json` 自动权限变更继续 rejected/excluded from commit。
- 后果：`T57` 正式标记完成，当前唯一任务切换到 `T58`。下一轮只做 artifact packaging 与 source-to-claim 对照整理，不新增实验、不修改 artifacts。
