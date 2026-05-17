# Provenance Split Structural Diagnostics

> Task: T41
>
> Updated: 2026-05-17
>
> Purpose: Compare `explicit_only / synthesized_only / hierarchy_mixed` provenance-split graphs on structural diagnostics — depth, leaf ratio, connectivity, and hyperbolicity proxy — to understand what each provenance type contributes to hierarchy structure.

---

## 1. Edge Count Verification

All six provenance split outputs were generated using T40 frozen configs and verified against expected edge counts from `docs/provenance_split_protocol.md`:

| Source | Split | Expected Edges | Actual Edges | Match |
| --- | ---: | ---: | ---: | --- |
| Field.Subfield | explicit_only | 116 | 116 | yes |
| Field.Subfield | synthesized_only | 36 | 36 | yes |
| Field.Subfield | hierarchy_mixed | 152 | 152 | yes |
| Order.Ring | explicit_only | 180 | 180 | yes |
| Order.Ring | synthesized_only | 120 | 120 | yes |
| Order.Ring | hierarchy_mixed | 300 | 300 | yes |

All edge counts match the protocol's expected values.

## 2. hierarchy_mixed Identity Verification

The protocol states that `hierarchy_mixed` should be identical to the full source graph because neither candidate contains `uses` edges. This was verified programmatically:

| Source | Source Nodes | Mixed Nodes | Source Edges | Mixed Edges | Identity |
| --- | ---: | ---: | ---: | ---: | --- |
| Field.Subfield | 133 | 133 | 152 | 152 | confirmed |
| Order.Ring | 253 | 253 | 300 | 300 | confirmed |

**Note**: This identity holds because the current candidate graphs contain only `extends` and `instance_of` edges and no `uses` edges. It is a factual observation about the current data, not a logical invariant — if future source graphs include `uses` edges, `hierarchy_mixed` will be a strict subset of the full graph.

## 3. Overview Comparison

| graph | nodes | edges | giant component ratio | cycle rank | diameter est. | delta/maxdist |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **Field.Subfield** | | | | | | |
| explicit_only | 89 | 116 | 0.506 | 32 | 7 | 0.286 |
| synthesized_only | 67 | 36 | 0.060 | 0 | 2 | 0.000 |
| hierarchy_mixed | 133 | 152 | 0.406 | 32 | 8 | 0.250 |
| **Order.Ring** | | | | | | |
| explicit_only | 125 | 180 | 0.792 | 60 | 12 | 0.125 |
| synthesized_only | 183 | 120 | 0.044 | 0 | 2 | 0.000 |
| hierarchy_mixed | 253 | 300 | 0.747 | 60 | 12 | 0.125 |

Key observations:
- The `cycle_rank` and `diameter_estimate` for `hierarchy_mixed` are identical to `explicit_only` in both sources. The synthesized edges do not add cycle rank or diameter.
- `synthesized_only` has cycle rank 0 and diameter 2 in both sources — it is structurally flat.
- Giant component ratio drops from explicit_only to hierarchy_mixed (Field.Subfield: 0.506 → 0.406) because synthesized edges introduce many small, disconnected star-like components.

## 4. Relation Layer Comparison

| graph | relation nodes | relation edges | longest chain | multi-parent | roots | leaves | leaf ratio | delta/maxdist (relation) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Field.Subfield** | | | | | | | | |
| explicit_only | 89 | 116 | 9 | 40 | 28 | 11 | 0.124 | 0.286 |
| synthesized_only | 67 | 36 | 1 | 0 | 31 | 36 | 0.537 | 0.000 |
| hierarchy_mixed | 133 | 152 | 10 | 40 | 36 | 37 | 0.278 | 0.125 |
| **Order.Ring** | | | | | | | | |
| explicit_only | 125 | 180 | 10 | 66 | 32 | 26 | 0.208 | 0.136 |
| synthesized_only | 183 | 120 | 1 | 0 | 63 | 120 | 0.656 | 0.000 |
| hierarchy_mixed | 253 | 300 | 10 | 66 | 40 | 127 | 0.502 | 0.143 |

Key observations:
- **Longest chain**: `explicit_only` has chains of length 9 (Field.Subfield) and 10 (Order.Ring). `synthesized_only` has longest chain = 1 in both — all `instance_of` edges are single-hop, no chaining. `hierarchy_mixed` inherits the explicit chain depth (10) and gains at most +1 from mixing.
- **Multi-parent count**: `synthesized_only` has 0 multi-parent nodes in both sources. All multi-parent structure comes from `explicit_only`.
- **Leaf ratio**: `synthesized_only` has very high leaf ratios (0.537 and 0.656) — most nodes are leaves with no outgoing edges. Adding synthesized edges to the mixed graph inflates the leaf ratio (Field.Subfield: 0.124 → 0.278; Order.Ring: 0.208 → 0.502).
- **Hyperbolicity proxy**: `synthesized_only` has delta/maxdist = 0.000 (perfectly tree-like because the graph is flat). `explicit_only` has moderate values (0.286 and 0.136). `hierarchy_mixed` is similar to or slightly lower than `explicit_only`.

