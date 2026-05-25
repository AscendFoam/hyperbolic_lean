# T62 Review Explanation

## 1. 通俗解释：这个 Task 在做什么？

项目已经走过了漫长的阶段：
1. **实验阶段（Milestone 1-4）**：构建数据管线、设计评测协议、跑对比实验。最后发现：双曲图网络（HGCN）只有在只保留 `extends` 边的纯层级图上才有优势；在完整图上欧氏网络（GCN）反而更强。
2. **论文阶段（Milestone 5）**：把实验发现写成论文、画图表、整理提交资产包、冻结仓库边界。

现在到了最后一步——**决定投哪个会议/期刊，并列出还差哪些格式工作**。这就是 T62 做的事。

## 2. T62 做了什么？详细解释

### 2.1 目标

T62 的目标是：在仓库已经冻结的前提下，不新增任何实验或数据，只做两件事：
1. **选 venue**：明确优先级最高的投稿目标（ITP、CPP 还是 FM？）
2. **列清单**：针对选定的 venue，写出从当前状态到可提交状态之间还差哪些工作

### 2.2 任务流程

T62 是一个纯文档/规划任务，不涉及任何代码修改。

**输入**：
- `docs/投稿路线图（FM-ITP-CPP-备选 venue 对照）.md`：记录了几个候选 venue 的对照分析
- `docs/paper_artifact_package.md`：冻结的提交资产包
- `docs/paper_draft.md`、`docs/paper_outline.md`：论文正文和骨架
- `docs/paper_figures_and_tables.md`：图表规格
- 所有治理文档（`docs/00~08`）

**产出**：
- 新建 `docs/venue_submission_plan.md`：Venue 选择 + 提交清单 + 资产修改说明
- 更新全部 8 份治理文档，把状态从 T61 切换到 T62

### 2.3 核心产出：`docs/venue_submission_plan.md`

这份文档包含三个部分：

**Part 1: Venue Choice / Priority（选 venue）**

确认了：
- **ITP（主 venue）**：Interactive Theorem Proving 会议，最适合 proof assistant 社区。论文讲的是 Lean/Mathlib hierarchy 的管线、协议和诊断，ITP 读者会直接理解为什么 `extends` vs `instance_of` 的区分重要。
- **CPP（副主 venue）**：Certified Programs and Proofs，重视可复现 artifact 和工具贡献。祖先解释 demo（T52a）直接满足 CPP 的 tool demo 标准。
- **FM（备选）**：需要多仓库复现后才能考虑，当前不活跃。
- 策略：先投 ITP，如果被拒则改格式投 CPP，不改变证据基础。

这个选择与 `docs/02_experiment_plan.md` 第 10.2 节的建设（ITP > CPP > FM）完全一致。

**Part 2: Submission Checklist（提交清单）**

列出 6 个类别的剩余工作：
1. **LaTeX 格式化**：选 LIPIcs/LNCS 模板、转换 markdown 到 LaTeX、加文档类/包、页面数检查
2. **作者信息**：作者名、机构、ORCID、通讯地址、关键词
3. **图表渲染**：F1（provenance split 结构图，分组柱状图）、F2（hop-depth delta 图，论文最重要的可视化）
4. **参考文献**：转 BibTeX、验证引用完整性
5. **提交资产**：打包 .tex/.bib/图表/README、运行提交清单
6. **叙事调整**：ITP 版调整摘要强调 proof assistant 基础设施

**Part 3: Asset Delta Note（资产修改说明）**

记录针对 ITP 的 3 处可选 wording 调整：
- 摘要首句加入 "ancestor explanation tool"
- 标题从问题式改方法论式
- 把 Proof-Side Bridge 从讨论节提升为独立节

明确声明：**不涉及数值修改、claim 边界扩张或 contribution 增减**。这些修改是可选且提升 venue fit 的，应该在 LaTeX 转换时一并应用，不修改当前 markdown source-of-truth。

### 2.4 治理同步

