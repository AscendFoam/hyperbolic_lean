# 小型目标仓库 / 模块级子集实验包

这个目录用于把后续实验路线从“Windows 上 full trace Mathlib”切换到两条更稳的工程路径：

1. 小型目标仓库完整 trace
2. 基于已有 normalized trace / declaration graph 的模块级子集实验

## 为什么这样切

前一轮 Mathlib 实验已经说明：

- `Build completed successfully` 不代表可控地完成了数据抽取
- `ExtractData.lean` 在 Windows 上会并行拉起大量 `lean.exe`
- full trace `mathlib4` 容易在抽取阶段触发高内存占用和长时间 warning

因此下一阶段不再把“先拿到一个全量 traced Mathlib”当作先决条件，而是优先保证：

- 数据规模可控
- 评测协议可重复
- relation-aware baseline 能继续推进

## 两条推荐路线

### 路线 A：小仓库完整 trace

适合场景：

- 想继续验证 `normalize -> graph -> precise hierarchy -> baseline` 的全链路
- 但不想再承担 Mathlib 级别的 tracing 成本

使用配置：

- `configs/trace_small_repo_template.json`

关键约束：

- `build_deps = false`
- `num_procs = 2`

这意味着：

- 优先只处理目标仓库自身文件
- 显式限制并行度，避免再次打满内存

### 路线 B：已有产物上的模块级子集

适合场景：

- 暂时不再追求新的 trace
- 先在已有 `lean4-example` 或后续任何可用 normalized trace 上做更细粒度子图实验

可以从两个层级切：

1. `normalized trace` 层切模块前缀
2. `full precise relation graph` 层切模块前缀

对应工具：

- `project_bootstrap/leandojo_graph_scaffold/src/filter_normalized_trace_by_modules.py`
- `project_bootstrap/leandojo_graph_scaffold/src/filter_declaration_graph_by_modules.py`

## 推荐优先级

建议先按下面顺序推进：

1. 先走路线 B，在已有 `lean4-example_full_precise_v1` 上做模块级 relation-aware 子图实验
2. 路线 B 跑顺后，再选一个小型 Lean 仓库走路线 A
3. 只有当这两条路线都稳定后，再考虑 Linux/WSL 上的受控 Mathlib 子集 tracing

## 配置清单

- `configs/trace_small_repo_template.json`
  小仓库 trace 模板，默认低线程 + `no build deps`

- `configs/filter_normalized_trace_example_modules.json`
  从 normalized trace 中抽模块子集的示例

- `configs/extract_filtered_modules_graph_example.json`
  从过滤后的 normalized trace 生成 closed-world graph

- `configs/filter_graph_example_modules.json`
  从已有 full precise graph 直接切模块级子图

- `configs/relation_gcn_filtered_modules_parent_prediction.json`
  模块级子图上的 GCN parent prediction 示例

- `configs/relation_hgcn_filtered_modules_parent_prediction.json`
  模块级子图上的 HGCN parent prediction 示例

## 第一轮真实小仓库候选

基于 `LeanDojo 4.20.0` / `Mathlib v4.20.0` 同档依赖版本，以及仓库体量与层级关键词密度，当前推荐候选为：

1. `plausible`
   - repo: `https://github.com/leanprover-community/plausible`
   - commit: `2ac43674e92a695e96caac19f4002b25434636da`
   - 特点: 仅约 `11` 个 Lean 文件，但已有明显 `class / structure / instance` 使用，第一轮最稳

2. `batteries`
   - repo: `https://github.com/leanprover-community/batteries`
   - commit: `7a0d63fbf8fd350e891868a06d9927efa545ac1e`
   - 特点: 约 `224` 个 Lean 文件，层级信号更丰富，但规模明显更大，适合第二轮

3. `lean4-cli`
   - repo: `https://github.com/leanprover/lean4-cli`
   - commit: `f9e25dcbed001489c53bceeb1f1d50bbaf7451d4`
   - 特点: 很小，但 `class / instance` 信号弱，更适合作为工具链验证样本，不适合作为层级主实验样本

因此第一轮真实小仓库 trace 默认优先选择 `plausible`。
