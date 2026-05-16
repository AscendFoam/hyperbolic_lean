# T31 通俗解释：最小 Query-Grouped Loss

## 一、这个任务在做什么？—— 通俗解释

### 背景：训练目标和评测目标不一致

在 T30 的审计中，我们发现了一个核心问题：**模型训练的目标和实际评测的目标不一样。**

评测时，我们用的是 **grouped retrieval**：给定一个 `(src, relation)` 查询，模型需要把所有真祖先排在候选列表前面。好的结果意味着：同一查询下，真祖先们的排名比非祖先靠前。

但训练时，模型学的是 **逐边二分类**：对每条边 `(src, dst, relation)` 独立判断"这条边存不存在"。模型不知道哪些边属于同一个查询，也不需要在同一查询内把正例排到负例前面。

打个比方：

```
评测问的是："在 A 的所有 instance_ancestor 候选中，把真祖先 B、C、D 排到最前面"
训练学的却是："A→B 这条边是不是真的？A→C 这条边是不是真的？……"（逐条判断）
```

这两个目标有本质区别：评测关心的是**组内排序质量**，训练却只关心**逐条真假判断**。

### T31 做了什么？

T31 的核心改动是：**让训练目标也变成"同一查询内的排序"。**

具体来说：
1. 训练时，把同一个 `(src, relation)` 查询下的所有正例和负例放在一起
2. 对这个查询内的所有候选算分数
3. 用 **sampled softmax / InfoNCE** 作为损失函数——让正例的分数高于负例
4. 用 grouped val MAP（而不是旧的 binary val AP）来选择最佳模型

这样，训练目标就和评测目标对齐了：**都是"同一查询内，正例排名靠前"。**

### 为什么要在 T31A 之后做？

T31A 修复了数据切分问题（同一查询不被拆到不同 split）。如果先不改 split 就换 loss，训练时仍会出现"查询被拆碎"的情况。T31A 保证了数据基础，T31 才能在可靠的数据上改训练目标。

---

## 二、实现细节解释

### 2.1 任务目标

任务包 `T31_min_query_grouped_loss.md` 的目标：

1. 实现最小 query-grouped loss（优先 sampled softmax 或 InfoNCE）
2. 只接一个现有 config（grouped retrieval runner）
3. query 分组 key 必须与 T31A 的 split/eval 对齐
4. 不重写 GCN/HGCN 架构，不运行长 sweep

### 2.2 代码变化

#### (1) `run_relation_grouped_retrieval_baseline.py` —— 核心改动

这是 T31 的主要改动文件。Grouped retrieval runner 在 T12 就已经存在，但之前用的是临时 ad hoc 的查询构造方式。T31 的改动让它与 eval 和 split 共享同一套 key 语义。

**`build_query_groups(...)` 重写**

旧实现自己手动从 split CSV 中按 `(src, rel)` 聚合正例，构造查询组。新实现改为：

```python
grouped_queries = build_grouped_ranking_queries(positive_examples, candidate_pools)
```

直接复用 `build_grouped_ranking_queries(...)`——这个函数也是 eval 侧用来构造 grouped ranking queries 的同一个函数。这保证了训练和评测使用完全一致的查询分组逻辑。

**`_sample_negative_ids(...)` 新增**

抽取为独立 helper，负例采样逻辑更清晰：
- 从候选池中排除自身和所有已知正例
- 按 `negative_ratio` 采样指定数量的负例
- 如果候选不够则全部返回

**`sampled_softmax_loss(...)` 替换 `grouped_softmax_loss(...)`**

```python
def sampled_softmax_loss(scores, positive_mask, torch, F):
    log_probs = F.log_softmax(scores, dim=0)
    pos_log_probs = log_probs[positive_mask]
    if pos_log_probs.numel() == 0:
        return scores.new_zeros(())
    return -pos_log_probs.mean()
```

这是标准的 InfoNCE / sampled-softmax 损失：对一个查询内的所有候选做 softmax，然后最大化正例的对数概率。

**模型选择改为 grouped val MAP**

旧实现用 binary val AP 选择最佳 checkpoint。新实现改为：

```python
current_metric = val_grouped_map if val_grouped_map is not None else float("-inf")
if current_metric > best_val_grouped_map:
    best_val_grouped_map = current_metric
    best_epoch = epoch
    best_state = ...
```

现在 best checkpoint 由 grouped val MAP 决定，不再是 binary AP。这直接修复了 T30 审计中的 M5 错配。

**`summarize_query_groups(...)` 新增**

记录训练查询的统计摘要，写入 `grouped_training_summary.json`：
- `query_key_fields = ["src_id", "relation_type"]`——明确声明 key 语义
- 每个 relation type 的查询数
- 每个查询的正例/负例/候选池大小统计

**`grouped_loss_name` 参数化**

支持 `"sampled_softmax"` 和 `"infonce"` 两种配置名（当前指向同一实现），以及旧名 `"grouped_softmax"` 自动映射到 `"sampled_softmax"`。

#### (2) `relation_tasks.py` 和 `relation_baseline_common.py` —— T31A 遗留改动

这两个文件的改动是 T31A 的 query-level split 实现（上一轮已 review），T31 没有额外修改它们。

#### (3) 新增 smoke 配置

`relation_grouped_gcn_typeclass_precise_v2_ancestor_ranking_smoke_t31.json`：

