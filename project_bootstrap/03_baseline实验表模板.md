# baseline 实验表模板

## 1. 使用目的

这个模板用于统一记录：

1. 图结构诊断结果
2. 欧氏 baseline 结果
3. 双曲 baseline 结果
4. probing / retrieval 结果

目标不是做漂亮表格，而是保证：

1. 每次实验都能回溯
2. 不同模型可以公平比较
3. 后期写论文时不用重新整理历史结果

## 2. 记录原则

1. 一次运行一个 `run_id`
2. 一次运行只记录一种主要结果
3. 必须记录数据版本和 split 版本
4. 必须记录 seed
5. 必须区分主结果与 exploratory 结果

## 3. 建议的主结果表

## 3.1 图结构诊断表

| graph_scope | num_nodes | num_edges | avg_depth | avg_branching | approx_hyperbolicity | notes |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| `Algebra_subgraph_v1` |  |  |  |  |  |  |
| `Topology_subgraph_v1` |  |  |  |  |  |  |
| `typeclass_graph_v1` |  |  |  |  |  |  |

## 3.2 link prediction 主表

| model | geometry | dim | params_m | split | MRR | Hits@1 | Hits@10 | MAP | AUROC | notes |
| :--- | :--- | ---: | ---: | :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| heuristic | none | 0 | 0 |  |  |  |  |  |  |  |
| Node2Vec | euclidean |  |  |  |  |  |  |  |  |  |
| GCN | euclidean |  |  |  |  |  |  |  |  |  |
| GraphSAGE | euclidean |  |  |  |  |  |  |  |  |  |
| Poincare | hyperbolic |  |  |  |  |  |  |  |  |  |
| HGCN | hyperbolic |  |  |  |  |  |  |  |  |  |

## 3.3 probing 主表

| task | model | geometry | dim | probe | split | macro_f1 | auroc | calibration | notes |
| :--- | :--- | :--- | ---: | :--- | :--- | ---: | ---: | ---: | :--- |
| decl_kind | Node2Vec | euclidean |  | linear |  |  |  |  |  |
| decl_kind | GCN | euclidean |  | linear |  |  |  |  |  |
| decl_kind | HGCN | hyperbolic |  | linear |  |  |  |  |  |
| CommGroup | GCN | euclidean |  | mlp |  |  |  |  |  |
| CommGroup | HGCN | hyperbolic |  | mlp |  |  |  |  |  |

## 3.4 retrieval 主表

| task | retriever | geometry | graph_scope | Recall@10 | MRR | nDCG@10 | useful_hit_rate | notes |
| :--- | :--- | :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| theorem_retrieval | BM25 | none |  |  |  |  |  |  |
| theorem_retrieval | dense_text | euclidean |  |  |  |  |  |  |
| theorem_retrieval | graph_embed | euclidean |  |  |  |  |  |  |
| theorem_retrieval | graph_embed | hyperbolic |  |  |  |  |  |  |
| proof_state_retrieval | graph_embed | hyperbolic |  |  |  |  |  |  |

## 4. 必做消融表

## 4.1 维度消融

| model | geometry | dim | task | metric | value | notes |
| :--- | :--- | ---: | :--- | :--- | ---: | :--- |
| GCN | euclidean | 16 |  |  |  |  |
| GCN | euclidean | 32 |  |  |  |  |
| HGCN | hyperbolic | 16 |  |  |  |  |
| HGCN | hyperbolic | 32 |  |  |  |  |

## 4.2 图范围消融

| graph_scope | model | task | metric | value | notes |
| :--- | :--- | :--- | :--- | ---: | :--- |
| typeclass_graph_v1 |  |  |  |  |  |
| Algebra_subgraph_v1 |  |  |  |  |  |
| Topology_subgraph_v1 |  |  |  |  |  |

## 4.3 标签族消融

| label_family | model | positive_count | unknown_count | metric | value | notes |
| :--- | :--- | ---: | ---: | :--- | ---: | :--- |
| decl_kind |  |  |  |  |  |  |
| CommGroup |  |  |  |  |  |  |
| CompactSpace |  |  |  |  |  |  |

## 5. 单次运行记录字段

建议每次运行都至少记录：

1. `run_id`
2. `date`
3. `task`
4. `graph_scope`
5. `split_name`
6. `model_name`
7. `geometry`
8. `dim`
9. `seed`
10. `best_metric`
11. `checkpoint_path`
12. `notes`

## 6. 结果解释注意事项

记录结果时要额外注意：

1. 不同几何空间比较时，要说明参数规模是否一致
2. probing 结果要说明 probe 类型  
   线性 probe 和 MLP probe 不能混写成一行结论
3. 若标签是高置信子集，需要写清正负样本数量
4. retrieval 结果要说明候选库大小
5. 若某实验失败，也应记录，不要只保留成功结果

## 7. 建议的文件配套

与这份模板配套使用的文件：

1. [templates/baseline_results_template.csv](d:\Codes\Math\hyperbolic_lean\project_bootstrap\templates\baseline_results_template.csv)
2. 每周实验日志
3. ablation 附表
4. 失败案例清单

## 8. 第 1 个月只需要先填哪些表

第 1 个月只建议先填：

1. 图结构诊断表
2. 单次运行记录表

link prediction、probing 和 retrieval 主表可以从第 2 个月开始正式填。
