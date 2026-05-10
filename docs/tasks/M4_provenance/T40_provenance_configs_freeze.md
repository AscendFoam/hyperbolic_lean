# T40 Provenance Configs Freeze

## Task ID
T40

## Goal
冻结 `explicit-only / synthesized-only / mixed` 三类图的生成配置和输出位置。

## Why Now
provenance split 是解释 Lean-specific synthesized relation 是否削弱双曲优势的关键里程碑。

## Allowed Files
- relevant configs under `project_bootstrap/**/configs`
- `docs/provenance_split_protocol.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不运行 seed sweep
- 不改变数据语义来追求模型结果
- 不覆盖历史配置

## Inputs to Read
- `project_bootstrap/leandojo_graph_scaffold/src/split_relations_by_provenance.py`
- existing provenance configs
- `docs/02_experiment_plan.md`
- `docs/06_eval_protocol.md`

## Expected Output
- 三类 provenance 图的配置索引和输出目录约定。

## Verification
```powershell
rg -n "explicit|synthesized|mixed|provenance" docs\provenance_split_protocol.md project_bootstrap\**\configs
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
adversarial
