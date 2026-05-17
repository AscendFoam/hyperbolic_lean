# 08 Risks and Open Questions

> 更新时间：2026-05-17

## 1. Active Risks

| ID | 风险 | 严重度 | 状态 | 缓解策略 |
| --- | --- | --- | --- | --- |
| R01 | 项目叙事回退到“证明双曲必胜” | High | Active | 所有文档和任务包默认使用 benchmark / protocol / diagnostics 主线 |
| R02 | grouped retrieval 与 hop bucket 报告入口已通过 T12/T13/T14 review 收口；剩余风险是后续误把 smoke artifact 当正式 benchmark 结果 | Low | Mitigated | 文档明确 smoke artifact 只用于输出链 spot-check；正式结果必须另走 seed sweep 与 diagnostics |
| R03 | 数据快照、版本和 config 仍有部分 unknown，导致结果不可复现 | High | Active | T10 reviewed manifest 与 T11 reviewed data card 已保留 unknown 限制；后续只能用可复现实据关闭未知字段 |
| R04 | relation layer 过浅，双曲价值不足 | High | Active | `T20` 已确认大多数 real-graph / hierarchy-focused relation layer 仍偏浅；后续优先转向 `mathlib_order_focus_v1` 中更深的模块级候选，但在训练验证前仍不把双曲设为主承诺 |
| R05 | full Mathlib trace 成本过高或再次卡住 | Medium | Active | 优先已有产物、模块级 probe、小仓库 trace |
| R06 | synthesized relation 语义复杂，负采样或层级解释失真 | High | Active | Milestone 4 做 provenance split |
| R07 | binary training 与 grouped retrieval 评测错配 | High | Mitigated | `T31` 已通过 adversarial review；reviewed grouped retrieval runner 已补入最小 query-grouped training 分支，并用 grouped val MAP 做 checkpoint selection。`T32` 也已在 `Field.Subfield` 与 `Order.Ring` 上用该路径完成真实 5-seed GCN grouped sweep。旧 BCE runners 仍保留为 legacy/auxiliary path，后续正式 grouped sweep 必须继续使用 grouped runner |
| R08 | 后续 worker 越界修改或重复做历史任务 | Medium | Active | `docs/04_task_board.md`、`docs/tasks/` 与根目录入口文档明确 Allowed files 与 Forbidden scope |
| R09 | 论文贡献被已有 Lean graph/export 工作稀释 | Medium | Active | 强调协议、诊断、条件性双曲结论和 proof-side bridge |
| R10 | `lean4-example`、LeanDojo、Python 环境等精确版本尚未从可复现实据锁定，若提前写成事实会削弱复现性声明 | High | Active | `docs/data_manifest.md` 继续将未证实字段标为 `unknown / needs verification`，待后续以环境清单或 trace 元数据补证 |
| R11 | provenance split 目前主要通过派生图家族与诊断报告表达，而不是 `edges.csv` 中的一等字段，若直接下游消费容易误解 relation 语义 | Medium | Mitigated | `T40` 已通过 `docs/provenance_split_protocol.md` 冻结 provenance split 配置、origin_map 与输出目录约定；provenance split 现在有正式协议入口，不再仅靠派生图目录名表达。`edges.csv` 一等字段问题仍保留为 Open Question 9 |
| R12 | hop bucket flatten helper 若分散在多个 runner 中，未来维护时可能出现字段漂移 | Low | Mitigated | T14 已把 `flatten_grouped_hop_bucket_summary` 收敛到 `relation_baseline_common.py`；后续只需防止新重复回流 |
| R13 | `docs/diagnostics_summary.md` 已通过 T20 review，但部分表格项使用 `n/a` 或未显式标注指标来源，可能降低文档精确性 | Low | Active | 后续文档精修时补全 plausible / hierarchy-focused 图的真实节点边数，并标注 longest-chain 等指标来源 |
| R14 | module-level candidate scan 的 raw hierarchy score 可能高估“小而紧凑”的候选，若不额外检查 positive scale、component ratio 与 closure expansion，容易把高分误写成默认 benchmark | Medium | Mitigated | `T21` 已把 `Mathlib.Algebra.Order.Ring`、`Mathlib.Algebra.Order`、`Ring.Subring`、`Field.Subfield` 分层；`T22` 已通过 review，并在 `docs/diagnostics_protocol.md` 中把规模、连续性和 closure cost 固化为显式 heuristic 门控 |
| R17 | `T22` 新增的诊断阈值来自当前 reviewed artifacts 的经验校准，若后续 provenance split、训练对齐或更大 traced graph 改变结构分布，这些阈值可能失真 | Medium | Active | 把阈值明确标成 heuristic；在 `T30+` / `T40+` 后根据新图分布重新校准，不把当前模板当作永久边界 |
| R15 | `docs/candidate_graph_audit.md` 的审计表存在轻微呈现歧义：`depth` 指 scan depth 而不是 structural depth，且 9 个入表模块的选择依据未完全展开 | Low | Active | 下次修改 candidate audit 时把 `depth` 改为 `scan depth`，并补一句选择范围说明；T21 review 判定不影响审计结论 |
| R16 | mathlib module-level scan 的 standalone checked-in config 缺失，当前只能从 `summary.json` 追踪 scan settings | Medium | Active | 后续 config freeze 或 diagnostics protocol 任务应记录该 traceability gap；正式 benchmark 前需要补齐 config 或说明复现路径 |
| R18 | `docs/diagnostics_protocol.md` 已通过 T22 review，但部分模板措辞仍可能让未来 worker 混淆“浅层风险”和“深层但碎片化风险”，且报告模板缺少 `multi-parent count` 行与 `ancestor_added_nodes` 内联定义 | Low | Active | 后续精修 diagnostics protocol 时处理；当前不影响 T22 完成或候选角色门控结果 |
| R19 | 当前 `ancestor_ranking` split 是按正例边而不是按 `(src, relation)` query 切分，同一 grouped query 可能跨 split 被拆碎，导致 val/test grouped eval 缺少完整 positive set，并把其他真祖先当成 non-positive candidate | High | Mitigated | `T31A` 已通过 adversarial review；`ancestor_ranking` / grouped ancestor retrieval 已切到 query-level split，并在 `run_manifest.json` 写入 disjointness 摘要 |
| R20 | `T31A` 只修了 grouped ancestor retrieval 路径，其他 task family 仍保留原 split 行为；如果未来把 grouped/query-level 语义扩展到其他任务，可能再次出现 split completeness 漏洞 | Medium | Active | 当前刻意保持窄改动范围；后续若扩展 grouped/query-aware 训练到其他任务，需要逐任务确认 split 单位 |
| R21 | T31 若使用的 grouped loss query key 与 T31A split/eval key 不一致，可能重新制造训练/评测错配，尤其是 `ancestor_label_mode="source_kind"` 下的 `extends_ancestor` / `instance_ancestor` 标签 | High | Mitigated | `T31` 已通过 adversarial review；grouped training query 构造复用 `build_grouped_ranking_queries(...)`，并在 smoke artifact 的 `grouped_training_summary.json`、`training_stats.json`、`result_summary.json` 中写入 `query_key_fields = [src_id, relation_type]` |
| R22 | T32 若误用旧 BCE runner 或省略 `negative_ratio`，会让 5-seed GCN sweep 与 T31 reviewed grouped protocol 不同口径 | High | Mitigated | `T32` 已通过 adversarial review；四份正式 grouped GCN config 均显式设置 `grouped_loss = sampled_softmax`、`negative_ratio = 10.0`，并在新的 `grouped_gcn_*_t32/` 目录中完成两组 5-seed artifact |
| R23 | `Field.Subfield` 作为 controlled probe 在 reviewed grouped GCN 5-seed sweep 下方差较大，若在 T33/T34 中与 `Order.Ring` 等权解读，可能放大小图 seed/split 敏感性 | Medium | Active | 将 `Field.Subfield` 继续视为 controlled probe，把 `Order.Ring` 视为 primary balanced candidate；T33/T34 汇总时同时报告两图，但不要让 `Field.Subfield` 单独主导总体结论 |
| R24 | `T33` 协议不匹配风险已关闭：matched grouped HGCN sweep 已完成 | Low | Mitigated | `T33` 使用了与 `T32` 相同的 grouped runner、split、seed list 与参数预算；报告与 artifact bundle 已成功生成并通过 review。 |
| R25 | Milestone 3 虽已有 smoke、正式 sweep 和 summary 报告，但尚未完成”从全新干净环境重新拉起正式 grouped benchmark”的独立复现闭环 | Medium | Active | 允许进入 T40/T41/T42，但对外结论继续保持”已有 reviewed 运行证据”而非”已完成 clean-room reproducibility”；后续需用环境锁定证据或 fresh-environment rerun 关闭该风险 |
| R26 | T40 冻结了 provenance split 配置与协议，但 split 实际生成（运行 `split_relations_by_provenance.py`）尚未执行；T41/T42 开始前必须先运行 split 生成、验证输出与协议中预期边数一致，并程序化校验当前两组候选图上的 `hierarchy_mixed = full source graph` identity | Medium | Active | T41 先运行 frozen config 生成 provenance-split 图；校验 `stats.json` 中的边数与协议中预期值一致，并把 `hierarchy_mixed` identity 校验写入 diagnostics 报告 |

