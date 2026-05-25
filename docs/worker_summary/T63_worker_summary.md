# T63 Worker Summary

> **Handoff-facing explanatory aid.** This document is the T63 worker's self-report of changes made, verification results, and remaining risks. It is not a research artifact, does not introduce new claims or numbers, and is preserved in the repository to help future maintainers trace what T63 accomplished and what risks remain open.
>
> Status: T63 worker executed (ITP-targeted LaTeX conversion / core figure rendering).

## Task

**T63 (ITP-Targeted LaTeX Conversion And Core Figure Rendering)**

Goal: Turn the reviewed submission-facing paper assets into a single ITP-targeted LaTeX source tree and render the two core figures needed by the paper narrative.

## Changes Made

### 1. Created `paper/itp/main.tex` (primary output)

- **Document class**: LLNCS (`\documentclass[runningheads]{llncs}`) — available in TeX Live 2024 and accepted by ITP.
- **Structure**: 6 main sections (Introduction, Experimental Setup, Results, Discussion, Limitations, Conclusion) + Appendix (Evidence Chain, Numeric Anchors). Faithfully converts all sections from `docs/paper_draft.md`.
- **Tables**: 13 tables covering candidate graphs, provenance splits, structural properties, training config, baseline results, explicit_only results, hop-bucket analysis, synthesized_only results, reproducibility check, proof-side bridge, summary, evidence chain, and numeric anchors.
- **Figures**: 2 `\includegraphics` entries referencing `figures/F1_provenance_structure.png` and `figures/F2_hop_depth_delta.png`.
- **Bibliography**: Wired to `references.bib` using `splncs04.bst` (LLNCS standard).
- **Numeric values**: All frozen from reviewed T32/T33/T41/T42/T43 artifacts. No new numbers or claims introduced.
- **Compile result**: 17 pages, zero errors, zero float overflow warnings. Output: `paper/itp/main.pdf`.

### 2. Created `paper/itp/references.bib`

- 10 BibTeX entries covering all works cited in the paper: Poincaré embeddings, HGCN, Hyperbolic GCN (Chami et al.), DeepMath, TacticToe, LeanDojo, and related works.

### 3. Rendered `paper/itp/figures/F1_provenance_structure.png`

- **Spec source**: `docs/paper_figures_and_tables.md` Section 2 (Figure F1).
- **Data source**: T41 structural diagnostics (Table T4 values).
- **Chart type**: 3-panel grouped bar chart (one panel per provenance split: explicit_only, synthesized_only, hierarchy_mixed), each showing Field.Subfield and Order.Ring side by side for 3 properties (longest chain, multi-parent nodes, leaf ratio).
- **Visual message**: synthesized_only adds no depth, only leaves.
- Rendered with matplotlib 3.10.0 at 200 DPI.

### 4. Rendered `paper/itp/figures/F2_hop_depth_delta.png`

- **Spec source**: `docs/paper_figures_and_tables.md` Section 2 (Figure F2).
- **Data source**: T42 hop-bucket analysis (Table T3 values).
- **Chart type**: Line chart with markers. X-axis: hop_2, hop_3, hop_4_plus. Y-axis: MAP delta (HGCN − GCN). Two series: Field.Subfield and Order.Ring.
- **Annotations**: Value labels on each point, dagger marker on FS hop_4_plus (4/5 seeds footnote), horizontal dashed line at delta = 0.
- **Visual message**: HGCN advantage grows monotonically from hop_2 to hop_4_plus.
- Rendered with matplotlib 3.10.0 at 200 DPI.

### 5. Created `paper/itp/README.md`

Records:
- Template assumption (LLNCS, TeX Live 2024)
- Compile verification (17 pages, 0 errors)
- Source mapping (LaTeX section ↔ markdown section)
- Remaining 8 deltas to final submission bundle

### 6. Governance Sync (5 docs + venue plan)

| Document | Change |
| --- | --- |
| `docs/03_architecture.md` | Status line → "T63 worker executing"; Section 7 gaps updated |
| `docs/04_task_board.md` | Status line → "T63 worker executing"; T63 execution note added |
| `docs/05_decision_log.md` | Status line → "T63 worker executing"; D054 added (Pending Review) |
| `docs/07_handoff.md` | Status line → "T63 worker executing"; item 95 added; Section 8 updated |
| `docs/08_risks_and_open_questions.md` | Status line → "T63 worker executing" |
| `docs/venue_submission_plan.md` | Checklist items updated: LaTeX conversion, figure rendering, and bibliography marked [x] Done by T63 |

### 7. No Changes To (Forbidden Scope Compliance)

- `docs/paper_draft.md` — not modified
- `docs/paper_outline.md` — not modified
- `docs/paper_figures_and_tables.md` — not modified
- `docs/paper_artifact_package.md` — not modified
- `docs/02_experiment_plan.md` — not modified
- All files under `project_bootstrap/`, `data/`, `artifacts/` — not modified
- `docs/review/*.md` — not modified
- `.claude/settings.json` — not modified
- No new experiments, seed sweeps, traces, split generation, model training, or demos

## Verification Results

### LaTeX Compilation

```
cd paper/itp
pdflatex -interaction=nonstopmode main.tex   # pass 1
bibtex main                                    # bibliography
pdflatex -interaction=nonstopmode main.tex   # pass 2
pdflatex -interaction=nonstopmode main.tex   # pass 3
```

Result: **17 pages, 0 errors, 0 float overflow warnings**. Output file: `main.pdf` (434 KB).

### Verification Command

```
rg -n "documentclass|title|abstract|section|includegraphics|bibliography|ITP|R25|R30|F1|F2" paper/itp/main.tex paper/itp/README.md paper/itp/references.bib docs/03_architecture.md docs/04_task_board.md docs/05_decision_log.md docs/07_handoff.md docs/08_risks_and_open_questions.md docs/venue_submission_plan.md
```

All required patterns present:
- `\documentclass[runningheads]{llncs}` in main.tex
- `\includegraphics` for F1 and F2 in main.tex
- `\bibliography{references}` and `\bibliographystyle{splncs04}` in main.tex
- R25 and R30 references in main.tex (Limitations section)
- F1 and F2 descriptions in README.md
- Governance docs show "T63 worker executing"
- venue_submission_plan.md shows completed checklist items

### Section Structure

main.tex contains 6 `\section` commands and 18 `\subsection` commands, faithfully covering all sections from `docs/paper_draft.md`.

### Figure Rendering

- `F1_provenance_structure.png`: 72 KB, 200 DPI, 3-panel grouped bar chart
- `F2_hop_depth_delta.png`: 367 KB, 200 DPI, line chart with markers

## Remaining Risks (Unchanged)

- **R25 (Active)**: Clean-environment reproducibility not completed. All claims remain "reviewed single-environment evidence."
- **R30 (Active)**: 5 contributions may exceed ITP/CPP page budget. Current 17 pages fits within ITP's ~16-20 page range. C3 or C5 can compress to appendix if needed.
- **R08 (Active)**: Worker Allowed Files scope governance pattern. This task used 11 allowed files.
- **R34 (Active, per T63 task package)**: Not modified in this round.
