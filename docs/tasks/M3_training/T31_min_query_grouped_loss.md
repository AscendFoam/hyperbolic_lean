# T31 Minimal Query-Grouped Loss

## Task ID
T31

## Goal
实现最小 query-grouped loss，优先 `sampled softmax` 或 `InfoNCE`，只接一个现有 config。

## Why Now
评测已是 grouped retrieval，训练目标也需要最小对齐版本来验证错配假设。`T31A` 已通过 adversarial review，并确认 grouped ancestor retrieval 的 query-level split completeness 已收口。

## Allowed Files
- relevant files under `project_bootstrap/baseline_scaffold/src`
- one new or updated config under `project_bootstrap/**/configs`
- `docs/training_alignment_audit.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不同时重写 GCN 与 HGCN 架构
- 不新增复杂模型
- 不更改已有正式 artifact
- 不运行长 seed sweep
- 不把 smoke 结果写成正式 benchmark 结论

## Inputs to Read
- `docs/training_alignment_audit.md`
- `docs/06_eval_protocol.md`
- `docs/review/T31A_review.md`
- relevant baseline runner files

## Expected Output
- 一个可运行的 query-grouped training 入口或 config。
- 最小 smoke test 结果，证明代码路径跑通。
- grouped loss 的 query 分组必须与 T31A 已 review 的 split / eval key 一致，即 `(src_id, relation_type)`。
- 当 `ancestor_label_mode="source_kind"` 时，注意 `relation_type` 是 `extends_ancestor` / `instance_ancestor`，不是原始 `extends` / `instance_of`。

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
