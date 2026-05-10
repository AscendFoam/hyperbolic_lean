# T42 Provenance Seed Sweeps

## Task ID
T42

## Goal
对三类 provenance 图运行 grouped retrieval / parent prediction 的 GCN 与 HGCN seed sweep。

## Why Now
结构差异需要与模型表现同口径关联，才能回答 synthesized relation 的影响。

## Allowed Files
- new artifacts under `artifacts/baselines/relation_seed_sweeps/`
- `docs/experiment_reports/provenance_seed_sweeps.md`
- relevant configs under `project_bootstrap/**/configs`
- `docs/04_task_board.md`
- `docs/07_handoff.md`

## Forbidden Scope
- 不修改已冻结协议
- 不只报告赢的模型
- 不覆盖历史 artifact

## Inputs to Read
- T40 and T41 outputs
- `docs/06_eval_protocol.md`
- seed sweep scripts and configs

## Expected Output
- GCN/HGCN 5-seed provenance 对照。
- grouped 指标、hop bucket、parent prediction 结果视任务可用性报告。

## Verification
```powershell
rg -n "explicit|synthesized|mixed|GCN|HGCN|mean|std|Recall|MAP|nDCG" docs\experiment_reports\provenance_seed_sweeps.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
adversarial
