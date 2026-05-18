# T50 Paper Skeleton

## Task ID
T50

## Goal
把 Milestone 1~4 已 reviewed 的证据整理成可投稿的 paper skeleton，围绕 `pipeline / protocol / diagnostics / provenance-conditional hyperbolic conclusion` 写出主张边界、贡献列表、图表计划、threats、venue fit 与 proof-side bridge。

## Why Now
Milestone 4 已经由 `T43_review` 正式收口，项目当前最缺的不是更多实验，而是把已经存在的 reviewed artifact 组织成可复述、不过度外推、可直接支撑后续投稿与 proof-side MVP 选择的叙事骨架。若继续停留在实验报告堆叠状态，后续 `T51/T52/T53` 会缺少统一 claim 边界与证据结构。

## Allowed Files
- `docs/paper_outline.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope
- 不要新增训练、seed sweep、图生成、结构诊断或任何代码改动
- 不要改写 T40/T41/T42/T43 已冻结的 provenance 语义、实验数值或主结论
- 不要把 mixed graph 上的结论改写成 “HGCN 整体优于 GCN”
- 不要忽略 clean-environment reproducibility、`R28` 或 `R29`
- 不要重写 `docs/02_experiment_plan.md`

## Inputs to Read
- `docs/02_experiment_plan.md`
- `docs/experiment_reports/grouped_training_summary.md`
- `docs/experiment_reports/provenance_summary.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/02_experiment_plan.md` 中链接的 venue 对照说明文档

## Expected Output
- 新增 `docs/paper_outline.md`，至少包含以下部分：
  - working title / one-paragraph positioning
  - central claim 与 non-claim 边界
  - 3~5 条 paper contributions
  - evidence ladder（Milestone 1~4 各自提供什么证据）
  - figures / tables plan
  - threats to validity
  - venue fit（至少覆盖 `ITP` / `CPP` / `FM`）
  - proof-side bridge：说明为什么 `T51` 需要从 paper story 延伸到 utility MVP
- 同步更新治理文档，使 `T50` 完成后项目可以切换到 `T51`

## T50-Specific Notes
- 必须把项目主结论写成 provenance-conditional：full source graph 上 GCN 仍领先，HGCN 只在 `explicit_only` hierarchy 上显出优势。
- 必须明确 `explicit_only` / `synthesized_only` / `hierarchy_mixed` 的证据角色分别为 primary evidence / controlled diagnostic / reproducibility check。
- 必须把 Milestone 3 与 Milestone 4 的关系写清楚：T43 是对 “GCN overall ahead” 的细化，而不是推翻。
- 必须保留 clean-environment reproducibility 尚未完全闭环的边界，不能写成已经完成 clean-room reproduction。
- 在 `R29` 关闭前，不要直接引用 `docs/experiment_reports/provenance_summary.md` Section 5.1 中 Field.Subfield `synthesized_only` 的错误 GCN 表格单元；在 `R28` 关闭前，不要把该 split 写成“全部 per-seed 都是 1.0”。
- 不要把 paper skeleton 写成已经接受或已经达到 SOTA 的叙事。

## Verification
```powershell
rg -n "Title|Claim|Contribution|Figure|Table|Threat|Venue|ITP|CPP|FM|proof-side|provenance-conditional" docs\paper_outline.md
rg -n "T50|paper_outline|Current Unique Task|Milestone 5|Venue|proof-side" docs\04_task_board.md docs\05_decision_log.md docs\07_handoff.md docs\08_risks_and_open_questions.md
```

## Docs to Update
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type
milestone
