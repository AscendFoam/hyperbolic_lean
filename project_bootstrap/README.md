# 项目启动包

这个目录是对 [形式化证明工程化实验方案（修订版）](d:\Codes\Math\hyperbolic_lean\docs\形式化证明工程化实验方案（修订版）.md) 的进一步拆解，目的是把“方案”推进到“可以按周执行”的层级。

## 目录说明

- [01_第1个月执行清单.md](d:\Codes\Math\hyperbolic_lean\project_bootstrap\01_第1个月执行清单.md)
  第 1 个月的周计划、交付物、验收条件和风险观察点。

- [02_数据Schema设计文档.md](d:\Codes\Math\hyperbolic_lean\project_bootstrap\02_数据Schema设计文档.md)
  从 declaration graph 到 proof-state graph 的数据层设计说明。

- [03_baseline实验表模板.md](d:\Codes\Math\hyperbolic_lean\project_bootstrap\03_baseline实验表模板.md)
  结果记录方式、建议表格结构、对比注意事项。

- [templates/baseline_results_template.csv](d:\Codes\Math\hyperbolic_lean\project_bootstrap\templates\baseline_results_template.csv)
  可直接复制使用的 baseline 记录模板。

- [leandojo_graph_scaffold/README.md](d:\Codes\Math\hyperbolic_lean\project_bootstrap\leandojo_graph_scaffold\README.md)
  LeanDojo 抽图脚手架说明。

- [baseline_scaffold/README.md](d:\Codes\Math\hyperbolic_lean\project_bootstrap\baseline_scaffold\README.md)
  Node2Vec / GCN baseline 的第一版骨架。

## 推荐使用顺序

1. 先看第 1 个月执行清单，明确当前 4 周要交付什么。
2. 再看数据 schema，避免后续抽图后字段对不上。
3. 跑 LeanDojo 抽图脚手架，先拿到 inventory，再接 normalized trace。
4. 初始化 `data/` 和 `artifacts/` 后，用 baseline scaffold 先跑 dry-run。
5. 从 baseline 表模板开始记录实验，不要等实验做多了再补。

## 当前定位

这个启动包优先服务于主线任务：

1. formal graph 数据管线
2. 欧氏 / 双曲 baseline
3. probing / retrieval

表达式级试验台和 `γ` 相关探索不在这个启动包里展开，只保留在上层方案文档中。
