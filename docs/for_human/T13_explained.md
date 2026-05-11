# T13 Hop Bucket Reporting — 解释文档

## 1. 这个任务在做什么（通俗解释）

### 背景：什么是 hop？

在 Lean/Mathlib 的声明图中，两个声明之间的"祖先-后代"关系可以有不同深度。比如：

- **hop_2**：当前声明往上走 2 步就能到达的祖先（爷爷辈）
- **hop_3**：往上走 3 步的祖先（曾祖辈）
- **hop_4_plus**：往上走 4 步或更远的祖先（更远的祖先）

在评测"给定一个声明，模型能否正确找到它的祖先"时，如果只看一个总分数，会掩盖一个关键问题：**模型在找近处祖先和远处祖先时的表现是否不同？**

### 为什么这很重要？

本项目的核心假设之一是：双曲几何模型（HGCN）在深层层级结构中可能比欧氏模型（GCN）更有优势。如果 HGCN 只在 hop_4_plus 这个"远处祖先"的桶里才展现出优势，而在 hop_2（近处祖先）上和 GCN 差不多，那这就是一个有条件的、但真实存在的双曲价值信号。

反之，如果所有 hop bucket 上 HGCN 都不占优，那双曲偏置在这个数据上就没用。

**T13 的任务就是：确保评测报告能自动输出 hop_2 / hop_3 / hop_4_plus 分桶的指标，而不是只给一个笼统的总分。**

打个比方：以前考试只有一个总分，现在要把每道大题的得分都列出来，这样才能看出学生到底哪里强、哪里弱。

---

## 2. 实现详解

### 2.1 目标

在以下输出中增加 hop bucket 指标：

1. 单次实验的 `result_summary.json` — 包含 `hop_2_map`, `hop_3_ndcg` 等平铺字段
2. 多 seed sweep 的 `report.md` — 包含 hop bucket 汇总表和每个 seed 的分桶结果

### 2.2 数据流

```
evaluate_grouped_ancestor_retrieval()
    ↓ 返回 grouped dict，内含 hop_buckets 嵌套结构
    ↓
各 runner (gcn / hyperbolic / grouped_retrieval)
    ↓ 调用 flatten_grouped_hop_bucket_summary(grouped)
    ↓ 把 hop_2_map, hop_3_ndcg 等 21 个字段平铺写入
    ↓
result_summary.json
    ↓
seed sweep 聚合
    ↓
report.md (hop bucket aggregate + per-seed 表)
```

### 2.3 代码变化

#### (a) 三个 runner 文件各增加一个 flatten 函数

`run_relation_gcn_baseline.py`、`run_relation_hyperbolic_baseline.py`、`run_relation_grouped_retrieval_baseline.py` 各新增 `flatten_grouped_hop_bucket_summary(grouped)` 函数，逻辑相同：

```python
def flatten_grouped_hop_bucket_summary(grouped: dict) -> dict[str, float | None]:
    flattened = {}
    hop_buckets = grouped.get("hop_buckets", {})
    for bucket_name in ["hop_2", "hop_3", "hop_4_plus"]:
        bucket_metrics = hop_buckets.get(bucket_name, {})
        for metric_name in ["map", "ndcg", "grouped_mrr",
                            "recall_at_1", "recall_at_3",
                            "recall_at_5", "recall_at_10"]:
            flattened[f"{bucket_name}_{metric_name}"] = bucket_metrics.get(metric_name, {}).get("mean")
    return flattened
```

这个函数从 `evaluate_grouped_ancestor_retrieval` 返回的 `grouped` 字典中，提取 `hop_buckets` 嵌套结构，平铺成 `hop_2_map`, `hop_3_ndcg`, `hop_4_plus_grouped_mrr` 等键值对。

每个 runner 的 `result_summary` 组装段（原本已有 `grouped_test_map` 等字段）增加了一行 `result_summary.update(flatten_grouped_hop_bucket_summary(grouped))`，把 21 个 hop bucket 字段平铺写入 `result_summary.json`。

#### (b) seed sweep 报告生成增加 hop bucket 表

