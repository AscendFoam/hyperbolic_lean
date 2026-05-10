# Data Manifest

> Updated: 2026-05-10
>
> Status: reviewed T10 manifest. Known unknowns remain intentionally labeled `unknown / needs verification`.

## Purpose

This manifest records the currently known version anchors, config entry points, and artifact roots for the traced formal-math graph pipeline. It is intentionally explicit about what is confirmed versus what is still `unknown / needs verification`.

## 1. Repository Snapshot

- Workspace repo: `hyperbolic_lean`
- Current repo commit: `b771a7c9802d6b650e5a36d0eae136a222d1ee04`
- Primary governance source of truth:
  - `docs/02_experiment_plan.md`
  - `docs/04_task_board.md`
  - `docs/06_eval_protocol.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`

## 2. Version Anchors

### 2.1 Lean

- Lean version for the small-target trace line: `v4.20.0`
  - Evidence:
    - `project_bootstrap/small_target_trace_package/README.md`
    - config names such as `trace_plausible_v420_small.json` and `trace_batteries_v420_small.json`
- Lean version for `traced_lean4_example_wsl`: `unknown / needs verification`
  - Reason: no single canonical version manifest is checked into the allowed files for that trace snapshot.

### 2.2 Mathlib

- `mathlib4` minimal / hierarchy-probe trace target commit: `c211948581bde9846a99e32d97a03f0d5307c31e`
  - Evidence:
    - `project_bootstrap/mathlib_minimal_trace_package/configs/trace_mathlib_algebra_order_minimal.json`
    - `project_bootstrap/next_traced_target_selection_package/configs/trace_mathlib_hierarchy_probe_v1.json`
- Mathlib version tag corresponding to the small-target route: `v4.20.0`
  - Evidence:
    - `project_bootstrap/small_target_trace_package/README.md`
- Mathlib commit used by `traced_lean4_example_wsl`: `unknown / needs verification`

### 2.3 LeanDojo / Tracing Tooling

- LeanDojo is the intended tracing toolchain for the trace pipeline.
  - Evidence:
    - `project_bootstrap/leandojo_graph_scaffold/README.md`
    - `project_bootstrap/leandojo_graph_scaffold/src/trace_repo_with_leandojo.py`
- Exact LeanDojo package version pinned in the current repo: `unknown / needs verification`
  - Reason: no checked-in requirements lock or environment manifest in the allowed files identifies an exact version.

### 2.4 Python Environment

- Baseline scaffold dependency recommendations:
  - `numpy`
  - `pandas`
  - `networkx`
  - `torch`
  - `torch_geometric`
  - `scikit-learn`
  - Evidence: `project_bootstrap/baseline_scaffold/requirements_baselines.txt`
- Exact Python version for the baseline environment: `unknown / needs verification`
- Exact conda environment definitions currently in-force: `unknown / needs verification`

## 3. Trace Targets And Commits

### 3.1 Small Target Trace Route

- `plausible`
  - repo: `https://github.com/leanprover-community/plausible`
  - commit: `2ac43674e92a695e96caac19f4002b25434636da`
  - config: `project_bootstrap/small_target_trace_package/configs/trace_plausible_v420_small.json`
  - output root: `data/raw/leandojo_trace/traced_plausible_v420_small`

- `batteries`
  - repo: `https://github.com/leanprover-community/batteries`
  - commit: `7a0d63fbf8fd350e891868a06d9927efa545ac1e`
  - config: `project_bootstrap/small_target_trace_package/configs/trace_batteries_v420_small.json`
  - output root: `data/raw/leandojo_trace/traced_batteries_v420_small`

- `lean4-example`
  - repo / commit are referenced in documentation, but no single T10-allowed config is the canonical source
  - version anchor: `unknown / needs verification`
  - current raw trace root: `data/raw/leandojo_trace/traced_lean4_example_wsl`

### 3.2 Mathlib Target Route

