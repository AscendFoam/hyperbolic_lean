# Paper Outline

> Status: Draft skeleton — not yet submitted, not yet peer-reviewed.
>
> Updated: 2026-05-23 (T57 figure/table source rendering: R28/R29 resolved, source doc linked)

---

## 1. Working Title

**Provenance-Conditional Hyperbolic Graph Learning on Traced Formal-Math Hierarchies: Pipeline, Protocol, Diagnostics, and Evidence Boundaries**

Alternative short title: **When Does Hyperbolic Geometry Help on Real Formal-Math Graphs?**

## 2. One-Paragraph Positioning

We present a reproducible engineering pipeline that extracts real traced Lean/Mathlib hierarchy graphs, standardizes them into relation-aware benchmark tasks with grouped multi-positive retrieval protocol, and systematically diagnoses when and why hyperbolic graph neural networks (HGCN) might outperform Euclidean baselines (GCN). Our central finding is provenance-conditional: on the full source graph (containing both `extends` and `instance_of` edges), GCN remains the stronger model; HGCN's advantage emerges only on the explicit hierarchy layer (`extends` edges alone), where genuine depth and branching exist, and grows monotonically with ancestor chain depth. This finding reframes the question from "which geometry wins?" to "which edge provenance composition determines which geometry is favored" — a methodological contribution for future work on hierarchical graph learning in formal mathematics.

## 3. Central Claim

**Claim:** Edge provenance composition is a first-class experimental variable in formal-math hierarchy graph learning. On real traced Lean/Mathlib graphs, HGCN outperforms GCN only when the graph is restricted to explicit (`extends`) hierarchy edges; adding synthesized (`instance_of`) edges — which are structurally flat — dilutes the hierarchical signal enough to revert the comparison in GCN's favor.

### Non-Claims (Explicit Boundaries)

1. We do **not** claim that HGCN is generally superior to GCN on formal-math graphs.
2. We do **not** claim that the provenance-conditional finding generalizes beyond the two reviewed candidate graphs (Field.Subfield: 133 nodes, Order.Ring: 253 nodes).
3. We do **not** claim clean-room reproducibility has been fully closed; current evidence comes from reviewed single-environment runs.
4. We do **not** claim the pipeline covers full Mathlib or end-to-end theorem proving.
5. We do **not** claim the diagnostics thresholds are theoretically optimal; they are empirically calibrated heuristics from reviewed artifacts.

## 4. Paper Contributions

### C1: Reproducible Traced Formal-Math Hierarchy Graph Pipeline

A version-locked pipeline from Lean/Mathlib traced repositories through normalized traces, declaration graphs, precise hierarchy extraction, coverage-aware repair, and relation-aware subgraph construction. Includes version manifest, data card, and frozen configurations for every processing step.

### C2: Grouped Multi-Positive Ancestor Retrieval Protocol

Standardized evaluation protocol that replaces the legacy single-positive `ancestor_ranking` with grouped retrieval metrics (MAP, nDCG, nDCG@10, MRR, Recall@k) and hop-bucket analysis (hop_2, hop_3, hop_4_plus). The protocol mandates query-level split disjointness: all positives for the same `(src, relation)` query remain in the same split.

### C3: Graph Structure Diagnostics Framework

A diagnostic framework that characterizes formal-math graphs by longest chain, leaf ratio, component structure, multi-parent branching, cycle rank, and delta-hyperbolicity proxy. The framework includes heuristic thresholds for classifying graphs as shallow forest, star forest, or hierarchy-rich — and uses these to predict whether hyperbolic models are worth testing before running expensive sweeps.

### C4: Provenance-Conditional Hyperbolic Advantage Finding

The first empirical demonstration that edge provenance composition — not graph size or model capacity — determines whether hyperbolic geometry helps on real formal-math graphs. On `explicit_only` graphs (all genuine hierarchy depth), HGCN outperforms GCN (Field.Subfield MAP +0.1247, Order.Ring MAP +0.0557), with advantage growing monotonically with hop depth (+0.03 at hop_2 to +0.25 at hop_4_plus). On `hierarchy_mixed` (full source graph), GCN remains ahead.