## 2. Open Questions

1. `docs/diagnostics_protocol.md` 中的经验阈值在 `T30+` / `T40+` 新证据进入后，是否仍应保持当前分层，还是需要重校准？
2. `closure expansion ratio` 是否应继续作为主门控，还是在后续版本中改成更稳定的 closure-cost 组合指标？
3. synthesized relation 是否真的降低 hierarchy 深度，还是主要改变候选分布和负采样难度？
4. provenance split 后，`explicit-only / synthesized-only / mixed` 是否会改变当前 “GCN 整体领先、HGCN 未建立优势” 的 grouped 结论？
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
| D06 | 对真实数据跑完整 seed sweep 验证 hop bucket 报告 | Closed by `T34` summary：`T32`/`T33` 已分别完成 GCN/HGCN grouped 5-seed sweep 并真实产出 hop bucket 聚合，且已纳入正式 grouped summary | 若后续 benchmark 扩展到 provenance split 或新图族，需要重新检查 hop bucket 汇总面是否保持一致 |
| D07 | 精修 `docs/diagnostics_summary.md` 的 `n/a` 数值与指标来源标注 | T20 review 确认不影响候选优先级或任务完成 | 下一次修改 diagnostics summary 或 candidate audit 文档时 |
| D08 | 精修 `docs/candidate_graph_audit.md` 的 `depth` 列名和入表模块选择说明 | T21 review 确认这是可读性问题，不影响数值准确性、优先级判断或任务完成 | 下一次修改 candidate audit，或 T22 需要引用该表作为模板示例时 |
| D09 | 精修 `docs/diagnostics_protocol.md` 的 flag 命名、report template 和字段定义 | T22 review 确认当前分类结果正确，问题只影响模板自洽性和可读性 | 下一次修改 diagnostics protocol 时，把 shallow forest condition 3 改名或加注为 fragmentation risk，补 `multi-parent count` 行，并内联定义 `ancestor_added_nodes` |
| D10 | query-level split completeness 前置任务 | Closed by T31A adversarial review; grouped ancestor retrieval 已切到 query-level split，query overlap 为 0 | 若未来把 grouped/query-level 语义扩展到其他 task family，则重新逐任务审查 split completeness |
| D11 | 精修 `docs/training_alignment_audit.md` 的 heading nesting、M6 mixed-language title，并补充 M3 split impact rough estimate | T30 review 确认这些是文档呈现和定量补强问题，不影响代码事实或任务完成；T31 本轮只补了最小 grouped-loss 状态，不扩展这组文档精修范围 | 下一次修改 training alignment audit，或需要把 T31/T31A 的影响写成更完整 split-impact analysis 时 |
| D12 | 区分 `grouped_loss="infonce"` 与 `sampled_softmax` 的实现或文档语义 | T31 review 接受当前二者指向同一 InfoNCE / sampled-softmax family 实现；最小任务不需要拆出独立 contrastive variant | 后续需要真正比较 loss variants，或文档中出现把 `infonce` 当作独立实现的表述时 |
| D13 | 统一 grouped runner 的 `negative_ratio` 默认值或强制配置校验 | T31 smoke config 显式设为 `1.0`，不影响已 review 结果；但 runner 默认 `10.0` 可能误导未来未显式配置的正式 sweep | T32/T33 正式 sweep config 编写时必须显式设置；若再次出现默认值混淆，则改 runner 默认或加配置校验 |
| D14 | 将 grouped runner 的 `total_loss = torch.tensor(0.0)` 清理为 device-aware 初始化 | T31 review 确认可运行且数值正确；这是代码整洁性问题，不阻塞 grouped protocol | 下一次修改 grouped runner training loop，或引入 GPU / 非 CPU 运行要求时 |
| D15 | 在 grouped 汇总报告中补入显式 config diff 表与可比性声明 | Closed by `T34` review：`docs/experiment_reports/grouped_training_summary.md` 已补入 config diff 表与 matched grouped comparability statement | 若后续新增新的 grouped baseline family，需要重新维护可比性边界 |
| D16 | 为 `grouped_training_summary.md` 的正式结果表补齐 Recall@1/3/5/10 汇总列 | T34 review 确认当前 MAP / nDCG / nDCG@10 已足以支持主结论；Recall 列缺失不阻塞里程碑关闭 | 下一次修改 grouped summary 报告，或需要把 Recall 作为主要展示面时 |
| D17 | 为 `grouped_training_summary.md` Section 6 补入历史 binary 数值来源的具体文件路径 | T34 review 确认历史数值可追溯，但正文未直接写出源文件名 | 下一次修改 grouped summary 报告时，把 `docs/阶段总结（2026-05-02，grouped retrieval training）.md` 显式写入正文 |

## 4. Risk Handling Rules

1. 任何高风险代码任务必须有 reviewer。
2. 核心算法、实验指标、数据 pipeline、旧项目迁移、架构变更使用 adversarial review。
3. 如果 reviewer BLOCK，同一任务最多自动复修一次；第二次仍 BLOCK，交给用户裁决。
4. 不把计划、mock、stub、未来能力写成已完成事实。
5. 每次任务完成后必须更新 handoff、风险或任务板中的至少一项。
## T34 Completion Note

- `T34` 已通过 review，当前剩余的 wording 风险不再是实验性问题，而是报告精修问题。
- 当前安全结论边界：
  - matched grouped `GCN` vs `HGCN` 可直接比较；
  - grouped-vs-binary 适合作为对齐证据；
  - 跨协议绝对数值不应被揉成一个平面排行榜。
- 当前保留风险：
  - 读者仍可能把早期 grouped-vs-binary gain 误读成与 `T32` / `T33` 完全同口径的 formal sweep；`T34` 已显式提示，但后续文档精修仍应继续压缩这种误读空间。