## 5. Structural Interpretation

### 5.1 Synthesized edges are structurally flat

The `instance_of` edges form a disconnected collection of star-like micro-components:
- No chaining (longest chain = 1).
- No multi-parent nodes (all `instance_of` edges point from a unique instance to a single class).
- Cycle rank = 0, diameter = 2.
- Hyperbolicity proxy = 0.000.

These edges encode type-class instance registrations, not hierarchical inheritance. They do not contribute depth or tree-like structure that hyperbolic models could exploit.

### 5.2 Explicit edges carry all hierarchy depth

The `extends` edges carry the full hierarchical signal:
- Longest chains of 9–10.
- Multi-parent nodes 40–66, reflecting genuine class/structure inheritance with multiple parents.
- Non-trivial cycle rank and moderate hyperbolicity proxy.
- Good giant component ratios (0.506 and 0.792).

### 5.3 Mixing dilutes structure

Adding synthesized edges to form `hierarchy_mixed` does not add structural depth — it only adds:
- Extra leaf nodes (Field.Subfield: leaves 11 → 37; Order.Ring: leaves 26 → 127).
- Smaller disconnected components (Field.Subfield: 5 → 13 components).
- Higher leaf ratio (Field.Subfield: 0.124 → 0.278; Order.Ring: 0.208 → 0.502).

The longest chain, cycle rank, and multi-parent count remain dominated by the explicit edges.

### 5.4 Implications for hyperbolic advantage

If `synthesized_only` edges are structurally flat, then:
1. A model trained on `synthesized_only` graphs would be solving a nearly trivial retrieval task with no meaningful hierarchy.
2. Adding synthesized edges to the mixed graph inflates leaf ratio and fragmentation, making the overall graph appear more star-like — which is precisely the structure where hyperbolic models offer least advantage.
3. The question "do synthesized edges dilute hyperbolic advantage?" has a clear structural answer: **yes, they dilute the hierarchical signal by adding flat, non-chaining edges that inflate leaf ratio and fragmentation without adding depth.**

This structural finding is consistent with T32/T33's empirical observation that HGCN did not establish advantage over GCN on the mixed graphs.

## 6. Diagnostics Protocol Classification

Applying the heuristic thresholds from `docs/diagnostics_protocol.md`:

| graph | longest chain | leaf ratio | classification |
| --- | ---: | ---: | --- |
| Field.Subfield explicit_only | 9 | 0.124 | non-shallow, moderate hierarchy |
| Field.Subfield synthesized_only | 1 | 0.537 | shallow star forest |
| Field.Subfield hierarchy_mixed | 10 | 0.278 | non-shallow, moderate leaf inflation |
| Order.Ring explicit_only | 10 | 0.208 | non-shallow, good hierarchy |
| Order.Ring synthesized_only | 1 | 0.656 | shallow star forest |
| Order.Ring hierarchy_mixed | 10 | 0.502 | non-shallow depth, but high leaf ratio |

- `synthesized_only` graphs are classified as **shallow star forests** by the diagnostics protocol (longest_chain <= 3 AND leaf_ratio >= 0.50).
- `explicit_only` graphs are the best structural candidates for testing hyperbolic advantage: deepest chains, lowest leaf ratios, most multi-parent branching.
- `hierarchy_mixed` has depth from explicit edges but leaf ratio inflation from synthesized edges.

## 7. Artifacts

- Provenance split output: `data/processed/declaration_graph/mathlib_{field_subfield,order_ring}_v1_{explicit_only,synthesized_only,hierarchy_mixed}/`
- Diagnostics artifacts: `artifacts/diagnostics/provenance_split_t41/`
- T40 frozen configs: `project_bootstrap/leandojo_graph_scaffold/configs/provenance_split_*_t40.json`
- T41 diagnostics config: `project_bootstrap/graph_diagnostics_package/configs/graph_diagnostics_provenance_split_t41.json`

## 8. Commands Used

```bash
# Generate provenance split graphs
python project_bootstrap/leandojo_graph_scaffold/src/split_relations_by_provenance.py \
    --config project_bootstrap/leandojo_graph_scaffold/configs/provenance_split_field_subfield_t40.json

python project_bootstrap/leandojo_graph_scaffold/src/split_relations_by_provenance.py \
    --config project_bootstrap/leandojo_graph_scaffold/configs/provenance_split_order_ring_t40.json

# Run structural diagnostics
python project_bootstrap/baseline_scaffold/src/run_graph_diagnostics.py \
    --config project_bootstrap/graph_diagnostics_package/configs/graph_diagnostics_provenance_split_t41.json
```
