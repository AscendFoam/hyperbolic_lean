# T34 Grouped Training Summary

## 1. Scope

This report only summarizes already-reviewed Milestone 3 evidence:

- `T32`: formal GCN grouped 5-seed sweep
- `T33`: formal HGCN grouped 5-seed sweep
- `T30` / `T31A` / `T31`: the reviewed alignment work that defines the grouped training path

It does not add new experiments, does not modify any sweep artifact, and does not reinterpret historical binary runs as if they were directly comparable to the matched `T32` / `T33` protocol.

## 2. Comparability Statement

`T32` and `T33` are directly comparable because they use the same:

- reviewed grouped retrieval runner
- candidate graphs: `Field.Subfield` and `Order.Ring`
- query task: grouped `ancestor_ranking`
- seed list: `[7, 42, 123, 2026, 3407]`
- split ratios: `val_ratio = 0.15`, `test_ratio = 0.15`
- grouped loss: `sampled_softmax`
- negative setting: `negative_ratio = 10.0`
- relation set: `["extends", "instance_of"]`
- dimensional budget: `input_dim = hidden_dim = output_dim = 16`
- optimizer schedule: `lr = 0.01`, `weight_decay = 1e-4`, `epochs = 100`, `eval_every = 5`, `patience = 12`

Therefore, the GCN-vs-HGCN comparison below is protocol-valid inside this matched grouped setting.

Historical binary runs are not directly comparable to `T32` / `T33` in absolute value because the reviewed path also changed training objective alignment and query-level split semantics before the formal sweeps.

## 3. Grouped vs Binary Protocol Diff

| aspect | historical binary path | reviewed grouped path | impact |
| --- | --- | --- | --- |
| training unit | edge `(src, dst, relation)` | query `(src, relation)` | grouped path matches task structure |
| positives per unit | single labeled edge | multi-positive ancestor set | avoids single-positive mismatch |
| loss | `BCEWithLogitsLoss` | sampled-softmax / InfoNCE-family grouped loss | optimizes within-query ranking |
| split semantics | historical edge-level split | query-level disjoint split for `ancestor_ranking` | formal grouped metrics are better defended |
| checkpoint selection | validation AP | validation grouped MAP | model selection matches benchmark |
| primary report surface | AP / AUROC / F1 plus legacy MRR | grouped MAP / nDCG / nDCG@10 / grouped-MRR / Recall@k / hop buckets | grouped path is the reviewed benchmark surface |

## 4. Explicit GCN vs HGCN Config Diff

Review-backed config diff result:

- Shared protocol fields are identical between `T32` and `T33`.
- Identity fields differ as expected: `run_id`, `model_type`, `artifacts_root`.
- The only model-specific additions in `T33` are the HGCN fields below.

| field | T32 GCN | T33 HGCN |
| --- | --- | --- |
| `model_type` | `gcn` | `hgcn` |
| `model_variant` | not present | `relation_hgcn_residual_v3` |
| `distance_signal_mode` | not present | `log1p_running_zscore_tanh` |
| `distance_stat_momentum` | not present | `0.1` |
| `residual_gate_init` | not present | `1.0` |
| `decoder_hidden_dim` | not present | `16` |
| `curvature` | not present | `1.0` |
| `grad_clip_norm` | not present | `1.0` |

Everything else that matters for protocol comparability is held fixed.

## 5. Formal Matched Grouped Results

### 5.1 Primary Metrics

| graph | GCN grouped MAP | HGCN grouped MAP | delta (HGCN - GCN) | GCN grouped nDCG | HGCN grouped nDCG | GCN grouped nDCG@10 | HGCN grouped nDCG@10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `Field.Subfield` | `0.4839 +/- 0.0783` | `0.4458 +/- 0.1150` | `-0.0381` | `0.6428 +/- 0.0653` | `0.6095 +/- 0.0908` | `0.5273 +/- 0.0850` | `0.4765 +/- 0.1128` |
| `Order.Ring` | `0.5789 +/- 0.0346` | `0.5616 +/- 0.0312` | `-0.0173` | `0.7293 +/- 0.0340` | `0.7111 +/- 0.0296` | `0.6129 +/- 0.0506` | `0.5899 +/- 0.0414` |

### 5.2 Interpretation

- `Field.Subfield`: GCN remains ahead on grouped MAP, nDCG, nDCG@10, and Recall@10. HGCN variance is also larger.
- `Order.Ring`: GCN still leads on grouped MAP, nDCG, and nDCG@10. HGCN is slightly higher on grouped MRR (`0.6123` vs `0.6101`), but that does not overturn the main ranking metrics.
- Across both reviewed formal graphs, `T33` does not establish an HGCN overtake under the matched grouped protocol.

## 6. Historical Grouped-vs-Binary Signal

The older phase summary dated `2026-05-02` reported large retrieval gains when moving from binary edge training to grouped retrieval training on earlier sweep bundles:

| graph | model | historical binary gMAP | historical grouped gMAP | historical grouped-vs-binary signal |
| --- | --- | ---: | ---: | --- |
| `Field.Subfield` | GCN | `0.144` | `0.321` | strong improvement |
| `Field.Subfield` | HGCN | `0.104` | `0.299` | strong improvement |
| `Order.Ring` | GCN | `0.208` | `0.291` | clear improvement |
| `Order.Ring` | HGCN | `0.148` | `0.291` | strong improvement |

Those historical numbers remain useful as evidence that binary edge training was a poor fit for grouped retrieval. They should not be read as numerically interchangeable with `T32` / `T33`, because the reviewed path later also fixed query-level split completeness and formalized the matched grouped sweep route.

## 7. Conclusion Buckets

### Accepted

1. The reviewed benchmark surface for Milestone 3 is grouped retrieval, not binary edge classification.
2. `T32` and `T33` are directly comparable inside the matched grouped protocol.
3. Under that matched protocol, GCN remains stronger than HGCN on the primary grouped metrics for both `Field.Subfield` and `Order.Ring`.

### Inconclusive

1. The exact magnitude of grouped-vs-binary improvement from older phase summaries cannot be carried over numerically to `T32` / `T33`.
2. Hop-bucket evidence for hyperbolic benefit remains mixed: `Order.Ring` shows some deeper-hop HGCN signal, but the full-graph grouped metrics still favor GCN.

### Deferred

1. Query-aware negative/candidate sampling beyond the minimal grouped path.
2. Provenance-split conclusions for `explicit-only / synthesized-only / mixed`.
3. Any stronger HGCN claim that would require new tuning or a different model family.

## 8. Bottom Line

Milestone 3 now has a clean reviewed story:

- the project moved from a binary-training mismatch to a reviewed grouped training path
- the formal matched grouped sweeps are now reproducible and comparable
- that cleaned-up comparison still does not show HGCN outperforming GCN overall

So the durable conclusion is not "HGCN wins once the protocol is fixed". The durable conclusion is narrower: fixing the protocol was necessary, and after fixing it, GCN still holds the stronger overall grouped result on the current reviewed candidate graphs.
