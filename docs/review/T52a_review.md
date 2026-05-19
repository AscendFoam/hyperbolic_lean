# Review: T52a

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

### NB1. `run_single_query` 查找 declaration 时使用 `row["declaration_id"] == decl_name` 但变量名 `decl_name` 实际对应 `--declaration-name` 参数

proof_side_ancestor_explanation.py:252-261 的查找逻辑在 `declaration_id` 字段上做精确匹配，这与 CLI 帮助文本和 T52a 任务包一致。但 T52a 任务包 Section 1 的示例格式是 `hash::Name`，如果 `declarations.csv` 中的 `declaration_id` 格式不是精确的 `hash::Name`（比如多一个前缀），脚本会报错并给出前 3 个示例。这是合理的错误处理，但建议在 demo report 中注明 `declaration_id` 的实际格式来源。当前不影响通过。

### NB2. BFS ancestor 搜索使用 `queue.pop(0)`（O(n) list pop），在大图上可能较慢

proof_side_ancestor_explanation.py:150 使用 `queue.pop(0)` 而不是 `collections.deque.popleft()`。当前图规模（89-133 节点）完全不影响性能，但若后续扩展到更大图，应改为 `deque`。非阻塞：当前规模下无实际影响。

### NB3. Field.Subfield CommRing 的 provenance quality difference 不够显著（explicit_only MAP 0.6607 vs hierarchy_mixed MAP 0.6887）

demo report Section 4.1 显示 Field.Subfield CommRing 上 hierarchy_mixed 的 MAP 反而略高于 explicit_only（0.6887 > 0.6607）。这与 T42 aggregate finding（HGCN 在 FS explicit_only 上大幅领先）的单点表现不完全一致。这本身不是 bug——单 query 与 aggregate 的方向不同是正常的——但 demo report 中对此没有解释。建议在 report 中加一句说明单 query 可以与 aggregate 方向不同。非阻塞：Order.Ring StrictOrderedCommRing 已经展示了足够显著的 provenance quality difference，满足了 acceptance criterion 2。

### NB4. Demo report 中使用了硬编码的绝对路径 `C:/ProgramData/anaconda3/envs/DLEnv/python.exe`

ancestor_explanation_demo_report.md:41, 69, 155 等处使用了项目环境特定的 Python 解释器路径。这对可移植性不利。建议在后续精修时改为通用的 `python` 命令。非阻塞：不影响功能或审查。

## Missing Tests

T52a 任务包的 `Verification` 块包含 3 类验证：

1. **任务包结构关键字段** — 已通过（rg 命令全部命中）
2. **关键概念覆盖率** — 已通过（rg 命令全部命中）
3. **编译检查** — 已通过（`python -m py_compile` PASS）

Worker 还在实际 artifact 上运行了 4 个 demo 命令（demo report Section 8），覆盖了：
- 两个候选图（field_subfield, order_ring）
- 两个模型类型（gcn, hgcn）
- single-query mode 和 comparison mode

这对一个 demo 任务来说是充分的验证覆盖。不需要额外的单元测试。

## Suspicious Implementation Details

### SD1. Ancestor ground truth 只用 `extends` 边构建，即使在 `hierarchy_mixed` 图上也是如此

proof_side_ancestor_explanation.py:140 只过滤 `edge_type == "extends"`。D033 已记录这是一个设计决策：无论 provenance mode 如何，ground truth 始终通过 extends 边追溯。这是正确的，因为 `instance_of` 边不构成层级祖先关系（synthesized 边是类型类实例化，不是数学层级继承）。

### SD2. `cosine_similarity` 函数对全图所有节点计算相似度

proof_side_ancestor_explanation.py:169-175 对所有节点计算 cosine similarity（包括 query 自身），然后在排序时跳过 query 自身。这是正确的实现。在全图规模（89-133 节点）下完全高效。

### SD3. `sys.path.insert(0, ...)` 导入 `common` 模块

proof_side_ancestor_explanation.py:22-23 将 `__file__` 所在目录插入 `sys.path` 来导入 `common.load_declaration_graph`。这与 T52a 任务包 Section 5 note 2 一致（"复用 `common.load_declaration_graph()` 的节点加载逻辑"）。由于脚本不修改任何已有文件，这是合理的 import 方式。

## Checklist Review

