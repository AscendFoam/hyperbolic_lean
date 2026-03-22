# data 目录说明

这个目录用于存放项目的数据文件，按生命周期分层：

- `raw/`
  原始数据，不做人工修改。

- `interim/`
  中间处理结果，例如 normalized trace、inventory 输出等。

- `processed/`
  可以直接被 baseline 或模型读取的结构化数据。

## 当前约定

1. 原始 trace 放在 `raw/leandojo_trace/`
2. normalized JSONL 放在 `interim/normalized_trace/`
3. declaration graph 放在 `processed/declaration_graph/`
4. proof-state graph 放在 `processed/proof_graph/`

## 注意

1. 所有数据快照都应该能追溯到具体的 Mathlib commit
2. 不要直接覆盖旧快照，优先新建版本目录或写 manifest
