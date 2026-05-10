# 04 Task Board

> 更新时间：2026-05-10
>
> Captain 原则：每轮只推进一个 `Current Unique Task`。Worker 不自动领取下一任务。

## Project Status

- 状态：Continue
- 当前阶段：治理入口、review 模板需求、版本 manifest 与 data card 已收口；当前推进 T12 协议冻结
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
- [ ] T12: 固化 grouped multi-positive ancestor retrieval 协议，确认代码入口、配置字段、指标名与输出格式
- [ ] T13: 增加或校验 hop bucket 常规报告入口，确保 `hop_2 / hop_3 / hop_4_plus` 出现在正式结果中

## Milestone 2: Diagnostics And Candidate Graph Selection

- [ ] T20: 复查 `real_graphs_v1`、`hierarchy_focus_v1`、`mathlib_order_focus_v1` 诊断产物，形成候选图优先级表
- [ ] T21: 对 module-level candidate scan 输出做 data-quality 审计，标出更深、更连续、更适合双曲检验的图
- [ ] T22: 为 shallow forest / star forest 判断写出可复用诊断阈值与报告模板

## Milestone 3: Grouped Retrieval Training Alignment

- [ ] T30: 阅读现有 grouped retrieval training 代码，定位 binary edge classification 与 grouped retrieval 的错配点
- [ ] T31: 实现最小 query-grouped loss 方案，优先 `sampled softmax` 或 `InfoNCE`，只接一个现有 config
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

`T12`: 固化 grouped multi-positive ancestor retrieval 协议，确认代码入口、配置字段、指标名与输出格式。

任务包位置：

`docs/tasks/M1_protocol/T12_grouped_protocol_freeze.md`

## Why Now

`T11` 已经通过 review，`docs/data_manifest.md` 与 `docs/data_card.md` 已成为当前数据资产入口。下一步必须把 grouped retrieval 协议与代码入口、配置字段、指标名和输出格式对齐，避免后续 worker 在未冻结协议上直接推进训练或论文结论。

## Worker Package Summary

- Task ID: `T12`
- Allowed files:
  - `docs/06_eval_protocol.md`
  - `docs/grouped_retrieval_protocol.md`
  - relevant config files under `project_bootstrap/**/configs`
  - relevant evaluation/reporting code under `project_bootstrap/baseline_scaffold/src`
  - `docs/04_task_board.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Forbidden scope:
  - 不大改模型架构
  - 不新增 unrelated task
  - 不删除旧结果
- Verification:
  - `rg -n "grouped|Recall@|MAP|nDCG|MRR|hop" project_bootstrap\baseline_scaffold\src docs\06_eval_protocol.md docs\grouped_retrieval_protocol.md`

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

## After Completion

Worker 完成后需要 reviewer 只读审查。Captain 根据 review 结果更新：

- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/05_decision_log.md`（如果产生关键决策）
