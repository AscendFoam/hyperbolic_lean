# T12 Review: Grouped Protocol Freeze

> Reviewer: Claude Code (adversarial review — task package specifies adversarial reviewer type)
> Date: 2026-05-10
> Task package: `docs/tasks/M1_protocol/T12_grouped_protocol_freeze.md`

## Verdict: PASS

## Blocking issues

- None.

## Non-blocking issues

- None.

## Missing tests or verification

- None. The task package requires `rg` keyword search across code and protocol docs; this was run and produces hits for all required terms (`grouped`, `Recall@`, `MAP`, `nDCG`, `MRR`, `hop`). The `git diff` was checked and confirms scope compliance.

For adversarial review, I performed the following additional verification beyond the task package requirements:

1. **Code change correctness**: The added line `result_summary["grouped_test_ndcg_at_10"] = grouped.get("ndcg_at_10")` at `run_relation_grouped_retrieval_baseline.py:472` was verified against:
   - The upstream metric computation in `relation_baseline_common.py:307`, which computes `ndcg_at_10` — confirmed this key exists.
   - The other two runners: `run_relation_gcn_baseline.py:385` and `run_relation_hyperbolic_baseline.py:501` both already emit `grouped_test_ndcg_at_10` — confirmed this brings the grouped retrieval runner into alignment.
   - The downstream consumers: `_patch_sweep_reports.py:106` and `run_relation_seed_sweep.py:191` both already expect `grouped_test_ndcg_at_10` — confirmed the field was already in use downstream but missing from this one runner's output.

2. **Protocol document accuracy**: All code entrypoint paths referenced in `docs/grouped_retrieval_protocol.md` and `docs/06_eval_protocol.md` were verified to exist on disk (6 source files + 2 config files).

3. **Metric set completeness**: The frozen metric set in the protocol doc (`Recall@1/3/5/10`, `MAP`, `nDCG`, `nDCG@10`, `grouped-MRR`) matches the output fields in `result_summary.json` and the computation in `relation_baseline_common.py`.

4. **Legacy key handling**: The `task = "ancestor_ranking"` compatibility mapping is clearly documented in both the protocol doc (Section 1) and the eval protocol (Section 3.1), with explicit notes that this no longer means single-positive ranking.

## Suspicious implementation details

- None. The code change is a single line that adds a field to a summary dict. It follows the exact same pattern as the adjacent lines (`grouped_test_ndcg`, `grouped_test_mrr`, etc.). It uses `.get()` for safe access, consistent with all other field extractions in the same block. No hardcoded values, no conditional logic, no side effects.

## Scope compliance

| Check | Result |
| --- | --- |
| Only `Allowed files` modified | Pass — `docs/grouped_retrieval_protocol.md` (new), `docs/06_eval_protocol.md`, `docs/04_task_board.md`, `docs/07_handoff.md`, `docs/08_risks_and_open_questions.md`, `project_bootstrap/baseline_scaffold/src/run_relation_grouped_retrieval_baseline.py` — all within allowed scope |
| No `Forbidden scope` violations | Pass — no model architecture changes, no new unrelated tasks, no deleted results |
| T12 not marked complete prematurely | Pass — checkbox unchecked, execution notes say "reviewer 前状态" |
| Plans not written as facts | Pass — both protocol docs carry "draft" status headers with explicit reviewer-pending caveats |

## Adversarial review: evaluation protocol integrity

Since this task modifies evaluation protocol documentation and touches metric output code, I specifically checked:

1. **No metric definition drift**: The frozen metric set in the protocol matches what the code actually computes. `nDCG@10` in the doc corresponds to `ndcg_at_10` computed from grouped queries, which is standard normalized discounted cumulative gain at position 10.

2. **No silent metric substitution**: The legacy `MRR` field is preserved in the output alongside the grouped metrics — no replacement, just addition. The protocol doc explicitly states legacy `MRR` is auxiliary only.

3. **No evaluation scope expansion**: The code change does not alter which edges are considered positives, how queries are constructed, or how negatives are sampled. It only adds a missing output field.

4. **Output field consistency across runners**: All three baseline runners (GCN, hyperbolic, grouped retrieval) now emit the same set of `grouped_test_*` fields. This was not the case before T12 — the grouped retrieval runner was missing `grouped_test_ndcg_at_10`.

## Task completion assessment

The task package requires:

1. **Documented grouped protocol** — `docs/grouped_retrieval_protocol.md` covers canonical task name, legacy key mapping, query unit, positive set, frozen config fields, frozen metric set, frozen output structure, and non-goals. ✓
2. **Code-field alignment** — The one identified gap (`grouped_test_ndcg_at_10` missing from the grouped retrieval runner) was fixed with a minimal one-line addition. ✓
3. **Output format includes Recall@k, MAP, nDCG, grouped-MRR** — All present in both the frozen metric set (Section 4 of protocol) and the `result_summary.json` field list (Section 5.2). ✓
4. **Config fields documented** — Section 3 of protocol doc lists all relevant config fields. ✓
5. **Governance docs updated** — `04_task_board.md`, `07_handoff.md`, `08_risks_and_open_questions.md` all updated. ✓

All deliverables present. The task correctly scopes hop bucket reporting as deferred to T13.

## Recommended next action

- Captain may mark T12 as complete.
- Captain should decide between T13 (hop bucket verification) and T20 (diagnostics review) as the next task. T13 closes out Milestone 1; T20 starts Milestone 2.
- The legacy `task = "ancestor_ranking"` naming question (Open Question #10) should be resolved before publishing any benchmark results, but does not block near-term work.
