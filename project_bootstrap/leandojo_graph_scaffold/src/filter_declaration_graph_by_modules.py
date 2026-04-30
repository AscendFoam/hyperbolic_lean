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


def matches_module_prefix(module_name: str, prefixes: list[str]) -> bool:
    return any(module_name == prefix or module_name.startswith(prefix + ".") for prefix in prefixes)


def main() -> None:
    parser = argparse.ArgumentParser(description="Filter a declaration graph by module prefixes.")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    graph_root = Path(config["graph_root"])
    output_root = Path(config["output_root"])
    output_root.mkdir(parents=True, exist_ok=True)

    include_module_prefixes = [str(prefix) for prefix in config.get("include_module_prefixes", []) if str(prefix).strip()]
    keep_edge_types = {str(edge_type) for edge_type in config.get("keep_edge_types", []) if str(edge_type).strip()}
    keep_only_internal_edges = bool(config.get("keep_only_internal_edges", True))
    drop_isolated_nodes = bool(config.get("drop_isolated_nodes", True))

    if not include_module_prefixes:
        raise ValueError("include_module_prefixes must be a non-empty list.")

    declarations = read_csv_rows(graph_root / "declarations.csv")
    edges = read_csv_rows(graph_root / "edges.csv")

    kept_declarations = [
        row for row in declarations
        if matches_module_prefix(row.get("module_name", ""), include_module_prefixes)
    ]
    kept_ids = {row["declaration_id"] for row in kept_declarations}

    kept_edges: list[dict] = []
    for row in edges:
        edge_type = row.get("edge_type", "")
        if keep_edge_types and edge_type not in keep_edge_types:
            continue
        src_in = row["src_id"] in kept_ids
        dst_in = row["dst_id"] in kept_ids
        if keep_only_internal_edges:
            if not (src_in and dst_in):
                continue
        else:
            if not (src_in or dst_in):
                continue
        kept_edges.append(row)

    if drop_isolated_nodes:
        covered_ids = {row["src_id"] for row in kept_edges} | {row["dst_id"] for row in kept_edges}
        kept_declarations = [row for row in kept_declarations if row["declaration_id"] in covered_ids]
        kept_ids = {row["declaration_id"] for row in kept_declarations}
        kept_edges = [
            row for row in kept_edges
            if row["src_id"] in kept_ids and row["dst_id"] in kept_ids
        ]
    else:
        covered_ids = {row["src_id"] for row in kept_edges} | {row["dst_id"] for row in kept_edges}

    decl_kind_counts = Counter(row.get("decl_kind", "") for row in kept_declarations)
    edge_type_counts = Counter(row.get("edge_type", "") for row in kept_edges)
    module_counts = Counter(row.get("module_name", "") for row in kept_declarations)
    stats = {
        "graph_root": str(graph_root),
        "output_root": str(output_root),
        "include_module_prefixes": include_module_prefixes,
        "keep_edge_types": sorted(keep_edge_types),
        "keep_only_internal_edges": keep_only_internal_edges,
        "drop_isolated_nodes": drop_isolated_nodes,
        "num_declarations": len(kept_declarations),
        "num_edges": len(kept_edges),
        "covered_node_count": len(covered_ids),
        "decl_kind_counts": dict(sorted(decl_kind_counts.items())),
        "edge_type_counts": dict(sorted(edge_type_counts.items())),
        "top_module_counts": dict(module_counts.most_common(30)),
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
