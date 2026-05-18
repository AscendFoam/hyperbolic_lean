# T43 通俗解释：Provenance Split 总结与 Milestone 4 收口

## 1. 这个任务在做什么？（通俗解释）

整个 Milestone 4 的故事线是这样的：

- **T40** 定了规矩：把 Lean 编译器里的层级边分成三类——手写的 `extends`（explicit）、自动生成的 `instance_of`（synthesized）、以及两者混合的 mixed。
- **T41** 给三类图做了"体检"：发现 synthesized 边全是最长链 = 1 的平坦星状森林，所有层级深度都来自 explicit 边。
- **T42** 给三类图做了"药物试验"：在 explicit_only 上，双曲模型 HGCN 首次赢了欧氏模型 GCN；在 synthesized_only 上，GCN 反而赢了；在混合图上，结论和 Milestone 3 一致（GCN 领先）。

**T43 就是"写结案报告"**——把 T41 的结构体检和 T42 的药物试验结果汇总成一个统一的、精确的、不过度外推的最终结论。

T43 不跑任何新实验，不改任何已有数据。它做的事情纯粹是文字层面的收口：把散落在多份报告中的发现，整合成一份可以被后续论文和 Milestone 5 直接引用的 provenance-conditional 结论。

## 2. 任务的实现详解

### 2.1 任务目标

T43 要求完成以下六件事：

1. 把 `explicit_only` 明确写成 primary evidence（主证据），HGCN 在该 split 上稳定领先
2. 把 `synthesized_only` 写成 controlled diagnostic（受控诊断），不是主模型对比证据
3. 把 `hierarchy_mixed` 写成 reproducibility check（可复现性校验），不是新的图族发现
4. 明确写出 synthesized 边的作用是结构性稀释，不贡献层级深度
5. 把项目结论从"GCN overall ahead"精化为 provenance-conditional 的条件性结论
6. 满足精度约束：注明 4/5 seeds 的 hop bucket 均值、登记 aggregate/per-seed 口径差异

### 2.2 任务流程

#### 第一步：产出主报告

Worker 创建了 `docs/experiment_reports/provenance_summary.md`，包含 10 个章节：

1. **Executive Summary** — 一句话概括核心发现和精化后的结论
2. **Evidence Sources** — T40/T41/T42 三份已通过 review 的证据来源
3. **Structural Evidence (T41)** — synthesized 边平坦、explicit 边承载深度、混合稀释结构
4. **Primary Evidence: explicit_only (T42)** — HGCN 在两组候选图上全面领先，含 hop bucket 分析
5. **Controlled Diagnostic: synthesized_only (T42)** — GCN 在平坦结构上优于 HGCN，含精度说明
6. **Reproducibility Check: hierarchy_mixed (T42)** — 与 T32/T33 完全一致的复现验证
7. **Synthesis: The Provenance-Conditional Conclusion** — 汇总表和精化结论的正式陈述
8. **Implications** — 五条关键推论
9. **Precision Notes and Follow-ups** — 4/5 seeds、口径差异、scope 局限性
10. **Source Documents** — 所有引用的源文件路径

#### 第二步：更新治理文档

- `docs/05_decision_log.md`：新增 D028（T42 review 通过并切换到 T43）和 D029（T43 完成，Milestone 4 叙事收口）
- `docs/04_task_board.md`：标记 T42 完成、切换到 T43、更新 Worker Package Summary 和 Execution Notes
- `docs/07_handoff.md`：新增 items 70-71、重写 Section 8 为 T43 完成后的下一步指引
- `docs/08_risks_and_open_questions.md`：R04 → Mitigated（provenance-conditional）、R06/R27 → Mitigated、新增 R28、Open Questions 3/4/5 更新为已回答或部分回答

### 2.3 核心结论

T43 最终形成的结论是：

> **在混合图（full source graph）上，GCN 仍然领先。HGCN 的优势是条件性的——它只在 explicit hierarchy 层（`extends` 边）上显现，那里存在真正的层级深度和分支结构。加入 synthesized `instance_of` 边——它们在结构上是平坦的——会稀释层级信号，让比较结果翻转回 GCN 领先。**

这个结论不与 Milestone 3 矛盾；它为 Milestone 3 的"GCN overall ahead"添加了 provenance 维度的条件性解释。

### 2.4 对后续开发的意义

1. **Milestone 4 可以闭合**：T43 是 Milestone 4 的最后一个任务。完成后项目可以进入 Milestone 5（论文骨架与 proof-side bridge）。

2. **论文叙事的关键转折**：从"双曲不行"到"双曲在特定条件下行"——这个条件性结论比无条件的模型胜负更有学术价值。它回答的不是"哪个模型更好"，而是"什么条件下哪个模型更好"。

3. **论文贡献点已成型**：(1) 可复现管线、(2) 标准化 grouped retrieval 协议、(3) 图结构诊断框架、(4) provenance-conditional 双曲结论——四个贡献点已经可以在 T50 中正式整理。

4. **对 proof-side bridge 的启示**：如果后续做 premise retrieval 或 ancestor explanation，应优先使用 explicit_only 图作为知识表示，因为这是 HGCN 表现最好的图形态。

5. **待核清项**：R28（synthesized_only aggregate/per-seed 口径差异）和 N1（FS synthesized_only 表格数值错误）需要在论文定稿前修正。

## 3. 为什么给出 PASS 的 review 结果？

### 3.1 任务目标完全达成

T43 要求的六件事全部完成：三类 provenance split 的角色分配正确、synthesized 边的结构性稀释作用已明确写出、项目结论已精化为 provenance-conditional、精度约束全部满足。

### 3.2 没有伪实现或超出范围

- T43 是纯文档任务，不涉及代码、训练或数据处理。所有数值均来自已通过 review 的 T41/T42 产物。
- Worker 没有新增训练或修改 T40/T41/T42 冻结的语义和数据。
- 所有修改的文件都在 Allowed Files 范围内。

### 3.3 精度约束已满足

- Field.Subfield explicit_only 的 hop_4_plus 基于 4/5 seeds：已在 Section 4.2 显式注明
- synthesized_only GCN aggregate 与 per-seed 口径差异：已在 Section 5.2 显式登记并关联 R28

### 3.4 一个数据表格错误不影响 PASS

Section 5.1 的 FS synthesized_only 表格中，GCN MAP 值被错误地写成 0.6857（实际上是 HGCN 的值，正确应为 1.0000）。这是一个复制粘贴错误。但：
- 周围的叙述文字正确地说明了"GCN matches or outperforms HGCN"
- Section 5.2 正确记录了 aggregate 值为 1.0000
- synthesized_only 只是 controlled diagnostic，不是主证据
- 主证据（explicit_only）的所有数值完全正确

因此这不构成 blocking issue，但在论文定稿前必须修正。

### 3.5 文档诚实且精确

- 报告明确区分了三类 split 的角色（primary/diagnostic/reproducibility）
- 没有声称"HGCN 优于 GCN"的无条件命题
- 候选图规模局限性已在 Section 9.4 显式承认
- 方差没有被隐藏（FS GCN explicit_only MAP std = 0.0800）
- hierarchy_mixed = full source graph 的 identity scope 局限性已注明（仅适用于不含 `uses` 边的候选图）

综上所述，T43 的工作质量满足 review 标准。核心发现可靠、精度约束已满足、治理文档更新完整。唯一需要后续修正的是 Section 5.1 的表格数值错误（N1）和 R28 的根因核清。
