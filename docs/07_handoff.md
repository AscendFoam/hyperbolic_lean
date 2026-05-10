# 07 Handoff

> 更新时间：2026-05-10
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

`T12`: 固化 grouped multi-positive ancestor retrieval 协议，确认代码入口、配置字段、指标名与输出格式。

任务包：

```text
docs/tasks/M1_protocol/T12_grouped_protocol_freeze.md
```

不要跳到训练或论文结论；当前必须先把 grouped retrieval 协议与代码入口、配置字段、指标名和输出格式对齐。

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

## 8. 下一步

下一轮应把 `T12` 任务包交给 worker 执行。Worker 完成后，把 `T12` diff 交给 reviewer 做只读审查。完成后由 Captain：

1. 决定是否将 `T12` 标记为完成。
2. 更新 `docs/04_task_board.md`、`docs/07_handoff.md`，必要时更新 `docs/08_risks_and_open_questions.md` 与 `docs/05_decision_log.md`。
3. 在 `T13` 与后续诊断任务之间选择下一任务，但不要在同一轮直接执行下一任务。

不要把 `docs/data_manifest.md` 中的 `unknown / needs verification` 字段上升为既成版本事实。
不要把 `docs/data_card.md` 中的 `recommended usage` 误读为最终 benchmark 定稿；这仍然只是当前治理口径下的使用边界，后续还需要 `T12` / `T13` protocol 和 reviewer 收口。
