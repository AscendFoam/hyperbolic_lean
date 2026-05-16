# T31A 通俗解释：Query-Level Split Completeness

## 一、这个任务在做什么？—— 通俗解释

### 背景：什么是 "split"？

在机器学习中，我们通常把数据分成三份：

- **训练集 (train)**：模型用来学习的数据
- **验证集 (val)**：训练过程中用来检查模型是否过拟合的数据
- **测试集 (test)**：最终评估模型真实能力的数据

这三份数据必须**互不重叠**，否则模型可能"偷看"了答案。

### 问题：旧 split 按"边"切，但评测按"查询"算

在这个项目中，核心任务是 **grouped ancestor retrieval**：给定一个声明（declaration）和一种关系（relation），找出它的所有祖先节点。

举个例子：

```
声明 A 通过 "instance_of" 关系可以到达祖先 B、C、D。
```

在 grouped retrieval 的评测中，`(A, instance_of)` 构成一个**查询（query）**，B、C、D 都是这个查询的**正例（positive）**。评测时，模型需要把 B、C、D 都排在候选列表的前面。

**旧的做法**是把每条边（A→B, A→C, A→D）独立地随机分到 train / val / test。这会导致什么问题？

```
A→B 分到了 train
A→C 分到了 val
A→D 分到了 test
```

这意味着在 val 评测时，模型只看到 A→C 是正例，但 A→B 和 A→D 被当成了"不是正例"（因为它们不在 val 里）。但实际上 B 和 D **也是 A 的祖先**！这会让评测结果失真——模型明明预测对了，但被扣分了。

### T31A 的修复：按"查询"切分

T31A 的核心改动是：**同一个查询下的所有边必须进入同一个 split。**

也就是说，如果 `(A, instance_of)` 这个查询被分到 val，那么 A→B、A→C、A→D 全部进 val，一条都不会跑到 train 或 test。

这保证了：val/test 的 grouped retrieval 评测拥有**完整的正例集合**，不会把真正的祖先误判为负例。

---

## 二、实现细节解释

### 2.1 任务目标

任务包 `T31A_query_level_split_completeness.md` 的目标：

1. 为 `ancestor_ranking` 任务实现 query-level split
2. 提供验证机制，证明同一 `(src, relation)` 查询不跨 split
3. 不影响其他任务（如 `parent_prediction`）
4. 不实现 grouped loss、不改模型架构

### 2.2 代码变化

#### (1) `relation_tasks.py` —— 新增 4 个函数

**`query_key_for_relation_example(example)`**

从一条正例边 `(src_id, dst_id, relation_type)` 提取查询键 `(src_id, relation_type)`。注意：这里的 `relation_type` 是经过 `ancestor_label_mode` 处理后的值（如 `extends_ancestor` / `instance_ancestor`），不是原始的 `extends` / `instance_of`。

**`stratified_split_relation_examples_by_query(...)`**

核心切分逻辑：

```
1. 按 relation_type 分桶（保证不同关系类型的比例在 split 间平衡）
2. 在每个桶内，按 (src, relation_type) 查询键分组
3. 随机打乱查询键
4. 按比例切分查询键（不是切分边）
5. 同一查询键下的所有边跟随进入同一 split
```

关键设计：切分单位是"查询"而不是"边"。一旦 `(A, instance_ancestor)` 这个查询被分到 train，它下面的所有边 A→B, A→C, A→D 全部进 train。

**`summarize_query_level_split(...)`**

生成切分摘要，包含：
- 每个 split 的查询数量
- 每个 split 的正例边数量
- 任意两个 split 之间的查询重叠数量
- `is_query_level_disjoint` 标志

**`assert_query_level_split_disjoint(...)`**

断言函数：如果发现查询重叠（某个查询同时出现在 train 和 val 中），立即抛出 `ValueError`。这不是软警告，是硬断言。

#### (2) `relation_baseline_common.py` —— 分支逻辑改动

`prepare_relation_run_data(...)` 函数的改动：

```python
if task_name == "ancestor_ranking":
    # 新路径：query-level split
    split = stratified_split_relation_examples_by_query(...)
    query_split_summary = assert_query_level_split_disjoint(split)
else:
    # 旧路径不变：edge-level split
    split = stratified_split_relation_examples(...)
    query_split_summary = None
```

