# 04 Task Board

> 更新时间：2026-05-10
>
> Captain 原则：每轮只推进一个 `Current Unique Task`。Worker 不自动领取下一任务。

## Project Status

- 状态：Continue
- 当前阶段：治理入口已完成，等待 T01 一致性复查
- 当前主线：`benchmark / protocol / diagnostics`
- 当前不主张：把“已经证明 HGCN 稳定优于 GCN”写成既成事实
- 当前证据等级：已有真实实验与工程原型，但尚未冻结成正式 benchmark artifact

## Milestone 0: Governance Bootstrap

- [x] T00: 创建根目录 `README.md`、`AGENTS.md`、`CLAUDE.md`，把项目定位、执行入口和 agent 规则写入仓库入口
- [ ] T01: 审查并校正 `docs/00~08` 与 `docs/tasks` 的一致性，确保任务包可以直接交给 worker
- [ ] T02: 建立 `docs/review/` 的 review 模板，并记录治理初始化 review

## Milestone 1: Data And Protocol Freeze

- [ ] T10: 生成版本锁定与数据资产 manifest，覆盖 Lean、Mathlib、LeanDojo、Python 依赖、关键 config 与现有 artifact
- [ ] T11: 写出 data card，描述当前可用图、字段、relation provenance、coverage-aware 处理与 unresolved 语义
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

`T01`: 审查并校正 `docs/00~08` 与 `docs/tasks` 的一致性，确保任务包可以直接交给 worker。

任务包位置：

`docs/tasks/M0_governance/T01_governance_consistency_review.md`

## Why Now

`T00` 已经经过 review 并完成收口，但治理文档之间还需要再做一轮一致性复查。当前最值得做的是确认 `docs/00~08`、`docs/tasks`、根目录入口与 review 流程完全对齐，然后再进入数据与协议冻结。

## Worker Package Summary

- Task ID: `T01`
- Allowed files:
  - `docs/00_raw_idea.md`
  - `docs/01_feasibility_report.md`
  - `docs/03_architecture.md`
  - `docs/04_task_board.md`
  - `docs/05_decision_log.md`
  - `docs/06_eval_protocol.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
  - `docs/reference/AI_coding_workflow.md`
  - `docs/tasks/**`
  - `README.md`
  - `AGENTS.md`
  - `CLAUDE.md`
- Forbidden scope:
  - 不修改 `docs/02_experiment_plan.md`
  - 不修改任何 `project_bootstrap/` 下的代码或配置
  - 不运行 tracing、训练、seed sweep 等长任务
  - 不把双曲优于欧氏写成已完成事实
- Verification:
  - `rg -n "Current Unique Task|T01|PASS|PASS_WITH_WARNINGS|BLOCK" docs/04_task_board.md docs/07_handoff.md docs/00_raw_idea.md docs/01_feasibility_report.md docs/03_architecture.md docs/05_decision_log.md docs/06_eval_protocol.md docs/08_risks_and_open_questions.md docs/reference/AI_coding_workflow.md README.md AGENTS.md CLAUDE.md`
  - 人工检查 T01 包是否只做文档一致性复查，不碰代码和实验配置

## Execution Note

- 2026-05-10：`T00` 已通过 review，根目录入口文档与相关 handoff 文档已收口。
- 2026-05-10：当前唯一任务切换为 `T01`，用于复查治理文档之间的一致性。

## After Completion

Worker 完成后需要 reviewer 只读审查。Captain 根据 review 结果更新：

- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/05_decision_log.md`（如果产生关键决策）
