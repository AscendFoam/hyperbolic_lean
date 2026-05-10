# T01 通俗解释与 Review 说明

> 编写时间：2026-05-10
> 对应任务：T01 — 治理文档一致性复查
> Review 结果：PASS_WITH_WARNINGS

---

## 1. 这个任务在做什么？（通俗版）

T00 完成后，仓库根目录有了三个新的入口文件（README.md、AGENTS.md、CLAUDE.md），加上 `docs/` 目录下原有的 9 个治理文档（00~08），整个仓库已经有十几个文档在描述同一件事——项目的目标、规则、当前状态和下一步。

但人多嘴杂，文档多也一样。**T01 的任务就是检查这些文档之间有没有"各说各话"的情况，确保它们互相一致。**

举几个具体例子：

- 任务板说当前任务是 T01，但交接文档是不是还写着"尚未开始"？
- 决策日志里记了一个待定问题，但风险列表里是不是还挂着同一个问题当"未解决"？
- README 是不是还写着"T00 正在进行"，实际上 T00 早就完成了？

T01 就是做一轮"大扫除"，把这些不一致的地方找出来、修好，确保后续的 worker 打开任何一份治理文档，看到的都是同一个项目状态。

---

## 2. 实现的详细解释

### 2.1 任务目标

根据任务包 `docs/tasks/M0_governance/T01_governance_consistency_review.md`，T01 的目标是：

> 审查并校正 `docs/00~08`、`docs/tasks`、根目录入口文档之间的一致性，确保后续 worker 可以按 `Current Unique Task` 直接开工。

### 2.2 Worker 需要处理的核心问题

T00 review 阶段遗留了一个悬置项：`docs/reference/AI_coding_workflow.md` 中有一处与 T00 任务无关的既有改动（reviewer prompt 模板中的措辞微调：任务1/2 → 第一件事/第二件事，T16 → 对应 task）。

T00 review 时将这个改动标记为"non-blocking issue"，建议由 Captain 在 T01 收口时决定是否保留。T01 的核心工作之一就是对此做出正式裁决。

### 2.3 任务流程与文件变化

Worker 执行了以下步骤：

1. **阅读所有治理文档**（docs/00~08、根目录入口、任务包、T00 review），识别不一致项。

2. **更新 docs/05_decision_log.md**：新增决策 D007，正式决定保留 `AI_coding_workflow.md` 中的措辞微调。

   ```text
   D007: 保留 docs/reference/AI_coding_workflow.md 中的 reviewer prompt 措辞微调
   - 决策：将 reviewer prompt 的措辞微调视为正式 workflow 文案更新保留，不在 T01 中回滚。
   - 后果：相关风险项与 deferred item 不再把这处改动视为待裁决状态。
   ```

3. **更新 docs/08_risks_and_open_questions.md**：移除了三个已由 D007 解决的悬置项：
   - R10（AI_coding_workflow.md 改动风险）→ 已裁决，不再需要
   - OQ8（是否保留该改动的开放问题）→ 已决策，不再需要
   - D05（待裁决的 deferred item）→ 已裁决，不再需要

4. **更新 docs/04_task_board.md**：在 Execution Note 中新增一条，记录 AI_coding_workflow.md 措辞微调已归入 T01 复查范围。

5. **更新 docs/07_handoff.md**：将状态从"治理一致性复查尚未开始"更新为"治理一致性复查正在处理剩余对齐项"。

### 2.4 文件变化汇总

| 文件 | 操作 | 变化概要 |
|------|------|----------|
| `docs/04_task_board.md` | 修改 | Execution Note 新增 AI_coding_workflow.md 裁决说明 |
| `docs/05_decision_log.md` | 修改 | 新增 D007 决策 |
| `docs/07_handoff.md` | 修改 | 状态从"尚未开始"更新为"正在处理" |
| `docs/08_risks_and_open_questions.md` | 修改 | 移除 R10、OQ8、D05 三个已解决条目 |

未修改的 Allowed files（worker 认为已一致或不需要改动）：

