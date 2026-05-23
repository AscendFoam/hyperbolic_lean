# T59 Review Explanation

## 1. 这个 task 在做什么？（通俗版）

T59 是这个项目"论文准备阶段"的最后一道工序。在此之前，项目已经：

1. 完成了所有实验（跑了 60 次模型训练，对比了双曲模型 HGCN 和欧氏模型 GCN）
2. 完成了论文初稿、图表源文件、以及"给投稿人看的资产包"
3. 通过了上一轮 T58 的审查

T59 的任务是**把这些已经写好的材料统一改成一个口径，让它看起来像是专门投某个会议（ITP/CPP）的论文，而不是一堆没对齐的草稿**。

具体要改三个东西：

- **贡献数量问题**：论文写了 5 条贡献，但目标会议一般只允许 20 页，5 条可能太多。需要决定是保留 5 条还是合并成更少的条数。
- **术语统一问题**：有一份文档里，同一个东西有时叫"5 个核心表格"，有时叫"4 个核心表格 + 1 个汇总表"，需要统一。
- **引用精确性问题**：有一张表的 HGCN 数据来源写的是模糊的"T33/T42"，需要改成更精确的"T33 是主要来源，T42 是交叉验证"。

**不能做**的事情：不能跑新实验、不能改代码、不能引入新数字。

## 2. 这个 task 的实现细节

### 任务目标

T59 的目标是把以下四份"论文面向"的文档收束成统一的投稿终态：

| 文档 | 作用 |
| --- | --- |
| `docs/paper_draft.md` | 论文正文草稿 |
| `docs/paper_outline.md` | 论文骨架（贡献列表、证据链、章节结构） |
| `docs/paper_figures_and_tables.md` | 图表源文件（给排版用） |
| `docs/paper_artifact_package.md` | 投稿资产包（说明每张图/每个结论来自哪个实验） |

同时还要更新 8 份"治理文档"，记录"T59 做了什么事"。

### Worker 的实际改动

#### 改动 1：贡献数量决策（保持 5 条，加 page-budget 备注）

**决策**：保持 5 条贡献（C1–C5）不变，但加入"如果页数不够可以压缩"的措辞。

具体改动三处：

- **`paper_outline.md`** Section 8：新增了一个"Page Budget Note"子节，写清楚"C3 或 C5 可以在页数紧张时放到附录，但默认保留 5 条结构"。
- **`paper_draft.md`** Section 7.4：R30 风险描述从"may need to merge"改成更积极的说法："current draft keeps C1–C5 with page-budget-aware wording; C3 or C5 can be condensed if needed"。
- **`paper_artifact_package.md`** Section 5 的 R30 条目同步更新。

#### 改动 2：核心表格术语统一

**问题**：`paper_artifact_package.md` 的 Section 4 原来有一个 "### Core Tables" 标题，下面列了 T1–T5 五张表。但 T1–T4 是"核心实验结果"，T5 是"汇总表"，属于不同类型的表。这就导致有的地方说"5 个核心表"，有的地方说"4 个核心表 + 1 个汇总表"。

**解决**：把原来的一个标题拆成两个：

```
### Core Tables (T1–T4)    ← 放 T1, T2, T3, T4
### Summary Table (T5)     ← 单独放 T5
```

这样既消除了术语不一致，又更清晰地反映了表格的职能差别。

#### 改动 3：Table T1 的 HGCN 来源更精确

**问题**：Table T1（混合图的 baseline 结果）的数据来源原来写的是 `T33/T42 aggregate.json (HGCN)`，看起来像是两个来源并列。

**解决**：改成更精确的表述：

- 旧：`T32/T33 aggregate.json (GCN), T33/T42 aggregate.json (HGCN)`
- 新：`T32 aggregate.json (GCN); T33 aggregate.json (HGCN, primary); T42 hierarchy_mixed sweeps (cross-check)`

这里的逻辑是：T33 是 HGCN 的正式实验，T42 的 `hierarchy_mixed` split 只是复验（确认结果一致）。所以 T33 是 primary，T42 是 cross-check。

