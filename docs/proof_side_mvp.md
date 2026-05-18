# T51 Proof-Side MVP Selection

> Status: Worker draft — awaiting review.
>
> Updated: 2026-05-18

---

## 1. Task Context

`T50` 已在 `docs/paper_outline.md` Section 9 中明确 proof-side bridge 的必要性：论文当前只有 pipeline / protocol / diagnostics / provenance-conditional finding，缺少一个下游 proof-engineering 任务来证明图表示质量的差异在实践中有意义。`T51` 的目标是从候选方向中选出一个最小可行 MVP，明确其输入、输出、验收标准、失败标准与不做事项，为 `T52` demo 任务包提供直接可执行的规格。

## 2. Candidate Comparison

### 2.1 Candidate A: Ancestor Explanation

**描述。** 给定一个 declaration，用 grouped retrieval 模型检索并排序其真祖先，附带 relation type（`extends` / `instance_of`）和层级路径信息。输出是一份带 provenance 标注的祖先排序列表，用户可直观看到哪些 hierarchy 路径贡献了该声明的数学语境。

**与论文贡献的直接映射：**

| 论文贡献 | Ancestor Explanation 对应 |
| --- | --- |
| C1 (Pipeline) | 直接使用 pipeline 产出的 declaration graph 和 precise hierarchy |
| C2 (Grouped Retrieval Protocol) | 查询结构就是 grouped multi-positive ancestor retrieval |
| C3 (Diagnostics) | 诊断框架预测的"哪些图适合双曲"直接影响 ancestor retrieval 质量 |
| C4 (Provenance-Conditional Finding) | 在 `explicit_only` vs `synthesized_only` vs `hierarchy_mixed` 上的 retrieval 质量差异就是 MVP 要展示的核心 |
| C5 (Training Alignment) | grouped retrieval training 的输出 embedding 直接驱动 ancestor ranking |

**复杂度：** Low。不需要新模型、新数据源或新训练流程；只需把已有 model output 包装成用户可读的 explanation 界面。

**Paper fit：** 直接延伸 C2 和 C4，让 provenance-conditional finding 变成可体验的工具而非抽象数字。

### 2.2 Candidate B: Relation-Aware Declaration Recommendation

**描述。** 给定一个部分构建的 import/extends 链，推荐下一个相关的 declaration。这是一个基于图结构的导航任务。

**与论文贡献的映射：**

| 论文贡献 | Declaration Recommendation 对应 |
| --- | --- |
| C1 / C2 | 使用已有图和 protocol |
| C4 | 可以展示 provenance 对推荐质量的影响 |
| 无直接映射 | 需要定义"部分链"的语义和推荐目标函数，这与当前 protocol 不直接对齐 |

**复杂度：** Medium。需要定义"部分链 → 推荐"的任务规格、训练/评测协议和 baseline，这超出了当前 pipeline 的已有能力。

**Paper fit：** 间接延伸 C4，但需要额外的任务定义和实验来证明有效。对 ITP/CPP 来说更像是 future work 而非 MVP demo。

**关键风险：** 当前 pipeline 没有"部分链"的训练信号或评测入口；从零定义这个任务可能导致 T52 scope 膨胀。

### 2.3 Candidate C: Premise Retrieval Demo

**描述。** 用 learned embedding 辅助 LeanDojo 风格的 premise retrieval，给定 proof state 或 theorem statement 检索相关前提。

**与论文贡献的映射：**

| 论文贡献 | Premise Retrieval 对应 |
| --- | --- |
| C1 | 需要桥接 declaration graph 和 LeanDojo premise data |
| 无直接映射 | premise retrieval 的任务结构与 ancestor retrieval 不同 |

**复杂度：** High。需要：(1) 桥接 declaration graph 与 LeanDojo proof state 数据；(2) 定义 graph embedding → premise scoring 的映射；(3) 在 LeanDojo benchmark 上评测。这至少需要一个完整的额外实验迭代。

**Paper fit：** 最有野心的方向，但与当前论文中心叙事（provenance-conditional hierarchy finding）距离最远。容易把论文拉成"图表示 + proof retrieval"的双线叙事，稀释中心 claim。

**关键风险：** 引入 LeanDojo 作为新依赖（违反 forbidden scope）；任务定义和评测协议需要从零设计；即使 demo 跑通，也无法直接服务于 provenance-conditional finding 的核心叙事。

### 2.4 Comparison Summary

| Dimension | A: Ancestor Explanation | B: Declaration Recommendation | C: Premise Retrieval |
| --- | --- | --- | --- |
| Complexity | Low | Medium | High |
| Direct mapping to C2 | Yes | Partial | No |
| Direct mapping to C4 | Yes (provenance quality difference is the demo) | Indirect | Indirect |
| Needs new training/protocol | No | Yes (new task definition) | Yes (new pipeline bridge) |
| New dependencies | None | None | LeanDojo (forbidden) |
| ITP narrative fit | Natural tool for hierarchy navigation | Useful but not directly reviewed | Too ambitious for current scope |
| CPP tool/demo angle | Lightweight provenance-aware explorer | Medium | Requires full integration |
| Risk of scope creep | Low | Medium (need to define task) | High (new pipeline + benchmark) |
| Addresses R31 | See Section 3 | Stronger by default | Stronger by default but infeasible |