1. **Task goal met?** Yes. T52a 目标是实现 ancestor explanation demo CLI 脚本，支持 single-query 和 comparison mode，加载 T42 reviewed embeddings，输出 ranked ancestor list 和 retrieval metrics。所有验收标准均满足（demo report Section 7）。

2. **Stayed within Allowed files?** Yes.
   - `proof_side_ancestor_explanation.py` — 新建，在 Allowed Files 中
   - `ancestor_explanation_demo_report.md` — 新建，在 Allowed Files 中
   - `docs/04_task_board.md` — 更新时间戳 + 执行说明
   - `docs/05_decision_log.md` — 更新时间戳 + D033
   - `docs/07_handoff.md` — 更新时间戳 + item 77 + 下一步
   - `docs/08_risks_and_open_questions.md` — 更新时间戳 + R32 Mitigated
   - 未修改 `project_bootstrap/baseline_scaffold/src/` 下任何已有文件（git diff 确认）

3. **Avoided Forbidden scope?** Yes.
   - 未重新训练模型
   - 未修改任何已有 src 文件
   - 未引入新依赖（只使用 numpy, json, argparse, pathlib, collections）
   - 未实现 theorem proving
   - 未修改 proof_side_mvp.md, paper_outline.md, 06_eval_protocol.md
   - comparison mode 是硬边界，不是可选增强
   - 未把输出退化成纯祖先列表

4. **No mocks/stubs/hardcoded outputs?** Confirmed. `rg` 搜索未发现 mock, stub, hardcode, fake, dummy, TODO, FIXME, placeholder。所有 retrieval ranking 从 `node_embeddings.npy` 实时计算。

5. **Tests/verification adequate?** Yes. 编译检查通过，实际运行验证覆盖两个候选图 × 两个模型 × 两种模式。Order.Ring StrictOrderedCommRing 展示了戏剧性的 provenance quality difference（MAP 0.6438 vs 0.1492）。

6. **No behavioral regressions?** Yes. 未修改任何已有文件。

7. **Model/data contracts clear?** Yes. CLI 参数定义清晰，JSON 输出格式结构化（包含所有必要 key），artifact path 精确匹配 T42 约定。

8. **Safety limits present?** Yes. Node ordering sanity check 在 embedding shape 不匹配时报错退出（line 118-123）。

9. **Docs updated without claiming planned work as complete?** Yes. T52a 未在 task board 中被标记为完成（`[ ]` 仍保留在 T52 行，T52a 没有 checkbox 条目），handoff 明确写 "等待 adversarial reviewer 只读审查"。

10. **Risks documented?** Yes. R32 已从 Active 更新为 Mitigated，并记录了实际 sanity check 验证结果。

## Adversarial Review Additional Checks

T52a reviewer type 为 adversarial。额外检查：

1. **Artifact data alignment**: 脚本使用 `common.load_declaration_graph()` 加载图数据，并立即验证 `len(declarations) == embeddings.shape[0]`。已通过实际运行验证（89, 125, 133 节点均通过 shape check）。

2. **Provenance narrative correctness**: Demo report 中的数值与 T42 aggregate finding 方向一致（HGCN 在 explicit_only 上优于 hierarchy_mixed）。Order.Ring StrictOrderedCommRing 的 per-query MAP 差异（0.6438 vs 0.1492）是 T42 aggregate finding（+0.0557 MAP on OR explicit_only）的单点具象化。

3. **No benchmark validity regression**: 脚本不修改任何 benchmark 数据或配置。

4. **No over-engineering**: 脚本 ~490 行，结构清晰（CLI → helpers → data loading → ancestor graph → scoring → comparison → formatting → main），没有不必要的抽象。

5. **No hidden coupling**: 脚本只依赖 `common.load_declaration_graph()` 和 numpy，没有隐式依赖训练代码或其他 runner。

## Recommended Next Action

Captain 应：
1. 将 T52a 标记完成（在 task board 中更新执行说明）。
2. 将 D033 从 Pending Review 更新为 Accepted。
3. 将 T52 行勾选为 `[x]`，确认 Milestone 5 的 demo 任务完成。
4. 当前唯一任务切换为 T53（里程碑审查），判断项目进入 Continue / Narrow / Resume-ready。
5. Demo report 中的硬编码 Python 路径（NB4）和 FS 单 query 方向差异（NB3）可在后续 drafting 时精修。
