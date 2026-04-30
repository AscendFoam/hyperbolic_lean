# baseline scaffold

这个目录提供 declaration-graph baseline 的第一版可训练脚手架，目标是把以下流程做成可复现闭环：

1. 读取 `declarations.csv` 和 `edges.csv`
2. 按固定协议生成 train/val/test split
3. 生成运行 manifest 和负采样统计
4. 在同口径设置下训练 baseline 并落盘结果到 `artifacts/baselines/`

## 当前包含内容

- `requirements_baselines.txt`
  Python 依赖建议

- `configs/node2vec_example.json`
  默认协议下的 Node2Vec 配置

- `configs/gcn_example.json`
  默认协议下的纯 PyTorch GCN 配置

- `configs/hyperbolic_example.json`
  默认协议下的第一版纯 PyTorch 双曲 baseline 配置

- `src/common.py`
  图读取、切分、 harder negatives 与输出工具

- `src/run_node2vec_baseline.py`
  Node2Vec baseline

- `src/run_gcn_baseline.py`
  纯 PyTorch GCN baseline

- `src/run_hyperbolic_baseline.py`
  第一版纯 PyTorch 双曲 baseline

## 默认评测协议

当前默认协议固定为：

1. 图使用 `closed-world` declaration graph
2. 负采样使用 `same_module`
3. 候选不足时退回 `random`
4. split seed offset 固定为 `train +101 / val +202 / test +303`

这样做的目的是避免 easy negatives 把 link prediction 做得过于乐观。

## 当前真实样本结果

在 `lean4-example` 的真实 closed-world 图上，默认协议下已有三组可直接对照的结果：

- Node2Vec: `test AP = 0.5580`, `test AUROC = 0.5524`
- GCN: `test AP = 0.9013`, `test AUROC = 0.8685`
- Hyperbolic v1: `test AP = 0.4196`, `test AUROC = 0.3825`

这说明：

1. harder negatives 已经把浅层随机游走 baseline 压到更可信的区间
2. 纯 PyTorch GCN 在当前协议下是明显更强的欧氏对照
3. 第一版双曲 baseline 已经稳定可训练，但当前性能还不足以支撑“优于欧氏 GCN”的主张

## 运行方式

在本地 `DLEnv` 中可直接运行：

```powershell
conda run -n DLEnv python .\project_bootstrap\baseline_scaffold\src\run_node2vec_baseline.py --config .\project_bootstrap\baseline_scaffold\configs\node2vec_example.json
conda run -n DLEnv python .\project_bootstrap\baseline_scaffold\src\run_gcn_baseline.py --config .\project_bootstrap\baseline_scaffold\configs\gcn_example.json
conda run -n DLEnv python .\project_bootstrap\baseline_scaffold\src\run_hyperbolic_baseline.py --config .\project_bootstrap\baseline_scaffold\configs\hyperbolic_example.json
```

## 下一步建议

最值得继续推进的方向是：

1. 在同一默认协议下补更强欧氏对照，例如 GraphSAGE 或更稳的 MLP edge decoder
2. 继续改进双曲 baseline，例如更合适的双曲解码器、曲率扫描和低维对照
3. 把 link prediction 扩展到模块切分或时间切分，减少边级随机切分带来的乐观偏差
