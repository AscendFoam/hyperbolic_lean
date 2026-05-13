# T30 解释文档：训练/评测错配审计

## 1. 这个任务在做什么（通俗版）

这个项目要训练图神经网络来预测 Lean/Mathlib 代码的层级关系。我们有两种"打分"方式：

- **训练时的打分**：模型看着一条边（比如"`Nat` extends `Eq`"），判断"这条边是不是真的存在"。就像做判断题，每道题只问一条边。
- **评测时的打分**：给模型一个查询（比如"`Nat` 通过 `extends` 关系有哪些祖先？"），让它在所有候选里排序。就像做排序题，要看哪些祖先排在前面。

问题在于：**我们训练模型做的是判断题，但考试考的是排序题。**

之前 T12-T14 已经修好了"考试怎么考"的部分（grouped retrieval 评测协议），但"平时怎么练"的部分还是老的判断题模式。T30 的任务就是**仔细读一遍训练代码，把训练和考试之间所有不一致的地方都找出来**，给下一步修复定好范围。

打个比方：我们已知考的是排序题，但还没具体看过课本的练习题是不是也是排序题。T30 就是翻开课本审计一遍。

---

## 2. 任务实现详解

### 2.1 任务目标

T30 的目标是产出一份 `docs/training_alignment_audit.md`，列出：

1. 当前训练用的是什么 loss（损失函数）
2. 训练的基本单位是什么（边 vs 查询）
3. 负采样（训练时的错误选项）是怎么组织的
4. 模型选择（checkpoint）用的是哪个指标
5. 报告层面是否还有旧指标的残留
6. 下一步 T31 的最小改造范围

### 2.2 任务流程

Worker 的执行步骤：

1. **阅读训练代码**：逐个读 `relation_tasks.py`、`relation_baseline_common.py`、`run_relation_gcn_baseline.py`、`run_relation_hyperbolic_baseline.py`。
2. **创建 `docs/training_alignment_audit.md`**：新文件，包含完整的错配审计。
3. **更新治理文档**：`04_task_board.md`、`07_handoff.md`、`08_risks_and_open_questions.md`。

### 2.3 发现的六个错配点

审计发现了六个层次的训练/评测不一致：

**M1. Loss 错配**：训练用 `BCEWithLogitsLoss`（逐边二分类），但评测看的是 grouped ranking（同一查询下的排序质量）。

- 训练问的是："`Nat` extends `Eq`"这条边存不存在？
- 评测问的是：在 `Nat` 的所有 extends 祖先里，`Eq` 排第几？

模型只学会了"这条边像不像真的"，没学到"同一查询下的候选该怎么排"。

**M2. 单位错配**：训练按"边"组织，评测按"查询 `(src, relation)`"组织。

- 有 5 个正例边的查询，在训练中权重是只有 1 个正例边的查询的 5 倍。
- 但评测时每个查询权重相同。这导致训练偏向正例多的查询。

**M3. Split 错配（最重要的发现）**：数据切分是按边切的，不是按查询切的。

这是本轮审计最重要的发现。举个例子：

假设 `Nat` 通过 `extends` 有 3 个祖先：`Eq`、`Ord`、`ToString`。这 3 条正例边：
- `(Nat, Eq, extends)` → 可能被分到 train
- `(Nat, Ord, extends)` → 可能被分到 val
- `(Nat, ToString, extends)` → 可能被分到 test

问题在于：
- val 只知道 `(Nat, Ord, extends)` 是正例，不知道 `Eq` 和 `ToString` 也是。
- `Eq` 和 `ToString` 仍然在候选池里，但会被当成"不是祖先"。
- 于是评测以为模型排错了，其实是 split 把答案拆碎了。

**这意味着现有的所有 grouped eval 结果都带有未知的噪声。**

**M4. 负采样错配**：训练时每条边只看一小批随机采样的负例，但评测时要在整个候选池上排序。

- 训练就像"从 100 个人里挑出 5 个不是你朋友的人"。
- 评测就像"从 1000 个人里按亲疏关系排序"。
- 模型在训练时没见过全池排序的场景。

**M5. 模型选择错配**：选最优 checkpoint 用的是 val binary AP（二分类指标），不是 grouped MAP/nDCG。

- 相当于"平时练习的成绩用判断题打分，但最终成绩按排序题算"。
- 训练过程不会为了让排序指标更好而去调整模型。

**M6. 报告残留**：`result_summary.json` 还保留着旧的 `ranking_test_mrr`（单正例 MRR），跟 grouped 指标并列，可能造成阅读混淆。

### 2.4 新增文件：`docs/training_alignment_audit.md`

文档结构：

| Section | 内容 |
| --- | --- |
| Section 1: Scope | 审计范围，只读不改代码 |
| Section 2: Current Code Path | 当前代码路径的完整梳理 |
| Section 3: What Is Already Aligned | 已经对齐的部分（避免过度渲染问题） |
| Section 4: Confirmed Mismatch Points | M1-M6 六个错配点 |
| Section 5: Minimal T31 Change Boundary | T31 的最小改造范围建议 |
| Section 6: Recommended Priority Order | P0-P3 优先级排序 |
| Section 7: Bottom Line | 总结 |

