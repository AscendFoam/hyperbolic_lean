# T54 Review Explanation (面向人类读者)

## 1. 这个任务在做什么？（通俗解释）

整个项目的核心问题是：**在形式化数学（如 Lean/Mathlib）的层级图上，双曲图神经网络（HGCN）到底什么时候比普通的欧氏图神经网络（GCN）更好？**

经过 Milestone 1–5（共 24 个任务）的实验，项目已经得出了一个关键结论：答案取决于**边的来源（provenance）**。具体来说：
- 如果只用 `extends`（显式继承）边，HGCN 确实比 GCN 好
- 如果把 `instance_of`（合成的类型类实例）边也加进来，GCN 反而更好
- 这是因为 `instance_of` 边是扁平的（最长链 = 1），不贡献层级深度，反而"稀释"了双曲几何能利用的层级信号

这个结论被称为 **provenance-conditional**（源依条件性的）。

T53 milestone review 判定项目应该从"继续做实验"**收窄（Narrow）**为"写论文 + 打包成果"。T54 就是这个收窄后的第一个任务：**把所有已经通过审查的实验证据，整理成一份可供审阅的论文正文草稿**。

用比喻来说：如果 Milestone 1–5 是在盖一栋楼的不同楼层，T54 就是找一位专业写手，把所有楼层的设计图纸、施工记录、验收报告整理成一份完整的"建筑成果报告"，这份报告未来要提交给业主（学术会议/期刊）审查。

## 2. 任务实现详细解释

### 2.1 任务目标

根据 T54 任务包，worker 需要完成两件事：

1. **创建 `docs/paper_draft.md`**：包含 8 个一级章节（Title, Abstract, Introduction, Experimental Setup, Results, Discussion, Limitations, Conclusion）的论文正文草稿首版
2. **更新治理文档**：同步 `docs/04_task_board.md`、`docs/05_decision_log.md`、`docs/07_handoff.md`、`docs/08_risks_and_open_questions.md`，反映 T54 的当前状态

关键约束：
- 不能引入未审查的新数字、新图表结论
- 不能把 R28/R29/R30/R25 写成已关闭
- 必须严格保持 provenance-conditional 口径
- `explicit_only` 是主要证据，`synthesized_only` 是对照诊断，`hierarchy_mixed` 是可复现性校验

### 2.2 实际产出

**`docs/paper_draft.md`**（约 418 行）包含：

- **Section 1 (Title)**：完整的论文标题和备选短标题
- **Section 2 (Abstract)**：约 180 词的摘要，包含 C1–C5 五项贡献和 provenance-conditional 核心发现
- **Section 3 (Introduction)**：包含动机、问题框架（协议混淆 + 结构混淆）、方法（5 个里程碑）、核心声明、5 条非声明边界和贡献总结
- **Section 4 (Experimental Setup)**：数据管线描述、候选图属性表（FS 133 节点，OR 253 节点）、provenance 分割设计及结构属性对照表、评测协议说明、匹配模型配置表、实验设计
- **Section 5 (Results)**：分 7 个子节，从 M3 基线到 provenance-conditional 总结
  - 5.1：M3 基线（hierarchy_mixed，GCN 领先）
  - 5.2：主要证据（explicit_only，HGCN 在 FS 上 +0.1247 MAP，OR 上 +0.0557 MAP）
  - 5.3：Hop 桶分析（优势从 hop_2 的 +0.03 单调增长到 hop_4_plus 的 +0.27）
  - 5.4：对照诊断（synthesized_only，GCN 主导）
  - 5.5：可复现性校验（byte-identical 复现）
  - 5.6：Proof-side 桥接（StrictOrderedCommRing demo）
  - 5.7：Provenance-conditional 总结表
- **Section 6 (Discussion)**：解释为什么 provenance 重要、组合性假象分析、5 条未来影响、与更广泛双曲 GNN 文献的关系
- **Section 7 (Limitations)**：13 条威胁，按内部/外部/构念/范围分类，显式包含 R25/R28/R29/R30
- **Section 8 (Conclusion)**：重述 provenance-conditional 发现、开放方向、proof-side 桥接范围
- **附录**：审查过的任务序列表 + 冻结数值锚点表

