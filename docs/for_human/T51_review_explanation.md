# T51 Review Explanation (面向人类读者的通俗解释)

## 1. T51 这个任务在做什么？

T51 是一个**纯文档决策任务**：从三个候选的 proof-side utility MVP 方向中选出一个，作为论文从"纯实验数据"走向"实际可用工具"的桥梁。

项目到 T50 为止已经建立了一条完整的证据链：从数据管线、评测协议、结构诊断到 provenance-conditional finding（HGCN 只在 explicit_only 层级图上优于 GCN）。但论文如果只展示数字表格，读者（尤其是 ITP 和 CPP 的 proof assistant 社区）会问一个关键问题：

> 这些图表示质量差异，对实际做形式化证明的人有什么意义？

T51 的任务就是回答这个问题——选出一个最小可行的 downstream utility，让图表示质量差异变成可体验的工具行为。

具体来说，三个候选方向是：

1. **Ancestor Explanation（祖先解释）**：给定一个 Lean 声明，用训练好的模型检索其真祖先，并附带 provenance 标注和层级路径信息。
2. **Declaration Recommendation（声明推荐）**：给定一个部分构建的 import/extends 链，推荐下一个相关声明。
3. **Premise Retrieval Demo（前提检索演示）**：用学到的 embedding 辅助 LeanDojo 风格的前提检索。

Worker 最终选择了 **Ancestor Explanation**。

## 2. T51 的实现详解

### 2.1 任务目标

T51 的目标不是写代码或跑实验，而是做出一个**架构决策**：

- 比较三个候选 MVP 方向的优劣
- 选出一个并说明理由
- 明确 MVP 的输入、输出、验收标准、失败标准和不做事项
- 为后续 T52（最小 demo 任务包）提供可直接执行的规格

### 2.2 任务流程

Worker 按照任务包的指示，执行了以下步骤：

1. **阅读输入文档**：读取了 `docs/paper_outline.md` 的 proof-side bridge 部分（Section 9），以及治理文档中 R31 风险的当前状态。

2. **新增 `docs/proof_side_mvp.md`**（约 200 行）：
   - **Section 1（Task Context）**：简述 T50 已建立的论文叙事和 proof-side bridge 缺口。
   - **Section 2（Candidate Comparison）**：逐一分析三个候选方向，包括与论文贡献（C1–C5）的映射表、复杂度评估和关键风险。最后给出综合比较表。
   - **Section 3（Selection: Ancestor Explanation）**：
     - 3.1 给出选择理由（4 条：直接映射 C2/C4、零新依赖、venue fit、风险可控）。
     - 3.2 正面回应 R31——论证 ancestor explanation 不是简单的"列出祖先"，而是一个 provenance-aware quality comparison tool，满足 CPP tool demo 的标准。
   - **Section 4（MVP Specification）**：
     - 4.1 输入：declaration name、candidate graph、provenance mode、model type
     - 4.2 输出：ranked ancestor list、ground truth comparison、retrieval metrics、hop-depth breakdown、provenance comparison
     - 4.3 验收标准（6 条）：功能性、provenance 差异可见、无新训练、无新依赖、CLI 入口、paper bridge 文档
     - 4.4 失败标准（3 条）：provenance 差异不可复现、scope 膨胀、输出不可解释
     - 4.5 不做事项（6 条）：不做端到端证明、不提升为 benchmark task 等
   - **Section 5（Paper Bridge Narrative）**：说明 MVP 如何服务于论文中的 Table 4-5 和 Fig 3-4，以及它在论文 Conclusion 和 Discussion 中的位置。
   - **Section 6（Open Items for T52）**：列出 T52 需要解决的 5 个开放问题（代码入口、model loading、输出格式、任务包设计、scope 约束）。

3. **更新治理文档**：
   - `docs/04_task_board.md`：更新时间戳，标记 T42/T43/T50 完成，将当前任务切换到 T51，新增执行说明。
   - `docs/05_decision_log.md`：新增 D031（ancestor explanation MVP 选择），状态为 Pending Review。
   - `docs/07_handoff.md`：更新时间戳，更新当前任务为 T51，新增 item 75 和下一步说明。
   - `docs/08_risks_and_open_questions.md`：将 R31 从 Active 更新为 Mitigated（附 T51 正面回应）；回答 Open Question 6。

