# 08 Risks and Open Questions

> 更新时间：2026-05-12

## 1. Active Risks

| ID | 风险 | 严重度 | 状态 | 缓解策略 |
| --- | --- | --- | --- | --- |
| R01 | 项目叙事回退到“证明双曲必胜” | High | Active | 所有文档和任务包默认使用 benchmark / protocol / diagnostics 主线 |
| R02 | grouped retrieval 与 hop bucket 报告入口已通过 T12/T13/T14 review 收口；剩余风险是后续误把 smoke artifact 当正式 benchmark 结果 | Low | Mitigated | 文档明确 smoke artifact 只用于输出链 spot-check；正式结果必须另走 seed sweep 与 diagnostics |
| R03 | 数据快照、版本和 config 仍有部分 unknown，导致结果不可复现 | High | Active | T10 reviewed manifest 与 T11 reviewed data card 已保留 unknown 限制；后续只能用可复现实据关闭未知字段 |
| R04 | relation layer 过浅，双曲价值不足 | High | Active | `T20` 已确认大多数 real-graph / hierarchy-focused relation layer 仍偏浅；后续优先转向 `mathlib_order_focus_v1` 中更深的模块级候选，但在训练验证前仍不把双曲设为主承诺 |
| R05 | full Mathlib trace 成本过高或再次卡住 | Medium | Active | 优先已有产物、模块级 probe、小仓库 trace |
| R06 | synthesized relation 语义复杂，负采样或层级解释失真 | High | Active | Milestone 4 做 provenance split |
| R07 | binary training 与 grouped retrieval 评测错配 | High | Active | Milestone 3 做 query-grouped training alignment |
| R08 | 后续 worker 越界修改或重复做历史任务 | Medium | Active | `docs/04_task_board.md`、`docs/tasks/` 与根目录入口文档明确 Allowed files 与 Forbidden scope |
| R09 | 论文贡献被已有 Lean graph/export 工作稀释 | Medium | Active | 强调协议、诊断、条件性双曲结论和 proof-side bridge |
| R10 | `lean4-example`、LeanDojo、Python 环境等精确版本尚未从可复现实据锁定，若提前写成事实会削弱复现性声明 | High | Active | `docs/data_manifest.md` 继续将未证实字段标为 `unknown / needs verification`，待后续以环境清单或 trace 元数据补证 |
| R11 | provenance split 目前主要通过派生图家族与诊断报告表达，而不是 `edges.csv` 中的一等字段，若直接下游消费容易误解 relation 语义 | Medium | Active | `docs/data_card.md` 明确 provenance 边界；Milestone 4 / T40-T43 继续把 provenance split 正式化 |
| R12 | hop bucket flatten helper 若分散在多个 runner 中，未来维护时可能出现字段漂移 | Low | Mitigated | T14 已把 `flatten_grouped_hop_bucket_summary` 收敛到 `relation_baseline_common.py`；后续只需防止新重复回流 |
| R13 | `docs/diagnostics_summary.md` 已通过 T20 review，但部分表格项使用 `n/a` 或未显式标注指标来源，可能降低文档精确性 | Low | Active | 后续文档精修时补全 plausible / hierarchy-focused 图的真实节点边数，并标注 longest-chain 等指标来源 |
| R14 | module-level candidate scan 的 raw hierarchy score 可能高估“小而紧凑”的候选，若不额外检查 positive scale、component ratio 与 closure expansion，容易把高分误写成默认 benchmark | Medium | Active | `T21` 已把 `Mathlib.Algebra.Order.Ring`、`Mathlib.Algebra.Order`、`Ring.Subring`、`Field.Subfield` 分层，并要求后续任务把规模、连续性和 closure cost 作为显式门控 |
| R15 | `docs/candidate_graph_audit.md` 的审计表存在轻微呈现歧义：`depth` 指 scan depth 而不是 structural depth，且 9 个入表模块的选择依据未完全展开 | Low | Active | 下次修改 candidate audit 时把 `depth` 改为 `scan depth`，并补一句选择范围说明；T21 review 判定不影响审计结论 |
| R16 | mathlib module-level scan 的 standalone checked-in config 缺失，当前只能从 `summary.json` 追踪 scan settings | Medium | Active | 后续 config freeze 或 diagnostics protocol 任务应记录该 traceability gap；正式 benchmark 前需要补齐 config 或说明复现路径 |

