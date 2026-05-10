# 07 Handoff

> 更新时间：2026-05-10
>
> 给下一个 Captain / Worker / Reviewer 的接手说明。

## 1. 当前项目状态

你接手的是“形式化图谱双曲化”项目。当前主线已经从“证明 HGCN 优于 GCN”收束为：

> 构建真实 traced Lean / Mathlib hierarchy 图的可复现实验管线、标准化 grouped retrieval 协议与结构诊断框架，并系统分析双曲归纳偏置在什么结构条件下可能有效。

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

T00: 创建根目录 `README.md`、`AGENTS.md`、`CLAUDE.md`，把项目定位、执行入口和 agent 工作规则写入仓库入口。

任务包：

```text
docs/tasks/M0_governance/T00_root_project_docs.md
```

不要跳到 T10 或代码实现；当前必须先补齐治理入口。

## 4. 当前已知事实

1. 当前没有稳定证据证明 HGCN 在真实 traced Lean hierarchy 图上优于 GCN。
2. 旧单正例 `ancestor_ranking` 协议不合理，默认已升级为 grouped multi-positive ancestor retrieval。
3. 真实 relation layer 往往是浅层、碎片化、叶子占优的 forest / star forest。
4. relation-aware GCN 是当前更强、更稳的 baseline。
5. full Mathlib trace 成本高，不作为当前前置条件。
6. 项目已有 `project_bootstrap/` 原型和 `artifacts/` 诊断/基线产物。

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

- `docs/04_task_board.md`
- `docs/tasks/`
- `docs/review/`

## 6. Worker 执行纪律

Worker 必须：

1. 只做 `Current Unique Task`。
2. 只改任务包的 Allowed files。
3. 不自动领取下一任务。
4. 完成后运行 Verification 或说明不能运行的原因。
5. 最后报告改动、验证和剩余风险。

Reviewer 默认只读。高风险任务使用 adversarial review。

## 7. 本轮 Captain 输出

本轮已经完成：

1. 阅读 `docs/reference/AI_coding_workflow.md` 和 `docs/02_experiment_plan.md`。
2. 创建 `docs/00~08` 治理文档。
3. 建立 `docs/tasks/` 与 `docs/review/` 目录。
4. 将第一个 worker 任务设为 T00。

尚未完成：

1. 根目录 `README.md`、`AGENTS.md`、`CLAUDE.md` 尚未创建。
2. T00 尚未由 worker 执行。
3. 治理初始化尚未经过 reviewer 审查。

## 8. 下一步

把 `docs/tasks/M0_governance/T00_root_project_docs.md` 交给 worker 执行。完成后让 reviewer 只读审查 diff，再由 Captain 标记 T00 状态并选择 T01 或 T10。
