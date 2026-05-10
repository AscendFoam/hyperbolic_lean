# AGENTS

This repository uses a Captain / Worker / Reviewer workflow. The repository files are the source of truth; chat sessions are only temporary executors.

## Roles

### Captain

- Reads the governance docs and keeps the project aligned with the current positioning.
- Maintains `docs/04_task_board.md`, `docs/07_handoff.md`, and related governance files after review.
- Decomposes work into task packages under `docs/tasks/`.
- Chooses exactly one `Current Unique Task` at a time.

### Worker

- Executes only the task package assigned for the current round.
- Modifies only the task package's `Allowed files`.
- Does not claim the next task automatically.
- Runs the required verification, or clearly states why it could not be run.
- Reports what changed, how it was verified, and any remaining risks.

### Reviewer

- Performs read-only review of the diff.
- Checks task completion, scope compliance, verification quality, regressions, pseudo-implementation risk, and documentation accuracy.
- Returns `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`.

## Non-Negotiable Rules

1. Only one current task is active at a time.
2. The task package is the execution boundary for the worker.
3. `Allowed files` are the only files a worker may edit in that round.
4. `Forbidden scope` must not be touched even if it looks nearby or tempting.
5. Plans, placeholders, mocks, and future ideas must not be written up as completed facts.
6. Review happens before Captain marks a task complete and advances the board.

## Task Package Contract

Each worker task package should define:

- `Task ID`
- `Goal`
- `Why now`
- `Allowed files`
- `Forbidden scope`
- `Inputs to read`
- `Expected output`
- `Verification`
- `Docs to update`
- `Reviewer type`

If a file is not listed in `Allowed files`, the worker should treat it as out of scope.

## Verification And Review

- Workers must run the task package verification command when feasible.
- If verification is manual, the worker should state the exact manual acceptance checks performed.
- Review is read-only by default.
- High-risk tasks should use adversarial review.

High-risk work includes:

- core algorithm changes
- experiment metrics or protocol changes
- data pipeline changes
- architecture migration
- legacy result migration
- resume-facing evidence claims

## Current Governance Entry Points

- `docs/04_task_board.md`: current unique task and milestone board
- `docs/07_handoff.md`: current project handoff for the next Captain / Worker / Reviewer
- `docs/08_risks_and_open_questions.md`: active risks and unresolved questions
- `docs/reference/AI_coding_workflow.md`: workflow reference
