# T50 Paper Skeleton

## Task ID
T50

## Goal
整理论文贡献骨架，围绕 pipeline / protocol / diagnostics / conditional hyperbolic conclusion。

## Why Now
在主要协议和诊断任务稳定后，需要把结果组织为可投稿叙事，避免项目散成脚本集合。

## Allowed Files
- `docs/paper_outline.md`
- `docs/05_decision_log.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`

## Forbidden Scope
- 不编造实验结果
- 不写成已被 acceptance 的论文
- 不改变项目主线为模型 SOTA

## Inputs to Read
- `docs/02_experiment_plan.md`
- `docs/投稿路线图（FM-ITP-CPP-备选 venue 对照）.md`
- milestone reports

## Expected Output
- paper outline，包含 claim、contributions、figures/tables、threats、venue fit。

## Verification
```powershell
rg -n "Contribution|Claim|Figure|Table|Threat|ITP|CPP|FM" docs\paper_outline.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`

## Reviewer Type
normal
