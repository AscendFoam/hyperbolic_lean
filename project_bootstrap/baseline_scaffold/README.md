# baseline scaffold

这个目录提供第一版 baseline 骨架，重点解决两件事：

1. 先把 `declarations.csv` 和 `edges.csv` 读通
2. 在正式训练前，把 split、manifest 和结果记录链路搭好

## 当前包含内容

- `requirements_baselines.txt`
  建议的 Python 依赖

- `configs/node2vec_example.json`
  Node2Vec baseline 示例配置

- `configs/node2vec_fixture_train.json`
  用仓库内最小 fixture 图做真训练的配置

- `configs/gcn_example.json`
  GCN baseline 示例配置

- `src/common.py`
  通用图数据读取、split 和输出工具

- `src/run_node2vec_baseline.py`
  Node2Vec baseline 骨架

- `src/run_gcn_baseline.py`
  GCN baseline 骨架

## 当前策略

考虑到本地环境当前是否安装完整依赖并不稳定，这套 baseline scaffold 做成了：

1. `Node2Vec` 已经补到第一版真实训练实现
2. `GCN` 仍然保持 scaffold 状态

也就是说，当前这套 baseline 当前的能力是：

1. 校验数据输入
2. 生成 split 文件
3. 生成运行 manifest
4. `Node2Vec` 训练 embedding 并做 link prediction 评估
5. 把实验元信息落到 `artifacts/baselines/`

## 推荐下一步

1. 先用 fixture 图跑通 `Node2Vec`
2. 再换成真实 declaration graph
3. 最后补 PyG 版或纯 torch 版 GCN 训练循环
