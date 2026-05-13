# T22 解释文档：诊断阈值与报告模板

## 1. 这个任务在做什么（通俗版）

这个项目的核心问题是：**双曲几何模型（HGCN）在什么样的图结构上才有可能比普通模型（GCN）更好？**

之前我们已经做了很多诊断（T20、T21），发现大部分真实的 Lean/Mathlib 代码关系图都比较"浅"——层级链很短，大部分节点都是叶子，结构像一片片散落的树丛（forest）甚至星形（star），而不是那种深深嵌套的树。在这种浅层结构上，普通模型已经足够好了，双曲模型的潜在优势没有释放空间。

但这些诊断结论目前只是零散地写在各个报告里，没有一个统一的标准。如果后续有人来做实验，可能会：

- 只看某个分数就决定哪个图值得测，忽略了图的规模和结构风险。
- 把"太浅太碎"的图当成正式基准测试的候选。
- 把临时的经验判断写成论文里的"结论"。

**T22 的任务就是把这些经验判断固化成一套可复用的检查清单和报告模板**，让后续所有人用同一套标准来筛选候选图。

打个比方：之前我们凭经验说"这个图太浅了，不适合做双曲测试"。T22 把这句话变成了具体的标准——"如果最长链 ≤ 4，就标记为浅层风险"。

---

## 2. 任务实现详解

### 2.1 任务目标

T22 的目标是产出一份 `docs/diagnostics_protocol.md`，包含：

1. **经验阈值（heuristic flags）**：用具体数值定义什么算"浅"、什么算"星形"、什么算"太碎"。
2. **候选角色门控（candidate role gates）**：根据多个指标的综合判断，把候选图分成四类角色。
3. **报告模板**：后续诊断报告必须填写的统一格式。
4. **校准表**：用已有的候选图验证模板的分类是否与之前审计的结论一致。

所有阈值都必须明确标注为 `heuristic`（经验性的），不是理论证明，也不是最终定论。

### 2.2 任务流程

Worker 的执行步骤：

1. **阅读输入材料**：`diagnostics_summary.md`、`candidate_graph_audit.md`、现有 diagnostics report、`02_experiment_plan.md`。
2. **创建 `docs/diagnostics_protocol.md`**：新文件，包含完整的诊断协议。
3. **更新 `docs/06_eval_protocol.md`**：在结构诊断部分加入指向新协议的链接和五个关键阈值摘要。
4. **更新 `docs/04_task_board.md`**：在 Execution Note 中记录 T22 完成状态。
5. **更新 `docs/07_handoff.md`**：补充 T22 当前状态和下一步审查重点。
6. **更新 `docs/08_risks_and_open_questions.md`**：新增 R17（阈值失真风险）和 D09（review 后微调），更新 R14 和开放问题。

### 2.3 新增文件：`docs/diagnostics_protocol.md`

这是 T22 的核心产出。文档结构：

**Section 2 - Required Inputs（必填输入）**：
定义每次诊断必须收集的 7 个基础字段，以及从中派生的 2 个门控量：

```
component ratio = largest_relation_component / relation nodes
closure expansion ratio = ancestor_added_nodes / relation nodes
```

**Section 3 - Heuristic Flags（经验标志）**：

五个维度的风险检测：

| 标志 | 触发条件 | 含义 |
| --- | --- | --- |
| Shallow forest risk | 最长链 ≤ 4，或（最长链 ≤ 6 且叶子率 ≥ 0.70），或（component ratio < 0.50 且叶子率 ≥ 0.70） | 图太浅或太碎 |
| Star-forest risk | 最长链 ≤ 3 且叶子率 ≥ 0.75 且多父节点很少 | 星形结构，层级信号弱 |
| Positive-scale | 正边 < 100（太小）/ 100-249（可用作 probe）/ ≥ 250（可进候选池）/ ≥ 800（大规模） | 数据规模是否够做有意义的实验 |
| Continuity | component ratio < 0.50（碎片化）/ 0.50-0.64（有风险）/ ≥ 0.65（较好） | 图的连通性 |
| Closure expansion | ≤ 0.60（负担可接受）/ 0.60-0.80（偏重）/ > 0.80（太重） | 祖先闭合带来的额外节点负担 |

**Section 4 - Candidate Role Gates（候选角色门控）**：

四个角色，从高到低：

| 角色 | 要求 | 典型候选 |
| --- | --- | --- |
| Default follow-up candidate | 最长链 ≥ 8、正边 ≥ 250、component ratio ≥ 0.65、leaf ratio ≤ 0.60、closure ratio ≤ 0.60、非星形 | `Mathlib.Algebra.Order.Ring` |
| Depth stress-test | 最长链 ≥ 10、正边 ≥ 800，但连续性或叶子率不达标 | `Mathlib.Algebra.Order` |
| Controlled probe | 最长链 ≥ 8、正边 100-249、component ratio ≥ 0.40、leaf ratio ≤ 0.60 | `Ring.Subring`、`Field.Subfield` |
| Diagnostic-only | 星形风险、或最长链 ≤ 4、或正边 < 100、或叶子率 ≥ 0.75 且规模不够 | `Batteries.*` |

