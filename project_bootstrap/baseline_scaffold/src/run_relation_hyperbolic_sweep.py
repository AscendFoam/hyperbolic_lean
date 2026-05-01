from __future__ import annotations

import argparse
import copy
import csv
from pathlib import Path

from common import ensure_dir, load_config, write_json
from run_relation_hyperbolic_baseline import run_relation_hyperbolic_experiment


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run low-dim / curvature sweeps for relation-aware hyperbolic baselines.")
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


def format_tag(value) -> str:
    text = str(value)
    return text.replace("-", "m").replace(".", "p")


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


def apply_decoder_hidden_mode(
    run_config: dict,
    dim: int,
    decoder_hidden_mode: str,
    min_decoder_hidden_dim: int,
) -> None:
    if decoder_hidden_mode == "keep":
        return
    if decoder_hidden_mode == "tie_output_dim":
        run_config["decoder_hidden_dim"] = max(dim, min_decoder_hidden_dim)
        return
    if decoder_hidden_mode == "double_output_dim":
        run_config["decoder_hidden_dim"] = max(dim * 2, min_decoder_hidden_dim)
        return
    raise ValueError(f"Unsupported decoder_hidden_mode: {decoder_hidden_mode}")


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
        return "# relation-aware hyperbolic sweep\n\nNo successful runs.\n"
    lines = [
        "# relation-aware hyperbolic sweep",
        "",
        "| rank | run_id | variant | dim | curvature | val AP | test AP | test AUROC | calibrated test F1 | best epoch |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for idx, row in enumerate(rows, start=1):
        calibrated_f1 = row.get("calibrated_test_f1")
        calibrated_text = "NA" if calibrated_f1 is None else f"{calibrated_f1:.4f}"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(idx),
                    str(row["run_id"]),
                    str(row["model_variant"]),
                    str(row["output_dim"]),
                    str(row["curvature"]),
                    f"{row['val_average_precision']:.4f}",
                    f"{row['test_average_precision']:.4f}",
                    f"{row['test_auroc']:.4f}",
                    calibrated_text,
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
    per_variant_overrides = sweep_config.get("per_variant_overrides", {})
    dim_mode = str(sweep_config.get("dim_mode", "tie_all"))
    decoder_hidden_mode = str(sweep_config.get("decoder_hidden_mode", "keep"))
    min_decoder_hidden_dim = int(sweep_config.get("min_decoder_hidden_dim", 1))
    sort_by = str(sweep_config.get("sort_by", "val_average_precision"))
    base_run_id = str(sweep_config.get("base_run_id_override", base_config["run_id"]))
    run_id_template = str(sweep_config.get("run_id_template", "{base_run_id}_{run_name}"))

    successful_rows: list[dict] = []
    failed_rows: list[dict] = []

    for variant in sweep_config["model_variants"]:
        for dim in sweep_config["dimensions"]:
            for curvature in sweep_config["curvatures"]:
                run_config = copy.deepcopy(base_config)
                run_config.update(shared_overrides)
                run_config.update(per_variant_overrides.get(variant, {}))
                apply_dim_mode(run_config, int(dim), dim_mode)
                apply_decoder_hidden_mode(
                    run_config,
                    dim=int(dim),
                    decoder_hidden_mode=decoder_hidden_mode,
                    min_decoder_hidden_dim=min_decoder_hidden_dim,
                )
                run_config["model_variant"] = variant
                run_config["curvature"] = float(curvature)

                run_name = (
                    str(sweep_config.get("run_name_template", "{variant}_dim{dim}_c{curvature}"))
                    .replace("{variant}", variant)
                    .replace("{dim}", str(dim))
                    .replace("{curvature}", format_tag(curvature))
                )
                run_config["run_id"] = (
                    run_id_template
                    .replace("{base_run_id}", base_run_id)
                    .replace("{run_name}", run_name)
                    .replace("{variant}", variant)
                    .replace("{dim}", str(dim))
                    .replace("{curvature}", format_tag(curvature))
                )
                run_config["artifacts_root"] = str((output_root / run_config["run_id"]).resolve().relative_to(workspace_root))

                print(
                    f"[relation-sweep] running variant={variant} dim={dim} curvature={curvature} "
                    f"-> {run_config['artifacts_root']}"
                )
                try:
                    result = run_relation_hyperbolic_experiment(run_config)
                    summary = result["result_summary"]
                    successful_rows.append(summary)
                except Exception as exc:  # noqa: BLE001 - sweep should continue on bad points
                    failed_rows.append(
                        {
                            "run_id": run_config["run_id"],
                            "model_variant": variant,
                            "output_dim": int(run_config["output_dim"]),
                            "curvature": float(curvature),
                            "error": str(exc),
                        }
                    )
                    print(f"[relation-sweep] failed: {run_config['run_id']} -> {exc}")

    successful_rows.sort(key=lambda row: row.get(sort_by, float("-inf")), reverse=True)
    write_summary_csv(output_root / "leaderboard.csv", successful_rows)
    write_json(output_root / "leaderboard.json", {"successful_runs": successful_rows, "failed_runs": failed_rows})
    (output_root / "leaderboard.md").write_text(build_markdown_table(successful_rows), encoding="utf-8")

    print(f"[done] successful runs: {len(successful_rows)}")
    print(f"[done] failed runs: {len(failed_rows)}")
    print(f"[done] sweep artifacts: {output_root}")


if __name__ == "__main__":
    main()
