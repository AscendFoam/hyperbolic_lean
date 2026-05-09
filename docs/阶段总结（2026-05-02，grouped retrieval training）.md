# 阶段总结（2026-05-02，grouped retrieval training）

> 主题：将训练目标从 binary edge classification 升级为 query-grouped softmax (InfoNCE) retrieval training，在 `Field.Subfield` 和 `Order.Ring` 上完成 5-seed 聚合对照，并分析训练-评测错配对 GCN/HGCN 相对表现的影响。

---

## 1. 本阶段完成了什么

本阶段的核心工作是**把训练目标对齐到 grouped retrieval**，消除了"训练做二分类、评测看 grouped retrieval"的第二层错配。

具体完成的内容：

1. **新建 `run_relation_grouped_retrieval_baseline.py`**（~350 行）
   - 以 `(src, relation)` 为训练单元，将正样本按查询分组
   - 使用 InfoNCE / grouped softmax loss：对每个查询的所有候选（正例 + 采样负例）做 softmax，优化正例的平均 log-prob
   - 每轮 epoch 重新采样负例（`resample_negatives_every_epoch: true`）
   - 支持 GCN 和 HGCN 两种 encoder（通过 `model_type` 配置）
   - 早停基于 validation grouped MAP（而非 binary AP）

2. **创建 4 组 baseline 配置**：
   - `grouped_gcn_field_subfield_anc_v1.json`
   - `grouped_hgcn_field_subfield_anc_v1.json`
   - `grouped_gcn_order_ring_anc_v1.json`
   - `grouped_hgcn_order_ring_anc_v1.json`

3. **完成 4 组 5-seed sweep（共 20 次训练）**：
   - seeds: `[7, 42, 123, 2026, 3407]`
   - negative_ratio: `10.0`
   - 每组生成 `aggregate.json`、`per_seed_results.csv`、`report.md`

4. **修复了 `ranking_test_hits_at_1` / `ranking_test_hits_at_10` 缺失的 bug**，并补丁了所有已完成的 sweep 结果。

相关产物路径：

- `artifacts/baselines/relation_seed_sweeps/grouped_gcn_field_subfield_v1/`
- `artifacts/baselines/relation_seed_sweeps/grouped_hgcn_field_subfield_v1/`
- `artifacts/baselines/relation_seed_sweeps/grouped_gcn_order_ring_v1/`
- `artifacts/baselines/relation_seed_sweeps/grouped_hgcn_order_ring_v1/`

---

## 2. 为什么这一步是必要的

上一阶段（2026-05-01）已经修正了**评测口径**（从单正例 ranking → grouped multi-positive retrieval），但训练目标仍然使用 `BCEWithLogitsLoss` 做二元边分类。这意味着：

- 训练时，模型学习的是"给定 (src, dst, rel)，这条边是否存在"
- 评测时，我们衡量的是"给定 (src, rel)，在所有候选 dst 中把真祖先排到前面"

这两者之间存在明确的目标错配。本阶段的目标是回答：

> 当前 GCN 优于 HGCN 的结论，到底是几何模型的本质差异，还是训练目标与 retrieval 任务之间错配造成的假象？

---

## 3. 核心实验结果

### 3.1 Grouped Retrieval Training vs Binary Training（5-seed 聚合）

#### Field.Subfield（133 nodes, 152 edges）

| 方法 | gMAP | gnDCG | gR@10 | gMRR | MRR | AP |
|------|------|-------|-------|------|-----|-----|
| **Grouped GCN** | **0.321 ± 0.022** | **0.505 ± 0.019** | **0.669 ± 0.057** | **0.368 ± 0.033** | **0.200 ± 0.013** | 0.542 ± 0.052 |
| Grouped HGCN | 0.299 ± 0.037 | 0.485 ± 0.030 | 0.630 ± 0.056 | 0.338 ± 0.044 | 0.186 ± 0.017 | 0.447 ± 0.068 |
| Binary GCN | 0.144 ± 0.023 | 0.353 ± 0.020 | 0.272 ± 0.060 | 0.182 ± 0.036 | 0.093 ± 0.017 | **0.973 ± 0.007** |
| Binary HGCN | 0.104 ± 0.017 | 0.314 ± 0.015 | 0.179 ± 0.061 | 0.141 ± 0.035 | 0.072 ± 0.015 | 0.803 ± 0.050 |

#### Order.Ring（253 nodes, 300 edges）

