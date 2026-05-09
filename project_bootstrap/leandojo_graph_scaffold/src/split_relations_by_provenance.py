"""Split a declaration graph's edges by provenance (explicit / synthesized / unknown).

Annotates each edge with an ``edge_origin`` dimension independent of ``edge_type``,
then produces split sub-graphs filtered by origin.

Typical usage:
    python split_relations_by_provenance.py --config configs/relation_split_batteries_v1.json
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


# ---------------------------------------------------------------------------
# core logic
# ---------------------------------------------------------------------------

EDGE_CSV_FIELDS = [
    "edge_id", "src_id", "dst_id", "edge_type",
    "evidence_source", "weight", "is_direct", "source_commit", "edge_origin",
]

DECL_CSV_FIELDS = None  # filled from source header


def annotate_edges(edges: list[dict], origin_map: dict[str, str]) -> list[dict]:
    for row in edges:
        row["edge_origin"] = origin_map.get(row["edge_type"], "unknown")
    return edges


def split_edges_by_origin(
    edges: list[dict],
    splits: dict[str, list[str]],
) -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = {}
    for split_name, origins in splits.items():
        origin_set = set(origins)
        result[split_name] = [row for row in edges if row["edge_origin"] in origin_set]
    return result


def filter_declarations(
    declarations: list[dict],
    edges: list[dict],
) -> list[dict]:
    covered = {row["src_id"] for row in edges} | {row["dst_id"] for row in edges}
    return [row for row in declarations if row["declaration_id"] in covered]


def process_source(
    source: dict,
    output_root: Path,
    origin_map: dict[str, str],
    splits: dict[str, list[str]],
) -> dict:
    graph_root = Path(source["graph_root"])
    name = source["name"]

    declarations = read_csv_rows(graph_root / "declarations.csv")
    global DECL_CSV_FIELDS
    DECL_CSV_FIELDS = list(declarations[0].keys())

    edges = read_csv_rows(graph_root / "edges.csv")
    annotate_edges(edges, origin_map)

    origin_counts = Counter(row["edge_origin"] for row in edges)
    edge_type_counts = Counter(row["edge_type"] for row in edges)

    results: dict[str, dict] = {}

    for split_name, split_edges in split_edges_by_origin(edges, splits).items():
        split_decls = filter_declarations(declarations, split_edges)

        out_dir = output_root / f"{name}_{split_name}"
        out_dir.mkdir(parents=True, exist_ok=True)

        write_csv(out_dir / "edges.csv", split_edges, EDGE_CSV_FIELDS)
        write_csv(out_dir / "declarations.csv", split_decls, DECL_CSV_FIELDS)

        split_edge_type_counts = Counter(row["edge_type"] for row in split_edges)
        split_origin_counts = Counter(row["edge_origin"] for row in split_edges)
        split_decl_kind_counts = Counter(row.get("decl_kind", "") for row in split_decls)

        stats = {
            "source_name": name,
            "split": split_name,
            "num_nodes": len(split_decls),
            "num_edges": len(split_edges),
            "edge_type_counts": dict(sorted(split_edge_type_counts.items())),
            "edge_origin_counts": dict(sorted(split_origin_counts.items())),
            "decl_kind_counts": dict(sorted(split_decl_kind_counts.items())),
            "output_dir": str(out_dir),
        }
        (out_dir / "stats.json").write_text(
            json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        results[split_name] = stats

        print(
            f"  {split_name:25s}  nodes={len(split_decls):>6d}  "
            f"edges={len(split_edges):>6d}  "
            f"types={dict(split_edge_type_counts)}"
        )

    source_stats = {
        "source_name": name,
        "source_graph_root": str(graph_root),
        "origin_map": origin_map,
        "source_total_nodes": len(declarations),
        "source_total_edges": len(edges),
        "source_edge_type_counts": dict(sorted(edge_type_counts.items())),
        "source_edge_origin_counts": dict(sorted(origin_counts.items())),
        "splits": results,
    }
    return source_stats


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split declaration graph edges by provenance origin."
    )
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    output_root = Path(config["output_root"])
    output_root.mkdir(parents=True, exist_ok=True)
    origin_map = config["origin_map"]
    splits = config["splits"]

    all_stats: list[dict] = []
    for source in config["source_graphs"]:
        print(f"\nProcessing: {source['name']}")
        stats = process_source(source, output_root, origin_map, splits)
        all_stats.append(stats)

    summary = {
        "config": str(args.config),
        "origin_map": origin_map,
        "split_names": list(splits.keys()),
        "sources": all_stats,
    }
    summary_path = output_root / "relation_split_summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nSummary written to: {summary_path}")


if __name__ == "__main__":
    main()
