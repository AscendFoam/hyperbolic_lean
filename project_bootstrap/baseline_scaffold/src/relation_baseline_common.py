from __future__ import annotations

import copy
import importlib.util
import math
from collections import defaultdict
from pathlib import Path

from common import (
    build_run_manifest,
    ensure_dir,
    load_declaration_graph,
    summarize_graph,
    write_json,
)
from relation_tasks import (
    build_relation_candidate_pools,
    build_grouped_ranking_queries,
    build_task_positive_examples,
    build_ranking_queries,
    build_ancestor_task_examples_with_hops,
    read_relation_split_examples,
    hop_bucket_name,
    sample_negative_relation_examples,
    stratified_split_relation_examples,
    summarize_ranking_ranks,
    summarize_relation_examples,
    write_relation_split_csv,
)


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def import_training_deps() -> tuple:
    import numpy as np
    import torch
    import torch.nn.functional as F
    from sklearn.metrics import accuracy_score, average_precision_score, f1_score, roc_auc_score

    return np, torch, F, accuracy_score, average_precision_score, f1_score, roc_auc_score


def build_relation_type_index(relation_types: list[str]) -> dict[str, int]:
    return {relation_type: idx for idx, relation_type in enumerate(relation_types)}


def build_edge_tensors(edge_examples, node_to_idx: dict[str, int], relation_to_idx: dict[str, int], torch):
    edges: list[list[int]] = []
    relation_ids: list[int] = []
    labels: list[float] = []
    for src_id, dst_id, relation_type, label in edge_examples:
        if src_id not in node_to_idx or dst_id not in node_to_idx:
            continue
        if relation_type not in relation_to_idx:
            continue
        edges.append([node_to_idx[src_id], node_to_idx[dst_id]])
        relation_ids.append(relation_to_idx[relation_type])
        labels.append(float(label))
    if not edges:
        raise ValueError("No valid relation examples were found after filtering.")
    return (
        torch.tensor(edges, dtype=torch.long),
        torch.tensor(relation_ids, dtype=torch.long),
        torch.tensor(labels, dtype=torch.float32),
    )


def build_relation_aware_adjacency(
    num_nodes: int,
    train_message_edges: list[dict],
    relation_to_idx: dict[str, int],
    symmetrize: bool,
    torch,
):
    num_relations = len(relation_to_idx)
    edge_pairs_by_relation: dict[int, set[tuple[int, int]]] = {
        relation_idx: set() for relation_idx in range(num_relations)
    }
    for row in train_message_edges:
        relation_idx = relation_to_idx[row["edge_type"]]
        src_idx = row["src_idx"]
        dst_idx = row["dst_idx"]
        edge_pairs_by_relation[relation_idx].add((src_idx, dst_idx))
        if symmetrize:
            edge_pairs_by_relation[relation_idx].add((dst_idx, src_idx))
    for relation_idx in range(num_relations):
        for node_idx in range(num_nodes):
            edge_pairs_by_relation[relation_idx].add((node_idx, node_idx))

    adjacency_by_relation: dict[int, object] = {}
    for relation_idx, edge_pairs in edge_pairs_by_relation.items():
        src = torch.tensor([s for s, _ in edge_pairs], dtype=torch.long)
        dst = torch.tensor([d for _, d in edge_pairs], dtype=torch.long)
        degree = torch.zeros(num_nodes, dtype=torch.float32)
        degree.index_add_(0, src, torch.ones(len(edge_pairs), dtype=torch.float32))
        deg_inv_sqrt = degree.pow(-0.5)
        deg_inv_sqrt[torch.isinf(deg_inv_sqrt)] = 0.0
        values = deg_inv_sqrt[src] * deg_inv_sqrt[dst]
        adjacency_by_relation[relation_idx] = torch.sparse_coo_tensor(
            torch.stack([src, dst], dim=0),
            values,
            (num_nodes, num_nodes),
        ).coalesce()
    return adjacency_by_relation


