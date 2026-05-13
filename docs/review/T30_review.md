# T30 Review

## Verdict: PASS

## Blocking issues

- None

## Non-blocking issues

1. **Section 4 sub-headings rendered at wrong nesting level**: Section 4 ("Confirmed Mismatch Points") contains M1–M6 as `##` headers, making them render as sibling sections rather than sub-sections. They should use `###` to nest under Section 4. This is purely a formatting issue and does not affect content correctness.

2. **M6 title contains mixed language**: The M6 heading "Reporting mismatch: grouped benchmark exists, but historical single-positive field still留在 summary surface" mixes Chinese characters into an otherwise English sentence. This is inconsistent with the clean English used in M1–M5 titles.

3. **M3 severity could benefit from a rough impact estimate**: The split mismatch (M3) is correctly identified as the most important finding, but the audit does not attempt even a rough structural estimate of how many `(src, relation)` queries are typically split across train/val/test in current configs. While running experiments is out of scope, a brief analysis based on the code path (e.g., noting that any query with ≥2 positive edges has a non-trivial probability of being split) would strengthen the P0 recommendation.

## Missing tests or verification

- None. The verification command (`rg -n "BCE|loss|grouped|query|negative|mismatch" docs\training_alignment_audit.md`) was run and hits all required keywords across the document. This is a documentation-only audit task; no code tests apply.

## Suspicious implementation details

- None. No code was modified. All seven specific code-level claims (BCEWithLogitsLoss, stratified_split by relation_type only, per-edge negative sampling, grouped query aggregation at eval time, binary AP checkpoint selection, and ranking_test_mrr coexisting with grouped fields) were independently verified against the actual source and confirmed correct.

## Scope compliance

- **Allowed files**: All edits are within scope. Four files modified: `docs/training_alignment_audit.md` (new), `docs/04_task_board.md`, `docs/07_handoff.md`, `docs/08_risks_and_open_questions.md`.
- **Forbidden scope**: No training code was modified. No long sweep was run. No unverified performance conclusions were made — the document explicitly states "不给出未验证性能结论" and only describes code facts and structural implications.
- **Expected output**: The audit lists current loss, batch/query structure, negative sampling, eval entry points, and minimal change points — meeting all requirements from the task package.

## Code claim verification

All seven code-level claims in the audit were independently verified against source:

| Claim | Source location | Verified |
| --- | --- | --- |
| `build_ancestor_task_examples_with_hops(...)` generates `(src, dst, relation)` edges | `relation_tasks.py:120-164` | Yes |
| `stratified_split_relation_examples(...)` groups by `relation_type` only, not `(src, relation)` | `relation_tasks.py:31-56` | Yes |
| `sample_negative_relation_examples(...)` samples per positive edge | `relation_tasks.py:219-302` | Yes |
| `build_grouped_ranking_queries(...)` aggregates by `(src, relation)` at eval time | `relation_tasks.py:380-410` | Yes |
| Both runners use `BCEWithLogitsLoss` | `run_relation_gcn_baseline.py:147`, `run_relation_hyperbolic_baseline.py:250` | Yes |
| Best checkpoint selected by `val_average_precision` | `run_relation_gcn_baseline.py:187-188`, `run_relation_hyperbolic_baseline.py:294-295` | Yes |
| `result_summary.json` contains both `ranking_test_mrr` and grouped fields | `run_relation_gcn_baseline.py:380-392`, `run_relation_hyperbolic_baseline.py:495-507` | Yes |

## Key positive observations

1. **M3 is a genuinely important discovery**: The finding that `stratified_split_relation_examples` splits by edge rather than by `(src, relation)` query is more severe than the task description anticipated. It means current grouped eval results have an unknown amount of positive-set incompleteness, which is correctly flagged as R19 (High) and prioritized as P0 in the recommendations.

2. **Section 3 ("What Is Already Aligned") is good practice**: By explicitly documenting what works correctly (grouped eval infrastructure, legacy key mapping, negative sampling exclusion), the audit avoids overstating the problem scope and gives T31 a clear boundary.

3. **Priority ordering (P0–P3) is well-reasoned**: Putting query-level split completeness ahead of grouped loss is correct — fixing the loss without fixing the split would produce unreliable grouped metrics regardless of training quality.

4. **Appropriate restraint on T31 boundary**: Section 5 gives clear recommendations without implementing anything, maintaining the audit-only scope. The D10 deferred item correctly tracks the Captain decision point about whether to merge split fix into T31.

5. **R07 update is precise**: The risk table update adds specific confirmed facts (edge-level BCE, per-edge negative sampling, binary AP checkpoint) rather than vague restatements.

## Recommended next action

- Accept T30 as complete. Captain should:
  1. Mark T30 as done in `04_task_board.md`.
  2. Update `07_handoff.md` to reflect review completion.
  3. Decide the T31 scope: whether query-level split fix is merged into T31 or split into a separate task. The audit's P0 recommendation and R19 severity strongly suggest it should be a prerequisite (either T31前置 or a new T31a), not deferred past T32/T33.
  4. Select the next task as T31 (or T31 + split-fix task).
- Optional future revision: fix M1–M6 heading nesting, clean up M6 title language.
