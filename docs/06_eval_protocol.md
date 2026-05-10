# 06 Eval Protocol

> 更新时间：2026-05-10
>
> 状态：协议冻结前草案。后续 T12 / T13 负责把本文件与代码输出字段完全对齐。

## 1. 默认任务

正式 ancestor 任务默认采用：

```text
grouped multi-positive ancestor retrieval
```

查询单位：

```text
(src, relation)
```

正例集合：

```text
同一查询下全部真实 ancestor
```

禁止把旧单正例 `ancestor_ranking` 的 MRR 当作主结论。它只能作为历史对照或辅助指标。

## 2. 推荐任务族

| 任务 | 用途 | 当前地位 |
| --- | --- | --- |
| grouped ancestor retrieval | 默认正式协议 | 主任务 |
| typed parent retrieval | 区分 `extends` 与 `instance_of` | 辅助主任务 |
| parent prediction | 与旧结果保持可比 | 辅助任务 |
| typed link prediction | 检查 relation typing 信号 | 诊断任务 |
| proof-side utility | 连接 proving workflow | 后续 MVP |

## 3. 指标

grouped retrieval 必须报告：

- `Recall@1`
- `Recall@3`
- `Recall@5`
- `Recall@10`
- `MAP`
- `nDCG`
- `nDCG@10`
- `grouped-MRR`

必须补充 hop bucket：

- `hop_2`
- `hop_3`
- `hop_4_plus`

多 seed 正式结果默认报告：

```text
mean ± std over 5 seeds
```

## 4. Split 原则

1. 同一 `(src, relation)` 查询下的正例不能泄漏到不同 split。
2. 查询级 split 优先于边级随机 split。
3. 模块级 split 优先于全图随机 split，用于检验泛化。
4. 所有 split 必须记录 seed、候选空间和负采样策略。
5. `unresolved` 或 coverage 不可靠的端点不能强行当高置信 negative。

## 5. Baseline 比较原则

所有模型比较必须满足：

1. 相同数据快照。
2. 相同 split。
3. 相同 seed sweep。
4. 相同候选集合。
5. 相同 grouped 指标。
6. 相近参数预算。
7. 报告训练目标是否与评测目标对齐。

默认 baseline 梯度：

1. 启发式 / 文本 baseline。
2. 欧氏图模型，如 GCN / GraphSAGE / GAT。
3. 双曲模型，如 Poincare / HGCN / Lorentz 变体。
4. 只有在前面三层结果明确后，再考虑复杂模型。

## 6. 结构诊断指标

每张正式图至少报告：

- nodes / edges
- relation nodes / relation edges
- largest component
- SCC 情况
- longest chain
- leaf ratio
- multi-parent count
- cycle rank
- diameter estimate
- approximate hyperbolicity proxy
- grouped retrieval difficulty

诊断报告必须明确判断：

1. 图是否是 shallow forest / star forest。
2. 是否存在更深、更连续、更有层级密度的候选子图。
3. 当前图是否适合继续检验双曲优势。

## 7. 数据资产要求

每次正式实验应绑定：

- Lean 版本
- Mathlib commit
- LeanDojo / tracing 工具版本
- Python 环境或依赖文件
- 图抽取脚本版本
- 评测脚本版本
- config 路径
- artifact 输出路径
- run id

T10 将负责把这些要求落成 version manifest。

## 8. 通过 / 失败判据

协议门通过条件：

1. grouped retrieval 已成为默认任务入口。
2. hop bucket 出现在常规报告中。
3. 5-seed mean ± std 可复现。
4. GCN / HGCN 同口径比较无明显数据泄漏。

双曲价值门通过条件，至少满足一项：

1. 低维下稳定优于欧氏模型。
2. 在更深 hop bucket 上形成稳定收益。
3. 在更纯层级图上显著优于欧氏 baseline。

若不满足，双曲保留为条件性 follow-up，不作为主论文承诺。

## 9. 当前治理状态

- `T00` 已通过 review，项目已有根目录入口文档。
- `T01` 将先复查治理文档一致性；本评测协议仍是协议冻结前草案。
- 真正的协议冻结仍由后续 `T12` / `T13` 完成，当前不得把本文件写成已与代码完全对齐的事实。
