# T32 GCN Grouped Training Sweep

> 更新时间：2026-05-17
>
> 范围：本报告只记录 `T32` 在 reviewed grouped retrieval runner / seed sweep path 下完成的 GCN 5-seed grouped training sweep。它不是 HGCN 对照，也不是最终 benchmark 定稿。

## 1. Scope

- Model family: GCN only
- Training path: `run_relation_grouped_retrieval_baseline.py` via `run_relation_seed_sweep.py`
- Grouped loss: `sampled_softmax`
- Seeds: `[7, 42, 123, 2026, 3407]`
- Query protocol: reviewed `ancestor_ranking` grouped multi-positive retrieval
- Query key: `(src_id, relation_type)` inherited from reviewed `T31A` / `T31` path
- Explicit negative sampling setting: `negative_ratio = 10.0` in both formal base configs

HGCN comparison remains `T33`.

## 2. Commands Run

```powershell
& 'C:\ProgramData\anaconda3\envs\DLEnv\python.exe' `
  'project_bootstrap\baseline_scaffold\src\run_relation_seed_sweep.py' `
  --config 'project_bootstrap\baseline_scaffold\configs\grouped_gcn_field_subfield_sweep_t32.json'

& 'C:\ProgramData\anaconda3\envs\DLEnv\python.exe' `
  'project_bootstrap\baseline_scaffold\src\run_relation_seed_sweep.py' `
  --config 'project_bootstrap\baseline_scaffold\configs\grouped_gcn_order_ring_sweep_t32.json'
```

## 3. Configs And Artifacts

| target graph | role in diagnostics | base config | sweep config | output root |
| --- | --- | --- | --- | --- |
| `Mathlib.Algebra.Field.Subfield` | controlled probe | `project_bootstrap/baseline_scaffold/configs/grouped_gcn_field_subfield_anc_t32.json` | `project_bootstrap/baseline_scaffold/configs/grouped_gcn_field_subfield_sweep_t32.json` | `artifacts/baselines/relation_seed_sweeps/grouped_gcn_field_subfield_t32/` |
| `Mathlib.Algebra.Order.Ring` | default follow-up candidate | `project_bootstrap/baseline_scaffold/configs/grouped_gcn_order_ring_anc_t32.json` | `project_bootstrap/baseline_scaffold/configs/grouped_gcn_order_ring_sweep_t32.json` | `artifacts/baselines/relation_seed_sweeps/grouped_gcn_order_ring_t32/` |

Per-target artifact bundle includes:

- `aggregate.json`
- `per_seed_results.csv`
- `per_seed_results.json`
- `report.md`
- one seed subdirectory per successful run

## 4. Aggregate Grouped Metrics

All five seeds succeeded on both graphs; `failed_runs = []`.

| graph | grouped MAP | grouped nDCG | grouped nDCG@10 | grouped MRR | Recall@1 | Recall@3 | Recall@5 | Recall@10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `Field.Subfield` | `0.4839 ± 0.0783` | `0.6428 ± 0.0653` | `0.5273 ± 0.0850` | `0.5043 ± 0.0658` | `0.1573 ± 0.0486` | `0.3841 ± 0.1383` | `0.5076 ± 0.1335` | `0.6422 ± 0.1266` |
| `Order.Ring` | `0.5789 ± 0.0346` | `0.7293 ± 0.0340` | `0.6129 ± 0.0506` | `0.6101 ± 0.0843` | `0.1273 ± 0.0562` | `0.3017 ± 0.0807` | `0.4269 ± 0.0628` | `0.6183 ± 0.0801` |

## 5. Hop-Bucket Aggregate

### 5.1 Field.Subfield

| bucket | MAP | nDCG | grouped MRR | Recall@10 |
| --- | ---: | ---: | ---: | ---: |
| `hop_2` | `0.2865 ± 0.0742` | `0.4618 ± 0.0566` | `0.3018 ± 0.0568` | `0.5722 ± 0.1685` |
| `hop_3` | `0.2331 ± 0.0981` | `0.4299 ± 0.0816` | `0.2320 ± 0.0836` | `0.4076 ± 0.1934` |
| `hop_4_plus` | `0.2669 ± 0.1537` | `0.5016 ± 0.1472` | `0.3181 ± 0.2518` | `0.3505 ± 0.2060` |

### 5.2 Order.Ring

| bucket | MAP | nDCG | grouped MRR | Recall@10 |
| --- | ---: | ---: | ---: | ---: |
| `hop_2` | `0.2281 ± 0.0342` | `0.4295 ± 0.0292` | `0.2497 ± 0.0453` | `0.4817 ± 0.0604` |
| `hop_3` | `0.3021 ± 0.0515` | `0.5200 ± 0.0387` | `0.3477 ± 0.0823` | `0.4618 ± 0.0749` |
| `hop_4_plus` | `0.4481 ± 0.0377` | `0.6697 ± 0.0251` | `0.5061 ± 0.0855` | `0.4600 ± 0.0740` |

Full hop-bucket `Recall@1/3/5/10` tables remain in:

- `artifacts/baselines/relation_seed_sweeps/grouped_gcn_field_subfield_t32/report.md`
- `artifacts/baselines/relation_seed_sweeps/grouped_gcn_order_ring_t32/report.md`

## 6. Execution Notes

1. This run stayed on the reviewed grouped path end to end:
   - grouped seed sweep runner
   - grouped retrieval training runner
   - query-level split semantics from `T31A`
   - grouped val MAP checkpoint selection from `T31`

2. Both formal base configs explicitly set:
   - `grouped_loss = "sampled_softmax"`
   - `negative_ratio = 10.0`
   - `message_relation_types = ["extends", "instance_of"]`

3. Under this reviewed grouped GCN path:
   - `Order.Ring` is stronger on grouped `MAP / nDCG / nDCG@10 / grouped-MRR`, and its seed variance is lower.
   - `Field.Subfield` has higher overall `Recall@10`, but variance is materially larger, which is consistent with its controlled-probe role.

4. These are T32 GCN-only artifacts. HGCN parity or overtake is not established here and remains the scope of `T33`.
