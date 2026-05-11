# T12 Explained: Grouped Protocol Freeze

## 1. 通俗解释：这个任务在做什么？

之前的 T10 和 T11 分别锁定了版本信息和数据资产的"说明书"。但还有一个关键问题没有解决：**评测协议到底怎么定义？代码里是怎么实现的？两者是否一致？**

举个例子：假设论文里说"我们报告 Recall@1、MAP、nDCG@10 和 grouped-MRR"，但代码里有一个 runner 漏掉了 nDCG@10 的输出。那么当有人跑 seed sweep 汇总结果时，这个 runner 的 nDCG@10 就是空的，导致汇总表有空洞。

T12 做的就是把这件事说清楚、对齐好：

1. 写一份正式的 grouped retrieval 协议文档，明确定义任务名、查询单元、正例集合、配置字段、指标集和输出格式
2. 检查代码输出是否与协议文档一致，如果有缝隙就做最小修正
3. 把 legacy 兼容问题（旧配置键 `ancestor_ranking` 实际上跑的是 grouped 协议）显式记录下来

## 2. 实现详解

### 2.1 任务目标

根据任务包 `docs/tasks/M1_protocol/T12_grouped_protocol_freeze.md`，T12 的目标是：

> 固化 grouped multi-positive ancestor retrieval 协议，确认代码入口、配置字段、指标名和输出格式。

注意：这个任务被标记为 **adversarial review**（对抗性审查），因为它涉及评测协议和指标定义的变更，属于高风险范畴。

### 2.2 任务流程

Worker 执行了以下步骤：

1. **阅读现有代码和文档**：
   - `relation_tasks.py`：任务构造和 hop 追踪
   - `relation_baseline_common.py`：grouped 指标计算
   - 三个 baseline runner（GCN、hyperbolic、grouped retrieval）
   - sweep/report 汇总代码

2. **创建 `docs/grouped_retrieval_protocol.md`**：新文件，包含七个部分：
   - **Canonical Task Name**：正式名称和 legacy 键映射
   - **Query Unit And Positives**：`(src, relation)` 查询单元和全部真祖先正例
   - **Frozen Config Fields**：10 个关键配置字段及其语义
   - **Frozen Metric Set**：8 个 grouped 指标 + 3 个 hop bucket + legacy MRR 的地位说明
   - **Frozen Output Structure**：`metrics.json` 和 `result_summary.json` 的标准键
   - **T12 Alignment Result**：本轮对齐状态说明
   - **Non-Goals**：明确 T12 不做什么（不改 legacy 键名、不改模型架构、不收口 hop bucket 报告）

3. **更新 `docs/06_eval_protocol.md`**：
   - 状态从"冻结前草案"推进到"T12 协议冻结草案"
   - 新增 Section 3.1：代码入口与字段映射（4 类代码入口、10 个冻结配置字段、10 个冻结输出字段）

4. **做最小代码修正**：
   - 在 `run_relation_grouped_retrieval_baseline.py` 第 472 行添加一行：
     ```python
     result_summary["grouped_test_ndcg_at_10"] = grouped.get("ndcg_at_10")
     ```
   - 原因：另外两个 runner（GCN 和 hyperbolic）已经在输出这个字段，下游 sweep/report 代码也已经在消费它，唯独 grouped retrieval runner 漏掉了。

5. **更新治理文档**：`04_task_board.md`、`07_handoff.md`、`08_risks_and_open_questions.md` 同步更新。

### 2.3 文件变化汇总

| 文件 | 变化类型 | 内容概要 |
| --- | --- | --- |
| `docs/grouped_retrieval_protocol.md` | 新增 | grouped retrieval 协议的完整冻结文档 |
| `docs/06_eval_protocol.md` | 修改 | 状态升级 + 新增 Section 3.1（代码入口与字段映射） |
| `run_relation_grouped_retrieval_baseline.py` | 修改 | 补齐 `grouped_test_ndcg_at_10` 输出字段（1 行） |
| `docs/04_task_board.md` | 修改 | 2 条 Execution Note |
| `docs/07_handoff.md` | 修改 | 2 条状态更新 + legacy 键提醒 |
| `docs/08_risks_and_open_questions.md` | 修改 | R02 描述更新 + Open Question #10（legacy 键重命名问题） |

### 2.4 代码修正的细节

这个修正非常精确，值得一说：

- **问题**：`run_relation_grouped_retrieval_baseline.py` 在构建 `result_summary.json` 时，遗漏了 `grouped_test_ndcg_at_10` 字段。
- **证据**：
  - `run_relation_gcn_baseline.py:385` 已经输出这个字段
  - `run_relation_hyperbolic_baseline.py:501` 已经输出这个字段
  - `_patch_sweep_reports.py:106` 已经在汇总表里引用这个字段
  - `run_relation_seed_sweep.py:191` 已经在 sweep 中收集这个字段
  - `relation_baseline_common.py:307` 已经计算 `ndcg_at_10`
- **修正**：只加了一行，跟相邻行的模式完全一致
- **风险**：零风险——只是把已有的中间计算结果暴露到 summary 里，不影响任何训练或推理逻辑

### 2.5 对后续开发的意义

T12 完成后，Milestone 1 只剩 T13（hop bucket 报告入口收口）。协议冻结的意义在于：

- **T20+（诊断与候选图筛选）**：后续的诊断实验可以直接引用 `docs/grouped_retrieval_protocol.md` 中的冻结指标集，不需要每次重新讨论"我们到底报哪些指标"。
- **T30+（训练对齐）**：训练代码改造时可以对照 Section 3 的配置字段列表，确保新的训练 loss 仍然输出标准字段格式。
- **T40+（provenance split）**：三类 provenance 图的 seed sweep 可以直接复用已经对齐的 sweep/report 代码。
- **论文写作**：论文的实验部分可以直接引用冻结协议作为方法论的 formal definition，不用把代码细节搬进论文。

## 3. 为什么给出 PASS 的 review 结果？

### 审查过程（adversarial review）

由于 T12 涉及评测协议和指标定义变更，按照 `CLAUDE.md` 和 `docs/08_risks_and_open_questions.md` 的规则，这次使用 **adversarial review**（对抗性审查）。这意味着我做了比普通审查更深入的验证：

1. **代码修正的正确性**：我验证了 `ndcg_at_10` 确实由上游 `relation_baseline_common.py:307` 计算，确认了另外两个 runner 已经在输出这个字段，确认了下游 sweep/report 代码已经在消费它。这证明了修正确实是"补齐遗漏"而不是"新增行为"。

2. **协议文档的准确性**：我抽查了协议文档中引用的全部 6 个代码文件路径和 2 个配置文件路径，全部在磁盘上实际存在。

3. **指标定义的一致性**：协议文档中的冻结指标集与 `result_summary.json` 的标准输出键一一对应，没有遗漏或多余。

4. **范围合规**：`git status` 确认只有 allowed files 被修改。代码改动只有 1 行。没有模型架构变更、没有删除旧结果、没有新增无关任务。

5. **文档诚实性**：两个协议文档都标注为 draft 状态，明确说明 reviewer 通过前不作为最终收口。legacy 键的兼容性问题被如实记录为 Open Question #10。

### 判决理由

- 所有 deliverables 齐备且质量合格。
- 唯一的代码修正是经过验证的最小对齐操作，不引入任何风险。
- 协议文档与实际代码完全吻合，没有"纸上谈兵"的问题。
- adversarial review 没有发现任何指标定义漂移、silent metric substitution 或 evaluation scope expansion 的问题。

因此判定为 **PASS**，无 blocking 或 non-blocking issues。
