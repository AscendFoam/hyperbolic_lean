# Grouped Retrieval Protocol

> Updated: 2026-05-11
>
> Status: Reviewed T12 protocol freeze. `docs/review/T12_review.md` returned PASS; hop-bucket report surfacing remains assigned to T13.

## 1. Canonical Task Name

The canonical benchmark protocol name is:

```text
grouped multi-positive ancestor retrieval
```

Current compatibility note:

- code and configs still use `task = "ancestor_ranking"` as the stable execution key
- this legacy key no longer means single-positive ranking
- under the frozen protocol, `ancestor_ranking` maps to grouped multi-positive evaluation by default

## 2. Query Unit And Positives

Query unit:

```text
(src, relation)
```

Positive set:

```text
all true ancestors under the same (src, relation) query
```

Current code path:

- task construction: `project_bootstrap/baseline_scaffold/src/relation_tasks.py`
- grouped positive closure with hop tracking:
  - `build_ancestor_task_examples_with_hops(...)`
  - `build_grouped_ranking_queries(...)`
- relation label mapping:
  - `ancestor_label_mode = "source_kind"` yields `extends_ancestor` for class/structure sources and `instance_ancestor` for instance sources
  - `ancestor_label_mode = "single"` yields `ancestor`

## 3. Frozen Config Fields

For grouped ancestor retrieval runs, the relevant config fields are:

- `task`
  - current execution value: `ancestor_ranking`
- `target_relation_types`
  - relation types retained for prediction examples
- `message_relation_types`
  - relation types retained for message passing
- `hierarchy_relation_types`
  - currently expected to include `extends` and `instance_of`
- `ancestor_label_mode`
  - currently `source_kind` or `single`
- `ancestor_min_hops`
  - lower bound on positive ancestor depth
- `class_like_decl_kinds`
  - controls hierarchy candidate pools, currently class-like nodes
- `exclude_held_out_direct_edges`
  - prevents direct held-out edges from leaking into message edges
- `negative_strategy`
- `negative_fallback_strategy`
- `seed`, `val_ratio`, `test_ratio`, `negative_ratio`

Representative config roots already using this structure:

- `project_bootstrap/baseline_scaffold/configs/relation_gcn_typeclass_precise_v2_ancestor_ranking.json`
- `project_bootstrap/baseline_scaffold/configs/relation_hgcn_typeclass_precise_v2_ancestor_ranking.json`

## 4. Frozen Metric Set

The grouped benchmark metric set is:

- `Recall@1`
- `Recall@3`
- `Recall@5`
- `Recall@10`
- `MAP`
- `nDCG`
- `nDCG@10`
- `grouped-MRR`

Hop-bucket breakdowns:

- `hop_2`
- `hop_3`
- `hop_4_plus`

Legacy single-positive `MRR` remains allowed only as:

- historical comparison
- auxiliary diagnostics

It is not a primary benchmark conclusion field.

## 5. Frozen Output Structure

### 5.1 metrics.json

Grouped retrieval metrics are expected under:

```text
ranking.{val,test}.grouped
```

Required grouped keys:

- `num_queries`
- `map`
- `ndcg`
- `ndcg_at_10`
- `grouped_mrr`
- `recall_at_1`
- `recall_at_3`
- `recall_at_5`
- `recall_at_10`
- `hop_buckets`

Current implementation entrypoint:

- `project_bootstrap/baseline_scaffold/src/relation_baseline_common.py`
  - `build_grouped_ranking_metrics(...)`
  - `build_ranking_task_metrics(...)`

### 5.2 result_summary.json

The flattened grouped fields expected by downstream sweep/reporting code are:

- `grouped_test_map`
- `grouped_test_ndcg`
- `grouped_test_ndcg_at_10`
- `grouped_test_mrr`
- `grouped_test_recall_at_1`
- `grouped_test_recall_at_3`
- `grouped_test_recall_at_5`
- `grouped_test_recall_at_10`

Current runner entrypoints producing these fields:

- `project_bootstrap/baseline_scaffold/src/run_relation_gcn_baseline.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_hyperbolic_baseline.py`
- `project_bootstrap/baseline_scaffold/src/run_relation_grouped_retrieval_baseline.py`

Current downstream consumers expecting the same flattened schema:

- `project_bootstrap/baseline_scaffold/src/run_relation_seed_sweep.py`
- `project_bootstrap/baseline_scaffold/src/_patch_sweep_reports.py`

## 6. Current T12 Alignment Result

Reviewed T12 alignment status:

- grouped query construction and grouped metric computation already exist in code
- `metrics.json` already stores `ndcg_at_10`
- legacy runner summaries were not fully uniform before T12
- T12 applies the minimum required summary-field alignment so grouped retrieval runners also expose `grouped_test_ndcg_at_10`

## 7. Non-Goals

T12 does not do the following:

- rename the legacy `ancestor_ranking` execution key across the codebase
- redesign model architecture
- claim that hop-bucket reporting is already universally wired into every formal report surface

That last item remains partly deferred to `T13`.
