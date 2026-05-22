# T53 Milestone Review

> Reviewer: Claude Code (milestone)
> Date: 2026-05-19
> Scope: Milestone 1–5 全部已 reviewed 产物的阶段性审查

## Verdict: Narrow

项目应从"继续开发实验"收窄为"paper-facing / packaging / cleanup"。

核心理由：五个 Milestone 的 reviewed 证据链已经闭合，核心 provenance-conditional finding 已通过 adversarial review 确立，proof-side bridge 已从 paper story 变成可运行 CLI demo。当前不需要新的实验 sweep、新模型、新数据源或新 demo；最紧迫的工作是把已有证据整理成可投稿的论文和 artifact package。

## 1. 总述

项目从 Milestone 0 到 Milestone 5 走完了完整的证据闭环：

1. **M1 (数据与协议冻结)**：version manifest、data card、grouped retrieval protocol、hop-bucket reporting、smoke-verified 输出链。全部通过 adversarial review（T10–T14）。
2. **M2 (诊断与候选图选择)**：结构诊断框架、module-level candidate audit、heuristic diagnostics protocol。全部通过 review（T20–T22）。
3. **M3 (训练对齐)**：binary-to-grouped training migration、query-level split fix、matched GCN/HGCN 5-seed formal sweep、grouped-vs-binary 总结。全部通过 review，M3 milestone review 判定 `PASS_WITH_WARNINGS`（T30–T34）。
4. **M4 (Provenance 拆分)**：provenance split 协议冻结、split 图生成与结构诊断、provenance-aware 5-seed sweep、provenance-conditional synthesis。全部通过 adversarial review（T40–T43）。
5. **M5 (论文与 Proof-Side Bridge)**：paper skeleton（5 contributions、evidence ladder、figures/tables plan、venue fit）、proof-side MVP 选择（ancestor explanation）、demo 任务包设计、demo CLI 实现。全部通过 review（T50–T52a）。

核心 provenance-conditional finding——"HGCN 仅在 `explicit_only` 层级图上优于 GCN，`hierarchy_mixed` 上 GCN 仍领先"——已经由 T42 的 60 次训练（零失败）确立，经 T43 收口、T50 paper skeleton 保持、T52a demo 验证。这一发现是 provenance-composition 条件性的，不是"HGCN 稳定优于 GCN"的通用主张。

**为什么是 Narrow 而不是 Continue：**

- 所有实验管线已 closed-loop，继续跑新 sweep 的边际收益极低。
- 论文骨架已就绪但尚未进入正式 drafting（LaTeX、figure rendering、table formatting）。
- 仍有精度问题（R28、R29）和页数预算问题（R30），这些都是 paper-facing 收窄工作，不是实验工作。
- Proof-side demo 已完成并通过 adversarial review，不需要新 demo 或新 proof-side 支线。

**为什么是 Narrow 而不是 Resume-ready：**

- 项目距离可投稿状态仍差一个完整的 paper drafting 周期（估计 1–2 个 task batch）。
- R28/R29 的精度修复和 R30 的贡献合并决策需要在 drafting 过程中解决，而不是暂停等待。
- Artifact packaging（将 `project_bootstrap/` 和 `artifacts/` 整理为可提交的 CPP artifact bundle）需要主动工作，不能仅靠"暂停"完成。

## 2. Evidence

### 2.1 Protocol / Governance 是否闭环

**结论：闭环。**

- M1 建立了 version manifest（T10）、data card（T11）、grouped retrieval protocol（T12）和 hop-bucket reporting（T13/T14），全部通过 adversarial review。
- M3 建立了 query-level split（T31A）和 grouped retrieval training（T31），在 `Field.Subfield` 与 `Order.Ring` 上完成 5-seed GCN/HGCN matched sweep（T32/T33）。
- M4 冻结了 provenance split 配置（T40）并程序化验证了 `hierarchy_mixed = full source graph` identity（T41）。
- 5-seed reproducibility 已在 T42 hierarchy_mixed split 上 byte-identical 确认（与 T32/T33 完全一致）。
- 治理闭环：每个 task 有 Allowed Files、Forbidden Scope、Verification commands、review verdict、governance sync。

唯一未闭合的 protocol 级缺口是 R25（clean-environment reproducibility），但这不影响当前 reviewed 证据的有效性，只限制对外宣称强度。

### 2.2 Grouped Benchmark 是否已 reviewed

**结论：已 reviewed。**

- T32 (GCN) 和 T33 (HGCN) 的 matched grouped 5-seed sweep 已通过 adversarial review。
- T34 总结报告已通过 review，明确区分了 matched grouped sweep 与历史 binary 数值的口径差异。
- T42 在 6 个 provenance split × 2 模型 × 5 seeds = 60 次训练中零失败，所有数值与 T32/T33 在 hierarchy_mixed 上 byte-identical。
- T43 把 T41/T42 的证据综合为 provenance-conditional conclusion，并通过 adversarial review。

