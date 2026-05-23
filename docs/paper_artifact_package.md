# Paper Artifact Package

> Status: Submission-facing packaging document — maps paper claims, tables, and figures to reviewed source documents.
>
> Created: 2026-05-23 (T58 worker)
>
> Purpose: Provide a single auditable document that records (1) which files are paper-facing source-of-truth, (2) which files are backing evidence, (3) the claim-to-source and table/figure-to-source mapping, (4) known exclusions and active boundaries, and (5) a submission/handoff checklist. This document does not introduce new numbers, claims, or conclusions.

---

## 1. Artifact Package Scope

This package covers all publication-facing assets that derive from reviewed T32/T33/T41/T42/T43/T50–T57 evidence. It does **not** cover:

- Binary submission assets (PDF, SVG, PNG, PPT) — to be generated during venue formatting
- Clean-environment reproduction (R25 remains active)
- Full Mathlib-scale validation
- Code-side artifact generation logic or build scripts

The package scope is: **document-level source-to-claim traceability for the paper draft and its supporting evidence.**

---

## 2. Source Documents Inventory

### 2.1 Paper-Facing Source-of-Truth Documents

These documents are the authoritative sources for their respective domains. Numbers, claims, and table/figure specs in the paper draft must trace to these documents.

| Document | Role | Frozen By |
| --- | --- | --- |
| `docs/paper_figures_and_tables.md` | Publication-facing figure/table source-of-truth. Contains exact numbers, captions, rendering specs, and cross-reference alignment for all core tables and figures. | T57 (reviewed PASS) |
| `docs/paper_draft.md` | Paper-facing draft. Inherits claim boundaries from `paper_outline.md` and reviewed evidence from T32–T43, T50–T52a. | T54 (PASS_WITH_WARNINGS), T55 (PASS_WITH_WARNINGS), T56 (PASS), T57 (PASS) |
| `docs/paper_outline.md` | Paper skeleton. Defines claim structure, contributions, evidence ladder, threats to validity, venue fit, and numeric anchors. | T50 (PASS_WITH_WARNINGS), T57 (synced R28/R29 status) |
| `docs/experiment_reports/provenance_summary.md` | Provenance split synthesis report. Primary evidence source for the provenance-conditional finding. | T43 (PASS), T56 (precision fix), T57 (granularity sync) |

### 2.2 Backing Evidence Documents

These documents provide the underlying experimental evidence that the source-of-truth documents reference. They are **not** edited during packaging; they are read-only references.

| Document | Role | Frozen By |
| --- | --- | --- |
| `docs/experiment_reports/gcn_grouped_training.md` | GCN grouped 5-seed sweep report (T32) | T32 (PASS) |
| `docs/experiment_reports/hgcn_grouped_training.md` | HGCN grouped 5-seed sweep report (T33) | T33 (PASS) |
| `docs/experiment_reports/grouped_training_summary.md` | Grouped-vs-binary summary (T34) | T34 (PASS) |
| `docs/experiment_reports/provenance_diagnostics.md` | Provenance split structural diagnostics (T41) | T41 (PASS) |
| `docs/experiment_reports/provenance_seed_sweeps.md` | Provenance-aware GCN/HGCN 5-seed sweeps (T42) | T42 (PASS) |
| `docs/experiment_reports/ancestor_explanation_demo_report.md` | Proof-side bridge demo report (T52a) | T52a (PASS) |
| `docs/grouped_retrieval_protocol.md` | Frozen grouped retrieval protocol (T12) | T12 (PASS) |
| `docs/provenance_split_protocol.md` | Frozen provenance split protocol (T40) | T40 (PASS) |
| `docs/diagnostics_protocol.md` | Heuristic diagnostics protocol (T22) | T22 (PASS) |
| `docs/training_alignment_audit.md` | Training alignment audit (T30) | T30 (PASS) |

### 2.3 Review Records

All reviews are stored in `docs/review/` and serve as audit trail. Key adversarial reviews: T12, T13, T31A, T31, T32, T33, T41, T42, T52a. Key milestone reviews: M3, T53.

---

## 3. Claim-to-Source Mapping

