# T31A Review: Query-Level Split Completeness

> Reviewer: adversarial (code + data pipeline change)
> Date: 2026-05-13
> Task package: `docs/tasks/M3_training/T31A_query_level_split_completeness.md`

## Verdict: PASS

## Blocking issues

- None.

## Non-blocking issues

1. **`ancestor_label_mode` 与 query key 的交互未显式文档化。** `query_key_for_relation_example` 使用 `(example[0], example[2])` = `(src_id, relation_type)`。当 `ancestor_label_mode="source_kind"` 时，`relation_type` 取值为 `extends_ancestor` / `instance_ancestor`，而非原始 `extends` / `instance_of`。这意味着 query-level split 实际按 `(src, extends_ancestor)` 和 `(src, instance_ancestor)` 两组分别切分，而不是按原始 `(src, extends)` 切分。这在当前场景下是正确的行为——因为 grouped retrieval 在 eval 侧 `build_grouped_ranking_queries` 也按 `(src_id, relation_type)` 分组，两边 key 语义一致——但值得在 `training_alignment_audit.md` 的 4.1 节补一句说明，避免未来 worker 混淆 "source_kind label" 和 "原始 relation type"。

2. **R19 状态更新仍保留 `Active`。** 风险表已更新为 "worker draft 已实现"，但未把状态改为 `Mitigated` 或加注 "pending review"。这是合理的保守处理（review 前不关风险），Captain 在 review 通过后应显式更新 R19 状态。

3. **Section numbering 连续性。** `training_alignment_audit.md` 的 Section 4 下面直接出现 4.1 和 4.2，而 Section M4 的 heading 是 `## M4.` 而不是 `## 4.`。这是 T30 遗留的 heading nesting 问题（已记录在 D11），T31A 没有让问题恶化，但也没有顺便修正。deferred 到 D11 处理。

4. **`stratified_split_relation_examples_by_query` 的分层粒度。** 当前先按 `relation_type` 分桶，再在每个桶内按 `(src, relation_type)` query 切分。这与旧 `stratified_split_relation_examples` 的分层策略一致（都是按 relation_type 分桶），因此 split 比例在各 relation_type 间是平衡的。这是合理的。但如果某个 relation_type 下 query 数极少（比如只有 1-2 个），`n_val` 和 `n_test` 都会 round 到 0，导致该 relation_type 的全部 query 进 train。当前 smoke 确认 `extends_ancestor` 只有少量 query（35 个 positive examples），但 split 结果仍是 disjoint 的。这不是 bug，但在更大图上可能需要关注 rare relation type 的 split 覆盖率。不需要本轮修复。

## Missing tests or verification

- None. Worker 已完成两层验证：
  1. `rg` 静态检查确认 query-level split 入口、断言和文档落点存在。
  2. 实际运行 smoke config，产物 `run_manifest.json` 中 `query_split_summary` 确认 `split_strategy = query_level`、所有 overlap 为 0、`is_query_level_disjoint = true`。

## Suspicious implementation details

- None. 实现直接且干净：
  1. `query_key_for_relation_example` 与 `build_grouped_ranking_queries` 使用完全一致的 key `(src_id, relation_type)`。
  2. `assert_query_level_split_disjoint` 在 split 后立即执行，如果不 disjoint 会 raise `ValueError`，不是软警告。
  3. 分支逻辑只在 `task == "ancestor_ranking"` 时走新路径，其他 task family 保持原 split。
  4. `query_split_summary` 写入 `run_manifest.json`，可追溯。
  5. 没有 mock、stub、hardcode 或过度抽象。

## Recommended next action

- Captain 应将 T31A 标记为完成。
- Captain 应更新 R19 状态从 `Active` 改为 `Mitigated`（或 `Active -> T31A reviewed and closed`）。
- Captain 应将 D10 标记为已关闭。
- 当前唯一任务可切换到 `T31`。
- T31 worker 应注意 Non-blocking issue #1 中 `ancestor_label_mode` 对 query key 的影响，确保 grouped loss 的 query 分组与 split 的 query 分组使用一致的 key 语义。
