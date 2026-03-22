# artifacts 目录说明

这个目录用于存放由脚本和实验生成的产物，不放原始数据。

推荐分层：

- `inventories/`
  trace 目录清点结果

- `graphs/`
  graph 统计、图结构诊断结果

- `baselines/`
  baseline 运行输出、split 文件、结果摘要

- `checkpoints/`
  模型权重

- `logs/`
  运行日志

## 当前约定

1. 每次实验都应带 `run_id`
2. 每个 `run_id` 对应一个子目录
3. 同一脚本的 dry-run 输出也应写入 artifacts，便于复查
