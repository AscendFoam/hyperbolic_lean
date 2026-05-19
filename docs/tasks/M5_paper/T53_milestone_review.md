# T53 Milestone Review

## Task ID

T53

## Goal

基于已经通过 review 的 Milestone 1~5 产物，完成一次只读型里程碑审查，明确项目下一阶段应进入：

- `Continue`
- `Narrow`
- `Resume-ready`

并把该判断写成正式的 milestone review 文档，供后续 captain/worker/reviewer 直接接续。

## Why Now

`T52a` 已经把 proof-side MVP 从任务包落实为真实可运行的 demo CLI 与 demo report。当前缺的不是继续扩写实现，而是把整个项目到 Milestone 5 的 reviewed 证据收束成一个阶段性裁决：

- 现在是否已经足够支持继续推进
- 是否需要收窄叙事或交付面
- 是否已经进入“可暂停、可恢复、可对外组织材料”的状态

如果没有这一步，后续 worker 很容易一边继续开发、一边重复讨论已经收束的方向判断。

## Allowed Files

- `docs/review/T53_milestone_review.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope

- 不新增任何训练、seed sweep、trace、split 生成、诊断运行或新 demo
- 不修改任何 `project_bootstrap/`、`data/`、`artifacts/` 下的代码或实验产物
- 不重写 `docs/02_experiment_plan.md`
- 不推翻已经通过 review 的历史 verdict；本任务只能在其基础上做阶段性归纳
- 不把尚未关闭的 `R28`、`R29`、`R30`、`R31` 写成“已完全解决”

## Inputs to Read

- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/paper_outline.md`
- `docs/proof_side_mvp.md`
- `docs/experiment_reports/grouped_training_summary.md`
- `docs/experiment_reports/provenance_summary.md`
- `docs/experiment_reports/ancestor_explanation_demo_report.md`
- `docs/review/M3_review.md`
- `docs/review/T43_review.md`
- `docs/review/T50_review.md`
- `docs/review/T51_review.md`
- `docs/review/T52_review.md`
- `docs/review/T52a_review.md`

## Expected Output

### 1. Milestone Review Document

新建：

`docs/review/T53_milestone_review.md`

文档至少要包含：

- 明确 verdict：`Continue` / `Narrow` / `Resume-ready`
- 一段简洁总述，说明为什么是这个 verdict
- `Evidence` 小节，至少覆盖：
  - protocol/governance 是否闭环
  - grouped benchmark 是否已 reviewed
  - provenance-conditional conclusion 是否已 reviewed
  - proof-side bridge 是否已从 paper story 变成真实 demo
- `Residual Risks` 小节，必须明确引用仍然活跃的高价值风险
- `Recommended Next Task Shape` 小节，说明后续任务应偏向：
  - 继续开发
  - 收窄为 paper-facing / packaging / cleanup
  - 或进入 resume-ready 整理态

### 2. Governance Sync

同步更新治理文档，使其与 T53 审查前后的状态一致：

- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

至少需要做到：

- 把 `T52a` 明确标记为已完成
- 把 `Current Unique Task` 切换为 `T53`
- 在 handoff 中明确：当前下一步不是继续写新 demo，而是执行 milestone review
- 在 decision log 中记录 T52a 已正式通过 review 并切换到 T53
- 风险文档中保持 `R28`、`R29`、`R30`、`R31` 的真实状态，不夸大 closure

## Acceptance Criteria

1. `docs/review/T53_milestone_review.md` 明确写出 `Continue` / `Narrow` / `Resume-ready` 之一，不能模糊表态。
2. 结论必须直接建立在已 reviewed 证据上，不能依赖未 review 的新分析。
3. `docs/04_task_board.md` 中 `T52a` 已完成，且 `Current Unique Task` 变为 `T53`。
4. `docs/07_handoff.md` 不再把 `T52a` 写成当前任务。
5. 风险文档对 `R28`、`R29`、`R30`、`R31` 的状态与当前事实一致，没有误写为 closed。

## Verification

```powershell
rg -n "Continue|Narrow|Resume-ready|Evidence|Residual Risks|Recommended Next Task Shape" docs\review\T53_milestone_review.md
rg -n "T52a|T53|Current Unique Task|Milestone 5" docs\04_task_board.md docs\07_handoff.md docs\05_decision_log.md
rg -n "R28|R29|R30|R31" docs\08_risks_and_open_questions.md docs\07_handoff.md docs\review\T53_milestone_review.md
```

## Docs to Update

- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type

milestone
