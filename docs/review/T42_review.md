# Review: T42

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

### N1. Report does not disclose that FS hop_4_plus mean is computed over 4 of 5 seeds

The report's Section 6.3 gives Field.Subfield explicit_only hop bucket means: GCN hop_4_plus MAP = 0.2774, HGCN hop_4_plus MAP = 0.5245. These values are correct but are computed over only 4 seeds — seed 2026 has null hop_4_plus for both GCN and HGCN (the split/query-level assignment for seed 2026 apparently produces no hop_4_plus queries in the FS explicit_only graph). The Order.Ring hop_4_plus means are computed over all 5 seeds.

**Assessment**: The reported means are numerically correct given the available data. The missing seed is symmetric (both models miss the same seed), so the comparison remains valid. However, the report should have noted that the FS hop_4_plus means are computed over 4 seeds, not 5, to avoid misleading readers into thinking all hop buckets have equal sample sizes. Low severity — the conclusion (HGCN advantage grows with hop depth) is supported by both candidates.

### N2. GCN FS synthesized_only per-seed MAP values are not all exactly 1.0

The report's Section 7.1 states "GCN achieves perfect scores on this trivial task" and the aggregate shows MAP mean = 1.0000, std = 0.0000. However, the per-seed data shows seed 123 has MAP = 0.8100 and seed 2026 has MAP = 0.9029, not 1.0000. The aggregate computation appears to have used the per-seed metrics.json rather than the per_seed_results.json values, or there is a discrepancy in which metric field was aggregated.

**Assessment**: This is a minor data reporting inconsistency. The aggregate.json shows mean=1.0000, std=0.0000 for grouped_test_map, but the per_seed_results.csv shows seeds 123 and 2026 with MAP < 1.0. This suggests either: (a) the aggregate used a different metric field (e.g., the training-side eval rather than test-side), or (b) the per_seed_results CSV is from a different run. The conclusion remains valid — GCN dominates HGCN on synthesized_only. However, claiming "perfect 1.0000" when per-seed values are not all 1.0 is a factual precision issue. T43 should clarify this discrepancy if it uses the synthesized_only data.

### N3. `.claude/settings.json` modified again

`.claude/settings.json` appears in the diff with permission-related changes. This is the same pattern observed in T14, T31, and other tasks — an automatic tool artifact, not an intentional worker change.

**Assessment**: Rejected/excluded from commit per established precedent. This file is not in T42's Allowed Files.

### N4. R04 upgraded to "Mitigated" may be overstated

The risks document upgraded R04 ("relation layer 过浅，双曲价值不足") from Active to Mitigated, citing T42 explicit_only results. The mitigation text correctly notes the conditional nature ("仅在去除 synthesized 边后出现"). However, "Mitigated" in the project's risk taxonomy means "the risk has been substantially addressed," and R04's original scope was about the overall relation layer — not a specific provenance subset.

**Assessment**: The upgrade is defensible because the mitigation text explicitly qualifies the condition. But the risk title "relation layer 过浅" is about the full relation layer, and on the full graph (hierarchy_mixed), the conclusion is still "GCN ahead." A more precise status might be "Partially Mitigated." This is a classification judgment call and does not affect the validity of T42's experimental work. T43 should decide whether to refine the risk status further.

## Missing Tests

None required. T42 is a sweep execution and analysis task. Both verification commands from the task package pass:

1. `rg -n "explicit_only|synthesized_only|hierarchy_mixed|GCN|HGCN|mean|std|Recall|MAP|nDCG|controlled diagnostic|reproducibility" docs\experiment_reports\provenance_seed_sweeps.md` — 91 keyword occurrences, all required terms present.

2. `rg -n "explicit_only|synthesized_only|hierarchy_mixed" artifacts\baselines\relation_seed_sweeps\**\report.md` — all 12 sweep report.md files contain the correct provenance split names in their config paths and per-seed tables.

Independent verification confirms:

