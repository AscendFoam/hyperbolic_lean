# 00 Raw Idea

> 更新时间：2026-05-17
>
> 项目名称：形式化图谱双曲化
>
> 状态：Go，已从原始假设推进为工程化 benchmark / protocol / diagnostics 主线。

## 1. 解决什么问题

本项目研究真实 traced Lean / Mathlib formal-math hierarchy 图能否支持稳定、可复现、可解释的图表示学习实验，尤其是检验双曲归纳偏置在什么结构条件下可能有效。

原始动机是“Lean/Mathlib hierarchy 具有层级结构，因此双曲表示可能优于欧氏表示”。截至 2026-05-09 的实验表明，强版本命题不能作为默认承诺。当前更准确的问题是：

> 如何构建一套面向真实 traced formal-math hierarchy 图的可复现实验管线、标准化 grouped retrieval 协议和结构诊断框架，并据此判断双曲几何何时值得使用。

## 2. 为什么现在值得做

1. Lean / Mathlib 生态已有 tracing、export、proof data 工具，但公开工作中尚缺一套围绕真实 hierarchy relation 图的统一任务协议和公平 baseline 对照。
2. 项目已经积累了可复用工程资产，包括 trace normalize、declaration graph、precise hierarchy、coverage-aware repair、relation-aware baseline 和 graph diagnostics。
3. 已有结果暴露出一个有价值的研究问题：真实 formal-math hierarchy 图常常是浅层、碎片化、叶子占优的 forest，而不是深层稳定树。
4. grouped multi-positive ancestor retrieval 已经修正了旧的单正例 ranking 口径，为 benchmark 化提供了清晰抓手。

## 3. 最小可验证实验

最小闭环不是继续调单个 HGCN，而是完成以下可验证链路：

1. 固定一个数据快照和版本 manifest。
2. 从 relation-aware 子图生成 grouped ancestor retrieval 任务。
3. 以相同 split、seed、候选集合和指标运行 GCN / HGCN 对照。
4. 输出 `Recall@k`、`MAP`、`nDCG`、`grouped-MRR` 和 hop bucket 结果。
5. 同时输出结构诊断，说明该图是否具备深层 hierarchy 条件。

首轮正式 worker 任务应先完成治理与协议冻结，再推进代码和实验。

## 4. 最相似已有工作

这些工作覆盖了相邻空间，但没有完整替代当前项目：

1. LeanDojo / LeanDojo-v2 / lean-training-data / jixia / Pantograph：提供 proof assistant 数据抽取与 theorem proving 任务基础。
2. lean4export / importGraph / doc-gen4：提供 declaration、import、文档层导出能力。
3. mathlib-network / The Network Structure of Mathlib / ProofGraph：提供 Mathlib 图结构分析和网络科学视角。
4. Poincare Embeddings / HGCN / Lorentz 或 hyperbolic GNN 系列：提供通用双曲图表示方法。
5. premise retrieval 与 proof-state retrieval 相关工作：覆盖 proving workflow 下游应用。

本项目的差异化点在于把 traced hierarchy 图、precise relation、coverage-aware repair、grouped retrieval 协议、结构诊断和 GCN/HGCN 公平对照连成闭环。

## 5. 失败标准

满足以下任一条件时，应暂停或缩窄项目，而不是继续扩大实验：

1. 无法锁定可复现数据快照、版本和评测入口。
2. grouped retrieval 协议无法稳定生成，或正例定义无法复查。
3. 结构诊断无法区分浅层 forest 与更深层 hierarchy。
4. 欧氏强 baseline、文本/启发式 baseline 和双曲 baseline 不能同口径比较。
5. 结果只能支持“某次 HGCN 小幅波动”，不能支持 benchmark / protocol / diagnostics 叙事。
6. proof-side 或论文叙事无法从现有 link prediction 扩展出清晰贡献。

## 6. 当前裁决

Go，但主线已收束：

- 不再以“证明双曲优于欧氏”为默认目标。
- 以“真实 traced formal-math hierarchy 图 benchmark / protocol / diagnostics”为主目标。
- 双曲模型保留为条件性研究对象，只有在更深、更纯层级、更低维或特定 hop bucket 上形成稳定收益时，才升级为主结论。

## 7. 治理启动状态

