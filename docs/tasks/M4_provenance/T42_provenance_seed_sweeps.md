# T42 Provenance Seed Sweeps

## Task ID
T42

## Goal
在 explicit_only / synthesized_only / hierarchy_mixed 三类 provenance 图上运行 grouped retrieval / parent prediction 的 GCN 与 HGCN 5-seed sweep，并给出按 split 分开的正式对照结论。

## Why Now
T41 已经证明三类 provenance 图的结构角色并不相同：explicit_only 承载层级深度与多父分支，synthesized_only 基本退化为 longest chain = 1 的 trivial task，hierarchy_mixed 在当前两组候选图上等同于 full source graph。下一步必须在这个前提下完成受约束的模型对比，而不是把三类 split 混成同一种实验对象。

## Allowed Files
- new artifacts under rtifacts/baselines/relation_seed_sweeps/
- docs/experiment_reports/provenance_seed_sweeps.md
- relevant configs under project_bootstrap/baseline_scaffold/configs/
- relevant configs under project_bootstrap/graph_diagnostics_package/configs/
- docs/04_task_board.md
- docs/07_handoff.md
- docs/08_risks_and_open_questions.md

## Forbidden Scope
- do not modify T40/T41 frozen provenance semantics, split directories, or protocol wording
- do not rewrite explicit_only / synthesized_only / hierarchy_mixed into a new split taxonomy
- do not treat synthesized_only as primary evidence for model ranking
- do not overwrite prior sweep artifacts or historical benchmark reports
- do not reopen unrelated runner refactors outside the configs and artifacts needed for this task

## Inputs to Read
- docs/provenance_split_protocol.md
- docs/experiment_reports/provenance_diagnostics.md
- docs/06_eval_protocol.md
- T32/T33 grouped sweep artifacts and reports
- T40/T41 outputs
- seed sweep scripts and current grouped baseline configs

## Expected Output
- matched GCN/HGCN 5-seed sweep artifacts for each candidate and each provenance split
- a report that separates:
  - explicit_only as the primary provenance comparison
  - synthesized_only as a controlled diagnostic
  - hierarchy_mixed as a reproducibility check against T32/T33
- grouped retrieval metrics with mean/std, hop-bucket summaries, and parent prediction summaries
- an explicit statement on whether HGCN shows any advantage specifically on explicit_only

## Verification
`powershell
rg -n "explicit_only|synthesized_only|hierarchy_mixed|GCN|HGCN|mean|std|Recall|MAP|nDCG|controlled diagnostic|reproducibility" docs\experiment_reports\provenance_seed_sweeps.md
rg -n "explicit_only|synthesized_only|hierarchy_mixed" artifacts\baselines\relation_seed_sweeps\**\report.md
`

## Docs to Update
- docs/04_task_board.md
- docs/07_handoff.md
- docs/08_risks_and_open_questions.md

## Reviewer Type
adversarial
