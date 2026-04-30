# 新 Mathlib Trace 最小可复现实验包

这个目录给出一套**最小但完整**的工程化实验设计包，用于把当前已经在 `lean4-example` 上跑通的 relation-aware 评测协议，迁移到一个更层级化、规模更大、但依然可控的新 Mathlib trace 上。

## 目标

这套包优先回答三个工程问题：

1. 新的 traced Mathlib 子集应当选哪里，才能比 `lean4-example` 更有层级结构信号？
2. 新 trace 应该沿用什么抽图协议，才能和当前 `typed_link / parent_prediction / ancestor_ranking` 结果严格同口径？
3. 第一轮 tracing 与评测如何控制范围，避免一上来就陷入“全量 Mathlib 太大、结论又不可归因”的状态？

## 设计原则

### 1. 先做“层级更丰富”的子集，不先追求“Mathlib 尽可能大”

当前 `lean4-example` 的主要瓶颈不是 `uses` 图太小，而是 `extends` 边过少。  
因此新 trace 的目标不是“比现在大很多”本身，而是“在可追踪规模内显著提高 precise `extends / instance_of` 密度”。

### 2. trace 前尽量只锁仓库版本，不过早做复杂切片

LeanDojo tracing 最稳定的方式仍然是对一个固定 commit 的仓库做标准 trace。  
真正的“目标子集”优先在 **trace 后的 declaration graph 层** 用模块前缀过滤实现，这样可复用当前脚手架，也更容易复查。

### 3. 评测口径尽量不变

为了让新旧结果可比较，第一轮新 Mathlib 实验建议继续固定：

- relation-aware message passing
- `typed_link_prediction`
- `parent_prediction`
- `ancestor_ranking`
- `same_module` harder negatives
- `temperature scaling + validation-max-F1 threshold`
- GCN / HGCN v3 同口径对照

## 推荐目标子集

### 首选：`Mathlib/Algebra/*` + `Mathlib/Order/*`

推荐第一轮最小包优先围绕以下模块前缀：

- `Mathlib.Algebra`
- `Mathlib.Order`

原因是：

1. 这两块通常比拓扑、分析等区域更密集地使用 structure/class/instance。
2. `instance_of` 和 typeclass 继承链通常更丰富，更适合 `parent_prediction` / `ancestor_ranking`。
3. 相比整库，这个前缀级切片仍然足够大，但没有大到第一轮就难以调试。

### 第二候选：`Mathlib/CategoryTheory/*`

如果第一候选的层级边仍不够丰富，可以把第二轮切到：

- `Mathlib.CategoryTheory`

这块通常在层级化结构上更强，但 proof/definition 复杂度也更高，适合作为第二阶段扩展，而不是最小包第一站。

## 目录内容

- `configs/trace_mathlib_algebra_order_minimal.json`
  LeanDojo trace 配置模板
- `configs/normalize_mathlib_algebra_order_minimal.json`
  normalized trace 配置模板
- `configs/extract_mathlib_closed_world_v1.json`
  全图 closed-world declaration graph 抽图配置
- `configs/filter_mathlib_algebra_order_modules_v1.json`
  基于模块前缀的目标子集切图配置
- `configs/extract_mathlib_algebra_order_precise_v1.json`
  精确 hierarchy 子图配置
- `configs/relation_gcn_mathlib_algebra_order_precise_parent_prediction_v1.json`
  GCN parent prediction 配置
- `configs/relation_hgcn_mathlib_algebra_order_precise_parent_prediction_v1.json`
  HGCN parent prediction 配置
- `configs/relation_gcn_mathlib_algebra_order_precise_typed_link_v1.json`
  GCN typed link 配置
- `configs/relation_hgcn_mathlib_algebra_order_precise_typed_link_v1.json`
  HGCN typed link 配置
- `configs/relation_gcn_mathlib_algebra_order_precise_ancestor_ranking_v1.json`
  GCN ancestor ranking 配置
- `configs/relation_hgcn_mathlib_algebra_order_precise_ancestor_ranking_v1.json`
  HGCN ancestor ranking 配置
- `实验执行清单.md`
  从 trace 到首轮结果的执行步骤
- `目标子集与评测协议设计.md`
  为什么这样选子集、为什么这样固定协议

## 最小工作流

### 1. trace 整个目标仓库

先对固定 commit 的目标仓库做标准 LeanDojo trace。

### 2. 生成 declaration index 与 precise hierarchy

用现有 Lean 元编程脚本导出：

- declaration index
- precise `extends / instance_of`

### 3. normalize + closed-world 抽图

把 trace 统一转成全限定名的 normalized trace，再抽出 closed-world declaration graph。

### 4. 按模块前缀做子集切图

用 `filter_declaration_graph_by_modules.py` 从全图切出：

- `Mathlib.Algebra.*`
- `Mathlib.Order.*`

### 5. 注入 precise hierarchy，形成 relation-aware 子图

在该子图上保留内部 `uses`，再加入精确 `extends / instance_of`。

### 6. 运行 relation-aware 基线

至少跑：

- `typed_link_prediction`
- `parent_prediction`
- `ancestor_ranking`

每个任务都做：

- GCN
- HGCN v3

## 首轮成功标准

第一轮新 Mathlib trace 不要求 HGCN 立刻赢 GCN，但至少应满足：

1. precise 子图中的 `extends` 数量明显高于 `lean4-example` 的 `19`
2. `parent_prediction` 与 `ancestor_ranking` 的 ranking 指标不再因样本过小而失真
3. relation-aware 协议可以完整复现，不需要额外改 runner
4. 新旧结果能够直接按同口径比较

如果这四点成立，这次新 trace 就已经是“有效数据升级”，值得继续做更强模型；否则应先回到子集选择与 precise relation 覆盖阶段，而不是盲目扩大规模。
