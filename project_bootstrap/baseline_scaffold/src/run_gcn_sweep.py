from __future__ import annotations

import argparse
import copy
import csv
from pathlib import Path

from common import ensure_dir, load_config, write_json
from run_gcn_baseline import run_gcn_experiment


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run low-dim GCN sweeps.")
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


def apply_dim_mode(run_config: dict, dim: int, dim_mode: str) -> None:
    if dim_mode == "tie_all":
        run_config["input_dim"] = dim
        run_config["hidden_dim"] = dim
        run_config["output_dim"] = dim
        return
    if dim_mode == "wide_hidden":
        run_config["input_dim"] = max(dim * 2, 16)
        run_config["hidden_dim"] = max(dim * 2, 16)
        run_config["output_dim"] = dim
        return
    raise ValueError(f"Unsupported dim_mode: {dim_mode}")


def write_summary_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_markdown_table(rows: list[dict]) -> str:
    if not rows:
        return "# gcn sweep\n\nNo successful runs.\n"
    lines = [
        "# gcn sweep",
        "",
        "| rank | run_id | dim | val AP | test AP | test AUROC | calibrated test F1 | threshold | best epoch |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for idx, row in enumerate(rows, start=1):
        lines.append(
            "| "
            + " | ".join(
                [
                    str(idx),
                    str(row["run_id"]),
                    str(row["output_dim"]),
                    f"{row['val_average_precision']:.4f}",
                    f"{row['test_average_precision']:.4f}",
                    f"{row['test_auroc']:.4f}",
                    f"{row['calibrated_test_f1']:.4f}",
                    f"{row['calibrated_threshold']:.4f}",
                    str(row["best_epoch"]),
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

    shared_overrides = sweep_config.get("shared_overrides", {})
    dim_mode = str(sweep_config.get("dim_mode", "tie_all"))
    sort_by = str(sweep_config.get("sort_by", "val_average_precision"))
    successful_rows: list[dict] = []
    failed_rows: list[dict] = []

    for dim in sweep_config["dimensions"]:
        run_config = copy.deepcopy(base_config)
        run_config.update(shared_overrides)
        apply_dim_mode(run_config, int(dim), dim_mode)
        run_config["run_id"] = f"{base_config['run_id']}_dim{dim}"
        run_config["artifacts_root"] = str((output_root / run_config["run_id"]).resolve().relative_to(workspace_root))

        print(f"[sweep] running GCN dim={dim} -> {run_config['artifacts_root']}")
        try:
            result = run_gcn_experiment(run_config)
            successful_rows.append(result["result_summary"])
        except Exception as exc:  # noqa: BLE001
            failed_rows.append(
                {
                    "run_id": run_config["run_id"],
                    "output_dim": int(run_config["output_dim"]),
                    "error": str(exc),
                }
            )
            print(f"[sweep] failed: {run_config['run_id']} -> {exc}")

    successful_rows.sort(key=lambda row: row.get(sort_by, float("-inf")), reverse=True)
    write_summary_csv(output_root / "leaderboard.csv", successful_rows)
    write_json(output_root / "leaderboard.json", {"successful_runs": successful_rows, "failed_runs": failed_rows})
    (output_root / "leaderboard.md").write_text(build_markdown_table(successful_rows), encoding="utf-8")

    print(f"[done] successful runs: {len(successful_rows)}")
    print(f"[done] failed runs: {len(failed_rows)}")
    print(f"[done] sweep artifacts: {output_root}")


if __name__ == "__main__":
    main()
