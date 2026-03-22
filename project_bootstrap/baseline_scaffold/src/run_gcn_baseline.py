from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from common import (
    build_run_manifest,
    ensure_dir,
    load_config,
    load_declaration_graph,
    sample_negative_edges,
    split_edges,
    summarize_graph,
    write_edge_split_csv,
    write_json,
)


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GCN baseline scaffold.")
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    graph_root = Path(config["graph_root"])
    artifacts_root = Path(config["artifacts_root"])
    ensure_dir(artifacts_root)

    declarations, edges = load_declaration_graph(graph_root)
    graph_summary = summarize_graph(declarations, edges)

    split = split_edges(
        edges=edges,
        val_ratio=float(config["val_ratio"]),
        test_ratio=float(config["test_ratio"]),
        seed=int(config["seed"]),
    )

    node_ids = [row["declaration_id"] for row in declarations]
    positive_pairs = set(split["train"] + split["val"] + split["test"])
    negative_ratio = float(config.get("negative_ratio", 1.0))

    for split_name, positive_edges in split.items():
        negatives = sample_negative_edges(
            node_ids=node_ids,
            positive_pairs=positive_pairs,
            num_samples=int(len(positive_edges) * negative_ratio),
            seed=int(config["seed"]) + hash(split_name) % 10000,
        )
        write_edge_split_csv(
            path=artifacts_root / f"{split_name}_edges.csv",
            split_name=split_name,
            positives=positive_edges,
            negatives=negatives,
        )

    dependency_status = {
        "torch": has_module("torch"),
        "torch_geometric": has_module("torch_geometric"),
        "numpy": has_module("numpy"),
    }
    manifest = build_run_manifest(config, graph_summary, dependency_status)
    write_json(artifacts_root / "run_manifest.json", manifest)

    if config.get("dry_run", False) or not all(dependency_status.values()):
        notes = {
            "mode": "dry_run",
            "message": (
                "GCN scaffold completed data validation and split generation. "
                "Install torch/torch_geometric/numpy and add a concrete training loop to continue."
            ),
        }
        write_json(artifacts_root / "gcn_dry_run_summary.json", notes)
        print("[done] dry-run completed")
        print(f"[done] artifacts: {artifacts_root}")
        return

    raise NotImplementedError(
        "Training loop is intentionally left as the next step. "
        "The scaffold has already prepared graph splits and manifests."
    )


if __name__ == "__main__":
    main()
