# T41 Provenance Diagnostics

## Task ID
T41

## Goal
先用 T40 冻结配置实际生成六个 provenance split 图目录，再对三类 provenance 图运行结构诊断，比较深度、叶子比例、连通性和 hyperbolicity proxy。

## Why Now
必须先确认 provenance split 已真实落盘，并验证 `explicit_only / synthesized_only / hierarchy_mixed` 是否真的改变结构，再解释后续模型差异。

## Allowed Files
- new data under `data/processed/declaration_graph/`
- new artifacts under `artifacts/diagnostics/`
- `docs/experiment_reports/provenance_diagnostics.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不运行模型训练
- 不覆盖已有 diagnostics
- 不把 proxy 写成严格 hyperbolicity 定理
- 不改动 T40 冻结的 provenance 语义或 config 约定

## Inputs to Read
- T40 protocol and review
- `project_bootstrap/leandojo_graph_scaffold/src/split_relations_by_provenance.py`
- `project_bootstrap/graph_diagnostics_package`
- `docs/diagnostics_protocol.md`

## Expected Output
- 六个 provenance split 图目录、对应 diagnostics artifacts，以及一份比较 `explicit_only / synthesized_only / hierarchy_mixed` 的 provenance diagnostics 报告。
- 报告中必须显式校验协议预期边数，并程序化验证当前两组候选图上的 `hierarchy_mixed = full source graph` identity。

## Verification
```powershell
rg -n "explicit_only|synthesized_only|hierarchy_mixed|longest|leaf|delta|component|identity|edge count" docs\experiment_reports\provenance_diagnostics.md
rg -n "\"num_edges\"|\"edge_type_counts\"" data\processed\declaration_graph\*_explicit_only\stats.json data\processed\declaration_graph\*_synthesized_only\stats.json data\processed\declaration_graph\*_hierarchy_mixed\stats.json
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
adversarial