```json
{
  "model_type": "gcn",
  "grouped_loss": "sampled_softmax",
  "negative_ratio": 1.0,
  "resample_negatives_every_epoch": false,
  "epochs": 1,
  ...
}
```

与 T14/T31A 的 smoke config 类似，但走的是 grouped retrieval runner 路径。`epochs=1` 意味着只跑一个 epoch，用于验证链路，不是正式 benchmark。

### 2.3 验证结果

Smoke 产出确认：

| 文件 | 关键字段 | 值 |
|------|---------|-----|
| `grouped_training_summary.json` | `query_key_fields` | `["src_id", "relation_type"]` |
| `grouped_training_summary.json` | `num_queries` | 780 |
| `grouped_training_summary.json` | `relation_type_counts` | `extends_ancestor: 11, instance_ancestor: 769` |
| `training_stats.json` | `training_loss` | `"sampled_softmax"` |
| `training_stats.json` | `best_val_grouped_map` | 0.203 |
| `result_summary.json` | `task_summary.query_split_summary.is_query_level_disjoint` | `true` |
| `result_summary.json` | `grouped_test_map` | 0.095 |

关键观察：训练查询数 (780) 与 T31A smoke 的 train query count (780) 完全一致，确认 query key 对齐。

### 2.4 对后续开发的意义

1. **T32 可以直接用 grouped runner 做 seed sweep。** T31 验证了 grouped retrieval runner 的完整链路：数据准备 -> query-level split -> grouped training -> grouped eval -> 结果落盘。T32 只需要换更大的图和更多 epoch。

2. **训练/评测错配的核心修复。** T30 审计列出了 M1-M5 五个错配点。T31A 修复了 M3 (split)，T31 修复了 M1 (loss) 和 M5 (model selection)。剩余的 M2 (query unit mismatch in BCE runners) 和 M4 (negative sampling mismatch) 属于旧 BCE runner 的边界问题，不影响 grouped runner 路径。

3. **Grouped runner 与旧 BCE runner 并存。** 这是一个有意的设计：旧 `run_relation_gcn_baseline.py` 仍然跑 BCE 训练，新 `run_relation_grouped_retrieval_baseline.py` 跑 grouped 训练。两条路径的对比结果将在 T34 汇总。

4. **模型选择的实际影响。** 旧 BCE runner 用 binary val AP 选模型，新 grouped runner 用 grouped val MAP 选模型。在 T32/T33 的 seed sweep 中，这两种选择策略的差异将成为一个重要的分析维度。

---

## 三、为什么 review 结果是 PASS？

### 核心判断

任务包要求四件事：
1. 实现最小 query-grouped loss —— 已完成（sampled softmax / InfoNCE）
2. 只接一个现有 config —— 已完成（grouped retrieval runner + GCN smoke config）
3. query key 与 T31A split/eval 一致 —— 已验证（三者共用 `build_grouped_ranking_queries` 的 `(src_id, relation_type)` key）
4. 不越界 —— 严格限制在 grouped runner 路径，没改 BCE runner 或模型架构

四件事都做到了。

### 具体审查点

**1. 是否真的完成了任务？**

是的。代码层面：
- 训练 query 构造改用 `build_grouped_ranking_queries`，与 eval 共享 key 语义
- Loss 从 BCE 改为 sampled softmax / InfoNCE
- Model selection 从 binary val AP 改为 grouped val MAP
- Smoke 成功运行并产出完整 artifact

**2. 是否有伪实现 / mock / stub / hardcode？**

没有。`sampled_softmax_loss` 是真实的 log-softmax 实现。`_sample_negative_ids` 从实际候选池采样。没有 hardcode 的数据路径或假损失值。

**3. 是否缺测试或验证？**

不缺。两层验证：`rg` 静态检查 + 实际 smoke 运行。三个产物文件都确认了 `training_loss`、`query_key_fields` 和 `query_split_summary` 的正确性。

**4. 是否过度工程？**

没有。改动集中在 `run_relation_grouped_retrieval_baseline.py`，没有引入新的抽象层或复杂的配置系统。`summarize_query_groups` 是轻量统计函数。`grouped_loss_name` 参数化只是两行兼容映射。

**5. 是否破坏已有功能？**

没有。`run_relation_gcn_baseline.py` 和 `run_relation_hyperbolic_baseline.py` 没有任何 diff。旧的 BCE 路径完全不受影响。

**6. 文档是否把计划写成事实？**

没有。`training_alignment_audit.md` 的 5.1 节写的是 "Worker Draft Status"，不是已完成结论。`08_risks_and_open_questions.md` 的 R07 仍保留 Active 状态（只是更新了描述），明确标注 "仍待 adversarial review"。handoff 指出 "当前不要切到 T32"。

### Non-blocking 注意事项

review 指出了 5 个非阻塞问题（详见 `docs/review/T31_review.md`），最值得注意的是：

1. `grouped_loss="infonce"` 当前与 `"sampled_softmax"` 是同一个实现，只是配置名不同。如果未来需要真正的 contrastive variant，需要增加实现。
2. runner 的 `negative_ratio` 默认值 (10.0) 与旧 runner (1.0) 和 smoke config (1.0) 不同，未来用户如果省略这个字段可能会得到意外行为。
3. `docs/00, 01, 03, 05, 06` 有修改但这些是 Captain 级别的 T31A review 后更新，不是 T31 worker 的越界修改。