同时更新了 `paper_figures_and_tables.md` 中 T1 的 cross-validation 注释，加上了 "T33 = primary, T42 = cross-check"。

#### 改动 4：治理文档同步

所有 8 份治理文档（`00_raw_idea.md` 到 `08_risks_and_open_questions.md`）都更新了状态行，把 "T58 review PASS" 和 "T59 worker executing" 写进去。`05_decision_log.md` 新增了 D046 条目记录 T59 的完成。`08_risks_and_open_questions.md` 新增了 D22 条目记录 T58 non-blocking notes 已由 T59 关闭。

### 没有改动的

- 没有跑任何新实验
- 没有改任何代码文件（`project_bootstrap/`、`data/`、`artifacts/`）
- 没有改 `docs/02_experiment_plan.md`
- 没有改 review 文件
- 没有引入新数字、新结论
- R25、R30、R08 仍然标记为 Active，没有写成已关闭
- 没有添加任何图片文件

### 对后续开发的意义

T59 是这个项目"最终论文编辑"阶段的收口任务。它完成后，项目将处于一个理论上的**提交前终态**：

- 论文正文（draft）已就绪
- 图表源文件已就绪
- 资产包（source-to-claim 映射）已就绪
- 所有术语和贡献叙事已统一

后续的方向从"写论文"转向"排版和格式适配"——这已经不属于这个实验性研究仓库的核心范围了。

## 3. 为什么我给了 PASS

我的审查结论是 **PASS**，理由如下：

### 任务完成情况

| 验收标准 | 状态 |
| --- | --- |
| AC1：四份 paper-facing 文档关于贡献结构和表格术语不再矛盾 | ✅ 全部一致 |
| AC2：Table T1 的 HGCN source 关系精确（T33 primary, T42 cross-check） | ✅ 已精确表述 |
| AC3：贡献数量调整在所有 paper-facing 文档中一致应用 | ✅ 3 处同步更新 |
| AC4：所有治理文档显示 T59 为当前任务，T58 已完成 | ✅ 8 份文档均已更新 |
| AC5：没有引入新实验或未 review 数字 | ✅ 只有文本改动 |

### 没有发现问题

- **没有伪实现**：所有改动都是文档文本编辑，不涉及代码。Text diff 可以在 git 中逐行审查。
- **没有 mock/stub**：不适用。
- **没有安全或合规问题**：不涉及。
- **没有过度工程**：改动量很小（~44 行新增，~17 行删除），完全针对任务书的目标。
- **没有破坏已有功能**：只改了文档文本，不改变任何可执行逻辑。
- **验证通过**：任务书中的三个 `rg` 验证命令全部通过。
- **没有把计划写成事实**：R25、R30、R08 继续标记为 Active。

### 非阻塞问题（不改变 PASS 结论）

我比对了 Worker 的总结和实际 diff，发现一个微小的清单遗漏：

- `paper_artifact_package.md` 的提交检查清单中，R30 条目仍然是 `- [ ]`（未勾选），但 Worker 实际已经做了相关改动。这个勾选应该在下次编辑时顺手补上。

这不是 blocking issue，因为清单本身是辅助性的，不影响文档内容的正确性。

## 4. 对 Worker 的 summary 和已有文档的补充

Worker 的 summary（`docs/worker_summary/T59_worker_summary.md`）写得很好，准确地描述了所做的改动。Verification 结果也完整汇报了。

我审阅了以下文件的一致性：

- 确认了 T59 任务书中列出的每条 Expected Output 都已被满足
- 确认了 `paper_artifact_package.md`、`paper_draft.md`、`paper_outline.md`、`paper_figures_and_tables.md` 四份文档对 C1–C5 的引用一致
- 确认了不再有任何 "5 core tables" 或 "4 core tables" 的不一致表述
- 确认了 R25、R30、R08 在 `paper_artifact_package.md` 中仍正确标记为 Active

唯一的补充意见是上面提到的提交检查清单勾选遗漏，这可以在 T59 review 接受后的快速修正中处理。