| 方法 | gMAP | gnDCG | gR@10 | gMRR | MRR | AP |
|------|------|-------|-------|------|-----|-----|
| **Grouped GCN** | **0.291 ± 0.020** | **0.493 ± 0.018** | **0.624 ± 0.032** | 0.339 ± 0.023 | 0.176 ± 0.009 | 0.610 ± 0.045 |
| Grouped HGCN | 0.291 ± 0.023 | 0.493 ± 0.022 | 0.606 ± 0.027 | **0.347 ± 0.034** | **0.178 ± 0.013** | 0.443 ± 0.014 |
| Binary GCN | 0.208 ± 0.024 | 0.419 ± 0.019 | 0.406 ± 0.045 | 0.260 ± 0.029 | 0.139 ± 0.014 | **0.971 ± 0.007** |
| Binary HGCN | 0.148 ± 0.019 | 0.362 ± 0.019 | 0.262 ± 0.049 | 0.197 ± 0.025 | 0.111 ± 0.012 | 0.874 ± 0.035 |

### 3.2 Grouped Retrieval Training 带来的提升幅度

| 图 | 模型 | gMAP 提升 | gR@10 提升 |
|---|------|----------|-----------|
| Field.Subfield | GCN | **+123%**（0.144 → 0.321） | **+146%**（0.272 → 0.669） |
| Field.Subfield | HGCN | +188%（0.104 → 0.299） | +252%（0.179 → 0.630） |
| Order.Ring | GCN | **+40%**（0.208 → 0.291） | **+54%**（0.406 → 0.624） |
| Order.Ring | HGCN | +97%（0.148 → 0.291） | +131%（0.262 → 0.606） |

---

## 4. 这组结果意味着什么

### 4.1 训练目标对齐显著改善了 retrieval 指标

在两张图上，grouped softmax 训练均带来了大幅度的 retrieval 性能提升。以 grouped MAP 为例：

- Field.Subfield GCN: 从 0.144 跃升至 0.321（+123%）
- Order.Ring GCN: 从 0.208 提升至 0.291（+40%）

这证实了此前"训练做二分类、评测看 retrieval"确实是一个显著的性能瓶颈。binary AP 虽然很高（~0.97），但这只是说明模型学会了区分正负边，并不意味着它擅长在候选池中排序。

### 4.2 GCN 在 Field.Subfield 上仍然占优，但 GCN/HGCN 差距大幅缩小

| 对比维度 | Binary Training | Grouped Training | 变化 |
|---------|----------------|-----------------|------|
| Field.Subfield GCN/HGCN gMAP 比值 | 1.39× | 1.07× | 差距从 39% 缩至 7% |
| Order.Ring GCN/HGCN gMAP 比值 | 1.41× | 1.00× | 差距消失（并列） |

**Field.Subfield**：GCN 仍然在 grouped retrieval training 下优于 HGCN（gMAP 0.321 vs 0.299），但差距从 binary training 的 39% 缩小到 7%。

**Order.Ring**：GCN 和 HGCN 在 gMAP 上完全持平（均为 0.291），HGCN 甚至在 gMRR（0.347 vs 0.339）和 ranking MRR（0.178 vs 0.176）上微弱领先。这是整个项目中首次出现 HGCN 在整体 retrieval 指标上追平甚至略超 GCN 的信号。

### 4.3 Binary AP 的下降是预期且正确的

Binary AP 从 ~0.97 下降到 0.54-0.61 并非退步。模型不再优化逐边分类，而是优化查询内排序，因此边级别的 binary AP 自然会降低。这正是训练目标更对齐任务结构的表现。

---

## 5. Hop 分桶分析

### 5.1 Grouped Retrieval Training 下的 hop 分桶（5-seed 聚合）

#### Field.Subfield

| 模型 | hop_2 MAP | hop_3 MAP | hop_4+ MAP | hop_2 R@10 | hop_3 R@10 | hop_4+ R@10 |
|------|-----------|-----------|------------|------------|------------|-------------|
| Grouped GCN | 0.242 ± 0.046 | 0.229 ± 0.069 | 0.273 ± 0.068 | 0.561 ± 0.067 | 0.507 ± 0.071 | 0.502 ± 0.092 |
| Grouped HGCN | 0.248 ± 0.048 | 0.204 ± 0.080 | 0.270 ± 0.041 | 0.523 ± 0.044 | 0.494 ± 0.129 | 0.517 ± 0.092 |

#### Order.Ring

