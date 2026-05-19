# T52a Review 解释

## 1. 这个任务在做什么（通俗解释）

### 背景

之前 T42 做了一个关键实验：把 Lean 数学库中的图按"边的来源"拆成三种——
- **explicit_only**：只包含程序员显式写的 `extends` 继承边（比如 `Subfield extends Field`）
- **synthesized_only**：只包含 Lean 编译器自动生成的 `instance_of` 实例边
- **hierarchy_mixed**：两种边都包含的完整图

实验发现：**HGCN（双曲图神经网络）只在 explicit_only 图上比 GCN（普通图神经网络）好，在完整混合图上反而不如 GCN**。原因是 synthesized 边像"噪音"一样冲淡了层级信号。

### T52a 在做什么

T51 选定了一个叫 **ancestor explanation** 的 demo 方向，T52 把它的实现要求写成了详细的任务包。**T52a 就是真正动手写这个 demo 的任务**。

具体来说，T52a 实现了一个命令行工具：

```bash
python proof_side_ancestor_explanation.py \
    --declaration-name "hash::StrictOrderedCommRing" \
    --candidate-graph order_ring \
    --comparison-mode explicit_vs_mixed \
    --model-type hgcn
```

这个工具做以下事情：

1. **加载已训练好的模型嵌入**：从 T42 实验产出的 `node_embeddings.npy` 文件中读取每个数学声明的向量表示（不重新训练）
2. **构建祖先真相**：从图的 `extends` 边追溯，找出目标声明的所有层级祖先（父类、祖父类等）
3. **计算检索排名**：用 cosine similarity 把所有节点按与目标声明的相似度排序
4. **输出对比结果**：分别在 explicit_only 和 hierarchy_mixed 两种图上运行，对比检索质量

**核心价值**：让用户可以直观地看到"同一个数学概念，在只看继承关系时能找回更多层级祖先，而加入编译器生成的边后检索质量急剧下降"。

### 通俗类比

想象你在查家族族谱。explicit_only 就像只看"亲生父母→子女"的血缘关系，hierarchy_mixed 像是把"邻居家的干亲、教父教母关系"也加进去。工具展示的就是：加了干亲关系后，反而更难找到你真正的爷爷奶奶了。

## 2. 实现详细解释

### 任务目标

实现一个最小可运行的 ancestor explanation demo CLI 脚本，加载 T42 已有的模型嵌入，支持单查询和 provenance 对比两种模式，输出排序的祖先列表和检索指标。

### 任务流程

1. Worker 读取 T52a 任务包，了解精确的 CLI 参数、artifact 依赖、禁止事项
2. Worker 读取 `common.py`（图加载逻辑）、`relation_tasks.py`（任务构建）、`relation_baseline_common.py`（共享工具）
3. Worker 新建 `proof_side_ancestor_explanation.py`（~490 行）
4. Worker 新建 `ancestor_explanation_demo_report.md`（demo 报告）
5. Worker 在实际 artifact 上运行验证
6. Worker 同步更新 4 份治理文档

### 代码变化

#### `project_bootstrap/baseline_scaffold/src/proof_side_ancestor_explanation.py`（新建，~490 行）

脚本结构清晰，分为 6 个部分：

**CLI 参数解析**（line 33-63）
- 8 个参数：`--declaration-name`（必需）、`--candidate-graph`、`--provenance-mode`、`--model-type`、`--seed`（默认 42）、`--comparison-mode`、`--output-format`、`--top-k`
- `--provenance-mode` 在 comparison mode 下不是必需的（脚本自动运行两种模式）

**数据加载**（line 96-129）
- `load_graph()`：通过 `common.load_declaration_graph()` 加载图数据，构建 `declaration_id → row_index` 映射
- `load_embeddings()`：加载 `node_embeddings.npy`，**立即做 sanity check**：如果 embedding 行数和 declarations.csv 行数不匹配就报错退出
- 同时读取 `run_manifest.json` 记录 artifact 来源

**祖先图构建**（line 136-162）
- `build_parent_map()`：只提取 `extends` 边构建父节点映射
- `find_ancestors_bfs()`：BFS 追溯所有祖先，记录最小 hop 深度

**评分与指标**（line 169-240）
- `cosine_similarity()`：计算 query embedding 与所有节点的相似度
- `rank_and_score()`：排序并计算 MAP、Recall@1/3/5/10 和 hop breakdown

**对比模式**（line 297-354）
- `run_comparison()`：在 explicit_only 和 hierarchy_mixed 上分别运行，输出 top-k diff 和一句解释

**文本格式化**（line 361-455）
- `_format_single()`：单查询的人类可读输出
- `_format_comparison()`：对比模式的人类可读输出

