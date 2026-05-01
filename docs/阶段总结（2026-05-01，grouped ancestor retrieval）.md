# 阶段总结（2026-05-01，grouped ancestor retrieval）

> 主题：将 `ancestor_ranking` 从单正例 ranking 升级为 `grouped multi-positive ancestor retrieval`，并据此重新评估当前 GCN/HGCN 结论。

---

## 1. 本阶段完成了什么

本阶段最重要的进展，不是又补了一轮模型，而是把 `ancestor_ranking` 的评测口径从“单个 `(src, relation, dst)` 的单正例排序”升级成了更符合真实任务结构的 **grouped multi-positive retrieval**：

1. 同一个 `(src, relation)` 下的所有真祖先都被视为正例，不再只看其中一个目标节点的 rank。
2. 默认汇报指标改为：
   - `Recall@1/3/5/10`
   - `MAP`
   - `nDCG`
   - `nDCG@10`
   - `grouped-MRR`
3. 额外补上了按 hop 分桶的评测：
   - `hop_2`
   - `hop_3`
   - `hop_4_plus`
4. 该协议已经在真实 `Mathlib` 模块级子图上完成单次复现和五个随机种子的聚合对照。

相关产物已经固化到：

- `artifacts/baselines/relation_seed_sweeps/grouped_multi_positive_summary_2026-05-01.md`
- `artifacts/baselines/relation_seed_sweeps/grouped_multi_positive_summary_2026-05-01.json`

---

## 2. 为什么这一步是必要的

此前的 `ancestor_ranking` 实际上存在明显的任务口径错配。根据已有 task-structure 诊断：

- `Field.Subfield` 的 `ancestor_ranking` 测试集中，平均每个 `(src, relation)` 有 `25.24` 个真祖先，单正例 `MRR` 的 `positive-block ceiling` 只有 `0.2431`。
- `Order.Ring` 的 `ancestor_ranking` 测试集中，平均每个 `(src, relation)` 有 `23.07` 个真祖先，单正例 `MRR` 的 `positive-block ceiling` 只有 `0.2221`。

这意味着旧协议低估模型几乎是必然的，因为它把一个天然的“多正例祖先检索”任务，压成了“单目标命中排名”任务。

因此，本阶段的核心不是“给 HGCN 找借口”，而是先把评测协议修正到与任务结构一致，再重新判断当前结论是否成立。

---

## 3. 新协议下的主要实验结果

### 3.1 五个随机种子的聚合结果

在 `Field.Subfield` 和 `Order.Ring` 两张更深层的 `Mathlib` hierarchy 子图上，当前 grouped 协议下的五 seed 聚合结果如下：

| 子图 | 模型 | grouped MAP | grouped nDCG | grouped-MRR | Recall@10 |
| --- | --- | ---: | ---: | ---: | ---: |
| `Field.Subfield` | GCN | `0.1441 ± 0.0225` | `0.3527 ± 0.0201` | `0.1815 ± 0.0357` | `0.2721 ± 0.0596` |
| `Field.Subfield` | HGCN | `0.1038 ± 0.0171` | `0.3137 ± 0.0148` | `0.1407 ± 0.0348` | `0.1793 ± 0.0608` |
| `Order.Ring` | GCN | `0.2082 ± 0.0242` | `0.4192 ± 0.0195` | `0.2604 ± 0.0285` | `0.4060 ± 0.0452` |
| `Order.Ring` | HGCN | `0.1482 ± 0.0186` | `0.3616 ± 0.0185` | `0.1970 ± 0.0247` | `0.2621 ± 0.0487` |

若保留旧口径的 `ranking_test_mrr` 仅作参考，则：

- `Field.Subfield`：GCN `0.0934 ± 0.0172`，HGCN `0.0719 ± 0.0151`
- `Order.Ring`：GCN `0.1393 ± 0.0144`，HGCN `0.1107 ± 0.0121`

### 3.2 这组结果意味着什么

