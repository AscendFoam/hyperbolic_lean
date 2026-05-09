# 项目交接 Prompt（给后续 AI）

你将接手一个关于 **Lean / Mathlib traced formal-math hierarchy 图数据工程、图结构诊断、relation-aware baseline，以及双曲方法适用性分析** 的在研项目。你的目标不是从零开始重新设计，而是**在现有工程、实验和结论的基础上继续推进**，避免重复劳动、错误回退和叙事漂移。

下面是你需要优先理解并严格遵守的项目上下文。

---

## 1. 你接手的项目到底在做什么

这个项目最初的动机，是想研究：

> 双曲嵌入 / 双曲 GNN 是否适合 Lean/Mathlib 的 traced formal-math hierarchy 图。

但经过多轮真实实验后，项目主线已经发生收敛。当前**最合理的项目定位**不再是：

> “证明双曲方法在形式化证明图上优于欧氏方法”

而应调整为：

> “构建真实 traced Lean/Mathlib hierarchy 图的可复现实验管线、标准化任务协议与结构诊断框架，并系统分析双曲归纳偏置在何种结构与任务条件下可能有效。”

请不要把项目重新带回“继续无休止调 HGCN，直到它赢”为主线。那条路已经被多轮实验证明边际收益很低。

---

## 2. 当前已经得出的关键结论

你必须把下面这些结论视为当前阶段的已知事实，除非后续有更强的新证据推翻它们。

### 2.1 当前没有证据表明 HGCN 在真实 traced Lean hierarchy 图上稳定优于 GCN

已经做过的真实图包括：

- `lean4-example`
- `plausible`
- `batteries`
- `Mathlib` 若干模块级 hierarchy 子图

在这些图上，**relation-aware 欧氏 GCN 通常比当前 HGCN 更稳、更强**。

### 2.2 这个结论已经不再主要归因于“数据没补齐”

项目已经做过：

- precise `extends / instance_of` 抽取
- coverage-aware relation backfill
- 全限定名统一
- closed-world / hierarchy-only / coverage-aware 多版子图重跑

因此，当前 `HGCN` 没赢，**不能再简单解释成 hierarchy coverage 不足**。

### 2.3 当前很多 relation layer 虽然 tree-like，但并不是深层 hierarchy tree

这是最重要的结构性结论之一：

- 很多真实子图是浅层、碎片化、叶子占优的 relation forest
- 大量节点是 `instance -> class` 的 star-like 结构
- `longest_chain` 常常只有 `1~4`

因此：

> “图看起来像树” 不等于 “它天然适合双曲几何”。

### 2.4 ancestor 任务的旧评测口径是有问题的

项目已经把旧的单正例 `ancestor_ranking` 修正为：

- grouped multi-positive ancestor retrieval

默认指标现在应当是：

- `Recall@1/3/5/10`
- `MAP`
- `nDCG`
- `nDCG@10`
- `grouped-MRR`

并且要做：

- `hop_2`
- `hop_3`
- `hop_4_plus`

分桶分析。

**不要再把旧的单正例 `MRR` 当主指标。**

---

## 3. 当前项目真正有价值的贡献点

你后续如果要写文档、整理方案、推进实验，请优先围绕下面这些点组织，而不是只盯着模型成绩。

### 3.1 工程贡献

- traced repo 到 normalized trace 的完整链路
- declaration graph 构建
- precise hierarchy exporter 与适配
- coverage-aware relation backfill
- 全限定名 ID 统一
- 小仓库 trace 包、模块级筛图包、图结构诊断包

### 3.2 协议贡献

- relation-aware 任务定义
- grouped multi-positive ancestor retrieval 协议
- calibration / threshold 协议
- hop-bucket 诊断

### 3.3 经验与诊断贡献

- 真实 traced Lean hierarchy 图并不天然呈现“深层稳定 hierarchy”
- 双曲优势不是天然出现的
- 当前失败更像“结构条件不满足”而不是“模型稍微调一下就能赢”

---

## 4. 项目里哪些东西已经有人做过，不能再当主创新

不要把下面这些点误判成主创新：

- “我们能 trace Lean repo”
- “我们能导出 Mathlib 图”
- “我们能做 import graph / declaration export”
- “我们能做基础网络统计”
- “我们用了 HGCN / Poincare / RotH”

这些在公开生态里都已有明显先行工作，参见：

- `LeanDojo / LeanDojo-v2`
- `lean-training-data`
- `jixia`
- `Pantograph`
- `importGraph`
- `lean4export`
- `mathlib-network`
- `ProofGraph`
- `The Network Structure of Mathlib`

你真正应该强调的是：

> 把真实 traced hierarchy 图、标准化任务协议、结构诊断和公平 baseline 对照连成闭环。

---

## 5. 你应优先阅读的文档

请按下面顺序建立上下文。

### 5.1 项目总定位与创新方向

- [基于深度调研报告的项目定位与创新方向修订.md](d:/Codes/Math/hyperbolic_lean/docs/基于深度调研报告的项目定位与创新方向修订.md)
- [深度调研报告.md](d:/Codes/Math/hyperbolic_lean/docs/深度调研报告.md)

