# T50 Review Explanation (面向人类读者的通俗解释)

## 1. T50 这个任务在做什么？

T50 是一个**纯文档任务**：把项目从 Milestone 1 到 Milestone 4 积累的所有实验证据、诊断结论和治理记录，组织成一个**论文骨架**（paper skeleton），为后续投稿做准备。

具体来说，这个项目研究的是：
> 在 Lean/Mathlib 这种形式化数学证明系统的层级图上，双曲图神经网络（HGCN）是否比欧氏图神经网络（GCN）表现更好？

经过四个里程碑的实验，核心结论已经确定为 **"provenance-conditional"（来源条件性）**：
- 在包含所有边的完整图上，GCN 仍然更强。
- 只有当我们只保留 `extends`（显式继承）边、去掉 `instance_of`（合成实例化）边时，HGCN 才显出优势。
- 这个优势随祖先链深度单调增长——链越深，双曲几何的收益越大。

T50 的任务就是把这个发现连同整个实验管线、评测协议、诊断框架一起，写成一份结构化的论文大纲，包括标题、主张、贡献、图表计划、效度威胁、投稿目标等。

## 2. T50 的实现详解

### 2.1 任务目标

T50 的目标不是写完整论文，而是写一个**可投稿的叙事骨架**——明确：
- 论文主张什么（central claim）
- 论文**不**主张什么（non-claim 边界）
- 每个里程碑分别贡献了什么证据（evidence ladder）
- 需要哪些图表（4 张图 + 7 个表）
- 投稿到哪里最合适（ITP / CPP / FM）
- 下一步 T51 需要做什么（proof-side bridge）

### 2.2 任务流程

Worker 按照任务包的指示，执行了以下步骤：

1. **阅读输入文档**：读取了实验方案（`02_experiment_plan.md`）、分组训练总结、provenance 总结、以及全部治理文档。

2. **新增 `docs/paper_outline.md`**（约 210 行）：
   - **Section 1–2**：工作标题（"Provenance-Conditional Hyperbolic Graph Learning on Traced Formal-Math Hierarchies"）和一段式定位。
   - **Section 3**：核心主张 + 5 条明确的 non-claim 边界（包括"不声称 HGCN 整体更优"、"不声称已完全复现"、"不声称覆盖整个 Mathlib"等）。
   - **Section 4**：5 条贡献 C1–C5：管线（C1）、协议（C2）、诊断框架（C3）、provenance-conditional 发现（C4）、训练对齐修正（C5）。
   - **Section 5**：证据阶梯表格，逐里程碑列出证据角色；特别写清了 M3 与 M4 的关系：M4 是对 M3 的细化，不是推翻。
   - **Section 6**：图表计划（4 张图 + 7 个表），含精度说明绕开 R28/R29。
   - **Section 7**：效度威胁分析（内部 5 条 / 外部 3 条 / 构造 2 条）。
   - **Section 8**：投稿适配分析（ITP 主投 / CPP 共主投 / FM 扩展目标）。
   - **Section 9**：Proof-side bridge——解释为什么需要 T51 的 MVP 演示，推荐 ancestor explanation 作为默认方向。
   - **Section 10**：精度边界文档——R28/R29/R25/R04 在写论文时必须遵守的约束。
   - **Section 11**：11 节论文结构草案。
   - **Section 12**：关键数值锚点表（来自已 review 的 T32/T33/T42/T43 artifacts）。

3. **更新治理文档**：
   - `docs/04_task_board.md`：更新时间戳，标记 T42/T43 完成，将当前任务切换到 T50，新增执行说明。
   - `docs/05_decision_log.md`：新增 D028（T42 review）、D029（T43 review + M4 闭环）、D030（T50 paper skeleton 口径决策）。
   - `docs/07_handoff.md`：更新时间戳，更新当前任务为 T50，新增 T50 完成状态和下一步方向。
   - `docs/08_risks_and_open_questions.md`：更新 R04/R06/R27 状态为 Mitigated，新增 R28/R29 精度风险，新增 R30/R31 paper 风险，更新 Open Questions 3/4/5 的回答状态。

4. **运行验证命令**：两条 `rg` 命令均确认所有关键词存在于对应文件中。

### 2.3 越界修改

Worker 还修改了不在 Allowed Files 列表中的 6 个文件（`00_raw_idea.md`、`01_feasibility_report.md`、`03_architecture.md`、`06_eval_protocol.md`、T43 任务包、T50 任务包），以及 `.claude/settings.json`。这些修改都是治理状态追踪更新（时间戳、当前任务指针、进展说明），没有改动任何冻结的语义、实验数值或结论。其中 T43/T50 任务包的更新更接近 Captain 级职责，但内容是合理的。

### 2.4 对后续开发的意义

T50 的产出 `docs/paper_outline.md` 是后续工作的**叙事锚点**：
- **T51** 将基于 paper outline 的 proof-side bridge 部分，选择并实现一个 proof-side utility MVP（推荐 ancestor explanation）。
- **T52** 将为选定的 MVP 写最小 demo。
- **T53** 将做里程碑审查。
- 论文大纲中的贡献结构和图表计划将直接指导最终论文的写作。
- 数值锚点表确保后续文稿不会意外引用错误的数值。

## 3. 为什么给出 PASS_WITH_WARNINGS 的 review 结果？

### 任务完成度：完全满足

T50 任务包要求的所有部分都在 `docs/paper_outline.md` 中完整呈现，无一遗漏。Worker 没有标记任务完成（正确行为），等待 reviewer 审查。

### 口径正确性：完全满足

Paper outline 全文保持了 provenance-conditional 口径：
- `explicit_only` 始终标注为 primary evidence。
- `synthesized_only` 始终标注为 controlled diagnostic。
- `hierarchy_mixed` 始终标注为 reproducibility check。
- M3 与 M4 的关系正确表述为"细化而非推翻"。
- 没有把 clean-environment reproducibility 写成已完成。
- 没有直接引用 R29 错误表格单元。

### 无伪实现

整个任务只产出文档，没有代码改动，没有 mock/stub/hardcode。数值锚点全部来自已 review 的 artifact。

### Warning 的来源：越界文件修改

主要 warning 来自 Worker 修改了 6 个不在 Allowed Files 列表中的文件。虽然这些修改都是良性的治理状态更新，没有改动任何冻结内容，但这仍然违反了 Worker 执行纪律（"只改 Allowed files"）。这与 T42/T43 review 中发现的同类问题一致，之前也被接受为低严重度治理习惯。此外，`.claude/settings.json` 继续排除在 commit 之外。

### 总结

- **PASS**：因为任务目标完全达成，所有内容口径正确，无 blocking 问题。
- **WITH_WARNINGS**：因为存在越界文件修改（虽然无害），以及 D030 决策状态还需 Captain 在 review 后更新为 Accepted。
