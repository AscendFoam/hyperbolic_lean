from __future__ import annotations

import csv
import random
from collections import Counter, defaultdict
from typing import Iterable

from common import build_declaration_metadata


RelationExample = tuple[str, str, str]


def filter_edges_by_types(edges: list[dict], relation_types: Iterable[str]) -> list[dict]:
    keep = set(relation_types)
    return [row for row in edges if row.get("edge_type", "") in keep]


def unique_relation_examples(edges: list[dict]) -> list[RelationExample]:
    seen: set[RelationExample] = set()
    examples: list[RelationExample] = []
    for row in edges:
        example = (row["src_id"], row["dst_id"], row["edge_type"])
        if example in seen:
            continue
        seen.add(example)
        examples.append(example)
    return examples


def stratified_split_relation_examples(
    examples: list[RelationExample],
    val_ratio: float,
    test_ratio: float,
    seed: int,
) -> dict[str, list[RelationExample]]:
    grouped: dict[str, list[RelationExample]] = defaultdict(list)
    for example in examples:
        grouped[example[2]].append(example)

    rng = random.Random(seed)
    split = {"train": [], "val": [], "test": []}
    for relation_type, rows in grouped.items():
        rows = list(rows)
        rng.shuffle(rows)
        n_total = len(rows)
        n_val = int(n_total * val_ratio)
        n_test = int(n_total * test_ratio)
        n_train = max(0, n_total - n_val - n_test)
        split["train"].extend(rows[:n_train])
        split["val"].extend(rows[n_train:n_train + n_val])
        split["test"].extend(rows[n_train + n_val:n_train + n_val + n_test])

    for split_name in split:
        rng.shuffle(split[split_name])
    return split


def build_relation_candidate_pools(
    declarations: list[dict],
    relation_types: Iterable[str],
    class_like_decl_kinds: Iterable[str],
) -> dict[str, list[str]]:
    relation_types = set(relation_types)
    class_like = set(class_like_decl_kinds)
    all_node_ids = [row["declaration_id"] for row in declarations]
    class_like_node_ids = [
        row["declaration_id"]
        for row in declarations
        if row.get("decl_kind", "") in class_like
    ]

    pools: dict[str, list[str]] = {}
    for relation_type in relation_types:
        if relation_type in {
            "extends",
            "instance_of",
            "ancestor",
            "extends_ancestor",
            "instance_ancestor",
            "hierarchy_ancestor",
        }:
            pools[relation_type] = class_like_node_ids
        else:
            pools[relation_type] = all_node_ids
    return pools


def build_parent_task_examples(
    edges: list[dict],
    hierarchy_relation_types: Iterable[str],
) -> list[RelationExample]:
    return unique_relation_examples(filter_edges_by_types(edges, hierarchy_relation_types))


def build_typed_link_task_examples(
    edges: list[dict],
    target_relation_types: Iterable[str],
) -> list[RelationExample]:
    return unique_relation_examples(filter_edges_by_types(edges, target_relation_types))


def build_ancestor_task_examples(
    declarations: list[dict],
    edges: list[dict],
    hierarchy_relation_types: Iterable[str],
    ancestor_label_mode: str = "source_kind",
    min_hops: int = 1,
) -> list[RelationExample]:
    metadata = {row["declaration_id"]: row for row in declarations}
    outgoing: dict[str, list[str]] = defaultdict(list)
    for row in filter_edges_by_types(edges, hierarchy_relation_types):
        outgoing[row["src_id"]].append(row["dst_id"])

    def relation_label(src_id: str) -> str:
        if ancestor_label_mode == "single":
            return "ancestor"
        src_kind = metadata.get(src_id, {}).get("decl_kind", "")
        if src_kind == "instance":
            return "instance_ancestor"
        return "extends_ancestor"

    closure_examples: list[RelationExample] = []
    seen: set[RelationExample] = set()
    for src_id in outgoing:
        stack = [(dst_id, 1) for dst_id in outgoing.get(src_id, [])]
        best_depth: dict[str, int] = {}
        while stack:
            dst_id, depth = stack.pop()
            if dst_id == src_id:
                continue
            prev_depth = best_depth.get(dst_id)
            if prev_depth is not None and prev_depth <= depth:
                continue
            best_depth[dst_id] = depth
            if depth >= min_hops:
                example = (src_id, dst_id, relation_label(src_id))
                if example not in seen:
                    seen.add(example)
                    closure_examples.append(example)
            for next_dst_id in outgoing.get(dst_id, []):
                next_depth = depth + 1
                if best_depth.get(next_dst_id, 10**9) > next_depth:
                    stack.append((next_dst_id, next_depth))
    return closure_examples


