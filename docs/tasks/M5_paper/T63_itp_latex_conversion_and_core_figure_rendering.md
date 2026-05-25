# T63 ITP-Targeted LaTeX Conversion And Core Figure Rendering

## Task ID

T63

## Goal

Turn the reviewed submission-facing paper assets into a single ITP-targeted LaTeX source tree and render the two core figures needed by the paper narrative.

This task should:

1. Create one coherent LaTeX source tree under `paper/itp/`.
2. Convert the current paper draft into LaTeX without changing reviewed numeric values or claim boundaries.
3. Render Figure F1 and Figure F2 from the reviewed specs in `docs/paper_figures_and_tables.md`.
4. Record the template assumption, compile verification, and remaining delta to final submission bundle in `paper/itp/README.md`.

## Why Now

`docs/review/T62_review.md` gave `PASS`. The venue path is now explicit: ITP is primary, CPP is co-primary, and FM is only a stretch target.

That means the next bottleneck is no longer venue choice. The next bottleneck is that the repo still lacks a single checkable LaTeX source tree and rendered core figures. At the same time, it is still too early to do the final submission bundle assembly in the same round, because mixing template conversion, figure rendering, and bundle packaging would make the task boundary too wide.

This is still a Narrow-phase task. Do not reopen experiments, artifact generation outside the two reviewed figures, or paper-facing claim changes.

## Allowed Files

- `paper/itp/main.tex`
- `paper/itp/README.md`
- `paper/itp/references.bib`
- `paper/itp/figures/F1_provenance_structure.png`
- `paper/itp/figures/F2_hop_depth_delta.png`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/venue_submission_plan.md`

## Forbidden Scope

- No new experiments, seed sweeps, traces, split generation, or demo changes
- No edits under `project_bootstrap/`, `data/`, or `artifacts/`
- Do not rewrite `docs/02_experiment_plan.md`
- Do not modify review files under `docs/review/`
- Do not modify `docs/paper_draft.md`, `docs/paper_outline.md`, `docs/paper_figures_and_tables.md`, or `docs/paper_artifact_package.md`
- Do not introduce any unreviewed number, claim, or figure/table conclusion
- Do not mark `R25`, `R30`, `R08`, or `R34` as closed in this round
- Do not assemble the final submission bundle, zip package, or CPP branch in this round
- Do not modify `.claude/settings.json`, and do not include it in any commit

## Inputs To Read

- `docs/review/T62_review.md`
- `docs/venue_submission_plan.md`
- `docs/paper_draft.md`
- `docs/paper_outline.md`
- `docs/paper_figures_and_tables.md`
- `docs/paper_artifact_package.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Expected Output

### 1. Single ITP-Targeted LaTeX Source Tree

Create a single LaTeX source tree rooted at `paper/itp/main.tex`. It must be clear how the reviewed paper draft maps into the LaTeX structure.

The source tree may stay minimal, but it must be coherent enough that a reviewer can inspect:

- title / abstract / section structure
- bibliography wiring
- figure inclusion points
- preservation of the reviewed claim boundary

### 2. Core Figure Rendering

Render the two reviewed core figures:

- `F1_provenance_structure.png`
- `F2_hop_depth_delta.png`

They must follow the exact reviewed specs in `docs/paper_figures_and_tables.md`. Do not invent new axes, captions, or numeric values.

### 3. README For Template Assumption And Remaining Delta

`paper/itp/README.md` must record:

- what ITP-targeted template assumption was used for this round
- whether the LaTeX file compiled locally
- what command was used for verification
- what remains before a final submission bundle can be assembled

### 4. Governance Sync

Update the relevant governance docs so they show:

- `T62_review` is `PASS`
- `T62` is complete
- `T63` is the current unique task
- the current phase is ITP-targeted LaTeX conversion / core figure rendering, not venue choice and not final bundle assembly

## Acceptance Criteria

1. `paper/itp/main.tex` exists and reflects the reviewed paper structure without introducing new claims or numbers
2. `paper/itp/figures/F1_provenance_structure.png` and `paper/itp/figures/F2_hop_depth_delta.png` exist
3. The LaTeX source references the rendered figures in the expected places
4. `paper/itp/README.md` clearly records template assumption, compile verification, and remaining bundle delta
5. Governance docs show `T62` complete and `T63` current
6. No reviewed markdown source-of-truth document was rewritten in this round

## Verification

```powershell
rg -n "documentclass|title|abstract|section|includegraphics|bibliography|ITP|R25|R30|F1|F2" paper\itp\main.tex paper\itp\README.md paper\itp\references.bib docs\03_architecture.md docs\04_task_board.md docs\05_decision_log.md docs\07_handoff.md docs\08_risks_and_open_questions.md docs\venue_submission_plan.md
```

If a local TeX runtime is available, also compile the file and report the exact command and result.

If compilation is not feasible, the worker report must state the exact blocker. "Did not try" is not acceptable.

## Docs To Update

- `paper/itp/main.tex`
- `paper/itp/README.md`
- `paper/itp/references.bib`
- `paper/itp/figures/F1_provenance_structure.png`
- `paper/itp/figures/F2_hop_depth_delta.png`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/venue_submission_plan.md`

## Reviewer Type

adversarial
