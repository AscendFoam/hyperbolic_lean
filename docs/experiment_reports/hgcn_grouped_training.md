# T33 HGCN Grouped Training Sweep

## Scope

- Model family: HGCN only
- Training path: `run_relation_grouped_retrieval_baseline.py` via `run_relation_seed_sweep.py`
- Grouped loss: `sampled_softmax`
- Seeds: `[7, 42, 123, 2026, 3407]`
- Query protocol: reviewed grouped `ancestor_ranking`
- Query key: `(src_id, relation_type)`
- Negative sampling: `negative_ratio = 10.0`

## Commands Run

```powershell
C:\ProgramData\anaconda3\envs\DLEnv\python.exe project_bootstrap\baseline_scaffold\src\run_relation_seed_sweep.py --config project_bootstrap\baseline_scaffold\configs\grouped_hgcn_field_subfield_sweep_t33.json
C:\ProgramData\anaconda3\envs\DLEnv\python.exe project_bootstrap\baseline_scaffold\src\run_relation_seed_sweep.py --config project_bootstrap\baseline_scaffold\configs\grouped_hgcn_order_ring_sweep_t33.json
```

## Configs And Artifacts

| graph | base config | sweep config | output root |
| --- | --- | --- | --- |
| `Field.Subfield` | `project_bootstrap/baseline_scaffold/configs/grouped_hgcn_field_subfield_anc_t33.json` | `project_bootstrap/baseline_scaffold/configs/grouped_hgcn_field_subfield_sweep_t33.json` | `artifacts/baselines/relation_seed_sweeps/grouped_hgcn_field_subfield_t33/` |
| `Order.Ring` | `project_bootstrap/baseline_scaffold/configs/grouped_hgcn_order_ring_anc_t33.json` | `project_bootstrap/baseline_scaffold/configs/grouped_hgcn_order_ring_sweep_t33.json` | `artifacts/baselines/relation_seed_sweeps/grouped_hgcn_order_ring_t33/` |

Each sweep bundle includes `aggregate.json`, `per_seed_results.csv`, `per_seed_results.json`, `report.md`, and one seed subdirectory per successful run.

## Aggregate Metrics

All five seeds succeeded on both graphs; `failed_runs = []`.

| graph | grouped MAP | grouped nDCG | grouped nDCG@10 | grouped MRR | Recall@10 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `Field.Subfield` | `0.4458 +/- 0.1150` | `0.6095 +/- 0.0908` | `0.4765 +/- 0.1128` | `0.4704 +/- 0.1345` | `0.5829 +/- 0.0570` |
| `Order.Ring` | `0.5616 +/- 0.0312` | `0.7111 +/- 0.0296` | `0.5899 +/- 0.0414` | `0.6123 +/- 0.0551` | `0.5505 +/- 0.0509` |

## Hop Buckets

### Field.Subfield

| bucket | MAP | nDCG | grouped MRR | Recall@10 |
| --- | ---: | ---: | ---: | ---: |
| `hop_2` | `0.3057 +/- 0.1300` | `0.4731 +/- 0.1046` | `0.3038 +/- 0.1237` | `0.5722 +/- 0.1104` |
| `hop_3` | `0.2886 +/- 0.1036` | `0.4749 +/- 0.0942` | `0.2977 +/- 0.1121` | `0.5604 +/- 0.1531` |
| `hop_4_plus` | `0.3899 +/- 0.2413` | `0.5902 +/- 0.2189` | `0.4254 +/- 0.3377` | `0.4901 +/- 0.2788` |

### Order.Ring

| bucket | MAP | nDCG | grouped MRR | Recall@10 |
| --- | ---: | ---: | ---: | ---: |
| `hop_2` | `0.2283 +/- 0.0306` | `0.4276 +/- 0.0250` | `0.2609 +/- 0.0351` | `0.4313 +/- 0.0856` |
| `hop_3` | `0.3126 +/- 0.0723` | `0.5358 +/- 0.0605` | `0.3989 +/- 0.1097` | `0.4490 +/- 0.0912` |
| `hop_4_plus` | `0.5042 +/- 0.0636` | `0.7030 +/- 0.0545` | `0.5789 +/- 0.1165` | `0.4659 +/- 0.1543` |

## Notes

- This is the HGCN counterpart to T32's GCN sweep, using the same grouped protocol and seed list.
- HGCN did not overtake T32 GCN on either graph under this protocol.
- Full per-seed `Recall@1/3/5/10` tables remain in the artifact bundle `report.md`.