**M3 结论（hierarchy_mixed 上 GCN 领先）仍然成立。M4 在此基础上加了 provenance 维度：explicit_only 上 HGCN 领先，synthesized_only 上 GCN 领先。** 两者不矛盾。

### 2.3 Provenance-Conditional Conclusion 是否已 reviewed

**结论：已 reviewed。**

T43 provenance summary 已通过 adversarial review（`docs/review/T43_review.md`，verdict: PASS）。核心结论的三层结构在 T43 中已明确：

| Split | Role | HGCN vs GCN (FS MAP) | HGCN vs GCN (OR MAP) |
|---|---|---|---|
| `explicit_only` | Primary evidence | HGCN +0.1247 | HGCN +0.0557 |
| `synthesized_only` | Controlled diagnostic | GCN ≥ HGCN | GCN +0.0893 |
| `hierarchy_mixed` | Reproducibility check | GCN +0.0381 | GCN +0.0173 |

Hop-bucket 分析进一步确认 HGCN 优势随深度单调增长（hop_2 +0.03 → hop_4_plus +0.25）。这一梯度是 provenance-conditional 的，在 hierarchy_mixed 上不存在。

精度边界已被登记：FS hop_4_plus 基于 4/5 seeds（已注明）、FS synthesized_only aggregate/per-seed 口径差异未核清（R28）、provenance_summary.md Section 5.1 表格错误（R29）。主结论不受影响，但外部发表前须修正。

### 2.4 Proof-Side Bridge 是否已从 Paper Story 变成真实 Demo

**结论：已变成真实 Demo。**

- T50 在 paper outline Section 9 中建立了 proof-side bridge 的必要性论证和 MVP 候选列表。
- T51 选择了 ancestor explanation 作为 MVP，并通过 review。
- T52 把 MVP 规格化为可执行的 demo 任务包（CLI 参数、artifact 依赖、acceptance criteria）。
- T52a 实现了 `proof_side_ancestor_explanation.py` CLI 脚本（~490 行），支持 single-query mode 和 `explicit_vs_mixed` comparison mode，并通过 adversarial review。

Demo 关键验证结果（来自 `docs/experiment_reports/ancestor_explanation_demo_report.md`）：

| Declaration | Candidate | Mode | HGCN MAP | True ancestors in top-10 |
|---|---|---|---|---|
| StrictOrderedCommRing | Order.Ring | explicit_only | 0.6438 | 6/44 |
| StrictOrderedCommRing | Order.Ring | hierarchy_mixed | 0.1492 | 0/44 |

Order.Ring StrictOrderedCommRing 展示了戏剧性的 provenance quality difference：synthesized 边把 HGCN top-10 从 6 个真祖先稀释到 0 个。这把 T42 aggregate finding 变成了可体验的 proof-engineering 工具演示。

## 3. Residual Risks

以下风险仍然活跃，且在 paper-facing 阶段必须处理：

### 高价值活跃风险

| ID | 风险 | 严重度 | 当前状态 | 对 Narrow 阶段的影响 |
|---|---|---|---|---|
| R01 | 项目叙事回退到"证明双曲必胜" | High | Active | Paper drafting 必须保持 provenance-conditional 口径 |
| R03 | 数据快照/版本仍有 unknown | High | Active | 不阻塞 drafting，但限制 reproducibility 声称 |
| R10 | 精确环境版本未从可复现实据锁定 | High | Active | 同 R03 |
| R25 | Clean-environment reproducibility 未闭合 | Medium | Active | Paper 必须写"reviewed single-environment evidence"而非"independently reproduced" |

### 精度级活跃风险（外部发表前必须修复）

| ID | 风险 | 严重度 | 当前状态 | 修复时机 |
|---|---|---|---|---|
| R28 | FS synthesized_only aggregate/per-seed 口径差异 | Medium | Active | Paper Table 4 定稿前 |
| R29 | provenance_summary.md Section 5.1 GCN MAP 表格错误 | Medium | Active | Paper Table 4 定稿前 |
| R30 | 5 条 contributions 对 ITP/CPP 页数预算过宽 | Medium | Active | Paper drafting 时决定是否合并（如 C1+C5） |

### 已缓解但需持续监控的风险

| ID | 风险 | 严重度 | 当前状态 | 监控要求 |
|---|---|---|---|---|
| R04 | Relation layer 过浅 | High | Mitigated (provenance-conditional) | Paper 不得升级为无条件结论 |
| R06 | Synthesized relation 语义复杂 | High | Mitigated | 不影响 drafting |
| R31 | Ancestor explanation MVP 可能过轻 | Medium | Mitigated | T52a 已证明 demo 有实质质量差异 |

### 明确不夸大 closure 的风险

