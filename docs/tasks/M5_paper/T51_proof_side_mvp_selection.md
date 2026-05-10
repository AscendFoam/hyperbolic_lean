# T51 Proof-Side MVP Selection

## Task ID
T51

## Goal
选择一个 proof-side utility MVP，例如 ancestor explanation 或 relation-aware declaration recommendation。

## Why Now
项目若能连接 proving workflow，论文价值会强于纯 link prediction benchmark。

## Allowed Files
- `docs/proof_side_mvp.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不实现 demo
- 不承诺端到端 theorem proving
- 不引入新大型依赖

## Inputs to Read
- `docs/paper_outline.md`
- `docs/基于深度调研报告的项目定位与创新方向修订.md`
- relevant proof-side literature notes in `docs/深度调研报告.md`

## Expected Output
- proof-side MVP 比较与选择结论。
- 明确输入、输出、验收标准和失败标准。

## Verification
```powershell
rg -n "ancestor explanation|declaration recommendation|premise retrieval|MVP|failure" docs\proof_side_mvp.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
normal