### 2.5 修改文件的变化

**`docs/04_task_board.md`**：
- 新增一条 Execution Note：T30 已产出草案，等待 review。

**`docs/07_handoff.md`**：
- 新增"当前状态补充"，说明 T30 处于 review 前状态。
- 新增第 38-39 条状态更新，重点指出 split 错配发现。
- 更新"下一步"部分，从"交 worker 执行"改为"交 reviewer 审查"，并给出三个审查重点。

**`docs/08_risks_and_open_questions.md`**：
- 更新 R07 描述，补充 T30 已确认的具体错配事实。
- 新增 R19（High）：query-level split 不完整导致的 grouped eval 可靠性风险。
- 更新 Open Question 4：改为"T31 是否能只做 query-grouped loss，而把 query-level split 修复推后"。
- 新增 D10：追踪 split 修复是否需要单独建任务。

### 2.6 对后续开发的意义

T30 是 Milestone 3（训练目标对齐）的起点。它为后续任务划定了清晰的边界：

1. **T31（query-grouped loss）**：T30 明确了最小改造范围——只加 grouped training 分支，不改旧任务。但 T30 也发现了一个比 loss 更前置的问题：split 不完整。

2. **Split 修复的优先级**：T30 把 split 修复排在 P0（最高优先级），高于 loss 修复（P1）。如果不先修 split，换了 grouped loss 之后 grouped eval 仍然不可靠。

3. **T32/T33（seed sweep）的可靠性**：T30 意味着在 split 修复之前，现有的 grouped eval 结果都有潜在的噪声。这为解读 T32/T33 的结果提供了必要的上下文。

4. **论文叙事**：如果最终论文要写"我们做了训练/评测对齐"，T30 的审计结构可以直接支撑方法论章节中的"我们识别了六个层次的对齐问题并系统修复"。

---

## 3. 为什么给出 PASS 的 review 结果

### 3.1 任务完成度

任务包要求的核心产出全部到位：

| 要求 | 实现情况 |
| --- | --- |
| 列出当前 loss | M1 确认为 `BCEWithLogitsLoss`，附带代码行号 |
| 列出 batch/query 结构 | M2 明确单位错配：训练按边、评测按查询 |
| 列出 negative sampling | M4 确认局部负采样 vs 全候选池 |
| 列出 eval 入口 | Section 2 梳理完整代码路径 |
| 列出最小改造点 | Section 5 给出 T31 五点边界，Section 6 给出 P0-P3 优先级 |

### 3.2 代码声明全部验证通过

审计文档中的七个具体代码声明（函数名、行号、行为）全部经独立核实确认正确：

- `BCEWithLogitsLoss`：`run_relation_gcn_baseline.py:147`、`run_relation_hyperbolic_baseline.py:250` ✓
- `stratified_split_relation_examples(...)` 只按 `relation_type` 分组：`relation_tasks.py:31-56` ✓
- 负采样按正例边组织：`relation_tasks.py:219-302` ✓
- grouped query 聚合：`relation_tasks.py:380-410` ✓
- checkpoint 选 `val_average_precision`：两个 runner 均确认 ✓
- `result_summary.json` 同时包含新旧字段：均确认 ✓

### 3.3 M3 的发现增加了超出预期的价值

任务描述预期的主要工作是"定位 BCE 与 grouped retrieval 的错配"，但 Worker 发现了一个更深层的问题：`stratified_split_relation_examples(...)` 按边切分而不是按查询切分。这意味着：

1. 不仅训练/评测不一致，评测本身的基础数据（split）就有结构性缺陷。
2. 即使换了 grouped loss，只要 split 不修，结果仍然不可靠。
3. 这影响所有现有的 grouped eval 结果的可信度。

这个发现被恰当地标为 R19（High severity），并推到 P0 优先级。审计没有越界去修代码，只是清楚地指出了问题和优先级。

### 3.4 适当的克制

审计文档在三个方面保持了恰当的克制：

1. **Section 3 "What Is Already Aligned"**：先说清楚已经做对的部分，避免过度渲染问题。
2. **不量化影响**：虽然指出了 split 会让查询被拆碎，但没有估算"有多少查询受影响"，因为这需要运行代码，超出只读审计范围。
3. **不给性能结论**：文档明确声明"不给出未验证性能结论"，只做结构审计。

### 3.5 发现的非阻塞问题

Review 中我发现了三个不影响完成但值得注意的细节问题：

1. **标题层级格式**：Section 4 下的 M1-M6 使用 `##` 标题，与 Section 4 同级，应该用 `###` 嵌套。这是纯格式问题。

2. **M6 标题混语**："historical single-positive field still留在 summary surface" 中英文混杂，与 M1-M5 的纯英文标题风格不一致。

3. **M3 缺少粗略影响估计**：虽然不能运行实验，但可以基于代码结构分析说"任何有 ≥2 条正例边的查询都有非零概率被拆碎"之类的定性估计，来加强 P0 推荐的说服力。

这三个问题都不影响审计结论的正确性或完整性，所以判定为 PASS。
