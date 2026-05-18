# T52a Ancestor Explanation Demo

## Task ID

T52a

## Goal

实现 ancestor explanation MVP demo：新增一个 CLI 脚本，给定 declaration name、candidate graph、model type 与 provenance mode，直接加载 T42 reviewed artifacts 中的 `node_embeddings.npy`，执行 ancestor retrieval ranking，并输出：

- ranked ancestor list
- per-query retrieval metrics
- hop-depth breakdown
- provenance-aware comparison result（`explicit_only` vs `hierarchy_mixed`）

该任务是 `T51` 选定、`T52` 打包后的唯一下游 demo 实现任务，不承诺端到端 theorem proving。

## Why Now

`T52_review` 已判定 `PASS`，说明 ancestor explanation demo 的实现边界已经足够清楚，可以进入真实落地阶段。当前最需要的不是继续讨论方向，而是把这个 proof-side bridge 变成一个可运行、可检查、可被 adversarial reviewer 审核的最小工具原型。

## Allowed Files

- `project_bootstrap/baseline_scaffold/src/proof_side_ancestor_explanation.py`
- `docs/experiment_reports/ancestor_explanation_demo_report.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope

- 不重新训练模型，不微调已有模型，不修改任何 runner 或 training 代码
- 不修改 `project_bootstrap/baseline_scaffold/src/` 下除新建 `proof_side_ancestor_explanation.py` 以外的任何文件
- 不引入新的大型依赖；只允许使用项目现有 Python 运行时与已有依赖
- 不实现端到端 theorem proving
- 不把 demo 写成“已证明可提升完整证明成功率”
- 不改写 `T43` 与 `T50/T51` 已确认的 provenance-conditional 结论
- 不把 ancestor explanation 扩张成新的 benchmark task、protocol extension 或并行 proof-side 支线
- 不把输出退化成纯祖先列表；provenance-aware comparison mode 是硬边界，不是可选增强
- 不修改 `docs/proof_side_mvp.md`、`docs/paper_outline.md`、`docs/06_eval_protocol.md`

## Inputs to Read

- `docs/proof_side_mvp.md`
- `docs/tasks/M5_paper/T52_proof_side_demo_package.md`
- `docs/review/T52_review.md`
- `docs/paper_outline.md`
- `docs/experiment_reports/provenance_seed_sweeps.md`
- `docs/experiment_reports/provenance_summary.md`
- `docs/08_risks_and_open_questions.md`
- `project_bootstrap/baseline_scaffold/src/common.py`
- `project_bootstrap/baseline_scaffold/src/relation_tasks.py`
- `project_bootstrap/baseline_scaffold/src/relation_baseline_common.py`

## Expected Output

### 1. CLI Script: `proof_side_ancestor_explanation.py`

新增脚本：

`project_bootstrap/baseline_scaffold/src/proof_side_ancestor_explanation.py`

脚本必须接受以下参数：

```text
--declaration-name   Declaration name exactly as it appears in declarations.csv
--candidate-graph    "field_subfield" or "order_ring"
--provenance-mode    "explicit_only" or "hierarchy_mixed" or "synthesized_only"
--model-type         "gcn" or "hgcn"
--seed               Integer seed, default 42
--comparison-mode    "none" or "explicit_vs_mixed", default "none"
--output-format      "text" or "json", default "text"
--top-k              Optional integer cutoff for display, default 10
```

`--declaration-name` 必须按 `declarations.csv` 中的精确字符串匹配，不允许在脚本内部偷偷做模糊匹配、后缀匹配或只取短名。

示例格式可以是：

```text
c211948581bde9846a99e32d97a03f0d5307c31e::Subfield
```

但 worker 必须先从目标 graph 的 `declarations.csv` 里确认示例 declaration 确实存在，再在 demo report 中写入实际使用的例子。

### 2. Script Behavior

#### Single-query mode (`--comparison-mode none`)

脚本必须：

1. 从 `data/processed/declaration_graph/mathlib_{candidate}_v1_{provenance}/` 读取图数据
2. 从精确 seed artifact 目录读取 embedding
3. 用图中的真实 `extends` 祖先关系构建 ground-truth ancestor set
4. 用 query declaration embedding 与 candidate ancestor embeddings 的相似度做排序
5. 输出：
   - ranked ancestor list
   - top-k 命中情况
   - MAP、Recall@1/3/5/10
   - hop 2 / 3 / 4+ breakdown

#### Provenance comparison mode (`--comparison-mode explicit_vs_mixed`)

必须对同一个 declaration、同一个 model type、同一个 seed，分别在：

- `explicit_only`
- `hierarchy_mixed`

两种 provenance mode 下运行并做并排比较。

输出至少包括：

- 两组 ranked ancestor list
- 两组 per-query metrics
- top-k ancestor diff
- 一句简短解释，指出是否出现“explicit_only 中能找回更深祖先，而 mixed 中被稀释”的现象

### 3. Output Format

- `text`：适合人读的 stdout 表格或分段文本
- `json`：结构化 stdout，至少包含：
  - `query_declaration`
  - `candidate_graph`
  - `model_type`
  - `seed`
  - `provenance_mode`
  - `ranked_ancestors`
  - `ground_truth_ancestors`
  - `metrics`
  - `hop_depth_breakdown`
  - `comparison`

### 4. Artifact Dependencies

只能依赖 T41/T42 reviewed artifacts。

图数据目录：

- `data/processed/declaration_graph/mathlib_{candidate}_v1_explicit_only/`
- `data/processed/declaration_graph/mathlib_{candidate}_v1_synthesized_only/`
- `data/processed/declaration_graph/mathlib_{candidate}_v1_hierarchy_mixed/`

embedding 目录必须使用精确路径模式，而不是模糊 wildcard 约定：

- `artifacts/baselines/relation_seed_sweeps/provenance_gcn_{candidate}_{provenance}_t42/provenance_gcn_{candidate}_{provenance}_t42_seed{seed}/node_embeddings.npy`
- `artifacts/baselines/relation_seed_sweeps/provenance_hgcn_{candidate}_{provenance}_t42/provenance_hgcn_{candidate}_{provenance}_t42_seed{seed}/node_embeddings.npy`

同一 seed 目录下还应读取：

- `run_manifest.json`

用于记录与校验 artifact 来源。

### 5. Critical Implementation Notes

1. `node_embeddings.npy` 的行顺序必须与训练时的节点顺序完全一致。
2. 脚本必须复用 `common.load_declaration_graph()` 的节点加载逻辑，或严格等价地复现它；否则 embedding 行号会错位。
3. 首次加载后必须立即做 sanity check：
   - `len(declarations.csv rows) == node_embeddings.shape[0]`
   - query declaration 能在 `declarations.csv` 中被精确找到
   - 至少一个真实祖先在排序结果中落在合理范围内，而不是明显全错位
4. 若 sanity check 失败，脚本必须报错退出，而不是继续输出看似正常的结果。

### 6. Demo Report

新增：

`docs/experiment_reports/ancestor_explanation_demo_report.md`

至少包含：

1. CLI 使用说明
2. 至少 3 个命令示例：
   - single query on `explicit_only`
   - single query on `hierarchy_mixed`
   - `explicit_vs_mixed` comparison mode
3. 至少 2 个 declaration 示例：
   - 一个来自 `Field.Subfield`
   - 一个来自 `Order.Ring`
4. 示例输出摘要
5. 观察到的 provenance quality difference
6. 该 demo 如何映射到 paper bridge，而不是独立新任务线

### 7. Acceptance Criteria

1. 可以对 reviewed candidate graph 中的真实 declaration 运行查询
2. 可以输出 ranked ancestors 与 per-query retrieval metrics
3. comparison mode 可运行，且不是空壳占位
4. 不需要任何新训练或新 checkpoint 生成
5. 不引入新依赖
6. demo report 明确说明这是 provenance-conditional finding 的 downstream manifestation

## Verification

```powershell
rg -n "Task ID|Goal|Why Now|Allowed Files|Forbidden Scope|Inputs to Read|Expected Output|Verification|Docs to Update|Reviewer Type" docs\tasks\M5_paper\T52a_ancestor_explanation_demo.md

rg -n "declaration-name|declarations.csv|explicit_vs_mixed|node_embeddings.npy|run_manifest.json|sanity check|adversarial" docs\tasks\M5_paper\T52a_ancestor_explanation_demo.md

python -m py_compile project_bootstrap\baseline_scaffold\src\proof_side_ancestor_explanation.py
```

实现完成后，worker 还应在报告中明确写出实际执行过的 demo 命令，以及为何这些命令足以覆盖 acceptance criteria。

## Docs to Update

- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type

adversarial
