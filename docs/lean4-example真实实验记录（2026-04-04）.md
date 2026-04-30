# lean4-example 真实实验记录（2026-04-04）

## 1. 实验目标

本次实验的目标是验证以下工程链路已经可在真实 LeanDojo trace 样本上闭环运行：

1. 真实 traced repo 获取
2. `*.trace.xml + *.dep_paths + *.ast.json` 归一化
3. declaration graph 抽取
4. Node2Vec baseline 训练与 link prediction 评估
5. 对比 `open-world` 与 `closed-world` 两种抽图策略的影响

本次实验使用 `lean4-example` 作为第一批真实样本，目标不是追求最终最强指标，而是验证工程管线、明确图构建边界，并识别后续扩展到更大 Lean 仓库时的主要风险。

## 2. 实验环境

### 2.1 运行环境

- Windows 主工作区
- WSL2: `Ubuntu-22.04`
- WSL 用户: `qcy`
- Lean 工具链: `elan + Lean 4.29.0`
- LeanDojo Python 环境: `/home/qcy/.venvs/lean-dojo`
- LeanDojo 版本: `4.20.0`
- Baseline 训练环境: `conda` 环境 `DLEnv`

### 2.2 样本来源

- Repo: `https://github.com/yangky11/lean4-example`
- Commit: `7b6ecb9ad4829e4e73600a3329baeb3b5df8d23f`

真实 traced repo 已成功生成，并同步到工作区：

- trace 输入目录: `data/raw/leandojo_trace/traced_lean4_example_wsl`

样本完整性检查结果：

- `*.trace.xml`: `907`
- `*.dep_paths`: `907`
- `*.ast.json`: `907`

## 3. 本次使用的正式配置

### 3.1 normalize 配置

- `project_bootstrap/leandojo_graph_scaffold/configs/example_normalize_leandojo_xml_config.json`

关键字段：

- `input_root = data/raw/leandojo_trace/traced_lean4_example_wsl`
- `output_path = data/interim/normalized_trace/lean4_example_normalized_declarations_from_xml.jsonl`
- `source_commit = 7b6ecb9ad4829e4e73600a3329baeb3b5df8d23f`

### 3.2 declaration graph 配置

开放世界版本：

- `project_bootstrap/leandojo_graph_scaffold/configs/example_trace_config.json`

关键字段：

- `output_root = data/processed/declaration_graph/lean4_example`
- `closed_world = false`（默认）

闭世界版本：

- `project_bootstrap/leandojo_graph_scaffold/configs/example_trace_closed_world_config.json`

关键字段：

- `output_root = data/processed/declaration_graph/lean4_example_closed_world`
- `closed_world = true`

### 3.3 Node2Vec baseline 配置

开放世界首轮配置：

- `project_bootstrap/baseline_scaffold/configs/node2vec_example.json`

关键字段：

- `run_id = node2vec_lean4_example_first_run_v1`
- `graph_root = data/processed/declaration_graph/lean4_example`
- `embedding_dim = 32`
- `walk_length = 10`
- `num_walks_per_node = 2`
- `window_size = 2`
- `epochs = 2`

闭世界配置：

- `project_bootstrap/baseline_scaffold/configs/node2vec_lean4_example_closed_world.json`

关键字段：

- `run_id = node2vec_lean4_example_closed_world_v1`
- `graph_root = data/processed/declaration_graph/lean4_example_closed_world`
- 其余训练超参与开放世界版本保持一致

## 4. 数据与图规模

### 4.1 normalize 结果

- normalized declarations: `33,321`

输出：

- `data/interim/normalized_trace/lean4_example_normalized_declarations_from_xml.jsonl`

### 4.2 declaration graph 结果

开放世界图：

- declarations: `33,321`
- edges: `189,066`

闭世界图：

- declarations: `33,321`
- edges: `146,347`

闭世界过滤统计：