def build_task_positive_examples(
    declarations: list[dict],
    edges: list[dict],
    task_name: str,
    target_relation_types: Iterable[str],
    hierarchy_relation_types: Iterable[str],
    ancestor_label_mode: str = "source_kind",
    ancestor_min_hops: int = 1,
) -> list[RelationExample]:
    if task_name == "typed_link_prediction":
        return build_typed_link_task_examples(edges, target_relation_types)
    if task_name == "parent_prediction":
        return build_parent_task_examples(edges, hierarchy_relation_types)
    if task_name == "ancestor_ranking":
        return build_ancestor_task_examples(
            declarations=declarations,
            edges=edges,
            hierarchy_relation_types=hierarchy_relation_types,
            ancestor_label_mode=ancestor_label_mode,
            min_hops=ancestor_min_hops,
        )
    raise ValueError(f"Unsupported task_name: {task_name}")


def _intersect_preserve_order(pool: list[str], allowed: Iterable[str]) -> list[str]:
    allowed_set = set(allowed)
    return [item for item in pool if item in allowed_set]


def _bucket_candidates_for_src(
    src_id: str,
    relation_type: str,
    relation_candidate_pools: dict[str, list[str]],
    metadata: dict[str, dict],
    buckets: dict[str, dict[str, list[str]]],
    strategy: str,
) -> list[str]:
    base_pool = relation_candidate_pools.get(relation_type, [])
    if strategy == "random":
        return list(base_pool)

    strategy_to_key = {
        "same_module": "module_name",
        "same_namespace": "namespace",
        "same_decl_kind": "decl_kind",
    }
    value = metadata.get(src_id, {}).get(strategy_to_key[strategy], "")
    if not value:
        return []
    return _intersect_preserve_order(base_pool, buckets[strategy].get(value, []))


def sample_negative_relation_examples(
    declarations: list[dict],
    positive_examples: list[RelationExample],
    all_positive_examples: set[RelationExample],
    relation_candidate_pools: dict[str, list[str]],
    negative_ratio: float,
    seed: int,
    negative_strategy: str = "same_module",
    negative_fallback_strategy: str = "random",
) -> tuple[list[RelationExample], dict]:
    if negative_ratio <= 0 or not positive_examples:
        return [], {
            "requested": 0,
            "sampled": 0,
            "negative_strategy": negative_strategy,
            "negative_fallback_strategy": negative_fallback_strategy,
            "strategy_usage": {
                "random": 0,
                "same_module": 0,
                "same_namespace": 0,
                "same_decl_kind": 0,
            },
        }

    metadata, buckets = build_declaration_metadata(declarations)
    rng = random.Random(seed)
    strategy_usage = {
        "random": 0,
        "same_module": 0,
        "same_namespace": 0,
        "same_decl_kind": 0,
    }
    negatives: set[RelationExample] = set()
    ordered_positives = list(positive_examples)
    rng.shuffle(ordered_positives)
    requested = int(len(positive_examples) * negative_ratio)
    max_attempts = max(2000, requested * 40)
    attempts = 0
    cursor = 0

    while len(negatives) < requested and attempts < max_attempts:
        src_id, _, relation_type = ordered_positives[cursor % len(ordered_positives)]
        cursor += 1
        attempts += 1

        primary_pool = _bucket_candidates_for_src(
            src_id=src_id,
            relation_type=relation_type,
            relation_candidate_pools=relation_candidate_pools,
            metadata=metadata,
            buckets=buckets,
            strategy=negative_strategy,
        )
        used_strategy = negative_strategy
        candidate_pool = primary_pool
        if len(candidate_pool) < 2:
            candidate_pool = _bucket_candidates_for_src(
                src_id=src_id,
                relation_type=relation_type,
                relation_candidate_pools=relation_candidate_pools,
                metadata=metadata,
                buckets=buckets,
                strategy=negative_fallback_strategy,
            )
            used_strategy = negative_fallback_strategy
        if len(candidate_pool) < 2:
            continue

        dst_id = rng.choice(candidate_pool)
        if dst_id == src_id:
            continue
        candidate = (src_id, dst_id, relation_type)
        if candidate in negatives or candidate in all_positive_examples:
            continue
        negatives.add(candidate)
        strategy_usage[used_strategy] += 1

    return list(negatives), {
        "requested": requested,
        "sampled": len(negatives),
        "negative_strategy": negative_strategy,
        "negative_fallback_strategy": negative_fallback_strategy,
        "strategy_usage": strategy_usage,
    }


