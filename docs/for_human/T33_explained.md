# T33 任务解释与 Review 说明

## 1. 这个任务在做什么（通俗版）

想象你在做一个考试排名系统：给定一个数学概念（比如"子域"），你需要从一堆候选概念中找出它真正的"祖先"（它继承了哪些类的性质）。系统用图神经网络来学习这种"继承关系"。

之前在 T32 中，我们用了一种叫 GCN 的"普通"图神经网络跑完了 5 次实验（每次用不同的随机种子），得到了一组基准成绩。现在 T33 要做的是：**换一个更特殊的图神经网络——HGCN（双曲图卷积网络），在完全相同的条件下再跑 5 次，看它能不能比 GCN 做得更好。**

HGCN 的特殊之处在于它工作在"双曲空间"而不是普通的"欧氏空间"里。双曲空间天然适合表达树状层次结构（想象一下把一棵无限大的树塞进一个有限的圆盘里）。理论上，如果数据确实有很强的层级结构，HGCN 应该能比 GCN 表现更好。

**结论是：在这两个测试图上，HGCN 没有超过 GCN。** 这说明当前这些数学概念图的层级结构可能不够深、不够"树状"，不足以让双曲几何的优势发挥出来。

## 2. 实现细节

### 2.1 任务目标

T33 的核心目标是：在 T32 已完成的 GCN grouped 5-seed baseline 基础上，用 HGCN 模型在**完全相同的实验条件**下做一组对照实验，以便判断双曲模型在 reviewed grouped protocol 下是否有增益。

### 2.2 任务流程

1. **创建 HGCN 配置文件**：Worker 新增了 4 个配置文件，分别对应两张图（`Field.Subfield` 和 `Order.Ring`）的 base config 和 sweep config。这些配置与 T32 的 GCN 配置**完全相同**，只做了以下 HGCN 相关切换：
   - `model_type` 从 `gcn` 改为 `hgcn`
   - 增加了 HGCN 模型特有字段：`model_variant`、`distance_signal_mode`、`distance_stat_momentum`、`residual_gate_init`、`curvature`、`decoder_hidden_dim`、`grad_clip_norm`

2. **运行 5-seed sweep**：对每张图运行 5 个不同随机种子（7, 42, 123, 2026, 3407，与 T32 相同）的训练和评测。

3. **生成报告**：汇总 5-seed 的 mean ± std 结果，包括 grouped MAP、grouped nDCG、grouped nDCG@10、grouped MRR、Recall@10，以及按 hop 距离分桶的结果。

4. **更新治理文档**：更新任务板、handoff 文档和风险文档。

### 2.3 关键实验结果

| 图 | 模型 | grouped MAP | grouped nDCG | grouped nDCG@10 |
|---|---|---|---|---|
| Field.Subfield | GCN (T32) | 0.4839 ± 0.0783 | 0.6428 ± 0.0653 | 0.5273 ± 0.0850 |
| Field.Subfield | HGCN (T33) | 0.4458 ± 0.1150 | 0.6095 ± 0.0908 | 0.4765 ± 0.1128 |
| Order.Ring | GCN (T32) | 0.5789 ± 0.0346 | 0.7293 ± 0.0340 | 0.6129 ± 0.0506 |
| Order.Ring | HGCN (T33) | 0.5616 ± 0.0312 | 0.7111 ± 0.0296 | 0.5899 ± 0.0414 |

HGCN 在两张图、所有主指标上均未超过 GCN。且 `Field.Subfield` 上 HGCN 的方差明显更大（0.1150 vs GCN 的 0.0783），说明 HGCN 在这个小图上对随机种子更敏感。

### 2.4 对后续开发的意义

这个结果对项目方向有重要影响：

1. **强化了项目定位调整**：当前图结构确实偏浅偏碎，双曲归纳偏置在这种条件下没有显示出优势。这进一步支持了项目主线从"证明 HGCN 优于 GCN"转向"构建 benchmark / protocol / diagnostics 框架"。

2. **Gate D（双曲价值门）未通过**：根据 `docs/02_experiment_plan.md` 的 Gate D 判据，HGCN 在低维下未优于欧氏模型、在更深层 hop bucket 上未形成稳定收益、在更纯层级图上未显著优于基线。这意味着双曲应降级为条件性 follow-up，而非主承诺。

3. **T34 的方向**：下一步 T34 需要汇总 grouped training 与旧 binary training 的差异，写出诊断报告，为后续是否继续押注双曲路线提供结构化证据。

## 3. 为什么给出 PASS 的 review 结果

### 核心判断

T33 worker 完全完成了任务包要求，没有发现任何阻塞性问题。

### 具体验证过程

1. **配置可比性已验证**：我逐字段 diff 了 T32 GCN 和 T33 HGCN 的 base config（两张图各一组），确认除 HGCN 模型特有字段和身份字段外，所有参数完全一致。这意味着实验条件确实可比。

2. **artifact 真实性已验证**：两组 sweep 各有 5 个 seed 子目录，包含 `aggregate.json`、`per_seed_results.csv`、`per_seed_results.json`、`report.md`，且 `failed_runs = []`。

3. **报告数值已验证**：报告中所有 mean ± std 值与 `aggregate.json` 逐字段核对一致，没有手工编造数字。

4. **协议字段已验证**：单 seed `result_summary.json` 包含 `training_loss = sampled_softmax`、`query_key_fields = [src_id, relation_type]`、`query_split_summary.is_query_level_disjoint = true`，与 T32 reviewed protocol 一致。

5. **Allowed files 约束已验证**：T33 worker 的所有变更限于 Allowed files 范围。工作树中的其他变更（如 `CLAUDE.md`、`docs/05_decision_log.md`）属于 Captain 在 T32→T33 过渡期间的历史改动。

6. **没有伪实现**：没有 mock、stub、hardcode 或 fake success path。所有结果来自真实的模型训练。

### 标记的三个非阻塞问题

1. 报告没有显式列出 HGCN vs GCN 的配置差异清单（但经 review 验证差异正确）
2. R24 风险条目标题用了英文而其余条目用中文
3. 报告缺少一段显式的"可比性约束"声明

这三个问题都不影响实验结果的有效性和正确性，可在后续 T34 汇总时补齐。
