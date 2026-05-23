# T60 Venue Formatting And Final Submission Asset Shaping

## Task ID

T60

## Goal

Turn the current paper-facing document set into a cleaner submission-facing asset set, without running any new experiments.

This task should:

1. Sync the submission checklist state in `docs/paper_artifact_package.md` with the actual T59 decisions.
2. Clarify the `Page Budget Note` so the draft stays self-consistent if C3 or C5 is compressed or moved to an appendix.
3. Keep `paper_draft`, `paper_outline`, `paper_figures_and_tables`, and `paper_artifact_package` aligned on what belongs in main text versus appendix / supplementary material.
4. Preserve all reviewed numbers, claim boundaries, and provenance-conditional wording.

## Why Now

`docs/review/T59_review.md` gave `PASS`. That means final paper editing / venue shaping is complete enough to treat as closed.

The remaining work is narrower and more submission-facing:

1. `paper_artifact_package.md` still has a checklist-state sync gap around `R30 page budget check`
2. `paper_outline.md` still leaves one page-budget compression path under-explained
3. these are final asset-shaping issues, not experiment or claim issues

This is still a Narrow-phase task. Do not reopen experiments, data, demo scope, or numerical analysis.

## Allowed Files

- `docs/paper_artifact_package.md`
- `docs/paper_outline.md`
- `docs/paper_draft.md`
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
- Do not add PNG, SVG, PDF, PPT, or other binary submission assets
- Do not modify `.claude/settings.json`, and do not include it in any commit

## Inputs To Read

- `docs/02_experiment_plan.md`
- `docs/review/T59_review.md`
- `docs/paper_artifact_package.md`
- `docs/paper_outline.md`
- `docs/paper_draft.md`
- `docs/paper_figures_and_tables.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Expected Output

### 1. Checklist Sync

Update:

- `docs/paper_artifact_package.md`

At minimum:

1. bring `R30 page budget check` into a state consistent with the actual reviewed T59 decision
2. if you mark it complete, make clear that this means "decision recorded and synchronized", not "R30 risk fully closed"
3. if you keep it incomplete, explain precisely why the reviewed T59 decision is still insufficient

Do not leave a silent mismatch between checklist state and reviewed facts.

### 2. Page-Budget Note Clarification

Update:

- `docs/paper_outline.md`

Clarify how the paper remains self-consistent if C3 or C5 is compressed, moved to appendix, or demoted in the main text.

At minimum, the note should answer:

1. what stays in the main story
2. what can move out
3. why the central claim and contribution structure still hold

### 3. Main-Text Vs Appendix Consistency

Update as needed:

- `docs/paper_draft.md`
- `docs/paper_figures_and_tables.md`
- `docs/paper_artifact_package.md`

Only change them if needed so they agree with the clarified Page Budget Note and checklist state.

Do not introduce new figures, new tables, or new claims.

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

- `T59_review` is `PASS`
- `T59` is complete
- `T60` is the current unique task
- `T59_review` non-blocking notes were folded into `T60`
- the current phase is still submission-facing cleanup, not new experiments

## Acceptance Criteria

1. `paper_artifact_package.md` no longer has a silent mismatch between the `R30 page budget check` checklist state and the reviewed T59 decision
2. `paper_outline.md` explains the page-budget compression path clearly enough that C3/C5 appendix demotion would still leave a coherent main story
3. `paper_draft`, `paper_figures_and_tables`, and `paper_artifact_package` do not contradict that page-budget clarification
4. All governance entry points show `T60` as the current unique task and `T59` as completed
5. No new experiment, artifact modification, or unreviewed number was introduced

## Verification

```powershell
rg -n "R30 page budget check|Page Budget Note|appendix|C3|C5|main text|正文" docs\paper_artifact_package.md docs\paper_outline.md docs\paper_draft.md
rg -n "T59|T60|PASS|submission asset|venue-formatting|R25|R30|D23" docs\00_raw_idea.md docs\01_feasibility_report.md docs\03_architecture.md docs\04_task_board.md docs\05_decision_log.md docs\06_eval_protocol.md docs\07_handoff.md docs\08_risks_and_open_questions.md
```

The worker report must also state:

- whether `R30 page budget check` was marked complete or kept open, and why
- how the Page Budget Note was clarified
- whether any main-text / appendix placement wording changed in `paper_draft` or `paper_figures_and_tables`

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
