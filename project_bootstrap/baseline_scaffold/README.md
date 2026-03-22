# baseline scaffold

这个目录提供第一版 baseline 骨架，重点解决两件事：

1. 先把 `declarations.csv` 和 `edges.csv` 读通
2. 在正式训练前，把 split、manifest、dry-run 摘要和结果记录链路搭好

## 当前包含内容

- `requirements_baselines.txt`
  建议的 Python 依赖

- `configs/node2vec_example.json`
  Node2Vec baseline 示例配置

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

1. **依赖缺失时可 dry-run**
2. **依赖齐全后可接真实训练实现**

也就是说，当前脚本的最低价值是：

1. 校验数据输入
2. 生成 split 文件
3. 生成运行 manifest
4. 把实验元信息落到 `artifacts/baselines/`

## 推荐下一步

1. 先用 dry-run 跑通
2. 安装依赖
3. 再补真实的 Node2Vec 训练实现
4. 最后补 PyG 版 GCN 训练循环