## 3. Selection: Ancestor Explanation

**决策：** 选择 **Candidate A: Ancestor Explanation** 作为 proof-side MVP。

### 3.1 Why Ancestor Explanation Over Alternatives

1. **直接服务于论文中心 claim。** Ancestor explanation 的核心 demo 就是：同一个 declaration 在 `explicit_only` 图上的 ancestor retrieval 质量高于 `hierarchy_mixed`（对 HGCN 而言），而 `synthesized_only` 上 retrieval 退化为 trivial。这把 provenance-conditional finding 从表格数字变成用户可体验的质量差异。

2. **零新依赖、零新训练。** 已有的 grouped retrieval model output 和 T32/T33/T42 artifact 直接可用。T52 只需把这些 artifact 包装成可读的 explanation 输出。

3. **与 ITP/CPP venue fit 高度对齐。** ITP 读者最关心的不是模型架构，而是"这个工具能否帮助我理解 formal-math hierarchy"。Ancestor explanation 直接回答这个问题。CPP 读者看重 artifact 和 tooling；一个 provenance-aware hierarchy explorer 天然是 tool contribution。

4. **风险可控。** 不需要定义新任务、新评测协议或新数据源。失败模式清晰（见 Section 5）。

### 3.2 Response to R31: Why Ancestor Explanation Is Not Too Lightweight

`R31` 担心 ancestor explanation 可能"过于轻量，不足以支撑 CPP 的 tool/demo 要求"。本节正面回应这一风险。

**Ancestor explanation 不是"列出祖先"。** 如果 MVP 只是调用一个 API 返回 sorted ancestor list，那确实过于轻量。但实际的 ancestor explanation MVP 要展示的是：

1. **Provenance-aware quality difference。** 同一个 declaration 的 ancestor retrieval，在三种 provenance split（`explicit_only` / `synthesized_only` / `hierarchy_mixed`）上给出不同的质量和覆盖度。用户看到的不是"这是祖先列表"，而是"你包含了 synthesized 边之后，检索质量发生了这样的变化"。

2. **Hop-depth-dependent quality gradient。** 利用 hop bucket 分析，展示 deeper ancestor 在不同 geometry 下的检索难度差异。这直接把 paper 的 Fig 3（hop-bucket HGCN vs GCN delta）变成可交互的 proof-engineering 视角。

3. **Concrete proof-engineering utility。** 对于正在理解一个复杂 typeclass hierarchy 的 proof engineer，知道哪些 ancestor 来自 `extends`（显式层级）、哪些来自 `instance_of`（编译器合成）具有直接实用价值。当前 Mathlib 文档工具（`doc-gen4`）不提供这种 provenance-aware hierarchy 导航。

**与 CPP tool demo 标准的对照：**
- CPP artifact evaluation 要求 artifact is functional and reusable。一个能对任意 reviewed candidate graph declaration 运行 provenance-aware ancestor retrieval 的 CLI 工具，满足这个标准。
- CPP 论文不要求 end-to-end proving；tool demo 需要展示 tool solves a real problem。Ancestor explanation 解决的是"hierarchy navigation quality depends on edge provenance"这个真实问题。
- 相比之下，premise retrieval demo（Candidate C）虽然更野心勃勃，但它引入的复杂度和新依赖使得在 T52 单一任务包内完成的风险极高，且与论文中心 claim 的距离更远。

**结论：** Ancestor explanation 作为 proof-side MVP 不是因为它最轻，而是因为它与 provenance-conditional finding 的映射最直接、scope 最可控、对 ITP/CPP venue 的叙事贡献最清晰。如果 reviewer 仍然认为它不够强，T52 可以在 demo 任务包中加入一个 provenance-aware hierarchy comparison mode 作为增强项，而不需要切换到完全不同的 MVP 方向。

## 4. MVP Specification

### 4.1 Inputs

| Input | Type | Source | Notes |
| --- | --- | --- | --- |
| Declaration name | String (fully qualified) | User input | e.g., `Mathlib.Algebra.Field.Subfield` |
| Candidate graph | Selection | Predefined: `Field.Subfield` or `Order.Ring` | The two reviewed candidate graphs |
| Provenance mode | Selection | `explicit_only` / `synthesized_only` / `hierarchy_mixed` | User chooses which split to query |
| Model type | Selection | `GCN` / `HGCN` | Which trained model to use |

### 4.2 Outputs

