# 04 Task Board

> 更新时间：2026-05-10
>
> Captain 原则：每轮只推进 `Current Unique Task`。Worker 不自动领取下一任务。

## Project Status

- 状态：Continue
- 当前阶段：治理初始化完成，等待第一个 worker 实现任务。
- 当前主线：benchmark / protocol / diagnostics，而不是证明 HGCN 必然优于 GCN。
- 当前证据等级：工程原型与真实实验结果已有，尚未形成冻结版 benchmark artifact。

## Milestone 0: Governance Bootstrap

- [ ] T00: 创建根目录 `README.md`、`AGENTS.md`、`CLAUDE.md`，把 Captain / Worker / Reviewer 规则写入仓库入口。
- [ ] T01: 审查并校正 `docs/00~08` 与 `docs/tasks` 的一致性，确保任务包可直接交给 worker。
- [ ] T02: 建立 `docs/review/` 的 review 文件模板，并记录治理初始化 review。

## Milestone 1: Data and Protocol Freeze

- [ ] T10: 生成版本锁定与数据资产 manifest，覆盖 Lean、Mathlib、LeanDojo、Python 依赖、关键 config 和已有 artifact。
- [ ] T11: 写出 data card，描述当前可用图、字段、relation provenance、coverage-aware 处理和 unresolved 语义。
- [ ] T12: 固化 grouped multi-positive ancestor retrieval 协议，确认代码入口、配置字段、指标名和输出格式。
- [ ] T13: 增加或校验 hop bucket 常规报告入口，确保 `hop_2 / hop_3 / hop_4_plus` 出现在正式结果中。

## Milestone 2: Diagnostics and Candidate Graph Selection

- [ ] T20: 复查现有 `real_graphs_v1`、`hierarchy_focus_v1`、`mathlib_order_focus_v1` 诊断产物，形成候选图优先级表。
- [ ] T21: 对 module-level candidate scan 输出做 data-quality 审计，标出更深、更连续、更适合双曲检验的图。
- [ ] T22: 为浅层 forest / star forest 判断写出可复用诊断阈值和报告模板。

## Milestone 3: Grouped Retrieval Training Alignment

- [ ] T30: 读取现有 grouped retrieval training 代码，定位 binary edge classification 与 grouped retrieval 的错配点。
- [ ] T31: 实现最小 query-grouped loss 方案，优先 `sampled softmax` 或 `InfoNCE`，只接一个现有 config。
- [ ] T32: 在 `Field.Subfield` 与 `Order.Ring` 上跑 GCN 5-seed grouped training 对照。
- [ ] T33: 在相同 split 和参数预算下跑 HGCN 5-seed grouped training 对照。
- [ ] T34: 汇总 grouped training 与旧 binary training 的差异，写入诊断报告。

## Milestone 4: Relation Provenance Split

- [ ] T40: 冻结 `explicit-only / synthesized-only / mixed` 三类图的生成配置和输出位置。
- [ ] T41: 对三类 provenance 图运行结构诊断，比较深度、叶子比例、连通性和 hyperbolicity proxy。
- [ ] T42: 对三类 provenance 图运行 grouped retrieval / parent prediction 的 GCN 与 HGCN seed sweep。
- [ ] T43: 汇总 provenance split 结果，回答 synthesized relation 是否削弱双曲优势。

## Milestone 5: Paper and Proof-Side Bridge

- [ ] T50: 整理论文贡献骨架，围绕 pipeline / protocol / diagnostics / conditional hyperbolic conclusion。
- [ ] T51: 选择一个 proof-side utility MVP，例如 ancestor explanation 或 relation-aware declaration recommendation。
- [ ] T52: 为 proof-side utility 写最小 demo 任务包，不承诺端到端 theorem proving。
- [ ] T53: 完成里程碑审查，判断项目进入 Continue / Narrow / Resume-ready。

## Current Unique Task

T00: 创建根目录 `README.md`、`AGENTS.md`、`CLAUDE.md`，把项目定位、执行入口和 agent 工作规则写入仓库入口。

任务包位置：`docs/tasks/M0_governance/T00_root_project_docs.md`

## Why Now

`docs/00~08` 已经建立为主状态，但 workflow 要求最小启动至少具备 `README.md` 和 `AGENTS.md`。当前根目录缺少这些入口，后续 worker 如果直接开工，容易不知道项目边界、当前唯一任务和 review 规则。

## Worker Package Summary

- Task ID: T00
- Allowed files:
  - `README.md`
  - `AGENTS.md`
  - `CLAUDE.md`
  - `docs/04_task_board.md`
  - `docs/07_handoff.md`
- Forbidden scope:
  - 不修改 `docs/02_experiment_plan.md`
  - 不改任何 `project_bootstrap/` 代码
  - 不运行长时间 tracing 或训练
  - 不把双曲优于欧氏写成已完成事实
- Verification:
  - `git diff -- README.md AGENTS.md CLAUDE.md docs/04_task_board.md docs/07_handoff.md`
  - 人工检查三份根目录文档是否包含项目定位、入口文件、agent 规则和当前任务流程。

## After Completion

Worker 完成后需要 reviewer 只读审查。Captain 根据 review 结果更新：

- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/05_decision_log.md`（如果产生关键决策）
