# T31 Minimal Query-Grouped Loss

## Task ID
T31

## Goal
实现最小 query-grouped loss，优先 `sampled softmax` 或 `InfoNCE`，只接一个现有 config。

## Why Now
评测已是 grouped retrieval，训练目标也需要最小对齐版本来验证错配假设。

## Allowed Files
- relevant files under `project_bootstrap/baseline_scaffold/src`
- one new or updated config under `project_bootstrap/**/configs`
- `docs/training_alignment_audit.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`

## Forbidden Scope
- 不同时重写 GCN 与 HGCN 架构
- 不新增复杂模型
- 不更改已有正式 artifact

## Inputs to Read
- `docs/training_alignment_audit.md`
- `docs/06_eval_protocol.md`
- relevant baseline runner files

## Expected Output
- 一个可运行的 query-grouped training 入口或 config。
- 最小 smoke test 结果，证明代码路径跑通。

## Verification
```powershell
python project_bootstrap\baseline_scaffold\src\run_relation_seed_sweep.py --help
rg -n "InfoNCE|sampled_softmax|grouped" project_bootstrap\baseline_scaffold\src project_bootstrap\**\configs
```

如环境不支持实际运行，必须说明阻塞原因。

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
adversarial