| Output | Type | Description |
| --- | --- | --- |
| Ranked ancestor list | List of (ancestor_name, relation_type, score) | Sorted by retrieval score, with provenance tag (`extends` or `instance_of`) |
| Ground truth comparison | List of true ancestors | From the declaration graph, for quality evaluation |
| Retrieval metrics | MAP, nDCG, Recall@k | Computed against ground truth for this single query |
| Hop-depth breakdown | Per-hop ancestor mapping | Which ancestors are at hop 2, 3, 4+ |
| Provenance comparison | Side-by-side metrics across splits | Same query under `explicit_only` vs `hierarchy_mixed` |

### 4.3 Acceptance Criteria

MVP 被视为成功当且仅当以下条件全部满足：

1. **Functional completeness.** 给定任意 reviewed candidate graph 中的 declaration name 和 provenance mode，工具能输出 ranked ancestor list 和 retrieval metrics。

2. **Provenance quality difference visible.** 在至少一个 declaration 上，`explicit_only` 模式下 HGCN 的 ancestor retrieval 质量高于 GCN（与 T42 reviewed findings 一致），而 `hierarchy_mixed` 模式下 GCN 不低于 HGCN。这种差异在输出中可直接对比。

3. **No new model training required.** MVP 使用 T32/T33/T42 已产出的 model artifact 或 embedding，不重新训练。

4. **No new dependencies beyond existing pipeline.** 不引入 LeanDojo、新 embedding 库或其他大型依赖。

5. **CLI or script interface.** 提供至少一个命令行入口，输入 declaration name + options，输出 structured result（JSON 或 formatted text）。

6. **Paper bridge documented.** 在 demo 输出或 README 中明确说明：这个工具是论文 provenance-conditional finding 的 downstream manifestation，不是独立的新贡献。

### 4.4 Failure Criteria

MVP 被视为失败如果以下任一条件发生：

1. **Provenance difference not reproducible in demo.** 如果在 demo 中无法复现 T42 reviewed 的 provenance-conditional quality difference（即 demo 输出与 reviewed artifact 矛盾），则 MVP 失败。此时应调查 artifact loading 或 query construction 的 bug，而不是调整数值。

2. **Scope expands beyond single-task demo.** 如果 T52 的实现需要新模型训练、新数据源、新评测协议或新的大型依赖，说明 MVP scope 失控。

3. **Quality difference is only numeric, not interpretable.** 如果输出只是原始 metric 数值，而无法让 proof engineer 理解"为什么这个祖先在 explicit_only 上排名更高"，则 MVP 不满足 tool demo 标准。

### 4.5 Exclusions (What T51/T52 Will NOT Do)

1. 不实现端到端 theorem proving。
2. 不把 proof-side MVP 写成"已证明可提升完整证明成功率"。
3. 不引入新的大型依赖（LeanDojo、新 embedding 库等）。
4. 不修改 T50 已确认的 provenance-conditional 论文口径。
5. 不把 ancestor explanation 升级为正式 benchmark task 或新 evaluation protocol——它是一个 demo，不是 protocol extension。
6. 不在 ancestor retrieval 之外开辟新的 proof-side 支线（如 premise retrieval 或 declaration recommendation）。

## 5. Paper Bridge Narrative

### 5.1 How Ancestor Explanation Serves the Paper

The ancestor explanation MVP bridges the gap between "provenance-conditional retrieval quality difference" (Tables 4-5, Fig 3-4 in the paper) and "this difference matters to proof engineers." Specifically:

- **Table 4** shows GCN vs HGCN MAP across splits → **MVP shows** the same comparison for a specific declaration, making the table entries tangible.
- **Fig 3** shows hop-bucket HGCN advantage → **MVP shows** which specific deep ancestors are correctly retrieved by HGCN but missed by GCN on `explicit_only`.
- **Fig 4** shows provenance-conditional summary → **MVP lets the user toggle** between splits and see quality change interactively.

### 5.2 Where It Fits in the Paper

- **Section 11 (Conclusion):** "We demonstrate the practical relevance of the provenance-conditional finding through an ancestor explanation tool that shows how edge provenance directly impacts the quality of hierarchy navigation for proof engineers."
- **Optional Section 8 (Discussion):** A paragraph connecting ancestor explanation to future proof-engineering tools.
- **Artifact package:** The CLI tool itself as a functional artifact for CPP/ITP artifact evaluation.

## 6. Open Items for T52

T52 需要在本 MVP 选择基础上完成以下工作：

1. 确定 demo 的具体代码入口（是在现有 `project_bootstrap/baseline_scaffold/src/` 下新增 script，还是独立 script）。
2. 确定 model artifact loading 方式（直接加载 T42 的 embedding output，还是加载 checkpoint 重新 inference）。
3. 设计 provenance comparison mode 的输出格式（side-by-side table、JSON diff、或 formatted text）。
4. 编写 T52 任务包的 allowed files、forbidden scope 和 verification commands。
5. 确保不引入新依赖、不重新训练模型、不修改已有 protocol。

---

## Verification

```powershell
rg -n "ancestor explanation|declaration recommendation|premise retrieval|MVP|failure" docs\proof_side_mvp.md
```
