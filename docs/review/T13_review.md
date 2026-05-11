# T13 Review — Hop Bucket Reporting

> Reviewer: Claude Code (adversarial)
> Date: 2026-05-11
> Task package: `docs/tasks/M1_protocol/T13_hop_bucket_reporting.md`

## Verdict: PASS

## Blocking issues

- None

## Non-blocking issues

1. **Code duplication of `flatten_grouped_hop_bucket_summary`** — The identical 16-line function is copy-pasted into three runner files (`run_relation_gcn_baseline.py:24-39`, `run_relation_hyperbolic_baseline.py:32-47`, `run_relation_grouped_retrieval_baseline.py:34-49`). Additionally, `run_relation_seed_sweep.py` and `_patch_sweep_reports.py` already had a pre-existing `flatten_hop_bucket_metrics` that does the same work from a different source path (`metrics.json` nested structure vs. the `grouped` dict returned by the evaluation function). The duplication is understandable given that each runner is independently executable and the task scope is intentionally minimal, but a future refactor could extract this to `relation_baseline_common.py`.

2. **`format_metric` helper also duplicated** — Added separately in both `run_relation_seed_sweep.py:71-74` and `_patch_sweep_reports.py:38-41`, replacing the prior inline ternary expressions. The refactoring is clean, but the helper is not shared.

3. **Hop Bucket Per Seed table only shows MAP and nDCG** — The per-seed table in the markdown report (`run_relation_seed_sweep.py:158-164`, `_patch_sweep_reports.py:99-108`) only includes `hop_2_map`, `hop_2_ndcg`, `hop_3_map`, `hop_3_ndcg`, `hop_4_plus_map`, `hop_4_plus_ndcg`. The aggregate table includes all 7 metrics per bucket (MAP, nDCG, grouped MRR, Recall@1/3/5/10). This asymmetry means per-seed drill-down is only available for 2 of 7 hop bucket metrics. This is a presentation choice, not a data loss — all 21 hop bucket fields are in the aggregate and per-seed CSV/JSON.

4. **Doc status wording** — `docs/06_eval_protocol.md` line 5 now says "T13 本轮已由 worker 补齐并校验 hop bucket 常规报告入口" which accurately describes what happened but could be read as implicitly endorsing completion. The next sentence correctly gates on adversarial review. No factual error, just a marginal clarity note.

## Missing tests or verification

1. **No end-to-end run** — The worker acknowledged this explicitly: the changes were only statically verified via `rg`. No `result_summary.json` or `report.md` was actually produced by running the modified code against real data. This is acceptable because:
   - The task package explicitly forbids running large-scale sweeps.
   - The code paths only read from existing data structures produced by `evaluate_grouped_ancestor_retrieval` in `relation_baseline_common.py` (lines 260-320), which already populates `hop_buckets`.
   - The data structure contract (`summarize_grouped_scores` returns `{count, mean, min, p50, p90, max}`) is verified at `relation_baseline_common.py:206-216`, and the new code only accesses `.get("mean")` which is always present.

2. **No unit test for `flatten_grouped_hop_bucket_summary`** — The function is simple enough (two nested loops over a fixed schema) that a unit test would be nice but is not blocking.

## Suspicious implementation details

1. **None.** The implementation is straightforward: each runner's `result_summary` assembly section already had `grouped.get("map")` etc., and the new code adds `result_summary.update(flatten_grouped_hop_bucket_summary(grouped))` in the same block. The data flow is:
   - `evaluate_grouped_ancestor_retrieval` returns `grouped` dict with `hop_buckets` nested structure
   - `flatten_grouped_hop_bucket_summary` reads from `grouped["hop_buckets"]` and flattens to `hop_{bucket}_{metric}` keys
   - These get written to `result_summary.json`
   - The seed sweep's pre-existing `flatten_hop_bucket_metrics` independently reads from `metrics.json` (the same data, different serialization path)
   - The aggregation loop in the sweep already listed all 21 hop bucket metric names, so aggregate computation works

2. **All access patterns are safe** — `.get()` with empty-dict defaults throughout, so missing hop bucket data gracefully produces `None` values rather than crashes.

## Scope compliance

- All changed files are within `Allowed files`: `project_bootstrap/baseline_scaffold/src/*.py`, `docs/06_eval_protocol.md`, `docs/04_task_board.md`, `docs/07_handoff.md`.
- No files outside allowed scope were touched.
- No training objective changes.
- No large-scale sweep executed.
- No dry-run results written as formal results.
- Documentation correctly marks T13 as pending adversarial review, not as completed.

## Recommended next action

- Captain may mark T13 as completed.
- The next task should be selected from Milestone 2 (T20-T22) per the experiment plan's phase ordering, unless the Captain judges otherwise.
- When real experiments are eventually run (e.g., T32/T33 seed sweeps), the end-to-end output chain should be spot-checked to confirm that `result_summary.json` and `report.md` contain the expected hop bucket values.
- Consider extracting the duplicated `flatten_grouped_hop_bucket_summary` to `relation_baseline_common.py` during a future refactor task.
