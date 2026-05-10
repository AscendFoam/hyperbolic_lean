# T41 Provenance Diagnostics

## Task ID
T41

## Goal
对三类 provenance 图运行结构诊断，比较深度、叶子比例、连通性和 hyperbolicity proxy。

## Why Now
必须先知道 provenance split 是否真的改变结构，再解释模型差异。

## Allowed Files
- new artifacts under `artifacts/diagnostics/`
- `docs/experiment_reports/provenance_diagnostics.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`

## Forbidden Scope
- 不运行模型训练
- 不覆盖已有 diagnostics
- 不把 proxy 写成严格 hyperbolicity 定理

## Inputs to Read
- T40 protocol and review
- `project_bootstrap/graph_diagnostics_package`
- `docs/diagnostics_protocol.md`

## Expected Output
- provenance diagnostics 报告和 artifact 路径。

## Verification
```powershell
rg -n "explicit|synthesized|mixed|longest|leaf|delta|component" docs\experiment_reports\provenance_diagnostics.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
adversarial
