# T41 通俗解释：Provenance Split 图的结构诊断

## 1. 这个任务在做什么？（通俗解释）

在 T40 中，我们冻结了三类 provenance 图的定义和配置：

- **explicit_only**：只包含程序员手写的 `extends` 继承边
- **synthesized_only**：只包含编译器自动生成的 `instance_of` 实例边
- **hierarchy_mixed**：两者都有

T40 只是写了配置文件和协议文档，但没有真正运行代码把这三类图"切出来"。

T41 就是实际动手的这一步：**用 T40 冻结的配置，把两张候选图（Field.Subfield 和 Order.Ring）各自切成 explicit_only / synthesized_only / hierarchy_mixed 三份，然后对切出来的六个图做结构诊断，比较它们的深度、叶子比例、连通性和双曲性代理指标。**

为什么要这么做？因为项目的一个核心问题是：**Lean 编译器自动生成的 synthesized 边，是不是在"稀释"层级信号，让双曲模型的优势无法释放？** 要回答这个问题，我们必须先从结构上搞清楚：这三类图到底长什么样？

打个比方：T40 是"画出实验方案"，T41 是"按方案做实验"。

## 2. 任务的实现详解

### 2.1 任务目标

1. 运行 T40 冻结配置，实际生成六个 provenance split 图目录
2. 校验每个 split 的边数与协议预期值一致
3. 程序化验证 `hierarchy_mixed = full source graph`（因为当前候选图不含 `uses` 边）
4. 对六个 split 图运行结构诊断
5. 产出比较报告，记录关键结构发现

### 2.2 任务流程

#### 第一步：生成 provenance split 图

Worker 运行了两次 `split_relations_by_provenance.py`，分别使用 T40 冻结的两份配置：

```bash
python split_relations_by_provenance.py --config provenance_split_field_subfield_t40.json
python split_relations_by_provenance.py --config provenance_split_order_ring_t40.json
```

每次运行生成三个目录，每个目录包含 `declarations.csv`、`edges.csv`、`stats.json`。总共六个目录：

| 目录 | 节点数 | 边数 | 边类型 |
| --- | ---: | ---: | --- |
| `mathlib_field_subfield_v1_explicit_only` | 89 | 116 | extends |
| `mathlib_field_subfield_v1_synthesized_only` | 67 | 36 | instance_of |
| `mathlib_field_subfield_v1_hierarchy_mixed` | 133 | 152 | extends + instance_of |
| `mathlib_order_ring_v1_explicit_only` | 125 | 180 | extends |
| `mathlib_order_ring_v1_synthesized_only` | 183 | 120 | instance_of |
| `mathlib_order_ring_v1_hierarchy_mixed` | 253 | 300 | extends + instance_of |

所有边数与 T40 协议中的预期值完全一致。

#### 第二步：校验边数和 identity

Worker 逐一对比了六个 split 的 `stats.json` 中的 `num_edges` 与协议预期值，全部匹配。

同时验证了 `hierarchy_mixed` 与源图的节点数和边数完全相同：
- Field.Subfield：133 节点、152 边 — 完全一致
- Order.Ring：253 节点、300 边 — 完全一致

报告明确标注这只是当前数据的事实（不含 `uses` 边），不是逻辑必然。

#### 第三步：运行结构诊断

Worker 创建了诊断配置 `graph_diagnostics_provenance_split_t41.json`，使用已有的 `run_graph_diagnostics.py` 对六个图运行结构诊断。诊断结果存放在 `artifacts/diagnostics/provenance_split_t41/`。

#### 第四步：撰写比较报告

`docs/experiment_reports/provenance_diagnostics.md` 包含 8 个章节：

1. **Edge Count Verification** — 六个 split 的边数校验表
2. **hierarchy_mixed Identity Verification** — 程序化 identity 验证
3. **Overview Comparison** — 全图层面的结构对比（连通性、cycle rank、diameter、delta/maxdist）
4. **Relation Layer Comparison** — 层级层面的对比（longest chain、multi-parent、leaf ratio、hyperbolicity proxy）
5. **Structural Interpretation** — 四条关键结构解读
6. **Diagnostics Protocol Classification** — 用 `diagnostics_protocol.md` 的阈值给每个图分类
7. **Artifacts** — 产物路径索引
8. **Commands Used** — 可复现的命令

#### 第五步：更新治理文档

- `docs/04_task_board.md`：新增 T41 执行记录
- `docs/07_handoff.md`：更新当前状态和下一步指引
- `docs/08_risks_and_open_questions.md`：R06 改为 Mitigated、R26 改为 Mitigated、新增 R27、更新 Open Question 3

### 2.3 核心发现

报告最重要的结构发现是：

