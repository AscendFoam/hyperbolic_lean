# 03 Architecture

> 更新时间：2026-05-23（T58 review PASS，T59 当前）
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
  paper_figures_and_tables.md
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
| `paper_figures_and_tables.md` | Publication-facing figure/table source-of-truth (T57) |
| `paper_artifact_package.md` | Submission-facing artifact package: source-to-claim mapping, table/figure-to-source mapping, exclusions, checklist (T58) |
| `data_manifest.md` | reviewed 数据资产与版本锚点清单，未知字段显式保留为 `unknown / needs verification` |
| `data_card.md` | reviewed 数据卡，描述当前图资产字段、relation provenance、coverage-aware 处理和使用边界 |

## 6. Agent 工作边界

Captain 只拆任务、维护治理文档、整合 review，不应直接做大规模实现。

Worker 只执行 `docs/tasks/...` 中指定的单个任务包，只改 Allowed files。

Reviewer 默认只读，只检查 diff 是否完成任务、是否有伪实现、缺验证或越界修改。

## 7. 当前架构缺口

1. T30 已形成 reviewed training alignment audit；T31A 已修复 grouped ancestor retrieval 的 query-level split completeness；T31 已在 grouped retrieval runner 中补入 reviewed 最小 query-grouped loss；T32/T33 已分别完成 matched GCN/HGCN grouped 5-seed 对照；T34 已把 grouped-vs-binary 与 matched GCN-vs-HGCN 结论收口成正式总结；T40 已把 provenance split 的配置与输出位置冻结成可复用协议入口；T41 已把 frozen config 真正落成六个 split 图目录并接通 diagnostics pipeline；T42 已在 provenance-aware split 上完成受约束的 GCN/HGCN 5-seed sweeps；T43 已把 provenance 结构诊断、seed sweep 结果、风险状态与项目叙事统一收口，并将 Milestone 4 结论固定为 provenance-conditional；T50 已把这些 reviewed artifact 提炼成 paper skeleton；T51 已从 proof-side bridge 中正式选定 ancestor explanation 作为 MVP；T52 已把该 MVP 收敛成 reviewed 的最小 demo implementation package；`T52a` 已实现并通过 review，把 proof-side bridge 落地为真实 demo CLI 与 demo report；`T53` 已完成 milestone review 并通过 review，正式将项目裁决为 **Narrow**；`T54` 已产出并通过 review 接受 paper-facing draft 首版；`T55` 已通过 review 并完成第二轮文稿结构 refinement；`T56` 已通过 review 并完成 precision cleanup：`R29` 修正、`R28` 基于 reviewed artifact 根因解释合法关闭；`T57` 已通过 review，并把 `docs/paper_figures_and_tables.md` 建成 publication-facing 图表源文档；`T58` 已通过 review，并把 `docs/paper_artifact_package.md` 收口为 submission-facing 的 source-to-claim 映射与提交检查清单。下一架构缺口是 `T59` 的最终 paper editing / venue shaping。
2. relation provenance split 已从“已冻结协议”推进到“已真实生成图并经结构诊断验证”的正式实验阶段；paper-facing 数值精度问题 `R28`/`R29` 已由 `T56` cleanup 关闭/修正；figure/table source rendering 已由 `T57` 收口；artifact packaging 已由 `T58` 收口。`T58_review` 的非阻塞项只剩表述层精修：统一 artifact package 中 core-table 术语，以及把 Table T1 的 HGCN source mapping 写成“`T33` primary，`T42` cross-check”这类更精确口径。后续优先 `T59`。
3. proof-side utility 已完成 MVP 选型、demo implementation 与 milestone 级裁决，当前缺的不是继续扩写 proof-side 功能面，而是把已有证据压缩成 venue-shaped 文稿：最终 paper editing、contribution/page-budget 收束，以及 submission-facing source mapping 的最后一轮精修。
4. `lean4-example`、LeanDojo、Python 环境等部分版本锚点仍需后续可复现实据补证。
5. mathlib module scan 的 standalone checked-in config 仍缺失，当前只能从 `summary.json` 追踪 scan settings。



