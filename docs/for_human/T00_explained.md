# T00 通俗解释与 Review 说明

> 编写时间：2026-05-10
> 对应任务：T00 — 创建根目录入口文档
> Review 结果：PASS

---

## 1. 这个任务在做什么？（通俗版）

想象你走进一个正在建设中的大楼。如果你在大门口看不到任何指示牌——不知道这栋楼是做什么的、有哪些房间、施工规则是什么——你很容易走错地方，甚至不小心把刚砌好的墙给拆了。

**T00 就是在给这个仓库"挂门牌和指示牌"。**

具体来说，仓库里虽然已经有很多内部文档（`docs/` 目录下的各种计划、任务板、风险评估等），但站在仓库最外层（根目录），你看不到任何说明。一个新来的 AI 助手（或人）直接打开这个仓库，不知道：

- 这个项目到底在研究什么
- 现在应该做什么、不应该做什么
- 谁负责决策、谁负责执行、谁负责检查
- 工作规则是什么

T00 的目标就是在根目录创建三个关键文件，解决这些问题：

| 文件 | 作用 | 类比 |
|------|------|------|
| `README.md` | 项目名片：一句话说清这是什么项目、当前重点、目录结构、如何开始工作 | 大楼门口的项目简介牌 |
| `AGENTS.md` | 工作规则：定义 Captain（指挥官）、Worker（执行者）、Reviewer（审查员）的职责和纪律 | 施工管理制度 |
| `CLAUDE.md` | 审查规则：专门给 Claude Code AI 审查员看的规则，包括如何判断任务是否合格 | 质检员手册 |

同时，T00 还要求更新两个现有文档（任务板和交接文档），确保它们与新建的入口文件保持一致。

---

## 2. 实现的详细解释

### 2.1 任务目标

根据任务包 `docs/tasks/M0_governance/T00_root_project_docs.md`，T00 的目标是：

> 创建根目录 `README.md`、`AGENTS.md`、`CLAUDE.md`，让后续 Captain / Worker / Reviewer 从仓库入口就能理解项目定位、当前治理文件、任务纪律和 review 方式。

这是一个**纯文档任务**，不涉及任何代码、实验或数据变更。

### 2.2 任务流程

Worker 按照任务包的要求执行了以下步骤：

1. **阅读输入文档**：阅读了 `docs/reference/AI_coding_workflow.md`、`docs/02_experiment_plan.md`、`docs/04_task_board.md` 等治理文档，理解当前项目定位和工作流规则。

2. **创建 README.md**：
   - 一句话定位：这是一个构建可复现 benchmark、protocol 和 diagnostics 管线的研究仓库
   - 明确当前主线是 benchmark / protocol / diagnostics，而非"证明双曲模型更强"
   - 明确当前**不主张**的内容（如 HGCN 已经优于 GCN 的声明）
   - 列出重要目录及其作用
   - 描述工作循环：Captain 选择任务 → Worker 执行 → Reviewer 审查 → Captain 收口

3. **创建 AGENTS.md**：
   - 定义 Captain（决策与维护治理文档）、Worker（执行任务包）、Reviewer（只读审查）三个角色
   - 列出不可违反的规则：单一任务制、只改 Allowed files、不碰 Forbidden scope、不把计划写成事实
   - 定义任务包的标准契约（Task ID、Goal、Allowed files、Forbidden scope 等）
   - 列出高风险工作类型（核心算法变更、评测协议变更等）

4. **创建 CLAUDE.md**：
   - 明确 Reviewer 默认只读
   - 定义 PASS / PASS_WITH_WARNINGS / BLOCK 三级判决及适用场景
   - 列出 adversarial review 的触发条件
   - 针对T00增加特定的 review 边界说明

5. **更新 docs/04_task_board.md**：
   - 改善措辞一致性（标点、格式微调）
   - 新增 Execution Note 段落，记录 worker 已完成但 T00 未勾选完成
   - 未擅自标记 T00 为完成状态

