# Batteries Real Trace Execution Package

This document packages the first real `batteries` pipeline in the same style as the completed `plausible` experiment:

`trace -> inventory -> normalize -> closed-world graph -> precise hierarchy export -> precise subgraph extraction -> relation-aware GCN/HGCN`

The goal of this round is not to maximize model performance immediately. The goal is to test whether `batteries` can provide richer internal `extends` structure than `plausible`, while keeping the engineering path controlled and reproducible.

## 1. Fixed Inputs

- Repo: `https://github.com/leanprover-community/batteries`
- Commit: `7a0d63fbf8fd350e891868a06d9927efa545ac1e`
- Trace config:
  - `project_bootstrap/small_target_trace_package/configs/trace_batteries_v420_small.json`
- Root module for Lean-side export:
  - `Batteries`
- Trace policy:
  - `build_deps = false`
  - `num_procs = 2`

## 2. Expected Output Paths

- Raw trace:
  - `data/raw/leandojo_trace/traced_batteries_v420_small`
- Trace inventory:
  - `artifacts/logs/batteries_trace_inventory_v1`
- Normalized trace:
  - `data/interim/normalized_trace/batteries_normalized_declarations_from_xml_v1.jsonl`
- Declaration index:
  - `data/interim/normalized_trace/batteries_declaration_index.tsv`
- Precise hierarchy export:
  - `data/interim/lean_meta_relations/batteries_precise_hierarchy_v1`
- Closed-world graph:
  - `data/processed/declaration_graph/batteries_closed_world_v1`
- Full precise graph:
  - `data/processed/declaration_graph/batteries_full_precise_v1`
- Typeclass precise graph:
  - `data/processed/declaration_graph/batteries_typeclass_precise_v1`

## 3. Step A: Run Real Trace In WSL

Run this from Windows PowerShell at repo root:

```powershell
wsl bash /mnt/d/Codes/Math/hyperbolic_lean/project_bootstrap/small_target_trace_package/scripts/run_wsl_trace.sh `
  /mnt/d/Codes/Math/hyperbolic_lean/project_bootstrap/small_target_trace_package/configs/trace_batteries_v420_small.json
```

What should happen:

- LeanDojo clones `batteries`
- tracing runs with `NUM_PROCS=2`
- output repo appears at:
  - `data/raw/leandojo_trace/traced_batteries_v420_small/batteries`

If tracing fails, do not continue to later steps. First inspect:

- Lean build errors
- missing toolchain / `lake`
- OOM or long-running worker issues

## 4. Step B: Inventory The Raw Trace

Run after trace completes:

```powershell
$env:PYTHONPATH='project_bootstrap/leandojo_graph_scaffold/src'
& 'C:\ProgramData\anaconda3\envs\DLEnv\python.exe' `
  'project_bootstrap/leandojo_graph_scaffold/src/inventory_trace_dir.py' `
  --trace-root 'data/raw/leandojo_trace/traced_batteries_v420_small' `
  --output-root 'artifacts/logs/batteries_trace_inventory_v1'
```

Minimum sanity checks:

- `*.trace.xml` files exist
- traced repo contains `.git`
- traced repo contains `.lake/build`

If there are no XML trace files, stop here and inspect the traced repo layout before normalization.

## 5. Step C: Normalize XML Trace

```powershell
$env:PYTHONPATH='project_bootstrap/leandojo_graph_scaffold/src'
& 'C:\ProgramData\anaconda3\envs\DLEnv\python.exe' `
  'project_bootstrap/leandojo_graph_scaffold/src/normalize_leandojo_trace.py' `
  --config 'project_bootstrap/small_target_trace_package/configs/normalize_batteries_v420_small.json'
```

Files produced:

- `data/interim/normalized_trace/batteries_normalized_declarations_from_xml_v1.jsonl`
- `artifacts/logs/batteries_normalize_trace_xml_v1_skips.json`

Immediate checks:

- normalized file is non-empty
- `decl_kind` distribution includes some `class` / `structure` / `instance`
- no obvious collapse to only a few modules

## 6. Step D: Build Closed-World Declaration Graph

```powershell
$env:PYTHONPATH='project_bootstrap/leandojo_graph_scaffold/src'
& 'C:\ProgramData\anaconda3\envs\DLEnv\python.exe' `
  'project_bootstrap/leandojo_graph_scaffold/src/extract_decl_graph.py' `
  --config 'project_bootstrap/small_target_trace_package/configs/extract_batteries_closed_world_v1.json'
```

Files produced under:

- `data/processed/declaration_graph/batteries_closed_world_v1`

Key stats to inspect:

- `num_declarations`
- `num_edges`
- `decl_kind_counts`
- whether the graph is still reasonably dense after closed-world filtering

## 7. Step E: Export Precise Hierarchy In WSL

Run inside the traced repo root:

