# 02 工程化实验方案

> 更新时间：2026-05-09
>
> 适用范围：当前这条面向 traced Lean/Mathlib hierarchy 图的工程化实验主线。
>
> 依据文档：
> [形式化证明工程化实验方案（修订版）](./形式化证明工程化实验方案（修订版）.md)
> [基于深度调研报告的项目定位与创新方向修订](./基于深度调研报告的项目定位与创新方向修订.md)
> [阶段总结（2026-05-01，grouped ancestor retrieval）](./阶段总结（2026-05-01，grouped%20ancestor%20retrieval）.md)
> [阶段总结（2026-05-02，grouped retrieval training）](./阶段总结（2026-05-02，grouped%20retrieval%20training）.md)
> [双曲优势假设的诊断分析与替代方向](./双曲优势假设的诊断分析与替代方向.md)
> [投稿路线图（FM-ITP-CPP-备选 venue 对照）](./投稿路线图（FM-ITP-CPP-备选%20venue%20对照）.md)

---

## 0. 修订说明

本方案不是对旧方案的简单续写，而是基于截至 2026-05-09 的真实实验进展重新定稿。相较于 [形式化证明工程化实验方案（修订版）](./形式化证明工程化实验方案（修订版）.md)，本版做了四个关键收束：

1. **主线收束**
   - 不再把“证明双曲优于欧氏”作为默认主目标。
   - 默认主目标改为：**构建真实 traced formal-math hierarchy 图的可复现实验管线、标准化协议与结构诊断框架，并在此基础上系统检验双曲归纳偏置何时可能有效。**

2. **协议升级**
   - `ancestor_ranking` 的默认口径改为 `grouped multi-positive ancestor retrieval`。
   - 训练侧也要逐步从 binary edge classification 迁移到 grouped retrieval / listwise / contrastive 训练。

3. **结构判断前置**
   - 当前真实图的 relation layer 主要呈现浅层、碎片化、叶子占优的 forest / star 形态。
   - 因此后续实验必须先做图结构筛选和诊断，再决定是否值得继续押注双曲路线。

4. **投稿叙事调整**
   - 更适合的叙事已经从“新双曲模型”转向“benchmark / protocol / diagnostics / proof engineering”。

---

## 1. 当前项目的真实位置

### 1.1 现在不应再这样表述

不建议把项目继续写成：

> 我们提出了一个更强的双曲模型，并在 Lean/Mathlib hierarchy 图上稳定优于欧氏模型。

因为截至目前，证据并不支持这个强版本命题。

### 1.2 现在更准确的表述

当前更合理的项目定位是：

> 我们构建了一套面向真实 traced Lean/Mathlib hierarchy 图的工程化实验管线，完成了 precise hierarchy 抽取、coverage-aware 修复、relation-aware 子图构建、grouped retrieval 协议与图结构诊断，并据此分析双曲归纳偏置在何种数据条件下可能有效。

这个定位同时保留了两件事：

1. 工程价值是真实的，不是脚本拼装。
2. 结论是条件性的，不是预设双曲必胜。

### 1.3 目前最稳定的经验判断

结合 `lean4-example`、`plausible`、`batteries` 以及模块级 `Mathlib` 候选子图的结果，当前可以稳妥地认为：

1. 旧的单正例 `ancestor_ranking` 协议确实不合理。
2. grouped multi-positive retrieval 更贴近真实任务结构。
3. grouped retrieval training 显著改善了任务对齐，但没有让 HGCN 形成稳定反超。
4. 当前真实图的 relation layer 往往过浅、过碎、过像星状森林，不是双曲优势最自然的释放场景。
5. 在现有数据和任务上，relation-aware GCN 仍是更强、更稳的 baseline。

---

## 2. 本项目的目标与非目标

### 2.1 目标

本阶段只追求下面五类成果：

1. **可复现管线**
   - traced repo -> normalized trace -> declaration graph -> precise hierarchy -> coverage-aware repair -> relation-aware benchmark。

2. **标准化协议**
   - 统一 node / edge 定义。
   - 统一 grouped retrieval 评测。
   - 统一 train/valid/test 切分和 seed sweep 方式。

3. **结构诊断**
   - 判断哪些真实图是 shallow forest。
   - 判断哪些局部模块更接近值得检验双曲优势的 hierarchy。

4. **训练目标对齐**
   - 从 binary edge classification 迁移到 query-grouped retrieval training。
   - 让训练目标和评测任务尽量一致。

