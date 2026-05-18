# T52a Ancestor Explanation Demo

## Task ID
T52a

## Goal
实现一个最小可用的 ancestor explanation demo：给定 declaration、候选图、provenance mode 和 model type，输出 provenance-aware 的 ancestor retrieval explanation；demo 必须服务于 `T51` 已确认的 paper bridge，而不是扩展为新的 benchmark 或 proving pipeline。

## Why Now
`T51` 已完成 MVP 选型，`T52` 已将其拆成可执行边界。当前需要一个最小但真实可运行的 demo，把 provenance-conditional finding 从表格数字转成可体验的工具输出，并为 `T53` 的 milestone judgment 提供“是否已有可交付 tool/demo 片段”的依据。

## Allowed Files
- `project_bootstrap/baseline_scaffold/src/proof_side_ancestor_explanation.py`
- `project_bootstrap/baseline_scaffold/src/relation_baseline_common.py`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不修改现有训练协议、split 语义或 benchmark 指标定义
- 不重训练模型，不新增实验，不补跑新的 seed sweep
- 不引入 LeanDojo、外部服务或大型新依赖
- 不把 demo 扩展成 declaration recommendation、premise retrieval 或端到端 theorem proving
- 不伪造或硬编码 ancestor explanation 结果
- 不把输出退化成纯祖先列表；必须保留 provenance-aware comparison mode
- 不改写 `T43`/`T50`/`T51` 已确认的 provenance-conditional 叙事

## Inputs to Read
- `docs/proof_side_mvp.md`
- `docs/review/T51_review.md`
- `docs/06_eval_protocol.md`
- `docs/experiment_reports/provenance_seed_sweeps.md`
- `docs/experiment_reports/provenance_summary.md`
- `project_bootstrap/baseline_scaffold/src/relation_baseline_common.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_gcn_baseline.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_hyperbolic_baseline.py`
- reviewed artifacts under `artifacts/baselines/relation_seed_sweeps/` when selecting model/checkpoint loading strategy

## Expected Output
- 新增一个可执行脚本 `project_bootstrap/baseline_scaffold/src/proof_side_ancestor_explanation.py`
- 推荐 CLI 形态至少支持以下参数：
  - `--declaration-name`
  - `--candidate-graph`
  - `--provenance-mode`
  - `--model-type`
  - `--comparison-mode`
  - `--output-format`
- demo 输出至少包含：
  - ranked ancestor list
  - relation/provenance tags
  - single-query quality summary
  - provenance-aware comparison view（至少能比较 `explicit_only` 与 `hierarchy_mixed`）
- 若实现中需要复用公共 helper，可在 `relation_baseline_common.py` 中增加最小共享函数，但不得影响现有 runner 行为。

## Verification
```powershell
rg -n "ancestor|provenance|comparison|declaration-name|candidate-graph|provenance-mode|model-type|output-format" project_bootstrap\baseline_scaffold\src\proof_side_ancestor_explanation.py
python -m py_compile project_bootstrap\baseline_scaffold\src\proof_side_ancestor_explanation.py
rg -n "T52a|ancestor explanation|proof_side_ancestor_explanation|comparison mode|Current Unique Task" docs\04_task_board.md docs\07_handoff.md docs\08_risks_and_open_questions.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
normal