6. **更新 docs/07_handoff.md**：
   - 更新项目描述为更准确的定位
   - 补充根目录入口文档到治理入口列表
   - 更新状态反映 worker 已完成但尚待 review
   - 明确下一步是 review → Captain 收口

7. **验证**：运行 `git diff` 命令确认改动范围，人工检查三份文档内容。

### 2.3 文件变化汇总

| 文件 | 操作 | 变化概要 |
|------|------|----------|
| `README.md` | 新建 | 项目定位、目录说明、工作循环、当前任务入口 |
| `AGENTS.md` | 新建 | 三角色职责、工作纪律、任务包契约、高风险定义 |
| `CLAUDE.md` | 新建 | Reviewer 只读规则、三级判决、adversarial review 触发条件 |
| `docs/04_task_board.md` | 修改 | 措辞优化、新增 Execution Note、T00 未勾选完成 |
| `docs/07_handoff.md` | 修改 | 项目描述更新、入口列表补充、状态和下一步更新 |

### 2.4 对后续开发的意义

T00 是整个项目的**治理基础**。它的完成意味着：

1. **后续 AI 助手有清晰的入口**：无论是 Captain、Worker 还是 Reviewer，都可以从根目录的三个文件快速理解项目定位和工作规则，不需要先翻遍 `docs/` 目录。

2. **防止方向偏移**：README.md 和 AGENTS.md 都明确写了当前不主张的内容（不声称 HGCN 已优于 GCN、不做端到端证明等），这防止了后续 worker 偏离主线的风险。

3. **建立了可复现的工作循环**：Captain → Worker → Reviewer 的单任务循环被明确写入文档，后续所有任务都按此流程推进。

4. **为 T01 及后续任务铺路**：T01（审查 docs/00~08 一致性）和 T10（版本锁定）都需要在项目定位明确的前提下才能正确执行。T00 提供了这个前提。

---

## 3. 为什么给出了 PASS 的 review 结果？

### Review 检查清单与结论

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 是否真的完成任务 | ✅ | 任务包要求的 5 个文件均已创建或更新，内容覆盖所有要求 |
| 是否有伪实现/mock/stub/hardcode | ✅ 无 | 全部为纯 Markdown 文档，无代码、无占位符 |
| 是否缺测试或验证 | ✅ 不缺 | Worker 运行了 `git diff` 验证，做了人工检查；对纯文档任务足够 |
| 是否过度工程 | ✅ 无 | 三个文件内容精炼，没有冗余或不必要的抽象 |
| 是否破坏已有功能 | ✅ 无 | 只修改了 Allowed files 范围内的文件，未触碰任何代码或实验配置 |
| 文档是否把计划写成事实 | ✅ 无 | 所有表述均使用条件性/进行时措辞，未将目标表述为已完成事实 |

### 关键正面发现

1. **定位准确**：三份文档均正确反映 benchmark / protocol / diagnostics 的主线定位，与 `docs/02_experiment_plan.md` 一致。

2. **非目标清晰**：README.md 明确写了"not currently claiming"的条目，包括不声称 HGCN 已稳定优于 GCN。

3. **T00 未被提前勾选完成**：任务板正确记录了 worker 状态，但没有擅自标记完成，遵循了"必须先 review"的流程。

4. **Forbidden scope 全部未触碰**：`docs/02_experiment_plan.md` 未修改、`project_bootstrap/` 未修改、未运行长任务、未声称双曲优势。

### 两个非阻塞问题

1. `CLAUDE.md` 中的 `Review Boundary For T00` 段落是 T00 专用的，T00 完成后应更新。这不影响 T00 本身的正确性。

2. `docs/reference/AI_coding_workflow.md` 有一个与 T00 无关的既有改动（reviewer prompt 模板的措辞微调）。Worker 正确标注了这一点且未触碰。Captain 收口时应决定保留或丢弃。

### 结论

Worker 完整地执行了任务包的所有要求，没有触碰任何 Forbidden scope，验证方式与任务包一致，文档内容准确无矛盾。两个非阻塞问题都是后续 Captain 可以轻松处理的小事项。因此判定为 **PASS**。
