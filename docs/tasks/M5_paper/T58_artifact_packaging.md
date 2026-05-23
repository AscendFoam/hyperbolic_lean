# T58 Artifact Packaging

## Task ID

T58

## Goal

Create a submission-facing artifact package from the paper-facing assets that were stabilized by T57, without running any new experiments.

This task should:

1. Create one packaging document that maps paper claims, tables, and figures back to reviewed source documents.
2. Fix the stale "Pending sync" rows still left in `docs/paper_figures_and_tables.md` Section 4.
3. Make the source-to-claim relationship across `paper_draft`, `paper_outline`, `paper_figures_and_tables`, and `provenance_summary` easier to audit.
4. Decide whether `docs/paper_draft.md` Section 5.4 should keep its current compressed wording or restore one short mechanistic sentence, without reopening R28/R29.

## Why Now

`docs/review/T57_review.md` gave `PASS`. That means the figure/table source rendering is complete enough to move on; the next rational step is packaging, not redoing T57.

The T57 review left two non-blocking follow-ups that fit naturally into packaging / final paper editing:

1. `docs/paper_figures_and_tables.md` Section 4 still has two stale "Pending sync" rows.
2. `docs/paper_draft.md` Section 5.4 may want one short mechanistic detail restored, but only if it improves final readability without expanding back into a long note.

## Allowed Files

- `docs/paper_artifact_package.md`
- `docs/paper_draft.md`
- `docs/paper_outline.md`
- `docs/paper_figures_and_tables.md`
- `docs/experiment_reports/provenance_summary.md`
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
- Do not introduce any unreviewed number, claim, or figure/table conclusion
- Do not mark `R25` or `R30` as closed
- Do not add PNG, SVG, PDF, PPT, or other binary submission assets
- Do not modify `.claude/settings.json`, and do not include it in any commit

## Inputs to Read

- `docs/02_experiment_plan.md`
- `docs/review/T57_review.md`
- `docs/paper_draft.md`
- `docs/paper_outline.md`
- `docs/paper_figures_and_tables.md`
- `docs/experiment_reports/provenance_summary.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Expected Output

### 1. Packaging Doc

Create:

- `docs/paper_artifact_package.md`

It must include at least:

1. artifact package scope
2. source documents inventory
3. claim-to-source mapping
4. table/figure-to-source mapping
5. known exclusions and active boundaries
6. submission / handoff checklist

It should make clear:

- which files are paper-facing source-of-truth documents
- which files are backing evidence only
- which risks remain active and must not be written as closed
- which files belong in later submission shaping and which do not

### 2. Source Doc Self-Consistency Fix

Update:

- `docs/paper_figures_and_tables.md`

At minimum:

1. Replace the two stale "Pending sync" rows in Section 4 with wording that matches the already-updated `docs/paper_outline.md`
2. Do not change any reviewed number
3. If you add a status label, tie it explicitly to T56/T57 reviewed sync

### 3. Final Paper-Editing Decision

Update:

- `docs/paper_draft.md`

Do one of these two options, and make the choice explicit:

1. Keep the current compressed Section 5.4 wording and record in `docs/paper_artifact_package.md` why that wording is sufficient
2. Restore one short mechanistic sentence such as "each query has exactly one positive ancestor and the candidate pool is small", but do not re-expand into a long explanatory paragraph and do not introduce new numbers

### 4. Optional Sync If Needed

Update only if needed for consistency:

- `docs/paper_outline.md`
- `docs/experiment_reports/provenance_summary.md`

Only change them if required for source-to-claim consistency or status wording consistency. Do not add new numbers or new conclusions.

### 5. Governance Sync

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

- `T58` is the current unique task
- `T57_review` is `PASS`
- the T57 non-blocking notes were folded into `T58`
- the next category after T58 is final paper editing / venue shaping, not new experiments

## Acceptance Criteria

1. `docs/paper_artifact_package.md` exists and contains artifact scope, source mapping, known exclusions, and checklist content
2. `docs/paper_figures_and_tables.md` Section 4 no longer contains the stale "Pending sync" rows called out by review
3. `docs/paper_draft.md` Section 5.4 has an explicit final state for the mechanistic-detail decision
4. The source-to-claim relationship across paper-facing docs is clearer after the task, not more scattered
5. All governance entry points show `T58` as the current unique task
6. No new experiment, no artifact modification, and no unreviewed number was introduced

## Verification

```powershell
rg -n "^## |^### |artifact|package|submission|checklist|source|claim|Figure|Table" docs\paper_artifact_package.md docs\paper_figures_and_tables.md docs\paper_draft.md docs\paper_outline.md
rg -n "Pending sync|Aligned|grouped_test_map|test_average_precision|1\.0000 ± 0\.0000|\+0\.3143" docs\paper_figures_and_tables.md docs\paper_draft.md docs\paper_outline.md docs\experiment_reports\provenance_summary.md
rg -n "T57|T58|PASS|artifact packaging|R25|R30|D21" docs\00_raw_idea.md docs\01_feasibility_report.md docs\03_architecture.md docs\04_task_board.md docs\05_decision_log.md docs\06_eval_protocol.md docs\07_handoff.md docs\08_risks_and_open_questions.md
```

The worker report must also state:

- which documents were treated as source-of-truth vs backing evidence
- how the stale T57 review rows were resolved
- whether the Section 5.4 mechanistic detail was kept compressed, restored briefly, or intentionally omitted

## Docs to Update

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
