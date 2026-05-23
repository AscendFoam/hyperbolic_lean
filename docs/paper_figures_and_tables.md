# Paper Figures and Tables Source Document

> Status: Publication-facing source-of-truth for figure/table rendering.
>
> Updated: 2026-05-23 (T57 worker draft)
>
> Purpose: Centralize all core figure and table specifications for the paper draft. Each entry records its intended placement, caption, exact data source, exact numbers, and rendering notes. This document is the single source that `docs/paper_draft.md`, `docs/paper_outline.md`, and `docs/experiment_reports/provenance_summary.md` should reference for figure/table content.

---

## 1. Core Tables

### Table T1: Full-Source-Graph Baseline (hierarchy_mixed)

- **Temporary ID**: Table 3 (per `paper_outline.md`)
- **Intended placement**: Paper Section 5.1 (Results: Milestone 3 Baseline)
- **Caption**: Grouped retrieval results on `hierarchy_mixed` (full source graph). GCN vs HGCN, 5-seed mean ± std. Training: sampled softmax, dim 16, negative_ratio 10.0, 100 epochs, patience 12.
- **Exact data source**:
  - GCN Field.Subfield: `artifacts/baselines/relation_seed_sweeps/grouped_gcn_field_subfield_t32/aggregate.json`
  - GCN Order.Ring: `artifacts/baselines/relation_seed_sweeps/grouped_gcn_order_ring_t32/aggregate.json`
  - HGCN Field.Subfield: `artifacts/baselines/relation_seed_sweeps/grouped_hgcn_field_subfield_t33/aggregate.json`
  - HGCN Order.Ring: `artifacts/baselines/relation_seed_sweeps/grouped_hgcn_order_ring_t33/aggregate.json`
  - Cross-validated by T42 hierarchy_mixed sweeps (byte-identical match confirmed in T42/T43)
- **Exact numbers**:

| Graph | GCN MAP | HGCN MAP | Delta | GCN nDCG | HGCN nDCG |
| --- | ---: | ---: | ---: | ---: | ---: |
| Field.Subfield | 0.4839 ± 0.0783 | 0.4458 ± 0.1150 | GCN +0.0381 | 0.6428 ± 0.0653 | 0.6095 ± 0.0908 |
| Order.Ring | 0.5789 ± 0.0346 | 0.5616 ± 0.0312 | GCN +0.0173 | 0.7293 ± 0.0340 | 0.7111 ± 0.0296 |

- **Rendering notes**: Delta column should use bold for the leading model. GCN leads on both graphs; this establishes the baseline that HGCN does not confer a general advantage on the full source graph.

---

### Table T2: Provenance-Aware Comparison (explicit_only and synthesized_only)

- **Temporary ID**: Table 4 (per `paper_outline.md`)
- **Intended placement**: Paper Section 5.2 + Section 5.4 (Primary Evidence + Controlled Diagnostic)
- **Caption**: Provenance-aware grouped retrieval results. GCN vs HGCN on `explicit_only` (primary evidence) and `synthesized_only` (controlled diagnostic). 5-seed mean ± std. Same training configuration as Table T1.
- **Exact data source**:
  - All values from T42 provenance-aware sweeps:
    - `artifacts/baselines/relation_seed_sweeps/provenance_gcn_field_subfield_explicit_only_t42/`
    - `artifacts/baselines/relation_seed_sweeps/provenance_hgcn_field_subfield_explicit_only_t42/`
    - `artifacts/baselines/relation_seed_sweeps/provenance_gcn_order_ring_explicit_only_t42/`
    - `artifacts/baselines/relation_seed_sweeps/provenance_hgcn_order_ring_explicit_only_t42/`
    - `artifacts/baselines/relation_seed_sweeps/provenance_gcn_field_subfield_synthesized_only_t42/`
    - `artifacts/baselines/relation_seed_sweeps/provenance_hgcn_field_subfield_synthesized_only_t42/`
    - `artifacts/baselines/relation_seed_sweeps/provenance_gcn_order_ring_synthesized_only_t42/`
    - `artifacts/baselines/relation_seed_sweeps/provenance_hgcn_order_ring_synthesized_only_t42/`
- **Exact numbers**:

**explicit_only (primary evidence):**

| Graph | GCN MAP | HGCN MAP | Delta | GCN nDCG | HGCN nDCG | GCN MRR | HGCN MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Field.Subfield | 0.5256 ± 0.0800 | 0.6503 ± 0.0481 | **HGCN +0.1247** | 0.6864 ± 0.0691 | 0.7696 ± 0.0435 | 0.5449 ± 0.1027 | 0.6738 ± 0.0588 |
| Order.Ring | 0.5836 ± 0.0978 | 0.6393 ± 0.0656 | **HGCN +0.0557** | 0.7332 ± 0.0725 | 0.7743 ± 0.0565 | 0.5888 ± 0.1472 | 0.7211 ± 0.0902 |

**synthesized_only (controlled diagnostic):**

| Graph | GCN MAP | HGCN MAP | Delta |
| --- | ---: | ---: | ---: |
| Field.Subfield | 1.0000 ± 0.0000 | 0.6857 ± 0.1140 | GCN +0.3143 |
| Order.Ring | 0.8453 ± 0.0295 | 0.7560 ± 0.0761 | GCN +0.0893 |

- **Rendering notes**:
  - Split into two sub-tables with clear labels: "primary evidence" and "controlled diagnostic".
  - Bold the winning model in the Delta column.
  - For FS synthesized_only GCN MAP = 1.0000: this is a trivially solvable flat star forest (longest chain = 1). No footnote about metric discrepancy needed — R28 is resolved (T56 audit confirmed `grouped_test_map` = 1.0 for all 5 seeds; the earlier "discrepancy" was a naming confusion between `grouped_test_map` and `test_average_precision`).
  - Include a single footnote: "Field.Subfield synthesized_only is a flat star forest (longest chain = 1, multi-parent = 0); GCN trivially achieves perfect MAP."

---

### Table T3: Hop-Bucket Delta on explicit_only

- **Temporary ID**: Table 5 (per `paper_outline.md`)
- **Intended placement**: Paper Section 5.3 (Hop-Bucket Analysis)
- **Caption**: Hop-bucket MAP comparison on `explicit_only`. HGCN advantage grows monotonically with ancestor chain depth. 5-seed mean ± std. *Field.Subfield hop_4_plus based on 4/5 seeds (seed 2026 produces no hop_4_plus queries; the missing seed is symmetric between GCN and HGCN).*
- **Exact data source**: Same T42 artifacts as Table T2; hop bucket fields from `aggregate.json` → `ranking.test.grouped.hop_buckets`
- **Exact numbers**:

**Field.Subfield explicit_only:**

| Bucket | GCN MAP | HGCN MAP | Delta |
| --- | ---: | ---: | ---: |
| hop_2 | 0.3403 ± 0.1295 | 0.3946 ± 0.1402 | +0.0543 |
| hop_3 | 0.2321 ± 0.1402 | 0.4050 ± 0.2321 | **+0.1729** |
| hop_4_plus* | 0.2774 ± 0.1002 | 0.5245 ± 0.1419 | **+0.2471** |

**Order.Ring explicit_only:**

| Bucket | GCN MAP | HGCN MAP | Delta |
| --- | ---: | ---: | ---: |
| hop_2 | 0.2347 ± 0.0352 | 0.2615 ± 0.1066 | +0.0268 |
| hop_3 | 0.2038 ± 0.0486 | 0.2989 ± 0.0958 | **+0.0951** |
| hop_4_plus | 0.4506 ± 0.1582 | 0.7214 ± 0.0264 | **+0.2708** |

- **Rendering notes**:
  - Bold deltas ≥ 0.15 to highlight the monotonic scaling pattern.
  - Footnote for FS hop_4_plus: "4/5 seeds; seed 2026 produces no hop_4_plus queries."
  - The key visual takeaway: HGCN advantage scales from ~+0.03–0.05 (hop_2) to ~+0.25–0.27 (hop_4_plus).
  - This table is the primary evidence for the "advantage scales with depth" claim (C4).

---

### Table T4: Structural Properties by Provenance Split