### C1: Reproducible Pipeline

- **Source**: `docs/paper_outline.md` Section 4 (C1), `docs/paper_draft.md` Section 4.1, `docs/grouped_retrieval_protocol.md`
- **Backing evidence**: T10 (version manifest), T11 (data card), T12–T14 (protocol freeze + hop bucket + smoke)
- **Review chain**: T10 PASS, T11 PASS, T12 PASS, T13 PASS, T14 PASS

### C2: Grouped Multi-Positive Ancestor Retrieval Protocol

- **Source**: `docs/paper_outline.md` Section 4 (C2), `docs/paper_draft.md` Section 4.4, `docs/grouped_retrieval_protocol.md`
- **Backing evidence**: T12 (protocol freeze), T13 (hop bucket), T31A (query-level split), T31 (grouped loss)
- **Review chain**: T12 PASS, T13 PASS, T31A PASS, T31 PASS

### C3: Graph Structure Diagnostics Framework

- **Source**: `docs/paper_outline.md` Section 4 (C3), `docs/paper_draft.md` Section 4.3, `docs/diagnostics_protocol.md`
- **Backing evidence**: T20–T22 (diagnostics + candidate selection + thresholds), T41 (provenance split structural diagnostics)
- **Review chain**: T20 PASS_WITH_WARNINGS, T21 PASS, T22 PASS, T41 PASS

### C4: Provenance-Conditional Hyperbolic Advantage Finding

- **Source**: `docs/paper_outline.md` Section 4 (C4), `docs/paper_draft.md` Sections 5.2–5.4, 5.7, `docs/paper_figures_and_tables.md` Tables T2, T3, T5 and Figure F2, `docs/experiment_reports/provenance_summary.md` Sections 4–7
- **Backing evidence**: T42 (provenance-aware 5-seed sweeps, 60 runs, zero failures), T41 (structural diagnostics per split), T32/T33 (hierarchy_mixed baseline)
- **Key numbers** (frozen, reviewed):
  - FS explicit_only HGCN MAP +0.1247 over GCN (T42)
  - OR explicit_only HGCN MAP +0.0557 over GCN (T42)
  - Hop-depth scaling: +0.03–0.05 (hop_2) → +0.25–0.27 (hop_4_plus) (T42)
  - FS synthesized_only GCN MAP 1.0000 ± 0.0000 (T42, verified by T56)
  - FS hop_4_plus based on 4/5 seeds (precision note)
- **Review chain**: T42 PASS, T43 PASS, T56 PASS (R28/R29 resolution), T57 PASS (figure/table source rendering)

### C5: Training Task Alignment Correction

- **Source**: `docs/paper_outline.md` Section 4 (C5), `docs/paper_draft.md` Sections 4.5–4.6, `docs/training_alignment_audit.md`
- **Backing evidence**: T30 (audit), T31A (query-level split), T31 (grouped loss), T32/T33 (matched sweeps)
- **Review chain**: T30 PASS, T31A PASS, T31 PASS, T32 PASS, T33 PASS

### Central Claim: Edge Provenance Composition Determines Geometry Preference

- **Source**: `docs/paper_outline.md` Section 3, `docs/paper_draft.md` Section 3.5, `docs/experiment_reports/provenance_summary.md` Section 7
- **Primary evidence**: C4 above (explicit_only = HGCN advantage; synthesized_only = GCN advantage; hierarchy_mixed = GCN advantage)
- **Mechanism**: Hop-bucket analysis confirms advantage scales with ancestor chain depth (Figure F2 / Table T3)
- **Controlled diagnostic**: synthesized_only confirms geometry-driven, not capacity artifact

---

## 4. Table/Figure-to-Source Mapping

### Core Tables (T1–T4)