- 2026-05-10：`T00` 已通过 reviewer 判定 `PASS`，根目录入口文档已建立。
- 2026-05-10：`T01` 已通过 reviewer 判定 `PASS_WITH_WARNINGS`，warnings 已接受并闭合；当前唯一任务切换为 `T10`。
- 2026-05-10：`T10` 已通过 reviewer 判定 `PASS`；当前唯一任务切换为 `T11`，用于写出 data card。
- 2026-05-10：`T11` 已通过 reviewer 判定 `PASS`；当前唯一任务切换为 `T12`，用于冻结 grouped retrieval 协议、代码入口、指标名与输出格式。
- 2026-05-11：`T12` 已通过 adversarial reviewer 判定 `PASS`；当前唯一任务切换为 `T13`，用于校验 hop bucket 常规报告入口。
- 2026-05-11：`T13` 已通过 adversarial reviewer 判定 `PASS`；当前唯一任务切换为 `T14`，用于做 Milestone 1 收口 smoke check 与轻量清理，不执行大规模实验。
- 2026-05-12：`T14` 已通过 normal reviewer 判定 `PASS`；Milestone 1 数据与协议冻结闭合，当前唯一任务切换为 `T20`，进入诊断与候选图选择。
- 2026-05-12：`T20` 已通过 reviewer 判定 `PASS_WITH_WARNINGS`；warnings 已延后到后续文档精修，当前唯一任务切换为 `T21`。
- 2026-05-12：`T21` 已通过 reviewer 判定 `PASS`；module-level candidate scan audit 将 `Mathlib.Algebra.Order.Ring` 提升为最平衡的下一步候选，当前唯一任务切换为 `T22`。
- 2026-05-13：`T22` 已通过 reviewer 判定 `PASS`；`docs/diagnostics_protocol.md` 成为 reviewed heuristic diagnostics protocol，当前唯一任务切换为 `T30`。
- 2026-05-13：`T30` 已通过 reviewer 判定 `PASS`；审计确认训练仍是 edge-level BCE，且 grouped query 可能被 edge-level split 拆碎；当前唯一任务切换为 `T31A`，先修 query-level split completeness。
- 2026-05-13：`T31A` 已通过 adversarial reviewer 判定 `PASS`；`ancestor_ranking` / grouped ancestor retrieval 已切到 query-level split，并通过 smoke 验证 `run_manifest.json` 中 query overlap 为 0；当前唯一任务切换为 `T31`，用于实现最小 query-grouped loss。
- 2026-05-16：`T31` 已通过 adversarial reviewer 判定 `PASS`；grouped retrieval runner 已具备最小 query-grouped training 路径，训练、split 与 eval 共用 `(src_id, relation_type)` query key，并用 grouped val MAP 做模型选择；当前唯一任务切换为 `T32`，用于运行 GCN 5-seed grouped training sweep。
- 2026-05-17：`T32` 已通过 adversarial reviewer 判定 `PASS`；已完成两组真实 5-seed GCN grouped training sweep，当前唯一任务切换为 `T33`，用于在相同 split 和参数预算下运行 HGCN 对照。
- 2026-05-17：`T33` 已通过 adversarial reviewer 判定 `PASS`；HGCN grouped 5-seed 对照已在与 `T32` 完全匹配的 grouped protocol 下收口，当前唯一任务切换为 `T34`，用于汇总 grouped training 与旧 binary training 的差异并写出可比性诊断。
- 2026-05-17：`T34` 已通过 milestone reviewer 判定 `PASS`；Milestone 3 的 grouped-vs-binary 总结已收口，当前唯一任务切换为 `T40`，进入 provenance split 配置冻结。
- 2026-05-17：`M3_review` 判定为 `PASS_WITH_WARNINGS`；允许进入 Milestone 4，但不应把当前证据升级为“已完成 clean-room reproducibility”或“已证明 HGCN 整体优于 GCN”。
- 2026-05-17：`T40` 已通过 adversarial reviewer 判定 `PASS`；provenance split 配置与协议冻结已完成，当前唯一任务切换为 `T41`，用于实际生成六个 provenance split 图目录、校验预期边数并运行结构诊断。
- 2026-05-17：T41 已通过 adversarial reviewer 判定 PASS；六个 provenance split 图已真实落盘并完成结构诊断，结论表明 explicit_only 才承载层级深度，synthesized_only 是 trivial controlled diagnostic，hierarchy_mixed 只作为 full-graph reproducibility check；当前唯一任务切换为 T42。