**Synthesized 边是平坦的星状森林：**
- longest chain = 1（所有 `instance_of` 边都是单跳，没有链式结构）
- multi-parent = 0（没有节点同时被多条边指向）
- cycle rank = 0, delta/maxdist = 0.000（结构上完全平坦）

**所有层级深度来自 Explicit 边：**
- longest chain 9–10（`extends` 继承链可以长达 9 到 10 层）
- multi-parent 40–66（有大量的多父节点分支）
- 适中的 hyperbolicity proxy（0.136–0.286）

**混合图从 synthesized 边继承的是碎片化，不是深度：**
- 叶子比例膨胀（Field.Subfield: 0.124 → 0.278; Order.Ring: 0.208 → 0.502）
- 连通分量增多（Field.Subfield: 5 → 13 个分量）
- longest chain、cycle rank、multi-parent 均不因加入 synthesized 边而增长

### 2.4 对后续开发的意义

1. **T42 的 primary split 应该是 `explicit_only`**：这是结构上最值得检验双曲优势的图——最深链、最多分支、最低叶子比例。如果 HGCN 要在任何 provenance split 上超过 GCN，最有可能就是在 `explicit_only` 上。

2. **T42 的 `synthesized_only` 应作为受控诊断**：longest chain = 1 意味着 grouped retrieval 任务退化为几乎平凡的单正例分类。在这个图上的模型对比几乎没有意义。

3. **T42 的 `hierarchy_mixed` 可作为一致性校验**：因为 `hierarchy_mixed` 等于完整源图，T42 在 `hierarchy_mixed` 上的结果应该与 T32/T33 的结果一致。如果不一致，说明 provenance split 过程可能引入了问题。

4. **回答了 Open Question 3 的结构部分**：synthesized 边确实不贡献层级深度，它们贡献的是叶子膨胀和碎片化。这对"双曲优势是否被 synthesized 边稀释"给出了明确的"是"的结构性证据。

5. **与 T32/T33 经验观察一致**：T32/T33 发现 HGCN 没有在混合图上建立优势。T41 的结构诊断提供了一个清晰的结构性解释：混合图中的 synthesized 边引入了大量平坦的星状结构，这恰恰是双曲模型最不擅长的图形态。

## 3. 为什么给出 PASS 的 review 结果？

### 3.1 任务目标完全达成

T41 要求做五件事：（1）生成六个 provenance split 图目录，（2）校验边数与协议预期一致，（3）程序化验证 hierarchy_mixed identity，（4）运行结构诊断，（5）产出比较报告。全部完成。

### 3.2 没有伪实现或 hardcode

- 六个 split 目录包含真实的 `edges.csv`，里面是真实的 Lean 声明名称（如 `Semigroup`、`Monoid`、`Subfield.toDivisionRing`），不是占位数据。
- CSV 行数与 `stats.json` 中的边数严格一致（header + N edges）。
- 诊断结果是真实工具输出的 `report.md`、`summary.json` 和六个 graph JSON，不是手写。

### 3.3 遵守了所有约束

- 没有运行模型训练（正确，T41 只是结构诊断）
- 没有覆盖已有 diagnostics（`provenance_split_t41` 是新目录，之前的诊断全部保留）
- 没有把 proxy 写成严格 hyperbolicity 定理（报告始终使用"hyperbolicity proxy"措辞）
- 没有改动 T40 冻结的 provenance 语义

### 3.4 文档诚实

- hierarchy_mixed identity 被标注为"factual observation about current data, not logical invariant"
- 报告清楚区分了已完成的结构分析和待做的模型训练（T42）
- 新增的 R27 风险明确提醒 `synthesized_only` 不应作为主要模型比较对象
- Open Question 3 被标注为"partially answered"，没有声称已完全回答

### 3.5 没有过度工程

报告篇幅与任务复杂度匹配。八个章节分别覆盖了边数校验、identity 校验、全图对比、层级对比、结构解读、分类标注、产物索引和可复现命令。没有添加不必要的内容。

### 3.6 不影响已有功能

没有源代码被修改，没有已有诊断被覆盖，没有 T40 配置被触碰。T41 是一个纯增量任务。

### 3.7 两个小的 scope 问题不影响 PASS

- `relation_split_summary.json` 被覆盖为最近一次运行的输出（脚本的默认行为），但实际 split 数据目录完好无损。
- 诊断配置 `graph_diagnostics_provenance_split_t41.json` 不在 Allowed Files 列表中，但它是运行诊断工具必需的工具侧配置，不是治理文档或代码变更。

这两个问题都已被记录为 Non-blocking，不阻塞任务完成。

综上所述，T41 的工作质量满足 adversarial review 标准，没有 blocking issue，判定为 PASS。
