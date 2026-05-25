# Venue Submission Plan

> Status: Venue-specific formatting / submission planning document.
>
> Created: 2026-05-23 (T62 worker), updated 2026-05-25 (T63 review PASS_WITH_WARNINGS; T63 complete; T64 current: core figure QA / regeneration)
>
> Purpose: Record the primary venue path, remaining venue-specific formatting/submission deltas, and any paper-facing asset adjustments needed before a venue-specific build. This document does not introduce new claims, numbers, or conclusions.

---

## 1. Venue Choice / Priority

### Primary Venue: ITP (Interactive Theorem Proving)

**Rationale:**
1. **Community fit.** The paper directly serves the proof assistant community with real traced Lean/Mathlib hierarchy graphs, hierarchy extraction tooling, grouped retrieval benchmarks, and structure diagnostics. ITP readers will immediately understand why `extends` vs `instance_of` provenance matters.
2. **Narrative alignment.** The paper's central story — pipeline, protocol, diagnostics, and provenance-conditional finding — maps naturally to ITP's interest in proof infrastructure and methodology. The ancestor explanation demo (T52a) provides an interactive proof-exploration use case.
3. **Evidence level.** ITP accepts methodological and infrastructure contributions without requiring multi-repo replication or end-to-end theorem proving. The current evidence base (60 provenance-aware seed sweeps across 2 candidates × 3 splits, with zero failures) is sufficient.
4. **Page budget.** 5 contributions (C1–C5) fit within ITP's typical ~16-20 page limit, with C3 or C5 compressible to appendix if needed.

### Co-Primary: CPP (Certified Programs and Proofs)

**Rationale:**
1. **Artifact focus.** CPP values reproducible artifact packages and tool-level contributions. The frozen artifact package (Section 9 of `paper_artifact_package.md`) and the ancestor explanation CLI demo directly meet CPP's submission expectations.
2. **Proof engineering framing.** CPP readers will value the pipeline engineering (C1), the protocol correction (C2), and the diagnostics framework (C3) as proof-engineering infrastructure.
3. **Preparation overlap.** Most formatting and packaging work for ITP also applies to CPP (LaTeX, figure rendering, artifact packaging). The primary delta is the document class/format and abstract framing.

### Stretch Target: FM

**Condition:** Move to FM after ITP/CPP submission if (a) multi-repo replication is completed and (b) the proof-side utility is extended. Not active for the current submission cycle.

### Backup: SEFM / ICFEM

**Condition:** Only if ITP/CPP submission is not viable at the current evidence level.

### Recommendation

Prepare the ITP submission first. CPP is structurally similar enough that conversion requires only formatting and light narrative reframing. Submit to ITP as primary; if rejected, reformat for CPP without changing the evidence base.

---

## 2. Submission Checklist (Venue-Specific Deltas)

This checklist records what remains to be done **after** the T61 repo freeze to produce a venue-ready submission for ITP. Items marked [common] apply to both ITP and CPP.

### 2.1 LaTeX / Document Formatting

- [ ] [common] Choose document class and style:
  - ITP typically uses **LIPIcs** (Leibniz International Proceedings in Informatics, via Schloss Dagstuhl) or **Springer LNCS** style.
  - Confirm ITP 2026/2027 CFP for the exact template requirement.
- [x] [common] Convert `docs/paper_draft.md` to LaTeX, one `.tex` file per section or a single main file. (Done by T63: `paper/itp/main.tex`)
- [x] [common] Add `\documentclass`, `\usepackage`, `\bibliographystyle` boilerplate. (Done by T63: LLNCS class, splncs04.bst)
- [ ] [common] Set up proper section numbering, cross-references (table/figure/section), and bibliography.
- [ ] [common] Verify page count fits within venue limit (~16 pages main text + references).

### 2.2 Author and Affiliation Boilerplate

- [ ] [common] Add author names, affiliations, ORCIDs (if not double-blind).
- [ ] [common] Add correspondence email or anonymization notice.
- [ ] [common] Add venue-required metadata (abstract, keywords, ACM CCS Concepts or similar).

