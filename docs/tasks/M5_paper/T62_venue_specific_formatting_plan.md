# T62 Venue-Specific Formatting And Submission Plan

## Task ID

T62

## Goal

Use the frozen repo package and venue roadmap to choose the primary submission venue path and turn it into a venue-specific formatting / submission checklist.

This task should:

1. Pick the primary venue track from the existing roadmap context, or make the venue priority explicit enough for the next formatting step.
2. Record what formatting / boilerplate / submission-assets still need to change before an actual venue-specific build.
3. Keep the current paper-facing claim boundary frozen unless a tiny wording sync is required to express the chosen venue constraints.

## Why Now

`docs/review/T61_review.md` gave `PASS`. The repo package boundary and handoff freeze are now complete, so the next bottleneck is not evidence gathering or repo hygiene. The next useful step is to decide how the frozen submission-facing assets should be shaped for a concrete venue path.

This is still a Narrow-phase task. Do not reopen experiments, data, demos, or proof-side scope.

## Allowed Files

- `docs/venue_submission_plan.md`
- `docs/paper_artifact_package.md`
- `docs/paper_draft.md`
- `docs/paper_outline.md`
- `docs/paper_figures_and_tables.md`
- `docs/投稿路线图（FM-ITP-CPP-备选 venue 对照）.md`
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

## Inputs To Read

- `docs/review/T61_review.md`
- `docs/paper_artifact_package.md`
- `docs/paper_draft.md`
- `docs/paper_outline.md`
- `docs/paper_figures_and_tables.md`
- `docs/投稿路线图（FM-ITP-CPP-备选 venue 对照）.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Expected Output

### 1. Venue Choice / Priority

State the primary venue path clearly enough for the next worker to know which formatting target is being prepared.

### 2. Submission Checklist

Write a concise checklist of the remaining venue-specific formatting / packaging deltas.

### 3. Asset Delta Note

Record whether any paper-facing wording or asset placement needs to move for the chosen venue.

### 4. Governance Sync

Update the governance docs so they show:

- `T61_review` is `PASS`
- `T61` is complete
- `T62` is the current unique task
- the current phase is venue-specific formatting / submission planning, not new experiments

## Acceptance Criteria

1. The primary venue path is explicit
2. The remaining venue-specific deltas are documented as a checklist
3. Any paper-facing wording changes are minimized and clearly bounded
4. All governance entry points show `T62` as the current unique task and `T61` as complete
5. No new experiment, artifact modification, or unreviewed number was introduced

## Verification

```powershell
rg -n "T61|T62|PASS|venue|formatting|submission|checklist|roadmap|R25|R30|R08" docs\00_raw_idea.md docs\01_feasibility_report.md docs\03_architecture.md docs\04_task_board.md docs\05_decision_log.md docs\06_eval_protocol.md docs\07_handoff.md docs\08_risks_and_open_questions.md docs\venue_submission_plan.md docs\投稿路线图（FM-ITP-CPP-备选 venue 对照）.md
```

The worker report must also state:

- which venue path is being treated as primary
- what formatting / submission deltas remain after T61
- whether any paper-facing wording or asset placement changed

## Docs To Update

- `docs/venue_submission_plan.md`
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
