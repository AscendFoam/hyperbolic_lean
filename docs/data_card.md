# Data Card

> Updated: 2026-05-10
>
> Status: draft data card prepared by `T11`; reviewer validation is still pending.

## Purpose

This data card describes the currently usable declaration-graph assets, their observed fields, relation semantics, coverage-aware handling, and usage limits. It should be read together with `docs/data_manifest.md`, which remains the source of truth for version anchors and `unknown / needs verification` items.

## 1. Scope

This document covers the currently inspected assets under `data/processed/declaration_graph/` and the linked diagnostics under `artifacts/diagnostics/`.

It does not claim that every graph root has identical files, labels, or split metadata. It also does not upgrade local snapshot strings into canonical version facts.

## 2. Observed Asset Layout

The declaration-graph roots currently follow this minimum file pattern:

- `declarations.csv`
- `edges.csv`
- `stats.json`

Optional files such as `labels.csv` and `splits.csv` are recommended by `data/processed/declaration_graph/README.md`, but they are not guaranteed in every current graph root. For example, `lean4_example_typeclass_precise_v2` currently contains only `declarations.csv`, `edges.csv`, and `stats.json`.

`data/processed/proof_graph/` is reserved for later proof-state assets and should not be treated as a current benchmark source.

## 3. Observed Field Schema

### 3.1 declarations.csv

Observed columns in inspected roots include:

- `declaration_id`
- `decl_name`
- `decl_short_name`
- `raw_decl_name`
- `name_qualification_source`
- `decl_kind`
- `module_name`
- `file_path`
- `namespace`
- `line_start`
- `line_end`
- `signature_text`
- `body_text`
- `docstring`
- `ast_size`
- `token_count`
- `dependency_depth`
- `source_commit`
- `trace_version`
- `source_trace_file`

Important interpretation notes:

- `source_commit` is useful for asset-local provenance, but it does not replace the reviewed version lock in `docs/data_manifest.md`.
- `trace_version` is an observed snapshot label, not a canonical environment manifest.
- `name_qualification_source` can differ by asset family, for example `ancestor_full_name` in `lean4_example_typeclass_precise_v2` and `declaration_index_only` in `mathlib_algebra_order_precise_coverage_index_v1`.

### 3.2 edges.csv

Observed columns in inspected roots include:

- `edge_id`
- `src_id`
- `dst_id`
- `edge_type`
- `evidence_source`
- `weight`
- `is_direct`
- `source_commit`

Observed `edge_type` values:

- `uses`
- `extends`
- `instance_of`

Observed `evidence_source` values:

- `normalized_trace`
- `lean_meta_exact`

### 3.3 stats.json

Observed `stats.json` fields include:

- graph-level counts such as `num_declarations` and `num_edges`
- type counts such as `decl_kind_counts` and `edge_type_counts`
- relation extraction settings such as `prefer_exact_relations`, `add_exact_extends_edges`, and `add_exact_instance_of_edges`
- skip counts such as `skipped_exact_relation_rows_missing_nodes`
- optional `coverage_aware_backfill` blocks for coverage-repaired assets

## 4. relation Semantics And Provenance

### 4.1 Base relation semantics

- `uses`: declaration-level dependency edges derived from normalized trace evidence
- `extends`: hierarchy edges between class-like declarations
- `instance_of`: instance-to-class hierarchy edges

The inspected assets show a clean provenance split at the base edge level:

- `uses` edges use `evidence_source = normalized_trace`
- `extends` and `instance_of` edges use `evidence_source = lean_meta_exact`

Representative counts:

- `lean4_example_typeclass_precise_v2`: `uses = 2755`, `instance_of = 959`, `extends = 19`
- `batteries_typeclass_precise_coverage_v1`: `uses = 20`, `instance_of = 4595`, `extends = 125`
- `mathlib_algebra_order_precise_coverage_index_v1`: `instance_of = 33402`, `extends = 1398`, no `uses`

### 4.2 relation provenance split assets

The repository already contains derived graph families and diagnostics for provenance-oriented views such as:

- `explicit-only`
- `synthesized-only`
- `mixed`

However, this provenance split is currently represented through derived asset families and diagnostics outputs, not through a first-class per-edge provenance field in the standard `edges.csv` schema. That is an unresolved semantic boundary for downstream tasks.

## 5. coverage-Aware Handling

coverage-aware handling remains mandatory for real hierarchy assets when relation endpoints would otherwise be missing from the declaration index.

Current rule of use:

- backfill recoverable endpoints
- keep unresolved items explicit
- do not coerce unresolved endpoints into negative labels

Observed representative behavior:

- `lean4_example_typeclass_precise_v2`
  - no `coverage_aware_backfill` block observed in `stats.json`
  - `skipped_exact_relation_rows_missing_nodes = 129`
  - consequence: some exact hierarchy rows were dropped because required nodes were absent
- `batteries_typeclass_precise_coverage_v1`
  - `coverage_aware_backfill.enabled = true`
  - `added_declarations = 4895`
  - `unresolved_names = 0`
  - consequence: relation endpoints were recovered aggressively before graph finalization
- `mathlib_algebra_order_precise_coverage_index_v1`
  - `coverage_aware_backfill.enabled = true`
  - `added_declarations = 27323`
  - `unresolved_names = 0`
  - consequence: the index graph is deliberately coverage-heavy and should be treated as a source pool for later module slicing, not as a simple small benchmark graph

## 6. Graph Families And recommended usage

| graph family | observed characteristics | recommended usage | not recommended usage |
| --- | --- | --- | --- |
| `lean4_example_typeclass_precise_v2` | small inspected graph with mixed `uses` + hierarchy edges; relation layer longest chain 4; some exact rows skipped due to missing nodes | protocol smoke tests, regression checks, grouped retrieval dry runs, small-scale baseline comparisons | sole evidence for broad geometry claims or final benchmark narrative |
| `lean4_example_typeclass_precise_v2_hierarchy_only` | hierarchy-only view; giant component only `95/1090`; tree-like and fragmented | hierarchy extraction audits, relation-only diagnostics, sanity checks for `extends` / `instance_of` behavior | standalone benchmark for retrieval quality |
| `plausible_typeclass_precise_v1` and `plausible_full_precise_v1` | very small assets; relation longest chain 1 in inspected diagnostics | historical comparison, pipeline smoke tests, debugging | default benchmark or stability claims |
| `batteries_typeclass_precise_coverage_v1` and related coverage views | coverage-aware repaired hierarchy; relation longest chain 4; giant component only `965/4956`; very shallow relation geometry | coverage-aware processing validation, provenance experiments, diagnostics on repaired real-repo graphs | default evidence for deep hierarchical retrieval or hyperbolic advantage |
| `batteries_full_precise_coverage_v1` and `full_with_uses` views | many extra `uses` edges on top of shallow hierarchy | dependency-rich diagnostics, ablations comparing full graph vs hierarchy-focused views | direct substitute for hierarchy benchmark graphs |
| `mathlib_algebra_order_precise_coverage_index_v1` | large relation index with coverage repair; no `uses`; many `instance_of` edges | source index for candidate module selection, module-level extraction, later benchmark curation | one-shot final benchmark graph without further filtering |
| `mathlib_order_focus_v1` candidate subgraphs such as `mathlib_algebra_order_ring_d4`, `mathlib_algebra_ring_subring_d4`, `mathlib_algebra_field_subfield_d4` | deeper relation chains around 10; materially richer hierarchy than current small-repo relation layers | next-round candidate benchmark families for grouped retrieval and grouped training alignment | immediate closure of the benchmark question before protocol and review work |

## 7. Known Limitations

### 7.1 unresolved version boundary

The following remain governed by `docs/data_manifest.md` and are still unresolved:

- exact Lean version for the `lean4-example` WSL trace snapshot
- exact Mathlib commit for the `lean4-example` WSL trace snapshot
- exact LeanDojo package version in the operational environment
- exact Python environment lock for model runs
- canonical version manifest for existing artifacts

### 7.2 unresolved schema boundary

The current standard graph roots do not yet guarantee:

- first-class provenance labels for `explicit-only / synthesized-only / mixed` on every edge row
- standardized `labels.csv` and `splits.csv` availability across all graph families
- a universal machine-readable distinction between benchmark-ready assets and diagnostic-only assets

### 7.3 structural limitation

Current diagnostics continue to show that many real relation layers are shallow or fragmented:

- `lean4_example` relation longest chain is 4
- `batteries` relation longest chain is 4 and giant component coverage is low
- candidate Mathlib module subgraphs are deeper, but they are still candidates rather than finalized default benchmarks

This limits what can honestly be claimed from current graph geometry.

## 8. Usage Rules

1. Cite both `docs/data_manifest.md` and this file when describing current dataset state.
2. Preserve `unknown / needs verification` items rather than inferring missing version facts from local snapshot strings.
3. Treat unresolved relation endpoints or provenance ambiguities as unresolved, not as reliable negatives.
4. Prefer module-level or reviewed typeclass/hierarchy assets for benchmark work; use full graphs and provenance variants mainly for diagnostics unless a later task formalizes them.
5. Do not describe `recommended usage` as a completion signal; benchmark promotion still requires later protocol and review tasks.
