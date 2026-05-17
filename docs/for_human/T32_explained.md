# T32 Explained: GCN Grouped Training 5-Seed Sweep

## 1. 这个任务在做什么？（通俗解释）

想象你在维护一个数学知识图谱——比如 Lean/Mathlib 形式化证明库里的类型层级关系。这个图谱里的节点是数学声明（如 `Field`、`Subfield`、`Ring`），边表示"扩展了"（extends）或"是某个类的实例"（instance_of）这样的层级关系。

现在我们想训练一个图神经网络（GCN），让它学会**回答这样一个问题**：

> 给定一个节点和一种关系类型（比如"Field"和"extends"），在所有候选祖先中，哪些才是真正的祖先？排序质量如何？

这就是 **grouped multi-positive ancestor retrieval**——同一个查询下可能有多个正确的祖先，模型需要对它们排序。

**T32 做的事情**就是：在两个具体的子图（`Field.Subfield` 和 `Order.Ring`）上，用已经 review 过的 grouped retrieval 训练路径，跑 **5 个不同随机种子**的 GCN 实验，然后汇总每个指标的平均值和标准差。

为什么跑 5 个种子？因为机器学习训练有随机性（初始化、数据切分、负采样等）。单次结果可能是运气好或运气差，5 次的平均值和标准差才能给出稳定、可复现的基线。

## 2. 实现详解

### 2.1 任务目标

在 `Field.Subfield` 和 `Order.Ring` 两个子图上，使用 T31 已通过 review 的 grouped retrieval runner，运行 GCN 的 5-seed grouped training sweep，产出可审查的 mean ± std 报告。

这是 HGCN 对照之前的**欧氏基线**——先搞清楚 GCN 在 grouped protocol 下表现如何，才能在 T33 中公平对比 HGCN。

### 2.2 任务流程

1. **创建配置文件**：为两个子图各创建一个 base config 和一个 sweep config。
2. **运行 sweep**：使用 seed sweep runner 对 5 个种子（7, 42, 123, 2026, 3407）分别运行训练和评测。
3. **汇总结果**：收集所有种子的指标，计算 mean ± std，写入实验报告。
4. **更新治理文档**：在任务板、交接文档、风险文档中记录本次工作。

### 2.3 配置文件变化

新增 4 个配置文件：

| 文件 | 用途 |
| --- | --- |
| `grouped_gcn_field_subfield_anc_t32.json` | Field.Subfield 的基础配置（单次运行参数） |
| `grouped_gcn_field_subfield_sweep_t32.json` | Field.Subfield 的 sweep 配置（引用 base，指定种子列表） |
| `grouped_gcn_order_ring_anc_t32.json` | Order.Ring 的基础配置 |
| `grouped_gcn_order_ring_sweep_t32.json` | Order.Ring 的 sweep 配置 |

每个 base config 中的关键设置：

- **`grouped_loss = "sampled_softmax"`**：训练使用 grouped softmax loss（而非旧的 binary cross-entropy），让训练目标与评测任务对齐。
- **`negative_ratio = 10.0`**：每个正例采样 10 个负例，显式写死，不依赖默认值。
- **`model_type = "gcn"`**：使用欧氏 GCN，不是双曲 HGCN。
- **`ancestor_label_mode = "source_kind"`**：祖先标签区分 `extends_ancestor` 和 `instance_ancestor`。
- **`target_relation_types = ["extends", "instance_of"]`**：只预测层级关系边。

Sweep config 则简单地引用 base config 并指定 5 个种子。

### 2.4 运行路径

```
sweep config → run_relation_seed_sweep.py
                ↓ (per seed)
              run_relation_grouped_retrieval_baseline.py
                ↓
              build_grouped_ranking_queries()  [T31 reviewed]
                ↓
              sampled_softmax loss, (src_id, relation_type) query key
                ↓
              grouped val MAP checkpoint selection
                ↓
              grouped eval: MAP, nDCG, nDCG@10, MRR, Recall@k, hop buckets
```

这个路径上的每个环节都经过前面 T31A（query-level split）和 T31（grouped training）的 review。T32 没有修改任何 runner 代码，只是创建了新的配置并运行。

### 2.5 产出物

**Artifacts**（在 `artifacts/baselines/relation_seed_sweeps/` 下）：

