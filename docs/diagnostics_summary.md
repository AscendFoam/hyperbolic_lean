# Diagnostics Summary

Updated: 2026-05-12

## Scope

This note summarizes existing diagnostics only. It does not rerun diagnostics, modify artifacts, or claim a final benchmark conclusion.

Reviewed sources:

- `artifacts/diagnostics/real_graphs_v1/report.md`
- `artifacts/diagnostics/hierarchy_focus_v1/report.md`
- `artifacts/diagnostics/mathlib_order_focus_v1/report.md`

## High-Level Takeaways

- Most existing real-graph and hierarchy-focused relation layers are still shallow and often look like a forest or star-forest.
- Those graphs are useful as diagnostics and sanity references, but they are weak foundations for a strong hyperbolic advantage claim.
- The strongest next-pass candidates come from `mathlib_order_focus_v1`, where several module-level graphs are materially deeper and have more multi-parent structure.

## Diagnostic Snapshot

| Graph | Nodes | Edges | Longest chain | Multi-parent | Leaves | Delta / maxdist | Judgment | Recommended role |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `lean4_example_*` relation layer | 1090 | 978 | 4 | 3 | 963 | n/a | shallow, leaf-heavy | diagnostic reference only |
| `plausible_*` relation layer | n/a | n/a | 1 | n/a | n/a | n/a | extremely shallow | diagnostic reference only |
| `batteries_*` relation layer | 4919 | 4720 | 4 | 12 | 4666 | n/a | shallow, leaf-heavy | diagnostic reference only |
| `lean4_example_typeclass_precise_v2` | n/a | n/a | 4 | n/a | n/a | n/a | shallow | hierarchy-focused reference |
| `plausible_typeclass_precise_v1` | n/a | n/a | 1 | n/a | n/a | n/a | extremely shallow | hierarchy-focused reference |
| `mathlib_algebra_order_d3` | 1349 | 1387 | 11 | 133 | 1044 | 0.182 | deepest current probe, but fragmented and leaf-heavy | top candidate for next-pass benchmark scan |
| `mathlib_algebra_order_ring_d4` | 253 | 300 | 10 | 66 | 127 | 0.107 | deep and more compact | strong practical candidate |
| `mathlib_algebra_ring_subring_d4` | 153 | 170 | 10 | 44 | 46 | 0.182 | focused and structurally nontrivial | controlled benchmark / ablation candidate |
| `mathlib_algebra_field_subfield_d4` | 133 | 152 | 10 | 40 | 37 | 0.250 | focused and promising, but small | controlled benchmark / ablation candidate |

## Shallow vs Candidate Split

Shallow or mostly diagnostic-only:

- `real_graphs_v1` relation layers for `lean4_example_*`, `plausible_*`, and `batteries_*`
- `hierarchy_focus_v1` graphs such as `lean4_example_typeclass_precise_v2` and `plausible_typeclass_precise_v1`

Candidate pool for follow-up tasks:

- `mathlib_algebra_order_d3`
- `mathlib_algebra_order_ring_d4`
- `mathlib_algebra_ring_subring_d4`
- `mathlib_algebra_field_subfield_d4`

## Provisional Candidate Priority

This is a provisional priority order for follow-up, not a final benchmark conclusion.

1. `mathlib_algebra_order_d3`
2. `mathlib_algebra_order_ring_d4`
3. `mathlib_algebra_ring_subring_d4`
4. `mathlib_algebra_field_subfield_d4`

## Priority Rationale

- `mathlib_algebra_order_d3` has the strongest depth signal among reviewed artifacts, with longest chain `11` and meaningful multi-parent structure. It is the best current stress test for whether deeper traced relation graphs can support stronger hyperbolic diagnostics. Its main weakness is fragmentation and a heavy leaf ratio.
- `mathlib_algebra_order_ring_d4` is slightly smaller and less extreme, but still deep with longest chain `10` and enough branching to be a realistic benchmark candidate. It may be the most practical next benchmark if `mathlib_algebra_order_d3` proves too fragmented.
- `mathlib_algebra_ring_subring_d4` and `mathlib_algebra_field_subfield_d4` are useful because they are focused, deeper than the shallow real-graph baselines, and likely easier to inspect manually. They look better as controlled probes or ablations than as the single top benchmark choice.

## What This Summary Does Not Claim

- It does not claim that hyperbolic models will outperform Euclidean baselines on these graphs.
- It does not claim that the current candidate priority is final.
- It does not replace later module-level candidate scans, training alignment work, or provenance-split diagnostics.

## Recommended Immediate Use

- Use this summary as the selection input for the next diagnostics-stage review.
- Treat `mathlib_algebra_order_d3` and `mathlib_algebra_order_ring_d4` as the main follow-up options.
- Treat `mathlib_algebra_ring_subring_d4` and `mathlib_algebra_field_subfield_d4` as smaller controlled probes.
- Keep shallow real-graph artifacts as reference evidence for why naive graph choice can hide any hyperbolic advantage behind forest-like structure.
