# T34 通俗解释：Grouped Training 汇总报告

## 一、这个任务在做什么？（通俗版）

这个项目在研究一个核心问题：**在 Lean 形式化数学库的层级结构图上，双曲神经网络（HGCN）到底能不能比普通欧氏神经网络（GCN）表现更好？**

要回答这个问题，项目经历了几个阶段：

1. 最早用的是一种叫 "binary edge classification"（二分类边训练）的方法来训练模型——让模型判断"两个数学对象之间有没有继承关系"。
2. 后来发现这种训练方式和实际评测不匹配——评测看的是"同一个查询下多个祖先的排序质量"，而训练只是在做简单的"有/无边"判断。
3. 于是项目把训练方式升级为 "grouped retrieval training"（分组检索训练）——让训练目标直接对齐评测任务。
4. 在升级后的新训练方式下，项目分别在 `Field.Subfield`（域/子域）和 `Order.Ring`（序/环）两组数学层级图上，用 5 个随机种子跑了 GCN 和 HGCN 的对比实验（这就是 T32 和 T33）。

**T34 做的事情很简单：** 把升级前后的差异、GCN 和 HGCN 的配置差异、以及最终的对比结果汇总成一份正式的诊断报告。不跑新实验，只做总结。

## 二、任务目标、流程和代码变化

### 任务目标

T34 的目标是产出 `docs/experiment_reports/grouped_training_summary.md`，必须包含：

1. **可比性声明**：明确说清楚 T32 和 T33 只能在 matched grouped protocol（匹配的分组协议）下直接比较，不能和历史 binary 训练的绝对数值混在一起比。
2. **协议差异表**：对比旧 binary 训练和新 grouped 训练在训练单元、损失函数、切分方式等方面的关键区别。
3. **GCN vs HGCN 配置差异表**：逐字段列出 T32 和 T33 的 config 文件中，哪些字段不同。
4. **结果汇总**：覆盖两组图的主指标和 hop bucket 分析。
5. **结论分级**：把结论分成 accepted（已确认）、inconclusive（不确定）、deferred（推迟到后续）三类。

### 任务流程

1. Worker 阅读了 T32 和 T33 的实验报告、review 文档、以及历史 binary 训练阶段的汇总文档。
2. Worker 基于这些已有材料，撰写了 `grouped_training_summary.md`。
3. Worker 同步更新了四个治理文档（任务板、决策日志、交接文档、风险文档）中与 T34 相关的 worker draft 记录。
4. Worker 运行了任务包指定的验证命令，确认关键词全部命中。

### 代码/配置变化

**没有代码变化。** T34 是一个纯文档任务。

**没有配置变化。** 没有新增或修改任何训练配置文件。

**文档变化：**

| 文件 | 变化 |
| --- | --- |
| `docs/experiment_reports/grouped_training_summary.md` | 新增，T34 的主要产出物 |
| `docs/04_task_board.md` | 更新 T32/T33 为已完成，T34 设为当前任务，补充执行记录和 T33/T34 completion note |
| `docs/05_decision_log.md` | 新增 D022（T32 review 通过）、D023（T33 review 通过）、D024（T34 worker draft 结论收窄） |
| `docs/07_handoff.md` | 更新当前任务为 T34，补充 T32/T33 key metrics 和状态更新 |
| `docs/08_risks_and_open_questions.md` | 更新 R07/R22 为 Mitigated，新增 R23/R24，更新 Open Question 4 和 D06/D15 |

### 对后续开发的意义

T34 是 **Milestone 3 的收口任务**。完成后：

- Milestone 3（Grouped Retrieval Training Alignment）正式闭合。
- 项目进入 Milestone 4（Relation Provenance Split），即比较 `explicit-only / synthesized-only / mixed` 三类关系图。
- T34 建立的"可比性边界"将成为后续所有实验报告的参照标准——任何读者如果看到这份汇总，就能清楚知道：
  - T32 和 T33 的数值可以互相比。
  - 历史 binary 数值不能和 T32/T33 直接比。
  - 当前结论是 GCN 仍然更强，不是"HGCN 在修正协议后赢了"。

## 三、为什么 review 给出了 PASS？

### Review 核心判断

1. **任务目标全部完成**：任务包要求的五个必要部分（可比性声明、协议差异、config diff 表、结果汇总、结论分级）在报告中都存在且内容正确。

2. **无 Forbidden scope 违规**：
   - 没有新跑实验（无 sweep artifact 变更）。
   - 没有修改 T32/T33 已收口结果（所有数值与 reviewed 报告逐字段一致）。
   - 没有修改训练代码或协议实现（源代码目录无变更）。
   - 没有修改 `docs/02_experiment_plan.md`。

3. **数值准确**：
   - GCN/HGCN grouped MAP、nDCG、nDCG@10 全部与 T32/T33 reviewed 报告匹配。
   - 历史 binary 数值（`0.144, 0.321, 0.104, 0.299, 0.208, 0.291, 0.148`）全部可追溯到 `docs/阶段总结（2026-05-02，grouped retrieval training）.md`。
   - Config diff 表中的 HGCN 特有字段与 T33 review 的逐字段验证一致。

4. **结论边界正确且审慎**：
   - 没有出现"HGCN 赢了"或"HGCN 在修正后有优势"的过度声称。
   - 明确区分了 matched grouped comparison（T32 vs T33）和跨协议历史对比。
   - 结论分级（accepted / inconclusive / deferred）使用合理，没有把不确定证据写成既成事实。

5. **无伪实现、mock、stub 或 hardcode**：这是一个 summary-only 文档任务，所有内容都来自已 reviewed 的实验报告和历史文档。

### Non-blocking Issues（不阻塞但值得后续改进）

1. `docs/05_decision_log.md` 中 D024 使用英文而非中文，与其他条目格式不一致。
2. 报告没有引用历史数值的具体文件来源。
3. 报告汇总表缺少 Recall@1/3/5/10 对比列。
4. 治理文档中新增的 Worker Draft Note 使用全英文。

这些都不影响结论正确性，可在后续文档精修中处理。
