# 03 Architecture

> 更新时间：2026-05-16
>
> 范围：当前仓库的工程资产、数据产物、实验入口和治理文档结构。

## 1. 顶层结构

```text
docs/
  00_raw_idea.md
  01_feasibility_report.md
  02_experiment_plan.md
  03_architecture.md
  04_task_board.md
  05_decision_log.md
  06_eval_protocol.md
  07_handoff.md
  08_risks_and_open_questions.md
  tasks/
  review/

project_bootstrap/
  leandojo_graph_scaffold/
  baseline_scaffold/
  small_target_trace_package/
  mathlib_minimal_trace_package/
  graph_diagnostics_package/
  next_traced_target_selection_package/

data/
  processed/

artifacts/
  diagnostics/
  baselines/
```

`docs/` 是项目主状态；`project_bootstrap/` 是当前主要代码与配置脚手架；`data/` 保存处理后数据说明与局部资产；`artifacts/` 保存脚本和实验输出。

## 2. 数据管线

当前推荐管线是：

```text
traced Lean repo
  -> inventory trace
  -> normalized trace JSONL
  -> declaration graph
  -> precise hierarchy export
  -> coverage-aware relation graph
  -> relation-aware task instances
  -> grouped retrieval / diagnostics / baselines
```

关键入口：

- `project_bootstrap/leandojo_graph_scaffold/src/inventory_trace_dir.py`
- `project_bootstrap/leandojo_graph_scaffold/src/normalize_leandojo_trace.py`
- `project_bootstrap/leandojo_graph_scaffold/src/extract_decl_graph.py`
- `project_bootstrap/leandojo_graph_scaffold/src/build_declaration_graph_from_index.py`
- `project_bootstrap/leandojo_graph_scaffold/src/extract_typeclass_subgraph.py`
- `project_bootstrap/leandojo_graph_scaffold/src/split_relations_by_provenance.py`

## 3. 任务与评测层

当前任务层由 `project_bootstrap/baseline_scaffold/src` 维护：

- `relation_tasks.py`：relation-aware task 定义。
- `relation_baseline_common.py`：共享读取、split、采样、输出逻辑。
- `run_relation_gcn_baseline.py`：GCN baseline。
- `run_relation_hyperbolic_baseline.py`：HGCN / hyperbolic baseline。
- `run_relation_seed_sweep.py`：多 seed 对照。
- `run_graph_diagnostics.py`：图结构诊断。
- `run_task_structure_diagnostics.py`：任务结构诊断。
- `scan_module_hierarchy_candidates.py`：模块级候选图扫描。

正式评测默认使用 `grouped multi-positive ancestor retrieval`，而不是旧单正例 `ancestor_ranking`。

## 4. 诊断与筛图层

诊断包位置：

- `project_bootstrap/graph_diagnostics_package`
- `project_bootstrap/next_traced_target_selection_package`

核心产物位置：

- `artifacts/diagnostics/real_graphs_v1/report.md`
- `artifacts/diagnostics/hierarchy_focus_v1/report.md`
- `artifacts/baselines/relation_seed_sweeps/`

诊断层负责回答：

1. relation layer 是否足够深。
2. 图是否只是 shallow forest / star forest。
3. 哪些模块值得进行双曲适用性复验。
4. grouped retrieval 难度是否与模型结果一致。

## 5. 治理文档职责

| 文件 | 职责 |
| --- | --- |
| `00_raw_idea.md` | 原始问题、最小实验、失败标准 |
| `01_feasibility_report.md` | 相关工作、差异化、Go/No-Go |
| `02_experiment_plan.md` | 当前实验方案主文档，不在本轮重写 |
| `03_architecture.md` | 仓库结构、数据流、模块职责 |
| `04_task_board.md` | 唯一任务状态与 worker 任务队列 |
| `05_decision_log.md` | 关键决策记录 |
| `06_eval_protocol.md` | 数据、split、指标、验收协议 |
| `07_handoff.md` | 给下一个 Captain / Worker 的接手说明 |
| `08_risks_and_open_questions.md` | 风险、开放问题、缓解策略 |
| `data_manifest.md` | reviewed 数据资产与版本锚点清单，未知字段显式保留为 `unknown / needs verification` |
| `data_card.md` | reviewed 数据卡，描述当前图资产字段、relation provenance、coverage-aware 处理和使用边界 |

## 6. Agent 工作边界

Captain 只拆任务、维护治理文档、整合 review，不应直接做大规模实现。

Worker 只执行 `docs/tasks/...` 中指定的单个任务包，只改 Allowed files。

Reviewer 默认只读，只检查 diff 是否完成任务、是否有伪实现、缺验证或越界修改。

## 7. 当前架构缺口

1. T30 已形成 reviewed training alignment audit；T31A 已修复 grouped ancestor retrieval 的 query-level split completeness；T31 已在 grouped retrieval runner 中补入 reviewed 最小 query-grouped loss。下一架构缺口是 T32/T33：在相同 grouped runner、split、seed 和显式 `negative_ratio` 下运行 GCN/HGCN 对照。
2. relation provenance split 需要从已有脚本能力推进到正式实验任务，并解决 per-edge provenance 字段边界。
3. proof-side utility 尚未进入工程实现。
4. `lean4-example`、LeanDojo、Python 环境等部分版本锚点仍需后续可复现实据补证。
5. mathlib module scan 的 standalone checked-in config 仍缺失，当前只能从 `summary.json` 追踪 scan settings。
