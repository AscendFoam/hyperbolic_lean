# 投稿路线图（FM / ITP / CPP / 备选 venue 对照）

> 更新时间：2026-05-01
>
> 适用对象：当前这条“traced Lean/Mathlib 图构建 + precise hierarchy 抽取 + relation-aware / grouped retrieval 评测 + GCN/HGCN 对照诊断”的项目主线。

---

## 1. 先给结论

基于目前已经完成的工程与实验，最稳妥的投稿路线不是“冲广义 AI 顶会”，而是沿着 **formal methods / theorem proving / proof engineering** 社区推进：

1. **主线优先级最高**：`ITP` 或 `CPP`
2. **冲刺目标**：`FM`
3. **备选且更稳**：`SEFM / ICFEM`
4. **若需要先拿社区反馈**：`FormaliSE` 或相关 workshop / doctoral track

当前最不建议的主叙事是：

> “双曲方法在形式化数学图上稳定优于欧氏方法”

当前更适合的主叙事是：

> “构建真实 traced formal-math hierarchy 图的工程管线、任务协议与诊断基线，并系统分析双曲归纳偏置在何种结构与任务条件下可能有效”

---

## 2. venue 对照表

| Venue | CCF/官方定位 | 当前适配点 | 当前短板 | 还缺什么材料 | 当前判断 |
| --- | --- | --- | --- | --- | --- |
| `ITP` | 官方 conference series 明确聚焦 interactive theorem proving；我没有在当前检索到的 CCF 软件工程/系统软件/程序设计语言页面上直接找到它。 | 社区和 `Lean / Mathlib / proof assistant` 高度贴合；真实 traced 仓库、precise hierarchy、模块级 `Mathlib` 子图、grouped ancestor retrieval 这些内容都容易被理解为“对 theorem proving 社区有直接价值”的基础设施与实验协议贡献。 | 纯模型结果不够强，`HGCN` 未形成稳定优势；如果只讲“模型谁赢了”，创新度不够集中。 | 1. 把贡献改写成“数据与协议 + 诊断基线”。 2. 至少补一项更贴近 proof assistant 使用场景的 downstream 任务或 case study。 3. 把 artifact 打磨到可复现发布级别。 | **最适合当前项目的主投方向之一** |
| `CPP` | 官方 conference series 明确聚焦 certified programs and proofs；我没有在当前检索到的 CCF 软件工程/系统软件/程序设计语言页面上直接找到它。 | 如果把工作强调为“proof engineering / proof infrastructure / proof graph benchmark”，与 `CPP` 也比较契合；尤其是 precise exporter、normalized trace、relation-aware task、可复现实验包，都是工程化贡献。 | `CPP` 往往更喜欢与程序证明、证明工具、证明产物消费方式更直接相关的故事；当前项目偏图学习诊断，和核心 `CPP` 风格还有一点距离。 | 1. 增加一个明确的 proof-side utility，例如 hierarchy retrieval 对搜索、导航、依赖理解的帮助。 2. 补一个更像 tool/demo 的使用场景。 3. 强化 “why this matters for proof development” 的段落。 | **与 ITP 并列的主投候选** |
| `FM` | CCF 软件工程/系统软件/程序设计语言页面中列为 `A 类`。 | `FM` 能容纳“formal methods + tool support + empirical evaluation + negative/diagnostic insight”这类组合；如果文章重点放在 traced formal-math graph engineering、协议修正、结构诊断与系统性复验，而不是单点模型 SOTA，叙事上是成立的。 | `FM` 的门槛会更看重“完整研究故事”；如果只是几张图上的 baseline 对照，容易显得像一篇未收束的 exploratory study。 | 1. 至少一套更完整的 benchmark/package 发布方案。 2. 更大一点的真实目标，证明结论不只来自单一小图。 3. 训练目标与评测协议进一步对齐，例如 grouped/listwise retrieval training。 4. 更系统的 error analysis 与威胁讨论。 | **可以冲，但属于 stretch target** |
| `SEFM` | 当前检索到的 CCF 软件工程/系统软件/程序设计语言页面上未直接找到。 | 很适合承接“软件工程化 + formal methods + toolchain + empirical study”叙事；对工程完整性、可复现性、评测协议设计通常比较友好。 | 影响力和理论高度一般不如上面三者；如果后续材料已经足够强，再投这里会有一点“保守”。 | 1. 把 tracing / normalization / diagnostics / baselines 做成清晰的软件包。 2. 多仓库复验。 3. 写清楚工程设计原则与失败案例。 | **强备选，现实可行** |
| `ICFEM` | CCF 软件工程/系统软件/程序设计语言页面中列为 `C 类`。 | 对 formal engineering、工具与实证研究较友好；当前项目的“工程化实验方案 + 真实仓库复验 + 协议修正”比较容易对接。 | 社区传播力通常弱于 `ITP / CPP / FM`；若后续目标是更强社区影响，优先级应低于前三者。 | 1. 强化工程完整性与 artifact。 2. 把 negative result 讲成“有约束的经验结论”，而不是单纯未跑出优势。 | **稳妥备选** |
| `ATVA / TASE` | CCF 软件工程/系统软件/程序设计语言页面中列为 `C 类`。 | 如果后续把文章更偏向“formal-analysis tooling + task protocol + verification-oriented diagnostics”，这两类 venue 也能接住。 | 和当前 Lean / proof assistant 叙事没有 `ITP / CPP` 那么天然贴合。 | 1. 更强调 formal analysis / verification 价值。 2. 补更清晰的 tool-evaluation 部分。 | **可作为 second-backup** |
| `FormaliSE` 或相关 workshop | workshop，不宜按主会级别理解。 | 很适合先投递“协议、诊断、初步 benchmark”版本，快速拿反馈，尤其当主线论文还差一轮大规模复验或 downstream case study 时。 | workshop 级别天然较低，不适合作为项目最终主目标。 | 1. 压缩成更短、更聚焦的故事。 2. 选择一个主结论，不要把所有工程细节都塞进去。 | **适合抢先交流，不适合作为终局目标** |

