# 07 Handoff

> 更新时间：2026-05-12
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

`T21`: 对 module-level candidate scan 输出做 data-quality 审计，标出更深、更连续、更适合双曲检验的图。

任务包：

```text
docs/tasks/M2_diagnostics/T21_candidate_scan_audit.md
```

不要跳到训练或论文结论；当前先审计 module-level candidate scan 的数据质量，不直接推进 T30+ 训练任务。

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
26. 当前唯一任务已切换到 `T21`；本轮只推荐下一任务，不执行 T21。

## 8. 下一步

下一轮可把 `T21` 任务包交给 worker 执行。Worker 完成后，把 `T21` diff 交给 reviewer 做只读审查。review 返回后由 Captain：

1. 决定是否将 `T21` 标记为完成，或要求返修。
2. 如果 `T21` 通过 review，再更新 `docs/04_task_board.md`、`docs/07_handoff.md`，必要时更新 `docs/08_risks_and_open_questions.md` 与 `docs/05_decision_log.md`。
3. 只有在 `T21` 闭合后，才在 T22 与其他后续任务之间选择下一任务；不要在同一轮直接执行下一任务。

不要把 `docs/data_manifest.md` 中的 `unknown / needs verification` 字段上升为既成版本事实。
不要把 `docs/data_card.md` 中的 `recommended usage` 误读为最终 benchmark 定稿；这仍然只是当前治理口径下的使用边界，后续还需要 T20+ diagnostics。
不要把 legacy `task = ancestor_ranking` 误读为旧单正例协议仍然有效；在 reviewed grouped protocol freeze 中，它只是 grouped multi-positive ancestor retrieval 的兼容执行键。
