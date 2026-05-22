# 01 Feasibility Report

> 更新时间：2026-05-22（T56 review 后更新）
>
> 结论：Go，条件是先完成协议冻结、数据资产化和任务治理，再推进新实验。

## 1. 问题定义

项目要回答的问题不是“是否能训练一个双曲模型”，而是：

> 在真实 traced Lean / Mathlib hierarchy 图上，怎样定义可复现、可比较、可解释的任务协议，并系统判断双曲归纳偏置的适用条件。

工程对象包括：

- traced repo
- normalized trace
- declaration graph
- precise `extends / instance_of`
- coverage-aware relation graph
- grouped multi-positive ancestor retrieval
- relation-aware baseline 与结构诊断

## 2. 相关工作矩阵

| 类别 | 代表工作或工具 | 已覆盖内容 | 本项目差异化点 |
| --- | --- | --- | --- |
| Lean tracing / proof data | LeanDojo, LeanDojo-v2, lean-training-data, jixia, Pantograph | proof state、premise、AST、trace 数据 | 面向 hierarchy relation 图的标准任务协议和结构诊断闭环 |
| Lean graph export | importGraph, lean4export, doc-gen4 | import graph、declaration export、文档结构 | 进一步构建 relation-aware benchmark 与 grouped retrieval |
| Mathlib network analysis | mathlib-network, The Network Structure of Mathlib, ProofGraph | 基础图统计、依赖网络、网络科学分析 | 将结构诊断与模型表现、任务口径和失败条件绑定 |
| 双曲图学习 | Poincare Embeddings, HGCN, Lorentz/HNN 变体 | 通用层级图建模 | 在 Lean hierarchy 真实数据上做条件性适用性分析 |
| Proving retrieval | premise retrieval, proof-state retrieval 系列 | 面向证明搜索的检索 | 后续可把 hierarchy graph 表示迁移到 proof-side utility |

## 3. 最像的 5 个已有工作

1. LeanDojo：最接近的数据与 proving workflow 基础设施。
2. mathlib-network：最接近的 Mathlib 图数据和网络结构分析。
3. ProofGraph：最接近的 proof assistant 图结构研究原型。
4. The Network Structure of Mathlib：最接近的 Mathlib 多层网络分析论文。
5. HGCN / Poincare Embeddings：最接近的双曲归纳偏置方法基础。

这些工作说明“导出图”和“一般双曲模型”不是充分创新点。项目必须强调协议、诊断、任务定义和真实 formal-math hierarchy 图上的条件性结论。

## 4. 可差异化点

1. 真实 traced repo 到 relation-aware hierarchy benchmark 的完整工程管线。
2. precise hierarchy 与 coverage-aware repair，而不是粗糙字符串或 import-level 图。
3. grouped multi-positive ancestor retrieval 协议，修正旧单正例 ranking。
4. hop bucket、relation provenance、图结构诊断与模型表现的联合解释。
5. 把双曲负结果写成结构性诊断，而不是简单调参失败。
6. 后续可接 proof-side task，提升到 theorem proving workflow 价值。

## 5. MVP 实验

MVP 应由三个最小闭环组成：

1. 数据与协议冻结：版本 manifest、data card、config index、默认 grouped retrieval 指标。
2. 诊断与筛图：对现有 `lean4-example`、`plausible`、`batteries`、Mathlib 模块候选输出结构诊断和优先级。
3. 同口径 baseline：在至少两个模块图上运行 GCN / HGCN 5-seed grouped retrieval，并保留 hop bucket 结果。

## 6. 风险

1. 数据规模与 tracing 成本失控，尤其是 full Mathlib。
2. relation layer 过浅，无法支撑双曲优势主张。
3. 训练目标仍停留在 binary edge classification，和 grouped retrieval 评测错配。
4. synthesized relation 语义复杂，可能扭曲层级信号。
5. 论文叙事过散，贡献被已有 export / graph analysis 工作稀释。
6. 治理文档与实验产物不同步，导致后续 worker 重复劳动。