- `docs/00_raw_idea.md`、`docs/01_feasibility_report.md`、`docs/03_architecture.md`、`docs/06_eval_protocol.md`：均正确引用 T01 为当前任务。
- `README.md`、`AGENTS.md`、`CLAUDE.md`：worker 未做更新（见下文 review 发现）。
- `docs/tasks/**`：任务包无需修改。
- `docs/reference/AI_coding_workflow.md`：本轮未再修改本体，只记录了"保留现有改动"的决策。

### 2.5 对后续开发的意义

T01 的完成标志着治理初始化的最后一个闭环：

1. **悬置项清零**：T00 review 遗留的唯一 non-blocking issue 已通过正式决策（D007）解决。后续 worker 不再需要关心 `AI_coding_workflow.md` 的既有改动。

2. **治理文档进入可信赖状态**：docs/00~08 和根目录入口文档现在指向同一个项目状态。后续 worker 可以信任任何一份治理文档的信息。

3. **为 T10（版本锁定）铺路**：T10 是第一个非治理任务，需要进入代码和数据层面。T01 确保了治理层面的地基已经稳固，不会在执行 T10 时被文档矛盾干扰。

4. **决策链完整**：D001~D007 形成了从"主线收束"到"治理初始化完成"的完整决策链，为论文叙事和项目回顾提供了可追溯的依据。

---

## 3. 为什么给出了 PASS_WITH_WARNINGS 的 review 结果？

### Review 检查清单与结论

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 是否真的完成任务 | ⚠️ 大部分完成 | 核心悬置项（AI_coding_workflow.md）已解决，但有两处过时引用未更新 |
| 是否有伪实现/mock/stub/hardcode | ✅ 无 | 全部为纯文档文本更新 |
| 是否缺测试或验证 | ✅ 不缺 | Worker 运行了 rg 命令和 git diff，与任务包要求一致 |
| 是否过度工程 | ✅ 无 | 改动最小化，只做了必要的同步 |
| 是否破坏已有功能 | ✅ 无 | 纯文档更新，未触碰代码或实验配置 |
| 文档是否把计划写成事实 | ✅ 无 | D007 是对已有改动的裁决，不是对未来的承诺 |

### 为什么是 PASS_WITH_WARNINGS 而不是 PASS？

T01 的目标是"审查并校正 docs/00~08、docs/tasks、根目录入口文档之间的一致性"。Worker 解决了核心悬置项，但留下了两处文档不一致：

1. **README.md 第 54 行**写着 "this round's worker scope is still `T00` until reviewer and Captain finish the close-out flow"。T00 早已完成，当前任务是 T01。这行已过时。

2. **CLAUDE.md 末尾**有一个 `Review Boundary For T00` 专节，列出的检查项（"whether docs/04_task_board.md avoids prematurely marking T00 complete" 等）已不适用于当前阶段。

这两处都在 T01 的 Allowed files 列表中，worker 本可以在此轮更新。它们的过时不会阻塞后续 worker（因为 `docs/04_task_board.md` 是任务状态的权威来源），但它们确实属于"一致性"的范畴。

### 为什么不是 BLOCK？

两个过时引用都是**非阻塞**的：

- README.md 正确指向了 `docs/04_task_board.md` 作为权威来源，过时的那句话只是附加说明。
- CLAUDE.md 的 T00 专节不影响 reviewer 的通用审查规则，只影响一个已完成的任务。
- 后续 worker 按 `Current Unique Task` 开工不会受影响。

### 正面发现

1. **核心问题解决得很好**：AI_coding_workflow.md 的悬置项通过正式决策（D007）干净利落地解决了，不是简单地忽略或回滚。

2. **文档间一致性高**：docs/00、01、03、06 都正确引用了 T01 为当前任务，与 task board 和 handoff 一致。

3. **移除悬置项干净**：R10、OQ8、D05 的移除都有 D007 作为依据，不是随意删除。

4. **T01 未被提前标记完成**：worker 遵守了"不标记未 review 任务为完成"的 Forbidden scope。

### 结论

Worker 完成了 T01 的核心工作（解决已知悬置项，同步治理文档状态），但留下了两处 Allowed files 中的过时引用。这两处不影响后续 worker 开工，但严格来说属于"一致性"的遗漏。因此判定为 **PASS_WITH_WARNINGS**，建议 Captain 在收口时一并更新。