- 全部 8 份治理文档（`00_raw_idea.md` 到 `08_risks_and_open_questions.md`）的状态行已更新为 "T62 worker executing"
- `05_decision_log.md` 新增 D052 记录 T62 的决策
- `07_handoff.md` 新增 item 93 记录 T62 执行
- `R25`、`R30`、`R08` 继续保留为活跃风险（不写成已关闭）

### 2.5 未改动的内容

- `docs/paper_draft.md`、`docs/paper_outline.md`、`docs/paper_figures_and_tables.md`、`docs/paper_artifact_package.md`：T62 未修改这些文档
- `docs/投稿路线图（FM-ITP-CPP-备选 venue 对照）.md`：不变，因为 venue 选择与已有路线图一致
- 所有 `project_bootstrap/`、`data/`、`artifacts/`：禁止范围

### 2.6 对后续开发的意义

T62 是项目从"写论文"到"准备提交"的关键桥梁：

1. **给后续 worker 明确的起点**：下一个人不需要再讨论"投哪里"，直接按照 `venue_submission_plan.md` 的 checklist 执行即可
2. **减少决策反复**：ITP → CPP 的降级路径已明确，不需要每次重新评估
3. **格式差额透明化**：6 类差额写清楚后，后续任务可以并行或串行地逐项完成
4. **claim boundary 保护**：asset delta note 明确声明哪些可以改（措辞）、哪些不可以改（数值、claim、contribution），防止格式化过程中无意引入新主张

## 3. 为什么 Review 结果是 PASS？

没有 blocking issue 的理由：

1. **任务目标完全达成**：
   - ✅ Venue 路径明确（ITP → CPP → FM）
   - ✅ 6 类格式差额清单完整且可执行
   - ✅ Asset delta note 说明清晰，且声明不涉及 claim 边界修改
   - ✅ 所有治理入口显示 T62 为当前任务

2. **没有伪实现或虚假完成**：`docs/venue_submission_plan.md` 是真实的规划文档，内容完整、逻辑自洽、与已有路线图和治理一致。

3. **没有额外实验或未 review 数值**：所有内容基于已有 reviewed 证据，未引入新 claim 或数字。

4. **遵循 Narrow 阶段纪律**：完全是规划/文档类工作，不涉及代码、数据、实验或 artifact。

唯一的非阻塞问题是一个老生常谈的模式：`.claude/settings.json` 被修改了（添加了 Read 权限模式）。这是至少第 7 次被注意到（T31、T43、T52a、T55、T57、T61、T62），每次都被排除在 commit 外。这次同样处理即可。

## 4. 下一步怎么做？

T62 通过后，项目有两个自然的后续方向：

### 方向 A：ITP LaTeX 转换（建议优先）
- 把 `docs/paper_draft.md` 转为 LIPIcs 或 LNCS 格式的 LaTeX
- 应用 3 处可选 ITP-specific wording 调整
- 根据 `paper_figures_and_tables.md` 的规格渲染 F1 和 F2 图表
- 转换参考文献为 BibTeX

### 方向 B：提交资产打包（可与 A 并行）
- 按 T62 checklist 的 Section 2.5 组装提交资产包
- 运行 `paper_artifact_package.md` Section 6 的提交检查清单
- 确认 R25 措辞正确（不写 "independently reproduced"）

### 长期
- 若 ITP 被拒，按 CPP 格式重新调整（主要是文档类和抽象措辞）
- 当前不需要任何新实验、新数据或新 demo

## 5. 对 Worker 总结的补充说明

Worker 的总结（`docs/worker_summary/T62_worker_summary.md`）准确且完整。以下几点可作补充：

1. **工作树含遗留改动**：检查 git diff 时会发现 `paper_artifact_package.md`、`paper_draft.md`、`paper_outline.md` 也有修改。但这些来自 T60/T61 未提交的工作，不是 T62 的改动。Worker 正确声明了 T62 未修改这些文件。

2. **决策日志 D052**：目前标记为 "Pending Review"。Review 通过后应更新为 "Accepted"。

3. **venue 选择与已有路线图一致**：`docs/02_experiment_plan.md` 第 10.2 节在 T62 之前就建议 ITP > CPP > FM，T62 没有改变这个优先级，只是将其正式化并补充了完整的提交清单。
