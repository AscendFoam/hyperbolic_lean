"""Patch existing sweep results with missing hits_at_k and regenerate all reports."""
import json
import csv
import math
import copy
from pathlib import Path


def mean_std(values):
    if not values:
        return {"count": 0, "mean": None, "std": None, "min": None, "max": None}
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return {
        "count": len(values),
        "mean": float(mean),
        "std": float(math.sqrt(variance)),
        "min": float(min(values)),
        "max": float(max(values)),
    }


def flatten_hop_bucket_metrics(metrics):
    flattened = {}
    hop_buckets = (
        metrics.get("ranking", {}).get("test", {}).get("grouped", {}).get("hop_buckets", {})
    )
    for bucket_name in ["hop_2", "hop_3", "hop_4_plus"]:
        bucket_metrics = hop_buckets.get(bucket_name, {})
        for metric_name in [
            "map", "ndcg", "grouped_mrr", "recall_at_1",
            "recall_at_3", "recall_at_5", "recall_at_10",
        ]:
            flattened[f"{bucket_name}_{metric_name}"] = bucket_metrics.get(metric_name, {}).get("mean")
    return flattened


def build_report(sweep_config, per_seed_rows, aggregate):
    lines = [
        "# Relation Seed Sweep", "",
        f"- Model type: {sweep_config['model_type']}",
        f"- Base config: {sweep_config['base_config']}",
        f"- Seeds: {sweep_config['seeds']}", "",
        "## Aggregate", "",
        "| metric | mean | std | min | max | count |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for metric_name, stats in aggregate["metrics"].items():
        mean = "NA" if stats["mean"] is None else f"{stats['mean']:.4f}"
        std = "NA" if stats["std"] is None else f"{stats['std']:.4f}"
        min_v = "NA" if stats["min"] is None else f"{stats['min']:.4f}"
        max_v = "NA" if stats["max"] is None else f"{stats['max']:.4f}"
        lines.append(f"| {metric_name} | {mean} | {std} | {min_v} | {max_v} | {stats['count']} |")
    lines.extend([
        "", "## Per Seed", "",
        "| seed | run_id | test AP | test AUROC | test F1 | calibrated test F1 | test MRR | grouped MAP | grouped nDCG | grouped MRR | grouped Recall@3 | grouped Recall@10 | hits@10 |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for row in per_seed_rows:
        lines.append(
            "| " + " | ".join([
                str(row.get("seed", "?")),
                str(row.get("run_id", "?")),
                "NA" if row.get("test_average_precision") is None else f"{row['test_average_precision']:.4f}",
                "NA" if row.get("test_auroc") is None else f"{row['test_auroc']:.4f}",
                "NA" if row.get("test_f1") is None else f"{row['test_f1']:.4f}",
                "NA" if row.get("calibrated_test_f1") is None else f"{row['calibrated_test_f1']:.4f}",
                "NA" if row.get("ranking_test_mrr") is None else f"{row['ranking_test_mrr']:.4f}",
                "NA" if row.get("grouped_test_map") is None else f"{row['grouped_test_map']:.4f}",
                "NA" if row.get("grouped_test_ndcg") is None else f"{row['grouped_test_ndcg']:.4f}",
                "NA" if row.get("grouped_test_mrr") is None else f"{row['grouped_test_mrr']:.4f}",
                "NA" if row.get("grouped_test_recall_at_3") is None else f"{row['grouped_test_recall_at_3']:.4f}",
                "NA" if row.get("grouped_test_recall_at_10") is None else f"{row['grouped_test_recall_at_10']:.4f}",
                "NA" if row.get("ranking_test_hits_at_10") is None else f"{row['ranking_test_hits_at_10']:.4f}",
            ]) + " |"
        )
    return "\n".join(lines) + "\n"


SWEEPS = {
    "grouped_gcn_field_subfield_v1": {
        "model_type": "grouped_gcn",
        "base_config": "grouped_gcn_field_subfield_anc_v1.json",
        "seeds": [7, 42, 123, 2026, 3407],
    },
    "grouped_hgcn_field_subfield_v1": {
        "model_type": "grouped_hgcn",
        "base_config": "grouped_hgcn_field_subfield_anc_v1.json",
        "seeds": [7, 42, 123, 2026, 3407],
    },
    "grouped_gcn_order_ring_v1": {
        "model_type": "grouped_gcn",
        "base_config": "grouped_gcn_order_ring_anc_v1.json",
        "seeds": [7, 42, 123, 2026, 3407],
    },
    "grouped_hgcn_order_ring_v1": {
        "model_type": "grouped_hgcn",
        "base_config": "grouped_hgcn_order_ring_anc_v1.json",
        "seeds": [7, 42, 123, 2026, 3407],
    },
}

METRIC_NAMES = [
    "test_average_precision", "test_auroc", "test_f1", "calibrated_test_f1",
    "ranking_test_mrr", "ranking_test_hits_at_1", "ranking_test_hits_at_10",
    "grouped_test_map", "grouped_test_ndcg", "grouped_test_ndcg_at_10",
    "grouped_test_mrr", "grouped_test_recall_at_1", "grouped_test_recall_at_3",
    "grouped_test_recall_at_5", "grouped_test_recall_at_10",
    "hop_2_map", "hop_2_ndcg", "hop_2_grouped_mrr", "hop_2_recall_at_1",
    "hop_2_recall_at_3", "hop_2_recall_at_5", "hop_2_recall_at_10",
    "hop_3_map", "hop_3_ndcg", "hop_3_grouped_mrr", "hop_3_recall_at_1",
    "hop_3_recall_at_3", "hop_3_recall_at_5", "hop_3_recall_at_10",
    "hop_4_plus_map", "hop_4_plus_ndcg", "hop_4_plus_grouped_mrr",
    "hop_4_plus_recall_at_1", "hop_4_plus_recall_at_3",
    "hop_4_plus_recall_at_5", "hop_4_plus_recall_at_10",
    "val_average_precision", "val_auroc",
]


def process_sweep(sweep_name, sweep_config):
    sweep_dir = Path(f"artifacts/baselines/relation_seed_sweeps/{sweep_name}")
    if not sweep_dir.exists():
        print(f"  SKIP {sweep_name}: directory not found")
        return

    per_seed_rows = []
    for seed_dir in sorted(sweep_dir.iterdir()):
        if not seed_dir.is_dir():
            continue
        rs_path = seed_dir / "result_summary.json"
        metrics_path = seed_dir / "metrics.json"
        if not rs_path.exists() or not metrics_path.exists():
            continue
        with open(rs_path) as f:
            rs = json.load(f)
        with open(metrics_path) as f:
            metrics = json.load(f)

        # Patch missing keys
        ranking_test = metrics.get("ranking", {}).get("test", {})
        patched = False
        if "ranking_test_hits_at_1" not in rs:
            rs["ranking_test_hits_at_1"] = ranking_test.get("hits_at_1")
            rs["ranking_test_hits_at_10"] = ranking_test.get("hits_at_10")
            patched = True
            with open(rs_path, "w") as f:
                json.dump(rs, f, indent=2, ensure_ascii=False)
        if patched:
            print(f"  Patched {seed_dir.name}")

        row = copy.deepcopy(rs)
        row.update(flatten_hop_bucket_metrics(metrics))
        per_seed_rows.append(row)

    if not per_seed_rows:
        print(f"  SKIP {sweep_name}: no seed data")
        return

    # Aggregate
    model_type = per_seed_rows[0].get("model_type", "unknown")
    aggregate = {
        "model_type": model_type,
        "base_run_id": per_seed_rows[0].get("run_id", "").rsplit("_seed", 1)[0],
        "successful_seeds": [
            row.get("seed", row.get("run_id", "").rsplit("seed", 1)[-1])
            for row in per_seed_rows
        ],
        "failed_runs": [],
        "metrics": {},
    }
    for mn in METRIC_NAMES:
        values = [float(row[mn]) for row in per_seed_rows if row.get(mn) is not None]
        aggregate["metrics"][mn] = mean_std(values)

    per_seed_rows.sort(key=lambda row: str(row.get("seed", row.get("run_id", ""))))

    # Write outputs
    with open(sweep_dir / "aggregate.json", "w") as f:
        json.dump(aggregate, f, indent=2, ensure_ascii=False)
    with open(sweep_dir / "per_seed_results.json", "w") as f:
        json.dump({"successful_runs": per_seed_rows, "failed_runs": []}, f, indent=2, ensure_ascii=False)
    fieldnames = list(per_seed_rows[0].keys())
    with open(sweep_dir / "per_seed_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(per_seed_rows)
    (sweep_dir / "report.md").write_text(
        build_report(sweep_config, per_seed_rows, aggregate), encoding="utf-8"
    )
    print(f"  {len(per_seed_rows)} seeds -> report.md generated")


if __name__ == "__main__":
    for name, cfg in SWEEPS.items():
        print(f"=== {name} ===")
        process_sweep(name, cfg)