- `dropped_external_edges = 43,637`
- `missing_dependency_count = 3,841`

说明：

1. `dropped_external_edges` 是原始依赖提及层面的丢弃计数，包含重复依赖提及。
2. 从最终图角度看，开放世界到闭世界的唯一路径边减少量为 `42,719`，即 `189,066 - 146,347`。
3. 这说明真实 trace 中存在大量指向“当前 declaration 集外部符号”的依赖边；如果不显式建模这些外部节点，开放世界图会天然变成一个不闭合图。

## 5. Baseline 实验结果

### 5.1 开放世界结果

run id:

- `node2vec_lean4_example_first_run_v1`

产物目录：

- `artifacts/baselines/node2vec_lean4_example_first_run_v1`

训练统计：

- `num_walks = 66,642`
- `num_pairs = 2,058,972`

评估结果：

| split | AUROC | AP | Accuracy | F1 | #positive | #negative |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| val | 0.8386 | 0.8165 | 0.7566 | 0.6780 | 14,662 | 18,906 |
| test | 0.8366 | 0.8166 | 0.7575 | 0.6790 | 14,625 | 18,906 |

### 5.2 闭世界结果

run id:

- `node2vec_lean4_example_closed_world_v1`

产物目录：

- `artifacts/baselines/node2vec_lean4_example_closed_world_v1`

训练统计：

- `num_walks = 66,642`
- `num_pairs = 2,057,068`

评估结果：

| split | AUROC | AP | Accuracy | F1 | #positive | #negative |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| val | 0.8194 | 0.8335 | 0.7312 | 0.6915 | 14,634 | 14,634 |
| test | 0.8235 | 0.8397 | 0.7388 | 0.7023 | 14,634 | 14,634 |

### 5.3 开放世界 vs 闭世界对比

| 维度 | 开放世界 | 闭世界 | 观察 |
| --- | ---: | ---: | --- |
| 节点数 | 33,321 | 33,321 | 相同 |
| 边数 | 189,066 | 146,347 | 闭世界减少 `42,719` 条唯一边 |
| test AUROC | 0.8366 | 0.8235 | 闭世界略低 |
| test AP | 0.8166 | 0.8397 | 闭世界更高 |
| test F1 | 0.6790 | 0.7023 | 闭世界更高 |
| test 样本平衡性 | 正负不平衡 | 正负平衡 | 闭世界更干净 |

初步解释：

1. 开放世界图包含大量指向外部 declaration 的边，但 baseline 当前并没有为这些外部节点构造真实 embedding 语义闭包，因此图结构存在“半开边界”。
2. 闭世界图删除了这部分外部依赖边，得到的是一个更加自洽的内部子图，因此 AP 和 F1 提升更符合预期。
3. AUROC 在闭世界下略低，说明模型对整体排序区分能力并没有同步显著提升，但正例检索质量和阈值判别质量更好。
4. 对当前阶段而言，闭世界图更适合作为第一版工程化 baseline 的正式默认设置。

## 6. 关键工程问题与风险

### 6.1 图边界定义风险

风险：

- 如果 declaration graph 中允许依赖边指向未纳入节点表的外部符号，训练图会出现不闭合边界，影响 embedding 学习与实验解释。

当前处理：

- 新增 `closed_world` 抽图开关。
- 在 `closed_world = true` 时显式丢弃外部依赖边，并记录丢弃计数。

后续建议：

- 方案书和论文正文应明确区分：
  - `open-world dependency graph`
  - `closed-world induced subgraph`

### 6.2 Windows / WSL 混合环境风险

风险：

- LeanDojo 在 WSL 中生成 traced repo 时，如果直接把完整 traced repo 复制到 `/mnt/d/...`，会因 Linux 权限/链接语义触发 `Operation not permitted`。

当前处理：

- traced repo 完整版保留在 WSL Linux 文件系统中。
- 工作区保留可供当前 pipeline 使用的真实 trace 文件集。