这轮结果说明两件事同时成立：

1. **旧单正例 MRR 协议确实有问题。**
   新的 grouped 协议更贴近任务本身，也更适合作为以后默认口径。
2. **但协议修正后，GCN 仍然稳定强于 HGCN。**
   换句话说，先前“GCN 明显更强”的结论并不是主要由单正例评测错配造成的假象。

更精确地说，当前可以把主张收敛为：

> 在更合理的 grouped multi-positive ancestor retrieval 口径下，relation-aware 欧氏 GCN 仍然是当前更强、更稳定的 baseline；双曲模型的潜在优势即使存在，也还没有在现有 traced `Mathlib` hierarchy 子图上形成稳定反超。

---

## 4. hop 分桶结果的额外信息

按 hop 分桶以后，可以看到一个比“谁赢了”更细的现象。

### 4.1 `Field.Subfield`

| 模型 | hop_2 MAP | hop_3 MAP | hop_4+ MAP | hop_2 R@10 | hop_3 R@10 | hop_4+ R@10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GCN | `0.0768` | `0.1170` | `0.1624` | `0.1780` | `0.2609` | `0.3341` |
| HGCN | `0.0872` | `0.0633` | `0.1077` | `0.1683` | `0.1217` | `0.1585` |

这里 GCN 随 hop 增大而持续提升，说明更深祖先并没有把欧氏模型“自然压垮”；相反，GCN 在更深祖先上的 retrieval 反而更稳定。HGCN 只在 `hop_2 MAP` 上略高于 GCN，但在 `hop_3 / hop_4+` 上没有形成持续优势。

### 4.2 `Order.Ring`

| 模型 | hop_2 MAP | hop_3 MAP | hop_4+ MAP | hop_2 R@10 | hop_3 R@10 | hop_4+ R@10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GCN | `0.0820` | `0.1120` | `0.2671` | `0.1697` | `0.2987` | `0.5412` |
| HGCN | `0.0615` | `0.1182` | `0.1756` | `0.1502` | `0.2518` | `0.3438` |

`Order.Ring` 上的信号稍微复杂一些：

1. HGCN 在 `hop_3` 的 `MAP / nDCG / grouped-MRR` 上已经接近甚至局部略高于 GCN。
2. 但一旦看整体 grouped 指标，尤其是 `Recall@10` 和 `hop_4_plus`，GCN 仍然明显占优。

因此，这轮结果更像是在说：

> 双曲信号并非完全不存在，但它目前只是零散地出现在某些中等深度 bucket 上，还没有成长为全局稳健优势。

---

## 5. 当前阶段最稳妥的结论

结合此前的图结构诊断、task-structure 诊断以及本阶段 grouped retrieval 结果，当前最稳妥的结论应写成：

1. `ancestor_ranking` 必须从现在开始默认采用 grouped multi-positive 协议，旧的单正例 `MRR` 不再适合作为主指标。
2. 在更合理的 grouped 口径下，GCN 仍然在 `Field.Subfield` 与 `Order.Ring` 上稳定优于 HGCN。
3. 因此，当前“GCN 更强”并不主要是评测口径错配造成的。
4. 但是，HGCN 在部分 deeper-hop bucket 上开始出现局部可见的信号，这说明“双曲完全无意义”也不能被写成最终结论。
5. 项目的近期主线不应继续围绕“如何再调一个更强 HGCN”展开，而应转向：
   - 协议标准化
   - 任务与训练目标对齐
   - 更大、更深层 hierarchy 目标上的系统复验

---

## 6. 可直接改写为论文实验段落的短版文字

下面这段文字已经接近论文正文风格，可作为后续写作底稿：