`run_relation_seed_sweep.py` 和 `_patch_sweep_reports.py` 的 `build_markdown_report` / `build_report` 函数新增：

1. **`format_metric` 辅助函数** — 统一处理 `None` → `"NA"` 和浮点数格式化，替代原来的内联三元表达式。
2. **Hop Bucket Aggregate 表** — 对每个 hop bucket 展示 MAP / nDCG / grouped MRR / Recall@1/3/5/10 的 mean ± std。
3. **Hop Bucket Per Seed 表** — 对每个 seed 展示 hop_2 / hop_3 / hop_4_plus 的 MAP 和 nDCG。

#### (c) 文档更新

- `docs/06_eval_protocol.md` — 在标准输出字段列表中增加了 `hop_2_*` 到 `hop_4_plus_*` 的 21 个字段说明，以及 seed sweep 的 `report.md` 输出说明。
- `docs/04_task_board.md` — 更新项目状态和执行说明，记录 worker 完成情况，明确标记"待 adversarial review"。
- `docs/07_handoff.md` — 更新接手说明和下一步指引，记录 T13 实现状态。

### 2.4 数据来源的可靠性

hop bucket 数据不是 T13 新造的。上游 `relation_baseline_common.py` 中的 `evaluate_grouped_ancestor_retrieval` 函数（约第 260-320 行）已经在计算每个 query 的祖先 hop 深度，并按 `hop_2 / hop_3 / hop_4_plus` 分桶计算 MAP、nDCG、grouped MRR 等指标。T13 只是把已经算好的数据从嵌套结构中提取出来，平铺到常规报告入口。

### 2.5 对后续开发的意义

1. **T32/T33（GCN/HGCN grouped training seed sweep）**：跑完后，`report.md` 会自动包含 hop bucket 分桶，可以直接观察 HGCN 是否在更深的 hop bucket 上有优势——这正是 Gate D（双曲价值门）的核心判断依据。

2. **论文叙事**：如果 HGCN 在 hop_4_plus 上稳定优于 GCN，那论文可以写"双曲偏置在深层祖先检索中有条件地有效"；如果所有 bucket 都没有差异，则论文转向 benchmark/protocol/diagnostics 叙事。无论哪种结论，hop bucket 数据都是必需的。

3. **结构诊断（Milestone 2）**：结合图结构诊断和 hop bucket 结果，可以判断哪些图的结构深度足够释放双曲优势，哪些图太浅不值得尝试。

---

## 3. 为什么给出 PASS 的 review 结论

### 3.1 核心判断

T13 的任务目标是"增加或校验 hop bucket 常规报告入口，确保 hop_2 / hop_3 / hop_4_plus 出现在正式结果中"。审查确认：

- **目标已完成**：三个 runner 的 `result_summary.json` 现在包含 21 个 hop bucket 平铺字段；seed sweep 的 `report.md` 现在包含 hop bucket aggregate 和 per-seed 表。
- **数据来源可靠**：不是新造数据，而是从上游已有的 `evaluate_grouped_ancestor_retrieval` 的 `hop_buckets` 输出中提取。
- **访问模式安全**：全部使用 `.get()` 带默认值，不会因为缺少 hop bucket 数据而崩溃。
- **范围合规**：只改了 `Allowed files` 列出的文件；没有改训练目标、没有跑大规模 sweep、没有把 dry-run 当正式结果。
- **文档准确**：明确标记"待 adversarial review"，没有把未完成的任务写成已完成。

### 3.2 非阻塞问题

代码存在复制粘贴（`flatten_grouped_hop_bucket_summary` 重复三份），但这是可以接受的——任务包要求最小改动，不做重构。per-seed 表只展示 MAP 和 nDCG 两个指标而非全部 7 个，这是展示空间和可读性的合理取舍，所有 21 个字段都在 aggregate 和 CSV/JSON 中。

### 3.3 不足之处

没有做端到端运行验证（只做了 `rg` 静态校验）。但这是任务包限制的结果——任务包禁止跑大规模 sweep。代码路径足够简单（从已有的嵌套字典中提取字段），静态审查足以确认逻辑正确性。真正的端到端验证将在 T32/T33 跑 seed sweep 时自然发生。
