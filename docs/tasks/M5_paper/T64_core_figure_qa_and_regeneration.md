# T64 Core Figure QA And Regeneration

## Task ID

T64

## Goal

Complete the final visual QA pass for the two reviewed core figures rendered in `T63`, and regenerate figure styling/annotations only if needed.

This task should:

1. Visually inspect `F1_provenance_structure.png` and `F2_hop_depth_delta.png` against `docs/paper_figures_and_tables.md`.
2. Fix only figure styling, layout, annotation, or readability issues.
3. Keep all reviewed values, claim boundaries, and provenance-conditional conclusions unchanged.
4. Record the QA result and any remaining bundle delta in `paper/itp/README.md`.

## Why Now

`docs/review/T63_review.md` returned `PASS_WITH_WARNINGS`.

The LaTeX source tree exists, but the reviewer identified two figure-specific follow-ups that should be closed before any final submission bundle work:

1. `F2` could not be independently visually verified.
2. `F1` shows a panel-scale inconsistency and a stray `1 1` label artifact.

This is the right narrow task to close those issues. Do not reopen experiments, paper drafting, or bundle assembly.

## Allowed Files

- `paper/itp/figures/F1_provenance_structure.png`
- `paper/itp/figures/F2_hop_depth_delta.png`
- `paper/itp/README.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/venue_submission_plan.md`

## Forbidden Scope

- No new experiments, seed sweeps, traces, split generation, or demos
- No edits under `project_bootstrap/`, `data/`, or `artifacts/`
- Do not rewrite `docs/02_experiment_plan.md`
- Do not modify review files under `docs/review/`
- Do not modify `docs/paper_draft.md`, `docs/paper_outline.md`, `docs/paper_figures_and_tables.md`, or `docs/paper_artifact_package.md`
- Do not introduce any unreviewed number, claim, or figure/table conclusion
- Do not mark `R25`, `R30`, `R08`, or `R34` as closed in this round
- Do not assemble the final submission bundle, zip package, or CPP branch in this round
- Do not modify `.claude/settings.json`, and do not include it in any commit

## Inputs To Read

- `docs/review/T63_review.md`
- `docs/paper_figures_and_tables.md`
- `paper/itp/README.md`
- `paper/itp/main.tex`
- `docs/venue_submission_plan.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Expected Output

### 1. Figure QA / Regeneration

Inspect both rendered figures visually and regenerate only if needed to fix readability issues.

### 2. README Update

`paper/itp/README.md` must record:

- what visual QA was performed
- whether either figure was regenerated
- what, if anything, remains before a final submission bundle can be assembled

### 3. Governance Sync

Update the governance docs so they show:

- `T63_review` is `PASS_WITH_WARNINGS`
- `T63` is complete
- `T64` is the current unique task
- the current phase is core figure QA / regeneration, not venue choice and not final bundle assembly

## Acceptance Criteria

1. `F1_provenance_structure.png` and `F2_hop_depth_delta.png` are visually checked against the reviewed specs
2. Any figure changes are limited to style, layout, or annotation readability
3. `paper/itp/README.md` records the QA result and remaining bundle delta
4. Governance docs show `T63` complete and `T64` current
5. No new experiment, artifact modification, or unreviewed number was introduced

## Verification

```powershell
rg -n "T63|T64|PASS_WITH_WARNINGS|figure|visual|regenerat|core figure|submission bundle|R25|R30|R08|R34" paper\itp\README.md docs\03_architecture.md docs\04_task_board.md docs\05_decision_log.md docs\07_handoff.md docs\08_risks_and_open_questions.md docs\venue_submission_plan.md
```

The worker report must also state:

- what visual QA check was performed on each figure
- whether either figure was regenerated
- what remains before final bundle assembly

## Docs To Update

- `paper/itp/figures/F1_provenance_structure.png`
- `paper/itp/figures/F2_hop_depth_delta.png`
- `paper/itp/README.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/venue_submission_plan.md`

## Reviewer Type

adversarial
