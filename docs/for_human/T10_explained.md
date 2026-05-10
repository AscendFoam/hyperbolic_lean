# T10 Explained: 版本锁定与数据资产 Manifest

## 1. 通俗解释：这个任务在做什么？

想象你在一个建筑工地上，已经搭建了不少实验设备（trace 工具、图构建脚本、训练模型），各种数据文件散落在仓库的不同角落。T10 的任务就是做一次**全面的资产清点**——把"我们用了哪个版本的 Lean？""哪个版本的 Mathlib？""哪些配置文件负责生成哪些数据？""哪些实验产物已经存在？"这些问题全部梳理清楚，写成一份清单。

这份清单（`docs/data_manifest.md`）的作用类似于实验记录本的第一页：**在开始任何可复现的正式实验之前，必须先锁定所有依赖的版本和数据的来源**。如果版本信息不确定，就必须老老实实地标上"未知 / 待核实"，而不能编造。

## 2. 实现详解

### 2.1 任务目标

根据任务包 `docs/tasks/M1_protocol/T10_version_manifest.md`，T10 的目标是：

> 生成版本锁定与数据资产 manifest，列出当前正式实验依赖的 Lean、Mathlib、LeanDojo、Python 依赖、关键 config、脚本和 artifact 路径。

核心约束：**不编造版本信息**，未知版本必须标为 `unknown / needs verification`。

### 2.2 任务流程

Worker 执行了以下步骤：

1. **阅读现有配置和文档**：查看 `project_bootstrap/` 下各子包的 README、configs、以及 `artifacts/` 目录结构，从这些可复现的文件中提取版本锚点。

2. **创建 `docs/data_manifest.md`**：新文件，包含八个部分：
   - **Repository Snapshot**：当前仓库 commit 和治理文档入口
   - **Version Anchors**：Lean（小目标 trace 路线确认 `v4.20.0`，`lean4-example` 标为 unknown）、Mathlib（确认了 `c211948...` commit，`lean4-example` 标为 unknown）、LeanDojo（确认使用但精确版本 unknown）、Python（列出了依赖包名，但精确版本 unknown）
   - **Trace Targets And Commits**：`plausible`、`batteries`、`lean4-example`、`mathlib4` 的 repo / commit / config / output root
   - **Data Asset Layout**：raw trace、interim、processed 目录下的文件清单
   - **Config Index**：按功能分类的代表性配置文件路径（trace、baseline、diagnostics、Mathlib follow-up）
   - **Artifact Index**：按类型分类的实验产物路径（diagnostics、baselines、seed sweeps）
   - **Known Unknowns**：明确列出六个尚未核实的字段
   - **Usage Rule**：指导后续任务如何引用和使用这份 manifest

3. **更新治理文档**：
   - `docs/04_task_board.md`：添加 T10 执行记录，修正 Allowed files 列表（移除不在任务包中的 `docs/tasks/**`），说明任务处于 reviewer 前状态
   - `docs/07_handoff.md`：更新接手说明，写明 T10 草稿已产出、哪些版本仍未核实
   - `docs/08_risks_and_open_questions.md`：新增 R10 风险（未锁定精确版本的复现性风险）和 Open Question #9（用什么证据关闭 unknowns）

4. **运行验证**：执行了任务包要求的 `rg` 检索和 `git diff` 命令。

### 2.3 文件变化汇总

| 文件 | 变化类型 | 内容概要 |
| --- | --- | --- |
| `docs/data_manifest.md` | 新增 | 版本锚点、config 索引、artifact 索引、known unknowns |
| `docs/04_task_board.md` | 修改 | 添加 2 条 Execution Note，修正 1 处 Allowed files 列表 |
| `docs/07_handoff.md` | 修改 | 更新第 7 节闭环状态，添加 reviewer 前约束 |
| `docs/08_risks_and_open_questions.md` | 修改 | 新增 R10 风险和 Open Question #9 |

### 2.4 对后续开发的意义

这份 manifest 是整个 **Milestone 1（Data And Protocol Freeze）** 的基础：

- **T11（data card）** 将在此基础上补充字段语义、relation provenance 描述和 coverage-aware 处理说明。
- **T12（协议固化）** 引用 manifest 中的 config index 来确认评测代码入口。
- **T20+（诊断与训练）** 的所有正式实验都应以 manifest 中锁定的版本为基准。

特别是 Section 7（Known Unknowns）提醒后续任务：在声称复现性之前，必须先用 `pip freeze`、trace 元数据或环境清单来关闭这些 unknowns。

## 3. 为什么给出 PASS 的 review 结果？

### 审查过程

我作为 reviewer 执行了以下检查：

1. **任务完成度**：任务包要求 version manifest、config index、artifact index、unknowns 四类内容，manifest 全部覆盖。
2. **范围合规**：`git status` 确认只有 `Allowed files` 被修改，`project_bootstrap/` 和代码文件完全未碰。
3. **路径真实性**：我抽查了 5 个 config 路径和 5 个 artifact/data 路径，全部在磁盘上实际存在。
4. **unknowns 诚实性**：所有无法从仓库内可复现文件确认的版本都标为 `unknown / needs verification`，没有编造。
5. **治理一致性**：`04_task_board.md`、`07_handoff.md`、`08_risks_and_open_questions.md` 三份文档的更新相互一致，且与 T01 review 后的状态衔接正确。
6. **未越权完成**：Worker 没有把 T10 标记为已完成，而是等待 reviewer 结论。

### 判决理由

- 任务包目标全部达成，没有遗漏。
- 没有伪实现、mock、stub 或 hardcode——这是一份纯文档任务，所有信息都来自仓库内可验证的文件。
- 验证命令已运行，结果与 diff 一致。
- 没有破坏已有功能（T10 是纯新增文档 + 治理文档更新，不影响任何代码行为）。
- 没有把计划写成事实——manifest 明确标注为 draft，unknowns 保留为 unknown。
- 唯一的小修正（移除 `docs/tasks/**` 从 Allowed files）是在修正任务板本身与任务包的不一致，属于合理的 self-correction。

因此判定为 **PASS**，无 blocking 或 non-blocking issues。