- **Temporary ID**: Table 6 (per `paper_outline.md`)
- **Intended placement**: Paper Section 4.3 (Experimental Setup: Structural Properties)
- **Caption**: Structural properties of candidate graphs by provenance split. `synthesized_only` graphs are flat star forests (longest chain = 1, multi-parent = 0, cycle rank = 0). All hierarchy depth comes from `explicit_only` edges.
- **Exact data source**: T41 structural diagnostics — `artifacts/diagnostics/provenance_split_t41/`
- **Exact numbers**:

| Property | FS explicit_only | FS synthesized_only | FS hierarchy_mixed | OR explicit_only | OR synthesized_only | OR hierarchy_mixed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Longest chain | 9 | 1 | 10 | 10 | 1 | 10 |
| Multi-parent nodes | 40 | 0 | 40 | 66 | 0 | 66 |
| Cycle rank | 32 | 0 | 32 | 60 | 0 | 60 |
| Leaf ratio | 0.124 | 0.537 | 0.278 | 0.208 | 0.656 | 0.502 |
| Delta/maxdist | 0.286 | 0.000 | — | 0.136 | 0.000 | — |
| Giant component ratio | 0.506 | — | — | 0.792 | — | — |

- **Rendering notes**:
  - Use shading or color to highlight that synthesized_only columns are uniformly "flat" (longest chain = 1, multi-parent = 0).
  - The key comparison is explicit_only vs synthesized_only: dramatic structural contrast.
  - `hierarchy_mixed` shows that adding synthesized edges inflates leaf ratio (0.124 → 0.278 for FS, 0.208 → 0.502 for OR) without adding depth.
  - Giant component ratio for synthesized_only is not meaningful (disconnected star fragments); use "—" or "n/a".

---

## 2. Core Figures

### Figure F1: Provenance Split / Structure Figure

- **Temporary ID**: Fig 2 (per `paper_outline.md`)
- **Intended placement**: Paper Section 4.3 or Section 5 (Results)
- **Caption**: Structural contrast across provenance splits. Left: `explicit_only` graphs exhibit genuine hierarchy depth (longest chain 9–10, multi-parent 40–66). Right: `synthesized_only` graphs are flat star forests (longest chain 1, multi-parent 0). Center: `hierarchy_mixed` inherits depth from explicit edges but gains leaf inflation from synthesized edges.
- **Exact data source**: Same T41 structural diagnostics as Table T4.
- **Qualitative encoding rule**: The figure should visually encode three structural dimensions:
  1. **Depth**: Longest chain (bar chart or heat strip, scale 0–10).
  2. **Branching**: Multi-parent nodes (bar chart, scale 0–70).
  3. **Leaf density**: Leaf ratio (bar chart, scale 0–1).
  Each dimension shown for all 6 provenance-split × candidate combinations. Color-code by provenance type (e.g., blue = explicit_only, red = synthesized_only, gray = hierarchy_mixed).
- **Rendering notes**:
  - A grouped bar chart with 3 groups (depth, branching, leaf ratio) × 2 candidates × 3 splits would work well.
  - Alternatively, a 3-panel figure: one panel per provenance split, each showing FS and OR side by side.
  - The visual message must be: "synthesized_only adds no depth, only leaves."
  - No binary rendering required this round; this spec is sufficient for subsequent LaTeX/Python rendering.

---

### Figure F2: Hop-Depth Delta Figure

- **Temporary ID**: Fig 3 (per `paper_outline.md`)
- **Intended placement**: Paper Section 5.3 (Hop-Bucket Analysis)
- **Caption**: HGCN vs GCN MAP delta on `explicit_only`, decomposed by hop depth. HGCN's advantage grows monotonically from hop_2 to hop_4_plus on both candidate graphs, confirming that hyperbolic geometry specifically benefits longer ancestor chains.
- **Exact data source**: Same T42 hop-bucket data as Table T3.
- **Exact numbers to encode**:

| Bucket | FS Delta | OR Delta |
| --- | ---: | ---: |
| hop_2 | +0.0543 | +0.0268 |
| hop_3 | +0.1729 | +0.0951 |
| hop_4_plus | +0.2471* | +0.2708 |

*FS hop_4_plus: 4/5 seeds.

