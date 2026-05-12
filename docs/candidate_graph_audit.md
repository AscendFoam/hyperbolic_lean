# Candidate Graph Audit

Updated: 2026-05-12

## Scope

This note audits existing module-level candidate scan outputs only. It does not rerun scans, modify configs, or start training.

Reviewed inputs:

- `docs/diagnostics_summary.md`
- `artifacts/diagnostics/module_hierarchy_scan_mathlib_algebra_order_index_v1/report.md`
- `artifacts/diagnostics/module_hierarchy_scan_mathlib_algebra_order_index_v1/ranking.csv`
- `artifacts/diagnostics/module_hierarchy_scan_mathlib_algebra_order_index_v1/summary.json`
- `artifacts/diagnostics/module_hierarchy_scan_batteries_v1/report.md`
- `artifacts/diagnostics/module_hierarchy_scan_batteries_v1/ranking.csv`
- `artifacts/diagnostics/module_hierarchy_scan_batteries_v1/summary.json`
- `project_bootstrap/graph_diagnostics_package/configs/module_hierarchy_scan_batteries_v1.json`

Note: the standalone checked-in config for the mathlib module scan is not present in the current workspace, but the scan settings are embedded in `summary.json`.

## Audit Criteria

- `longest chain`: depth signal.
- `relation positive edges`: current positive-scale proxy from the retained relation layer.
- `component ratio`: `largest_relation_component / relation_nodes`, used as a continuity proxy.
- `leaf ratio`: higher values indicate more forest-like or star-like structure.
- `ancestor_added_nodes`: closure sensitivity proxy. Large values mean the candidate depends heavily on ancestor expansion rather than the seed module alone.

## Main Findings

- The `mathlib_algebra_order_index_v1` scan contains usable candidates for follow-up. The `batteries_v1` scan remains mostly too shallow or too small for the next benchmark pass.
- Raw scan score is not enough. Several small modules score very well because they are locally clean, but their positive scale is limited and their semantics are narrow.
- `Mathlib.Algebra.Order.Ring` is the most balanced next-pass candidate once continuity and positive scale are weighted alongside depth.
- `Mathlib.Algebra.Order` remains the strongest stress-test graph for depth and positive scale, but its fragmentation and leaf-heavy shape are still material audit risks.
- `Mathlib.Algebra.Ring.Subring` and `Mathlib.Algebra.Field.Subfield` remain strong controlled probes, but both are closure-heavy and smaller than the top two follow-up choices.

## Audit Table

`relation positive edges` below means retained relation edges on the scan relation layer.

| module | depth | relation nodes | relation positive edges | longest chain | component ratio | leaf ratio | ancestor added | Priority | main risk |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `Mathlib.Algebra.Order.Ring` | 4 | 253 | 300 | 10 | 0.747 | 0.502 | 116 | P1 balanced follow-up | moderate closure expansion, still some fragmentation |
| `Mathlib.Algebra.Order` | 3 | 1349 | 1387 | 11 | 0.489 | 0.774 | 213 | P2 depth stress-test | leaf-heavy and fragmented despite strong scale |
| `Mathlib.Algebra.Ring.Subring` | 4 | 153 | 170 | 10 | 0.431 | 0.301 | 106 | P3 controlled probe | small-to-medium scale and heavy ancestor closure |
| `Mathlib.Algebra.Field.Subfield` | 4 | 133 | 152 | 10 | 0.406 | 0.278 | 95 | P4 controlled probe | small scale and heavy ancestor closure |
| `Mathlib.Algebra.Field` | 3 | 199 | 227 | 10 | 0.583 | 0.467 | 101 | Hold secondary candidate | less scale than P1/P2 and closure cost is still high |
| `Mathlib.Algebra.Small` | 3 | 102 | 135 | 10 | 0.931 | 0.422 | 59 | Hold small clean probe | high score but too small and narrow for main benchmark use |
| `Mathlib.Algebra.Equiv` | 3 | 117 | 153 | 10 | 0.897 | 0.436 | 66 | Hold small clean probe | high score but limited scale and narrow semantics |
| `Batteries.Control.AlternativeMonad` | 3 | 30 | 28 | 4 | 0.567 | 0.533 | 11 | Not recommended for benchmark | too shallow and too small |
| `Batteries.Classes.Order` | 3 | 25 | 26 | 3 | 1.000 | 0.760 | 0 | Not recommended for benchmark | fully connected but tiny and leaf-heavy |

## Priority Interpretation

1. `Mathlib.Algebra.Order.Ring` should be treated as the best balanced candidate from a data-quality perspective. It keeps chain length `10`, has a much better component ratio than `Mathlib.Algebra.Order`, and still provides enough relation positives to support later grouped retrieval or parent-prediction comparisons.
2. `Mathlib.Algebra.Order` should be kept as the main depth stress-test rather than the default benchmark. Its positive scale is the strongest in the audited pool, but the giant component only covers about half of the relation nodes and the leaf ratio stays high.
3. `Mathlib.Algebra.Ring.Subring` and `Mathlib.Algebra.Field.Subfield` are still useful, but they now read more like controlled probes than default benchmark choices. Their scan scores are high partly because they are compact and structurally cleaner, not because they dominate on scale.

## Why Some High-Score Modules Were Not Promoted

- `Mathlib.Algebra.Small` and `Mathlib.Algebra.Equiv` are structurally cleaner than the larger order-oriented candidates, but they are much smaller and narrower. They are better audit references or ablations than default benchmark graphs.
- The `Batteries` family does not provide enough depth. Even its best module-level candidates only reach `longest chain = 4`, which is too close to the already-known shallow diagnostic regime.

## Audit-Level Risks

- The scan hierarchy score can over-rank small, compact modules if positive scale and closure cost are not checked separately.
- Several attractive depth-4 candidates depend heavily on ancestor closure. That weakens the claim that they are cleanly module-local benchmarks.
- The mathlib scan is reproducible from `summary.json`, but its standalone config file is not checked into the current workspace, which weakens traceability.

## Provisional Outcome

This audit does not set a final benchmark conclusion. It only reorders follow-up priority under a stricter data-quality lens:

1. `Mathlib.Algebra.Order.Ring`
2. `Mathlib.Algebra.Order`
3. `Mathlib.Algebra.Ring.Subring`
4. `Mathlib.Algebra.Field.Subfield`

Secondary hold set:

- `Mathlib.Algebra.Field`
- `Mathlib.Algebra.Small`
- `Mathlib.Algebra.Equiv`

Rejected for next benchmark pass:

- `Batteries` module-scan candidates as a family
