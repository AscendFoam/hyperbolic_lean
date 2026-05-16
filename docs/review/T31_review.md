# T31 Review: Minimal Query-Grouped Loss

> Reviewer: adversarial (training objective + data pipeline change)
> Date: 2026-05-13
> Task package: `docs/tasks/M3_training/T31_min_query_grouped_loss.md`

## Verdict: PASS

## Blocking issues

- None.

## Non-blocking issues

1. **`grouped_loss="infonce"` is accepted as config alias but maps to the same implementation as `sampled_softmax`.** Lines 343-347 normalize `"grouped_softmax"` to `"sampled_softmax"` and accept both `"sampled_softmax"` and `"infonce"`, but the actual loss function `sampled_softmax_loss` (line 141) is identical for both. The worker correctly disclosed this in the handoff and training alignment audit ("`grouped_loss="infonce"` 目前只是兼容配置名"). This is acceptable for a minimal implementation — the mathematical form `F.log_softmax -> -pos_log_probs.mean()` is indeed the InfoNCE / sampled-softmax family — but future work should either (a) explicitly document that both names point to the same implementation, or (b) differentiate them if a true contrastive variant is needed. Not blocking because the task package says "优先 sampled softmax 或 InfoNCE" and the current implementation covers both semantics.

2. **`negative_ratio` default differs between grouped runner and config.** The grouped runner uses `float(config.get("negative_ratio", 10.0))` (line 406) while the smoke config uses `"negative_ratio": 1.0`. The old GCN/HGCN runners also default to `1.0`. The smoke config explicitly sets it to `1.0`, so the smoke result is correct, but the runner default of `10.0` could surprise future users who omit this field. Not blocking because it doesn't affect the current smoke or task correctness.

3. **`total_loss` accumulation uses `torch.tensor(0.0)` instead of `new_zeros`.** Line 222 creates `total_loss = torch.tensor(0.0)` which doesn't live on the same device as model parameters. This works because PyTorch broadcasts on addition, but it would be cleaner to use `scores.new_zeros(())` (as done inside `sampled_softmax_loss` at line 146). Not blocking because the smoke runs successfully and the accumulation is numerically correct.

4. **`docs/00_raw_idea.md`, `docs/01_feasibility_report.md`, `docs/03_architecture.md`, `docs/05_decision_log.md`, `docs/06_eval_protocol.md` are modified but not in T31's Allowed Files.** These are Captain-level updates recording the T31A review result and task switch to T31 — they are not T31 worker changes. The T31 worker's actual file scope is within bounds: `run_relation_grouped_retrieval_baseline.py`, `relation_baseline_common.py`, `relation_tasks.py` (under `src/`), the new config, and the listed docs. Not blocking because the out-of-scope changes are Captain updates, not worker modifications.

5. **`.claude/settings.json` auto-permission diff present.** Same pattern as T14. Should be excluded from any commit, not part of T31 review scope.

## Missing tests or verification

- None. Worker completed both verification steps:
  1. Static: `rg -n "InfoNCE|sampled_softmax|grouped"` confirms the loss function and query group construction are present in source and config.
  2. Runtime: smoke run succeeded with `epochs=1`, and all three artifact files (`grouped_training_summary.json`, `training_stats.json`, `result_summary.json`) confirm `training_loss = sampled_softmax` and `query_key_fields = ["src_id", "relation_type"]`.

- The smoke artifact also confirms:
  - `query_split_summary.is_query_level_disjoint = true` (T31A evidence carried forward).
  - `training_stats.best_val_grouped_map = 0.203` confirming grouped val MAP drives model selection (not binary AP).
  - 780 training queries with the correct relation type breakdown (`extends_ancestor: 11, instance_ancestor: 769`).

## Suspicious implementation details

- None. The implementation is clean and well-targeted:

  1. **Query key alignment is solid.** `build_query_groups` calls `build_grouped_ranking_queries(positive_examples, candidate_pools)` which uses the same `(src_id, relation_type)` key as T31A split and eval. The key semantics chain is:

     ```
     T31A split: stratified_split_relation_examples_by_query -> key = (example[0], example[2])
     T31 training: build_query_groups -> build_grouped_ranking_queries -> key = (src_id, relation_type)
     T31 eval: build_ranking_task_metrics -> build_grouped_ranking_queries -> key = (src_id, relation_type)
     ```

     All three use the identical key construction.

  2. **Model selection uses grouped val MAP.** Lines 306-308 use `val_grouped_map` (not binary val AP) for best-checkpoint selection. This directly addresses M5 in the training alignment audit.

  3. **No mock, stub, or hardcode.** The `_sample_negative_ids` helper does real negative sampling from the candidate pool, excluding self and all positives. `sampled_softmax_loss` is a real InfoNCE/sampled-softmax implementation using `F.log_softmax`.

  4. **No architecture changes.** The model constructors (`RelationAwareGCNLinkPredictor`, `RelationAwareHyperbolicLinkPredictor`) are imported as-is.

  5. **Old BCE runners untouched.** `run_relation_gcn_baseline.py` and `run_relation_hyperbolic_baseline.py` have no diff in this task.

## Recommended next action

- Captain should mark T31 as complete.
- Captain should update R07 status to reflect that the grouped runner path now has aligned training/eval (while the old BCE runners remain unchanged).
- Captain should update R21 from Mitigated to Mitigated/Closed after confirming this review.
- Current unique task can switch to `T32` (5-seed GCN grouped training sweep on `Field.Subfield` and `Order.Ring`).
- T32 worker should use the grouped retrieval runner (not the old BCE runner) and run with `negative_ratio` explicitly configured rather than relying on the runner's default of `10.0`.
