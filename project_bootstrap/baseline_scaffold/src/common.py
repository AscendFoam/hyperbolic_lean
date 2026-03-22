from __future__ import annotations

import csv
import json
import random
from pathlib import Path
from typing import Iterable


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_declaration_graph(graph_root: Path) -> tuple[list[dict], list[dict]]:
    declarations_path = graph_root / "declarations.csv"
    edges_path = graph_root / "edges.csv"
    if not declarations_path.exists() or not edges_path.exists():
        raise FileNotFoundError(
            "Expected declaration graph files were not found. "
            f"Need: {declarations_path} and {edges_path}. "
            "Run normalize_leandojo_trace.py + extract_decl_graph.py first."
        )
    declarations = read_csv_rows(declarations_path)
    edges = read_csv_rows(edges_path)
    return declarations, edges


def summarize_graph(declarations: list[dict], edges: list[dict]) -> dict:
    node_ids = {row["declaration_id"] for row in declarations}
    src_ids = [row["src_id"] for row in edges]
    dst_ids = [row["dst_id"] for row in edges]
    covered_nodes = set(src_ids) | set(dst_ids)
    return {
        "num_declarations": len(declarations),
        "num_edges": len(edges),
        "num_covered_nodes": len(covered_nodes),
        "isolated_node_count": len(node_ids - covered_nodes),
        "decl_kind_counts": count_by_key(declarations, "decl_kind"),
        "edge_type_counts": count_by_key(edges, "edge_type"),
    }


def count_by_key(rows: Iterable[dict], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = row.get(key, "")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def unique_edge_pairs(edges: list[dict]) -> list[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    pairs: list[tuple[str, str]] = []
    for row in edges:
        pair = (row["src_id"], row["dst_id"])
        if pair in seen:
            continue
        seen.add(pair)
        pairs.append(pair)
    return pairs


def split_edges(
    edges: list[dict],
    val_ratio: float,
    test_ratio: float,
    seed: int,
) -> dict[str, list[tuple[str, str]]]:
    pairs = unique_edge_pairs(edges)
    rng = random.Random(seed)
    rng.shuffle(pairs)

    n_total = len(pairs)
    n_val = int(n_total * val_ratio)
    n_test = int(n_total * test_ratio)
    n_train = max(0, n_total - n_val - n_test)

    train = pairs[:n_train]
    val = pairs[n_train:n_train + n_val]
    test = pairs[n_train + n_val:n_train + n_val + n_test]
    return {"train": train, "val": val, "test": test}


def sample_negative_edges(
    node_ids: list[str],
    positive_pairs: set[tuple[str, str]],
    num_samples: int,
    seed: int,
) -> list[tuple[str, str]]:
    rng = random.Random(seed)
    negatives: set[tuple[str, str]] = set()
    if len(node_ids) < 2:
        return []
    max_attempts = max(1000, num_samples * 20)
    attempts = 0
    while len(negatives) < num_samples and attempts < max_attempts:
        src = rng.choice(node_ids)
        dst = rng.choice(node_ids)
        attempts += 1
        if src == dst:
            continue
        pair = (src, dst)
        if pair in positive_pairs or pair in negatives:
            continue
        negatives.add(pair)
    return list(negatives)


def write_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def write_edge_split_csv(path: Path, split_name: str, positives: list[tuple[str, str]], negatives: list[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["split", "src_id", "dst_id", "label"])
        for src, dst in positives:
            writer.writerow([split_name, src, dst, 1])
        for src, dst in negatives:
            writer.writerow([split_name, src, dst, 0])


def build_run_manifest(config: dict, graph_summary: dict, dependency_status: dict) -> dict:
    return {
        "run_id": config["run_id"],
        "task": config["task"],
        "graph_root": config["graph_root"],
        "artifacts_root": config["artifacts_root"],
        "seed": config["seed"],
        "dry_run": config.get("dry_run", False),
        "graph_summary": graph_summary,
        "dependency_status": dependency_status,
    }