```powershell
wsl
cd /mnt/d/Codes/Math/hyperbolic_lean/data/raw/leandojo_trace/traced_batteries_v420_small/batteries
export PATH="$HOME/.elan/bin:$PATH"
lake env lean --run /mnt/d/Codes/Math/hyperbolic_lean/project_bootstrap/leandojo_graph_scaffold/lean/ExportPreciseHierarchy.lean Batteries /mnt/d/Codes/Math/hyperbolic_lean/data/interim/lean_meta_relations/batteries_precise_hierarchy_v1
lake env lean --run /mnt/d/Codes/Math/hyperbolic_lean/project_bootstrap/leandojo_graph_scaffold/lean/ExportDeclarationIndex.lean Batteries /mnt/d/Codes/Math/hyperbolic_lean/data/interim/normalized_trace/batteries_declaration_index.tsv
```

Expected outputs:

- `data/interim/lean_meta_relations/batteries_precise_hierarchy_v1/nodes.tsv`
- `data/interim/lean_meta_relations/batteries_precise_hierarchy_v1/relations.tsv`
- `data/interim/normalized_trace/batteries_declaration_index.tsv`

Important note:

- The current Lean exporters already use `loadExts := true`.
- This is necessary. Without it, `isClass` / `Meta.isInstance` can silently fail.

## 8. Step F: Extract Precise Subgraphs

### Full precise graph

```powershell
$env:PYTHONPATH='project_bootstrap/leandojo_graph_scaffold/src'
& 'C:\ProgramData\anaconda3\envs\DLEnv\python.exe' `
  'project_bootstrap/leandojo_graph_scaffold/src/extract_typeclass_subgraph.py' `
  --config 'project_bootstrap/small_target_trace_package/configs/extract_batteries_full_precise_v1.json'
```

### Typeclass precise graph

```powershell
$env:PYTHONPATH='project_bootstrap/leandojo_graph_scaffold/src'
& 'C:\ProgramData\anaconda3\envs\DLEnv\python.exe' `
  'project_bootstrap/leandojo_graph_scaffold/src/extract_typeclass_subgraph.py' `
  --config 'project_bootstrap/small_target_trace_package/configs/extract_batteries_typeclass_precise_v1.json'
```

Key files to inspect:

- `data/processed/declaration_graph/batteries_full_precise_v1/stats.json`
- `data/processed/declaration_graph/batteries_typeclass_precise_v1/stats.json`

Main go/no-go criteria:

- `exact_extends_edge_count` is meaningfully above `lean4-example`'s `19`
- `instance_of` remains non-trivial
- matched precise relations are not mostly dropped during join

## 9. Step G: First Baseline Runs

### Full precise GCN

```powershell
$env:PYTHONPATH='project_bootstrap/baseline_scaffold/src'
& 'C:\ProgramData\anaconda3\envs\DLEnv\python.exe' `
  'project_bootstrap/baseline_scaffold/src/run_relation_gcn_baseline.py' `
  --config 'project_bootstrap/small_target_trace_package/configs/relation_gcn_batteries_full_precise_parent_prediction_v1.json'
```

### Full precise HGCN

```powershell
$env:PYTHONPATH='project_bootstrap/baseline_scaffold/src'
& 'C:\ProgramData\anaconda3\envs\DLEnv\python.exe' `
  'project_bootstrap/baseline_scaffold/src/run_relation_hyperbolic_baseline.py' `
  --config 'project_bootstrap/small_target_trace_package/configs/relation_hgcn_batteries_full_precise_parent_prediction_v1.json'
```

### Typeclass precise GCN

```powershell
$env:PYTHONPATH='project_bootstrap/baseline_scaffold/src'
& 'C:\ProgramData\anaconda3\envs\DLEnv\python.exe' `
  'project_bootstrap/baseline_scaffold/src/run_relation_gcn_baseline.py' `
  --config 'project_bootstrap/small_target_trace_package/configs/relation_gcn_batteries_typeclass_precise_parent_prediction_v1.json'
```

### Typeclass precise HGCN

```powershell
$env:PYTHONPATH='project_bootstrap/baseline_scaffold/src'
& 'C:\ProgramData\anaconda3\envs\DLEnv\python.exe' `
  'project_bootstrap/baseline_scaffold/src/run_relation_hyperbolic_baseline.py' `
  --config 'project_bootstrap/small_target_trace_package/configs/relation_hgcn_batteries_typeclass_precise_parent_prediction_v1.json'
```

## 10. Recommended Interpretation Order

Use the outputs in this order:

1. Compare `batteries_closed_world_v1` size to `plausible_closed_world_v1`
2. Check whether `batteries_precise_hierarchy_v1` contains meaningful internal `extends`
3. Compare `batteries_full_precise_v1` and `batteries_typeclass_precise_v1`
4. Only then interpret GCN vs HGCN

This avoids over-reading model differences before confirming that the graph actually contains the hierarchy signal we are looking for.

## 11. Success Criteria For This Round

This round is successful if at least the following hold:

1. The full real pipeline runs end-to-end on `batteries`
2. Internal exact `extends` is clearly richer than in `plausible`
3. The precise join does not collapse most relations
4. At least one of `full precise` or `typeclass precise` is large enough to support stable `parent_prediction`

## 12. Failure Branches

If `batteries` still yields very few internal `extends`:

1. keep the real pipeline as validated
2. do not over-invest in more HGCN tuning on this repo
3. move to a more targeted module-level or Mathlib-subset hierarchy trace

If trace cost is too high:

1. preserve the trace inventory and failure logs
2. reduce ambition to module-level experiments
3. only return to larger real traces after the next gate decision
