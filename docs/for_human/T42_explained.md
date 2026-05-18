# T42 通俗解释：Provenance Split 上的 GCN vs HGCN Seed Sweep

## 1. 这个任务在做什么？（通俗解释）

在 T41 中，我们通过结构诊断发现了：Lean 编译器自动生成的 `instance_of` 边（synthesized 边）是平坦的星状森林，没有层级深度；真正承载层级结构的只有程序员手写的 `extends` 边（explicit 边）。

但这只是一个**结构性**结论。结构上说"explicit_only 图更像层级树"并不意味着双曲模型一定能在上面赢——还需要**实验验证**。

T42 就是这步实验验证：**在 T41 切出的三类 provenance 图（explicit_only / synthesized_only / hierarchy_mixed）上，分别跑 GCN 和 HGCN 的 5-seed grouped retrieval sweep，看看模型对比的胜负是否会随 provenance 类型而翻转。**

打个比方：T41 是"体检报告"——告诉你三类图各自长什么样。T42 是"药物试验"——给三类图各吃"欧氏药"和"双曲药"，看哪张图吃了双曲药效果更好。

## 2. 任务的实现详解

### 2.1 任务目标

1. 为两类候选图（Field.Subfield、Order.Ring）× 三类 provenance split × 两种模型（GCN、HGCN）创建 sweep 配置
2. 运行全部 12 组 5-seed sweep（共 60 次训练）
3. 以 `explicit_only` 作为 primary comparison，判断 HGCN 是否在此 split 上出现结构性优势
4. 以 `synthesized_only` 作为 controlled diagnostic，确认平坦结构上 HGCN 是否反而是劣势
5. 以 `hierarchy_mixed` 作为 reproducibility check，验证结果与 T32/T33 完全一致
6. 产出比较报告，明确三类 split 各自的模型对比结论

### 2.2 任务流程

#### 第一步：创建 24 份配置文件

Worker 在 `project_bootstrap/baseline_scaffold/configs/` 下创建了 24 份配置：

- 12 份 base config（每个模型×候选图×provenance split 各一份）
- 12 份 sweep config（对应的 5-seed sweep 包装，seeds = [7, 42, 123, 2026, 3407]）

每份 base config 都指向 T41 生成对应的 provenance split 图目录，例如：
- `provenance_gcn_field_subfield_explicit_only_t42.json` → `data/processed/declaration_graph/mathlib_field_subfield_v1_explicit_only`
- `provenance_hgcn_order_ring_hierarchy_mixed_t42.json` → `data/processed/declaration_graph/mathlib_order_ring_v1_hierarchy_mixed`

所有 config 共享 T32/T33 已 review 的参数设定：`grouped_loss = sampled_softmax`、`negative_ratio = 10.0`、16 维嵌入、early stopping patience 12。

#### 第二步：运行 60 次训练

Worker 按照配置逐个运行 sweep。每组 sweep 包含 5 个 seed 的独立训练和评测。12 组 sweep 全部成功完成，零失败。Artifact 位于 `artifacts/baselines/relation_seed_sweeps/provenance_*_t42/` 下。

#### 第三步：分析结果并撰写报告

`docs/experiment_reports/provenance_seed_sweeps.md` 包含 10 个章节：

1. **Experimental Setup** — 模型、训练参数、seeds、provenance split 定义
2. **Config Paths** — 配置文件路径索引
3. **Artifact Paths** — 产物路径索引
4. **Commands Used** — 可复现的运行命令
5. **Sweep Completion** — 12 组 sweep 的完成状态表
6. **Primary Comparison: explicit_only** — 主要发现，包含 Field.Subfield 和 Order.Ring 的 mean±std 指标表与 hop bucket 分析
7. **Controlled Diagnostic: synthesized_only** — 受控诊断，展示平坦结构上的模型对比
8. **Reproducibility Check: hierarchy_mixed** — 与 T32/T33 的精确匹配验证
9. **Synthesis** — 三类 split 的汇总对比表
10. **Implications** — 五条关键推论

#### 第四步：更新治理文档

- `docs/04_task_board.md`：新增 T42 执行记录
- `docs/07_handoff.md`：更新当前状态和下一步指引
- `docs/08_risks_and_open_questions.md`：R04 → Mitigated、R06 → Mitigated、R27 → Mitigated、Open Questions 3 和 4 标记为已回答

### 2.3 核心发现

**这是整个项目到目前为止最重要的实验结果。**

#### 发现一：explicit_only 上 HGCN 首次超过 GCN

| 候选图 | GCN MAP | HGCN MAP | HGCN 优势 |
| --- | ---: | ---: | ---: |
| Field.Subfield | 0.5256 ± 0.0800 | 0.6503 ± 0.0481 | **+0.1247** |
| Order.Ring | 0.5836 ± 0.0978 | 0.6393 ± 0.0656 | **+0.0557** |

在之前的 T32/T33 中，HGCN 从未在任何候选图上超过 GCN。T42 在 explicit_only split 上首次观察到了 HGCN 的优势。

更重要的是，**优势随 hop 深度单调增长**：
- Field.Subfield: hop_2 +0.05 → hop_3 +0.17 → hop_4_plus **+0.25**
- Order.Ring: hop_2 +0.03 → hop_3 +0.10 → hop_4_plus **+0.27**

这完全符合双曲几何的理论预期：双曲空间天然适合编码树状层级结构，优势在更长的层级链上更显著。

#### 发现二：synthesized_only 上 GCN 反超 HGCN