### C5: Training Task Alignment Correction

The migration from binary edge classification training (BCEWithLogitsLoss) to query-grouped retrieval training (sampled softmax / InfoNCE-family loss), with training query keys explicitly aligned to evaluation query keys `(src_id, relation_type)`. This alignment is shown to be necessary but not sufficient for HGCN to outperform GCN — the provenance composition remains the decisive factor.

## 5. Evidence Ladder

| Milestone | Task | Evidence Provided | Role in Paper |
| --- | --- | --- | --- |
| M1: Data & Protocol Freeze | T10–T14 | Version manifest, data card, grouped retrieval protocol, hop-bucket reporting, smoke-verified output chain | Pipeline reproducibility (C1, C2) |
| M2: Diagnostics & Candidate Selection | T20–T22 | Structural diagnostics across real graphs, module-level candidate scan, heuristic diagnostics protocol with thresholds | Diagnostics framework (C3) |
| M3: Grouped Retrieval Training Alignment | T30–T34 | Training alignment audit, query-level split fix, matched GCN/HGCN grouped 5-seed sweeps, grouped-vs-binary comparison | Training alignment (C5), baseline establishment |
| M4: Relation Provenance Split | T40–T43 | Provenance split protocol, structural diagnostics per split, provenance-aware 5-seed sweeps, provenance-conditional synthesis | Provenance finding (C4), refined conclusion |

### Evidence Roles Within M4

- **`explicit_only` (primary evidence):** Isolates genuine hierarchy structure. HGCN outperforms GCN on both candidates across all primary metrics. This is the main evidence for the provenance-conditional hyperbolic advantage.
- **`synthesized_only` (controlled diagnostic):** Confirms HGCN's advantage on `explicit_only` is geometry-driven, not a capacity artifact. GCN matches or outperforms HGCN on these flat star-forest graphs (longest chain = 1, multi-parent = 0).
- **`hierarchy_mixed` (reproducibility check):** Results byte-identically reproduce T32/T33 from Milestone 3. GCN remains ahead on the full source graph, consistent with the original M3 conclusion.

### M3–M4 Relationship

T43 refines the Milestone 3 conclusion "GCN overall ahead, HGCN not established as stronger." The M3 conclusion remains correct for `hierarchy_mixed` (the full source graph). M4 does not overturn this; it adds the provenance dimension that was previously uncontrolled: the explicit hierarchy layer does favor HGCN, but this advantage is masked by the dominant flat synthesized layer in the mixed graph.

## 6. Figures and Tables Plan

### Figures

| ID | Content | Purpose |
| --- | --- | --- |
| Fig 1 | Pipeline overview: Lean repo → trace → declaration graph → precise hierarchy → coverage-aware repair → relation-aware subgraph → grouped retrieval evaluation | Show the end-to-end engineering contribution (C1) |
| Fig 2 | Graph structure diagnostic dashboard: longest chain, leaf ratio, component distribution across real graphs and provenance splits | Visualize diagnostics framework (C3) and the structural difference between `explicit_only` and `synthesized_only` |
| Fig 3 | Hop-bucket HGCN vs GCN comparison on `explicit_only`: delta MAP at hop_2, hop_3, hop_4_plus for both candidates | Demonstrate the monotonic scaling of hyperbolic advantage with depth (C4) |
| Fig 4 | Provenance-conditional summary: GCN vs HGCN MAP across all three splits × two candidates | Single visual encoding of the central claim (C4) |

### Tables