**Section 7 - Report Template（报告模板）**：
一个标准化的 markdown 模板，后续所有诊断报告都必须使用这个格式填写。

### 2.4 修改文件的变化

**`docs/06_eval_protocol.md`**：
- 在 Section 6（结构诊断指标）末尾插入了指向 `diagnostics_protocol.md` 的链接。
- 新增五个关键阈值的摘要（最长链、叶子率、正边数、component ratio、closure expansion ratio）。
- 更新治理状态记录 T22 worker draft 状态。

**`docs/04_task_board.md`**：
- 新增一条 Execution Note：T22 已产出草案，等待 review。

**`docs/07_handoff.md`**：
- 新增"当前状态补充"，说明 T22 处于 review 前状态。
- 新增第 33-34 条状态更新。
- 更新"下一步"部分，从"交 worker 执行"改为"交 reviewer 审查"。

**`docs/08_risks_and_open_questions.md`**：
- 更新 R14 描述，补充 T22 worker draft 已固化门控。
- 新增 R17：诊断阈值可能随后续实验失真的风险。
- 更新 Open Questions 1-2，从"T22 应该怎么写"改为"阈值是否需要重校准"。
- 新增 D09：review 后微调阈值的 deferred item。

### 2.5 对后续开发的意义

T22 完成了 Milestone 2（诊断与候选图选择）的最后一块拼图：

1. **T20**（已完成）：复查现有诊断，给出初步候选优先级。
2. **T21**（已完成）：对候选图做数据质量审计，发现 raw score 会偏向小型紧凑模块。
3. **T22**（当前）：把 T20-T21 的经验判断固化为可复用模板。

Milestone 2 完成后，项目进入 **Milestone 3：Grouped Retrieval Training Alignment**。T30 将阅读现有训练代码，定位 binary edge classification 与 grouped retrieval 之间的错配。T22 的诊断模板确保：

- 后续 T32/T33 训练实验只使用经过门控筛选的候选图（如 `Mathlib.Algebra.Order.Ring`）。
- 训练结果的报告格式与诊断模板一致，避免混乱。
- 如果后续 T40 provenance split 改变了图结构分布，模板可以重新校准。

---

## 3. 为什么给出 PASS 的 review 结果

### 3.1 任务完成度

任务包要求的核心产出全部到位：

| 要求 | 实现情况 |
| --- | --- |
| 可复用报告模板 | Section 7 提供了完整的 markdown 模板 |
| 经验阈值，标注为 heuristic | Section 3 所有阈值都明确标注为 heuristic |
| 覆盖 longest chain、leaf ratio、positive scale、component ratio、closure expansion | Sections 3.1-3.5 逐一覆盖 |
| 不写理论证明 | 全文反复强调"不是理论结论"、"不是最终 benchmark 排名" |
| 不修改实验代码 | 仅修改文档文件 |
| 不启动训练 | 未涉及任何训练代码或配置 |

### 3.2 校准一致性

我用 `candidate_graph_audit.md` 中的实际数值逐一验证了模板中五个候选角色的分类：

- `Mathlib.Algebra.Order.Ring`：通过了 default follow-up 的全部 6 个门控条件。
- `Mathlib.Algebra.Order`：符合 depth stress-test 的 3 个条件（链长 11 ≥ 10、正边 1387 ≥ 800、component ratio 0.489 < 0.65）。
- `Ring.Subring` 和 `Field.Subfield`：都符合 controlled probe 的条件，且 closure expansion ratio > 0.60 被正确标注为 "closure-heavy"。
- `Batteries.*`：正确归类为 diagnostic-only（链长 3-4 ≤ 4，正边 < 100）。

所有数值校验均通过，模板分类与 T21 审计结论完全一致。

### 3.3 发现的非阻塞问题

Review 中我发现了三个不影响完成但值得注意的问题：

1. **Shallow forest flag 条件 3 会误标深层但碎片化的图**：`Mathlib.Algebra.Order`（链长 11）会被标记为 "shallow forest risk"，因为它的 component ratio 0.489 < 0.50 且 leaf ratio 0.774 ≥ 0.70。问题在于这个图并不"浅"，而是"碎"。但 Section 4 的角色门控系统仍然正确把它分类为 depth stress-test，所以最终分类没有出错——只是 flag 的名字可能在语义上引起困惑。

2. **报告模板缺少 `multi-parent count` 行**：这个字段在 Required Inputs 和 star-forest 检测中都用到了，但模板表格里没有。后续填表时可能需要手写补上。

3. **`ancestor_added_nodes` 缺少内联定义**：公式里引用了这个字段，但定义在另一个文档里。在协议文档自身中补一句定义会更好。

这三个问题都不影响模板的正确性和可用性，所以判定为 PASS 而非 PASS_WITH_WARNINGS。它们可以在后续微调时处理（已记录为 D09 deferred item）。

### 3.4 治理合规

- 只修改了任务包允许的 5 个文件，没有越界。
- `06_eval_protocol.md` 中的阈值摘要与 `diagnostics_protocol.md` 完全一致。
- `07_handoff.md` 和 `04_task_board.md` 的状态更新相互匹配。
- `08_risks_and_open_questions.md` 新增的 R17 和 D09 是合理的跟踪项。
