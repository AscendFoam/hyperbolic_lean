# T11 Review: Data Card

> Reviewer: Claude Code (read-only review)
> Date: 2026-05-10
> Task package: `docs/tasks/M1_protocol/T11_data_card.md`

## Verdict: PASS

## Blocking issues

- None.

## Non-blocking issues

- None.

## Missing tests or verification

- None. The task package requires `rg` keyword search and `git diff`; both were run. I additionally cross-checked the data card's quantitative claims (edge counts, coverage-aware backfill numbers, skipped counts) against the actual `stats.json` files for all three representative graph roots (`lean4_example_typeclass_precise_v2`, `batteries_typeclass_precise_coverage_v1`, `mathlib_algebra_order_precise_coverage_index_v1`) — all values match exactly. CSV column headers in `declarations.csv` and `edges.csv` also match the field descriptions in the card.

## Suspicious implementation details

- None. No version numbers were fabricated. No coverage-unreliable data was written as reliable. The data card explicitly preserves unresolved boundaries (Section 7.1, 7.2, 7.3) and references `docs/data_manifest.md` for version unknowns rather than duplicating or upgrading them.

## Scope compliance

| Check | Result |
| --- | --- |
| Only `Allowed files` modified | Pass — `docs/data_card.md` (new), `docs/04_task_board.md`, `docs/07_handoff.md`, `docs/08_risks_and_open_questions.md` |
| No `Forbidden scope` violations | Pass — no data files changed, no artifacts recomputed, no unreliable coverage presented as reliable |
| T11 not marked complete prematurely | Pass — checkbox unchecked, execution note says "reviewer 前状态" |
| Plans not written as facts | Pass — card header says "draft"; Section 8 rule 5 explicitly warns against treating `recommended usage` as completion signal |

## Task completion assessment

The task package requires:

1. **Graph list** — Section 6 provides a comprehensive table of all major graph families with observed characteristics, recommended usage, and not-recommended usage. ✓
2. **Field descriptions** — Section 3 documents observed columns in `declarations.csv`, `edges.csv`, and `stats.json` with interpretation notes. ✓
3. **Relation provenance** — Section 4 covers `uses / extends / instance_of` semantics, `evidence_source` values, representative edge counts, and the provenance split boundary. ✓
4. **Coverage-aware handling** — Section 5 documents the rule of use and three representative coverage behaviors with concrete `stats.json` fields. ✓
5. **Known limitations** — Section 7 covers unresolved version boundary, unresolved schema boundary, and structural limitation. ✓
6. **Recommended usage** — Section 6 table and Section 8 usage rules provide clear guidance. ✓
7. **Governance doc updates** — `04_task_board.md`, `07_handoff.md`, `08_risks_and_open_questions.md` all updated. ✓

All required deliverables are present. The quantitative claims in the card were verified against actual `stats.json` files and match exactly.

The newly added R11 risk and Open Question #9 in `docs/08_risks_and_open_questions.md` are well-scoped: they correctly identify the gap between the current provenance representation (derived directory names) and the ideal (first-class per-edge provenance field), and link this to Milestone 4 / T40–T43 for resolution.

## Recommended next action

- Captain may mark T11 as complete.
- Captain should decide whether to proceed to T12 (protocol freeze) or T13 (hop bucket verification) as the next task.
- The schema boundary issues in Section 7.2 (standardized `labels.csv` / `splits.csv`, first-class provenance labels) should be tracked as prerequisites for Milestone 3+ training tasks.