def write_relation_split_csv(
    path,
    split_name: str,
    positives: list[RelationExample],
    negatives: list[RelationExample],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["split", "src_id", "dst_id", "relation_type", "label"])
        for src_id, dst_id, relation_type in positives:
            writer.writerow([split_name, src_id, dst_id, relation_type, 1])
        for src_id, dst_id, relation_type in negatives:
            writer.writerow([split_name, src_id, dst_id, relation_type, 0])


def read_relation_split_examples(path) -> list[tuple[str, str, str, int]]:
    rows: list[tuple[str, str, str, int]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                (
                    row["src_id"],
                    row["dst_id"],
                    row["relation_type"],
                    int(row["label"]),
                )
            )
    return rows


def build_message_edges_for_training(
    edges: list[dict],
    message_relation_types: Iterable[str],
    held_out_direct_examples: set[RelationExample],
    exclude_held_out_direct_edges: bool,
) -> list[dict]:
    kept_rows: list[dict] = []
    for row in edges:
        relation_type = row.get("edge_type", "")
        if relation_type not in set(message_relation_types):
            continue
        example = (row["src_id"], row["dst_id"], relation_type)
        if exclude_held_out_direct_edges and example in held_out_direct_examples:
            continue
        kept_rows.append(row)
    return kept_rows


def build_ranking_queries(
    positive_examples: list[RelationExample],
    relation_candidate_pools: dict[str, list[str]],
) -> list[dict]:
    queries: list[dict] = []
    for src_id, dst_id, relation_type in positive_examples:
        candidate_ids = relation_candidate_pools.get(relation_type, [])
        if dst_id not in candidate_ids:
            candidate_ids = list(candidate_ids) + [dst_id]
        queries.append(
            {
                "src_id": src_id,
                "dst_id": dst_id,
                "relation_type": relation_type,
                "candidate_ids": candidate_ids,
            }
        )
    return queries


def summarize_relation_examples(examples: list[RelationExample]) -> dict[str, int]:
    counts = Counter(relation_type for _, _, relation_type in examples)
    return dict(sorted(counts.items()))


def summarize_ranking_ranks(ranks: list[int]) -> dict:
    if not ranks:
        return {
            "num_queries": 0,
            "mrr": None,
            "hits_at_1": None,
            "hits_at_3": None,
            "hits_at_10": None,
            "mean_rank": None,
            "median_rank": None,
        }

    sorted_ranks = sorted(ranks)
    mrr = sum(1.0 / rank for rank in ranks) / len(ranks)
    hits_at_1 = sum(rank <= 1 for rank in ranks) / len(ranks)
    hits_at_3 = sum(rank <= 3 for rank in ranks) / len(ranks)
    hits_at_10 = sum(rank <= 10 for rank in ranks) / len(ranks)
    midpoint = len(sorted_ranks) // 2
    if len(sorted_ranks) % 2 == 1:
        median_rank = float(sorted_ranks[midpoint])
    else:
        median_rank = 0.5 * (sorted_ranks[midpoint - 1] + sorted_ranks[midpoint])
    return {
        "num_queries": len(ranks),
        "mrr": float(mrr),
        "hits_at_1": float(hits_at_1),
        "hits_at_3": float(hits_at_3),
        "hits_at_10": float(hits_at_10),
        "mean_rank": float(sum(ranks) / len(ranks)),
        "median_rank": float(median_rank),
    }