| 模型 | hop_2 MAP | hop_3 MAP | hop_4+ MAP | hop_2 R@10 | hop_3 R@10 | hop_4+ R@10 |
|------|-----------|-----------|------------|------------|------------|-------------|
| Grouped GCN | 0.167 ± 0.029 | 0.191 ± 0.025 | 0.238 ± 0.022 | 0.436 ± 0.070 | 0.488 ± 0.047 | 0.538 ± 0.047 |
| Grouped HGCN | 0.180 ± 0.027 | 0.206 ± 0.020 | **0.264 ± 0.015** | 0.456 ± 0.064 | 0.498 ± 0.047 | **0.560 ± 0.025** |

### 5.2 Hop 分桶的关键观察

1. **Order.Ring 上 HGCN 在所有 hop 深度上均略优于 GCN**：
   - hop_2 MAP: HGCN 0.180 vs GCN 0.167
   - hop_3 MAP: HGCN 0.206 vs GCN 0.191
   - hop_4+ MAP: HGCN 0.264 vs GCN 0.238
   - R@10 在所有 hop 上也是 HGCN 领先

   但整体 grouped MAP 两者持平（0.291 vs 0.291），说明 HGCN 在 hop-bucket 内的微弱优势被查询分布的加权平均抵消了。

2. **Field.Subfield 上两者在 hop 分桶内交替领先**：
   - hop_2 MAP: HGCN 0.248 > GCN 0.242
   - hop_3 MAP: GCN 0.229 > HGCN 0.204
   - hop_4+ MAP: GCN 0.273 ≈ HGCN 0.270
   - R@10 在 hop_4+ 上 HGCN 反而略高（0.517 vs 0.502）

3. **与上一阶段 binary training 的对比**：上一阶段 binary training 的 Field.Subfield hop_2 MAP 只有 0.077-0.087，grouped softmax 训练将 hop_2 MAP 提升到 0.24-0.25，约 3 倍改善。所有 hop 深度均有显著提升。

---

## 6. 对项目主线的影响

### 6.1 核心结论更新

本阶段的结果需要更新上一阶段的结论。目前最准确的表述是：

> 1. 训练目标与 retrieval 任务的错配确实是一个显著瓶颈。从 binary classification 切换到 grouped softmax 训练后，retrieval 指标在两张图上均有 40%-252% 的提升。
> 2. 在 Field.Subfield 上，GCN 仍然优于 HGCN（gMAP 0.321 vs 0.299），但差距从 39% 缩小到 7%。
> 3. 在 Order.Ring 上，GCN 与 HGCN 的差距已完全消失（gMAP 均为 0.291），HGCN 在 gMRR 和 hop-bucket 分析上甚至出现微弱领先。
> 4. 此前"GCN 大幅优于 HGCN"的结论中，相当一部分可归因于训练目标错配，而非纯粹的几何模型差异。
> 5. 但即便在对齐训练目标后，HGCN 也未能在 Field.Subfield 上形成稳定反超，说明双曲几何的优势仍然受限于图结构。

### 6.2 对论文叙事的影响

这组结果对论文的贡献是双向的：

**正面贡献**：
- 训练目标对齐带来巨大改善，本身就是有价值的实验发现
- GCN/HGCN 差距的缩小说明之前的负结果部分来自实验设计，这加强了对诊断框架价值的论证
- Order.Ring 上的 hop-bucket 分析为"何时双曲可能有效"提供了更细粒度的证据

**需谨慎表述的部分**：
- HGCN 只在 Order.Ring 上追平 GCN，在 Field.Subfield 上仍落后
- 即使追平，也并非大幅超越
- 样本量较小（5 seeds × 2 graphs），不宜过度解读微弱差异

### 6.3 建议的论文定位

基于目前所有证据，论文最有说服力的叙事应是：

> 1. 我们构建了面向真实 traced Lean/Mathlib hierarchy 图的标准化实验管线
> 2. 我们发现训练目标与 retrieval 任务之间的错配是影响模型性能的关键因素
> 3. 在对齐训练目标后，双曲模型在部分图上追平了欧氏模型，但未能形成稳定优势
> 4. Hop-bucket 分析显示，双曲几何在某些中间深度 ancestor bucket 上可能有局部优势，但这种优势高度依赖于图结构
> 5. 这些发现共同指向一个更根本的结论：当前 traced formal math hierarchy 图的结构特征（浅层化、碎片化、star-like instance_of）可能才是限制双曲方法发挥的根本原因，而非模型设计本身

---

## 7. 可直接改写为论文实验段落的短版文字