def evaluate_split(logits, labels, accuracy_score, average_precision_score, f1_score, roc_auc_score):
    prob = logits.sigmoid().detach().cpu().numpy()
    y = labels.detach().cpu().numpy().astype(int)
    pred = (prob >= 0.5).astype(int)

    auroc = None
    average_precision = None
    if len(set(y.tolist())) >= 2:
        auroc = float(roc_auc_score(y, prob))
    if int(y.sum()) > 0:
        average_precision = float(average_precision_score(y, prob))

    return {
        "auroc": auroc,
        "average_precision": average_precision,
        "accuracy": float(accuracy_score(y, pred)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "num_examples": int(len(y)),
        "num_positive": int(y.sum()),
        "num_negative": int(len(y) - y.sum()),
    }


def fmt_metric(value) -> str:
    if value is None:
        return "NA"
    return f"{value:.4f}"


def flatten_grouped_hop_bucket_summary(grouped: dict) -> dict[str, float | None]:
    flattened: dict[str, float | None] = {}
    hop_buckets = grouped.get("hop_buckets", {})
    for bucket_name in ["hop_2", "hop_3", "hop_4_plus"]:
        bucket_metrics = hop_buckets.get(bucket_name, {})
        for metric_name in [
            "map",
            "ndcg",
            "grouped_mrr",
            "recall_at_1",
            "recall_at_3",
            "recall_at_5",
            "recall_at_10",
        ]:
            flattened[f"{bucket_name}_{metric_name}"] = bucket_metrics.get(metric_name, {}).get("mean")
    return flattened


def build_ranking_metrics(model, embeddings, queries, node_to_idx, relation_to_idx, torch):
    ranks: list[int] = []
    model.eval()
    with torch.no_grad():
        for query in queries:
            src_id = query["src_id"]
            dst_id = query["dst_id"]
            relation_type = query["relation_type"]
            candidate_ids = [candidate_id for candidate_id in query["candidate_ids"] if candidate_id in node_to_idx]
            if src_id not in node_to_idx or dst_id not in node_to_idx or len(candidate_ids) < 2:
                continue
            edge_index = torch.tensor(
                [[node_to_idx[src_id], node_to_idx[candidate_id]] for candidate_id in candidate_ids],
                dtype=torch.long,
            )
            relation_ids = torch.tensor(
                [relation_to_idx[relation_type] for _ in candidate_ids],
                dtype=torch.long,
            )
            logits = model.decode(embeddings, edge_index, relation_ids)
            order = torch.argsort(logits, descending=True).detach().cpu().tolist()
            ranked_ids = [candidate_ids[idx] for idx in order]
            try:
                rank = ranked_ids.index(dst_id) + 1
            except ValueError:
                continue
            ranks.append(rank)
    return summarize_ranking_ranks(ranks)


def average_precision_from_binary_relevance(binary_relevance: list[int]) -> float | None:
    positive_count = sum(binary_relevance)
    if positive_count <= 0:
        return None
    hits = 0
    precision_sum = 0.0
    for idx, is_positive in enumerate(binary_relevance, start=1):
        if not is_positive:
            continue
        hits += 1
        precision_sum += hits / idx
    return precision_sum / positive_count


def dcg_at_k(binary_relevance: list[int], k: int | None = None) -> float:
    if k is None:
        k = len(binary_relevance)
    score = 0.0
    for idx, is_positive in enumerate(binary_relevance[:k], start=1):
        if not is_positive:
            continue
        score += 1.0 / math.log2(idx + 1)
    return score


def ndcg_from_binary_relevance(binary_relevance: list[int], k: int | None = None) -> float | None:
    positive_count = sum(binary_relevance)
    if positive_count <= 0:
        return None
    if k is None:
        k = len(binary_relevance)
    ideal = [1] * min(positive_count, k)
    ideal_dcg = dcg_at_k(ideal, k=k)
    if ideal_dcg <= 0:
        return None
    return dcg_at_k(binary_relevance, k=k) / ideal_dcg


def summarize_grouped_scores(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "mean": None, "min": None, "p50": None, "p90": None, "max": None}
    ordered = sorted(values)
    return {
        "count": len(ordered),
        "mean": float(sum(ordered) / len(ordered)),
        "min": float(ordered[0]),
        "p50": float(ordered[len(ordered) // 2]),
        "p90": float(ordered[min(len(ordered) - 1, int(0.9 * (len(ordered) - 1)))]),
        "max": float(ordered[-1]),
    }


def build_grouped_ranking_metrics(model, embeddings, grouped_queries, node_to_idx, relation_to_idx, torch):
    grouped_ap: list[float] = []
    grouped_ndcg: list[float] = []
    grouped_ndcg_10: list[float] = []
    grouped_mrr: list[float] = []
    grouped_recall_1: list[float] = []
    grouped_recall_3: list[float] = []
    grouped_recall_5: list[float] = []
    grouped_recall_10: list[float] = []
    hop_bucket_metrics: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    model.eval()
    with torch.no_grad():
        for query in grouped_queries:
            src_id = query["src_id"]
            relation_type = query["relation_type"]
            positive_ids = [node_id for node_id in query["positive_ids"] if node_id in node_to_idx]
            candidate_ids = [candidate_id for candidate_id in query["candidate_ids"] if candidate_id in node_to_idx]
            if src_id not in node_to_idx or len(candidate_ids) < 2 or not positive_ids:
                continue

            edge_index = torch.tensor(
                [[node_to_idx[src_id], node_to_idx[candidate_id]] for candidate_id in candidate_ids],
                dtype=torch.long,
            )
            relation_ids = torch.tensor(
                [relation_to_idx[relation_type] for _ in candidate_ids],
                dtype=torch.long,
            )
            logits = model.decode(embeddings, edge_index, relation_ids)
            order = torch.argsort(logits, descending=True).detach().cpu().tolist()
            ranked_ids = [candidate_ids[idx] for idx in order]
            ranked_positive_set = set(positive_ids)
            binary_relevance = [1 if candidate_id in ranked_positive_set else 0 for candidate_id in ranked_ids]
            positive_ranks = [rank + 1 for rank, candidate_id in enumerate(ranked_ids) if candidate_id in ranked_positive_set]
            if not positive_ranks:
                continue

            ap = average_precision_from_binary_relevance(binary_relevance)
            ndcg = ndcg_from_binary_relevance(binary_relevance)
            ndcg_10 = ndcg_from_binary_relevance(binary_relevance, k=10)
            first_positive_rank = min(positive_ranks)
            positive_count = len(positive_ids)

            grouped_ap.append(ap if ap is not None else 0.0)
            grouped_ndcg.append(ndcg if ndcg is not None else 0.0)
            grouped_ndcg_10.append(ndcg_10 if ndcg_10 is not None else 0.0)
            grouped_mrr.append(1.0 / first_positive_rank)
            grouped_recall_1.append(sum(rank <= 1 for rank in positive_ranks) / positive_count)
            grouped_recall_3.append(sum(rank <= 3 for rank in positive_ranks) / positive_count)
            grouped_recall_5.append(sum(rank <= 5 for rank in positive_ranks) / positive_count)
            grouped_recall_10.append(sum(rank <= 10 for rank in positive_ranks) / positive_count)

            bucket_to_positive_ids = query.get("positive_ids_by_hop_bucket", {})
            for bucket_name, bucket_positive_ids in bucket_to_positive_ids.items():
                bucket_positive_set = {node_id for node_id in bucket_positive_ids if node_id in node_to_idx}
                if not bucket_positive_set:
                    continue
                bucket_relevance = [1 if candidate_id in bucket_positive_set else 0 for candidate_id in ranked_ids]
                bucket_positive_ranks = [
                    rank + 1 for rank, candidate_id in enumerate(ranked_ids) if candidate_id in bucket_positive_set
                ]
                if not bucket_positive_ranks:
                    continue
                hop_bucket_metrics[bucket_name]["recall_at_1"].append(
                    sum(rank <= 1 for rank in bucket_positive_ranks) / len(bucket_positive_set)
                )
                hop_bucket_metrics[bucket_name]["recall_at_3"].append(
                    sum(rank <= 3 for rank in bucket_positive_ranks) / len(bucket_positive_set)
                )
                hop_bucket_metrics[bucket_name]["recall_at_5"].append(
                    sum(rank <= 5 for rank in bucket_positive_ranks) / len(bucket_positive_set)
                )
                hop_bucket_metrics[bucket_name]["recall_at_10"].append(
                    sum(rank <= 10 for rank in bucket_positive_ranks) / len(bucket_positive_set)
                )
                bucket_ap = average_precision_from_binary_relevance(bucket_relevance)
                bucket_ndcg = ndcg_from_binary_relevance(bucket_relevance)
                bucket_first_rank = min(bucket_positive_ranks)
                hop_bucket_metrics[bucket_name]["map"].append(bucket_ap if bucket_ap is not None else 0.0)
                hop_bucket_metrics[bucket_name]["ndcg"].append(bucket_ndcg if bucket_ndcg is not None else 0.0)
                hop_bucket_metrics[bucket_name]["grouped_mrr"].append(1.0 / bucket_first_rank)

    return {
        "num_queries": len(grouped_ap),
        "map": float(sum(grouped_ap) / len(grouped_ap)) if grouped_ap else None,
        "ndcg": float(sum(grouped_ndcg) / len(grouped_ndcg)) if grouped_ndcg else None,
        "ndcg_at_10": float(sum(grouped_ndcg_10) / len(grouped_ndcg_10)) if grouped_ndcg_10 else None,
        "grouped_mrr": float(sum(grouped_mrr) / len(grouped_mrr)) if grouped_mrr else None,
        "recall_at_1": float(sum(grouped_recall_1) / len(grouped_recall_1)) if grouped_recall_1 else None,
        "recall_at_3": float(sum(grouped_recall_3) / len(grouped_recall_3)) if grouped_recall_3 else None,
        "recall_at_5": float(sum(grouped_recall_5) / len(grouped_recall_5)) if grouped_recall_5 else None,
        "recall_at_10": float(sum(grouped_recall_10) / len(grouped_recall_10)) if grouped_recall_10 else None,
        "hop_buckets": {
            bucket_name: {
                metric_name: summarize_grouped_scores(values)
                for metric_name, values in sorted(metric_values.items())
            }
            for bucket_name, metric_values in sorted(hop_bucket_metrics.items())
        },
    }


def prepare_relation_run_data(config: dict) -> dict:
    graph_root = Path(config["graph_root"])
    artifacts_root = Path(config["artifacts_root"])
    ensure_dir(artifacts_root)

    declarations, edges = load_declaration_graph(graph_root)
    graph_summary = summarize_graph(declarations, edges)

    task_name = str(config["task"])
    target_relation_types = list(config.get("target_relation_types", ["uses", "instance_of", "extends"]))
    hierarchy_relation_types = list(config.get("hierarchy_relation_types", ["extends", "instance_of"]))
    ancestor_label_mode = str(config.get("ancestor_label_mode", "source_kind"))
    ancestor_min_hops = int(config.get("ancestor_min_hops", 1))
    positive_hop_lookup: dict[tuple[str, str, str], int] = {}
    if task_name == "ancestor_ranking":
        positive_examples, positive_hop_lookup = build_ancestor_task_examples_with_hops(
            declarations=declarations,
            edges=edges,
            hierarchy_relation_types=hierarchy_relation_types,
            ancestor_label_mode=ancestor_label_mode,
            min_hops=ancestor_min_hops,
        )
    else:
        positive_examples = build_task_positive_examples(
            declarations=declarations,
            edges=edges,
            task_name=task_name,
            target_relation_types=target_relation_types,
            hierarchy_relation_types=hierarchy_relation_types,
            ancestor_label_mode=ancestor_label_mode,
            ancestor_min_hops=ancestor_min_hops,
        )
    split = stratified_split_relation_examples(
        examples=positive_examples,
        val_ratio=float(config["val_ratio"]),
        test_ratio=float(config["test_ratio"]),
        seed=int(config["seed"]),
    )

    prediction_relation_types = sorted({relation_type for _, _, relation_type in positive_examples})
    message_relation_types = list(config.get("message_relation_types", target_relation_types))
    relation_candidate_pools = build_relation_candidate_pools(
        declarations=declarations,
        relation_types=prediction_relation_types,
        class_like_decl_kinds=config.get("class_like_decl_kinds", ["class", "structure"]),
    )
    all_positive_examples = set(positive_examples)
    negative_ratio = float(config.get("negative_ratio", 1.0))
    negative_strategy = str(config.get("negative_strategy", "same_module"))
    negative_fallback_strategy = str(config.get("negative_fallback_strategy", "random"))
    negative_sampling_stats: dict[str, dict] = {}

    for split_name, positive_split_examples in split.items():
        negatives, sampling_stats = sample_negative_relation_examples(
            declarations=declarations,
            positive_examples=positive_split_examples,
            all_positive_examples=all_positive_examples,
            relation_candidate_pools=relation_candidate_pools,
            negative_ratio=negative_ratio,
            seed=int(config["seed"]) + {"train": 101, "val": 202, "test": 303}[split_name],
            negative_strategy=negative_strategy,
            negative_fallback_strategy=negative_fallback_strategy,
        )
        negative_sampling_stats[split_name] = sampling_stats
        write_relation_split_csv(
            path=artifacts_root / f"{split_name}_edges.csv",
            split_name=split_name,
            positives=positive_split_examples,
            negatives=negatives,
        )

    dependency_status = {
        "torch": has_module("torch"),
        "numpy": has_module("numpy"),
        "sklearn": has_module("sklearn"),
    }
    manifest = build_run_manifest(config, graph_summary, dependency_status)
    manifest["task_summary"] = {
        "num_positive_examples": len(positive_examples),
        "relation_type_counts": summarize_relation_examples(positive_examples),
    }
    write_json(artifacts_root / "run_manifest.json", manifest)
    write_json(artifacts_root / "negative_sampling_stats.json", negative_sampling_stats)

    return {
        "graph_root": graph_root,
        "artifacts_root": artifacts_root,
        "declarations": declarations,
        "edges": edges,
        "graph_summary": graph_summary,
        "split": split,
        "prediction_relation_types": prediction_relation_types,
        "message_relation_types": message_relation_types,
        "relation_candidate_pools": relation_candidate_pools,
        "positive_hop_lookup": positive_hop_lookup,
        "dependency_status": dependency_status,
        "negative_sampling_stats": negative_sampling_stats,
        "task_summary": copy.deepcopy(manifest["task_summary"]),
    }


def load_relation_split_triplets(artifacts_root: Path) -> dict[str, list[tuple[str, str, str, int]]]:
    return {
        "train": read_relation_split_examples(artifacts_root / "train_edges.csv"),
        "val": read_relation_split_examples(artifacts_root / "val_edges.csv"),
        "test": read_relation_split_examples(artifacts_root / "test_edges.csv"),
    }


def build_ranking_task_metrics(
    model,
    embeddings,
    split_examples: dict[str, list[tuple[str, str, str, int]]],
    relation_candidate_pools: dict[str, list[str]],
    node_to_idx: dict[str, int],
    relation_to_idx: dict[str, int],
    positive_hop_lookup: dict[tuple[str, str, str], int],
    torch,
):
    metrics = {}
    for split_name in ["val", "test"]:
        positive_rows = [
            (src_id, dst_id, relation_type)
            for src_id, dst_id, relation_type, label in split_examples[split_name]
            if label == 1
        ]
        queries = build_ranking_queries(positive_rows, relation_candidate_pools)
        metrics[split_name] = build_ranking_metrics(
            model=model,
            embeddings=embeddings,
            queries=queries,
            node_to_idx=node_to_idx,
            relation_to_idx=relation_to_idx,
            torch=torch,
        )
        grouped_queries = build_grouped_ranking_queries(
            positive_rows,
            relation_candidate_pools,
            positive_hop_lookup=positive_hop_lookup,
        )
        metrics[split_name]["grouped"] = build_grouped_ranking_metrics(
            model=model,
            embeddings=embeddings,
            grouped_queries=grouped_queries,
            node_to_idx=node_to_idx,
            relation_to_idx=relation_to_idx,
            torch=torch,
        )
    return metrics
