# T22 Review

## Verdict: PASS

## Blocking issues

- None

## Non-blocking issues

1. **Shallow forest flag condition 3 can mislabel deep-but-fragmented graphs**: Section 3.1 condition 3 (`component ratio < 0.50 AND leaf ratio >= 0.70`) triggers "shallow forest risk" on `Mathlib.Algebra.Order` (component ratio 0.489, leaf ratio 0.774) even though it has the longest chain in the entire pool (11). The structural problem is fragmentation, not shallowness, so the flag name "shallow forest risk" is semantically misleading for this case. The candidate role gate system in Section 4 correctly classifies it as "depth stress-test" rather than "diagnostic-only," so the final outcome is correct — but a future worker reading only the flags could be confused. Consider renaming the flag to "fragmentation risk" or adding a clarifying note that the flag is about structure, not necessarily depth.

2. **Report template omits `multi-parent count`**: Section 2 lists `multi-parent count` as a required input, and Section 3.2 uses it in the star-forest flag. However, the report template in Section 7 does not include a row for `multi-parent count`. Adding it would make the template self-consistent with the required inputs and the star-forest detection logic.

3. **`ancestor_added_nodes` not defined inline**: The `closure expansion ratio` formula references `ancestor_added_nodes`, which is explained in `candidate_graph_audit.md` but not in the protocol itself. A brief inline definition (e.g., "nodes added to the seed module when expanding to include all ancestors in the relation layer") would improve self-containedness for future workers who may not read the audit document first.

## Missing tests or verification

- None. The verification command (`rg -n "heuristic|shallow|star forest|longest chain|leaf ratio|template" docs\diagnostics_protocol.md`) was run and hits all required keywords across the document. This is a documentation-only task; no code tests apply.

## Suspicious implementation details

- None. No code was changed. All five modified/new files (`docs/diagnostics_protocol.md`, `docs/06_eval_protocol.md`, `docs/04_task_board.md`, `docs/07_handoff.md`, `docs/08_risks_and_open_questions.md`) are within the task package's Allowed Files.

## Scope compliance

- **Allowed files**: All edits are within scope. No files outside the allowed list were modified.
- **Forbidden scope**: No theory proofs were written (all thresholds labeled `heuristic`). No experiment code was modified. No training or seed sweep was started. T21 audit priority is referenced as calibration input, not written as a final benchmark conclusion.
- **Expected output**: The protocol covers `longest chain`, `leaf ratio`, positive scale, `component ratio`, and `closure expansion ratio` gating, and includes a reusable report template — meeting all requirements from the task package.

## Calibration verification

All five candidates in Section 5 were cross-checked against `docs/candidate_graph_audit.md` numeric values:

| candidate | gate section | checks | result |
| --- | --- | --- | --- |
| `Mathlib.Algebra.Order.Ring` | 4.1 default follow-up | chain 10>=8, edges 300>=250, ratio 0.747>=0.65, leaf 0.502<=0.60, closure 0.458<=0.60, no star-forest | PASS all gates |
| `Mathlib.Algebra.Order` | 4.2 depth stress-test | chain 11>=10, edges 1387>=800, ratio 0.489<0.65 | PASS |
| `Mathlib.Algebra.Ring.Subring` | 4.3 controlled probe | chain 10>=8, edges 170 in [100-249], ratio 0.431>=0.40, leaf 0.301<=0.60, closure 0.693>0.60 (noted closure-heavy) | PASS |
| `Mathlib.Algebra.Field.Subfield` | 4.3 controlled probe | chain 10>=8, edges 152 in [100-249], ratio 0.406>=0.40, leaf 0.278<=0.60, closure 0.714>0.60 (noted closure-heavy) | PASS |
| `Batteries.*` | 4.4 diagnostic-only | chain 3-4<=4, edges 26-28<100 | PASS |

Thresholds in `06_eval_protocol.md` Section 6 are consistent with `diagnostics_protocol.md` Sections 3 and 4.

## Key positive observations

1. **Clean heuristic framing throughout**: The document consistently labels all thresholds as `heuristic`, explicitly states it is "not a theoretical conclusion" and "not a final benchmark ranking," and requires reports to carry the same disclaimer.

2. **Well-structured gating system**: The two-layer design (flags in Section 3 for individual risk signals, role gates in Section 4 for final classification) is clear and allows a candidate to carry risk flags without being automatically disqualified.

3. **Calibration table is honest about being a snapshot**: Section 5 explicitly says "这组映射是当前模板校准点，不是永久排序."

4. **Governance notes are appropriate**: Section 8 correctly notes that the protocol doesn't close R14 or R16, doesn't replace the eval protocol, and should be recalibrated when new evidence arrives.

5. **New risk R17 and deferred item D09 are well-placed**: They correctly track the heuristic staleness risk and the review-adjustment loop.

## Recommended next action

- Accept T22 as complete. Captain should:
  1. Mark T22 as done in `04_task_board.md`.
  2. Update `07_handoff.md` to reflect review completion.
  3. Select the next task. The natural next step is T30 (reading existing grouped retrieval training code to locate the training/eval mismatch), which depends on the candidate selection work from T20-T22 but does not require further diagnostics protocol changes.
- Optional future revision: rename shallow forest flag condition 3 to reflect fragmentation rather than shallowness, add `multi-parent count` row to the report template, and add an inline definition for `ancestor_added_nodes`.