- **Qualitative encoding rule**: Grouped bar chart or line chart. X-axis: hop buckets (hop_2, hop_3, hop_4_plus). Y-axis: MAP delta (HGCN − GCN). Two series: Field.Subfield and Order.Ring. Error bars from per-seed std (optional; the main message is monotonic growth).
- **Rendering notes**:
  - Line chart with markers may better convey the monotonic growth pattern than bars.
  - If bars are used, group by candidate graph (FS, OR) with 3 bars each.
  - Include a horizontal dashed line at delta = 0 as reference.
  - Footnote marker (*) on FS hop_4_plus for the 4/5 seed note.
  - This figure is the single most important visual for the C4 claim.

---

## 3. Summary Table (Paper Section 5.7)

### Table T5: Provenance-Conditional Conclusion Summary

- **Temporary ID**: Table in Section 5.7 (not separately numbered in outline)
- **Intended placement**: Paper Section 5.7 (Summary)
- **Caption**: Provenance-conditional model comparison across all three splits. Edge provenance composition determines which geometry is favored.
- **Exact data source**: Synthesized from Tables T1 and T2.
- **Exact numbers**:

| Provenance Split | HGCN vs GCN (FS MAP) | HGCN vs GCN (OR MAP) | Structural Role |
| --- | --- | --- | --- |
| `explicit_only` (primary) | **HGCN +0.1247** | **HGCN +0.0557** | Deep hierarchy |
| `synthesized_only` (diagnostic) | GCN +0.3143 | GCN +0.0893 | Flat star forest |
| `hierarchy_mixed` (reproducibility) | GCN +0.0381 | GCN +0.0173 | Depth + leaf inflation |

- **Rendering notes**:
  - Bold the winning model in each cell.
  - This table encodes the central claim in its most compact form.
  - FS synthesized_only GCN delta (+0.3143) now matches main table granularity (previously qualitative-only "GCN wins" in provenance_summary.md).

---

## 4. Cross-Reference Consistency

### Source doc → Paper draft alignment

| Source entry | Paper draft section | Current alignment status |
| --- | --- | --- |
| Table T1 | Section 5.1 | Aligned (numbers match) |
| Table T2 explicit_only | Section 5.2 | Aligned (numbers match) |
| Table T2 synthesized_only | Section 5.4 | Aligned (numbers match) |
| Table T3 | Section 5.3 | Aligned (numbers match) |
| Table T4 | Section 4.3 | Aligned (numbers match) |
| Table T5 | Section 5.7 | Aligned (numbers match) |
| Figure F1 | Section 4.3 or 5 | Spec ready for rendering |
| Figure F2 | Section 5.3 | Spec ready for rendering |

### Source doc → provenance_summary.md alignment

| Source entry | provenance_summary.md section | Current alignment status |
| --- | --- | --- |
| Table T2 synthesized_only | Section 5.1 main table | Aligned |
| Table T5 | Section 7.2 summary table | Synced (T57): FS synthesized_only delta unified from "GCN wins" to "GCN wins (+0.3143 MAP)" |

### Source doc → paper_outline.md alignment

| Source entry | paper_outline.md section | Current alignment status |
| --- | --- | --- |
| Section 6 Figures plan | Fig 2, Fig 3 | Pending sync: precision note for Table 4 must be updated (R28/R29 now resolved) |
| Section 6 Tables plan | Table 3–6 | Pending sync: precision note must be removed |

---

## 5. Numerical Precision Notes

1. **R28 (resolved)**: FS synthesized_only GCN `grouped_test_map` = 1.0 for all 5 seeds. The previously reported "aggregate vs per-seed discrepancy" was a naming confusion between `grouped_test_map` and `test_average_precision`. Both metrics are correct and internally consistent. Closed by T56 artifact audit.
2. **R29 (resolved)**: FS synthesized_only GCN MAP table cell in provenance_summary.md Section 5.1 was corrected from HGCN copy-paste value (0.6857) to verified T42 value (1.0000 ± 0.0000). Closed by T56.
3. **FS hop_4_plus (active precision note)**: Based on 4/5 seeds (seed 2026 produces no hop_4_plus queries). Comparison is symmetric. Must be footnoted in any publication.
4. **All numeric anchors are frozen**: Values come from reviewed T32/T33/T41/T42/T43 artifacts and must not be altered without re-running experiments.
