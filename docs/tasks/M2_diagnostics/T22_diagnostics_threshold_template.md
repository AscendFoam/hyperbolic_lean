# T22 Diagnostics Threshold Template

## Task ID
T22

## Goal
为 shallow forest / star forest 判断写出可复用诊断阈值和报告模板。

## Why Now
结构诊断需要从临时解释变成可复用协议，支撑论文里的 diagnostics contribution。

## Allowed Files
- `docs/diagnostics_protocol.md`
- `docs/06_eval_protocol.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不把经验阈值写成理论证明
- 不修改实验代码
- 不启动训练或 seed sweep
- 不把 T21 audit priority 写成最终 benchmark conclusion

## Inputs to Read
- `docs/diagnostics_summary.md`
- `docs/candidate_graph_audit.md`
- `artifacts/diagnostics/*/report.md`
- `docs/02_experiment_plan.md`

## Expected Output
- 可复用报告模板。
- 经验阈值或分类规则，明确标注为 heuristic。
- 至少覆盖 `longest chain`、`leaf ratio`、positive scale、component ratio 与 closure expansion / closure cost 的门控口径。

## Verification
```powershell
rg -n "heuristic|shallow|star forest|longest chain|leaf ratio|template" docs\diagnostics_protocol.md
```

## Docs to Update
- `docs/06_eval_protocol.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
normal