R28、R29、R30、R31 仍按真实状态记录：
- **R28**：Active。Field.Subfield `synthesized_only` GCN aggregate MAP = 1.0000 但 per-seed 有 seed 123 MAP = 0.8100、seed 2026 MAP = 0.9029。根因未核清。主结论（controlled diagnostic 定性不变）不受影响，但外部发表前必须修正。
- **R29**：Active。`docs/experiment_reports/provenance_summary.md` Section 5.1 的 Field.Subfield `synthesized_only` GCN MAP 表格单元写错（误写为 0.6857，实际 aggregate 为 1.0000）。外部发表前必须修正。
- **R30**：Active。5 条 contributions 在 ITP（~20 页）/CPP（~20 页）页数预算内可能过宽。Drafting 时应判断是否合并（如 C1+C5 合为 pipeline+alignment）。
- **R31**：Mitigated。`T51_review` 接受 ancestor explanation 作为 provenance-aware quality comparison tool，`T52a` 已展示实质 provenance quality difference。不夸大为"已完全解决"——如果 CPP reviewer 仍认为 tool demo 不够强，可能需要后续补强。

## 4. Recommended Next Task Shape

项目应进入 **paper-facing / packaging / cleanup** 收窄阶段。具体来说：

### 应该做的

1. **Paper drafting**。基于 `docs/paper_outline.md` 的 5 contributions 结构进入正式 LaTeX drafting。优先 ITP/CPP 版本。Drafting 过程中自然会产生 R30（是否合并 contributions）的裁决。

2. **Figure / table rendering**。把 `docs/paper_outline.md` Section 6 的 4 figures + 7 tables 从文字描述变成实际渲染的 PDF/PNG。T42/T43 的 numeric anchors 已锁定（Section 12），可以直接使用。

3. **Precision fixes (R28/R29)**。在 paper Table 4 定稿前修复 `docs/experiment_reports/provenance_summary.md` Section 5.1 的错误表格单元，并核清 FS synthesized_only aggregate/per-seed 口径差异的根因。

4. **Artifact packaging**。将 `project_bootstrap/` 和 `artifacts/` 整理为可提交的 CPP artifact bundle（含 README、复现指令、config index）。

### 不应该做的

1. **不跑新实验**。60 次 provenance sweep 已 zero-failed 完成，继续跑不会产生新发现。
2. **不扩展 demo**。T52a 的 CLI 已通过 adversarial review，不需要新 demo 或新 proof-side 支线。
3. **不修改已冻结的 protocol 语义**。T40/T41/T42 的 provenance split 配置、图结构和 sweep 结果是 reviewed 证据，不应改动。
4. **不引入新模型、新数据源或新依赖**。当前证据链已足以支撑 provenance-conditional finding。
5. **不把项目重新带回"HGCN 稳定优于 GCN"的旧叙事**。R01 仍然活跃。

### 建议的下一任务形态

下一任务应为 **paper drafting 起步**，具体可能包括：
- T54: Paper LaTeX 框架搭建 + Introduction/Background 初稿
- T55: Figure 1–4 和 Table 1–7 的渲染与精度校验
- T56: R28/R29 精度修复
- T57: CPP artifact package 打包

这些任务的具体设计应由 Captain 在 T53 review 闭合后根据 paper drafting 的实际需要派发。

## 5. Milestone Closure Summary

| Milestone | Tasks | Closure Review | Status |
|---|---|---|---|
| M0: Governance Bootstrap | T00–T02 | T00 PASS, T01 PASS_WITH_WARNINGS, T02 PM-accepted | Closed |
| M1: Data & Protocol Freeze | T10–T14 | All PASS (T14 PASS) | Closed |
| M2: Diagnostics & Candidate Selection | T20–T22 | All PASS (T20 PASS_WITH_WARNINGS) | Closed |
| M3: Grouped Retrieval Training Alignment | T30–T34 | All PASS (M3 review PASS_WITH_WARNINGS) | Closed |
| M4: Relation Provenance Split | T40–T43 | All PASS (T43 PASS) | Closed |
| M5: Paper & Proof-Side Bridge | T50–T52a | T50 PASS_WITH_WARNINGS, T51/T52/T52a PASS | Closed |

**Total tasks reviewed: 24 (T00–T14, T20–T22, T30–T34, T40–T43, T50–T52a)**

**Adversarial reviews: T12, T13, T14, T31A, T31, T32, T33, T40, T41, T42, T52a**

**Milestone reviews: M3 (PASS_WITH_WARNINGS)**

## 6. One-Paragraph Assessment for Handoff

Milestone 1–5 全部通过 review 并闭合。核心 provenance-conditional finding 已由 T42 的 60 次训练确立、T43 收口、T50 保持、T52a demo 验证。项目现在应 Narrow 到 paper drafting + figure rendering + precision fixes + artifact packaging。不需要新实验、新模型、新 demo 或新数据源。活跃风险（R01/R03/R10/R25/R28/R29/R30）是 paper-facing 收窄工作中的待处理项，不阻塞 drafting 起步。R28/R29 在 paper Table 4 定稿前必须修复。R30 在 drafting 过程中自然裁决。