- `mathlib4` minimal algebra/order trace
  - repo: `https://github.com/leanprover-community/mathlib4`
  - commit: `c211948581bde9846a99e32d97a03f0d5307c31e`
  - config: `project_bootstrap/mathlib_minimal_trace_package/configs/trace_mathlib_algebra_order_minimal.json`
  - output root: `data/raw/leandojo_trace/traced_mathlib_minimal_wsl`

- `mathlib4` hierarchy probe
  - repo: `https://github.com/leanprover-community/mathlib4`
  - commit: `c211948581bde9846a99e32d97a03f0d5307c31e`
  - config: `project_bootstrap/next_traced_target_selection_package/configs/trace_mathlib_hierarchy_probe_v1.json`
  - output root: `data/raw/leandojo_trace/traced_mathlib_hierarchy_probe_v1`

## 4. Data Asset Layout

### 4.1 Raw Trace Roots

Currently present under `data/raw/leandojo_trace/`:

- `traced_batteries_v420_small`
- `traced_lean4_example_wsl`
- `traced_plausible_v420_small`

### 4.2 Intermediate Assets

Currently present under `data/interim/`:

- `inventories/`
- `normalized_trace/`
- `lean_meta_relations/`

Known precise hierarchy roots under `data/interim/lean_meta_relations/`:

- `batteries_precise_hierarchy_v1`
- `lean4_example_precise_hierarchy_v1`
- `mathlib_hierarchy_probe_v1`
- `plausible_precise_hierarchy_v1`

### 4.3 Processed Declaration Graph Assets

Representative processed graph roots under `data/processed/declaration_graph/`:

- `lean4_example_full_precise_v1`
- `lean4_example_typeclass_precise_v2`
- `lean4_example_typeclass_precise_v2_hierarchy_only`
- `plausible_full_precise_v1`
- `plausible_typeclass_precise_v1`
- `batteries_full_precise_coverage_v1`
- `batteries_typeclass_precise_coverage_v1`
- `batteries_hierarchy_only_precise_coverage_v1`
- `mathlib_hierarchy_probe_index_v1`
- `mathlib_algebra_order_precise_coverage_index_v1`

## 5. Config Index

This section lists the main config families that later tasks should treat as the current entry points, not an exhaustive dump of every JSON file.

### 5.1 Trace / Normalize / Graph Extraction

- LeanDojo scaffold:
  - `project_bootstrap/leandojo_graph_scaffold/configs/example_normalize_leandojo_xml_config.json`
  - `project_bootstrap/leandojo_graph_scaffold/configs/example_trace_config.json`
  - `project_bootstrap/leandojo_graph_scaffold/configs/example_full_precise_relation_graph_config.json`
- Small target trace package:
  - `project_bootstrap/small_target_trace_package/configs/trace_plausible_v420_small.json`
  - `project_bootstrap/small_target_trace_package/configs/trace_batteries_v420_small.json`
  - `project_bootstrap/small_target_trace_package/configs/normalize_plausible_v420_small.json`
  - `project_bootstrap/small_target_trace_package/configs/normalize_batteries_v420_small.json`
- Mathlib minimal / probe:
  - `project_bootstrap/mathlib_minimal_trace_package/configs/trace_mathlib_algebra_order_minimal.json`
  - `project_bootstrap/next_traced_target_selection_package/configs/trace_mathlib_hierarchy_probe_v1.json`
  - `project_bootstrap/next_traced_target_selection_package/configs/normalize_mathlib_hierarchy_probe_v1.json`

### 5.2 Baseline Training / Evaluation

- Baseline scaffold representative configs:
  - `project_bootstrap/baseline_scaffold/configs/node2vec_example.json`
  - `project_bootstrap/baseline_scaffold/configs/gcn_example.json`
  - `project_bootstrap/baseline_scaffold/configs/hyperbolic_example.json`
  - `project_bootstrap/baseline_scaffold/configs/relation_gcn_typeclass_precise_v2_parent_prediction.json`
  - `project_bootstrap/baseline_scaffold/configs/relation_hgcn_typeclass_precise_v2_parent_prediction.json`

