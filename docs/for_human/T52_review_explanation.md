# T52 Review 解释

## 1. 这个任务在做什么（通俗解释）

### 背景

这个项目研究的是：在 Lean 形式化数学库（比如 Mathlib）中，声明（declaration）之间形成的层级关系图，能否用双曲图神经网络（HGCN）比普通图神经网络（GCN）更好地做"祖先检索"——即给定一个数学概念，找出它的"父概念"、"祖父概念"等层级祖先。

经过一系列实验（T40-T43），项目得到了一个关键发现：**HGCN 只在 `explicit_only`（只包含显式 extends 边）的图上优于 GCN，而在混合图上 GCN 仍然领先**。这个发现叫做"provenance-conditional"结论。

### T52 在做什么

T51 已经选定了一个叫 **ancestor explanation** 的 demo 方向——把上面的 provenance-conditional 发现变成一个用户可以直接运行的工具。但 T51 只选了方向，没有写具体的实现规格。

**T52 的任务就是：把 ancestor explanation 的实现要求写成一份详细的"任务包"文档**，让下一个 worker 可以直接照着做，而不需要再做方向选择或规格讨论。

打个比方：T51 决定了"我们要造一把椅子"，T52 的任务就是画一张详细的椅子设计图纸（但不动手造），下一个任务 T52a 才是照图纸造椅子。

### 交付物

T52 产出了一份重写的文档 `T52a_ancestor_explanation_demo.md`，包含：

- CLI 命令行参数设计（声明名、候选图、provenance 模式、模型类型等 7 个参数）
- 两种运行模式：单查询模式 和 provenance 对比模式（对比 explicit_only 和 hierarchy_mixed 的检索质量差异）
- artifact 依赖表（从哪个目录加载图数据、从哪个目录加载训练好的节点嵌入）
- 一个关键实现注意事项：`node_embeddings.npy` 文件的行顺序必须和图的节点顺序对齐，否则检索结果全部错误
- 11 条禁止事项（不重训模型、不引入新依赖、不修改已有代码等）

## 2. 实现详细解释

### 任务目标

T52 的目标是把 T51 选定的 ancestor explanation MVP 的实现边界写成可以直接派发给后续 worker 的最小 demo 实现任务包。**T52 本身不实现任何代码，只写文档**。

### 任务流程

1. Worker 读取 T52 任务包，了解允许和禁止的范围
2. Worker 读取 T51 的 `proof_side_mvp.md`（MVP 规格）、`paper_outline.md`（论文叙事需要）、T42 的实验报告（artifact 路径和结果）
3. Worker 重写 `T52a_ancestor_explanation_demo.md`，从旧的不完整草稿升级为完整的 worker 任务包
4. Worker 同步更新 4 份治理文档

### 文件变化

#### `docs/tasks/M5_paper/T52a_ancestor_explanation_demo.md`（核心产物，从 68 行扩展到 158 行）

这是最重要的变化。旧版本是一个不完整的草稿，新版本是一个完整的、可直接执行的 worker 任务包，新增内容包括：

- **CLI 参数精确规格**：7 个参数的完整定义和默认值
- **两种运行模式的详细行为描述**：single-query mode 的 5 步执行流程、comparison mode 的 4 步执行流程
- **Artifact 依赖表**：6 个 T41/T42 reviewed artifact 的路径模式
- **Critical implementation note**：node ordering 对齐的详细说明
- **Demo report 要求**：至少 3 个 usage example、至少 2 个 declaration 的输出
- **Acceptance criteria verification**：6 条来自 T51 的验收标准

#### `docs/04_task_board.md`（+3 行）

添加 T52 worker 执行说明条目（一条 Execution Note）。

#### `docs/05_decision_log.md`（+10 行）

添加 D032 决策记录：T52 的 5 个设计决策（artifact loading 策略、代码入口选择、node ordering 对齐、comparison mode 为硬边界、adversarial review）。

#### `docs/07_handoff.md`（+7 行）

添加第 76 条 T52 worker 完成说明，更新"下一步"从 T52 切换到 T52a。

#### `docs/08_risks_and_open_questions.md`（+3 行）

新增 R32（node ordering alignment 风险，High Active）。

### 对后续开发的意义

T52 把 demo 的实现边界写得非常窄、非常实：

1. **T52a worker 只需要做一件事**：写一个 CLI 脚本和一个 demo 报告，不碰任何已有代码
2. **Artifact 依赖明确**：只依赖 T42 已 reviewed 的产物，不需要重训模型
3. **验收标准明确**：6 条 acceptance criteria 直接来自 T51
4. **风险已预登记**：R32 提前警告了 node ordering 对齐问题，并写入了 sanity check 要求
5. **Paper bridge 清晰**：demo 输出要映射到论文的 Table 4、Fig 3、Fig 4

这使得 T52a 可以在非常窄的 scope 内完成，避免了 scope creep。

## 3. 为什么给出 PASS 的 review 结果

### 检查要点

| 检查项 | 结果 |
|--------|------|
| 是否完成任务目标 | 是。T52a 已从草稿重写为完整的下游 worker 任务包 |
| 是否在 Allowed Files 范围内 | 是。只修改了 5 个文件，全部在 T52 Allowed Files 中 |
| 是否遵守 Forbidden Scope | 是。未实现 demo、未新增实验、未修改代码、未引入新依赖 |
| 是否有 mock/stub/hardcode | 不适用（纯文档任务） |
| 验证是否充分 | 是。3 条验证命令全部通过 |
| 是否有破坏性变更 | 不适用（未修改代码） |
| 文档是否把计划写成事实 | 否。T52 在 task board 中仍标记为 `[ ]`，handoff 明确写"等待 reviewer 只读审查" |
| 风险是否已登记 | 是。R32 已新增为 High Active |

### 非阻塞问题

发现了 3 个非阻塞问题，均不影响任务完成或后续工作：

1. **T52a reviewer type 升级为 adversarial**：这是合理的（涉及 artifact 对齐），但 T52 自身仍是 normal。一致性可在 Captain 更新时处理。
2. **Artifact path pattern 是硬编码假设**：建议 T52a worker 实现时加入路径存在性检查。可在 T52a 阶段处理。
3. **Declaration name 示例格式可能变化**：T52a worker 应从实际 artifact 获取可用名称。可在 T52a 阶段处理。

### 结论

T52 是一个执行得非常干净的文档任务：worker 精确地完成了"把 MVP 方向写成可执行任务包"的目标，没有越界，没有把计划写成事实，没有遗漏关键约束。3 个非阻塞问题都是给 T52a 实现阶段的建议，不需要 T52 返修。

**Verdict: PASS**