后续建议：

- 大规模 trace 阶段优先在 WSL Linux 文件系统内完成。
- Windows 工作区只保留必要产物，不强求完整 repo 镜像。

### 6.3 实验耗时风险

风险：

- 真实图上的 Node2Vec 在较重参数下会超时，尤其是 `walk_length`、`num_walks_per_node`、`epochs` 同时偏大时。

当前处理：

- 首轮真实实验采用轻量可完成配置。

后续建议：

- 将参数搜索拆成：
  1. 可完成的 smoke setting
  2. 中等预算 setting
  3. 投稿级 setting

### 6.4 负采样与评测定义风险

风险：

- 当前 negative edge 是随机采样，尚未控制模块内/跨模块、同 namespace、同 kind 等更难负例。

影响：

- 当前指标可作为工程打通基线，但不足以支撑投稿级结论。

后续建议：

- 补充 harder negatives：
  - same module negatives
  - same namespace negatives
  - same decl_kind negatives

## 7. 当前结论

本次实验已经可以支撑以下结论：

1. 真实 LeanDojo trace 到 declaration graph 到 Node2Vec baseline 的工程闭环已经打通。
2. `lean4-example` 级别的真实样本足以暴露“开放世界依赖边界”这个核心工程问题。
3. 对当前 baseline 而言，闭世界图比开放世界图更适合作为正式默认设置。
4. 第一轮真实实验已经给出可复现实验产物，可直接纳入方案书的“原型系统验证”部分。

## 8. 下一轮计划

建议按以下顺序推进：

1. 将 `closed_world` 图设为默认 baseline 图。
2. 在抽图阶段加入模块级、namespace 级统计，补充图诊断报告。
3. 将 Node2Vec baseline 扩展为多组参数预算，并形成标准实验表。
4. 实现 `GCN` 第一版可训练基线，优先在 closed-world 图上对齐评测。
5. 设计更严格的负采样与切分协议，减少“随机负例过易”带来的指标高估。
6. 在第二个真实仓库上复现实验，验证当前设计是否能跨 repo 稳定迁移。

## 9. 复现实验命令

### 9.1 normalize

```powershell
conda run -n DLEnv python .\project_bootstrap\leandojo_graph_scaffold\src\normalize_leandojo_trace.py `
  --config .\project_bootstrap\leandojo_graph_scaffold\configs\example_normalize_leandojo_xml_config.json
```

### 9.2 开放世界抽图

```powershell
conda run -n DLEnv python .\project_bootstrap\leandojo_graph_scaffold\src\extract_decl_graph.py `
  --config .\project_bootstrap\leandojo_graph_scaffold\configs\example_trace_config.json
```

### 9.3 闭世界抽图

```powershell
conda run -n DLEnv python .\project_bootstrap\leandojo_graph_scaffold\src\extract_decl_graph.py `
  --config .\project_bootstrap\leandojo_graph_scaffold\configs\example_trace_closed_world_config.json
```

### 9.4 开放世界 Node2Vec

```powershell
conda run -n DLEnv python .\project_bootstrap\baseline_scaffold\src\run_node2vec_baseline.py `
  --config .\project_bootstrap\baseline_scaffold\configs\node2vec_example.json
```

### 9.5 闭世界 Node2Vec

```powershell
conda run -n DLEnv python .\project_bootstrap\baseline_scaffold\src\run_node2vec_baseline.py `
  --config .\project_bootstrap\baseline_scaffold\configs\node2vec_lean4_example_closed_world.json
