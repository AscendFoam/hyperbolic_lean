# Review: T55

Verdict: PASS_WITH_WARNINGS

## Blocking Issues

None.

The paper draft refinements directly address all four T54 deferred warnings: abstract compression, Background section, Related Work section, and synthesized_only diagnostic explicitness. All acceptance criteria are satisfied. All claim boundaries and active risks are preserved.

## Non-Blocking Issues

### 1. Allowed Files scope overrun (fifth consecutive task)

The T55 task package lists 5 Allowed Files:
- `docs/paper_draft.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

The diff shows 4 additional files were modified:
- `docs/00_raw_idea.md` (timestamp + execution notes for T53/T54)
- `docs/01_feasibility_report.md` (timestamp + next-step text T53→T55)
- `docs/03_architecture.md` (timestamp + architecture gap updates)
- `docs/06_eval_protocol.md` (timestamp + task status sync)

This is the fifth consecutive task with this pattern (T50 → T52a → T53 → T54 → T55). The T50 review initially classified this as "rejected future precedent." The T54 review classified it as "Deferred" and noted "this is the third consecutive task where this pattern recurs." It is now the fifth.

Ironically, R08 was updated in this very diff to note: "后续任务要么严格限制 worker 只改列出的文件，要么在任务包中显式扩大 Allowed Files，避免继续依赖隐含惯例。" Yet the worker proceeded to do the same thing.

**Classification:** Deferred with governance note. The edits are benign governance synchronization (timestamps, status updates, execution notes) that do not alter experimental results, claim boundaries, or protocol semantics. However, this pattern has now recurred across five consecutive tasks and continues to undermine the Allowed Files enforcement mechanism. Either the Captain should expand Allowed Files in future task packages to explicitly include all `docs/00–08` governance docs, or the worker should strictly limit edits to the listed files. The current middle ground — where the pattern is noted in reviews but never enforced — erodes the governance contract.

### 2. Background and Related Work placement as subsections

The task package explicitly permits non-independent sections: "不要求新增独立一级章节。允许通过 Introduction 内新增小节、Discussion 内承接段落、或其他等价结构实现。" The worker placed Background as Section 3.2 (within Introduction) and Related Work as Section 6.5 (within Discussion). This satisfies the acceptance criteria and the task specification.

However, R33 (now Mitigated) correctly notes: "最终 venue 格式化仍可能要求独立章节而非子节." This is a venue-specific formatting concern, not a T55 scope defect.

**Classification:** Accepted placement choice. The subsections are substantive and well-organized. Venue reformatting is a future task.

### 3. Abstract word count

The worker reports abstract compression from ~180 to ~140 words. By token-based counting, the refined abstract is approximately 155 words, which is a meaningful reduction from the T54 estimate of ~180 words. The exact count depends on whether code-formatted terms (`extends`, `instance_of`) are counted as single tokens or multiple words, but the direction and magnitude of the reduction are consistent with the task goal.

The rest of the draft also grew: Background (Section 3.2) adds ~120 words, Related Work (Section 6.5) adds ~230 words. The net change in total draft length is approximately +350 words of substantive content, balanced by abstract compression of ~25 words. This is expected — adding Background and Related Work was the primary goal.

**Classification:** Accepted. The abstract is genuinely more compact. The overall draft grew because it now includes previously missing content, which is the intent of the refinement.

### 4. D19 marked as "Closed"

The worker marked D19 as "Closed by T55" in `docs/08_risks_and_open_questions.md`. The deferred item was: "在 paper draft 中补齐更显式的 Background / Related Work 承接，并进一步压缩 abstract." The T55 refinements directly satisfy this. The re-trigger condition ("若后续 venue 格式要求独立一级章节而非子节") is a legitimate caveat that does not invalidate the closure.

**Classification:** Accepted. D19 closure is substantively justified by the refinements, with appropriate re-trigger caveat.

## Missing Tests

Not applicable. This is a documentation-only task (paper draft refinement). All three verification commands passed:

1. **8 section headers**: All confirmed (Title through Conclusion, lines 11, 19, 29, 89, 185, 299, 348, 386)
2. **Key concepts**: Background present at Section 3.2 (line 37), Related Work present at Section 6.5 (line 336). `provenance-conditional`: 16 occurrences, `explicit_only`/`synthesized_only`/`hierarchy_mixed`: 51 occurrences, R28/R29/R30/R25: 7 occurrences
3. **Governance references**: T55, Narrow, Current Unique Task correctly referenced across `docs/04_task_board.md`, `docs/05_decision_log.md`, `docs/07_handoff.md`, `docs/08_risks_and_open_questions.md`

## Suspicious Implementation Details

### Refinement quality

Each of the four required refinements was checked against the current `docs/paper_draft.md`:

1. **Abstract compression**: The abstract is now 2 paragraphs + closing line, approximately 155 words (down from ~180). C1–C5 are listed compactly rather than expanded. The provenance-conditional main finding, single-environment boundary, and 60-sweep validation are retained. ✓

2. **Background (Section 3.2)**: Three well-organized paragraphs covering (a) Lean/Mathlib hierarchy semantics with the structural distinction between `extends`, `instance_of`, and `uses`; (b) hyperbolic GNN theoretical motivation and its dependence on actual tree-likeness; (c) formal-math graph tooling landscape and this paper's differentiated positioning as methodology rather than new model. Content is accurate and does not introduce unreviewed claims. ✓

3. **Related Work and Positioning (Section 6.5)**: Four paragraphs covering (a) hyperbolic embeddings literature (Poincaré, HGCN, Lorentzian) and the key difference (engineered hierarchies vs synthetic trees); (b) formal-math graph datasets (DeepMath, TacticToe, LeanDojo) and orthogonal contribution; (c) proof assistant hierarchy navigation tools; (d) explicit differentiation statement ("This paper is not a 'new model' contribution. Our contribution is methodological..."). All content stays within the reviewed evidence boundary and the paper_outline.md claim framework. ✓

4. **synthesized_only explicitness (Section 5.4)**: Table now includes a Field.Subfield row with `*see note below*` placeholder (not a fabricated number). A new paragraph "Why Field.Subfield is not presented as a verified table row" explicitly explains: (a) Order.Ring has a verified numeric row; (b) Field.Subfield GCN values are omitted due to R28 aggregate/per-seed discrepancy; (c) omission is not to hide a counterexample but to avoid presenting unverified precision as fact. The Section 5.7 summary table has a footnote `\* FS synthesized_only GCN numeric withheld...` referencing Section 5.4. ✓

### Claim boundary integrity

All boundaries from the task specification remain intact:
1. `explicit_only` is primary evidence — unchanged ✓
2. `synthesized_only` is controlled diagnostic — unchanged ✓
3. `hierarchy_mixed` is reproducibility check — unchanged ✓
4. Mixed graph: GCN still ahead — unchanged ✓
5. R28/R29/R30/R25 all open — unchanged ✓
6. No claim of HGCN general superiority — unchanged ✓
7. Non-claims (Section 3.6) — match paper_outline.md Section 3 ✓

### No forbidden scope violations in the draft

- No new experiments, seed sweeps, traces, splits, or demos ✓
- No modifications to `project_bootstrap/`, `data/`, or `artifacts/` ✓
- No rewrite of `docs/02_experiment_plan.md` ✓
- No modification of `docs/paper_outline.md` ✓
- No modification of `docs/experiment_reports/provenance_summary.md` ✓
- R28/R29/R30/R25 not written as closed ✓
- No unreviewed new numbers or chart conclusions ✓
- No figure rendering or artifact packaging content ✓

### Numeric accuracy

All numeric anchors in the refined draft remain unchanged from the T54 draft, which was verified to match T32/T33/T41/T42/T43/T52a artifacts. The Background and Related Work sections do not introduce new numeric claims. ✓

### Governance sync accuracy

- `docs/04_task_board.md`: T53→T55 correctly reflected in Current Unique Task, Why Now, Worker Package Summary, and Execution Note. Project Status correctly shows Narrow. T53 and T54 marked complete [x], T55 remains [ ] (pending review). ✓
- `docs/05_decision_log.md`: D034 (Narrow), D035 (T53→T54), D036 (T54 draft), D037 (T54→T55), D038 (T55 refinement) all correctly documented. ✓
- `docs/07_handoff.md`: Section 3 updated to T55, items 78-82 added for T53/T54/T55 history, Section 8 updated. ✓
- `docs/08_risks_and_open_questions.md`: R33 from Active→Mitigated (substantiated by T55 refinements), D19 closed, timestamps updated. ✓

## Recommended Next Action

1. **Captain should mark T55 as complete.** All 6 acceptance criteria are satisfied:
   - 8 section headers retained ✓
   - Background and Related Work explicitly retrievable ✓
   - Abstract more compact than T54, provenance-conditional main conclusion retained ✓
   - synthesized_only section explains Field.Subfield omission ✓
   - Governance docs consistent with T55 ✓
   - No new experiments, no experiment report modifications, no unreviewed numbers ✓

2. **Captain should address the Allowed Files scope pattern** that has now recurred across five consecutive tasks (T50, T52a, T53, T54, T55). Options:
   - Expand Allowed Files in future task packages to explicitly include all `docs/00–08` files when governance sync is expected, or
   - Instruct workers to strictly limit edits to listed files

3. **Next task** should address one of:
   - Figure/table rendering (translating the refined draft's tables into publication-quality renderings)
   - R28/R29 precision fixes (resolving the aggregate/per-seed discrepancy and source table cell error before external submission)
   - Artifact packaging for CPP submission
   - R30 contribution count decision (merge or retain, given the refined abstract is now leaner)

4. **Commit** should include all changes but continue to exclude `.claude/settings.json`.