## 2. Open Questions

1. T22 应如何把 `Mathlib.Algebra.Order.Ring` 作为默认下一轮 benchmark 候选、`Mathlib.Algebra.Order` 作为 depth stress-test 的经验依据写成可复用模板？
2. T22 是否应显式引入最小 positive scale、最小 component ratio 和最大 closure expansion 之类的阈值，避免 raw hierarchy score 偏向小而紧凑的模块？
3. synthesized relation 是否真的降低 hierarchy 深度，还是主要改变候选分布和负采样难度？
4. query-grouped loss 在 GCN 上是否已经足够改善训练/评测对齐？
5. HGCN 若仍不赢，是否能在更深 hop bucket 或低维预算下形成局部价值？
6. proof-side utility 应优先选择 ancestor explanation、declaration recommendation，还是 premise retrieval 正则化？
7. 是否需要把 `project_bootstrap/` 中的脚手架整理成正式 `src/` 包，还是继续以实验包形式维护？
8. 哪一种可复现实据应被视为关闭 `T10` 剩余 unknowns 的规范来源：导出的 conda/pip lock、trace 元数据，还是单独的机器可读版本清单？
9. `explicit-only / synthesized-only / mixed` 是否应在后续数据快照中成为 `edges.csv` 的一等字段，而不是继续依赖派生图目录名与诊断产物表达？
10. 是否要在后续版本中把 legacy `task = ancestor_ranking` 正式重命名为更不易混淆的 grouped 协议键，还是继续保留兼容别名？

## 3. Deferred Items

| ID | 项目 | 暂缓原因 | 重新触发条件 |
| --- | --- | --- | --- |
| D01 | full Mathlib trace | 成本高、风险大、不是当前瓶颈 | 小仓库与模块级 probe 均稳定，且确需更大数据 |
| D02 | 复杂 hyperbolic transformer | 当前图结构和 baseline 尚未支持 | 强欧氏与简单双曲对照已完成，且候选图具备深层结构 |
| D03 | 端到端 theorem proving | 超出当前 MVP | proof-side retrieval demo 证明图表示有实用价值 |
| D04 | 简历素材同步到中枢项目 | 证据等级尚未提升 | 完成一个 milestone review 且 reviewer 通过 |
| D05 | 把 `format_metric` 等 report 展示 helper 进一步完全抽到共享模块 | T14 已处理 correctness 相关的 hop bucket flatten 去重；展示 helper 仍有轻微重复，但不影响协议字段或 smoke 结论 | report 展示逻辑再次扩展，或出现展示字段漂移 |
| D06 | 对真实数据跑完整 seed sweep 验证 hop bucket 报告 | 当前阶段禁止大规模 sweep，T13 静态验证已足够通过 review | T32/T33 或正式 benchmark sweep 启动时 |
| D07 | 精修 `docs/diagnostics_summary.md` 的 `n/a` 数值与指标来源标注 | T20 review 确认不影响候选优先级或任务完成 | 下一次修改 diagnostics summary 或 candidate audit 文档时 |
| D08 | 精修 `docs/candidate_graph_audit.md` 的 `depth` 列名和入表模块选择说明 | T21 review 确认这是可读性问题，不影响数值准确性、优先级判断或任务完成 | 下一次修改 candidate audit，或 T22 需要引用该表作为模板示例时 |

## 4. Risk Handling Rules

1. 任何高风险代码任务必须有 reviewer。
2. 核心算法、实验指标、数据 pipeline、旧项目迁移、架构变更使用 adversarial review。
3. 如果 reviewer BLOCK，同一任务最多自动复修一次；第二次仍 BLOCK，交给用户裁决。
4. 不把计划、mock、stub、未来能力写成已完成事实。
5. 每次任务完成后必须更新 handoff、风险或任务板中的至少一项。