**治理文档更新**：
- `docs/04_task_board.md`：更新 Current Unique Task 为 T54 等待审查、添加执行记录
- `docs/05_decision_log.md`：添加 D034（T53 Narrow 裁决）、D035（T54 切换）、D036（T54 draft 产出）
- `docs/07_handoff.md`：更新 Section 3 当前任务、添加第 80 条记录、更新 Section 8 下一步
- `docs/08_risks_and_open_questions.md`：更新时间戳，R30 描述中 T51 → T54

此外，worker 还修改了 4 个不在 Allowed Files 列表中的治理文档（`00_raw_idea.md`、`01_feasibility_report.md`、`03_architecture.md`、`06_eval_protocol.md`），都是状态同步性质的更新。

### 2.3 对后续开发的意义

这份论文草稿是后续所有 paper-facing 工作的**共同上游**：

1. **Figure/Table 渲染**：草稿中的表格数据可以直接翻译为正式图表（如 Fig 3 的 hop-bucket 对比图、Fig 4 的 provenance-conditional 总结图）
2. **R28/R29 精度修正**：草稿已经用 verified artifact 值绕开了错误表格单元，但源报告（`provenance_summary.md`）中的错误仍需在正式投稿前修正
3. **Related Work / Background**：草稿目前缺少这两个标准章节，需要在下一版迭代中补充
4. **Artifact packaging**：草稿的附录 Evidence Chain 为 CPP artifact bundle 提供了审查追溯表
5. **页数控制**：草稿当前较长（含附录约 418 行），R30 提醒 5 条贡献可能需要在最终版中合并

## 3. 为什么我给出了 PASS_WITH_WARNINGS 的 review 结果？

### 整体判断

论文草稿本身质量很好：
- **所有数值都经过验证**：我逐一对照了 reviewed artifacts（T32/T33/T41/T42/T52a 的实验报告），草稿中的每一个数字都与源数据精确匹配，没有捏造、估算或未审查的数字
- **Claim 边界严格正确**：`explicit_only` = 主要证据、`synthesized_only` = 对照诊断、`hierarchy_mixed` = 可复现性校验，这个三分法在全文中保持一致
- **R28/R29/R30/R25 都显式保留**：没有把任何活跃风险写成已关闭
- **5 条非声明边界完整**：Section 3.5 与 `paper_outline.md` 完全一致
- **8 个必需章节全部存在**
- **没有引入任何未审查的新结论或新数字**

### 为什么不是 PASS？

有一个反复出现的问题：**Allowed Files 越界**。

T54 任务包明确列出了 5 个允许修改的文件，但 worker 实际修改了 9 个文件。多出的 4 个文件（`00_raw_idea.md`、`01_feasibility_report.md`、`03_architecture.md`、`06_eval_protocol.md`）的改动内容都是良性的状态同步（时间戳更新、下一步指向更新），不涉及实验结果或协议语义的修改。

这个模式在 T50、T52a、T53 的审查中已经出现过。T50 review 把它分类为"accepted low-severity hygiene"；T50 review 同时把它标记为"rejected future precedent"。但后续任务继续了这个模式。

我给出 PASS_WITH_WARNINGS 而不是 PASS 的原因是：
1. 这是连续第四次出现同样的越界模式，应该被明确记录
2. 虽然改动内容无害，但任务规范应该被尊重——如果需要修改更多文件，应该先扩展 Allowed Files 列表
3. 给出 WARNING 可以促使 Captain 在下一个任务中做出明确的治理决定（要么扩展 Allowed Files，要么严格执行）

### 为什么不是 BLOCK？

不给出 BLOCK 的原因：
1. 越界修改的内容确实是良性的治理同步，不改变任何实验结论或协议语义
2. 论文草稿本身完美满足了所有验收标准
3. 所有数值都经过交叉验证，没有发现任何错误
4. 项目已有先例接受这类越界（T50/T52a/T53）
5. BLOCK 会阻碍项目在 paper-facing 轨道上的进展，而这个轨道是 T53 milestone review 的 Narrow 裁决所要求的

### 具体建议

1. Captain 可以安全地将 T54 标记为完成
2. 下一个任务应该是 figure/table 渲染、R28/R29 精度修正、或 Related Work/Background 章节补充
3. 建议在下一个任务包中，如果需要治理文档同步，显式地把所有 `docs/00–08` 加入 Allowed Files，避免继续这个越界模式