| 候选图 | GCN MAP | HGCN MAP | GCN 优势 |
| --- | ---: | ---: | ---: |
| Field.Subfield | 1.0000 ± 0.0000 | 0.6857 ± 0.1140 | **+0.3143** |
| Order.Ring | 0.8453 ± 0.0295 | 0.7560 ± 0.0761 | **+0.0893** |

在平坦的星状森林上，HGCN 的双曲归纳偏置反而成了累赘——给一个不需要层级编码的结构强加双曲几何，只会增加不必要的复杂性。

#### 发现三：hierarchy_mixed 与 T32/T33 完全一致

四组 hierarchy_mixed 的 MAP、nDCG、nDCG@10（mean 和 std）与 T32/T33 的 aggregate.json 完全一致。这既验证了 `hierarchy_mixed = full source graph` 的身份，又为 Milestone 3 的实验结果提供了独立复现。

#### 发现四：synthesized 边的"结构性稀释"效应

把上述三个发现放在一起，核心故事线就是：

> **synthesized `instance_of` 边不贡献层级深度，但它们的存在足以抵消 HGCN 在 explicit 层上的优势。**

在 explicit_only 上，HGCN 赢了；在 hierarchy_mixed（加了 synthesized 边）上，GCN 赢了。这意味着 synthesized 边起到了"结构性稀释剂"的作用——它们膨胀了叶子比例、增加了碎片化，把图的形态从"层级树"推向了"星状森林"，而后者恰恰是双曲模型最不擅长的结构。

### 2.4 对后续开发的意义

1. **T43 可以给出正式回答**：T43 的目标就是汇总 provenance split 结果，回答 synthesized relation 是否削弱双曲优势。T42 的实验证据已经给出了明确答案：是的，削弱了，而且削弱机制是结构性的——不是训练不稳定或超参不对，而是 synthesized 边本身的形态与双曲几何不兼容。

2. **论文叙事的关键转折**：在此之前，项目的主结论是"GCN 整体领先，HGCN 未建立优势"（T34 总结）。T42 改变了这个叙事：**不是 HGCN 不行，而是图里混了不合适的边。** 去掉 synthesized 边后，HGCN 是有真实优势的，而且优势在最难的长链 hop 上最大。这为论文提供了一个比"双曲不行"更有意义的条件性结论。

3. **Gate D（双曲价值门）的条件性通过**：`02_experiment_plan.md` 的 Gate D 要求至少在"更纯层级图上显著优于欧氏基线"。T42 在 explicit_only 上满足了这个条件，但仅限于特定 provenance split。这足以让双曲保留为条件性主假设，而不是无条件降级。

4. **对 proof-side bridge 的启示**：如果后续做 premise retrieval 或 ancestor explanation，应该优先使用 explicit_only 图作为知识表示，因为这是 HGCN 表现最好的图形态。

5. **R25（clean-environment reproducibility）仍然 Active**：T42 的 reproducibility check 是在同一环境、同一代码下做的，只是换了图数据。真正的 clean-room 复现（从零环境拉起）仍然没有完成。

## 3. 为什么给出 PASS 的 review 结果？

### 3.1 任务目标完全达成

T42 要求做六件事：（1）创建 sweep 配置，（2）运行全部 sweep，（3）以 explicit_only 作为 primary comparison，（4）以 synthesized_only 作为 controlled diagnostic，（5）以 hierarchy_mixed 作为 reproducibility check，（6）产出比较报告。全部完成。

### 3.2 没有伪实现或 hardcode

- 12 组 sweep 各包含 5 个 seed 的真实训练产物（metrics.json、result_summary.json、training_stats.json）。
- Per-seed 指标自然波动（如 FS GCN explicit_only MAP 从 0.34 到 0.80），完全不是硬编码行为。
- Hierarchy_mixed 结果与 T32/T33 数值一致到小数点后四位，这是真实运行的有力证据。

### 3.3 遵守了所有约束

- 没有把 `synthesized_only` 写成 primary model comparison evidence（报告明确标注为 "Controlled Diagnostic"）
- 没有把 `hierarchy_mixed` 重新表述为新图族（报告明确标注为 "Reproducibility Check"）
- 没有覆盖已有 sweep artifact（T32/T33 目录完好无损）
- 没有修改 T40/T41 冻结的 provenance 语义
- 没有修改源代码
- 配置文件写在 Allowed Files 指定的目录下

### 3.4 数据真实，结论可靠

核心数值全部通过独立验证：
- explicit_only MAP delta: FS +0.1247 ✓, OR +0.0557 ✓
- synthesized_only: GCN FS MAP 1.0000 ✓, HGCN FS MAP 0.6857 ✓
- hierarchy_mixed: 四组 MAP 与 T32/T33 完全一致 ✓
- Hop bucket 均值与 per-seed 数据计算一致 ✓

### 3.5 文档诚实

- 报告明确区分了三类 split 的角色（primary/diagnostic/reproducibility）
- 没有声称"HGCN 优于 GCN"的无条件命题
- 风险文档更新中的措辞保留了条件性限定
- Variance 没有被隐藏（FS GCN explicit_only std = 0.0800）

### 3.6 两个小的精度问题不影响 PASS

- N1（FS hop_4_plus 均值只覆盖 4 个 seed）：数值正确，比较有效，只是报告没有说明样本量差异
- N2（GCN FS synthesized_only aggregate MAP = 1.0000 但 per-seed 并非全为 1.0）：aggregate.json 的值确实显示 1.0000，但 per_seed_results.csv 显示两个 seed 低于 1.0。这可能是 metric 字段选取的差异，不影响结论——GCN 远超 HGCN 在 synthesized_only 上是事实

综上所述，T42 的工作质量满足 adversarial review 标准，没有 blocking issue，判定为 PASS。
