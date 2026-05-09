from __future__ import annotations

import argparse
import copy
import csv
import math
from pathlib import Path

from common import ensure_dir, load_config, write_json
from run_relation_gcn_baseline import run_relation_gcn_experiment
from run_relation_hyperbolic_baseline import run_relation_hyperbolic_experiment
from run_relation_grouped_retrieval_baseline import run_grouped_retrieval_experiment


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run multi-seed sweeps for relation-aware baselines.")
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


def mean_std(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "mean": None, "std": None, "min": None, "max": None}
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return {
        "count": len(values),
        "mean": float(mean),
        "std": float(math.sqrt(variance)),
        "min": float(min(values)),
        "max": float(max(values)),
    }


def write_summary_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def flatten_hop_bucket_metrics(result: dict) -> dict[str, float | int | None]:
    flattened: dict[str, float | int | None] = {}
    hop_buckets = (
        result.get("metrics", {})
        .get("ranking", {})
        .get("test", {})
        .get("grouped", {})
        .get("hop_buckets", {})
    )
    tracked_metric_names = [
        "map",
        "ndcg",
        "grouped_mrr",
        "recall_at_1",
        "recall_at_3",
        "recall_at_5",
        "recall_at_10",
    ]
    for bucket_name in ["hop_2", "hop_3", "hop_4_plus"]:
        bucket_metrics = hop_buckets.get(bucket_name, {})
        for metric_name in tracked_metric_names:
            metric_payload = bucket_metrics.get(metric_name, {})
            flattened[f"{bucket_name}_{metric_name}"] = metric_payload.get("mean")
    return flattened


