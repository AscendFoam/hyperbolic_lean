# T57 Figure/Table Source Rendering

## Task ID

T57

## Goal

在不新增任何实验的前提下，把已经稳定的 reviewed 数值边界转成 publication-facing 的 figure/table source rendering。重点是：

1. 从 `docs/paper_outline.md` 的 figures/tables plan 中抽出当前投稿最关键的 core assets。
2. 新建一个 source-of-truth 文档，集中记录这些 figure/table 的标题、caption、放置位置、数据来源、最终数值和 rendering notes。
3. 同步收紧 `docs/paper_draft.md`、`docs/paper_outline.md` 与 `docs/experiment_reports/provenance_summary.md` 的表格粒度和引用一致性。
4. 吸收 `T56_review` 的 non-blocking notes：
   - `provenance_summary.md` Section 5 summary table 中 FS `synthesized_only` 不再只写 qualitative label，而要与主表粒度保持一致；
   - `paper_draft.md` Section 5.4 的长解释段在不损失事实边界的前提下压缩；
   - 治理文档继续保留 `R28` closure 的可追溯性。

## Why Now

`T56` 已通过 review，`R28`/`R29` 的 precision 风险已经收口。继续延迟 figure/table source rendering 只会让后续 artifact packaging 建立在分散的文稿表格和 appendix 引用上，增加返工成本。

当前最合理的顺序是：

1. 先把稳定下来的数值与图表位组织成统一 source；
2. 再做 artifact packaging；
3. 不回头开新实验。

## Allowed Files

- `docs/paper_draft.md`
- `docs/paper_outline.md`
- `docs/experiment_reports/provenance_summary.md`
- `docs/paper_figures_and_tables.md`
- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope

- 不新增任何实验、seed sweep、trace、split 生成或新 demo
- 不修改任何 `project_bootstrap/`、`data/`、`artifacts/` 下的代码或产物
- 不重写 `docs/02_experiment_plan.md`
- 不引入未 review 的新数值、新图表结论或新 claim
- 不把 mixed graph 改写成 “HGCN 整体优于 GCN”
- 不重新打开 `R28` / `R29`
- 不把 `R25`、`R30` 写成已关闭
- 不做 artifact packaging；该工作留给后续单独任务
- 不生成 PNG/SVG/PDF 等二进制图像资产；本轮只产出 publication-facing source 文档与同步文本

## Inputs to Read

- `docs/02_experiment_plan.md`
- `docs/review/T56_review.md`
- `docs/review/T55_review.md`
- `docs/paper_outline.md`
- `docs/paper_draft.md`
- `docs/experiment_reports/provenance_summary.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Expected Output

### 1. Source-Of-Truth Figure/Table Doc

新建：`docs/paper_figures_and_tables.md`

至少包含以下内容：

1. **Core tables**
   - mixed baseline table
   - provenance-aware comparison table
   - hop-bucket delta table
   - structural-properties table
2. **Core figures**
   - provenance split / structure figure spec
   - hop-depth delta figure spec
3. 每个条目都必须写清：
   - figure/table 编号或临时编号
   - intended placement（对应 paper section）
   - caption
   - exact data source
   - exact numbers or exact qualitative encoding rule
   - rendering notes（例如颜色、坐标轴、是否需要 footnote）

本轮允许使用 Markdown table、编号列表和文字 rendering spec，不要求实际生成二进制图片。

### 2. Paper Draft Sync

更新：`docs/paper_draft.md`

至少完成：

1. 把当前正文中的 core table / figure 引用与 `docs/paper_figures_and_tables.md` 对齐。
2. 压缩 Section 5.4 关于 FS `synthesized_only` GCN = 1.0000 的长解释段，但不能丢失以下事实：
   - `grouped_test_map` 与 `test_average_precision` 是不同指标；
   - 两条指标都正确；
   - `R28` 已由 `T56` 关闭，根因是 metric naming confusion。
3. 保持 provenance-conditional 主结论不变。

### 3. Source Report Sync

更新：`docs/experiment_reports/provenance_summary.md`

至少完成：

1. Section 5 summary table 中 FS `synthesized_only` 不再只写 `GCN wins`，而要与主表粒度统一。
2. 不引入任何新数值；只能使用已经在 T42/T56 reviewed evidence 中稳定下来的数值。

### 4. Outline Sync

更新：`docs/paper_outline.md`

至少完成：

1. Figures and Tables Plan 与当前 `R28/R29` 状态一致，不再把它们写成未解决 precision note。
2. 明确 T57 的 source doc 如何承接 outline 中的图表计划。

### 5. Governance Sync

同步更新：

- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

至少写清：

- `T57` 是当前唯一任务
- `T56` 已通过 review
- `R28/R29` 已关闭/修正
- 当前下一步是 figure/table source rendering，artifact packaging 留待后续

## Acceptance Criteria

1. 新增 `docs/paper_figures_and_tables.md`，且至少包含 4 个 core tables 和 2 个 core figure specs。
2. `paper_draft.md` 中的 core table / figure 引用与 source doc 一致。
3. `provenance_summary.md` Section 5 summary table 的粒度与主表不再明显失配。
4. `paper_outline.md` 不再把 `R28/R29` 写成未解决 precision note。
5. 所有治理入口都反映 `T57` 是当前唯一任务。
6. 没有新增实验、没有修改 artifact、没有引入未 review 新数值。

## Verification

```powershell
rg -n "^## |^### |Figure|Table|caption|source|placement|rendering" docs\paper_figures_and_tables.md docs\paper_draft.md docs\paper_outline.md
rg -n "GCN \\+0\\.3143|1\\.0000 ± 0\\.0000|grouped_test_map|test_average_precision" docs\paper_figures_and_tables.md docs\paper_draft.md docs\experiment_reports\provenance_summary.md docs\paper_outline.md
rg -n "T56|T57|PASS|R28|R29|D20|artifact packaging" docs\00_raw_idea.md docs\01_feasibility_report.md docs\03_architecture.md docs\04_task_board.md docs\05_decision_log.md docs\06_eval_protocol.md docs\07_handoff.md docs\08_risks_and_open_questions.md
```

Worker 最后还应在报告中简要说明：

- 这轮选了哪几个 core figures/tables，为什么
- 如何保证 source doc、paper draft 和 provenance summary 的数值一致
- 如何吸收 `T56_review` 的 non-blocking notes

## Docs to Update

- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type

adversarial
