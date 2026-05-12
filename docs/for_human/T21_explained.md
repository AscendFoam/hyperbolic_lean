# T21 通俗解释

## 这个任务在做什么？

T20 告诉我们"哪些数学库的家谱图够深，值得继续研究"。但 T20 只看了已经被提取出来的几张图。

T21 要回答的问题是：**在这些库的更细粒度扫描中，到底有哪些模块是真正值得作为下一步实验对象的？质量如何？**

打个比方：T20 是看了一张地图上的几个城市，说"这几个看起来不错"。T21 是把每个城市的人口普查数据拿来，仔细看看哪个城市的基础设施最好、人口结构最均衡、交通最方便，然后给出一个更靠谱的推荐排序。

## 任务流程详解

### 输入
T21 读取了两套模块级扫描的产物：
- `artifacts/diagnostics/module_hierarchy_scan_mathlib_algebra_order_index_v1/` — Mathlib 代数序相关模块的扫描，包含 103 个候选模块
- `artifacts/diagnostics/module_hierarchy_scan_batteries_v1/` — Batteries 库的扫描，包含 9 个候选模块

### 审计维度
worker 不只看"这张图有多深"，而是从五个角度综合评估：
1. **longest chain**（最长链）：图有多"像树"（深层 vs 浅层）
2. **relation positive edges**（正例边数）：有多少真实的祖先-后代关系可以用来训练和评测
3. **component ratio**（连通分量比）：最大连通分量占全部节点的比例，衡量图的连续性
4. **leaf ratio**（叶子比）：叶子节点占比，越高越像星状森林
5. **ancestor added nodes**（祖先闭包扩展量）：需要从外部引入多少节点才能完成祖先闭包，越高说明这个模块越依赖外部上下文

### 核心产出
`docs/candidate_graph_audit.md` 包含：

1. **审计表**：9 个精选模块的完整指标对比
2. **优先级排序**：
   - P1（最佳平衡候选）：`Mathlib.Algebra.Order.Ring` — 连通性好（0.747）、叶子比适中（0.502）
   - P2（深度压力测试）：`Mathlib.Algebra.Order` — 最深最长（chain=11），但碎片化严重（component ratio 仅 0.489）
   - P3/P4（受控探针）：`Ring.Subring` 和 `Field.Subfield`
3. **二级备选**：`Mathlib.Algebra.Field`、`Small`、`Equiv`
4. **明确排除**：Batteries 模块族（太浅太小）

### 一个重要发现
T20 的排序是 `Order` > `Order.Ring`。但 T21 反转了这个排序：**`Order.Ring` 比 `Order` 更适合作为默认 benchmark**。原因是虽然 `Order` 更大更深，但它的连通性很差（最大连通分量只覆盖 48.9% 的节点），而且叶子占 77.4%。`Order.Ring` 虽然小一些，但 74.7% 的节点在一个连通分量里，结构更紧凑、更适合训练和评测。

另外，T21 还发现扫描工具的 raw hierarchy score 会偏向"小而紧凑"的模块——一个只有 30 个节点的小模块可能得分比 1300 个节点的大模块高，但显然不适合作为 benchmark。这个发现被记录为新的风险 R14。

### 同时更新的文档
- `04_task_board.md`：记录 T21 已完成 worker 执行
- `07_handoff.md`：更新接手说明，反映 T21 的核心审计结论
- `08_risks_and_open_questions.md`：新增 R14 风险，更新开放问题 Q1-Q2

### 对后续开发的意义
T21 直接决定了 Milestone 3（训练对齐）应该选哪张图来做实验。后续 T30+ 的 seed sweep 都应该优先使用 `Mathlib.Algebra.Order.Ring`。同时，T22（诊断阈值模板）需要把 T21 提出的 positive scale / component ratio / closure cost 约束写成正式阈值。

## 为什么 review 结果是 PASS？

### 完成度验证
- 任务目标"审计 module-level candidate scan 输出，标出更深、更连续、更适合双曲检验的图"完全达成
- 审计表中的每一项数值都与原始扫描产物（`summary.json`、`stats.json`）交叉验证，全部准确
- 文档明确标注"provisional"，没有把审计结论写成最终 benchmark 定论

### 没有发现的问题
- 没有伪实现或 mock（纯文档任务，没有代码改动）
- 没有重跑扫描或修改 configs（遵守了 Forbidden scope）
- 没有破坏已有功能
- 所有改动都在 Allowed Files 范围内

### 值得肯定的亮点
- **数据驱动地反转了 T20 的排序**：从 `Order` > `Order.Ring` 变为 `Order.Ring` > `Order`，这个判断有充分的数据支撑（连通性和叶子比的差异）
- **发现了 raw score 的偏差问题**并记录为 R14 风险
- 审计维度选择合理，没有只看单一指标

### 两个小瑕疵（不影响通过）
1. 审计表的 "depth" 列指的是模块扫描深度（scan depth=3 或 4），不是图的结构深度（longest chain=10 或 11）。虽然两列同时出现可以帮助区分，但列名本身可能会让不熟悉上下文的读者困惑
2. 审计表只选了 9 个模块，没有解释为什么是这 9 个而不是其他（扫描总共覆盖了 112 个候选）。选得合理，但缺少显式的选择理由说明

这两个问题都是文档呈现的细节，不影响审计结论的正确性或任务完成度。
