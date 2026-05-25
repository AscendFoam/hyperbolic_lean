# T61 Final Repo Packaging And Handoff Freeze

## Task ID

T61

## Goal

Freeze the final repository handoff package after `T60_review` returned `PASS`, without running any new experiments.

This task should:

1. Make the final repo package boundary explicit: what stays as committed handoff material, what is only explanatory helper text, and what should not be treated as a new research claim.
2. Keep `docs/for_human/T60_review_explanation.md` and `docs/worker_summary/T60_worker_summary.md` as committed handoff-facing aids, and label them clearly as explanatory materials rather than research artifacts.
3. Ensure the governance docs point clearly to `T61` as the current unique task and describe the repo freeze as the next step after `T60`.
4. Preserve all reviewed paper-facing assets and all reviewed numeric values as-is.

## Why Now

`docs/review/T60_review.md` gave `PASS`. That means submission-facing cleanup is complete enough to stop reopening the paper story.

The remaining work is repository-level packaging and handoff freeze:

1. making the next maintainer's entry path obvious,
2. keeping the final repo boundary explicit so the package does not drift back into active paper editing,
3. preserving the two handoff-facing helper docs as committed explanatory aids rather than new research outputs.

This is still a Narrow-phase task. Do not reopen experiments, data, or paper-facing claim boundaries.

## Allowed Files

- `docs/for_human/T60_review_explanation.md`
- `docs/worker_summary/T60_worker_summary.md`
- `docs/paper_artifact_package.md`
- `docs/paper_draft.md`
- `docs/paper_outline.md`
- `docs/paper_figures_and_tables.md`
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
- Do not add binary assets
- Do not modify `.claude/settings.json`, and do not include it in any commit

## Inputs To Read

- `docs/review/T60_review.md`
- `docs/for_human/T60_review_explanation.md`
- `docs/worker_summary/T60_worker_summary.md`
- `docs/paper_artifact_package.md`
- `docs/paper_draft.md`
- `docs/paper_outline.md`
- `docs/paper_figures_and_tables.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Expected Output

### 1. Repo Package Boundary

Clarify which files are:

- final repo package / committed handoff material
- explanatory handoff-only aids
- still-active risks or boundaries that must remain open

### 2. Handoff Note Decision

Keep `docs/for_human/T60_review_explanation.md` and `docs/worker_summary/T60_worker_summary.md` in the repo as handoff-facing aids.

Make their role explicit so they are not mistaken for new claims or research artifacts.

### 3. Governance Freeze

Update the governance docs so they clearly state:

- `T60_review` is `PASS`
- `T60` is complete
- `T61` is the current unique task
- the current phase is final repo packaging / handoff freeze

### 4. Paper-Facing Assets

Do not change reviewed numbers or claims.

Only touch `paper_artifact_package`, `paper_draft`, `paper_outline`, or `paper_figures_and_tables` if a small wording sync is absolutely needed for the final repo package boundary.

## Acceptance Criteria

1. The final repo package boundary is explicit and auditable
2. The role of `docs/for_human/T60_review_explanation.md` and `docs/worker_summary/T60_worker_summary.md` is decided and documented
3. All governance entry points show `T61` as the current unique task and `T60` as complete
4. No new experiment, artifact modification, or unreviewed number was introduced

## Verification

```powershell
rg -n "T60|T61|PASS|repo packaging|handoff freeze|final repo package|for_human|worker_summary|R25|R30|R08" docs\00_raw_idea.md docs\01_feasibility_report.md docs\03_architecture.md docs\04_task_board.md docs\05_decision_log.md docs\06_eval_protocol.md docs\07_handoff.md docs\08_risks_and_open_questions.md docs\for_human\T60_review_explanation.md docs\worker_summary\T60_worker_summary.md
```

The worker report must also state:

- that the two T60 helper docs were kept as committed handoff-facing aids
- how the final repo package boundary was clarified
- whether any paper-facing wording had to move in order to keep the handoff freeze consistent

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
