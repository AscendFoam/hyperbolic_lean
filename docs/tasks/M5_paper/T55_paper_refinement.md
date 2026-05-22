# T55 Paper Refinement

## Task ID

T55

## Goal

在 `T54` 已通过 `PASS_WITH_WARNINGS` 的首版正文草稿基础上，对 `docs/paper_draft.md` 做第二轮 paper-facing refinement，使文稿更接近投稿形态，同时不越过当前 reviewed evidence 边界。重点是：

1. 收紧 abstract，降低页数与信息密度风险。
2. 补齐更显式的 Background / Related Work 承接。
3. 让 `synthesized_only` 作为 controlled diagnostic 的表格与文字边界更清楚。
4. 保持 provenance-conditional 口径，不引入任何新实验、新数字或未 review 结论。

## Why Now

`docs/review/T54_review.md` 已将首版 paper draft 判定为 `PASS_WITH_WARNINGS`。这说明文稿主体已经成立，但 reviewer 明确留下了三类 deferred 事项：

- abstract 接近常见投稿上限；
- Background / Related Work 承接不够显式；
- `synthesized_only` 小节的表格呈现可进一步减少读者误读。

在继续做 figure/table 渲染、R28/R29 precision fixes 或 artifact packaging 之前，先把正文结构收紧更稳妥，也更符合 **Narrow** 阶段的 paper-facing 主线。

## Allowed Files

- `docs/paper_draft.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope

- 不新增任何实验、seed sweep、trace、split 生成或新 demo
- 不修改任何 `project_bootstrap/`、`data/`、`artifacts/` 下的代码或产物
- 不重写 `docs/02_experiment_plan.md`
- 不修改 `docs/paper_outline.md`
- 不修改 `docs/experiment_reports/provenance_summary.md`
- 不修改任何 reviewed 数值来源文档
- 不把 `R28`、`R29`、`R30`、`R25` 写成已关闭
- 不把 `hierarchy_mixed` 改写成 HGCN 整体优于 GCN
- 不新增 figure 渲染、图像资产、artifact packaging 内容

## Inputs to Read

- `docs/02_experiment_plan.md`
- `docs/paper_outline.md`
- `docs/paper_draft.md`
- `docs/review/T54_review.md`
- `docs/review/T53_review.md`
- `docs/review/T53_milestone_review.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/experiment_reports/grouped_training_summary.md`
- `docs/experiment_reports/provenance_summary.md`
- `docs/experiment_reports/ancestor_explanation_demo_report.md`

## Expected Output

### 1. Refined Paper Draft

更新：
`docs/paper_draft.md`

至少完成以下 refinement：

1. **Abstract 收紧**
   - 压缩为更接近投稿摘要长度的版本。
   - 保留 C1–C5 的核心信息，但避免过度展开。
   - 保留 single-environment / limited-generalization 边界。

2. **Background / Related Work 承接补齐**
   - 不要求新增独立一级章节。
   - 允许通过 Introduction 内新增小节、Discussion 内承接段落、或其他等价结构实现。
   - 至少要让读者明确看到：
     - Lean/Mathlib hierarchy semantics 的必要背景；
     - hyperbolic graph learning 与 formal-math graph tooling 的相关工作位置；
     - 本文差异化点不是“新模型”，而是 pipeline / protocol / diagnostics / provenance-conditional finding。

3. **Controlled Diagnostic 表述更显式**
   - 在 `synthesized_only` 结果小节中明确说明：
     - Order.Ring 表中有 verified numeric row；
     - Field.Subfield 因 `R28` 精度边界仅保留 prose note；
     - omission 不是为了隐藏反例，而是为了避免把未核清单元写成精确表格事实。

4. **Claim Boundary 保持不变**
   - `explicit_only` 仍是 primary evidence；
   - `synthesized_only` 仍是 controlled diagnostic；
   - `hierarchy_mixed` 仍是 reproducibility check；
   - mixed graph 上 GCN 仍领先；
   - 不关闭 `R28/R29/R30/R25`。

### 2. Governance Sync

同步更新：

- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

最少需要写清：

- `T55` 正在执行的 refinement 目标；
- `T54_review` 中 deferred warnings 的承接关系；
- 当前仍处于 **Narrow** 的 paper-facing 轨道；
- `T55` 之后的候选方向仍是 figure/table rendering、R28/R29 precision fixes、artifact packaging。

## Acceptance Criteria

1. `docs/paper_draft.md` 仍保留 8 个一级章节骨架。
2. 文稿中能明确检索到 `Background` 与 `Related Work` 承接文字或等价小节标题。
3. abstract 比 `T54` 首版更紧凑，且没有丢失 provenance-conditional 主结论与关键边界。
4. `synthesized_only` 小节明确解释为什么 Field.Subfield 不以完整表格行呈现。
5. 治理文档中的 `Current Unique Task`、handoff 与风险状态与 `T55` 一致。
6. 没有新增实验、没有修改实验报告、没有引入未 review 新数字。

## Verification

```powershell
rg -n "## 1\. Title|## 2\. Abstract|## 3\. Introduction|## 4\. Experimental Setup|## 5\. Results|## 6\. Discussion|## 7\. Limitations|## 8\. Conclusion" docs\paper_draft.md
rg -n "Background|Related Work|provenance-conditional|explicit_only|synthesized_only|hierarchy_mixed|R28|R29|R30|R25" docs\paper_draft.md
rg -n "T54|T55|Current Unique Task|Narrow" docs\04_task_board.md docs\05_decision_log.md docs\07_handoff.md docs\08_risks_and_open_questions.md
```

Worker 最后还应在报告中简要说明：

- abstract 主要删减了什么；
- Background / Related Work 放在了哪里；
- 如何确保没有跨越 `R28/R29/R30/R25` 的边界。

## Docs to Update

- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type

adversarial
