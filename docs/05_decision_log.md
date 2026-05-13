# 05 Decision Log

> 更新时间：2026-05-13
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
