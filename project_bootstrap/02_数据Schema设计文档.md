# 数据 Schema 设计文档

## 1. 文档目标

这份文档定义主线项目的数据层最小规范，目标是让后续的抽图脚本、baseline 模型和评估脚本都围绕统一 schema 工作。

当前优先支持三个对象层级：

1. declaration graph
2. labels / metadata
3. proof-state graph  
   proof-state 部分在第 1 个月只做预留，不要求立刻全量实现

## 2. 设计原则

1. **先最小可行，再逐步扩展**
2. **字段要支持复现**
3. **ID 必须稳定**
4. **unknown 与 missing 要区分**
5. **原始数据与处理后数据分层保存**

## 3. 建议目录结构

```text
data/
├─ raw/
│  ├─ leandojo_trace/
│  └─ manifests/
├─ interim/
│  ├─ normalized_trace/
│  └─ inventories/
└─ processed/
   ├─ declaration_graph/
   │  ├─ declarations.csv
   │  ├─ edges.csv
   │  ├─ labels.csv
   │  ├─ splits.csv
   │  └─ stats.json
   └─ proof_graph/
      ├─ proof_states.csv
      ├─ tactic_steps.csv
      ├─ theorem_links.csv
      └─ stats.json
```

## 4. ID 设计

## 4.1 declaration_id

建议规则：

`{mathlib_commit}::{decl_name}`

示例：

`abc1234::Mathlib.Topology.Basic.CompactSpace`

原因：

1. 便于跨文件唯一定位
2. 便于不同数据快照区分

## 4.2 edge_id

建议规则：

`{src_id}--{edge_type}--{dst_id}`

## 4.3 state_id

建议规则：

`{theorem_id}::step_{step_idx}::state_{local_hash}`

## 4.4 run_id

用于记录实验结果，建议规则：

`{date}_{task}_{model}_{seed}`

## 5. declaration graph schema

## 5.1 declarations.csv

每一行对应一个 formal declaration。

| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `declaration_id` | string | 是 | 主键 |
| `decl_name` | string | 是 | 完整声明名 |
| `decl_kind` | string | 是 | `def/theorem/lemma/class/instance/...` |
| `module_name` | string | 是 | 模块名 |
| `file_path` | string | 是 | 相对路径 |
| `namespace` | string | 否 | 所属命名空间 |
| `line_start` | int | 否 | 起始行 |
| `line_end` | int | 否 | 结束行 |
| `signature_text` | string | 否 | 声明签名或类型信息 |
| `body_text` | string | 否 | 定义体或 proof term 摘要 |
| `docstring` | string | 否 | 文档字符串 |
| `ast_size` | int | 否 | AST 节点数 |
| `token_count` | int | 否 | 文本 token 数 |
| `dependency_depth` | int | 否 | 预计算层级深度 |
| `source_commit` | string | 是 | Mathlib commit |
| `trace_version` | string | 否 | trace 导出版本 |

### 最小必填字段

如果第 1 个月字段拿不全，至少保证：

- `declaration_id`
- `decl_name`
- `decl_kind`
- `module_name`
- `file_path`
- `source_commit`

## 5.2 edges.csv

每一行对应一条图边。

| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `edge_id` | string | 是 | 主键 |
| `src_id` | string | 是 | 源节点 |
| `dst_id` | string | 是 | 目标节点 |
| `edge_type` | string | 是 | 例如 `uses/depends_on/extends/instance_of` |
| `evidence_source` | string | 否 | 边来源，如 `trace/ast/manual` |
| `weight` | float | 否 | 可选权重 |
| `is_direct` | bool | 否 | 是否直接依赖 |
| `source_commit` | string | 是 | Mathlib commit |

### 推荐 edge_type

第一版建议最多保留 4 类：

1. `uses`
2. `depends_on`
3. `extends`
4. `instance_of`

如果早期无法稳定区分 `uses` 和 `depends_on`，优先保留一种统一类型。

## 5.3 labels.csv

每一行对应一个 declaration 在某个标签上的取值。

| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `declaration_id` | string | 是 | 外键 |
| `label_name` | string | 是 | 标签名 |
| `label_value` | string | 是 | `positive/negative/unknown` |
| `label_source` | string | 是 | `metaprogramming/manual/syntax` |
| `confidence` | float | 否 | 0 到 1 |
| `query_repr` | string | 否 | 触发该标签的 Lean 查询表示 |
| `notes` | string | 否 | 附加说明 |

### 标签语义约束

1. `unknown` 不是负样本
2. `negative` 必须有比“实例综合失败”更强的依据
3. 主实验优先用高置信 `positive`

## 5.4 splits.csv

用于记录训练/验证/测试划分。

| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `entity_id` | string | 是 | declaration_id 或其他实体 id |
| `entity_type` | string | 是 | `declaration/edge/theorem/state` |
| `split_name` | string | 是 | `train/valid/test` |
| `split_strategy` | string | 是 | `module/time/random/edge_mask` |
| `split_version` | string | 是 | 划分版本号 |

## 6. proof graph schema

这一部分在第 1 个月先定义，不强制立即全量抽出。

## 6.1 proof_states.csv

| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `state_id` | string | 是 | 主键 |
| `theorem_id` | string | 是 | 关联 theorem |
| `step_idx` | int | 是 | 证明步序号 |
| `goal_text` | string | 是 | 当前 goal 的 pretty text |
| `local_context_text` | string | 否 | local context 的序列化文本 |
| `goal_hash` | string | 否 | 用于去重 |
| `source_commit` | string | 是 | Mathlib commit |

## 6.2 tactic_steps.csv

| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `transition_id` | string | 是 | 主键 |
| `theorem_id` | string | 是 | 所属 theorem |
| `from_state_id` | string | 是 | 起始状态 |
| `to_state_id` | string | 否 | 结果状态，失败时可空 |
| `tactic_text` | string | 是 | tactic 原文 |
| `tactic_head` | string | 否 | tactic 首符号 |
| `success` | bool | 是 | 是否成功 |
| `error_text` | string | 否 | 失败错误信息 |
| `step_idx` | int | 是 | 步序号 |

## 6.3 theorem_links.csv

用于把 theorem 与 declaration graph 或 proof graph 关联起来。

| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `theorem_id` | string | 是 | theorem declaration id |
| `linked_declaration_id` | string | 是 | 相关 declaration |
| `link_type` | string | 是 | `mentions/uses/retrieved_as_neighbor` |

## 7. 规范化规则

## 7.1 文本字段

1. 保留原始 Lean 名称，不做语义改写
2. 换行统一为 `\n`
3. 空字符串与缺失值区分

## 7.2 布尔与标签字段

1. 布尔字段只使用 `true/false`
2. 标签字段使用 `positive/negative/unknown`

## 7.3 路径字段

1. 原始存储中保留相对路径
2. 日志或 UI 中再映射为绝对路径

## 8. 数据验证 checklist

每次生成新数据快照后，至少做以下检查：

1. `declaration_id` 是否唯一
2. `edge_id` 是否唯一
3. `src_id/dst_id` 是否都能在 declarations 中找到
4. `label_value` 是否只出现在三值集合中
5. split 是否互斥
6. 各文件是否都带 `source_commit`

## 9. 第 1 个月最小可行 schema

如果时间很紧，先只保证下面四张表：

1. `declarations.csv`
2. `edges.csv`
3. `labels.csv`
4. `stats.json`

proof-state 相关三张表可以推迟到第 2 个月再落地。

## 10. 推荐的 stats.json 字段

建议至少包含：

```json
{
  "source_commit": "abc1234",
  "trace_version": "TODO",
  "num_declarations": 0,
  "num_edges": 0,
  "num_modules": 0,
  "decl_kind_counts": {},
  "edge_type_counts": {},
  "label_name_counts": {},
  "generated_at": "YYYY-MM-DDTHH:MM:SS"
}
```

## 11. 第 2 个月前不要扩展的字段

以下字段先不要急着加入：

1. 全量 proof term
2. 复杂 AST 子树 JSON
3. 所有 tactic 中间错误栈
4. 大规模自然语言释义

原因是它们会显著增加复杂度，但对第一个 baseline 的帮助有限。
