# ITP-Targeted LaTeX Source Tree

## Template Assumption

This LaTeX source uses the **LLNCS** (Springer Lecture Notes in Computer Science) document class, which is available in TeX Live 2024 and is accepted by ITP.

- Document class: `llncs` (runningheads option)
- Bibliography style: `splncs04.bst` (bundled with LLNCS)
- Compile command: `pdflatex main && bibtex main && pdflatex main && pdflatex main`

ITP has used both LLNCS and LIPIcs in different years. If the CFP specifies LIPIcs, change `\documentclass[runningheads]{llncs}` to `\documentclass{lipics}` and adjust the preamble accordingly.

## Compile Verification

Compiled locally with **TeX Live 2024** on Windows 11:

```powershell
cd paper/itp
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Result: **17 pages**, zero errors, output `main.pdf` generated successfully.

Page budget: ITP typically allows ~16-20 pages. The current 17 pages fit within this range. If compression is needed, C3 (diagnostics framework) or C5 (training alignment) can be shortened.

## Source Mapping

The LaTeX source is a faithful conversion of `docs/paper_draft.md` (T58 reviewed version):

| LaTeX Section | Markdown Source Section |
| --- | --- |
| Section 1 (Introduction) | Sections 3.1–3.7 |
| Section 2 (Experimental Setup) | Section 4 |
| Section 3 (Results) | Section 5 |
| Section 4 (Discussion) | Section 6 |
| Section 5 (Limitations) | Section 7 |
| Section 6 (Conclusion) | Section 8 |
| Appendix A (Evidence Chain) | Appendix A |

All numeric values are frozen from reviewed T32/T33/T41/T42/T43 artifacts. No new numbers or claims were introduced during conversion.

## Figures

- `figures/F1_provenance_structure.png`: Grouped bar chart showing structural properties (longest chain, multi-parent nodes, leaf ratio) across provenance splits for both candidate graphs. Rendered from specs in `docs/paper_figures_and_tables.md` Section 2 (Figure F1). Data source: T41 structural diagnostics.
- `figures/F2_hop_depth_delta.png`: Line chart showing HGCN vs GCN MAP delta on `explicit_only`, decomposed by hop depth. Rendered from specs in `docs/paper_figures_and_tables.md` Section 2 (Figure F2). Data source: T42 hop-bucket analysis.

## Remaining Delta to Final Submission Bundle

The following items remain before a final submission bundle can be assembled:

1. **Author information**: Replace `Anonymous Author(s)` with actual names, affiliations, and emails (or keep anonymous for double-blind review per CFP instructions).
2. **ITP CFP confirmation**: Verify the exact template requirement (LLNCS vs LIPIcs) from the target year's CFP.
3. **Table rendering**: Tables are currently in LaTeX `tabular` format. Verify they render correctly at print size.
4. **Figure quality check**: Inspect rendered figures at actual print resolution (300 DPI minimum for print).
5. **Bibliography completeness**: The current `references.bib` covers works cited in the paper. Additional entries may be needed if reviewers request more related work.
6. **Submission bundle**: Package `.tex`, `.bib`, figures, and any required style files into a single archive.
7. **CPP branch**: If CPP submission is also planned, create a variant using ACM format (different document class and bibliography style).
8. **Artifact evaluation bundle**: If the venue supports AE, prepare the pipeline, protocol, and demo tool as a separate package.