5. **论文可写性**
   - 把项目推进成 benchmark / protocol / diagnostics 论文，而不是被绑定在单一模型胜负上。

### 2.2 非目标

当前不再把以下事项作为主承诺：

1. 自动证明双曲一定优于欧氏。
2. 直接做端到端长证明生成。
3. 一开始就把全量 Mathlib 当成唯一目标。
4. 把表达式级显式编码当作主论文中心。
5. 把 `γ` 等特殊常数探索当作主项目承诺。

---

## 3. 证据链与设计后果

### 3.1 任务口径已经修正

`ancestor_ranking` 的真实结构不是单一 positive ranking，而是：

> 同一个 `(src, relation)` 查询下对应多个真祖先。

因此默认协议应为：

- `Recall@1/3/5/10`
- `MAP`
- `nDCG`
- `grouped-MRR`
- hop 分桶：`hop_2`、`hop_3`、`hop_4_plus`

旧的单正例 `MRR` 只能作为辅指标。

### 3.2 训练侧也存在错配

即便评测已经修正，如果训练仍然是 `BCEWithLogitsLoss` 的逐边二分类，那么仍然存在第二层错配：

- 训练学的是“这条边存不存在”
- 评测看的是“同一查询下候选祖先的排序质量”

因此下一阶段必须推进：

- `grouped softmax`
- `InfoNCE`
- `listwise ranking`
- `contrastive retrieval`

### 3.3 图结构已经给出约束

当前诊断更支持这样的判断：

- 全图并不天然是深层树。
- relation layer 虽然干净，但大多是浅层 forest / star forest。
- 在这种结构上，欧氏模型本来就可能足够强。

所以后续实验不应默认“多调 HGCN 就会赢”，而应优先筛选更深层、更连续、更有层级密度的候选图。

---

## 4. 数据资产与版本锁定

### 4.1 必须锁定的对象

每次正式实验都必须固定：

1. `Lean` 版本
2. `Mathlib` commit
3. `LeanDojo` / tracing 工具版本
4. Python 依赖与模型依赖
5. 图抽取脚本版本
6. 评测脚本版本

### 4.2 需要固化的中间产物

建议把每个数据快照都写成完整资产包，至少包含：

1. normalized trace
2. declaration graph
3. precise hierarchy graph
4. coverage-aware backfill 结果
5. relation-aware 子图
6. 图结构诊断报告
7. baseline 结果汇总

### 4.3 关键的现有资产

当前可以直接作为对照或复验基础的资产包括：

- `artifacts/diagnostics/real_graphs_v1/report.md`
- `artifacts/diagnostics/hierarchy_focus_v1/report.md`
- `artifacts/baselines/relation_seed_sweeps/`

这些资产已经足够支撑后续写成 benchmark 型论文的骨架。

---

## 5. 图构建与切分策略

### 5.1 推荐的图族

后续不应只保留一张“大图”，而应拆成以下图族：

1. **full graph**
   - 用于整体诊断，不作为唯一主战场。

2. **relation-aware hierarchy graph**
   - 只保留 `extends / instance_of` 等层级边。

3. **typeclass-heavy graph**
   - 适合检验 `instance_of` 主导的场景。

4. **hierarchy-only graph**
   - 去掉大部分 `uses` 上下文，检验纯层级结构。

5. **explicit-only / synthesized-only / mixed**
   - 用于拆解 Lean 特有边的来源。

6. **module-level candidate subgraphs**
   - 例如 `Mathlib.Algebra.Order.Ring`
   - `Mathlib.Algebra.Ring.Subring`
   - `Mathlib.Algebra.Field.Subfield`
   - `Batteries.Control.AlternativeMonad`
   - `Batteries.Classes.Order`

### 5.2 切分原则

切分不能随机糊弄，至少要满足以下约束：

1. 同一 `(src, relation)` 的正例不能泄漏到不同 split。
2. 查询级切分优先于单边随机切分。
3. 模块级切分优先于全图随机切分。
4. 需要保留 seed sweep 的可复现入口。

### 5.3 coverage-aware 处理

对于真实仓库，必须继续保留 coverage-aware 思路：

- 能回填的端点要回填
- 无法可靠恢复的端点要显式标注
- 不能把 unresolved 强行当负例

---

## 6. 任务体系

### T0. 图结构诊断