> We found that the original `ancestor_ranking` protocol substantially mismatched the task structure of traced `Mathlib` hierarchy graphs, because each `(source, relation)` query typically has many true ancestors rather than a single positive target. We therefore upgraded evaluation to grouped multi-positive ancestor retrieval, where all true ancestors under the same query are treated as positives and performance is reported by grouped `Recall@k`, `MAP`, `nDCG`, and grouped-MRR, together with hop-bucketed breakdowns (`2-hop`, `3-hop`, `4+ hop`). On five random seeds, relation-aware GCN remained consistently stronger than HGCN on both `Mathlib.Algebra.Field.Subfield` and `Mathlib.Algebra.Order.Ring`. For example, on `Order.Ring`, GCN achieved grouped `MAP = 0.2082 ± 0.0242`, grouped `nDCG = 0.4192 ± 0.0195`, and `Recall@10 = 0.4060 ± 0.0452`, compared with HGCN’s `0.1482 ± 0.0186`, `0.3616 ± 0.0185`, and `0.2621 ± 0.0487`. These results show that the previously observed GCN advantage is not primarily an artifact of single-positive ranking mismatch. At the same time, the hop-bucket analysis indicates that weak hyperbolic signals may emerge in some intermediate-depth ancestor buckets, suggesting that the hyperbolic hypothesis is not fully invalidated, but remains unstable under current traced graphs, tasks, and models.

对应的中文短版也可以写成：

> 我们发现，原始 `ancestor_ranking` 协议与 traced `Mathlib` hierarchy 图的真实任务结构存在显著错配：同一个 `(source, relation)` 查询往往对应多个真祖先，而非单个正例目标。为此，我们将评测升级为 grouped multi-positive ancestor retrieval，将同一查询下的所有真祖先统一视为正例，并汇报 grouped `Recall@k`、`MAP`、`nDCG` 与 grouped-MRR，同时补充 `2-hop / 3-hop / 4+ hop` 分桶分析。在 `Mathlib.Algebra.Field.Subfield` 和 `Mathlib.Algebra.Order.Ring` 上的五个随机种子结果显示，relation-aware GCN 仍稳定优于 HGCN。例如在 `Order.Ring` 上，GCN 的 grouped `MAP / nDCG / Recall@10` 分别达到 `0.2082 ± 0.0242 / 0.4192 ± 0.0195 / 0.4060 ± 0.0452`，显著高于 HGCN 的 `0.1482 ± 0.0186 / 0.3616 ± 0.0185 / 0.2621 ± 0.0487`。这表明先前观察到的 GCN 优势并不主要是由单正例 ranking 口径造成的评测假象；但 hop 分桶结果也显示，双曲信号在部分中等深度祖先 bucket 上开始出现局部迹象，因此更合理的结论应是：双曲假设尚未被完全否定，但在当前 traced 图、任务定义与模型设计下仍缺乏稳定证据。

---

## 7. 下一阶段最合适的工作

我认为当前最值得做的，不是继续“追双曲 SOTA”，而是把项目推进到一个更强、更稳、也更容易写成论文的方向。按优先级排序，建议如下。

### 7.1 第一优先级：把 grouped 协议正式固化为默认协议

这一步的目标是让整个项目以后都在统一口径上积累结果，而不是继续混用旧的单正例 `MRR`。

建议直接做三件事：

1. 将 grouped `MAP / nDCG / Recall@k / grouped-MRR` 写入默认 baseline 表模板与实验文档。
2. 将 hop-bucket 统计接到更多已有 sweep 结果上，形成统一 summary。
3. 把“单正例 `MRR` 只作为辅指标”的原则写进方案书/论文的实验协议部分。

这一步投入很小，但收益很高，因为它能把当前项目从“实验还在调口径”推进到“协议已经稳定”。

### 7.2 第二优先级：把训练目标也对齐到 grouped retrieval

当前我们虽然已经修正了评测协议，但训练目标仍然主要是 **binary edge classification**。这意味着现在仍然存在“训练做二分类，测试看 grouped retrieval”的第二层错配。

因此，下一步很适合推进：

