# T14 Review — M1 Smoke Check And Cleanup

> Reviewer: Claude Code (normal review)
> Date: 2026-05-11
> Task package: `docs/tasks/M1_protocol/T14_m1_smoke_check_and_cleanup.md`

## Verdict: PASS

## Blocking issues

- None

## Non-blocking issues

1. **`.claude/settings.json` has an unrelated auto-permission diff** — The working tree shows `.claude/settings.json` gained `Bash(git status *)` in the allowlist. This is not in the task package's `Allowed Files` and is a Claude Code auto-permission artifact, not an intentional project change. It should not be committed as part of T14. The worker likely didn't notice because Claude Code added it automatically. **Recommendation**: Captain should exclude this file when staging T14 changes.

2. **`format_metric` duplication in sweep reporters not addressed** — `run_relation_seed_sweep.py:71-74` and `_patch_sweep_reports.py:38-41` still have identical `format_metric` helpers. The worker explicitly scoped this out, which is correct — the task package says "如果清理会扩大范围，则只记录 deferred item", and D05 already tracks this. Acceptable deferral.

3. **Smoke only covers GCN runner, not HGCN or grouped retrieval** — The smoke ran `run_relation_gcn_baseline.py` only. The HGCN runner and grouped retrieval runner were not smoke-tested. However, all three runners now import the same `flatten_grouped_hop_bucket_summary` from `relation_baseline_common.py`, so if the import works for GCN (which the smoke confirms), it works for the others too. The dedup specifically eliminated the per-runner copy-paste, making this a low residual risk.

## Missing tests or verification

- None beyond what the task provides. The smoke itself IS the verification. I independently read `artifacts/smoke/.../result_summary.json` and confirmed:
  - `grouped_test_ndcg_at_10` is present: `0.09507366307751126`
  - All 21 hop bucket fields are present with real float values (no `null`)
  - Values vary across buckets (`hop_2_map=0.0898`, `hop_3_map=0.0121`, `hop_4_plus_map=0.0357`), confirming the field paths are not all reading the same data
  - `hop_1` is correctly excluded from `result_summary.json` (only `hop_2 / hop_3 / hop_4_plus` per protocol)
- The static verification (`rg`) was also run per the task package.

## Suspicious implementation details

1. **None.** The dedup is clean: each runner's local `flatten_grouped_hop_bucket_summary` definition was removed, and the import from `relation_baseline_common` was added in its place. The function signature and body are identical to what was in the runners. The smoke config is appropriately minimal (dim=8, epochs=1, single seed) and explicitly outputs to `artifacts/smoke/`, not to the baseline artifact directory.

2. **Smoke values are plausible for a tiny config.** `hop_4_plus_recall_at_10=0.0` might look suspicious but is expected for a single-epoch, 8-dimensional run on a shallow graph — the model hasn't learned anything useful for distant ancestors.

## Scope compliance

- Changed files within `Allowed Files`:
  - `project_bootstrap/baseline_scaffold/src/relation_baseline_common.py` — added shared function
  - `project_bootstrap/baseline_scaffold/src/run_relation_gcn_baseline.py` — replaced local def with import
  - `project_bootstrap/baseline_scaffold/src/run_relation_hyperbolic_baseline.py` — replaced local def with import
  - `project_bootstrap/baseline_scaffold/src/run_relation_grouped_retrieval_baseline.py` — replaced local def with import
  - `docs/06_eval_protocol.md`, `docs/04_task_board.md`, `docs/07_handoff.md`, `docs/08_risks_and_open_questions.md` — updated per task
- New files:
  - `project_bootstrap/baseline_scaffold/configs/relation_gcn_typeclass_precise_v2_ancestor_ranking_smoke_t14.json` — allowed ("relevant small/smoke config files")
  - `artifacts/smoke/...` — allowed ("smoke output under `artifacts/smoke/`")
- No training objective changes.
- No new model architecture.
- No large-scale sweep.
- Smoke not written as formal benchmark result — explicitly disclaimed in all docs and in the `06_eval_protocol.md` smoke convention section.
- `docs/02_experiment_plan.md` was not modified, per forbidden scope.

## Recommended next action

- Captain may mark T14 as completed.
- Captain should exclude `.claude/settings.json` from the T14 commit (it's a Claude Code auto-permission artifact, not a project change).
- With M1 fully closed, the next task should come from Milestone 2 (T20-T22: diagnostics and candidate graph selection), which aligns with the experiment plan's phase ordering.
- D05 (`format_metric` dedup) and D06 (full seed sweep verification) remain deferred to their stated trigger conditions.
