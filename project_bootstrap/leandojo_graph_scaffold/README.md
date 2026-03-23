# LeanDojo 抽图脚手架

这个目录提供一个**两段式脚手架**：

1. 先对 trace 目录做 inventory，弄清楚导出了什么
2. 再把原始 trace 归一化成 JSONL
3. 最后把“规范化后的 trace”转成 declaration graph 的 CSV

之所以做成两段式，是因为不同 LeanDojo / Mathlib 版本的导出格式可能不同。  
如果一开始就把脚本写死到某个具体字段上，很容易在版本切换时全部失效。

## 当前包含内容

- [configs/example_trace_config.json](d:\Codes\Math\hyperbolic_lean\project_bootstrap\leandojo_graph_scaffold\configs\example_trace_config.json)
  示例配置文件

- [configs/example_normalize_config.json](d:\Codes\Math\hyperbolic_lean\project_bootstrap\leandojo_graph_scaffold\configs\example_normalize_config.json)
  trace 归一化配置示例

- [configs/example_normalize_leandojo_xml_config.json](d:\Codes\Math\hyperbolic_lean\project_bootstrap\leandojo_graph_scaffold\configs\example_normalize_leandojo_xml_config.json)
  针对真实 LeanDojo traced repo 布局的 XML 适配配置示例

- [src/inventory_trace_dir.py](d:\Codes\Math\hyperbolic_lean\project_bootstrap\leandojo_graph_scaffold\src\inventory_trace_dir.py)
  对 trace 目录做文件清点和后缀统计

- [src/normalize_leandojo_trace.py](d:\Codes\Math\hyperbolic_lean\project_bootstrap\leandojo_graph_scaffold\src\normalize_leandojo_trace.py)
  将原始 trace 尽量归一化成 declaration-level JSONL

- [src/extract_decl_graph.py](d:\Codes\Math\hyperbolic_lean\project_bootstrap\leandojo_graph_scaffold\src\extract_decl_graph.py)
  将“规范化后的 JSONL trace”转换为 `declarations.csv` 和 `edges.csv`

- [src/trace_repo_with_leandojo.py](d:\Codes\Math\hyperbolic_lean\project_bootstrap\leandojo_graph_scaffold\src\trace_repo_with_leandojo.py)
  安装好 LeanDojo 后，直接 trace 一个真实 Lean 仓库

## 推荐工作流

## 第一步：拿到 trace 目录后先做 inventory

```powershell
python .\project_bootstrap\leandojo_graph_scaffold\src\inventory_trace_dir.py `
  --trace-root D:\path\to\trace `
  --output-root D:\path\to\inventory_out
```

这一步的目标不是抽图，而是回答：

1. 有哪些文件类型
2. 目录层级长什么样
3. 样本文件大不大
4. 后续该从哪些文件里解析 declaration 信息

## 第二步：把原始 trace 适配成 normalized JSONL

现在已经提供了两类 adapter：

1. `generic_json`
   面向通用 JSON/JSONL 导出
2. `leandojo_trace_xml`
   面向 LeanDojo traced repo 中真实常见的 `*.trace.xml + *.dep_paths` 结构

如果你拿到的是标准 traced repo，优先用后者。

归一化后的目标结构如下：

```json
{
  "decl_name": "Mathlib.Topology.Basic.compact_def",
  "decl_kind": "theorem",
  "module_name": "Mathlib.Topology.Basic",
  "file_path": "Mathlib/Topology/Basic.lean",
  "line_start": 10,
  "line_end": 20,
  "signature_text": "CompactSpace X -> ...",
  "dependencies": [
    "Mathlib.Topology.Basic.CompactSpace",
    "Mathlib.Order.Basic.le_refl"
  ]
}
```

可以先这样运行：

```powershell
python .\project_bootstrap\leandojo_graph_scaffold\src\normalize_leandojo_trace.py `
  --config .\project_bootstrap\leandojo_graph_scaffold\configs\example_normalize_leandojo_xml_config.json
```

`extract_decl_graph.py` 读取的就是这种规范化后的 JSONL。

## 如何得到真实 trace 样本

最简单的方式是按 LeanDojo 官方文档的例子先 trace 一个小仓库，而不是一开始就上全量 Mathlib。

例如：

```powershell
conda run -n DLEnv python .\project_bootstrap\leandojo_graph_scaffold\src\trace_repo_with_leandojo.py `
  --repo-url https://github.com/yangky11/lean4-example `
  --commit 7b6ecb9ad4829e4e73600a3329baeb3b5df8d23f `
  --dst-dir data/raw/real_trace_samples/traced_lean4_example
```

trace 成功后，你会在输出目录里看到类似：

- `*.dep_paths`
- `*.ast.json`
- `*.trace.xml`

其中 `*.trace.xml` 是当前 adapter 最关注的文件。

## fixture

目录里还放了一个最小 fixture：

- `fixtures/lean4_example/Example.trace.xml`
- `fixtures/lean4_example/Example.dep_paths`

它不是完整 LeanDojo 输出，只是为了帮助快速验证 XML adapter 的逻辑是否通顺。

## 第三步：从 normalized trace 抽 declaration graph

```powershell
python .\project_bootstrap\leandojo_graph_scaffold\src\extract_decl_graph.py `
  --config .\project_bootstrap\leandojo_graph_scaffold\configs\example_trace_config.json
```

## 输出内容

脚手架会输出：

- `declarations.csv`
- `edges.csv`
- `stats.json`

字段设计与 [02_数据Schema设计文档.md](d:\Codes\Math\hyperbolic_lean\project_bootstrap\02_数据Schema设计文档.md) 对齐。

## 当前边界

这个脚手架目前**不是完整产品代码**，而是为了帮助你更快进入第 1 个月的数据阶段。

它当前不做：

1. 直接调用 LeanDojo trace API
2. 直接解析某个特定版本的原始 AST 字段
3. proof-state 图抽取
4. 标签抽取

这些都应该在 trace 样本稳定后再补。

## 下一步建议

当你拿到第一批真实 trace 样本后，优先补的不是模型代码，而是：

1. `normalize_leandojo_trace.py`
2. declaration kind 映射规则
3. edge type 细分规则
4. 数据质量检查脚本
