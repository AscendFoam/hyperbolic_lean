# 下一个 Traced 目标选择包

这套包用于把“下一个该 trace 哪个目标”从讨论推进成可执行选择。

当前目标不是直接追新 baseline，而是先回答一个更关键的问题：

> 在现有候选里，哪个目标最有希望筛出 `longest_chain > 4` 的模块级 hierarchy 子图？

## 结论先行

基于当前已经完成的真实结果：

1. `plausible` 不适合作为下一目标。
   - 内部几乎没有有效 `extends`
   - relation layer `longest_chain = 1`
2. `batteries` 也不再适合作为“验证更深 hierarchy”的下一目标。
   - 已有 coverage-aware 图
   - 全图 relation layer `longest_chain = 4`
   - 模块级扫描后的最佳候选仍只到 `4`
3. 如果目标是优先找到 `longest_chain > 4` 的模块，那么在现有候选中，**唯一仍值得继续投入的是受控的 Mathlib 子域路线**。

因此，这套包的首选路径是：

- 仓库：`mathlib4`
- 运行环境：WSL
- tracing 策略：`build_deps=false` + `num_procs=2`
- 第一轮子域：`Mathlib.Algebra.*` + `Mathlib.Order.*`
- 第二轮备选子域：`Mathlib.CategoryTheory.*`

## 目录

- `候选排序与选择结论.md`
  解释为什么首选目标是 `mathlib4` 而不是继续停留在 `batteries / plausible`。
- `第一轮复现实验清单.md`
  从 trace 到模块级筛图的可执行步骤。
- `configs/trace_mathlib_hierarchy_probe_v1.json`
  第一轮 WSL trace 配置。
- `configs/normalize_mathlib_hierarchy_probe_v1.json`
  normalize 配置。
- `configs/extract_mathlib_hierarchy_probe_closed_world_v1.json`
  全库 closed-world 抽图配置。
- `configs/filter_mathlib_algebra_order_hierarchy_probe_v1.json`
  首轮子域过滤配置。
- `configs/extract_mathlib_algebra_order_precise_coverage_v1.json`
  首轮 precise hierarchy coverage-aware 配置。
- `configs/module_hierarchy_scan_mathlib_algebra_order_precise_coverage_v1.json`
  首轮模块级 hierarchy 扫描配置。
- `configs/filter_mathlib_category_theory_hierarchy_probe_v1.json`
  第二轮备选子域过滤配置。
- `configs/extract_mathlib_category_theory_precise_coverage_v1.json`
  第二轮备选 precise 配置。
- `configs/module_hierarchy_scan_mathlib_category_theory_precise_coverage_v1.json`
  第二轮备选模块扫描配置。
- `scripts/run_mathlib_hierarchy_local_exporters.sh`
  在 traced `mathlib4` 仓库里本地运行 `ExportPreciseHierarchy.lean` / `ExportDeclarationIndex.lean`。

## 第一轮的真正目标

第一轮不是立刻跑 GCN/HGCN，而是先完成下面这个 gate：

1. 成功 trace 一个受控的 `mathlib4` 样本。
2. 成功导出 declaration index 与 precise hierarchy。
3. 成功构造 `Algebra + Order` 的 coverage-aware precise 图。
4. 成功跑模块级扫描。
5. 判断是否出现满足以下条件的候选模块：
   - `longest_chain > 4`
   - `relation_nodes >= 40`
   - `relation_edges >= 40`
   - `largest_relation_component >= 30`
   - `leaf_ratio <= 0.85`

只有这个 gate 过了，下一步才值得把 relation-aware `parent_prediction` / multi-seed GCN-HGCN 对照迁过去。