> We further investigated whether the previously observed GCN advantage over HGCN was partly caused by training-evaluation mismatch — specifically, training with binary cross-entropy on individual edges while evaluating with grouped multi-positive retrieval metrics. We replaced the training objective with query-grouped softmax (InfoNCE) loss, where each `(source, relation)` query forms a group of positives and sampled negatives, and the model optimizes the mean log-probability of true positives under a softmax over all candidates. On `Mathlib.Algebra.Field.Subfield` (133 nodes), this change improved grouped MAP from `0.144 ± 0.023` to `0.321 ± 0.022` for GCN and from `0.104 ± 0.017` to `0.299 ± 0.037` for HGCN. On `Mathlib.Algebra.Order.Ring` (253 nodes), grouped MAP improved from `0.208 ± 0.024` to `0.291 ± 0.020` (GCN) and from `0.148 ± 0.019` to `0.291 ± 0.023` (HGCN). Critically, the GCN/HGCN gap on `Order.Ring` disappeared entirely (both at grouped MAP = 0.291), with HGCN showing slight advantages in grouped-MRR (0.347 vs 0.339) and all hop-bucket metrics. On `Field.Subfield`, GCN maintained a marginal 7% lead in grouped MAP (0.321 vs 0.299), substantially reduced from the 39% gap under binary training. These results indicate that the previously reported GCN dominance was partly attributable to training-objective mismatch rather than purely to geometric model superiority, though HGCN still did not achieve consistent gains across both graphs.

中文版：

> 我们进一步研究了此前观察到的 GCN 优势是否部分源于训练-评测错配——即使用二元交叉熵逐边训练，却以 grouped multi-positive retrieval 指标评测。我们将训练目标替换为查询分组 softmax (InfoNCE) 损失：每个 `(source, relation)` 查询构成一组正例与采样负例，模型在所有候选上做 softmax 并优化正例的平均 log-probability。在 `Mathlib.Algebra.Field.Subfield`（133 节点）上，这一改变将 GCN 的 grouped MAP 从 `0.144 ± 0.023` 提升至 `0.321 ± 0.022`，HGCN 从 `0.104 ± 0.017` 提升至 `0.299 ± 0.037`。在 `Mathlib.Algebra.Order.Ring`（253 节点）上，grouped MAP 从 `0.208 ± 0.024` 提升至 `0.291 ± 0.020`（GCN），从 `0.148 ± 0.019` 提升至 `0.291 ± 0.023`（HGCN）。值得注意的是，`Order.Ring` 上 GCN/HGCN 的差距完全消失（grouped MAP 均为 0.291），HGCN 在 grouped-MRR（0.347 vs 0.339）和所有 hop 分桶指标上甚至略占优势。在 `Field.Subfield` 上，GCN 仍保持 7% 的微弱领先（0.321 vs 0.299），但相比 binary training 下 39% 的差距已大幅缩小。这些结果表明，此前报告的 GCN 主导地位部分归因于训练目标错配而非纯粹的几何模型优劣，但 HGCN 仍未在两张图上形成稳定优势。

---

## 8. 下一阶段最合适的工作

### 8.1 第一优先级：将 grouped retrieval training 扩展到更多图

当前结果仅在 2 张图上，需要扩展到：
- `batteries` 全图（已有 trace）
- 更多 `Mathlib` 模块级子图（如 `Ring.Subring`、`Algebra.Order` 更大簇）
- 此前的 explicit_only / synthesized_only / hierarchy_mixed 拆分图

目标：验证 grouped softmax 的改善是否跨图稳定，以及 GCN/HGCN 差距缩小的趋势是否可复现。

### 8.2 第二优先级：补齐 explicit / synthesized / mixed relation 拆分实验

上一阶段在 `batteries` 上做了 relation provenance 拆分（explicit_only / synthesized_only / hierarchy_mixed），但用的是 binary training。应该：
- 在拆分图上复跑 grouped retrieval training
- 比较 explicit（extends）与 synthesized（instance_of）边在 grouped softmax 下的学习效果差异
- 结合图结构诊断分析 star-like instance_of 边对 retrieval 性能的影响

### 8.3 第三优先级：探索更强的 retrieval 训练策略

当前 grouped softmax 已经大幅改善，但还有探索空间：
- Hard negative mining（按难度分级的负例采样）
- Temperature scaling（InfoNCE 温度参数调节）
- 多正例 contrastive loss 的变体
- 在 encoder 层面注入 relation-aware attention

---

## 9. 一句话结论

> 训练目标对齐是关键：从 binary classification 切换到 grouped softmax retrieval training 后，retrieval 指标在两张 Mathlib hierarchy 子图上均获得 40%-252% 的提升；GCN/HGCN 差距在 Order.Ring 上完全消失，在 Field.Subfield 上从 39% 缩小到 7%。这说明此前"GCN 大幅优于 HGCN"的结论部分来自训练目标错配，但即便在对齐后，HGCN 也未形成稳定反超。