- `grouped_gcn_field_subfield_t32/`：包含 5 个种子子目录、`aggregate.json`、`report.md`、`per_seed_results.csv/json`
- `grouped_gcn_order_ring_t32/`：同上

每个种子子目录包含：模型嵌入、训练统计、评测结果、split manifest 等。

**实验报告**：`docs/experiment_reports/gcn_grouped_training.md`，记录了精确命令、配置路径、artifact 路径、所有 grouped 指标的 mean ± std、hop bucket 分桶结果。

### 2.6 关键结果

| 图 | grouped MAP | grouped nDCG | grouped nDCG@10 |
| --- | ---: | ---: | ---: |
| Field.Subfield | 0.4839 ± 0.0783 | 0.6428 ± 0.0653 | 0.5273 ± 0.0850 |
| Order.Ring | 0.5789 ± 0.0346 | 0.7293 ± 0.0340 | 0.6129 ± 0.0506 |

注意 `Field.Subfield` 的标准差明显更大（MAP std 0.0783 vs 0.0346），说明这个小图对种子更敏感。这与它被定位为 "controlled probe"（受控探测）而非主战场的角色一致。

### 2.7 对后续开发的意义

1. **T33 的比较基准**：T32 建立了 GCN grouped baseline。T33 将在相同 split、相同参数预算、相同种子下跑 HGCN，形成 GCN vs HGCN 的公平对照。

2. **训练-评测对齐的验证**：T32 是第一个真正在完整 5-seed sweep 中使用 grouped retrieval training 的实验。它证明了 T31 的 grouped training 路径在规模化运行中是可用的。

3. **方差诊断**：`Field.Subfield` 的高方差为后续 T33/T34 提供了重要信号——不应把小图结果等权解读，`Order.Ring` 作为更大的图更适合做主要对照。

4. **Hop bucket 基线**：T32 首次给出了 grouped protocol 下的 hop 分桶基线。后续可以看 HGCN 是否在更深的 hop bucket（如 hop_4_plus）上表现不同。

## 3. 为什么给出 PASS 的 review 结果？

### 3.1 核心检查点

**1. 是否真的完成了任务？**

是的。任务要求在 `Field.Subfield` 和 `Order.Ring` 上各跑 5-seed GCN grouped training sweep，并产出实验报告。两个 sweep 都 5/5 成功完成，报告包含所有要求的指标（grouped MAP、nDCG、nDCG@10、Recall@k、grouped-MRR、hop bucket、mean ± std）。

**2. 是否使用了正确的训练路径？**

是的。通过检查每个种子目录中的 `training_stats.json`（`training_loss = "sampled_softmax"`）、`grouped_training_summary.json`（`query_key_fields = [src_id, relation_type]`）和 `result_summary.json`（`is_query_level_disjoint = true`），确认了训练路径完全走的是 T31 reviewed 的 grouped retrieval runner。

**3. 配置是否显式设置了关键参数？**

是的。两个 base config 都显式写了 `grouped_loss = "sampled_softmax"` 和 `negative_ratio = 10.0`，没有依赖 runner 默认值。

**4. 报告中的数字是否真实？**

是的。我逐项比对了 `aggregate.json` 中的精确数值和 `gcn_grouped_training.md` 中展示的四位小数，所有值完全匹配。

**5. 是否有伪实现或 hardcode？**

没有发现。所有指标来自真实的训练和评测过程，每个种子的结果都是独立运行的，指标之间有一致的内部逻辑（例如 hop bucket 的聚合值与 per-seed 值一致）。

**6. 是否改了不该改的东西？**

没有。Git diff 显示只修改了 3 个允许的治理文档和新增了 5 个允许的文件。没有修改任何源代码，没有碰 HGCN，没有改 T31 的 grouped protocol。

**7. 文档是否把计划写成事实？**

没有。任务板和交接文档都明确写着"pending adversarial review"、"不要切到 T33"。报告清楚标注了这是 GCN-only，HGCN 对照是 T33 的事。

### 3.2 Non-blocking issues

审查中发现了两个非阻塞问题：
1. hop bucket 表格只展示了部分 Recall 指标（详细值在 artifact 的 report.md 中），但这符合任务包"where available"的措辞。
2. 报告中"gMAP"和"grouped MAP"两种写法混用，不影响理解但可以统一。

这些都不影响核心结论，所以判定为 PASS。