```

## 10. 补充实验：closed-world harder negatives

为了验证第一轮 `closed-world` 结果是否受到“随机负采样过易”的影响，本轮进一步增加了第二个对照实验。

### 10.1 设定

- 图版本：`closed-world`
- 负采样策略：`same_module`
- fallback 策略：`random`
- 训练超参数：与第一轮 `closed-world Node2Vec` 保持一致
- 配置文件：`project_bootstrap/baseline_scaffold/configs/node2vec_lean4_example_closed_world_same_module_negatives.json`
- 产物目录：`artifacts/baselines/node2vec_lean4_example_closed_world_same_module_negatives_v1`

### 10.2 结果

- val AP: `0.5457`
- test AP: `0.5472`
- val AUROC: `0.5469`
- test AUROC: `0.5519`
- val F1: `0.4581`
- test F1: `0.4646`

训练统计：

- `num_walks = 66,642`
- `num_pairs = 2,057,068`

### 10.3 负采样实际执行情况

- train: requested `117,079`，sampled `117,079`，其中 `same_module = 117,048`，fallback `random = 31`
- val: requested `14,634`，sampled `14,634`，其中 `same_module = 14,627`，fallback `random = 7`
- test: requested `14,634`，sampled `14,634`，其中 `same_module = 14,631`，fallback `random = 3`

这说明 harder negatives 不是名义设置，而是几乎完全按 `same_module` 执行成功。

### 10.4 解释

1. 与随机负采样闭世界 baseline 相比，AP 从 `0.8397` 下降到 `0.5472`，说明随机负采样显著低估了任务难度。
2. 当前任务在更严格负例下仍然高于随机猜测，但已经不能被视为“接近解决”的状态。
3. 后续正式实验必须至少同时报告：
   - easy negatives
   - hard negatives
4. 如果论文只报告随机负采样结果，会明显高估模型对真实结构歧义的区分能力。

### 10.5 对下一轮实验的影响

- `closed-world` 仍应保留为默认主图。
- `same_module` harder negatives 应纳入默认评测协议。
- 在 harder negatives 设定下，再比较欧氏方法与双曲方法，才更接近投稿级证据标准。

## 11. 补充实验：默认协议下的纯 PyTorch GCN

为了在更严格评测协议下继续扩展欧氏 baseline，本轮新增了一版不依赖 `torch_geometric`、可直接在当前 `DLEnv` 中训练的纯 PyTorch GCN。

### 11.1 默认评测协议

当前默认协议固定为：

- 图版本：`closed-world`
- 负采样策略：`same_module`
- fallback：`random`
- split seed：使用稳定映射，不再依赖 Python `hash()`

这意味着后续 Node2Vec、GCN 以及新的欧氏/双曲模型，都应在同一 harder-negative 协议下比较。

### 11.2 默认协议 Node2Vec 结果

配置文件：`project_bootstrap/baseline_scaffold/configs/node2vec_example.json`

产物目录：`artifacts/baselines/node2vec_lean4_example_default_protocol_v1`

结果：

- val AP: `0.5556`
- test AP: `0.5580`
- val AUROC: `0.5483`
- test AUROC: `0.5524`
- val F1: `0.4599`
- test F1: `0.4704`

### 11.3 默认协议 GCN 结果

配置文件：`project_bootstrap/baseline_scaffold/configs/gcn_example.json`

产物目录：`artifacts/baselines/gcn_lean4_example_default_protocol_v1`

结果：

- val AP: `0.9020`
- test AP: `0.9013`
- val AUROC: `0.8691`
- test AUROC: `0.8685`
- val F1: `0.6673`
- test F1: `0.6677`
- best epoch: `30`

### 11.4 当前解释

1. 在同一 `closed-world + same_module harder negatives` 协议下，纯 PyTorch GCN 明显优于 Node2Vec。
2. 这说明默认协议收紧之后，任务并没有失去可学习性，而是更真实地暴露了模型结构能力差异。
3. 纯欧氏图神经网络已经足以构成后续双曲方法的强基线，因此下一步如果引入双曲 GNN，会处在更可信的比较框架里。
4. 由于当前 GCN 仍然只使用图结构和可学习节点参数，还未融合文本、声明类型特征或更难切分，因此这仍然只是第一版可训练基线，而不是最终上界。
