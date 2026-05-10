# T21 Candidate Scan Audit

## Task ID
T21

## Goal
审计 module-level candidate scan 输出，标出更深、更连续、更适合双曲检验的图。

## Why Now
候选图质量决定后续 seed sweep 是否有解释价值。

## Allowed Files
- `docs/candidate_graph_audit.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不重新扫描，除非现有产物缺失且 Captain 批准
- 不修改 configs
- 不启动训练

## Inputs to Read
- `docs/diagnostics_summary.md`
- `artifacts/diagnostics/module_hierarchy_scan_*`
- `project_bootstrap/graph_diagnostics_package/configs/module_hierarchy_scan_*.json`

## Expected Output
- 候选图审计表，至少包含模块名、节点边数、关系深度、正例规模、推荐优先级、风险。

## Verification
```powershell
rg -n "Priority|module|longest|positive|risk" docs\candidate_graph_audit.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
normal