目标：

- 判断图是不是浅层 forest
- 判断哪类图更接近可释放双曲优势的层级结构

主要指标：

- longest chain
- leaf ratio
- component size
- cycle rank
- approximate hyperbolicity proxy
- ancestor/descendant recovery difficulty

产出：

- 诊断报告
- 候选子图排序
- go/no-go 建议

### T1. Grouped ancestor retrieval

目标：

- 作为 `ancestor_ranking` 的默认正式协议

输入：

- `(src, relation)`

正例：

- 同查询下全部真祖先

指标：

- grouped `MAP`
- grouped `nDCG`
- grouped `Recall@k`
- grouped-MRR
- hop-bucketed 结果

### T2. Typed parent retrieval

目标：

- 显式区分 `extends` 与 `instance_of`
- 验证 relation typing 是否影响模型差异

这一步很重要，因为当前许多图的层级信号并不等价。

### T3. Query-grouped retrieval training

目标：

- 把训练目标对齐到 grouped retrieval

建议实现：

- `InfoNCE`
- sampled softmax
- listwise ranking loss
- query-aware negative sampling

### T4. Relation provenance split

目标：

- 比较 `explicit-only`
- 比较 `synthesized-only`
- 比较 `mixed`

希望回答的问题是：

> Lean 特有的 synthesized 边，是否正在削弱双曲几何最容易利用的层级信号？

### T5. Proof-side retrieval / case study

目标：

- 让图表示不只停留在 link prediction
- 至少和 proof workflow 有一层直接接触

候选任务：

- premise retrieval
- relation-aware declaration recommendation
- hierarchy navigation
- ancestor explanation

---

## 7. 模型梯度与 baseline 体系

### 7.1 第一层：启发式与文本 baseline

先给最小可解释基线：

- degree / PageRank / ancestor overlap
- BM25 / lexical retrieval
- 简单文本匹配

### 7.2 第二层：欧氏图模型

作为强欧氏对照：

- GCN
- GraphSAGE
- GAT
- 简单 graph transformer

### 7.3 第三层：双曲模型

只在前两层已经站稳后再比较：

- Poincaré embedding
- HGCN
- Lorentz / hyperbolic GNN 变体

### 7.4 第四层：可选复杂模型

只有在任务和图结构都明确支持时，才考虑：

- 更复杂的 hyperbolic transformer
- relation-aware hyperbolic attention

### 7.5 统一比较原则

所有模型比较都要满足：

1. 相同数据快照
2. 相同 split
3. 相同 seed sweep
4. 相同评测协议
5. 相近参数预算

---

## 8. 阶段计划与阶段门

### 阶段 0：冻结版本与资产包

目标：

- 锁定 Lean / Mathlib / tracing 版本
- 固定数据快照
- 固定评测协议

交付物：

- version manifest
- data card
- experiment config index

### 阶段 1：图诊断与候选图筛选

目标：

- 给出全图和模块级图的结构画像
- 筛出更值得做双曲检验的候选图

阶段门：

- 诊断报告必须说明哪些图“浅”、哪些图“更深”
- 必须形成明确的优先级列表

### 阶段 2：协议固化

目标：

- 固化 grouped ancestor retrieval
- 固化 hop-bucket 统计
- 固化 grouped-MRR 作为主指标之一

阶段门：

- 以后所有正式结果都默认使用 grouped 协议

### 阶段 3：训练目标对齐

目标：

- 把训练从 binary edge classification 迁到 grouped retrieval

阶段门：

- 至少在 `Field.Subfield` 和 `Order.Ring` 上完成 5-seed 对照

### 阶段 4：relation provenance 拆分

目标：

- 对 `explicit-only / synthesized-only / mixed` 做系统比较

阶段门：

- 至少能回答“哪类边最削弱双曲优势”

### 阶段 5：更大更深层模块复验

优先候选：

1. `Mathlib.Algebra.Order.Ring`
2. `Mathlib.Algebra.Ring.Subring`
3. 更大的 `Mathlib.Algebra.Order` 局部簇

阶段门：

- 候选图的层级链长度和正例数必须明显高于当前最小图

### 阶段 6：应用性补强

目标：

- 至少给出一个 proof-side utility

可选产出：

- premise retrieval demo
- ancestor explanation demo
- relation-aware recommendation demo

---

## 9. 当前最关键的 go / no-go 判据

### Gate A：数据门