4. **运行验证命令**：两条 `rg` 命令均确认所有关键词存在于对应文件中。

### 2.3 关键设计决策

**为什么选 Ancestor Explanation 而不是 Declaration Recommendation 或 Premise Retrieval？**

| 方向 | 不选的理由 |
| --- | --- |
| Declaration Recommendation | 需要定义"部分链→推荐"的新任务规格，超出当前 pipeline 已有能力，T52 scope 膨胀风险中等 |
| Premise Retrieval | 需要引入 LeanDojo 作为新依赖（违反 forbidden scope），需要桥接 declaration graph 与 proof state 数据，与论文中心叙事（provenance-conditional finding）距离最远 |

Ancestor Explanation 的核心优势：

1. **直接服务于论文中心 claim**——同一个 declaration 在 `explicit_only` vs `hierarchy_mixed` 上的 retrieval 质量差异，就是把 provenance-conditional finding 从数字变成体验。
2. **零新依赖、零新训练**——T32/T33/T42 的 artifact 直接可用。
3. **与 ITP/CPP venue fit 高度对齐**——ITP 读者关心"hierarchy navigation 能否帮助理解 formal-math"；CPP 读者看重 tool artifact。

**如何回应 R31（ancestor explanation 可能过于轻量）？**

Worker 的论证是：ancestor explanation 不是"列出祖先"，而是 **provenance-aware quality comparison tool**。它的核心展示不是返回一个排序列表，而是让用户看到：
- 包含 synthesized 边后，检索质量发生了什么变化
- 更深层祖先在不同几何下的检索难度差异
- 哪些 ancestor 来自显式继承（extends），哪些来自编译器合成（instance_of）

这满足 CPP artifact evaluation 的"functional and solves a real problem"标准。

### 2.4 对后续开发的意义

T51 的产出 `docs/proof_side_mvp.md` 是 T52 的**直接输入规格**：

- **T52** 将基于 Section 4 的 MVP specification 编写最小 demo 任务包，包括 CLI 入口、model artifact loading 方式、provenance comparison mode 输出格式。
- MVP 的验收标准（6 条）和失败标准（3 条）为 T52 提供了明确的 done/not-done 判断依据。
- Section 6 的 Open Items 列出了 T52 需要解决的 5 个具体设计问题。
- 论文大纲中的 proof-side bridge 部分（Section 9）和 Section 5 的 Paper Bridge Narrative 将在 T53 里程碑审查时一起评估。

## 3. 为什么给出 PASS 的 review 结果？

### 任务完成度：完全满足

T51 任务包要求的所有部分都在 `docs/proof_side_mvp.md` 中完整呈现：

- 三个候选方向逐一比较 ✓
- 选择结论和理由 ✓
- R31 正面回应 ✓
- MVP 规格（输入/输出/验收/失败/不做）✓
- Paper bridge 叙事 ✓

### 口径正确性：完全满足

- 文档正确地将 MVP 定位为 paper bridge，而非独立研究贡献。
- 选择 ancestor explanation 的理由直接映射到论文贡献（C2/C4），而非发明新的贡献维度。
- 没有改写 T50 已确认的 provenance-conditional 口径。
- R28/R29/R31 的精度边界在文档和治理更新中被正确保留。

### 无伪实现

整个任务只产出文档，没有代码改动，没有 mock/stub/hardcode。

### Worker 纪律：优秀

与 T50 和更早的任务相比，T51 worker 有一个显著改进：**完全没有修改 Allowed Files 之外的文件**。之前的 T50 worker 修改了 6 个越界文件（虽然是良性的治理更新），T51 worker 则完全遵守了纪律。这是一个正面趋势。

### 没有 Blocking 问题

唯一需要 Captain 后续处理的是 D031 的状态更新（从 "Pending Review" 改为 "Accepted"），这是标准流程。

### 总结

- **PASS**：因为任务目标完全达成，所有内容口径正确，无 blocking 问题，Worker 纪律优秀。