### 5.3 Diagnostics / Candidate Selection

- Diagnostics package representative configs:
  - `project_bootstrap/graph_diagnostics_package/configs/graph_diagnostics_real_graphs_v1.json`
  - `project_bootstrap/graph_diagnostics_package/configs/graph_diagnostics_hierarchy_focus_v1.json`
  - `project_bootstrap/graph_diagnostics_package/configs/graph_diagnostics_mathlib_order_focus_v1.json`
  - `project_bootstrap/graph_diagnostics_package/configs/module_hierarchy_scan_batteries_v1.json`
  - `project_bootstrap/graph_diagnostics_package/configs/task_structure_relation_split_v1.json`

### 5.4 Mathlib Follow-Up Route

- Next traced target selection package representative configs:
  - `project_bootstrap/next_traced_target_selection_package/configs/filter_mathlib_algebra_order_hierarchy_probe_v1.json`
  - `project_bootstrap/next_traced_target_selection_package/configs/extract_mathlib_algebra_order_precise_coverage_v1.json`
  - `project_bootstrap/next_traced_target_selection_package/configs/module_hierarchy_scan_mathlib_algebra_order_precise_coverage_v1.json`

## 6. Artifact Index

### 6.1 Top-Level Artifact Buckets

Present under `artifacts/`:

- `baselines`
- `checkpoints`
- `diagnostics`
- `graphs`
- `inventories`
- `logs`
- `tmp_inventory_batteries`
- `tmp_inventory_plausible`
- `tmp_repo_probe`

### 6.2 Diagnostics Roots

Representative diagnostics roots under `artifacts/diagnostics/`:

- `real_graphs_v1`
- `hierarchy_focus_v1`
- `mathlib_order_focus_v1`
- `module_hierarchy_scan_batteries_v1`
- `module_hierarchy_scan_mathlib_algebra_order_index_v1`
- `relation_split_v1`
- `relation_split_comparison`
- `task_structure_relation_split_v1`
- `task_structure_mathlib_order_focus_v1`

### 6.3 Baseline Roots

Representative baseline roots under `artifacts/baselines/`:

- `node2vec_lean4_example_closed_world_v1`
- `gcn_lean4_example_default_protocol_v1`
- `hyperbolic_lean4_example_default_protocol_v1`
- `relation_gcn_lean4_example_full_precise_v1_parent_prediction_v1`
- `relation_hgcn_lean4_example_full_precise_v1_parent_prediction_v1`
- `relation_gcn_plausible_full_precise_parent_prediction_v1`
- `relation_hgcn_plausible_full_precise_parent_prediction_v1`
- `relation_gcn_mathlib_hierarchy_probe_algebra_order_parent_prediction_v1`
- `relation_hgcn_mathlib_hierarchy_probe_algebra_order_parent_prediction_v1`
- `relation_seed_sweeps/`

## 7. Known Unknowns

The following fields remain intentionally unresolved in this draft:

- exact Lean version for the `lean4-example` WSL trace snapshot
- exact Mathlib commit for the `lean4-example` WSL trace snapshot
- exact LeanDojo package version in the current operational environment
- exact Python version and full lockfile / conda spec for the active training environment
- canonical version manifest for already-produced `artifacts/` runs
- whether every currently present artifact directory was generated from the latest config revision or an earlier local variant

These should stay labeled `unknown / needs verification` until a later task confirms them from a reproducible environment manifest rather than inference.

## 8. Usage Rule

Until a stricter machine-readable manifest exists, later tasks should:

1. cite this file for the currently known version anchors
2. preserve `unknown / needs verification` labels instead of silently filling gaps
3. avoid upgrading tentative version guesses into facts without a reproducible source
