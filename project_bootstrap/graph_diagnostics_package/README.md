# 图结构诊断实验包

这套实验包用于把“形式化数学图是否真的具备适合双曲建模的层级几何”从讨论推进到可执行诊断。

当前目标不是直接训练新模型，而是先回答三个前置问题：

1. 当前真实 traced Lean 图在整体上更像树状结构，还是更像小世界/稠密局部团簇网络？
2. `extends + instance_of` 关系层本身是否足够深、足够稀疏、足够 tree-like，值得继续为双曲模型投入优化？
3. `lean4-example / plausible / batteries` 三类真实图之间，层级信号是否在更真实的小仓库上变得更清楚？

## 目录

- `configs/graph_diagnostics_real_graphs_v1.json`
  面向当前主要真实图的统一对照配置。
- `configs/graph_diagnostics_hierarchy_focus_v1.json`
  聚焦 typeclass / hierarchy 子图的更轻量配置。
- `configs/module_hierarchy_scan_batteries_v1.json`
  面向 `batteries` 的模块级 hierarchy 候选扫描配置。
- `configs/relation_seed_sweep_*.json`
  面向候选模块子图的多 seed GCN/HGCN 对照配置。
- `scripts/run_dlenv_graph_diagnostics.ps1`
  在 Windows + `DLEnv` 下直接执行诊断的包装脚本。
- `scripts/run_dlenv_module_hierarchy_scan.ps1`
  在 Windows + `DLEnv` 下直接执行模块级 hierarchy 候选扫描。
- `scripts/run_dlenv_relation_seed_sweep.ps1`
  在 Windows + `DLEnv` 下直接执行 relation-aware 多 seed sweep。
- `执行清单.md`
  从运行到解释结果的操作说明。

## 预期产物

每次运行会在配置指定的 `artifacts/diagnostics/...` 目录下产出：

- `report.md`
- `summary.json`
- `graphs/<graph_name>.json`

这些结果可直接用于：

- 修订方案书中的“双曲优势假设”判断
- 决定下一步是否值得继续投入 HGCN / HNN / Lorentz 系模型
- 选择更适合的目标图、任务与评测协议

## 推荐起点

先运行 `graph_diagnostics_real_graphs_v1.json`，拿到跨仓库诊断全景；
若确认需要深挖层级层，再运行 `graph_diagnostics_hierarchy_focus_v1.json`。

如果要继续推进到“模块级筛图”，直接运行 `module_hierarchy_scan_batteries_v1.json`。

如果要验证某个模块级候选上的 GCN/HGCN 结果是否稳定，继续运行对应的
`relation_seed_sweep_*.json`。
