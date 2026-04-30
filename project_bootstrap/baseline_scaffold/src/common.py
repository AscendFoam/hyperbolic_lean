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


def build_declaration_metadata(declarations: list[dict]) -> tuple[dict[str, dict], dict[str, dict[str, list[str]]]]:
    metadata: dict[str, dict] = {}
    buckets = {
        "same_module": {},
        "same_namespace": {},
        "same_decl_kind": {},
    }
    strategy_to_key = {
        "same_module": "module_name",
        "same_namespace": "namespace",
        "same_decl_kind": "decl_kind",
    }

    for row in declarations:
        node_id = row["declaration_id"]
        metadata[node_id] = {
            "module_name": row.get("module_name", ""),
            "namespace": row.get("namespace", ""),
            "decl_kind": row.get("decl_kind", ""),
        }
        for strategy, key in strategy_to_key.items():
            value = row.get(key, "")
            if not value:
                continue
            buckets[strategy].setdefault(value, []).append(node_id)

    return metadata, buckets


def split_seed_offset(split_name: str) -> int:
    offsets = {
        "train": 101,
        "val": 202,
        "test": 303,
    }
    if split_name not in offsets:
        raise ValueError(f"Unsupported split_name: {split_name}")
    return offsets[split_name]


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
    declarations: list[dict],
    positive_pairs: set[tuple[str, str]],
    num_samples: int,
    seed: int,
    negative_strategy: str = "random",
    negative_fallback_strategy: str = "random",
) -> tuple[list[tuple[str, str]], dict]:
    allowed_strategies = {"random", "same_module", "same_namespace", "same_decl_kind"}
    if negative_strategy not in allowed_strategies:
        raise ValueError(f"Unsupported negative_strategy: {negative_strategy}")
    if negative_fallback_strategy not in allowed_strategies:
        raise ValueError(f"Unsupported negative_fallback_strategy: {negative_fallback_strategy}")

    rng = random.Random(seed)
    negatives: set[tuple[str, str]] = set()
    metadata, buckets = build_declaration_metadata(declarations)
    strategy_usage = {strategy: 0 for strategy in allowed_strategies}

    if len(node_ids) < 2:
        return [], {
            "requested": num_samples,
            "sampled": 0,
            "negative_strategy": negative_strategy,
            "negative_fallback_strategy": negative_fallback_strategy,
            "strategy_usage": strategy_usage,
        }

    strategy_to_key = {
        "same_module": "module_name",
        "same_namespace": "namespace",
        "same_decl_kind": "decl_kind",
    }

    def get_candidate_pool(src_id: str, strategy: str) -> list[str]:
        if strategy == "random":
            return node_ids
        key = strategy_to_key[strategy]
        value = metadata.get(src_id, {}).get(key, "")
        if not value:
            return []
        return buckets[strategy].get(value, [])

    max_attempts = max(1000, num_samples * 20)
    attempts = 0
    while len(negatives) < num_samples and attempts < max_attempts:
        src = rng.choice(node_ids)
        candidate_pool = get_candidate_pool(src, negative_strategy)
        used_strategy = negative_strategy
        if len(candidate_pool) < 2:
            candidate_pool = get_candidate_pool(src, negative_fallback_strategy)
            used_strategy = negative_fallback_strategy
        if len(candidate_pool) < 2:
            attempts += 1
            continue
        dst = rng.choice(candidate_pool)
        attempts += 1
        if src == dst:
            continue
        pair = (src, dst)
        if pair in positive_pairs or pair in negatives:
            continue
        negatives.add(pair)
        strategy_usage[used_strategy] += 1

    return list(negatives), {
        "requested": num_samples,
        "sampled": len(negatives),
        "negative_strategy": negative_strategy,
        "negative_fallback_strategy": negative_fallback_strategy,
        "strategy_usage": strategy_usage,
    }


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
        "config_snapshot": config,
        "graph_summary": graph_summary,
        "dependency_status": dependency_status,
    }


def set_global_random_seed(seed: int, np=None, torch=None) -> dict[str, bool]:
    random.seed(seed)
    status = {
        "python_random": True,
        "numpy": False,
        "torch": False,
    }
    if np is not None:
        np.random.seed(seed)
        status["numpy"] = True
    if torch is not None:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        status["torch"] = True
    return status