| ID | Content | Purpose |
| --- | --- | --- |
| Table 1 | Dataset summary: source repos, candidate graphs, node/edge counts, relation types, provenance composition | Ground the reader in data scale and scope |
| Table 2 | Protocol comparison: legacy single-positive vs grouped multi-positive retrieval (metrics, split semantics, training objective) | Show why the protocol upgrade matters (C2, C5) |
| Table 3 | Grouped retrieval 5-seed results on `hierarchy_mixed`: GCN vs HGCN, MAP/nDCG/nDCG@10/MRR, mean ± std for both candidates | Establish the M3 baseline that GCN leads on the full graph |
| Table 4 | Provenance-aware results: GCN vs HGCN on `explicit_only` and `synthesized_only`, same metrics | Present the primary evidence and controlled diagnostic (C4) |
| Table 5 | Hop-bucket analysis: per-bucket MAP delta (HGCN - GCN) on `explicit_only` | Show depth-dependent scaling (C4) |
| Table 6 | Structural properties by provenance split: longest chain, leaf ratio, multi-parent nodes, cycle rank, diameter | Connect structure to model performance (C3, C4) |
| Table 7 | Diagnostics thresholds: heuristic classification criteria for shallow forest / star forest / hierarchy-rich | Codify the diagnostics framework for reuse (C3) |

**Precision note for Table 4 (resolved):** Field.Subfield `synthesized_only` GCN MAP = 1.0000 ± 0.0000 (verified T42 artifact, all 5 seeds `grouped_test_map` = 1.0). A previously reported "aggregate vs per-seed discrepancy" (R28) was resolved by T56 as a metric naming confusion between `grouped_test_map` and `test_average_precision`; both metrics are correctly computed and internally consistent. A table-cell error in `provenance_summary.md` Section 5.1 (R29) was also corrected by T56. Detailed figure/table specs are now in `docs/paper_figures_and_tables.md`.

## 7. Threats to Validity

### Internal Validity

1. **Small graph scale.** Both reviewed candidates are small (133 and 253 nodes). The provenance-conditional finding is empirically established on these two graphs; statistical power for detecting interaction effects is limited. Generalization to larger formal-math graphs requires further evidence.
2. **Single-environment execution.** All sweeps ran in one environment. Clean-room reproducibility has not been independently verified. Clean-environment reproduction remains an open risk (R25).
3. **Hop_4_plus sample size.** On Field.Subfield `explicit_only`, hop_4_plus means are computed over 4 of 5 seeds (seed 2026 produces no hop_4_plus queries). The comparison is symmetric (both GCN and HGCN lack that seed), but statistical estimates at this bucket are less stable.
4. **Heuristic diagnostics thresholds.** The shallow-forest / star-forest / hierarchy-rich classification thresholds are empirically calibrated from current reviewed artifacts, not theoretically derived. They may not transfer to graphs with different size or topology distributions (R17).
5. **Metric naming precision in synthesized_only diagnostics (resolved).** Field.Subfield `synthesized_only` GCN shows `grouped_test_map` = 1.0 for all 5 seeds, while `test_average_precision` varies (0.81–1.00, aggregate 0.9426). A previously reported "aggregate vs per-seed discrepancy" (R28) was traced by T56 artifact audit to a naming confusion between these two metrics; both are correctly computed. The controlled-diagnostic conclusion is unaffected.

### External Validity

6. **Lean/Mathlib specificity.** The provenance split semantics (`extends` = explicit, `instance_of` = synthesized) are Lean-specific. Other proof assistants (Coq, Isabelle) have different hierarchy mechanisms; the provenance-conditional finding may not directly transfer.
7. **Limited task scope.** The paper covers ancestor retrieval and parent prediction only. Other proof-side tasks (premise retrieval, declaration recommendation, proof search) may exhibit different geometry preferences.
8. **Module-level subgraph selection.** The two candidates are manually selected subgraphs from Mathlib. The selection itself introduces a form of reporting bias, even though selection criteria are documented and reviewed.

### Construct Validity

9. **Grouped retrieval as proxy.** Ancestor retrieval quality is a proxy for downstream proof utility. Whether better retrieval translates to better proof assistance has not been demonstrated end-to-end.
10. **Hyperbolicity proxy.** The structural diagnostics use delta-hyperbolicity proxy and approximate metrics rather than exact hyperbolicity computation, which is intractable for larger graphs.

## 8. Venue Fit

### ITP (Interactive Theorem Proving) — Primary Target