def build_markdown_report(config: dict, per_seed_rows: list[dict], aggregate: dict) -> str:
    lines = [
        "# Relation Seed Sweep",
        "",
        f"- Model type: {config['model_type']}",
        f"- Base config: {config['base_config']}",
        f"- Seeds: {config['seeds']}",
        "",
        "## Aggregate",
        "",
        "| metric | mean | std | min | max | count |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for metric_name, stats in aggregate["metrics"].items():
        mean = "NA" if stats["mean"] is None else f"{stats['mean']:.4f}"
        std = "NA" if stats["std"] is None else f"{stats['std']:.4f}"
        min_value = "NA" if stats["min"] is None else f"{stats['min']:.4f}"
        max_value = "NA" if stats["max"] is None else f"{stats['max']:.4f}"
        lines.append(
            f"| {metric_name} | {mean} | {std} | {min_value} | {max_value} | {stats['count']} |"
        )
    lines.extend(
        [
            "",
            "## Per Seed",
            "",
            "| seed | run_id | test AP | test AUROC | test F1 | calibrated test F1 | test MRR | grouped MAP | grouped nDCG | grouped MRR | grouped Recall@3 | grouped Recall@10 | hits@10 |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in per_seed_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["seed"]),
                    str(row["run_id"]),
                    "NA" if row["test_average_precision"] is None else f"{row['test_average_precision']:.4f}",
                    "NA" if row["test_auroc"] is None else f"{row['test_auroc']:.4f}",
                    "NA" if row["test_f1"] is None else f"{row['test_f1']:.4f}",
                    "NA" if row["calibrated_test_f1"] is None else f"{row['calibrated_test_f1']:.4f}",
                    "NA" if row["ranking_test_mrr"] is None else f"{row['ranking_test_mrr']:.4f}",
                    "NA" if row.get("grouped_test_map") is None else f"{row['grouped_test_map']:.4f}",
                    "NA" if row.get("grouped_test_ndcg") is None else f"{row['grouped_test_ndcg']:.4f}",
                    "NA" if row.get("grouped_test_mrr") is None else f"{row['grouped_test_mrr']:.4f}",
                    "NA" if row.get("grouped_test_recall_at_3") is None else f"{row['grouped_test_recall_at_3']:.4f}",
                    "NA" if row.get("grouped_test_recall_at_10") is None else f"{row['grouped_test_recall_at_10']:.4f}",
                    "NA" if row["ranking_test_hits_at_10"] is None else f"{row['ranking_test_hits_at_10']:.4f}",
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    sweep_config = load_config(args.config)
    config_dir = args.config.parent
    workspace_root = Path.cwd().resolve()

    base_config_path = Path(sweep_config["base_config"])
    if not base_config_path.is_absolute():
        base_config_path = (config_dir / base_config_path).resolve()
    base_config = load_config(base_config_path)

    output_root = Path(sweep_config["output_root"])
    if not output_root.is_absolute():
        output_root = (workspace_root / output_root).resolve()
    ensure_dir(output_root)

    model_type = str(sweep_config["model_type"]).strip().lower()
    if model_type == "gcn":
        runner = run_relation_gcn_experiment
    elif model_type == "hgcn":
        runner = run_relation_hyperbolic_experiment
    elif model_type in ("grouped_gcn", "grouped_hgcn"):
        runner = run_grouped_retrieval_experiment
    else:
        raise ValueError(f"Unsupported model_type: {model_type}")

    shared_overrides = copy.deepcopy(sweep_config.get("shared_overrides", {}))
    run_name_template = str(sweep_config.get("run_name_template", "{base_run_id}_seed{seed}"))

    per_seed_rows: list[dict] = []
    failed_rows: list[dict] = []

    for seed in sweep_config["seeds"]:
        seed = int(seed)
        run_config = copy.deepcopy(base_config)
        run_config.update(shared_overrides)
        run_config["seed"] = seed
        run_config["run_id"] = (
            run_name_template
            .replace("{base_run_id}", str(base_config["run_id"]))
            .replace("{seed}", str(seed))
        )
        run_config["artifacts_root"] = str((output_root / run_config["run_id"]).resolve().relative_to(workspace_root))

        print(f"[seed-sweep] running seed={seed} -> {run_config['artifacts_root']}")
        try:
            result = runner(run_config)
            summary = copy.deepcopy(result["result_summary"])
            summary["seed"] = seed
            summary.update(flatten_hop_bucket_metrics(result))
            per_seed_rows.append(summary)
        except Exception as exc:  # noqa: BLE001
            failed_rows.append({"seed": seed, "error": str(exc), "run_id": run_config["run_id"]})
            print(f"[seed-sweep] failed seed={seed}: {exc}")

    metric_names = [
        "test_average_precision",
        "test_auroc",
        "test_f1",
        "calibrated_test_f1",
        "ranking_test_mrr",
        "ranking_test_hits_at_1",
        "ranking_test_hits_at_10",
        "grouped_test_map",
        "grouped_test_ndcg",
        "grouped_test_ndcg_at_10",
        "grouped_test_mrr",
        "grouped_test_recall_at_1",
        "grouped_test_recall_at_3",
        "grouped_test_recall_at_5",
        "grouped_test_recall_at_10",
        "hop_2_map",
        "hop_2_ndcg",
        "hop_2_grouped_mrr",
        "hop_2_recall_at_1",
        "hop_2_recall_at_3",
        "hop_2_recall_at_5",
        "hop_2_recall_at_10",
        "hop_3_map",
        "hop_3_ndcg",
        "hop_3_grouped_mrr",
        "hop_3_recall_at_1",
        "hop_3_recall_at_3",
        "hop_3_recall_at_5",
        "hop_3_recall_at_10",
        "hop_4_plus_map",
        "hop_4_plus_ndcg",
        "hop_4_plus_grouped_mrr",
        "hop_4_plus_recall_at_1",
        "hop_4_plus_recall_at_3",
        "hop_4_plus_recall_at_5",
        "hop_4_plus_recall_at_10",
        "val_average_precision",
        "val_auroc",
    ]
    aggregate = {
        "model_type": model_type,
        "base_run_id": base_config["run_id"],
        "successful_seeds": [row["seed"] for row in per_seed_rows],
        "failed_runs": failed_rows,
        "metrics": {},
    }
    for metric_name in metric_names:
        values = [
            float(row[metric_name])
            for row in per_seed_rows
            if row.get(metric_name) is not None
        ]
        aggregate["metrics"][metric_name] = mean_std(values)

    per_seed_rows.sort(key=lambda row: int(row["seed"]))
    write_summary_csv(output_root / "per_seed_results.csv", per_seed_rows)
    write_json(output_root / "per_seed_results.json", {"successful_runs": per_seed_rows, "failed_runs": failed_rows})
    write_json(output_root / "aggregate.json", aggregate)
    (output_root / "report.md").write_text(build_markdown_report(sweep_config, per_seed_rows, aggregate), encoding="utf-8")

    print(f"[done] successful seeds: {len(per_seed_rows)}")
    print(f"[done] failed seeds: {len(failed_rows)}")
    print(f"[done] output: {output_root}")


if __name__ == "__main__":
    main()
