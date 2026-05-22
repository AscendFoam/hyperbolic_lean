# T56 Publication-Facing Precision Cleanup

## Task ID

T56

## Goal

在不新增任何实验的前提下，核对并清理 `R28/R29` 对外文稿引用链中的 publication-facing precision 问题。重点是：

1. 审计 `docs/experiment_reports/provenance_summary.md` 与 reviewed T42/T43 artifact 叙述是否一致。
2. 修正已经确认属于文稿层 copy-paste / 引用错误的内容，尤其是 `R29`。
3. 对 `R28` 给出更严格的状态判断：
   - 如果能仅凭现有 reviewed artifact 解释清楚 aggregate/per-seed 差异，就明确收口；
   - 如果不能，就把不可关闭的边界写得更清楚，而不是模糊带过。
4. 把精度状态同步到 `docs/paper_draft.md` 与治理入口，保证后续 figure/table rendering 与 artifact packaging 站在一致的数字边界上。

## Why Now

`docs/review/T55_review.md` 已将 paper draft 的结构性 refinement 判定为 `PASS_WITH_WARNINGS`。当前最紧迫的剩余工作不再是扩写正文，而是收口 `R28/R29` 这类会直接影响对外引用、表格渲染与 artifact package 可信度的 precision 风险。

如果继续跳过这一步直接做 figure/table rendering，后续图表和摘要就会建立在不稳定的数值引用边界上，返工成本更高。

## Allowed Files

- `docs/experiment_reports/provenance_summary.md`
- `docs/paper_draft.md`
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
- 不修改 `docs/paper_outline.md`
- 不引入未 review 的新数值、新图表或新结论
- 不把 mixed graph 改写成 “HGCN 整体优于 GCN”
- 不关闭 `R25`、`R30`
- 不关闭 `R28`，除非只基于现有 reviewed artifact 能严格解释 aggregate/per-seed 差异根因
- 不新增 figure 渲染、图片资产或 artifact packaging 内容

## Inputs to Read

- `docs/02_experiment_plan.md`
- `docs/review/T43_review.md`
- `docs/review/T54_review.md`
- `docs/review/T55_review.md`
- `docs/experiment_reports/provenance_summary.md`
- `docs/paper_draft.md`
- `docs/paper_outline.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- reviewed T42/T43 artifact paths cited inside `docs/experiment_reports/provenance_summary.md`

## Expected Output

### 1. Precision-Cleaned Source Report

更新 `docs/experiment_reports/provenance_summary.md`，至少完成：

1. 明确检查并修正 `R29` 对应的错误表格单元或等价文稿引用。
2. 对 `R28` 给出更精确的说明：
   - 明确 aggregate 与 per-seed 差异出现在哪些字段；
   - 明确这是否影响主结论；
   - 若仍无法关闭，写清为什么当前只能保留为开放 precision risk。
3. 不新增任何未 review 的数值，只允许把已有 reviewed artifact 的数值和边界写得更准确。

### 2. Paper-Facing Sync

更新 `docs/paper_draft.md`，确保：

1. 文中不再隐式依赖 `R29` 对应的错误单元。
2. `R28/R29` 的精度边界与 source report 一致。
3. provenance-conditional 主结论保持不变。

### 3. Governance Sync

同步更新以下治理文档：

- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

至少写清：

- `T56` 正在处理的是 `R28/R29` 的 publication-facing precision cleanup
- `R28` 是否关闭、降级或继续保留
- `R29` 是否已修正
- 后续下一任务仍应是 figure/table rendering 或 artifact packaging，而不是新实验

## Acceptance Criteria

1. `docs/experiment_reports/provenance_summary.md` 中与 `R29` 对应的错误单元不再以错误形式出现。
2. `R28` 的当前状态比进入 `T56` 前更明确，不能只是重复旧描述。
3. `docs/paper_draft.md` 与 `docs/experiment_reports/provenance_summary.md` 对 `R28/R29` 的说法一致。
4. 所有治理入口都反映 `T56` 是当前唯一任务。
5. 没有新增实验、没有修改 artifact、没有引入未 review 新数值。

## Verification

```powershell
rg -n "Field\\.Subfield|synthesized_only|MAP|aggregate|per_seed|R28|R29" docs\experiment_reports\provenance_summary.md docs\paper_draft.md
rg -n "T55|T56|PASS_WITH_WARNINGS|R28|R29|R08|D19" docs\00_raw_idea.md docs\01_feasibility_report.md docs\03_architecture.md docs\04_task_board.md docs\05_decision_log.md docs\06_eval_protocol.md docs\07_handoff.md docs\08_risks_and_open_questions.md
```

Worker 最后还应在报告中简要说明：

- `R29` 具体修正了什么
- `R28` 最终是关闭、降级还是继续保留，依据是什么
- 为什么这些修改没有越出 reviewed evidence 边界

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
