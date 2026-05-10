# hyperbolic_lean

`hyperbolic_lean` is a proof-engineering research repo for building a reproducible benchmark, protocol, and diagnostics pipeline over traced Lean/Mathlib hierarchy graphs.

## Current Positioning

The current main line is:

- benchmark / protocol / diagnostics
- grouped multi-positive ancestor retrieval
- graph-structure diagnosis before larger model claims
- strong relation-aware Euclidean baselines before hyperbolic follow-up

This repo is not currently claiming:

- that HGCN has already been shown to beat GCN on real traced Lean hierarchy graphs
- end-to-end theorem proving
- full-Mathlib tracing as a prerequisite for every next step

## Important Directories

- `docs/`: project governance, plan, task board, evaluation protocol, handoff, risks
- `docs/tasks/`: worker task packages with allowed files, forbidden scope, and verification
- `docs/review/`: reviewer outputs
- `project_bootstrap/`: existing prototype packages and scaffolds
- `artifacts/`: diagnostics, baselines, graphs, logs, inventories, and related outputs
- `data/`: local data assets used by experiments

## How To Start A Work Cycle

Read in this order:

1. `README.md`
2. `AGENTS.md`
3. `docs/02_experiment_plan.md`
4. `docs/04_task_board.md`
5. `docs/07_handoff.md`
6. `docs/08_risks_and_open_questions.md`

Then follow the single-task loop:

1. Captain selects the `Current Unique Task` from `docs/04_task_board.md`.
2. Worker only executes the task package in `docs/tasks/`.
3. Reviewer performs read-only review and returns `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`.
4. Captain updates the governance docs after review and only then advances to the next task.

## Current Unique Task Entry

The current task entry is maintained in:

- `docs/04_task_board.md`
- `docs/tasks/M1_protocol/T11_data_card.md`

As of 2026-05-10, `T10` has passed review and the current worker scope is `T11` until that round is reviewed and closed.
