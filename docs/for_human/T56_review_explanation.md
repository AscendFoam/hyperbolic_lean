# T56 Review Explanation (面向人类读者)

## 1. 这个任务在做什么？（通俗解释）

这个项目的研究人员构建了一套实验管线，用来分析"在形式化数学的层级图中，双曲图神经网络（HGCN）是否比普通图神经网络（GCN）更有效"。他们已经在两组数学模块（Field.Subfield 和 Order.Ring）上跑完了所有实验，得出了一个核心发现：

> HGCN 只在"纯继承边"（explicit_only）的图上有优势，而在包含合成边的完整图上 GCN 仍然更强。

但论文发表之前，还有两个文档层面的精度问题需要清理：

- **R29**：实验报告里有一张表格，Field.Subfield 模块的 GCN 结果那一格，不小心把 HGCN 的数值（0.6857）复制粘贴到了 GCN 的格子里。这是一个纯文档错误。
- **R28**：之前有人注意到报告里写的"汇总均值为 1.0，但某些种子的值低于 1.0"，怀疑可能是数据计算管线出了 bug。这个问题悬而未决，阻碍了论文对外发表。

T56 的任务就是：**不跑任何新实验**，仅通过重新检查已有的实验数据文件，把这两个精度问题搞清楚并修正文档。

## 2. 任务的实现细节

### 2.1 任务目标

1. 修正 R29 的表格单元格复制粘贴错误
2. 搞清楚 R28 的"汇总 vs 单种子差异"到底是怎么回事
3. 把修正结果同步到论文草稿和所有治理文档中

### 2.2 Worker 做了什么

#### R29 修正

Worker 直接回到 T42 阶段的真实实验产物目录（`artifacts/baselines/relation_seed_sweeps/provenance_gcn_field_subfield_synthesized_only_t42/`），读取了其中的 `aggregate.json` 文件，确认：

- GCN 的 `grouped_test_map`（分组检索的 MAP 指标）= 1.0（满分），5 个种子的标准差 = 0.0
- 这与之前表格里写的 0.6857（那是 HGCN 的值）完全不同

于是把 `provenance_summary.md` Section 5.1 的表格从：

| Field.Subfield | 0.6857 ± 0.1140* | 0.6857 ± 0.1140 | — |

修正为：

| Field.Subfield | 1.0000 ± 0.0000 | 0.6857 ± 0.1140 | GCN +0.3143 |

#### R28 解析

这是本次任务最有技术含量的部分。Worker 读取了 T42 产物的三个输出文件：

1. `aggregate.json`：汇总统计
2. `per_seed_results.json`：每个种子的详细指标
3. `per_seed_results.csv`：CSV 格式的种子级别数据

然后发现了关键事实：

| 指标名 | seed 7 | seed 42 | seed 123 | seed 2026 | seed 3407 | 汇总均值 |
|---|---|---|---|---|---|---|
| `grouped_test_map` | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| `test_average_precision` | 1.0 | 1.0 | 0.81 | 0.9029 | 1.0 | 0.9426 |

原始 T43 报告中说的 "seed 123 MAP = 0.8100, seed 2026 MAP = 0.9029" —— 这些数字是对的，但它们是 `test_average_precision`（sklearn 的逐查询平均精度），不是 `grouped_test_map`（分组检索 MAP）。

**两个指标计算方式不同、语义不同、结果不同，但各自都是正确的。** 所谓的"差异"其实是在比较两个不同指标的数值，自然不一样。这就像拿身高和体重比——数字不同不代表秤坏了。

#### Paper draft 同步

`paper_draft.md` 的多处被更新：

- Section 5.4 表格补入了 Field.Subfield 的已验证行
- Section 5.4 解释段落从 "为什么不呈现 Field.Subfield" 改为 "为什么 GCN MAP = 1.0000 并不意外"
- Section 5.7 汇总表更新
- Section 7.1.5/7.1.6 局限性段落更新
- Numeric Anchors 附录新增 4 行 synthesized_only 数值

#### 治理文档同步

8 份治理文档全部更新了时间戳和 T56 状态。`08_risks_and_open_questions.md` 中 R28 和 R29 从 Active 改为 Resolved，D18 关闭。`05_decision_log.md` 新增 D040。

### 2.3 变更范围

- 修改了 10 个文件，全部在 Allowed Files 列表内
- 没有修改任何代码、配置、实验产物或数据处理脚本
- 没有运行新实验
- provenance-conditional 主结论保持不变

### 2.4 对后续开发的意义

R28/R29 的关闭意味着：

1. **后续图表渲染可以安全使用这些数值**——不再有悬置的精度边界
2. **论文的 Numeric Anchors 附录现在是完整的**——所有 six synthesized_only 数值行都已填入
3. **项目的核心结论更稳固**——R28 不是数据 bug，而是 metric 命名混淆，控制诊断结论不受影响
4. 后续任务可以直接进入 figure/table rendering 和 artifact packaging，不需要再回头处理精度问题

## 3. 为什么我给出了 PASS 的 review 结果？

### 核心判断依据

**1. R29 修正经过独立验证，确实正确。**

我直接读取了 T42 artifact 的 `aggregate.json`，确认 `grouped_test_map` 的 mean = 1.0, std = 0.0。修正后的表格值与 artifact 完全一致。

**2. R28 的根因解析经过独立验证，确实正确。**

我直接读取了三个产物文件（aggregate.json、per_seed_results.json、per_seed_results.csv），确认 `grouped_test_map` 在所有 5 个种子中均为 1.0，而 `test_average_precision` 确实在 seed 123 和 seed 2026 上低于 1.0。原始报告中的 0.8100 和 0.9029 确实是 `test_average_precision` 的值，不是 `grouped_test_map`。Worker 的诊断完全正确。

**3. 文件范围严格遵守任务包的 Allowed Files。**

`git diff` 确认恰好修改了 10 个文件，全部在 Allowed Files 列表内。没有触及 Forbidden scope 中的任何内容（代码、产物、02_experiment_plan.md、paper_outline.md 等）。

**4. 没有伪实现、mock、stub 或 hardcode。**

所有修改都是基于真实 T42 artifact 数值的文档修正，没有引入任何未经审核的新数值。

**5. provenance-conditional 主结论未被移动。**

HGCN 在 explicit_only 上领先、GCN 在 hierarchy_mixed 和 synthesized_only 上领先的核心结论完全保持不变。修正只是让数值引用更精确。

### 非阻塞问题

我标注了 3 个非阻塞问题（详见 review），包括汇总表呈现粒度不一致、解释段篇幅较长、以及 R28 关闭条件满足性未显式标注。这些都不影响任务完成的正确性，可在后续轮次中自然处理。

## 4. Worker 是否已写了 review 和 explanation 文档？

Worker 未写 `docs/review/T56_review.md` 和 `docs/for_human/T56_review_explanation.md`——这是正确的行为，因为 Worker 的职责是执行任务并报告结果，review 和 explanation 是 Reviewer 的职责。本文档即为 Reviewer 产出的 review explanation。