| Paper Table | Source Doc Entry | Primary Data Source | Backing Evidence |
| --- | --- | --- | --- |
| Table T1 (hierarchy_mixed baseline) | `paper_figures_and_tables.md` Table T1 | T32 aggregate.json (GCN); T33 aggregate.json (HGCN, primary); T42 hierarchy_mixed sweeps (cross-check) | T32 PASS, T33 PASS, T42 PASS (exact match) |
| Table T2 (provenance-aware comparison) | `paper_figures_and_tables.md` Table T2 | T42 provenance sweep aggregate.json (12 sweep dirs) | T42 PASS |
| Table T3 (hop-bucket delta) | `paper_figures_and_tables.md` Table T3 | T42 aggregate.json → ranking.test.grouped.hop_buckets | T42 PASS |
| Table T4 (structural properties) | `paper_figures_and_tables.md` Table T4 | T41 provenance_split diagnostics | T41 PASS |

### Summary Table (T5)

| Paper Table | Source Doc Entry | Primary Data Source | Backing Evidence |
| --- | --- | --- | --- |
| Table T5 (provenance-conditional summary) | `paper_figures_and_tables.md` Table T5 | Synthesized from T1 and T2 | T42 PASS, T57 PASS |

### Core Figures

| Paper Figure | Source Doc Entry | Primary Data Source | Rendering Status |
| --- | --- | --- | --- |
| Figure F1 (provenance split / structure) | `paper_figures_and_tables.md` Figure F1 | T41 structural diagnostics | Spec ready; no binary rendering in this package |
| Figure F2 (hop-depth delta) | `paper_figures_and_tables.md` Figure F2 | T42 hop-bucket data | Spec ready; no binary rendering in this package |

### Supplementary Tables in Paper Draft

| Paper Section | Table Content | Source |
| --- | --- | --- |
| Section 4.1 | Candidate graph properties (nodes/edges) | `paper_draft.md` Section 4.1 |
| Section 4.2 | Provenance split design | `paper_draft.md` Section 4.2 |
| Section 5.2 | explicit_only per-metric comparison | `paper_figures_and_tables.md` Table T2 |
| Section 5.3 | Hop-bucket analysis | `paper_figures_and_tables.md` Table T3 |
| Section 5.4 | synthesized_only comparison | `paper_figures_and_tables.md` Table T2 |
| Section 5.5 | hierarchy_mixed reproduction | `paper_figures_and_tables.md` Table T1 |
| Section 5.7 | Provenance-conditional summary | `paper_figures_and_tables.md` Table T5 |

---

## 5. Known Exclusions and Active Boundaries

### Excluded from Current Package

1. **Binary figure rendering**: Figure F1 and F2 specs are ready in `paper_figures_and_tables.md`, but no PNG/SVG/PDF files are included. Rendering requires Python/LaTeX tooling in a subsequent venue-formatting step.
2. **Clean-environment reproduction (R25)**: All 60 provenance sweep runs and all Milestone 3 baseline runs were executed in a single environment. The evidence is reported as "reviewed single-environment runs," not "independently reproduced." This risk must not be written as closed.
3. **Full Mathlib validation**: The provenance-conditional finding is established on two candidate graphs (Field.Subfield: 133 nodes, Order.Ring: 253 nodes). Generalization to larger formal-math graphs requires further evidence.
4. **Cross-assistant transfer**: The provenance split semantics (`extends` = explicit, `instance_of` = synthesized) are Lean-specific. Other proof assistants have different hierarchy mechanisms.
5. **End-to-end theorem proving**: The proof-side bridge is a demonstration tool, not a theorem prover.

### Active Risks That Must Not Be Written as Closed

| Risk | Description | Status | Handling |
| --- | --- | --- | --- |
| R25 | Clean-environment reproducibility not completed | Active | Write "reviewed single-environment evidence," never "independently reproduced" |
| R30 | 5 contributions may exceed ITP/CPP page budget | Active | T59 decision: keep 5-contribution structure with page-budget-aware wording; C3 or C5 may relocate to appendix if needed |
| R08 | Worker Allowed Files scope governance pattern | Active | Future tasks must explicitly list all allowed files in the task package |

### Resolved Precision Items (for Reference)

