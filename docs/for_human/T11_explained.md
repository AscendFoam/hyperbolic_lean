# T11 Explained: Data Card

## 1. 通俗解释：这个任务在做什么？

如果 T10（版本锁定 manifest）做的是"清点仓库里有哪些设备和材料、各自是什么版本"，那么 T11 做的就是**给每一类材料写说明书**——

- 每张图里有哪些字段？每个字段是什么意思？
- 三种关系边（`uses`、`extends`、`instance_of`）分别代表什么语义？
- 有些图做了"覆盖率修复"（coverage-aware backfill），这意味着什么？没修复的又意味着什么？
- 哪些图可以用来做正式 benchmark？哪些只适合跑诊断？
- 还有哪些事情是我们**不知道**的？

这份说明书（`docs/data_card.md`）就是为了让后续做协议冻结（T12）、训练对齐（T30+）和 provenance 拆分（T40+）的人（或 AI）能快速理解每张图能干什么、不能干什么，而不是盲猜。

## 2. 实现详解

### 2.1 任务目标

根据任务包 `docs/tasks/M1_protocol/T11_data_card.md`，T11 的目标是：

> 写出当前可用图和数据资产的 data card，说明字段、relation 类型、coverage-aware 处理、unresolved 语义和使用限制。

### 2.2 任务流程

Worker 执行了以下步骤：

1. **阅读输入文档**：`docs/data_manifest.md`（T10 产出）、`data/processed/` 下的图数据、`artifacts/diagnostics/` 下的诊断报告。

2. **创建 `docs/data_card.md`**：新文件，包含八个部分：

   - **Scope**：明确文档覆盖范围——`data/processed/declaration_graph/` 和关联的诊断产物，不声称每张图 schema 完全一致。
   - **Observed Asset Layout**：描述当前图根的最小文件模式（`declarations.csv`、`edges.csv`、`stats.json`），指出 `labels.csv` / `splits.csv` 不是所有图根都有。
   - **Observed Field Schema**：详细列出 `declarations.csv`（19 列）、`edges.csv`（8 列）、`stats.json` 的观察字段和解读注意事项。例如 `source_commit` 是资产本地溯源，不等同于 `data_manifest.md` 中的正式版本锁定。
   - **Relation Semantics And Provenance**：解释 `uses / extends / instance_of` 的语义、`evidence_source` 的区分（`normalized_trace` vs `lean_meta_exact`），以及 provenance split 目前是通过派生目录表达而非 `edges.csv` 一等字段。
   - **Coverage-Aware Handling**：给出三条使用规则（回填、保留未解析、不强转负例），并用三个代表性图根的具体 `stats.json` 数据说明不同的 coverage 行为。
   - **Graph Families And Recommended Usage**：一张综合表，列出所有主要图族的特征、推荐用途和不推荐用途。
   - **Known Limitations**：三类限制——版本边界（引用 `data_manifest.md` 的 unknowns）、schema 边界（缺少一等 provenance 字段和标准化 labels/splits）、结构限制（关系层偏浅）。
   - **Usage Rules**：五条使用规则，特别强调不要把 `recommended usage` 误读为最终 benchmark 定稿。

3. **更新治理文档**：
   - `docs/04_task_board.md`：添加 2 条 Execution Note，更新 Project Status。
   - `docs/07_handoff.md`：补充 T11 草稿状态说明和 `recommended usage` 边界提醒。
   - `docs/08_risks_and_open_questions.md`：新增 R11（provenance split 不是一等字段的风险）和 Open Question #9（是否应在后续数据快照中加入一等 provenance 字段）。

4. **运行验证**：执行了任务包要求的 `rg` 检索和 `git diff`。

### 2.3 文件变化汇总

| 文件 | 变化类型 | 内容概要 |
| --- | --- | --- |
| `docs/data_card.md` | 新增 | 图资产字段模式、relation 语义、coverage-aware 规则、recommended usage 表、known limitations |
| `docs/04_task_board.md` | 修改 | Project Status 更新 + 2 条 Execution Note |
| `docs/07_handoff.md` | 修改 | 补充 T11 草稿内容和边界提醒 |
| `docs/08_risks_and_open_questions.md` | 修改 | 新增 R11 风险和 Open Question #9 |

### 2.4 对后续开发的意义

T11 的 data card 是 Milestone 1（Data And Protocol Freeze）的第二块拼图，与 T10 的 manifest 互补：

- **T12（协议固化）** 将引用 data card 中的字段说明和 relation 语义来确认评测代码的字段映射。
- **T20+（诊断与候选图筛选）** 将依据 Section 6 的 recommended usage 表来选择正式 benchmark 图。
- **T40+（provenance split）** 将解决 R11 风险——把 provenance 标签从派生目录名升级为 `edges.csv` 的一等字段。
- **T30+（训练对齐）** 将受益于 Section 7.2 指出的 schema 边界——知道 `labels.csv` / `splits.csv` 尚未标准化，需要先补齐。

特别是 Section 6 的 recommended usage 表，为后续实验提供了清晰的"哪些图适合什么用途"的参考，避免了"随便拿一张图就跑 benchmark"的风险。

## 3. 为什么给出 PASS 的 review 结果？

### 审查过程

1. **任务完成度**：任务包要求图列表、字段说明、relation provenance、known limitations、recommended usage 五类内容，data card 全部覆盖。
2. **范围合规**：`git status` 确认只有 `Allowed files` 被修改，数据文件和 artifact 未触碰。
3. **数据准确性**：我抽查了三个代表性图根的 `stats.json`，data card 中引用的所有边数量、coverage-aware backfill 参数、skipped 数值均与实际文件完全一致。CSV 列头也与 data card 中的字段描述完全匹配。
4. **provenance 声明**：`_explicit_only` / `_synthesized_only` 目录确实存在于 `data/processed/declaration_graph/` 下，印证了 data card 关于 provenance split 通过派生目录表达的描述。
5. **诚实性**：未解析的字段保持为未解析，没有编造版本信息，没有把 coverage 不可靠的数据写成可靠标签。
6. **治理一致性**：三份治理文档的更新相互一致，新增的 R11 和 Open Question #9 准确地将 provenance schema 不足与 Milestone 4 关联。
7. **未越权完成**：Worker 没有把 T11 标记为完成，等待 reviewer 结论。

### 判决理由

- 任务包目标全部达成，没有遗漏。
- 所有定量声明都通过了交叉验证。
- 没有伪实现、mock、stub 或 hardcode——这是一份纯文档任务，所有信息都来自仓库内可验证的文件。
- 没有破坏已有功能。
- 没有把计划写成事实——draft 标注清晰，usage rules 明确警告不要过度解读。
- 推荐用途表（Section 6）既给出了正面建议，也给出了"不推荐"的边界，这比只说"可以用于什么"更严格。

因此判定为 **PASS**，无 blocking 或 non-blocking issues。