然后把 `query_split_summary` 写入 `run_manifest.json` 的 `task_summary` 字段。

#### (3) 新增 smoke 配置

`relation_gcn_typeclass_precise_v2_ancestor_ranking_query_split_smoke_t31a.json` 与 T14 的 smoke config 几乎一致，只是 `run_id` 和 `artifacts_root` 指向新路径。这是一个最小配置（epochs=1, dim=8），不构成正式 benchmark。

### 2.3 验证结果

实际运行的 smoke 产出 `run_manifest.json` 中确认：

| 字段 | 值 |
|------|-----|
| split_strategy | query_level |
| train query count | 780 |
| val query count | 96 |
| test query count | 96 |
| train_val overlap | 0 |
| train_test overlap | 0 |
| val_test overlap | 0 |
| is_query_level_disjoint | true |

### 2.4 对后续开发的意义

1. **T31 可以安全推进 grouped loss。** T31 的核心是实现 query-grouped training objective（如 sampled softmax / InfoNCE）。在 query-level split 完成后，训练时可以确保同一查询的所有正例都在同一个 split 中，不会出现"训练集看到半个查询、测试集看到另半个"的情况。

2. **评测结果更可靠。** 之前 edge-level split 导致 grouped retrieval 的 val/test 指标可能低估模型实际能力（因为部分真正例被误判为负例）。修复后，评测指标更能反映真实排序质量。

3. **只影响 ancestor_ranking 路径。** 这是一个刻意收窄的设计：`parent_prediction` 等其他任务仍使用旧的 edge-level split，因为它们的评测语义不需要 grouped query。

4. **R19 风险可以降级。** T30 审计时发现的最高优先级前置风险（split mismatch）现在有了代码层面的修复和验证，后续可以把 R19 从 Active 降为 Mitigated。

---

## 三、为什么 review 结果是 PASS？

### 核心判断

任务包要求三件事：
1. 实现 query-level split —— 已完成
2. 提供验证证明不跨 split —— 已完成（硬断言 + smoke 产出）
3. 不越界 —— 严格限制在 ancestor_ranking 路径

三件事都做到了，代码实现干净、没有 mock 或 hardcode、与评测侧的 query 分组 key 一致。

### 具体审查点

**1. 是否真的完成了任务？**

是的。代码路径确实走了 `stratified_split_relation_examples_by_query`，而不是只在文档里声明。smoke 运行产物 `run_manifest.json` 直接证明 split_strategy = query_level 且所有 overlap = 0。

**2. 是否有伪实现 / mock / stub / hardcode？**

没有。4 个新函数都是真实实现，逻辑清晰，没有硬编码路径或假数据。

**3. 是否缺测试或验证？**

不缺。两层验证：`rg` 静态检查 + 实际 smoke 运行。`assert_query_level_split_disjoint` 是硬断言，如果 split 有问题会直接报错。

**4. 是否过度工程？**

没有。4 个函数各司其职，没有过度抽象。`summarize_query_level_split` 和 `assert_query_level_split_disjoint` 的分离是合理的——前者生成可序列化摘要，后者做运行时断言。

**5. 是否破坏已有功能？**

没有。改动只在 `task == "ancestor_ranking"` 分支生效，其他任务走 `else` 保持原逻辑不变。

**6. 文档是否把计划写成事实？**

没有。`training_alignment_audit.md` 的 4.1 节写的是 "T31A 已在代码路径上补入..."，这是对已完成代码的客观描述，不是计划。4.2 节的 "Post-Fix Interpretation" 明确标注了边界："这次修复没有把训练单位改成 query；那仍属于 T31"。风险表 R19 仍保留 Active 状态，等待 review 关闭后才降级。

### Non-blocking 注意事项

review 指出了 4 个非阻塞问题（详见 `docs/review/T31A_review.md`），其中最值得注意的是：`query_key_for_relation_example` 使用的 `relation_type` 是经过 `ancestor_label_mode` 处理后的值（`extends_ancestor` / `instance_ancestor`），不是原始 relation type。这在当前场景下是正确的（与评测侧的分组 key 一致），但 T31 worker 在实现 grouped loss 时应确保使用同样的 key 语义。
