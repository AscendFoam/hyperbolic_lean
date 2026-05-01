from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict, deque
from pathlib import Path

from common import ensure_dir, load_config, load_declaration_graph, summarize_graph, write_json
from relation_tasks import (
    build_relation_candidate_pools,
    build_task_positive_examples,
    stratified_split_relation_examples,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run task-structure diagnostics for relation tasks.")
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


def quantile(sorted_values: list[float], q: float) -> float | None:
    if not sorted_values:
        return None
    if len(sorted_values) == 1:
        return float(sorted_values[0])
    idx = (len(sorted_values) - 1) * q
    lo = math.floor(idx)
    hi = math.ceil(idx)
    if lo == hi:
        return float(sorted_values[lo])
    frac = idx - lo
    return float(sorted_values[lo] * (1.0 - frac) + sorted_values[hi] * frac)


def summarize_values(values: list[int | float]) -> dict[str, float | int | None]:
    materialized = [float(v) for v in values]
    if not materialized:
        return {
            "count": 0,
            "mean": None,
            "min": None,
            "p50": None,
            "p90": None,
            "p95": None,
            "p99": None,
            "max": None,
        }
    ordered = sorted(materialized)
    return {
        "count": len(ordered),
        "mean": sum(ordered) / len(ordered),
        "min": ordered[0],
        "p50": quantile(ordered, 0.50),
        "p90": quantile(ordered, 0.90),
        "p95": quantile(ordered, 0.95),
        "p99": quantile(ordered, 0.99),
        "max": ordered[-1],
    }


def harmonic_number(n: int) -> float:
    return sum(1.0 / idx for idx in range(1, n + 1))


def expected_random_mrr(pool_size: int) -> float:
    return 0.0 if pool_size <= 0 else harmonic_number(pool_size) / pool_size


def expected_random_hits_at_k(pool_size: int, k: int) -> float:
    if pool_size <= 0:
        return 0.0
    return min(k, pool_size) / pool_size


def expected_positive_block_mrr(num_targets: int) -> float:
    return 0.0 if num_targets <= 0 else harmonic_number(num_targets) / num_targets


def expected_positive_block_hits_at_k(num_targets: int, k: int) -> float:
    if num_targets <= 0:
        return 0.0
    return min(k, num_targets) / num_targets


def build_hierarchy_graph(edges: list[dict], hierarchy_relation_types: set[str]) -> tuple[dict[str, set[str]], dict[str, int]]:
    outgoing: dict[str, set[str]] = defaultdict(set)
    out_degree: dict[str, int] = defaultdict(int)
    for row in edges:
        if row.get("edge_type", "") not in hierarchy_relation_types:
            continue
        src_id = row["src_id"]
        dst_id = row["dst_id"]
        if dst_id in outgoing[src_id]:
            continue
        outgoing[src_id].add(dst_id)
        out_degree[src_id] += 1
    return dict(outgoing), dict(out_degree)


def bfs_distances(outgoing: dict[str, set[str]], source: str) -> dict[str, int]:
    seen = {source}
    queue = deque([(source, 0)])
    distances = {source: 0}
    while queue:
        node, depth = queue.popleft()
        for nbr in outgoing.get(node, set()):
            if nbr in seen:
                continue
            seen.add(nbr)
            distances[nbr] = depth + 1
            queue.append((nbr, depth + 1))
    return distances


def hop_priority_expected_rr(target_hop: int, all_hops: list[int]) -> float:
    smaller = sum(1 for hop in all_hops if hop < target_hop)
    equal = sum(1 for hop in all_hops if hop == target_hop)
    if equal <= 0:
        return 0.0
    total = 0.0
    for rank in range(smaller + 1, smaller + equal + 1):
        total += 1.0 / rank
    return total / equal


def hop_priority_expected_hits_at_k(target_hop: int, all_hops: list[int], k: int) -> float:
    smaller = sum(1 for hop in all_hops if hop < target_hop)
    equal = sum(1 for hop in all_hops if hop == target_hop)
    if equal <= 0:
        return 0.0
    hits = 0
    for rank in range(smaller + 1, smaller + equal + 1):
        hits += 1 if rank <= k else 0
    return hits / equal


def analyze_split(
    split_name: str,
    split_examples: list[tuple[str, str, str]],
    all_positive_by_group: dict[tuple[str, str], list[tuple[str, int]]],
    relation_candidate_pools: dict[str, list[str]],
    outgoing: dict[str, set[str]],
    out_degree: dict[str, int],
) -> dict[str, object]:
    distance_cache: dict[str, dict[str, int]] = {}
    relation_counts = Counter()
    hop_histogram = Counter()
    pool_sizes: list[int] = []
    non_target_true_counts: list[int] = []
    positives_per_source_relation: list[int] = []
    direct_parent_counts: list[int] = []
    hop_values: list[int] = []
    random_mrr_values: list[float] = []
    random_hits10_values: list[float] = []
    positive_block_mrr_values: list[float] = []
    positive_block_hits10_values: list[float] = []
    hop_priority_mrr_values: list[float] = []
    hop_priority_hits10_values: list[float] = []
    unique_sources = set()
    unique_source_relations = set()

    for src_id, dst_id, relation_type in split_examples:
        if src_id not in distance_cache:
            distance_cache[src_id] = bfs_distances(outgoing, src_id)
        hop = int(distance_cache[src_id][dst_id])
        positives = all_positive_by_group[(src_id, relation_type)]
        positive_hops = [depth for _, depth in positives]
        num_targets = len(positives)
        pool_size = len(relation_candidate_pools[relation_type])
        direct_parents = int(out_degree.get(src_id, 0))

        relation_counts[relation_type] += 1
        hop_histogram[hop] += 1
        pool_sizes.append(pool_size)
        non_target_true_counts.append(num_targets - 1)
        positives_per_source_relation.append(num_targets)
        direct_parent_counts.append(direct_parents)
        hop_values.append(hop)
        random_mrr_values.append(expected_random_mrr(pool_size))
        random_hits10_values.append(expected_random_hits_at_k(pool_size, 10))
        positive_block_mrr_values.append(expected_positive_block_mrr(num_targets))
        positive_block_hits10_values.append(expected_positive_block_hits_at_k(num_targets, 10))
        hop_priority_mrr_values.append(hop_priority_expected_rr(hop, positive_hops))
        hop_priority_hits10_values.append(hop_priority_expected_hits_at_k(hop, positive_hops, 10))
        unique_sources.add(src_id)
        unique_source_relations.add((src_id, relation_type))

    return {
        "split": split_name,
        "num_queries": len(split_examples),
        "unique_sources": len(unique_sources),
        "unique_source_relation_groups": len(unique_source_relations),
        "relation_type_counts": dict(sorted(relation_counts.items())),
        "hop_histogram": {str(key): value for key, value in sorted(hop_histogram.items())},
        "hop_summary": summarize_values(hop_values),
        "candidate_pool_size_summary": summarize_values(pool_sizes),
        "non_target_true_ancestors_summary": summarize_values(non_target_true_counts),
        "positives_per_source_relation_summary": summarize_values(positives_per_source_relation),
        "direct_parent_count_summary": summarize_values(direct_parent_counts),
        "random_ranking_baseline": {
            "mrr": summarize_values(random_mrr_values),
            "hits_at_10": summarize_values(random_hits10_values),
        },
        "positive_block_ceiling": {
            "mrr": summarize_values(positive_block_mrr_values),
            "hits_at_10": summarize_values(positive_block_hits10_values),
        },
        "hop_priority_oracle": {
            "mrr": summarize_values(hop_priority_mrr_values),
            "hits_at_10": summarize_values(hop_priority_hits10_values),
        },
    }


def analyze_task(base_config_path: Path) -> dict[str, object]:
    config = load_config(base_config_path)
    graph_root = Path(config["graph_root"])
    if not graph_root.is_absolute():
        graph_root = (Path.cwd().resolve() / graph_root).resolve()

    declarations, edges = load_declaration_graph(graph_root)
    target_relation_types = list(config.get("target_relation_types", ["uses", "instance_of", "extends"]))
    hierarchy_relation_types = list(config.get("hierarchy_relation_types", ["extends", "instance_of"]))
    ancestor_label_mode = str(config.get("ancestor_label_mode", "source_kind"))
    ancestor_min_hops = int(config.get("ancestor_min_hops", 1))
    task_name = str(config["task"])

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
    relation_candidate_pools = build_relation_candidate_pools(
        declarations=declarations,
        relation_types=prediction_relation_types,
        class_like_decl_kinds=config.get("class_like_decl_kinds", ["class", "structure"]),
    )

    outgoing, out_degree = build_hierarchy_graph(edges, set(hierarchy_relation_types))
    distance_cache: dict[str, dict[str, int]] = {}
    all_positive_by_group: dict[tuple[str, str], list[tuple[str, int]]] = defaultdict(list)
    all_positive_by_source = Counter()
    for src_id, dst_id, relation_type in positive_examples:
        if src_id not in distance_cache:
            distance_cache[src_id] = bfs_distances(outgoing, src_id)
        hop = int(distance_cache[src_id][dst_id])
        all_positive_by_group[(src_id, relation_type)].append((dst_id, hop))
        all_positive_by_source[src_id] += 1

    return {
        "graph_root": str(graph_root),
        "task": task_name,
        "base_run_id": str(config["run_id"]),
        "graph_summary": summarize_graph(declarations, edges),
        "relation_candidate_pool_sizes": {
            relation_type: len(node_ids)
            for relation_type, node_ids in sorted(relation_candidate_pools.items())
        },
        "all_positive_relation_counts": dict(
            sorted(Counter(relation_type for _, _, relation_type in positive_examples).items())
        ),
        "all_positive_hop_histogram": {
            str(key): value
            for key, value in sorted(
                Counter(hop for group in all_positive_by_group.values() for _, hop in group).items()
            )
        },
        "all_positive_per_source_summary": summarize_values(list(all_positive_by_source.values())),
        "all_positive_per_source_relation_summary": summarize_values(
            [len(group) for group in all_positive_by_group.values()]
        ),
        "split_diagnostics": {
            split_name: analyze_split(
                split_name=split_name,
                split_examples=rows,
                all_positive_by_group=all_positive_by_group,
                relation_candidate_pools=relation_candidate_pools,
                outgoing=outgoing,
                out_degree=out_degree,
            )
            for split_name, rows in split.items()
        },
    }


def fmt(value: float | int | None, precision: int = 4) -> str:
    if value is None:
        return "NA"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{precision}f}"


