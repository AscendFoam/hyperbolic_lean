from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Filter a declaration graph by edge types.")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    graph_root = Path(config["graph_root"])
    output_root = Path(config["output_root"])
    output_root.mkdir(parents=True, exist_ok=True)

    keep_edge_types = set(config["keep_edge_types"])
    drop_isolated_nodes = bool(config.get("drop_isolated_nodes", False))

    declarations = read_csv_rows(graph_root / "declarations.csv")
    edges = read_csv_rows(graph_root / "edges.csv")

    kept_edges = [row for row in edges if row.get("edge_type", "") in keep_edge_types]
    covered_ids = {row["src_id"] for row in kept_edges} | {row["dst_id"] for row in kept_edges}
    if drop_isolated_nodes:
        kept_declarations = [row for row in declarations if row["declaration_id"] in covered_ids]
    else:
        kept_declarations = declarations

    decl_kind_counts = Counter(row.get("decl_kind", "") for row in kept_declarations)
    edge_type_counts = Counter(row.get("edge_type", "") for row in kept_edges)
    stats = {
        "graph_root": str(graph_root),
        "output_root": str(output_root),
        "keep_edge_types": sorted(keep_edge_types),
        "drop_isolated_nodes": drop_isolated_nodes,
        "num_declarations": len(kept_declarations),
        "num_edges": len(kept_edges),
        "decl_kind_counts": dict(sorted(decl_kind_counts.items())),
        "edge_type_counts": dict(sorted(edge_type_counts.items())),
        "covered_node_count": len(covered_ids),
        "isolated_node_count": len(kept_declarations) - len(covered_ids.intersection({row["declaration_id"] for row in kept_declarations})),
    }

    decl_fields = list(kept_declarations[0].keys()) if kept_declarations else list(declarations[0].keys())
    edge_fields = list(kept_edges[0].keys()) if kept_edges else list(edges[0].keys())
    write_csv(output_root / "declarations.csv", kept_declarations, decl_fields)
    write_csv(output_root / "edges.csv", kept_edges, edge_fields)
    (output_root / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[done] declarations: {len(kept_declarations)}")
    print(f"[done] edges: {len(kept_edges)}")
    print(f"[done] output: {output_root}")


if __name__ == "__main__":
    main()