1. **query-grouped/listwise ancestor retrieval training**
   - 以 `(src, relation)` 为训练单元。
   - 在候选池上直接优化 sampled softmax / listwise ranking / contrastive retrieval loss。
2. 保持 GCN 与 HGCN 的 encoder 不变，只替换训练目标与 decoder 读出方式。
3. 先在现有 `Field.Subfield / Order.Ring` 上复验，再决定是否值得扩展到更大模块。

这是当前最有希望产生“真正新的研究信息”的一步，因为它能回答一个比“谁赢了”更本质的问题：

> 现在的瓶颈到底来自几何模型，还是来自训练目标和 retrieval 任务之间的错配？

### 7.3 第三优先级：把同一协议迁到更大、更深层的 `Mathlib` 模块

这一步仍然值得继续，但应当建立在“协议已稳定”和“训练目标更对齐”的基础上，而不是马上继续扩新图。

当前更合适的候选顺序是：

1. `Mathlib.Algebra.Order.Ring`
   - 当前已知 `longest_chain` 更深，`ancestor_ranking(min_hops=2)` 正样本也更多。
   - 是最适合作为下一轮主目标的模块。
2. `Mathlib.Algebra.Ring.Subring`
   - 深度与结构也足够好，可以作为第二个复验点。
3. 更大的 `Mathlib.Algebra.Order` 局部簇
   - 可作为“更大但更混合”的对照图。

这一阶段的目标不是再证明一次 “GCN 仍赢”，而是把问题推进到：

> 在更大、更深层、样本更多的真实 hierarchy 子图上，协议修正后、训练目标也对齐后，双曲是否仍然不占优？

如果这个问题的答案仍然是否定的，那么届时“当前 traced formal math hierarchy 未呈现稳定双曲优势”就会成为一个更强、也更可信的论文结论。

### 7.4 第四优先级：从“普通 ancestor retrieval”扩到更贴结构的任务

如果前面三步完成后仍想继续拓展任务，我认为比继续堆 HGCN 结构更有价值的，是补充更贴层级语义的任务：

1. `typed parent retrieval`
   - 将 `extends` 与 `instance_of` 显式区分。
2. `ancestor-set retrieval`
   - 直接预测整组祖先，而不是只做边判断。
3. `hop-aware retrieval`
   - 例如区分“是否属于 2-hop / 3-hop / 4+ hop 祖先”。
4. `path-sensitive ranking`
   - 若后续能导出更精确的 hierarchy path 信息，可以把路径结构也纳入任务。

这些任务的价值在于：即使最终 HGCN 仍然不赢，项目也能自然转化为一个 **formal math graph benchmark / diagnostics / retrieval protocol** 方向，而不是被绑定在单一模型假设上。

---

## 8. 当前最推荐的项目主线

基于目前所有证据，我认为这个项目现在最适合的主线，不再是：

> “证明双曲方法在形式化证明图上优于欧氏方法”

而应调整为：

> “构建真实 traced formal-math hierarchy 图的工程管线、诊断协议与 retrieval benchmark，并系统分析在何种结构与任务条件下双曲归纳偏置可能有效。”

这条主线更强的原因有三点：

1. 它和当前已有证据最一致，不需要硬拗结论。
2. 它的工程积累已经很扎实：trace、normalize、precise hierarchy、graph diagnostics、grouped retrieval 协议都已经具备。
3. 即使最终双曲模型没有赢，这条线仍然能产出一个完整、可信、可投稿的研究故事。

---

## 9. 一句话结论

本阶段最重要的结论是：

> 我们已经证明，旧的单正例 `ancestor_ranking` 口径确实不合理；但在更严格、更贴任务本身的 grouped multi-positive retrieval 协议下，GCN 依然稳定强于 HGCN。因此，项目下一步最值得推进的不是继续微调双曲模型，而是把 grouped retrieval 协议固化为默认标准，并进一步把训练目标与任务结构对齐，再迁移到更大、更深层的真实 `Mathlib` hierarchy 子图上复验。