| Item | Resolution | Closed By |
| --- | --- | --- |
| R28 | FS synthesized_only GCN "aggregate vs per-seed discrepancy" was metric naming confusion (`grouped_test_map` vs `test_average_precision`). Both metrics correct. | T56 (PASS) |
| R29 | FS synthesized_only GCN MAP table cell in provenance_summary.md corrected from HGCN copy-paste value to verified T42 value `1.0000 ± 0.0000`. | T56 (PASS) |
| D20 | provenance_summary.md Section 5 summary table granularity unified; paper_draft.md Section 5.4 compressed. | T57 (PASS) |
| D21 | paper_figures_and_tables.md Section 4 stale "Pending sync" rows corrected; Section 5.4 mechanistic detail decision recorded. | T58 (this task) |

---

## 6. Submission / Handoff Checklist

### Before Submission

- [ ] All numeric values in paper draft match `paper_figures_and_tables.md` exactly
- [ ] All tables and figures have captions that reference the correct source doc entries
- [ ] Figure F1 and F2 are rendered from specs in `paper_figures_and_tables.md`
- [ ] R25 wording check: no claim of "independently reproduced" anywhere in the paper
- [ ] R30 page budget check: contributions fit within target venue limits
- [ ] FS hop_4_plus footnote present (4/5 seeds)
- [ ] FS synthesized_only footnote present (flat star forest, trivially solvable)
- [ ] Metric naming clarification in Section 5.4 (or its absence is intentional)
- [ ] Abstract does not overclaim beyond provenance-conditional finding
- [ ] Non-claims section (Section 3.6) is intact and accurate

### Source Doc Consistency

- [x] `paper_figures_and_tables.md` cross-reference table (Section 4) matches actual `paper_outline.md` status
- [x] `paper_draft.md` Section 5.7 summary table matches `paper_figures_and_tables.md` Table T5
- [x] `provenance_summary.md` Section 7.2 summary table matches `paper_figures_and_tables.md` Table T5
- [x] `paper_outline.md` Section 12 numeric anchors match `paper_figures_and_tables.md` exact numbers
- [x] R28/R29 status is "resolved by T56" across all source docs

### Post-Submission Asset Tracking

- [ ] Binary figures (F1, F2) generated and cross-checked against source doc specs
- [ ] Supplementary materials packaged (if venue requires)
- [ ] Artifact evaluation bundle prepared (if venue requires)
- [ ] `.claude/settings.json` excluded from any commit

---

## 7. Section 5.4 Mechanistic Detail Decision

**Decision**: Restore one short mechanistic sentence.

**Rationale**: The compressed explanation in `paper_draft.md` Section 5.4 states "making retrieval trivial" but does not explain *why* it is trivial. A reviewer could reasonably ask why a flat star forest produces perfect MAP. Adding one sentence ("Each `(src, relation_type)` query has exactly one positive ancestor, and the candidate pool is small.") restores the mechanistic explanation without expanding back into the longer paragraph that T57 compressed. This does not introduce new numbers or new claims.

**What was added**: One sentence after "making retrieval trivial" in Section 5.4.

**What was not added**: No paragraph expansion, no new numbers, no reopening of R28/R29.

---

## 8. Source Documents Treated as Truth vs Backing Evidence

| Category | Documents | Treatment |
| --- | --- | --- |
| **Paper-facing source-of-truth** | `paper_figures_and_tables.md`, `paper_draft.md`, `paper_outline.md`, `provenance_summary.md` | Authoritative for their respective domains. Numbers here are frozen and must not be altered without re-running experiments. |
| **Backing evidence (experiment reports)** | `gcn_grouped_training.md`, `hgcn_grouped_training.md`, `grouped_training_summary.md`, `provenance_diagnostics.md`, `provenance_seed_sweeps.md`, `ancestor_explanation_demo_report.md` | Read-only references. These documents prove the provenance of the numbers in source-of-truth docs. |
| **Protocol/audit documents** | `grouped_retrieval_protocol.md`, `provenance_split_protocol.md`, `diagnostics_protocol.md`, `training_alignment_audit.md` | Frozen protocol definitions. These define the experimental methodology that the evidence was produced under. |
| **Review records** | `docs/review/*.md` | Audit trail. These verify that each piece of evidence was independently reviewed before being incorporated into source-of-truth docs. |
| **Governance documents** | `docs/00–08` | Project management and state tracking. These do not contain experimental numbers but record decision history and task progression. |
