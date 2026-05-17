# T40 通俗解释：冻结 Provenance Split 配置与输出位置

## 1. 这个任务在做什么？（通俗解释）

在这个项目中，我们研究的是形式化数学（用计算机验证的数学证明）中的"声明之间的层级关系图"。比如在 Lean/Mathlib 这个数学库中，`Ring` 继承自 `Semiring`，`Semiring` 继承自 `AddMonoid`——这些继承关系构成了一张图。

但问题是：这些"继承"关系其实有两种不同的来源：

1. **显式的（explicit）**：程序员在代码里明确写出来的 `extends` 关系。比如 `class Ring extends Semiring`。
2. **合成的（synthesized）**：Lean 编译器通过 typeclass 机制自动推断出来的 `instance_of` 关系。比如编译器发现某个类型满足 `Ring` 的条件，就自动建立一条 `instance_of` 边。

这两类边混在一起构成了完整的层级图。我们想知道：**如果只保留显式边、或只保留合成边，图的结构会怎样变化？这会不会影响双曲图神经网络的表现？**

T40 的任务就是：**冻结这三类图（显式边、合成边、混合边）的生成配置和输出规则**，写成正式的协议文档，让后续的 T41（结构诊断）和 T42（模型训练）可以直接使用，不需要重新定义什么是什么。

可以把它理解成：在正式做实验之前，先把实验材料的定义和来源写清楚、锁死，防止后续有人随意改定义来"凑"结果。

## 2. 任务的实现详解

### 2.1 任务目标

冻结以下内容：
- `origin_map`：哪种边算"显式"，哪种算"合成"
- 三类 split 的定义：`explicit_only`（只有 extends）、`synthesized_only`（只有 instance_of）、`hierarchy_mixed`（两者都有）
- 配置文件的格式和存放位置
- 输出目录的命名规则
- 每类图预期的节点数和边数

### 2.2 任务流程

1. **阅读现有代码和配置**：Worker 读取了 `split_relations_by_provenance.py` 这个已有的 split 脚本，确认它支持需要的配置格式。

2. **创建两份 frozen config**：
   - `provenance_split_field_subfield_t40.json`：针对 Field.Subfield 候选图的 split 配置
   - `provenance_split_order_ring_t40.json`：针对 Order.Ring 候选图的 split 配置

   两份配置结构完全相同：
   - `_t40_frozen: true` 标记（表示已审查，不可随意修改）
   - `source_graphs`：指向实际的源图目录
   - `origin_map`：`extends → explicit, instance_of → synthesized`
   - `splits`：三类 provenance split 的定义

3. **编写协议文档** `docs/provenance_split_protocol.md`，包含 7 个章节：
   - Section 1：Provenance 语义定义
   - Section 2：代码入口（split 脚本路径和用法）
   - Section 3：配置索引（包含 T40 frozen 和历史参考配置）
   - Section 4：输出目录约定（精确到每个 split 的目录名和预期文件列表）
   - Section 5：生成命令（直接可复制执行）
   - Section 6：T41/T42 使用指南（包含 T41 诊断配置建议和 T42 sweep 配置模板）
   - Section 7：完整性规则（6 条 integrity rules，防止后续随意修改 origin_map 或覆盖历史配置）

4. **更新治理文档**：
   - `docs/04_task_board.md`：更新当前任务状态为 T40，记录 T32/T33/T34 完成和 M3 review 结论
   - `docs/07_handoff.md`：更新接手说明，反映 Milestone 4 状态
   - `docs/08_risks_and_open_questions.md`：将 R11 从 Active 改为 Mitigated，新增 R26（split 实际生成未执行）

### 2.3 关键设计决策

- **origin_map 选择**：`extends → explicit, instance_of → synthesized` 是最自然的映射，与 Lean 编译模型一致。`uses` 边映射为 `unknown`，不出现在任何 split 中。

- **`hierarchy_mixed` 的特殊性**：当前两个候选图（Field.Subfield 和 Order.Ring）都没有 `uses` 边，所以 `hierarchy_mixed` = 完整源图。这意味着 T42 的 `hierarchy_mixed` 结果应该与 T32/T33 的结果完全一致，可以作为一个一致性校验点。

- **配置的不可变性**：通过 `_t40_frozen` 标记和 integrity rules（Section 7），确保后续任务不会随意修改 provenance 语义来追求有利的模型结果。这是项目"不为了赢而改规则"原则的具体体现。

### 2.4 对后续开发的意义

1. **T41 可以直接消费**：T41 只需运行两份 frozen config 生成 6 个 split 图目录，然后跑结构诊断。不需要重新定义 split 语义。

2. **T42 有配置模板**：协议文档 Section 6.2 给出了 T42 sweep 配置的 `target_relation_types`、`message_relation_types`、`hierarchy_relation_types` 模板，T42 worker 可以直接参照。

3. **回答核心问题的基础**：Milestone 4 的核心问题是"synthesized relation 是否削弱双曲优势"。T40 冻结了三类图的定义，使得 T41 可以先做结构诊断（图变浅了吗？），T42 再做模型对比（双曲模型在只保留显式边时表现更好吗？）。

4. **与已有结果的桥接**：`hierarchy_mixed` 与完整源图的等价性意味着 T42 的 `hierarchy_mixed` 结果应与 T32/T33 matched sweep 数值一致，提供了跨里程碑的一致性校验。

## 3. 为什么给出 PASS 的 review 结果？

### 3.1 任务目标完全达成

T40 的目标是"冻结三类 provenance 图的生成配置和输出位置"。Worker 创建了两份 frozen config、一份完整的协议文档（7 个章节覆盖语义、配置索引、输出约定、生成命令、使用指南、完整性规则），并更新了治理文档。所有目标都已达成。

### 3.2 没有伪实现或 hardcode

- 两份 config 指向真实的源图目录，包含正确的 JSON 结构。
- 协议文档中的预期边数（Field.Subfield: 116 extends + 36 instance_of = 152; Order.Ring: 180 extends + 120 instance_of = 300）与实际 `stats.json` 完全吻合，独立验证通过。
- Split 脚本是真实可运行的代码（182 行 Python），不是 stub。

### 3.3 遵守了所有约束

- 没有运行 seed sweep（正确，T40 只是配置冻结）
- 没有修改数据语义
- 没有覆盖历史配置（`relation_split_batteries_v1.json` 未被触碰）
- 没有修改任何源代码
- 只修改了 Allowed Files 范围内的文件

### 3.4 文档诚实

- 协议文档标记自身为"T40 worker draft, pending adversarial review"
- 明确记录了 split 实际生成尚未执行（R26）
- 明确记录了 `edges.csv` 仍缺少一等 `edge_origin` 列（R11 residual）
- 没有把配置冻结写成"已完成 split 生成"

### 3.5 没有过度工程

协议文档的篇幅与复杂度匹配任务需要：T41/T42 确实需要明确的语义定义、配置索引、输出约定和使用指南。没有添加不必要的内容。

### 3.6 不影响已有功能

没有任何源代码被修改，没有覆盖已有配置，没有改变已有 artifact。T40 是一个纯增量任务。

综上所述，T40 的工作质量满足 adversarial review 标准，没有 blocking issue，判定为 PASS。