- **Fit:** Strong. The paper directly serves the proof assistant community with real traced Lean/Mathlib graphs, hierarchy extraction tooling, and retrieval benchmarks.
- **Narrative angle:** "We built infrastructure for understanding and navigating formal-math hierarchies, and discovered that the question of which representation geometry works is answered by looking at edge provenance, not model architecture."
- **What to emphasize:** Pipeline engineering, protocol design, diagnostics for proof engineers, retrieval relevance to hierarchy navigation.
- **What to downplay:** Model architecture details; the contribution is methodology, not a new model.

### CPP (Certified Programs and Proofs) — Co-Primary Target

- **Fit:** Strong if framed as proof engineering infrastructure. CPP values tooling, artifact quality, and reproducible experimental packages.
- **Narrative angle:** "A reproducible proof-graph engineering pipeline with standardized evaluation, enabling systematic study of representation choices on real proof artifacts."
- **What to emphasize:** Artifact reproducibility, tool-level contributions, the pipeline as infrastructure for future proof-graph research.
- **What to add:** At least one proof-side utility demo (ancestor explanation or hierarchy navigation tool) to strengthen the tool/demo angle.

### FM (Formal Methods) — Stretch Target

- **Fit:** Moderate to strong if the paper achieves a complete story: data engineering, protocol correction, structural diagnosis, conditional model finding, and at least one downstream application.
- **Narrative angle:** "A systematic empirical study of how graph structure and edge provenance in formal methods artifacts interact with representation learning choices."
- **What to emphasize:** Completeness of the empirical methodology, the provenance-conditional finding as a methodological contribution, threats-to-validity analysis.
- **What to add before submission:** Multi-repository replication (beyond the current two Mathlib subgraphs), and a more complete benchmark/artifact package.

### Venue Prioritization

1. Prepare ITP/CPP version first (most natural community fit).
2. Expand to FM version if multi-repo replication and proof-side utility are completed.
3. Fall back to SEFM/ICFEM if additional evidence is needed.

### Page Budget Note

The five contributions (C1–C5) are scoped for ITP/CPP page limits (~20 pages). C3 or C5 can be condensed to appendix-level detail if budget pressure increases, but the current 5-contribution structure remains the default for venue submission.

## 9. Proof-Side Bridge

### Why T51 Must Extend the Paper Story to a Utility MVP

The paper skeleton above has a clear gap: while it demonstrates that graph representation quality depends on provenance composition, it does not yet show that this quality difference matters for any downstream proof-engineering task. Without at least one proof-side utility demonstration:

1. The paper risks being read as "an infrastructure paper without an application," which weakens the contribution at ITP and especially CPP.
2. The provenance-conditional finding remains abstract — readers cannot see what better retrieval enables in practice.
3. The bridge from graph representation to proof workflow remains hypothetical.

### Candidate Utility MVPs for T51

| Candidate | Proof-Side Contact | Complexity | Paper Fit |
| --- | --- | --- | --- |
| Ancestor explanation | Given a declaration, retrieve and rank its true ancestors with relation types; show which hierarchy paths contribute to its mathematical context | Low | Directly extends C2 (grouped retrieval) with a proof-exploration interface |
| Relation-aware declaration recommendation | Given a partially built import/extends chain, recommend the next relevant declaration | Medium | Extends C4 (provenance-conditional) with a navigation task |
| Premise retrieval demo | Use learned embeddings for informal theorem premise selection | High | Most ambitious but furthest from current pipeline |

The ancestor explanation MVP is recommended as the default choice for T51 because it (a) directly uses the already-reviewed grouped retrieval protocol, (b) makes the provenance-conditional finding tangible ("the quality of ancestor explanations depends on which edges you include"), and (c) can be demonstrated as a lightweight tool without requiring end-to-end theorem proving.

## 10. Provenance-Precision Boundaries for Paper Drafting

The following constraints must be respected until the corresponding risks are formally closed:

- **R28 (resolved by T56):** Field.Subfield `synthesized_only` GCN "aggregate vs per-seed discrepancy" was traced to metric naming confusion (`grouped_test_map` vs `test_average_precision`). Both metrics are correct. The table cell in this outline now uses the verified T42 value 1.0000 ± 0.0000.
- **R29 (resolved by T56):** The wrong GCN MAP table cell in `provenance_summary.md` Section 5.1 has been corrected to the verified T42 value 1.0000 ± 0.0000.
- **R25 (active):** Clean-environment reproducibility is not closed. Write "reviewed single-environment evidence," not "independently reproduced."
- **R04 (mitigated, provenance-conditional):** The hyperbolic advantage finding is conditional on provenance composition. Do not generalize it beyond the reviewed splits and candidate graphs.

## 11. Paper Structure (Draft Section Outline)

1. **Introduction** — Problem framing: formal-math hierarchies as graph learning targets; the gap between theoretical hyperbolic advantage and empirical evidence; why protocol and provenance matter.
2. **Background** — Lean/Mathlib hierarchy semantics; hyperbolic graph neural networks; ancestor retrieval as a task.
3. **Pipeline** (C1) — Tracing, extraction, normalization, coverage-aware repair, relation-aware subgraph construction.
4. **Protocol** (C2) — Grouped multi-positive retrieval; query-level split; hop-bucket analysis; metric suite.
5. **Diagnostics Framework** (C3) — Structural properties; heuristic classification; candidate selection criteria.
6. **Experiments** — Setup (candidates, hyperparameters, seeds); M3 baseline (Table 3); training alignment (C5); provenance split design.
7. **Results** (C4) — `explicit_only` primary evidence (Tables 4–5, Fig 3); `synthesized_only` controlled diagnostic; `hierarchy_mixed` reproducibility check (Tables 3, 4); provenance-conditional synthesis (Fig 4).
8. **Discussion** — Why provenance matters; implications for future formal-math graph work; relationship to broader hyperbolic GNN literature.
9. **Threats to Validity** — Internal, external, construct (Section 7 above).
10. **Related Work** — Formal-math graph datasets; hyperbolic embeddings; proof assistant tooling; graph-based retrieval.
11. **Conclusion** — Summary of contributions; provenance-conditional finding; proof-side bridge (Section 9).

## 12. Key Numeric Anchors (Reviewed, Not to Be Modified)

These values come from reviewed T32/T33/T42/T43 artifacts and must not be altered in the paper draft:

| Quantity | Value | Source |
| --- | --- | --- |
| GCN MAP, Field.Subfield `hierarchy_mixed` | 0.4839 ± 0.0783 | T32/T42 (exact match) |
| HGCN MAP, Field.Subfield `hierarchy_mixed` | 0.4458 ± 0.1150 | T33/T42 (exact match) |
| GCN MAP, Order.Ring `hierarchy_mixed` | 0.5789 ± 0.0346 | T32/T42 (exact match) |
| HGCN MAP, Order.Ring `hierarchy_mixed` | 0.5616 ± 0.0312 | T33/T42 (exact match) |
| GCN MAP, Field.Subfield `explicit_only` | 0.5256 ± 0.0800 | T42 |
| HGCN MAP, Field.Subfield `explicit_only` | 0.6503 ± 0.0481 | T42 |
| GCN MAP, Order.Ring `explicit_only` | 0.5836 ± 0.0978 | T42 |
| HGCN MAP, Order.Ring `explicit_only` | 0.6393 ± 0.0656 | T42 |
| Field.Subfield `explicit_only` hop_4_plus HGCN-GCN delta | +0.2471 (4/5 seeds) | T42 |
| Order.Ring `explicit_only` hop_4_plus HGCN-GCN delta | +0.2708 (5/5 seeds) | T42 |
| Field.Subfield `synthesized_only` longest chain | 1 | T41 |
| Order.Ring `synthesized_only` longest chain | 1 | T41 |
| Field.Subfield `explicit_only` longest chain | 9 | T41 |
| Order.Ring `explicit_only` longest chain | 10 | T41 |