### 5.2 当前阶段主结论

- [阶段总结（2026-05-01，grouped ancestor retrieval）.md](d:/Codes/Math/hyperbolic_lean/docs/阶段总结（2026-05-01，grouped%20ancestor%20retrieval）.md)
- [双曲优势假设的诊断分析与替代方向.md](d:/Codes/Math/hyperbolic_lean/docs/双曲优势假设的诊断分析与替代方向.md)

### 5.3 投稿与叙事路线

- [投稿路线图（FM-ITP-CPP-备选 venue 对照）.md](d:/Codes/Math/hyperbolic_lean/docs/投稿路线图（FM-ITP-CPP-备选%20venue%20对照）.md)

### 5.4 方案书主文档

- [形式化证明工程化实验方案（修订版）.md](d:/Codes/Math/hyperbolic_lean/docs/形式化证明工程化实验方案（修订版）.md)

---

## 6. 你必须知道的代码与实验入口

### 6.1 Trace / normalize / graph extraction

核心源码目录：

- [project_bootstrap/leandojo_graph_scaffold/src](d:/Codes/Math/hyperbolic_lean/project_bootstrap/leandojo_graph_scaffold/src)

重点脚本：

- [trace_repo_with_leandojo.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/leandojo_graph_scaffold/src/trace_repo_with_leandojo.py)
- [normalize_leandojo_trace.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/leandojo_graph_scaffold/src/normalize_leandojo_trace.py)
- [inventory_trace_dir.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/leandojo_graph_scaffold/src/inventory_trace_dir.py)
- [extract_decl_graph.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/leandojo_graph_scaffold/src/extract_decl_graph.py)
- [build_declaration_graph_from_index.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/leandojo_graph_scaffold/src/build_declaration_graph_from_index.py)
- [extract_typeclass_subgraph.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/leandojo_graph_scaffold/src/extract_typeclass_subgraph.py)
- [audit_precise_hierarchy_mismatches.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/leandojo_graph_scaffold/src/audit_precise_hierarchy_mismatches.py)

### 6.2 Baseline / diagnostics

核心目录：

- [project_bootstrap/baseline_scaffold/src](d:/Codes/Math/hyperbolic_lean/project_bootstrap/baseline_scaffold/src)

重点脚本：

- [relation_tasks.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/baseline_scaffold/src/relation_tasks.py)
- [relation_baseline_common.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/baseline_scaffold/src/relation_baseline_common.py)
- [run_relation_gcn_baseline.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/baseline_scaffold/src/run_relation_gcn_baseline.py)
- [run_relation_hyperbolic_baseline.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/baseline_scaffold/src/run_relation_hyperbolic_baseline.py)
- [run_relation_seed_sweep.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/baseline_scaffold/src/run_relation_seed_sweep.py)
- [run_graph_diagnostics.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/baseline_scaffold/src/run_graph_diagnostics.py)
- [run_task_structure_diagnostics.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/baseline_scaffold/src/run_task_structure_diagnostics.py)
- [scan_module_hierarchy_candidates.py](d:/Codes/Math/hyperbolic_lean/project_bootstrap/baseline_scaffold/src/scan_module_hierarchy_candidates.py)

### 6.3 小仓库 trace 与 batteries 执行包

目录：

- [project_bootstrap/small_target_trace_package](d:/Codes/Math/hyperbolic_lean/project_bootstrap/small_target_trace_package)

重点脚本：

- [run_wsl_trace.sh](d:/Codes/Math/hyperbolic_lean/project_bootstrap/small_target_trace_package/scripts/run_wsl_trace.sh)
- [run_batteries_local_exporters.sh](d:/Codes/Math/hyperbolic_lean/project_bootstrap/small_target_trace_package/scripts/run_batteries_local_exporters.sh)

### 6.4 模块级筛图与 Mathlib probe 包

目录：

- [project_bootstrap/graph_diagnostics_package](d:/Codes/Math/hyperbolic_lean/project_bootstrap/graph_diagnostics_package)
- [project_bootstrap/next_traced_target_selection_package](d:/Codes/Math/hyperbolic_lean/project_bootstrap/next_traced_target_selection_package)

重点脚本：

- [run_dlenv_graph_diagnostics.ps1](d:/Codes/Math/hyperbolic_lean/project_bootstrap/graph_diagnostics_package/scripts/run_dlenv_graph_diagnostics.ps1)
- [run_dlenv_module_hierarchy_scan.ps1](d:/Codes/Math/hyperbolic_lean/project_bootstrap/graph_diagnostics_package/scripts/run_dlenv_module_hierarchy_scan.ps1)
- [run_dlenv_relation_seed_sweep.ps1](d:/Codes/Math/hyperbolic_lean/project_bootstrap/graph_diagnostics_package/scripts/run_dlenv_relation_seed_sweep.ps1)

---

## 7. 重要产物路径

### 7.1 grouped retrieval 结果