---

## 3. 每个 venue 最匹配的叙事版本

| Venue | 最推荐叙事 |
| --- | --- |
| `ITP` | “我们构建了面向 Lean/Mathlib 的真实 traced hierarchy 图抽取与评测管线，并发现许多直觉上被认为适合双曲表示的结构，在真实 proof graph 中其实更浅、更碎、更 star-like；因此提出了更合理的任务协议与诊断框架。” |
| `CPP` | “我们提供一套可复现的 proof graph engineering pipeline，使 formal proof artifact 可以被抽取、标准化、诊断，并用于 hierarchy retrieval / relation-aware prediction 等任务。” |
| `FM` | “我们系统研究 traced formal-math graphs 的结构、协议与模型错配问题，展示从数据工程到评测修正再到基线诊断的完整闭环，并用真实仓库与 `Mathlib` 模块复验结论。” |
| `SEFM / ICFEM` | “这是一套以工程可落地性与经验诊断为核心的 formal-math graph infrastructure paper，重点是 toolchain、benchmark、协议与复现。” |

---

## 4. 从现在到可投稿，还差哪些“硬材料”

这些材料无论投 `ITP / CPP / FM`，几乎都值得补：

1. **更稳定的主实验包**
   当前 strongest story 已经不是 `HGCN` 反超，而是：
   - precise hierarchy 抽取
   - grouped multi-positive retrieval 协议
   - relation-aware 欧氏基线
   - 图结构与任务结构诊断

2. **更像 benchmark 的发布形态**
   需要把下面几部分整理成可以开源复现的成套 artifact：
   - tracing config
   - normalization config
   - precise exporter
   - declaration graph / hierarchy graph 构建脚本
   - baseline config
   - diagnostics config
   - 结果汇总模板

3. **至少一个更贴 proof workflow 的任务**
   例如：
   - hierarchy navigation / ancestor retrieval
   - typed parent retrieval
   - relation-aware declaration recommendation
   - 面向 proof exploration 的 case study

4. **一轮更强的“任务-训练对齐”实验**
   当前评测已经升级成 grouped retrieval，但训练目标仍偏 binary link prediction。
   下一步最值得补的是：
   - query-grouped retrieval training
   - listwise / contrastive retrieval loss
   - 与现有 grouped metrics 同口径复验

5. **一段更明确的威胁与适用边界分析**
   这恰好是当前项目的强项，不应该回避：
   - traced graph 受抽图协议影响很大
   - full graph 与 relation layer 的几何性质不一致
   - 双曲优势在真实数据中并非天然出现
   - 负结果来自真实结构诊断，而不是简单“模型没调好”

---

## 5. 推荐的投稿顺序

如果按“投入产出比 + 当前成熟度”排序，我建议：

1. **第一优先：准备 `ITP / CPP` 版本**
   把文章主结论收敛到：
   - real traced Lean graph engineering
   - precise hierarchy extraction
   - grouped retrieval protocol
   - graph/task diagnostics
   - relation-aware baseline study

2. **第二优先：把同一套材料扩到可冲 `FM` 的版本**
   触发条件是至少补上以下两项中的一项：
   - 一个更强的 task-aligned training 结果
   - 一个更完整的多仓库 / 多模块复验与 artifact package

3. **第三优先：若主线稿件还差火候，则转 `SEFM / ICFEM`**
   这不是失败路线，而是更强调工程价值与可复现性的路线。

4. **第四优先：若需要尽快交流，可先发 workshop**
   尤其适合在正式主投前先拿社区反馈，压实叙事。

---

## 6. 一个更现实的判断

如果后续实验按当前最合理的方向推进，我对投稿层级的判断是：

- **最现实的强匹配目标**：`ITP`、`CPP`
- **最合理的冲刺目标**：`FM`
- **最稳的备选**：`SEFM`、`ICFEM`

而“广义 AI 顶会式 CCF-A 主线投稿”目前仍然不现实，原因不是项目没价值，而是：

1. 当前贡献更偏 **formal-math graph infrastructure + diagnostics + evaluation protocol**；
2. 主要发现是“负结果 + 边界条件澄清”，而不是一个普适的新模型 SOTA；
3. 真正最懂这件事价值的审稿社区，仍然是 theorem proving / formal methods，而不是大而泛的图学习或机器学习主会。

---

## 7. 一句话版本

> 这条项目线现在最适合投向 `ITP / CPP`，以 `FM` 为冲刺、`SEFM / ICFEM` 为稳妥备选；论文核心不应继续押注“证明双曲优于欧氏”，而应收敛为“真实 traced formal-math hierarchy 图的工程构建、协议修正、结构诊断与强基线研究”。

---

## 8. 官方入口

- CCF 软件工程 / 系统软件 / 程序设计语言推荐列表：<https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/>
- ITP conference series：<https://itp-conference.github.io/>
- CPP conference series：<https://www.sigplan.org/Conferences/CPP/>
- CPP 2026 页面：<https://popl26.sigplan.org/home/CPP-2026>
- FM 2026 CFP：<https://www.fmeurope.org/2025/09/10/fm-2026-call-for-papers/>
