# T57 Review Explanation (For Human)

## 1. What is this task trying to accomplish?

The project has completed its experimental phase (Milestones 1–4, covering protocol freeze, graph diagnostics, grouped retrieval training, and provenance split experiments). The core finding — "HGCN only outperforms GCN on the explicit hierarchy layer, not on the full mixed graph" — has been reviewed and stabilized. The previous task (T56) cleaned up the last numerical precision issues (R28/R29).

T57's job was to take all these stable, reviewed numbers and organize them into a **publication-ready figure and table specification document**. Think of it as creating a "master blueprint" for every table and figure that will appear in the final paper — what numbers go where, what the caption says, where the data comes from, and how it should be rendered. No new experiments, no new numbers, just organizing existing evidence into a form that can directly feed into LaTeX or a rendering tool.

Additionally, T57 needed to absorb two non-blocking notes from the T56 review:
- The summary table in `provenance_summary.md` was using a vague "GCN wins" label instead of the exact delta (+0.3143).
- The explanation in the paper draft about a peculiar perfect-score result (GCN MAP = 1.0000) was too long and needed compression.

## 2. What did the implementation change?

### New file: `docs/paper_figures_and_tables.md`

This is the central deliverable — a source-of-truth document containing:

**4 Core Tables:**
- **T1 (Mixed Baseline)**: GCN vs HGCN on the full source graph. Result: GCN leads. This is the "starting point" that shows HGCN is not generally better.
- **T2 (Provenance-Aware Comparison)**: The key table — split into `explicit_only` (where HGCN wins) and `synthesized_only` (where GCN wins). This is the primary evidence for the paper's central claim.
- **T3 (Hop-Bucket Delta)**: Shows that HGCN's advantage grows with ancestor chain depth — from ~+0.03 at hop_2 to ~+0.25 at hop_4_plus. This is the mechanism evidence.
- **T4 (Structural Properties)**: Shows that `synthesized_only` graphs are flat star forests (longest chain = 1) while `explicit_only` graphs have genuine hierarchy (longest chain = 9–10). This explains *why* the provenance split matters.

**2 Core Figure Specs:**
- **F1 (Structure Contrast)**: A visual specification for showing the dramatic structural difference between provenance splits.
- **F2 (Hop-Depth Delta)**: A visual specification for the monotonic growth of HGCN's advantage with depth — the single most important visual for the paper.

**1 Summary Table (T5)**: A compact "one-glance" table encoding the entire provenance-conditional conclusion.

Each entry includes: temporary ID, intended paper section placement, caption, exact artifact path for data sourcing, exact numbers, and rendering notes (colors, bolding, footnotes).

### Changes to `docs/paper_draft.md`

- **Section 5.4 compressed**: The explanation for why GCN achieves perfect MAP (1.0000) on the flat `synthesized_only` graph was compressed from ~120 words to ~60 words. All three required facts were preserved:
  1. `grouped_test_map` and `test_average_precision` are different metrics
  2. Both are correctly computed and internally consistent
  3. The previously reported "discrepancy" (R28) was resolved by T56 as metric naming confusion
- **Section 5.7 footnote updated** to reference the new source document.

### Changes to `docs/experiment_reports/provenance_summary.md`

- **Section 7.2 summary table**: FS `synthesized_only` entry changed from qualitative "GCN wins" to quantitative "GCN wins (+0.3143 MAP)". This brings the summary table to the same granularity as the main tables.

### Changes to `docs/paper_outline.md`

- **Section 6 precision note**: Updated from "unresolved R28/R29" to "resolved by T56" with verified values.
- **Section 7 internal validity item 5**: Updated from "Root cause not yet resolved (R28)" to resolved metric naming confusion.
- **Section 10 provenance-precision boundaries**: R28/R29 updated from "active" constraints to "resolved by T56".

### Governance document updates (8 files)

All governance docs (`00_raw_idea.md` through `08_risks_and_open_questions.md`) were updated with:
- T57 status as current task
- Worker execution summary
- Timestamps
- D20 marked as closed (the deferred item about summary table granularity)
- D042 added to decision log

### Significance for the project

This task represents a critical transition point: the project is moving from "doing experiments and writing reports" to "preparing a submission-ready paper." The new `paper_figures_and_tables.md` serves as the bridge between raw experimental evidence and the final publication format. Future tasks (artifact packaging, final paper editing) can now reference this single source-of-truth document rather than hunting through multiple experiment reports.

The compression of Section 5.4 and the granularity unification in the summary table are small but important refinements — they ensure that when a human reviewer or reader encounters the paper, every table and figure tells a consistent story at a consistent level of detail.

## 3. Why was the review verdict PASS?

**All six acceptance criteria were met:**

1. The new source document contains 4 core tables + 2 core figure specs (minimum was 4 + 2). ✓
2. Paper draft references are aligned with the source doc. ✓
3. `provenance_summary.md` summary table granularity now matches the main tables. ✓
4. `paper_outline.md` no longer treats R28/R29 as unresolved. ✓
5. All 8 governance docs reflect T57 as the current task. ✓
6. No new experiments, no artifact changes, no unreviewed values. ✓

**Numerical consistency was verified independently:** I grepped for all key numeric values (`1.0000 ± 0.0000`, `+0.3143`, `+0.1247`, `+0.0557`, etc.) across `paper_figures_and_tables.md`, `paper_draft.md`, and `provenance_summary.md`. Every number matches exactly. No fabrication, no copy-paste errors.

**Section 5.4 compression preserved all required facts:** The task specified three facts that must not be lost. All three are present in the compressed version. The dropped content was supplementary mechanistic detail (e.g., "candidate pool mean = 31"), which the task explicitly allowed removing.

**No mock, stub, or fake content:** Every number traces to a specific artifact path from reviewed tasks (T32, T33, T41, T42, T43). The document is a genuine organizational effort, not fabrication.

**Three non-blocking issues were noted:**
1. The source document's own cross-reference table says "Pending sync" for `paper_outline.md` changes that were actually completed — a stale self-reference that should say "Aligned."
2. `.claude/settings.json` was auto-modified and must be excluded from any commit (established pattern).
3. The compression dropped a minor mechanistic detail about why retrieval is trivial — acceptable, but worth noting for final editing.

None of these block the task's completion.

## 4. Supplement to the worker's summary

The worker's summary was accurate and thorough. A few supplementary observations:

1. **Cross-reference self-consistency**: The worker noted the cross-reference consistency matrix but missed that two rows in it became stale after the `paper_outline.md` edits were completed. The matrix says "Pending sync" for changes that were already done. This is a minor oversight — the actual synchronization was correct, but the tracking table wasn't updated.

2. **Figure F1/F2 rendering feasibility**: The figure specs are well-designed for subsequent rendering. F2 (hop-depth delta) in particular has clear encoding rules (line chart with markers, x-axis = hop buckets, y-axis = MAP delta) that map directly to matplotlib/pgfplots code. The rendering notes are specific enough to avoid ambiguity.

3. **D20 closure is clean**: The deferred item D20 (unify summary table granularity + compress Section 5.4) was precisely the work T57 did. The risks document correctly marks it as "Closed by T57" with specific details. No loose ends.

4. **No new numerical claims**: I verified that no numbers appear in the source doc that don't already exist in reviewed artifacts. The document is purely organizational — it collects, formats, and cross-references existing reviewed evidence without adding new claims.
