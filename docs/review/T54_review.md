# Review: T54

Verdict: PASS_WITH_WARNINGS

## Blocking Issues

None.

The paper draft itself is well-constructed, numerically accurate, and respects all claim boundaries. The blocking concern is about scope violations in governance docs, but these fall into the same category as prior reviews (T50, T52a, T53) where Captain-side governance sync across `docs/00–08` was accepted as low-severity hygiene. See Non-Blocking Issues #1 below.

## Non-Blocking Issues

### 1. Allowed Files scope overrun (recurring pattern)

The T54 task package explicitly lists 5 Allowed Files:
- `docs/paper_draft.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

The diff shows 4 additional files were modified:
- `docs/00_raw_idea.md` (timestamp + execution note)
- `docs/01_feasibility_report.md` (timestamp + next-step text)
- `docs/03_architecture.md` (timestamp + architecture gap updates)
- `docs/06_eval_protocol.md` (timestamp + task status sync)

These are the same type of Captain-side governance sync edits that appeared in T50 and T52a reviews. The pattern was previously classified as "accepted low-severity hygiene" (T50 review) and "rejected future precedent" (T50 review non-blocking). The worker continues this pattern.

**Classification:** Deferred. The edits are benign governance synchronization (timestamps, status updates, next-step pointers) that do not alter experimental results, claim boundaries, or protocol semantics. However, this is the third consecutive task where this pattern recurs. Future tasks should either expand the Allowed Files list to explicitly include all `docs/00–08` governance docs, or strictly limit edits to the listed files.

### 2. Section 5.4 synthesized_only table incomplete

Section 5.4 (Controlled Diagnostic: synthesized_only) only shows Order.Ring results in the comparison table:

| Candidate | GCN MAP | HGCN MAP | Delta |
| --- | ---: | ---: | ---: |
| Order.Ring | 0.8453 ± 0.0295 | 0.7560 ± 0.0761 | GCN +0.0893 |

Field.Subfield results are omitted entirely, with only a prose note about the R28 aggregate/per-seed discrepancy. This is an acceptable presentation choice given R28, but it makes the table asymmetric. A reader may wonder whether Field.Subfield was omitted because it contradicts the narrative.

**Classification:** Accepted presentation choice. The R28 precision note in the prose is adequate. The next draft could add a footnote row like "Field.Subfield: R28 unresolved, see note" to make the omission explicit rather than silent.

### 3. Abstract length

The abstract runs approximately 180 words across two paragraphs. For ITP/CPP submissions, abstracts are typically 150–200 words. The current length is within range but near the upper bound. If page budget becomes tight (R30), the abstract could be tightened.

**Classification:** Deferred to finalization. Not blocking.

### 4. Missing Related Work section

The paper outline (Section 11, item 10) planned a "Related Work" section covering formal-math graph datasets, hyperbolic embeddings, proof assistant tooling, and graph-based retrieval. The draft does not include this section. The 8 required sections (Title through Conclusion) are all present, satisfying the acceptance criteria, but Related Work is a standard section that target venues will expect.

**Classification:** Deferred. The task specification lists exactly 8 required sections and does not include Related Work. Adding it is appropriate for a future draft iteration, not a T54 requirement. Noted here for planning.

### 5. Missing Background section

Similar to Related Work, the paper outline planned a "Background" section (Section 11, item 2) covering Lean/Mathlib hierarchy semantics, hyperbolic GNNs, and ancestor retrieval. The draft folds some of this into the Introduction (Section 3.1). This is a reasonable structural choice for a first draft but may need to be separated out for venue formatting.

**Classification:** Deferred. Same rationale as Related Work.

## Missing Tests

Not applicable. This is a documentation-only task (paper draft). The verification commands were run and passed:
- 8 section headers confirmed in `docs/paper_draft.md`
- All key concepts present (provenance-conditional: 22 occurrences, explicit_only: 20, synthesized_only: 14, hierarchy_mixed: 17, R28/R29/R30/R25 all present)
- Governance docs reference T54, Narrow, Current Unique Task

## Suspicious Implementation Details

### Numeric accuracy

All numeric anchors in the paper draft have been verified against reviewed experiment reports:

- **Hierarchy mixed MAP values** (4 values): Match T32/T33/T42 artifacts exactly
- **Explicit only MAP values** (4 values): Match T42 artifacts exactly
- **Hop bucket deltas** (2 values): Match T42 artifacts exactly
- **Structural properties** (longest chain, multi-parent, leaf ratio): Match T41 diagnostics exactly
- **Ancestor explanation demo values** (MAP 0.6438 vs 0.1492): Match T52a demo report exactly
- **Synthesized only MAP values** (OR): Match T42 artifacts exactly

No fabricated, estimated, or unreviewed numbers detected. The paper_outline.md Section 12 frozen numeric anchors are reproduced identically in the draft's Appendix A.2.

### Claim boundary integrity

The draft correctly maintains:
1. `explicit_only` as primary evidence — confirmed in Sections 3.4, 4.2, 5.2, 5.7, 6.1, 8
2. `synthesized_only` as controlled diagnostic — confirmed in Sections 4.2, 5.4, 5.7
3. `hierarchy_mixed` as reproducibility check with GCN ahead — confirmed in Sections 5.1, 5.5, 5.7
4. R28/R29/R30/R25 all retained as open risks — confirmed in Sections 5.4, 7.1.5, 7.1.6, 7.1.2, 7.4.12
5. Non-claims explicitly listed — Section 3.5 matches paper_outline.md Section 3 exactly
6. No claim of HGCN general superiority over GCN — consistently written as provenance-conditional

### No forbidden scope violations in the draft

- No new experiments, seed sweeps, traces, splits, or demos
- No modifications to `project_bootstrap/`, `data/`, or `artifacts/`
- No rewrite of `docs/02_experiment_plan.md`
- No modification of `docs/experiment_reports/provenance_summary.md`
- R28/R29/R30/R25 not written as closed
- No unreviewed new numbers or chart conclusions

## Recommended Next Action

1. **Captain should mark T54 as complete.** The paper draft satisfies all 5 acceptance criteria:
   - 8 section headers present ✓
   - Core claims match paper_outline.md and T53 milestone review ✓
   - R28/R29/R30/R25 boundaries retained ✓
   - Governance docs consistent with T54 status ✓
   - No forbidden scope modifications (within the draft itself) ✓

2. **Captain should accept the 4 governance doc edits** (`00_raw_idea.md`, `01_feasibility_report.md`, `03_architecture.md`, `06_eval_protocol.md`) as low-severity hygiene, following the precedent from T50/T52a/T53 reviews, but should add a governance note that future tasks should explicitly include all `docs/00–08` in Allowed Files if governance sync is expected.

3. **Next task** should address one of:
   - Figure/table rendering (translating draft tables into publication-quality figures)
   - R28/R29 precision fixes (resolving the aggregate/per-seed discrepancy and source table error)
   - Related Work and Background sections for the next draft iteration
   - Artifact packaging for CPP submission

4. **Commit** should include all changes but continue to exclude `.claude/settings.json`.
