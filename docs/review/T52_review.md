# Review: T52

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

### NB1. T52a `reviewer type` 从 `normal` 升级为 `adversarial`，但 T52 自身任务包仍写 `normal`

T52 任务包（`T52_proof_side_demo_package.md`）第 65 行写 `Reviewer type: normal`，而 T52a 重写后第 158 行写 `adversarial`。这是一个 D032 的设计决策（T52a 涉及 artifact 数据对齐和 provenance narrative 正确性），逻辑上合理。但 T52 自身仍应沿用 `normal`，因为它本身只是写任务包的文档任务。当前没有造成实际混淆，后续 Captain 更新时注意保持一致性即可。

### NB2. T52a artifact path pattern 假设 embedding 子目录命名格式为 `provenance_{model}_{candidate}_{provenance}_t42_seed{seed}`

这个路径模式在 T42 任务执行时确实如此生成，且 T42 已通过 review。但 T52a 任务包没有显式要求 worker 在实现时验证路径是否存在再做 fallback。建议 T52a worker 实现时加入路径存在性检查。此为非阻塞建议，可在 T52a 实现阶段处理。

### NB3. T52a `--declaration-name` 的 example 格式为 hash::Name

T52a 第 61 行给出的示例 `"c211948581bde9846a99e32d97a03f0d5307c31e::Subfield"` 是当前 `declarations.csv` 中的实际格式。但如果后续图数据格式变化，这个硬编码示例可能误导 worker。非阻塞：T52a worker 应在实现时从实际 artifact 中获取可用的 declaration names。

## Missing Tests

T52 是纯文档任务（编写任务包），不涉及代码实现。验证命令（3 条 `rg` 命令）全部通过，覆盖了：
1. T52a 任务包结构关键字段完整性
2. 关键概念覆盖率
3. 治理文档中 T52/T52a 引用一致性

T52a 的 `Verification` 块额外包含 `python -m py_compile` 预检命令，这是给 T52a 实现阶段用的，不属于 T52 本身的验证范围。

## Suspicious Implementation Details

### SD1. T52a `Allowed Files` 列出了 `docs/05_decision_log.md`，但 T52 任务包原始 Allowed Files 未包含此文件

T52 原始任务包 Allowed Files 为：`docs/tasks/M5_paper/T52a_ancestor_explanation_demo.md`、`docs/04_task_board.md`、`docs/05_decision_log.md`、`docs/07_handoff.md`、`docs/08_risks_and_open_questions.md`。Worker 在 T52a 中也列出了 `docs/05_decision_log.md`，这与 T52 自身 Allowed Files 一致（`docs/05_decision_log.md` 是 T52 的 Allowed Files 之一）。确认无越界。

### SD2. T52a `Forbidden Scope` 从旧版 7 条扩展到 11 条

旧版 T52a（diff 中可见删除的部分）有 7 条 forbidden scope。新版扩展到 11 条。新增的 4 条（不修改已有 src 文件、不升级为 benchmark task、不修改 proof_side_mvp.md 和 paper_outline.md、demo 不是 protocol extension）都是合理的收束。这不是 scope creep 而是更精确的边界界定。

### SD3. R32 风险等级为 High Active

`docs/08_risks_and_open_questions.md` 新增了 R32（node ordering alignment 风险），等级为 High Active。这是合理的风险登记：`node_embeddings.npy` 的行顺序与 `declarations.csv` 的节点顺序对齐确实是一个关键正确性风险。T52a 已在 critical implementation note 中写入了 sanity check 要求。

## Checklist Review

1. **Task goal met?** Yes. T52 的目标是把 ancestor explanation MVP 写成可直接派发的下游 worker demo 任务包。T52a 已重写为完整的任务包，包含 Goal、CLI 参数规格、两种运行模式、artifact 依赖表、acceptance criteria verification、11 条 forbidden scope、验证命令、reviewer type。
2. **Stayed within Allowed files?** Yes. Worker 只修改了 5 个文件，全部在 T52 Allowed Files 范围内：`T52a_ancestor_explanation_demo.md`、`04_task_board.md`、`05_decision_log.md`、`07_handoff.md`、`08_risks_and_open_questions.md`。
3. **Avoided Forbidden scope?** Yes. Worker 未实现 demo 代码、未新增实验、未修改已有代码、未引入新依赖、未把计划写成事实。
4. **No mocks/stubs/hardcoded outputs?** N/A — 纯文档任务。
5. **Tests/verification adequate?** Yes. 3 条验证命令全部通过。
6. **No behavioral regressions?** N/A — 未修改代码。
7. **Model/data contracts clear?** T52a 的 artifact 依赖表、CLI 参数规格和输出格式定义清晰且 JSON-serializable。
8. **Safety limits present?** N/A — 不涉及执行。
9. **Docs updated without claiming planned work as complete?** Yes. T52 在 `04_task_board.md` 中仍标记为 `[ ]`（未完成），handoff 中明确写 "Worker 未标记任务完成，等待 reviewer 只读审查"。
10. **Risks documented?** Yes. R32 已新增并登记为 High Active。

## Recommended Next Action

Captain 应：
1. 将 T52 标记完成。
2. 将 D032 从 Pending Review 更新为 Accepted。
3. 当前唯一任务切换为 T52a（ancestor explanation demo 实现），按 T52a 任务包执行。
4. T52a reviewer type 为 adversarial，因为涉及 artifact 数据对齐和 provenance narrative 正确性。
5. T52a 实现时注意 R32 的 sanity check 要求。
