# T32 Review: GCN Grouped Training Sweep

> Reviewer: Claude Code (adversarial)
> Date: 2026-05-17
> Task package: `docs/tasks/M3_training/T32_gcn_grouped_training_sweep.md`

## Verdict: PASS

Blocking issues
- None.

Non-blocking issues
- The experiment report Section 5 hop bucket table only shows MAP / nDCG / grouped MRR / Recall@10 per bucket. The task package says "hop bucket results where available" and the full Recall@1/3/5/10 per bucket tables exist in the artifact `report.md`. This is an acceptable presentation choice but could be improved in a future revision by either inlining the full table or adding a one-line summary per bucket (e.g. Recall@5).
- The report alternates between "grouped MAP" and "gMAP" in different sections. Minor readability concern only; no ambiguity in meaning.

Missing tests or verification
- None. Both sweep commands ran to completion (5/5 seeds each, `failed_runs = []`). The task package verification commands have been executed. Artifact `aggregate.json`, `report.md`, and per-seed `result_summary.json` all exist and are internally consistent.

Suspicious implementation details
- None found. Cross-checks performed:
  - `aggregate.json` mean/std values match `gcn_grouped_training.md` to all displayed decimal places for both graphs and all reported metrics (grouped MAP, nDCG, nDCG@10, MRR, Recall@1/3/5/10, hop buckets).
  - Per-seed `result_summary.json` confirms `training_loss = "sampled_softmax"`, `query_key_fields = [src_id, relation_type]`, `is_query_level_disjoint = true`, and `best_val_grouped_map` checkpoint selection across all checked seeds.
  - `grouped_training_summary.json` confirms candidate pool, positives/negatives per query, and relation type distribution are consistent with the grouped retrieval protocol.
  - Both base configs explicitly set `grouped_loss = "sampled_softmax"` and `negative_ratio = 10.0`; sweep configs correctly reference them.
  - No source code was changed (verified via `git diff HEAD -- project_bootstrap/baseline_scaffold/src/`).
  - All tracked and untracked files fall within the task package's Allowed files.

## Scope Compliance

| check | result |
| --- | --- |
| Only allowed files modified/created | PASS — 3 tracked doc updates + 5 new files, all within allowed scope |
| No HGCN code changes | PASS — no files under `src/` touched |
| No T31 grouped protocol changes | PASS — configs reference existing runner without modification |
| No historical artifact overwrite | PASS — new directories `grouped_gcn_*_t32/` created |
| No smoke masquerading as formal benchmark | PASS — separate artifact directories with 5 seeds each |
| No `docs/02_experiment_plan.md` edit | PASS — no change to experiment plan |

## Metric Reproducibility Spot-Check

Field.Subfield (from `aggregate.json`):

| metric | aggregate.json mean | report value | match |
| --- | ---: | ---: | --- |
| grouped_test_map | 0.48388 | 0.4839 | yes |
| grouped_test_ndcg | 0.64280 | 0.6428 | yes |
| grouped_test_ndcg_at_10 | 0.52726 | 0.5273 | yes |
| grouped_test_mrr | 0.50435 | 0.5043 | yes |
| grouped_test_recall_at_10 | 0.64220 | 0.6422 | yes |
| hop_2_map | 0.28646 | 0.2865 | yes |
| hop_4_plus_ndcg | 0.50163 | 0.5016 | yes |

Order.Ring (from `aggregate.json`):

| metric | aggregate.json mean | report value | match |
| --- | ---: | ---: | --- |
| grouped_test_map | 0.57893 | 0.5789 | yes |
| grouped_test_ndcg | 0.72927 | 0.7293 | yes |
| grouped_test_ndcg_at_10 | 0.61290 | 0.6129 | yes |
| hop_3_map | 0.30215 | 0.3021 | yes |
| hop_4_plus_map | 0.44809 | 0.4481 | yes |

All spot-checked values match to the displayed precision (4 decimal places).

## Documentation Claims Check

- The report correctly describes results as "GCN only" and states "HGCN comparison remains T33".
- `04_task_board.md` correctly marks T32 checkbox as still unchecked and states "pending adversarial review".
- `07_handoff.md` correctly instructs "不要切到 T33" and lists review focus items.
- `08_risks_and_open_questions.md` correctly updates R22 to Mitigated and adds R23 for Field.Subfield variance sensitivity.
- No document claims hyperbolic superiority or any HGCN result.

Recommended next action
- Captain should mark T32 as complete, update the task board checkbox, and switch the current unique task to T33 (HGCN grouped training sweep under same split and parameter budget). T33 should use the same seed list `[7, 42, 123, 2026, 3407]` and comparable parameter budget (16-dim) for fair GCN-vs-HGCN comparison.