def build_report(rows: list[dict[str, object]]) -> str:
    lines = [
        "# Task Structure Diagnostics",
        "",
        "## Overview",
        "",
        "| task | queries(test) | unique sources(test) | avg positives/source-rel(test) | avg non-target positives/query(test) | avg hop(test) | random MRR(test) | positive-block ceiling MRR(test) | hop-priority oracle MRR(test) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        test_diag = row["split_diagnostics"]["test"]
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["base_run_id"]),
                    fmt(test_diag["num_queries"]),
                    fmt(test_diag["unique_sources"]),
                    fmt(test_diag["positives_per_source_relation_summary"]["mean"]),
                    fmt(test_diag["non_target_true_ancestors_summary"]["mean"]),
                    fmt(test_diag["hop_summary"]["mean"]),
                    fmt(test_diag["random_ranking_baseline"]["mrr"]["mean"]),
                    fmt(test_diag["positive_block_ceiling"]["mrr"]["mean"]),
                    fmt(test_diag["hop_priority_oracle"]["mrr"]["mean"]),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Details", ""])
    for row in rows:
        lines.append(f"### {row['base_run_id']}")
        lines.append(
            f"- Graph: {row['graph_root']}"
        )
        lines.append(
            f"- Task: {row['task']}, relation counts: {row['all_positive_relation_counts']}, candidate pools: {row['relation_candidate_pool_sizes']}"
        )
        lines.append(
            f"- All positives per source summary: mean={fmt(row['all_positive_per_source_summary']['mean'])}, p50={fmt(row['all_positive_per_source_summary']['p50'])}, max={fmt(row['all_positive_per_source_summary']['max'])}"
        )
        lines.append(
            f"- All positives per source-relation summary: mean={fmt(row['all_positive_per_source_relation_summary']['mean'])}, p50={fmt(row['all_positive_per_source_relation_summary']['p50'])}, max={fmt(row['all_positive_per_source_relation_summary']['max'])}"
        )
        for split_name in ["val", "test"]:
            split_diag = row["split_diagnostics"][split_name]
            lines.append(f"- {split_name}: queries={split_diag['num_queries']}, unique_sources={split_diag['unique_sources']}, relation_counts={split_diag['relation_type_counts']}")
            lines.append(
                f"  hop mean={fmt(split_diag['hop_summary']['mean'])}, p50={fmt(split_diag['hop_summary']['p50'])}, max={fmt(split_diag['hop_summary']['max'])}, histogram={split_diag['hop_histogram']}"
            )
            lines.append(
                f"  non-target true ancestors/query mean={fmt(split_diag['non_target_true_ancestors_summary']['mean'])}, p50={fmt(split_diag['non_target_true_ancestors_summary']['p50'])}, max={fmt(split_diag['non_target_true_ancestors_summary']['max'])}"
            )
            lines.append(
                f"  positives/source-rel mean={fmt(split_diag['positives_per_source_relation_summary']['mean'])}, p50={fmt(split_diag['positives_per_source_relation_summary']['p50'])}, max={fmt(split_diag['positives_per_source_relation_summary']['max'])}"
            )
            lines.append(
                f"  direct parents/source mean={fmt(split_diag['direct_parent_count_summary']['mean'])}, p50={fmt(split_diag['direct_parent_count_summary']['p50'])}, max={fmt(split_diag['direct_parent_count_summary']['max'])}"
            )
            lines.append(
                f"  expected random ranking: MRR={fmt(split_diag['random_ranking_baseline']['mrr']['mean'])}, Hits@10={fmt(split_diag['random_ranking_baseline']['hits_at_10']['mean'])}"
            )
            lines.append(
                f"  positive-block ceiling: MRR={fmt(split_diag['positive_block_ceiling']['mrr']['mean'])}, Hits@10={fmt(split_diag['positive_block_ceiling']['hits_at_10']['mean'])}"
            )
            lines.append(
                f"  hop-priority oracle: MRR={fmt(split_diag['hop_priority_oracle']['mrr']['mean'])}, Hits@10={fmt(split_diag['hop_priority_oracle']['hits_at_10']['mean'])}"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    workspace_root = Path.cwd().resolve()

    output_root = Path(config["output_root"])
    if not output_root.is_absolute():
        output_root = (workspace_root / output_root).resolve()
    ensure_dir(output_root)
    ensure_dir(output_root / "analyses")

    rows: list[dict[str, object]] = []
    for analysis_cfg in config["analyses"]:
        base_config_path = Path(analysis_cfg["base_config"])
        if not base_config_path.is_absolute():
            base_config_path = (workspace_root / base_config_path).resolve()
        result = analyze_task(base_config_path)
        result["name"] = analysis_cfg["name"]
        rows.append(result)
        write_json(output_root / "analyses" / f"{analysis_cfg['name']}.json", result)
        print(
            f"[done] task diagnostics: {analysis_cfg['name']} "
            f"task={result['task']} "
            f"queries(test)={result['split_diagnostics']['test']['num_queries']}"
        )

    report = build_report(rows)
    (output_root / "report.md").write_text(report, encoding="utf-8")
    write_json(output_root / "summary.json", {"config": config, "analyses": rows})
    print(f"[done] report: {output_root / 'report.md'}")
    print(f"[done] summary: {output_root / 'summary.json'}")


if __name__ == "__main__":
    main()
