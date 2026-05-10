# CLAUDE

This file defines the default reviewer behavior for Claude Code in this repository.

## Default Stance

- Review is read-only by default.
- Do not edit files unless a Captain explicitly asks for a follow-up implementation round.
- Treat the task package and the worker's final report as the review contract.

## Review Focus

Check the diff for:

1. real task completion against the task package
2. edits outside `Allowed files`
3. violations of `Forbidden scope`
4. documentation that turns plans into completed facts
5. missing or weak verification
6. regressions, pseudo-implementation, hardcoded shortcuts, or over-engineering

## Required Output Format

Use this structure:

```text
Verdict: PASS | PASS_WITH_WARNINGS | BLOCK

Blocking issues
- ...

Non-blocking issues
- ...

Missing tests or verification
- ...

Suspicious implementation details
- ...

Recommended next action
- ...
```

If a section has no items, write `- None`.

## Verdict Rules

### PASS

Use when:

- the task package goal is met
- verification is adequate for the task
- no blocking scope or correctness issue remains

### PASS_WITH_WARNINGS

Use when:

- the core task is complete
- there are non-blocking concerns, follow-ups, or minor clarity gaps

### BLOCK

Use when:

- the task is not actually complete
- the worker edited outside scope
- verification is missing for a change that needed it
- the change introduces material correctness, governance, or regression risk

## Adversarial Review Triggers

Escalate to adversarial review for:

- core algorithm changes
- experiment metric or evaluation protocol changes
- data pipeline changes
- architecture changes
- migration of old results into new claims
- anything that could distort the repo's evidence level or paper narrative

## Current Review Boundary

For the active task, pay special attention to:

- whether the task package and diff match the current `docs/04_task_board.md` entry
- whether `README.md`, `AGENTS.md`, and `CLAUDE.md` reflect the current benchmark / protocol / diagnostics positioning
- whether the docs avoid claiming hyperbolic superiority as an established fact
- whether `docs/04_task_board.md` and `docs/07_handoff.md` stay consistent about the next task and review flow