## 7. Go / No-Go 判断

Go：

- 已有足够工程资产支持继续推进。
- 已有真实负结果和结构诊断支持更稳的 benchmark / protocol / diagnostics 叙事。
- 下一步任务可拆成小型 worker 包，不需要一次性大改。
- `T00` 已通过 review，说明根目录治理入口已经达到继续推进的最低要求。
- `T01` 已通过 review with warnings accepted，说明治理一致性复查可以收口。
- `T10` 已通过 review，版本锚点与数据资产入口已形成 reviewed manifest。
- `T11` 已通过 review，当前可用图、字段、relation provenance、coverage-aware 边界和 recommended usage 已形成 reviewed data card。
- `T12` 已通过 adversarial review，grouped multi-positive ancestor retrieval 的代码入口、配置字段、指标名和核心输出字段已形成 reviewed protocol freeze。
- `T13` 已通过 adversarial review，hop bucket 常规报告入口已接入单次 runner summary 与 seed sweep report；review 留下的重复 helper 与端到端 spot-check 作为后续轻量清理跟踪。
- `T14` 已通过 normal review，最小 smoke 已真实落盘 `grouped_test_ndcg_at_10` 与 `hop_2 / hop_3 / hop_4_plus` 字段，Milestone 1 可视为闭合。
- `T20` 已通过 review with warnings，现有诊断产物已经形成 provisional candidate priority；其中 `mathlib_algebra_order_d3` 是最强候选，`mathlib_algebra_order_ring_d4` 是实用 fallback，部分表格精修留作后续。
- `T21` 已通过 review，module-level candidate scan audit 进一步确认 `Mathlib.Algebra.Order.Ring` 是当前最平衡的 follow-up 候选，`Mathlib.Algebra.Order` 更适合作为 depth stress-test；raw hierarchy score 偏向小而紧凑模块的风险已进入后续阈值治理。
- `T22` 已通过 review，`docs/diagnostics_protocol.md` 把 shallow forest / star forest、positive scale、component ratio 与 closure expansion 等判断固化为 reviewed heuristic diagnostics protocol；该协议仍不是理论证明或最终 benchmark 排名。
- `T30` 已通过 review，`docs/training_alignment_audit.md` 确认当前训练仍是 edge-level BCE，并发现 grouped retrieval 的 P0 前置风险：同一 `(src, relation)` query 可能跨 split 被拆碎。
- `T31A` 已通过 adversarial review，grouped ancestor retrieval 的 query-level split completeness 已收口；同一 `(src, relation_type)` query 不再跨 `train / val / test`，且 disjointness 摘要已写入 run manifest。
- `T31` 已通过 adversarial review，grouped retrieval runner 的最小 query-grouped loss 路径已收口；训练 query、split 与 eval 使用同一 `(src_id, relation_type)` key，best checkpoint 改由 grouped val MAP 驱动。
- `T34` 已通过 milestone review，Milestone 3 的 grouped-vs-binary 诊断总结已收口；当前下一步切换为 `T40`，进入 provenance split 配置冻结。

No-Go 条件：

- 若无法冻结数据快照和 grouped 协议，则暂停实验。
- 若所有候选图都过浅且无法接 proof-side utility，则项目应转为纯经验报告或归档。
- 若后续只剩“继续调 HGCN 直到赢”，则不应继续作为主线。

当前下一步是执行 `T57`：`T56` 已经通过 review 并被判定为 `PASS`，说明 publication-facing precision cleanup 已经到位。`R29` 已修正，`R28` 已基于现有 reviewed artifact 的根因解释合法关闭。这个阶段不应回到新实验或新 demo，而应把稳定下来的数字边界转成 figure/table source rendering，并顺手处理 `T56_review` 留下的非阻塞表达精修（summary table 粒度统一、Section 5.4 长解释段压缩）。artifact packaging 继续作为下一步单独任务；`R30` 与 clean-environment reproducibility (`R25`) 边界继续保留。



