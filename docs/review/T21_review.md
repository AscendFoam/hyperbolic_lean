# T21 Review

## Verdict: PASS

## Blocking issues

- None

## Non-blocking issues

1. **"depth" column label ambiguity**: The audit table has a "depth" column (values 3 or 4) and a separate "longest chain" column. The "depth" column refers to the module hierarchy scan depth parameter (d3/d4), not the graph's structural depth. This distinction is critical — "depth 4" means the scan expanded 4 levels of module nesting, while "longest chain 10" is the graph's actual chain length. A reader could confuse these two meanings of "depth." Consider renaming to "scan depth" or "module depth" in a future revision.

2. **Audit table coverage not explained**: The mathlib scan contains 103 candidates across depths 2–4, but the audit table only includes 9 entries. The selection is clearly guided by the T20 provisional priority, but the document does not explicitly state why these specific 9 were chosen and not others (e.g., `Mathlib.Algebra.Colimit`, `Mathlib.Algebra.Order.CauSeq`, or depth-2 modules like `Mathlib.Algebra` with 6800 nodes). This is reasonable judgment (the T20 candidates plus a few secondary/batteries contrasts), but making the selection rationale explicit would help future readers.

3. **Config traceability gap acknowledged but not resolved**: The document notes that the standalone config for the mathlib module scan is not checked into the workspace, and that scan settings are embedded in `summary.json`. This is honest but leaves a reproducibility gap that should be tracked.

## Missing tests or verification

- None. The task is documentation-only. The verification command (`rg -n "Priority|module|longest|positive|risk" docs\candidate_graph_audit.md`) was run and all target keywords are present. Cross-checking every numeric value in the audit table against `summary.json` and individual `stats.json` files confirms all data is accurate.

## Suspicious implementation details

- None. No code was changed. All four modified/new files (`docs/candidate_graph_audit.md`, `docs/04_task_board.md`, `docs/07_handoff.md`, `docs/08_risks_and_open_questions.md`) are within the task package's Allowed Files. No artifacts, configs, or training code were modified.

## Scope compliance

- **Allowed files**: All edits are within scope.
- **Forbidden scope**: No scan was rerun, no configs were modified, no training was started.
- **Expected output**: The audit table includes module name, node/edge counts, relation depth, positive scale, recommended priority, and risk — meeting all requirements.

## Key positive observations

1. **All numeric values verified correct** against source artifacts (`summary.json`, `stats.json`, `ranking.csv`, `report.md`) for all 9 entries in the audit table.

2. **Insightful priority reordering**: T20 had `mathlib_algebra_order_d3` (=`Mathlib.Algebra.Order`) as #1 and `mathlib_algebra_order_ring_d4` (=`Mathlib.Algebra.Order.Ring`) as #2. T21 justifiably reverses this: `Order.Ring` becomes P1 because its component ratio (0.747 vs 0.489) and leaf ratio (0.502 vs 0.774) make it more balanced, even though `Order` has a longer chain (11 vs 10) and more positive edges (1387 vs 300). This reordering is well-supported by the data-quality audit.

3. **New risk R14 is valuable**: The identification that raw hierarchy score can over-rank small compact modules is an important finding that wasn't previously tracked.

4. **Appropriate language discipline**: The document explicitly states "This audit does not set a final benchmark conclusion" and labels the outcome as "Provisional."

5. **Open questions appropriately refined**: Q1–Q2 were updated from T20-era `order_d3` vs `order_ring_d4` to the more specific question of whether `Order.Ring` should be the default benchmark and whether T22 should codify explicit thresholds.

## Recommended next action

- Accept T21 as complete. Captain should:
  1. Mark T21 as done in `04_task_board.md`.
  2. Update `07_handoff.md` to reflect review completion.
  3. Select the next task. The natural next step is T22 (diagnostic threshold template), which T21's R14 and Open Question 2 directly feed into.
- Optional future revision: rename "depth" column to "scan depth" for clarity.
