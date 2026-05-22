# T54 Paper Draft

## Task ID

T54

## Goal

基于 `T53` 的 **Narrow** 裁决，把当前已经通过 review 的 pipeline / protocol / diagnostics / provenance / proof-side 证据收敛成一份可审阅的 paper-facing 正文草稿首版，作为后续 figure/table、precision fixes 与 artifact packaging 的共同上游。

## Why Now

`T53` 已经通过 review，项目阶段已明确从“继续扩实验”切换为 “paper-facing / packaging / cleanup”。如果此时不先把 claim boundary、evidence ordering、limitations 和 paper-facing 表述写成正文草稿，后续 `R28/R29` 精度修正、figure/table 渲染和 artifact packaging 会缺少统一叙事锚点，容易再次回到“边做边改 story”的不稳定状态。

## Allowed Files

- `docs/paper_draft.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope

- 不新增任何实验、seed sweep、trace、split 生成或新 demo
- 不修改任何 `project_bootstrap/`、`data/`、`artifacts/` 下的代码或产物
- 不修改 `docs/02_experiment_plan.md`
- 不修改 `docs/experiment_reports/provenance_summary.md`
- 不修改 `docs/paper_outline.md`
- 不把 `R28`、`R29`、`R30`、`R25` 写成已关闭
- 不把 `hierarchy_mixed` 改写成 HGCN 总体胜过 GCN
- 不引入未 review 的新数字、新图表结论或新 related-work 主张

## Inputs to Read

- `docs/02_experiment_plan.md`
- `docs/paper_outline.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/experiment_reports/grouped_training_summary.md`
- `docs/experiment_reports/provenance_summary.md`
- `docs/experiment_reports/ancestor_explanation_demo_report.md`
- `docs/review/M3_review.md`
- `docs/review/T43_review.md`
- `docs/review/T50_review.md`
- `docs/review/T51_review.md`
- `docs/review/T52a_review.md`
- `docs/review/T53_milestone_review.md`
- `docs/review/T53_review.md`

## Expected Output

### 1. Paper Draft

新建：
`docs/paper_draft.md`

该草稿至少应包含以下正文结构：

- `## 1. Title`
- `## 2. Abstract`
- `## 3. Introduction`
- `## 4. Experimental Setup`
- `## 5. Results`
- `## 6. Discussion`
- `## 7. Limitations`
- `## 8. Conclusion`

### 2. Required Content Boundaries

草稿必须满足：

- 明确保持 provenance-conditional 主结论：
  - `explicit_only` 是 primary evidence
  - `synthesized_only` 是 controlled diagnostic
  - `hierarchy_mixed` 是 reproducibility check，且 mixed graph 上 GCN 仍领先
- 明确把 T42/T43/T52a 的证据组织成 paper-facing 叙事，而不是简单复制报告段落
- 明确写出 proof-side bridge 已经落地为 ancestor explanation demo，但不夸大为 end-to-end theorem proving
- 明确写出 clean-environment reproducibility 尚未闭合
- 明确保留 `R28` / `R29` / `R30` / `R25` 的精度与范围边界

### 3. Governance Sync

同步更新治理文档，使其反映：

- `T53` 已完成且 review 通过
- 当前唯一任务是 `T54`
- 下一阶段先做 paper draft，不做新实验

## Acceptance Criteria

1. `docs/paper_draft.md` 已创建，且包含完整的 8 个一级章节。
2. 草稿中的核心 claim 与 `docs/paper_outline.md`、`docs/review/T53_milestone_review.md` 一致，没有把 provenance-conditional 结论写宽。
3. 草稿明确保留 `R28`、`R29`、`R30`、`R25` 的边界，没有把它们写成已关闭。
4. `docs/04_task_board.md`、`docs/05_decision_log.md`、`docs/07_handoff.md` 与 `T54` 当前唯一任务状态一致。
5. 没有修改 forbidden scope 中的任何文件。

## Verification

```powershell
rg -n "## 1\. Title|## 2\. Abstract|## 3\. Introduction|## 4\. Experimental Setup|## 5\. Results|## 6\. Discussion|## 7\. Limitations|## 8\. Conclusion" docs\paper_draft.md
rg -n "provenance-conditional|explicit_only|synthesized_only|hierarchy_mixed|R28|R29|R30|R25|ancestor explanation" docs\paper_draft.md
rg -n "T53|T54|Current Unique Task|Narrow" docs\04_task_board.md docs\05_decision_log.md docs\07_handoff.md
```

## Docs to Update

- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type

normal