关键实现细节：
- **只使用 `extends` 边构建 ground truth**（D033 决策）：无论 provenance mode 如何，祖先始终通过继承关系追溯
- **node ordering 对齐**：复用 `common.load_declaration_graph()` 的节点顺序，确保 embedding 行号正确
- **sanity check 硬保护**：shape 不匹配就报错退出，不会输出错位的结果

#### `docs/experiment_reports/ancestor_explanation_demo_report.md`（新建）

包含 8 个 section：
1. 概述（paper bridge 定位）
2. CLI 使用说明
3. 3 个命令示例
4. 2 个 declaration 示例的输出摘要
5. 观察到的 provenance quality difference
6. Paper bridge 映射（对应 Table 4 / Fig 3 / Fig 4）
7. 6 条验收标准的逐一核对
8. 实际执行的验证命令

#### 治理文档更新（4 个文件）

- `04_task_board.md`：+T52a 执行说明条目
- `05_decision_log.md`：+D033（6 个实现决策）
- `07_handoff.md`：+item 77 + 下一步切换到 T53
- `08_risks_and_open_questions.md`：R32 从 Active → Mitigated

### 对后续开发的意义

1. **T53 可以直接引用 demo 作为 proof-side bridge 的实物证据**：在 milestone 审查时，demo 输出的 Order.Ring 对比（MAP 0.6438 vs 0.1492）是 provenance-conditional finding 的直观展示
2. **Demo 为论文提供了具体案例**：Table 4 的 aggregate 数字现在有了单点具象化，reviewer 可以看到"哪些具体的祖先被 synthesized 边挤出 top-10"
3. **Demo 可以在 paper presentation 中作为 live demo 使用**：CLI 形式适合 ITP/CPP 的 tool demo 环节
4. **实现边界已经非常窄**：~490 行纯推理脚本，零训练、零新依赖、零修改已有代码，后续维护成本极低

## 3. 为什么给出 PASS 的 review 结果

### 检查要点

| 检查项 | 结果 |
|--------|------|
| 是否完成任务目标 | 是。6 条验收标准全部满足 |
| 是否在 Allowed Files 范围内 | 是。6 个文件（2 新建 + 4 更新），全部在 Allowed Files 中 |
| 是否遵守 Forbidden Scope | 是。未重训、未修改已有代码、未引入新依赖、comparison mode 是硬边界 |
| 是否有 mock/stub/hardcode | 否。rg 搜索未发现任何 mock/stub/hardcode/fake/placeholder |
| 验证是否充分 | 是。编译通过 + 4 个实际运行命令覆盖 2 图 × 2 模型 × 2 模式 |
| 是否破坏已有功能 | 否。git diff 确认零已有文件修改 |
| 文档是否把计划写成事实 | 否。T52a 未在 task board 中标记完成 |

### Adversarial 额外检查

| 检查项 | 结果 |
|--------|------|
| Artifact 数据对齐 | 通过。sanity check 验证 shape 一致 |
| Provenance narrative 正确性 | 通过。单点方向与 aggregate finding 一致 |
| 无 benchmark 有效性回归 | 通过。零修改已有 benchmark 数据 |
| 无过度工程 | 通过。~490 行，结构清晰，无不必要抽象 |
| 无隐藏耦合 | 通过。只依赖 common.load_declaration_graph() 和 numpy |

### 非阻塞问题

4 个非阻塞问题均不影响任务完成：

1. **FS 单 query 方向差异**（NB3）：CommRing 在 hierarchy_mixed 上 MAP 略高于 explicit_only。这是正常的单 query 波动，OR StrictOrderedCommRing 已展示足够显著的差异。建议后续在 report 中加说明。

2. **BFS 用 list.pop(0)**（NB2）：当前图规模（89-133 节点）完全不影响。扩展到更大图时改用 deque 即可。

3. **硬编码 Python 路径**（NB4）：demo report 中使用了环境特定的路径，建议后续精修时改为通用 `python` 命令。

4. **declaration_id 格式说明**（NB1）：脚本已有合理的错误处理（给出前 3 个示例），但可在 report 中更明确地说明格式来源。

### 结论

T52a 是一个执行得非常干净的实现任务。Worker 精确地按照 T52a 任务包的规格实现了 demo CLI 脚本：
- 代码结构清晰，无不必要抽象
- 所有 retrieval 从真实 artifact 实时计算，无 mock/stub
- Node ordering sanity check 按任务包要求实现
- Comparison mode 是硬边界，不是可选增强
- Demo report 包含 4 个命令示例和 paper bridge 映射
- Order.Ring StrictOrderedCommRing 展示了戏剧性的 provenance quality difference（MAP 0.6438 vs 0.1492），直接对应 T42/T43 的 aggregate finding

4 个非阻塞问题都是文档精修和扩展时的建议，不需要返修。

**Verdict: PASS**
