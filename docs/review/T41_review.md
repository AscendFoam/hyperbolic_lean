# Review: T41

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

### N1. `relation_split_summary.json` overwritten with last-run output

`data/processed/declaration_graph/relation_split_summary.json` was overwritten from the previous batteries split results to the Order.Ring provenance split output. The split script (`split_relations_by_provenance.py`) appears to write its output summary to this single file, so the Field.Subfield run was in turn overwritten by the Order.Ring run.

**Assessment**: Technically within Allowed Files ("new data under `data/processed/declaration_graph/`"). The actual split data directories (the six `mathlib_*_v1_*/` directories with `declarations.csv`, `edges.csv`, `stats.json`) remain intact and independently verified. The summary file is a script output artifact, not a governance document. The original batteries split directories also remain untouched. Acceptable as-is, but the split script's design of writing to a single summary file is a minor architectural concern for reproducibility.

### N2. Diagnostics config created outside Allowed Files

`project_bootstrap/graph_diagnostics_package/configs/graph_diagnostics_provenance_split_t41.json` was created by the worker but is not listed in T41's Allowed Files. The Allowed Files specify "new artifacts under `artifacts/diagnostics/`" and specific docs, but not configs under `project_bootstrap/graph_diagnostics_package/configs/`.

**Assessment**: Low severity. This is a standard diagnostics runner config (seed, sample sizes, graph paths) — not a governance document, not a code change, and does not modify existing configs. It is a necessary tool-side artifact for running the diagnostics. No action required now, but future task packages should include tool-side configs in Allowed Files when the task requires running diagnostic tools.

### N3. `synthesized_only` longest chain = 1 makes T42 model comparison nearly trivial

The report correctly identifies that `synthesized_only` graphs have longest chain = 1, multi-parent = 0, cycle rank = 0. This means every node in the relation layer has at most one outgoing edge, and the grouped retrieval task reduces to a trivial binary classification (each query has exactly one positive ancestor at depth 1).

**Assessment**: The worker correctly flagged this as R27. The report's Section 5.4 already notes the implications. This is a finding, not an implementation issue. T42 should treat `synthesized_only` as a controlled diagnostic, not a primary model comparison.

## Missing Tests

None required. T41 is a data generation and structural diagnostics task. The verification commands from the task package both pass:

1. `rg -n "explicit_only|synthesized_only|hierarchy_mixed|longest|leaf|delta|component|identity|edge count" docs\experiment_reports\provenance_diagnostics.md` — all keywords present across all required sections.
2. `rg -n "\"num_edges\"|\"edge_type_counts\"" data\processed\declaration_graph\*_explicit_only\stats.json ...` — all six `stats.json` files contain the required fields with correct values.

Independent verification confirms:

1. **Edge counts**: All six splits match protocol expected values exactly (FS: 116/36/152; OR: 180/120/300). Verified by reading `stats.json` from each split and cross-checking against source graph `stats.json`. Also verified by counting CSV lines (header + N edges).
2. **hierarchy_mixed identity**: Both candidates confirmed — `hierarchy_mixed` has identical node and edge counts to the full source graph.
3. **Real data, not mock**: `edges.csv` files contain real Lean declaration names (e.g., `Semigroup`, `Monoid`, `Subfield.toDivisionRing`, `RingCone.nonneg.isMaxCone`) with proper `edge_type` and `edge_origin` columns.
4. **No source code modified**: Only data files and documentation were changed.
5. **No existing diagnostics overwritten**: `provenance_split_t41` is a new directory; all previous diagnostics directories remain intact.
6. **No T40 frozen semantics modified**: T40 configs and protocol document untouched.

## Suspicious Implementation Details

None found. Specific checks:

1. **No mock/stub/hardcode**: All six split directories contain real `edges.csv` with verifiable Lean declaration names and edge types. The `edge_origin` column correctly shows `explicit` for `extends` edges and `synthesized` for `instance_of` edges.
2. **No fake execution**: The split script was actually run, producing real output files with correct row counts. The diagnostics were actually run, producing a complete `report.md`, `summary.json`, and six individual graph JSON files.
3. **No data semantic manipulation**: The T40 frozen `origin_map` (`extends → explicit`, `instance_of → synthesized`) was used as-is. No edge types were reclassified.
4. **No over-engineering**: The report covers exactly what the task requires — edge count verification, identity verification, structural comparison across three provenance types, diagnostics protocol classification, and implications for T42. No speculative extensions.
5. **No proxy-as-theorem**: The report consistently uses "hyperbolicity proxy" and "delta/maxdist" as a structural metric, never claiming it constitutes a formal hyperbolicity theorem.

## Recommended Next Action

Captain should mark T41 as complete and advance to T42. T42 worker must:

1. Use `explicit_only` graphs as the primary provenance split for testing hyperbolic advantage — these have the deepest chains (9–10), most multi-parent branching (40–66), and lowest leaf ratios.
2. Treat `synthesized_only` as a controlled diagnostic only — the retrieval task is trivial (longest chain = 1).
3. Use `hierarchy_mixed` results as a reproducibility check against T32/T33 (since hierarchy_mixed = full source graph for both candidates).
4. Generate separate sweep configs for each provenance split, following the config templates in `docs/provenance_split_protocol.md` Section 6.2.
5. Pay special attention to whether HGCN shows any advantage on `explicit_only` graphs specifically, where the hierarchical structure is strongest.