### 2.3 Figure and Table Rendering

- [x] Figure F1 (provenance split / structure): Render from spec in `paper_figures_and_tables.md` Section 2. (Done by T63: `paper/itp/figures/F1_provenance_structure.png`; final visual QA / possible style regeneration handled in T64)
- [x] Figure F2 (hop-depth delta): Render from spec in `paper_figures_and_tables.md` Section 2. (Done by T63: `paper/itp/figures/F2_hop_depth_delta.png`; final visual QA / possible style regeneration handled in T64)
- [ ] [common] Verify all rendered figures have correct captions referencing source doc entries.
- [ ] [common] Verify all table numbers in the PDF match `paper_figures_and_tables.md` specs.
- [ ] [common] Check that FS hop_4_plus footnote (4/5 seeds) appears in Table T3 / Figure F2.
- [ ] [common] Check that FS synthesized_only footnote (flat star forest, trivially solvable) appears in Table T2.

### 2.4 Bibliography

- [x] [common] Convert all citations to BibTeX format. (Done by T63: `paper/itp/references.bib`)
- [ ] [common] Verify that all cited works appear in the bibliography and vice versa.
- [ ] [common] Choose bibliography style matching venue requirements.

### 2.5 Submission Assets

- [ ] [common] Create submission bundle: `.tex` source, `.bib`, figures (PDF/PNG), style file, README.
- [ ] [common] Run `paper_artifact_package.md` Section 6 submission checklist.
- [ ] [common] Verify `R25` wording: no claim of "independently reproduced" anywhere.
- [ ] [common] Exclude `.claude/settings.json` from any submission or commit.
- [ ] [common] Package artifact evaluation bundle (if venue supports AE).

### 2.6 Venue-Specific Narrative Adjustments

- [ ] ITP: Tweak abstract and introduction to emphasize proof-assistant infrastructure and hierarchy understanding. Downplay model architecture details.
- [ ] CPP: Light reframe of abstract to emphasize proof engineering, reproducibility, and tool contributions. No change to evidence or numbers.
- [ ] FM (deferred): Not needed for current cycle.

---

## 3. Asset Delta Note

### Paper-facing wording changes required for ITP

The following minimal wording adjustments are needed when formatting for ITP. None alter the evidence base, claim boundary, or numeric values.

| Location | Current Wording | Proposed ITP Wording | Rationale |
| --- | --- | --- | --- |
| Abstract, line 1 | "pipeline, evaluation protocol, diagnostics framework, and training alignment correction" | "pipeline, evaluation protocol, diagnostics framework, training alignment, and an ancestor explanation tool" | ITP readers value seeing the proof-facing tool early |
| Section 1 (Title alt) | "When Does Hyperbolic Geometry Help on Real Formal-Math Graphs?" | "A Reproducible Pipeline for Understanding Formal-Math Hierarchy Graphs" | The short title should reflect the methodology contribution, not the open question, for ITP's reader base |
| Section 9 (Proof-Side Bridge) | Currently a discussion section | Promoted to a dedicated short section "Ancestor Explanation Tool" (Section 8, moving Limitations to 9) | ITP values tool demonstrations; a short dedicated section signals engineering completion |

These changes are **optional refinements** that improve venue fit without altering claims or evidence. They should be applied during the LaTeX conversion step, not in the current markdown source-of-truth.

### No changes needed

- No numeric values are altered.
- No claim boundaries are expanded.
- No contribution (C1–C5) is added or removed.
- No risk (R25, R30, R08) is written as closed.
- No experiment or artifact modification is introduced.

---

## 4. Timeline Note

ITP's typical submission deadlines are in **January–February** (for the summer conference) or **April–May** (for a fall conference), depending on the year. CPP typically co-locates with POPL and has deadlines in **October–November**. Verify the exact CFP before setting a target cycle.

The current repo state (T61 frozen, paper-facing assets reviewed, ancestor explanation demo running) is **submission-ready for the formatting phase** — no experiments, data collection, or evidence generation remain before a venue-specific build.
