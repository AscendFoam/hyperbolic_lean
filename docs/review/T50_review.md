# Review: T50

Verdict: PASS_WITH_WARNINGS

## Blocking Issues

None.

## Non-Blocking Issues

### 1. Out-of-Allowed-Files edits (6 files)

The worker modified `docs/00_raw_idea.md`, `docs/01_feasibility_report.md`, `docs/03_architecture.md`, `docs/06_eval_protocol.md`, `docs/tasks/M4_provenance/T43_provenance_summary.md`, and `docs/tasks/M5_paper/T50_paper_skeleton.md`. None of these are in the T50 Allowed Files list (`docs/paper_outline.md`, `docs/04_task_board.md`, `docs/05_decision_log.md`, `docs/07_handoff.md`, `docs/08_risks_and_open_questions.md`).

**Assessment:** All out-of-scope changes are governance-state tracking updates (timestamps, current task pointers, execution notes, progress appendices). None alter frozen semantics, experimental values, or the T40–T43 conclusions. The T43 task package and T50 task package updates are arguably closer to "captain-level governance editing" than to worker output, but they were done by the worker. The `.claude/settings.json` auto-permission diff is present as usual (continue to exclude from commit).

**Classification:** Accepted as low-severity governance hygiene — consistent with how prior reviews (T42, T43) handled the same pattern. However, the worker should not be modifying task packages (`docs/tasks/**/*.md`); that is a captain responsibility.

### 2. D030 decision status is "Pending review" rather than "Accepted"

`docs/05_decision_log.md` D030 has status `Pending review`. This is actually correct behavior — the worker did not presume the decision was accepted before review. Noted for completeness; captain should update to `Accepted` after this review closes.

### 3. R30 / R31 are self-identified risks that may need merging

The worker added R30 (contributions too broad for page limits) and R31 (ancestor explanation MVP may be too lightweight). These are reasonable risk registrations. R30 in particular should be addressed during T50 review: the 5 contributions could potentially be merged (C1+C5 as pipeline+alignment) for shorter venues.

### 4. Numeric anchors in Section 12 of paper_outline.md use `synthesized_only` GCN values not directly quoted

The paper outline correctly avoids quoting the erroneous R29 table cell. However, Section 6 Table 4 and Section 12 reference `synthesized_only` structural properties only (longest chain), not MAP values, which is the correct approach. No issue here — confirmed as properly handled.

### 5. `docs/07_handoff.md` Section numbering gap

The handoff has Section 8 ("下一步 / Next Steps") placed before Section 4 ("当前已知事实"). This numbering anomaly (sections 3 → 8 → 4 → 5 → 6 → 7 → 8) was introduced by the T42 worker and persists. Not caused by T50, but worth noting for a future cleanup.

## Missing Tests

Not applicable — T50 is a documentation-only task. The verification commands were run and reported as passing with all required keywords present.

## Suspicious Implementation Details

None detected. The paper outline:

- Correctly maintains provenance-conditional wording throughout all 12 sections.
- Correctly assigns evidence roles: `explicit_only` = primary, `synthesized_only` = controlled diagnostic, `hierarchy_mixed` = reproducibility check.
- Correctly states the M3–M4 relationship as refinement, not overturning.
- Correctly preserves clean-environment reproducibility as an open boundary (Non-Claim #3, Threat #2).
- Correctly avoids citing the R29 erroneous table cell (Section 10, Section 6 precision note).
- Correctly avoids claiming R28 is resolved (Section 10).
- Does not contain any mock, stub, hardcoded, or fabricated content.
- Does not claim the paper has been accepted, submitted, or achieved SOTA.
- Numeric anchors in Section 12 match reviewed T32/T33/T42 artifact values exactly.

## Verification of Task Completion

Checked against the T50 task package requirements:

| Requirement | Status |
| --- | --- |
| New `docs/paper_outline.md` created | Done |
| Working title + one-paragraph positioning | Done (Section 1–2) |
| Central claim + non-claim boundaries | Done (Section 3, 5 non-claims) |
| 3–5 paper contributions | Done (Section 4, C1–C5) |
| Evidence ladder (M1–M4) | Done (Section 5, with M3–M4 relationship and per-split roles) |
| Figures/tables plan | Done (Section 6, 4 figures + 7 tables + precision note) |
| Threats to validity | Done (Section 7, 10 threats across internal/external/construct) |
| Venue fit (ITP/CPP/FM) | Done (Section 8, with prioritization) |
| Proof-side bridge | Done (Section 9, with 3 candidate MVPs and recommendation) |
| `explicit_only` = primary evidence | Enforced throughout |
| `synthesized_only` = controlled diagnostic | Enforced throughout |
| `hierarchy_mixed` = reproducibility check | Enforced throughout |
| M3–M4 relationship clarified | Done (Section 5, "M3–M4 Relationship") |
| Clean-environment reproducibility boundary preserved | Done (Non-Claim #3, Threat #2) |
| R28/R29 bypassed correctly | Done (Section 6 precision note, Section 10) |
| Governance docs updated | Done (04, 05, 07, 08) |
| No new experiments, code changes, or semantic modifications | Confirmed |
| Worker did not mark task complete | Confirmed |

All T50-specific notes from the task package are satisfied.

## Recommended Next Action

1. Captain marks T50 as complete.
2. Captain updates D030 status from "Pending review" to "Accepted".
3. Captain sets current unique task to T51 (proof-side utility MVP selection).
4. When staging for commit, exclude `.claude/settings.json` as usual.
5. Consider whether R30 warrants merging C1+C5 before entering T51, or defer to paper drafting phase.
