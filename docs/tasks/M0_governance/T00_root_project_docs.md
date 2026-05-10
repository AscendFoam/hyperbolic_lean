# T00 Root Project Docs

## Task ID

T00

## Goal

创建根目录 `README.md`、`AGENTS.md`、`CLAUDE.md`，让后续 Captain / Worker / Reviewer 从仓库入口就能理解项目定位、当前治理文件、任务纪律和 review 方式。

## Why Now

`docs/00~08` 已经初始化，但 workflow 要求最小启动至少具备 `README.md` 和 `AGENTS.md`。当前根目录缺少这些入口，后续 worker 容易直接改代码或重复历史任务。

## Allowed Files

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`

## Forbidden Scope

- 不修改 `docs/02_experiment_plan.md`
- 不修改 `project_bootstrap/` 下任何代码或配置
- 不运行 tracing、训练、seed sweep 等长任务
- 不新增实验结果或声称双曲已经稳定优于欧氏
- 不领取 T01 或 T10

## Inputs to Read

- `docs/reference/AI_coding_workflow.md`
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Expected Output

1. `README.md`
   - 项目一句话定位
   - 当前主线与非目标
   - 重要目录说明
   - 如何开始一个 Captain / Worker / Reviewer 循环
   - 当前唯一任务入口

2. `AGENTS.md`
   - Captain / Worker / Reviewer 职责
   - 单任务纪律
   - Allowed files / Forbidden scope 规则
   - verification 与 review 规则

3. `CLAUDE.md`
   - Claude reviewer 只读审查规则
   - PASS / PASS_WITH_WARNINGS / BLOCK 输出格式
   - 高风险任务 adversarial review 触发条件

4. `docs/04_task_board.md`
   - 若 T00 完成，由 worker 不要标记完成；只可在备注中说明已按任务包更新入口文档。最终勾选由 Captain 在 review 后完成。

5. `docs/07_handoff.md`
   - 补充 T00 worker 已创建入口文档的交接说明。

## Verification

运行或人工完成：

```powershell
git diff -- README.md AGENTS.md CLAUDE.md docs/04_task_board.md docs/07_handoff.md
```

验收标准：

1. 三个根目录文件存在且内容不矛盾。
2. README 没有把计划写成已完成事实。
3. AGENTS 明确 worker 只能改 Allowed files。
4. CLAUDE 明确 reviewer 默认只读。
5. 没有修改 Forbidden scope。

## Docs to Update

- `docs/04_task_board.md`
- `docs/07_handoff.md`

## Reviewer Type

normal

## Worker Final Report Must Include

1. 改了什么。
2. 如何验证。
3. 是否有未完成或不确定事项。
4. 是否触碰了 Forbidden scope。
