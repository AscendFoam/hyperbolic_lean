# Review: M3

> Reviewer: Claude Code (milestone)
> Date: 2026-05-17
> Scope: `T30`, `T31A`, `T31`, `T32`, `T33`, `T34`

## Verdict: PASS_WITH_WARNINGS

Milestone 3 can be closed, and the project may enter Milestone 4. The grouped training alignment story is now complete enough to support the next stage, but two warning classes remain: full clean-environment reproducibility is not yet proven end to end, and some report/governance polish remains deferred.

## 1. 当前功能是否真的完成

是，按 Milestone 3 的定义已经完成。

本里程碑要求的核心能力已经全部具备并通过 review：

1. `T30` 明确识别了旧 binary edge training 与 grouped retrieval 目标错配。
2. `T31A` 把 grouped ancestor retrieval 切到 query-level split，并补入 disjointness 证据。
3. `T31` 在 reviewed grouped runner 中补入最小 query-grouped loss 路径。
4. `T32` 完成 GCN grouped 5-seed 正式 sweep。
5. `T33` 完成与 `T32` 匹配口径的 HGCN grouped 5-seed 正式 sweep。
6. `T34` 把 grouped-vs-binary 协议差异、matched GCN-vs-HGCN 对照、以及结论边界收口成正式总结。

因此，Milestone 3 的功能性目标“形成 reviewed grouped training benchmark surface，并完成 matched GCN/HGCN 对照”已真正完成。

## 2. 是否能从干净环境运行

结论：**部分可以证明，但尚不能宣称已被完整证明。**

已具备的证据：

- `T14` 和 `T31` 有 smoke artifact，说明最小链路可运行。
- `T32` / `T33` 有真实 5-seed artifact，说明正式 grouped sweep 在当前工作环境中已成功执行。
- `T10` / `T11` 已把部分环境未知项显式保留为 `unknown / needs verification`，没有伪装成已锁定事实。

尚未闭合的缺口：

- 没有一份“从全新干净环境重新拉起 M3 正式 sweep”的独立复现记录。
- `lean4-example`、LeanDojo、Python 等精确环境锚点仍未全部由机器可读证据关闭。

因此，本里程碑可宣称“已有可审查运行证据”，但**不能**宣称“已完成 clean-room reproducibility 证明”。

## 3. 是否有测试、demo 或实验结果

有，而且证据充分。

- 测试 / spot-check：
  - `T14` GCN smoke
  - `T31` grouped training smoke
- 正式实验：
  - `T32` GCN grouped 5-seed sweep
  - `T33` HGCN grouped 5-seed sweep
- 总结报告：
  - `docs/experiment_reports/gcn_grouped_training.md`
  - `docs/experiment_reports/hgcn_grouped_training.md`
  - `docs/experiment_reports/grouped_training_summary.md`

这些证据足以支持 Milestone 3 的结论。

## 4. 是否存在伪完成

结论：**没有发现核心功能层面的伪完成。**

原因：

- `T32` / `T33` 的数值、artifact、config 与报告已被逐字段交叉核验。
- `T34` 没有把旧 binary 数值伪装成与 matched grouped sweep 直接可比。
- 文档明确保留了“GCN 仍领先、HGCN 未被建立为更强”的窄结论边界。
- `unknown / needs verification` 仍保留在 manifest / data card 中，没有被偷偷抹平。

剩余问题主要是文档精修与可复现性证明不足，不属于伪完成。

## 5. 是否允许进入下一里程碑

**允许。**

建议进入 `Milestone 4: Relation Provenance Split`，当前唯一任务切换为 `T40`：

`docs/tasks/M4_provenance/T40_provenance_configs_freeze.md`

进入下一里程碑的理由：

1. Milestone 3 的协议、训练、对照和总结都已收口。
2. 当前最关键未回答问题已经转向 provenance：Lean-specific synthesized relation 是否改变结构诊断与双曲偏置表现。
3. 继续停留在 Milestone 3 只会重复已有 grouped-vs-HGCN 争论，边际收益低。

## Warnings

1. **全新干净环境复现仍未闭合。**
   - 分类：deferred
   - 影响：不阻塞进入 M4，但阻塞更强的“完全可复现”对外表述。

2. **T34 报告仍有少量呈现层面缺口。**
   - 分类：deferred
   - 内容：Recall 汇总列未补齐、历史数值来源未写到具体文件路径。
   - 影响：不改变 M3 结论，但降低文档精确度。

3. **部分治理文档新增段落存在中英混杂。**
   - 分类：accepted
   - 说明：本轮 Captain 已在 05/08 治理文档中直接收口主要问题；剩余非治理报告文字可后续精修。

## Recommended Next Action

Captain 可关闭 `T34` 与 Milestone 3，并把当前唯一任务切换到 `T40`，不执行 `T40`，只做下一轮派工准备。