通过条件：

1. 版本锁定完成
2. 数据快照稳定
3. 至少一类标签可靠
4. 至少一张图能稳定抽取

### Gate B：协议门

通过条件：

1. grouped retrieval 已成为默认协议
2. 单正例 `MRR` 只保留为辅指标
3. hop 分桶已接入常规报告

### Gate C：训练门

通过条件：

1. grouped retrieval training 跑通
2. 训练/评测目标对齐
3. 结果在多个 seed 上稳定复现

### Gate D：双曲价值门

只有满足以下至少一项，才继续把双曲作为主假设：

1. 低维下优于欧氏模型
2. 在更深层 hop bucket 上形成稳定收益
3. 在更纯层级图上显著优于欧氏基线

若不满足，则双曲应降级为条件性 follow-up，而不是主承诺。

### Gate E：应用价值门

至少要满足一个：

1. retrieval 明显优于文本 baseline
2. proof-side utility 可演示
3. 图表示对 proving workflow 有直接帮助

若不满足，论文主线应转为 benchmark / diagnostics。

---

## 10. 论文叙事与投稿接口

### 10.1 当前最稳妥的主叙事

> 我们构建了真实 traced formal-math hierarchy 图的工程化管线、协议与诊断框架，并系统研究了在什么结构与任务条件下，双曲归纳偏置才可能对形式化数学图真正有效。

### 10.2 最适合的 venue 方向

当前优先级建议仍然是：

1. `ITP`
2. `CPP`
3. `FM`
4. `SEFM / ICFEM`
5. `FormaliSE` / workshop

其中：

- `ITP` 最适合 proof assistant 社区叙事。
- `CPP` 最适合 proof engineering / infrastructure 叙事。
- `FM` 适合完整的 formal methods + empirical protocol story。

### 10.3 论文里应突出什么

正文应突出：

1. 可复现管线
2. 任务口径修正
3. 图结构诊断
4. grouped retrieval 协议
5. 强欧氏 baseline
6. 条件性双曲结论

不应突出：

1. 单点 HGCN SOTA
2. 不稳定的小幅数值波动
3. 过度扩展的模型花活

---

## 11. 风险与备选路线

### 11.1 数据风险

风险：

- 版本漂移
- 关系端点缺失
- 标签语义不稳

对策：

- 固定快照
- 使用三值标签
- 不把 unresolved 当负例

### 11.2 模型风险

风险：

- HGCN 训练不稳定
- 双曲收益只在局部 bucket 偶发出现
- 参数量带来假增益

对策：

- 先做欧氏强基线
- 控制参数预算
- 做等预算对照

### 11.3 论文风险

风险：

- 故事线太散
- 过度依赖负结果
- 贡献点不够集中

对策：

- 主文只讲一条线
- 附录放失败案例
- 把贡献压成 benchmark / protocol / diagnostics

---

## 12. 近期最优先的执行顺序

未来最值得马上推进的顺序是：

1. **冻结数据与协议**
   - 先把默认 grouped retrieval 和版本锁定写死。

2. **扩展 grouped retrieval training**
   - 先在 `Field.Subfield`、`Order.Ring`、`Mathlib.Algebra.Order.Ring` 上跑通。

3. **做 relation provenance 拆分**
   - `explicit-only / synthesized-only / mixed` 三类图都要有结果。

4. **做更深层候选图复验**
   - 优先选更深、更连续的模块。

5. **整理成 benchmark / protocol 论文骨架**
   - 让结果服务于一个完整故事，而不是单次对照。

---

## 13. 默认工作约定

后续所有正式工作建议默认遵守以下约定：

1. 默认评测协议是 `grouped multi-positive ancestor retrieval`。
2. 默认训练目标优先尝试 grouped retrieval，而不是 binary edge classification。
3. 默认对照基线先做强欧氏，再做双曲。
4. 默认报告必须包含 5-seed mean ± std。
5. 默认必须补 hop 分桶。
6. 默认不能把 `synthesized` 负例当成高置信 negative。
7. 默认不能把当前项目写成“已经证明双曲优于欧氏”。

---

## 14. 一句话总结

> 现在的工程主线不是继续追一个更强的 HGCN，而是把真实 traced formal-math hierarchy 图的协议、诊断、训练对齐和 retrieval benchmark 做成一条稳定的研究管线，并据此判断双曲归纳偏置在何种结构条件下才真正值得用。
