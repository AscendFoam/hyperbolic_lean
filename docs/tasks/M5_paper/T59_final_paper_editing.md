# T59 Final Paper Editing And Venue Shaping

## Task ID

T59

## Goal

Turn the reviewed paper-facing assets into a venue-shaped final draft set, without running any new experiments.

This task should:

1. Harmonize contribution structure, page-budget language, and submission-facing terminology across `paper_draft`, `paper_outline`, `paper_figures_and_tables`, and `paper_artifact_package`.
2. Decide whether the current 5-contribution structure should remain as-is or be merged/tightened for venue budget; if changed, apply the change consistently across all paper-facing docs.
3. Absorb the two non-blocking notes from `docs/review/T58_review.md`:
   - standardize the artifact-package wording around "5 core tables" versus "4 core tables + 1 summary table"
   - make Table T1's HGCN source mapping precise by treating `T33` as the primary source and `T42` as cross-check / corroboration, rather than leaving a compound `T33/T42` phrasing
4. Preserve the provenance-conditional claim boundary and avoid introducing any new numbers, claims, or evidence classes.

## Why Now

`docs/review/T58_review.md` gave `PASS`. That means artifact packaging is good enough to treat as closed.

The next bottleneck is no longer packaging completeness. It is final paper coherence:

1. paper-facing documents still need one submission-facing terminology pass
2. contribution count / page-budget pressure (`R30`) is still active
3. T58 review left two non-blocking wording issues that fit naturally into final paper editing

This is still a Narrow-phase task. Do not reopen experiments, demos, or data generation.

## Allowed Files

- `docs/paper_draft.md`
- `docs/paper_outline.md`
- `docs/paper_figures_and_tables.md`
- `docs/paper_artifact_package.md`
- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope

- No new experiments, seed sweeps, traces, split generation, model training, or demos
- No edits under `project_bootstrap/`, `data/`, or `artifacts/`
- Do not rewrite `docs/02_experiment_plan.md`
- Do not modify review files under `docs/review/`
- Do not introduce any unreviewed number, claim, or figure/table conclusion
- Do not mark `R25`, `R30`, or `R08` as closed in this round
- Do not add PNG, SVG, PDF, PPT, or other binary submission assets
- Do not modify `.claude/settings.json`, and do not include it in any commit

## Inputs to Read

- `docs/02_experiment_plan.md`
- `docs/review/T58_review.md`
- `docs/paper_draft.md`
- `docs/paper_outline.md`
- `docs/paper_figures_and_tables.md`
- `docs/paper_artifact_package.md`
- `docs/experiment_reports/provenance_summary.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Expected Output

### 1. Venue-Shaped Paper-Facing Sync

Update:

- `docs/paper_draft.md`
- `docs/paper_outline.md`
- `docs/paper_figures_and_tables.md`
- `docs/paper_artifact_package.md`

Bring them into one consistent submission-facing state:

1. contributions / section structure agree
2. table inventory terminology agrees
3. central claim remains provenance-conditional
4. wording is compressed enough for venue-facing use without deleting reviewed caveats

### 2. Contribution-Count / Page-Budget Decision

Make one explicit choice:

1. keep the current 5-contribution structure, but tighten wording so it reads as page-budget-aware, or
2. merge / collapse one or more contributions for a narrower venue-facing story

Whichever choice you make, it must be applied consistently across:

- `docs/paper_outline.md`
- `docs/paper_draft.md`
- `docs/paper_artifact_package.md`

Do not leave mixed contribution counts or stale labels behind.

### 3. T58 Review Non-Blocking Cleanup

At minimum:

1. standardize `docs/paper_artifact_package.md` so the table inventory uses one consistent phrasing
2. make Table T1's HGCN source mapping precise enough that a reviewer can tell `T33` is the primary reviewed source and `T42` is only a corroborating cross-check

Do not change any reviewed numeric value.

### 4. Governance Sync

Update:

- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

At minimum, record:

- `T58_review` is `PASS`
- `T58` is complete
- `T59` is the current unique task
- `T58_review` non-blocking notes were folded into `T59`
- the current phase is still final paper editing / venue shaping, not new experiments

## Acceptance Criteria

1. `paper_draft`, `paper_outline`, `paper_figures_and_tables`, and `paper_artifact_package` no longer disagree about contribution structure or table inventory terminology
2. `docs/paper_artifact_package.md` makes Table T1's HGCN source relationship precise enough for audit (`T33` primary, `T42` cross-check)
3. Any contribution-count / page-budget adjustment is applied consistently across all paper-facing docs
4. All governance entry points show `T59` as the current unique task and `T58` as completed
5. No new experiment, artifact modification, or unreviewed number was introduced

## Verification

```powershell
rg -n "contribution|contributions|C1|C2|C3|C4|C5|venue|page|budget" docs\paper_draft.md docs\paper_outline.md docs\paper_artifact_package.md
rg -n "5 core tables|4 core tables|summary table|T33/T42|T33|T42|HGCN" docs\paper_artifact_package.md docs\paper_figures_and_tables.md
rg -n "T58|T59|PASS|venue shaping|R25|R30|R08" docs\00_raw_idea.md docs\01_feasibility_report.md docs\03_architecture.md docs\04_task_board.md docs\05_decision_log.md docs\06_eval_protocol.md docs\07_handoff.md docs\08_risks_and_open_questions.md
```

The worker report must also state:

- whether the 5-contribution structure was kept or merged
- how the core-table terminology was standardized
- how Table T1's HGCN source mapping was made more precise

## Docs To Update

- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type

adversarial
