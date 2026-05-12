# T20 Review

## Verdict: PASS_WITH_WARNINGS

## Blocking issues

- None

## Non-blocking issues

1. **`n/a` entries for plausible and hierarchy-focused graphs**: The summary table uses `n/a` for node/edge counts on `plausible_*` relation layer and on `lean4_example_typeclass_precise_v2` / `plausible_typeclass_precise_v1`. The actual artifacts contain real numbers (e.g., plausible relation layer: 72 nodes, 68 edges; plausible_typeclass_precise_v1: 78 nodes, 145 edges). While these graphs are correctly judged as shallow/extremely shallow and the missing numbers do not affect any priority decision, the `n/a` entries are factually imprecise where real data exists.

2. **Mixed metric source in single table**: The summary table includes both relation-layer graphs and hierarchy-focused full graphs in one table using a single "Longest chain" column. The original reports have separate sub-tables for full-graph overview metrics (diameter est.) and relation-layer metrics (longest chain). The summary does not annotate which source each row draws from. For all rows the values match the relation-layer sub-table, but this sourcing is implicit.

## Missing tests or verification

- None. The task is documentation-only. The verification command (`rg -n "longest chain|leaf|candidate|priority|shallow|forest" docs\diagnostics_summary.md`) was run and all target keywords are present. Cross-checking the summary table against the three source artifacts confirms that all concrete numeric values are accurate.

## Suspicious implementation details

- None. No code was changed. All four modified files (`diagnostics_summary.md`, `04_task_board.md`, `07_handoff.md`, `08_risks_and_open_questions.md`) are within the task package's Allowed Files. No artifacts were modified.

## Scope compliance

- **Allowed files**: All edits are within scope (`docs/diagnostics_summary.md`, `docs/04_task_board.md`, `docs/07_handoff.md`, `docs/08_risks_and_open_questions.md`).
- **Forbidden scope**: No diagnostics were rerun, no artifacts were modified, and no diagnostic estimate is written as a precise theorem.
- **Expected output**: `docs/diagnostics_summary.md` contains graph list, key structural metrics, shallow/deeper judgment, and candidate priority.

## Key positive observations

1. The summary correctly identifies that most real-graph and hierarchy-focused relation layers are shallow forest/star-forest structures.
2. The provisional priority order is well-justified: `mathlib_algebra_order_d3` (deepest, longest chain 11, 133 multi-parent) is the strongest candidate; `mathlib_algebra_order_ring_d4` is a practical fallback; the smaller two graphs are appropriately positioned as controlled probes.
3. The "What This Summary Does Not Claim" section and the explicit "provisional, not a final benchmark conclusion" language prevent premature certainty.
4. The R04 update in `08_risks_and_open_questions.md` accurately reflects T20 findings without overstating them.
5. Open questions 1-2 were appropriately refined to reflect the T20 provisional ranking.

## Recommended next action

- Accept T20 as complete. Captain should:
  1. Mark T20 as done in `04_task_board.md`.
  2. Update `07_handoff.md` to reflect review completion.
  3. Select the next task (T21 or T22) based on the provisional candidate priority.
- Optional: if a future revision of `diagnostics_summary.md` is convenient, fill in the `n/a` entries from the actual artifact data.