- [grouped_multi_positive_summary_2026-05-01.md](d:/Codes/Math/hyperbolic_lean/artifacts/baselines/relation_seed_sweeps/grouped_multi_positive_summary_2026-05-01.md)
- [grouped_multi_positive_summary_2026-05-01.json](d:/Codes/Math/hyperbolic_lean/artifacts/baselines/relation_seed_sweeps/grouped_multi_positive_summary_2026-05-01.json)

### 7.2 seed sweep 结果目录

- [artifacts/baselines/relation_seed_sweeps](d:/Codes/Math/hyperbolic_lean/artifacts/baselines/relation_seed_sweeps)

重点子目录：

- `gcn_mathlib_field_subfield_anc_v1`
- `hgcn_mathlib_field_subfield_anc_v1`
- `gcn_mathlib_order_ring_anc_v1`
- `hgcn_mathlib_order_ring_anc_v1`
- `gcn_batteries_classes_order_v1`
- `hgcn_batteries_classes_order_v1`
- `gcn_batteries_control_alternative_monad_v1`
- `hgcn_batteries_control_alternative_monad_v1`

### 7.3 diagnostics 结果目录

- [artifacts/diagnostics](d:/Codes/Math/hyperbolic_lean/artifacts/diagnostics)

重点子目录：

- `real_graphs_v1`
- `hierarchy_focus_v1`
- `mathlib_order_focus_v1`
- `task_structure_mathlib_order_focus_v1`
- `module_hierarchy_scan_batteries_v1`
- `module_hierarchy_scan_mathlib_algebra_order_index_v1`

---

## 8. 环境与运行习惯

### 8.1 Python / PowerShell

这个项目里，之前的执行习惯是：

- Windows 下直接用显式解释器路径
- 不依赖 `conda run`

例如：

```powershell
& 'C:\ProgramData\anaconda3\envs\DLEnv\python.exe' ...
```

### 8.2 WSL

当前机器已经配置了：

- [C:\Users\26410\.wslconfig](C:\Users\26410\.wslconfig)

内容大致为：

```ini
[wsl2]
memory=16GB
processors=4

[experimental]
autoMemoryReclaim=gradual
networkingMode=mirrored
```

这意味着：

- WSL 已被限额
- 后续 `vmmemWSL` 的缓存回收会比之前更好

### 8.3 trace 重任务不要无脑 full Mathlib

项目已经实际踩过坑：

- full trace Mathlib 在 Windows / WSL 混合环境里代价高、风险大
- 容易构建时间过长、内存被打满、路径与 git repo 状态出问题

因此当前策略是：

- 优先小仓库 trace
- 或使用已有构建产物做模块级子集
- 或先做 hierarchy probe / module scan，再决定是否扩图

不要轻易重新走 full Mathlib trace。

---

## 9. 当前最推荐的下一步

如果你接手后要继续推进，优先顺序建议如下。

### 9.1 第一优先：继续做“协议与结构诊断”而不是追 HGCN SOTA

最值得补的方向：

- explicit / synthesized / mixed relation 拆分
- relation layer 结构差异诊断
- 在拆分图上复跑 grouped retrieval / parent prediction

这是目前最有希望把“经验负结果”推进成“结构性解释”的一步。

### 9.2 第二优先：把训练目标对齐到 grouped retrieval

建议做：

- query-grouped retrieval training
- listwise ranking
- contrastive grouped loss

并在现有：

- `Field.Subfield`
- `Order.Ring`

上复验。

### 9.3 第三优先：把图表示迁到 proof-side 下游任务

例如：

- LeanDojo premise retrieval 的图正则化
- relation-aware declaration recommendation
- hierarchy navigation / ancestor explanation

这一步比继续堆模型结构更容易形成论文层面的新意。

---

## 10. 你必须避免的几类错误

1. 不要重新把项目主张写成“证明双曲优于欧氏”。
2. 不要把“能导出 Lean 图”当主要创新。
3. 不要忽视 grouped multi-positive 协议，回退到旧单正例 ranking。
4. 不要只看单次 seed 结果，尽量做多 seed 聚合。
5. 不要忽略图结构诊断，直接把模型输赢解释成几何优劣。
6. 不要动不动就 full trace Mathlib。
7. 不要在已有真实负结果上继续做低收益的 decoder 小修补，除非有很强的新假设支撑。

---

## 11. 如果你要继续写论文/方案，最推荐的叙事

最推荐的主叙事是：

> 我们构建并标准化了真实 traced Lean/Mathlib hierarchy 图的实验管线与评测协议，发现 formal-math hierarchy 图在真实数据中并不天然满足深层双曲层级假设；在此基础上，我们提出 relation-aware、grouped multi-positive 的任务口径与诊断框架，并系统分析双曲归纳偏置何时可能成立、何时会因图结构浅层化与合成边机制而失效。

这个叙事比“某个 HGCN 版本终于赢了 1 个点”更稳、更可信，也更适合当前项目的真实证据。

---

## 12. 一句话交接

> 这个项目当前最重要的资产，不是某个双曲模型，而是一整套面向真实 traced Lean hierarchy 图的工程管线、协议标准化和结构诊断框架；你接手后最该做的，是在这个基础上继续把“何时双曲有效”讲清楚，而不是重新回到“如何把 HGCN 调赢”的旧主线。