1. **Sweep completion**: All 12 sweep directories exist, each with 5 seed subdirectories, aggregate.json, per_seed_results.json, per_seed_results.csv, and report.md. Zero failed runs across all 60 training runs.

2. **Config correctness**: Base configs correctly point to provenance split graph directories (e.g., `mathlib_field_subfield_v1_explicit_only`). All use `grouped_loss = sampled_softmax`, `negative_ratio = 10.0`, 16-dim embeddings, and seeds [7, 42, 123, 2026, 3407]. HGCN configs use the same `relation_hgcn_residual_v3` architecture as T33.

3. **Primary finding verified**: HGCN MAP - GCN MAP on explicit_only is +0.1247 (FS) and +0.0557 (OR), matching the report exactly.

4. **Reproducibility check verified**: All four hierarchy_mixed sweep results are numerically identical to T32/T33 aggregate values (MAP, nDCG, nDCG@10 mean and std all match to 4 decimal places).

5. **Controlled diagnostic verified**: GCN FS synthesized_only aggregate MAP = 1.0000; HGCN FS synthesized_only MAP = 0.6857. GCN OR synthesized_only MAP = 0.8453; HGCN OR = 0.7560.

6. **Hop bucket data verified**: FS and OR hop bucket means match the report. FS hop_4_plus computed over 4 seeds (seed 2026 null); OR hop_4_plus over all 5 seeds.

7. **Historical artifacts untouched**: T32 and T33 sweep directories remain intact with their original structure.

8. **No T40/T41 semantics modified**: No provenance split directories, configs, or protocol documents were changed.

9. **No source code modified**: Only data artifacts, configs, and documentation were changed.

## Suspicious Implementation Details

None found. Specific checks:

1. **No fake execution**: All 60 runs produced real per-seed directories with metrics.json, result_summary.json, and training_stats.json. The per-seed metric values vary naturally across seeds (e.g., FS GCN explicit_only MAP ranges from 0.3435 to 0.7956), which is inconsistent with mock/hardcode behavior.

2. **No data manipulation**: The hierarchy_mixed results are numerically identical to T32/T33, which is strong evidence that the sweep runner was used correctly and the provenance split data is genuine.

3. **No over-engineering**: The report covers exactly the three-way provenance comparison specified in the task package (primary/diagnostic/reproducibility). No speculative extensions.

4. **No proxy-as-theorem**: The report correctly frames results as "HGCN advantage is conditional on provenance composition" rather than claiming universal superiority.

5. **Correct provenance hierarchy respected**: explicit_only as primary, synthesized_only as controlled diagnostic, hierarchy_mixed as reproducibility check — all three roles clearly stated and correctly handled in the report.

6. **Variance is honest**: FS GCN explicit_only MAP std = 0.0800 (high variance across seeds) is reported without suppression, consistent with the small graph size. The report does not cherry-pick favorable seeds.

## Recommended Next Action

Captain should mark T42 as complete and advance to T43. T43 worker must:

1. Synthesize T41 structural diagnostics with T42 experimental results to give a unified answer to "does synthesized relation dilute hyperbolic advantage?"

2. The answer is now clearly **yes** at the structural level (T41: synthesized edges are flat, longest chain = 1) and at the empirical level (T42: HGCN wins only on explicit_only, loses on hierarchy_mixed and synthesized_only).

3. Formally update R04 and related risks to reflect the conditional nature of HGCN advantage — it is real but only on the explicit hierarchy layer.

4. Consider whether the Milestone 3 conclusion ("GCN overall ahead") should be refined to "GCN ahead on mixed graphs; HGCN ahead on explicit-only hierarchy" for the paper narrative.

5. Address N2's aggregate vs per-seed discrepancy for synthesized_only GCN MAP before any external publication.

6. Ensure the paper narrative treats this as a nuanced finding (provenance-conditional advantage) rather than a simple "HGCN beats GCN" claim.
