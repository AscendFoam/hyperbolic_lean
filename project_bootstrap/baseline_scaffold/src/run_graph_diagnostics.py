from __future__ import annotations

import argparse
import itertools
import math
import random
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Iterable

from common import ensure_dir, load_config, load_declaration_graph, summarize_graph, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run structural diagnostics on declaration graphs.")
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


def summarize_values(values: Iterable[int | float]) -> dict[str, float | int | None]:
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


def build_graph_indices(
    declarations: list[dict],
    edges: list[dict],
    relation_edge_types: set[str],
) -> dict:
    node_ids = [row["declaration_id"] for row in declarations]
    node_set = set(node_ids)

    out_neighbors: dict[str, set[str]] = {node_id: set() for node_id in node_ids}
    in_neighbors: dict[str, set[str]] = {node_id: set() for node_id in node_ids}
    undirected_neighbors: dict[str, set[str]] = {node_id: set() for node_id in node_ids}

    relation_out_neighbors: dict[str, set[str]] = defaultdict(set)
    relation_in_neighbors: dict[str, set[str]] = defaultdict(set)
    relation_undirected_neighbors: dict[str, set[str]] = defaultdict(set)
    relation_edge_count = 0

    undirected_edge_pairs: set[tuple[str, str]] = set()
    relation_undirected_edge_pairs: set[tuple[str, str]] = set()
    edge_type_counts: Counter[str] = Counter()

    for row in edges:
        src_id = row["src_id"]
        dst_id = row["dst_id"]
        edge_type = row.get("edge_type", "")
        if src_id not in node_set or dst_id not in node_set:
            continue

        edge_type_counts[edge_type] += 1
        out_neighbors[src_id].add(dst_id)
        in_neighbors[dst_id].add(src_id)

        if src_id != dst_id:
            undirected_neighbors[src_id].add(dst_id)
            undirected_neighbors[dst_id].add(src_id)
            undirected_edge_pairs.add(tuple(sorted((src_id, dst_id))))

        if edge_type not in relation_edge_types:
            continue

        relation_edge_count += 1
        relation_out_neighbors[src_id].add(dst_id)
        relation_in_neighbors[dst_id].add(src_id)
        if src_id != dst_id:
            relation_undirected_neighbors[src_id].add(dst_id)
            relation_undirected_neighbors[dst_id].add(src_id)
            relation_undirected_edge_pairs.add(tuple(sorted((src_id, dst_id))))

    relation_node_ids = sorted(
        set(relation_out_neighbors.keys())
        | set(relation_in_neighbors.keys())
        | set(relation_undirected_neighbors.keys())
    )
    for node_id in relation_node_ids:
        relation_out_neighbors.setdefault(node_id, set())
        relation_in_neighbors.setdefault(node_id, set())
        relation_undirected_neighbors.setdefault(node_id, set())

    return {
        "node_ids": node_ids,
        "out_neighbors": out_neighbors,
        "in_neighbors": in_neighbors,
        "undirected_neighbors": undirected_neighbors,
        "undirected_edge_count": len(undirected_edge_pairs),
        "edge_type_counts": dict(sorted(edge_type_counts.items())),
        "relation_node_ids": relation_node_ids,
        "relation_out_neighbors": dict(relation_out_neighbors),
        "relation_in_neighbors": dict(relation_in_neighbors),
        "relation_undirected_neighbors": dict(relation_undirected_neighbors),
        "relation_edge_count": relation_edge_count,
        "relation_undirected_edge_count": len(relation_undirected_edge_pairs),
    }


def connected_components(adj: dict[str, set[str]], nodes: list[str]) -> list[list[str]]:
    seen: set[str] = set()
    components: list[list[str]] = []

    for start in nodes:
        if start in seen:
            continue
        seen.add(start)
        queue = deque([start])
        component: list[str] = []
        while queue:
            node = queue.popleft()
            component.append(node)
            for nbr in adj.get(node, set()):
                if nbr in seen:
                    continue
                seen.add(nbr)
                queue.append(nbr)
        components.append(component)
    return components


def bfs_distances(adj: dict[str, set[str]], source: str, allowed: set[str] | None = None) -> dict[str, int]:
    seen = {source}
    queue = deque([(source, 0)])
    distances = {source: 0}
    while queue:
        node, dist = queue.popleft()
        for nbr in adj.get(node, set()):
            if allowed is not None and nbr not in allowed:
                continue
            if nbr in seen:
                continue
            seen.add(nbr)
            distances[nbr] = dist + 1
            queue.append((nbr, dist + 1))
    return distances


def component_size_summary(components: list[list[str]]) -> dict[str, float | int | None]:
    sizes = sorted((len(component) for component in components), reverse=True)
    return {
        "count": len(sizes),
        "largest": sizes[0] if sizes else 0,
        "second_largest": sizes[1] if len(sizes) > 1 else 0,
        "top10": sizes[:10],
        "size_summary": summarize_values(sizes),
    }


def distance_and_hyperbolicity_diagnostics(
    adj: dict[str, set[str]],
    component_nodes: list[str],
    rng: random.Random,
    distance_source_count: int,
    hyperbolicity_landmarks: int,
    max_hyperbolicity_quadruples: int,
) -> dict[str, object]:
    if not component_nodes:
        return {
            "distance_stats": None,
            "diameter_estimate": None,
            "hyperbolicity_proxy": None,
        }

    sample_size = min(distance_source_count, len(component_nodes))
    sampled_sources = sorted(rng.sample(component_nodes, sample_size))
    component_node_set = set(component_nodes)
    collected_distances: list[int] = []
    diameter_estimate = 0
    bfs_cache: dict[str, dict[str, int]] = {}

    for source in sampled_sources:
        distances = bfs_distances(adj, source, allowed=component_node_set)
        bfs_cache[source] = distances
        values = [dist for node_id, dist in distances.items() if node_id != source]
        collected_distances.extend(values)
        if values:
            diameter_estimate = max(diameter_estimate, max(values))

    hyperbolicity_proxy = None
    landmark_count = min(hyperbolicity_landmarks, len(component_nodes))
    if landmark_count >= 4:
        landmark_nodes = sampled_sources[:]
        if len(landmark_nodes) < landmark_count:
            extras = [node_id for node_id in component_nodes if node_id not in set(landmark_nodes)]
            landmark_nodes.extend(rng.sample(extras, landmark_count - len(landmark_nodes)))
        landmark_nodes = landmark_nodes[:landmark_count]

        landmark_distances: dict[str, dict[str, int]] = {}
        for source in landmark_nodes:
            if source in bfs_cache:
                landmark_distances[source] = bfs_cache[source]
            else:
                landmark_distances[source] = bfs_distances(adj, source, allowed=component_node_set)

        pair_distances: list[int] = []
        for left_idx, left in enumerate(landmark_nodes):
            for right in landmark_nodes[left_idx + 1:]:
                pair_distances.append(landmark_distances[left][right])

        quadruples = list(itertools.combinations(landmark_nodes, 4))
        if len(quadruples) > max_hyperbolicity_quadruples:
            quadruples = rng.sample(quadruples, max_hyperbolicity_quadruples)

        deltas: list[float] = []
        for a, b, c, d in quadruples:
            s1 = landmark_distances[a][b] + landmark_distances[c][d]
            s2 = landmark_distances[a][c] + landmark_distances[b][d]
            s3 = landmark_distances[a][d] + landmark_distances[b][c]
            ordered = sorted([s1, s2, s3])
            deltas.append((ordered[2] - ordered[1]) / 2.0)

        mean_pair_distance = sum(pair_distances) / len(pair_distances) if pair_distances else None
        max_delta = max(deltas) if deltas else None
        hyperbolicity_proxy = {
            "landmark_count": len(landmark_nodes),
            "quadruple_count": len(deltas),
            "delta_max": max_delta,
            "delta_mean": (sum(deltas) / len(deltas)) if deltas else None,
            "delta_p90": quantile(sorted(deltas), 0.90) if deltas else None,
            "mean_pair_distance": mean_pair_distance,
            "diameter_estimate_on_landmarks": max(pair_distances) if pair_distances else None,
            "delta_over_mean_pair_distance": (
                None if not deltas or not mean_pair_distance else max_delta / mean_pair_distance
            ),
            "delta_over_diameter_estimate": (
                None if not deltas or diameter_estimate == 0 else max_delta / diameter_estimate
            ),
        }

    return {
        "sampled_source_count": len(sampled_sources),
        "distance_stats": summarize_values(collected_distances),
        "diameter_estimate": diameter_estimate if diameter_estimate > 0 else None,
        "hyperbolicity_proxy": hyperbolicity_proxy,
    }


def strongly_connected_components(adj: dict[str, set[str]]) -> tuple[list[list[str]], dict[str, int]]:
    nodes = list(adj.keys())
    visited: set[str] = set()
    order: list[str] = []

    for start in nodes:
        if start in visited:
            continue
        stack: list[tuple[str, int]] = [(start, 0)]
        visited.add(start)
        while stack:
            node, state = stack.pop()
            if state == 0:
                stack.append((node, 1))
                for nbr in adj.get(node, set()):
                    if nbr in visited:
                        continue
                    visited.add(nbr)
                    stack.append((nbr, 0))
            else:
                order.append(node)

    reverse_adj: dict[str, set[str]] = {node: set() for node in nodes}
    for src_id, nbrs in adj.items():
        for dst_id in nbrs:
            reverse_adj.setdefault(dst_id, set()).add(src_id)

    components: list[list[str]] = []
    component_index: dict[str, int] = {}
    assigned: set[str] = set()

    for start in reversed(order):
        if start in assigned:
            continue
        stack = [start]
        assigned.add(start)
        component: list[str] = []
        while stack:
            node = stack.pop()
            component.append(node)
            component_index[node] = len(components)
            for nbr in reverse_adj.get(node, set()):
                if nbr in assigned:
                    continue
                assigned.add(nbr)
                stack.append(nbr)
        components.append(component)

    return components, component_index


def condensation_longest_path(
    adj: dict[str, set[str]],
    components: list[list[str]],
    component_index: dict[str, int],
) -> int:
    if not components:
        return 0

    dag: dict[int, set[int]] = {idx: set() for idx in range(len(components))}
    indegree = {idx: 0 for idx in range(len(components))}

    for src_id, nbrs in adj.items():
        src_comp = component_index[src_id]
        for dst_id in nbrs:
            dst_comp = component_index[dst_id]
            if src_comp == dst_comp or dst_comp in dag[src_comp]:
                continue
            dag[src_comp].add(dst_comp)
            indegree[dst_comp] += 1

    queue = deque([idx for idx, deg in indegree.items() if deg == 0])
    best = {idx: 0 for idx in dag}
    longest = 0

    while queue:
        node = queue.popleft()
        longest = max(longest, best[node])
        for nbr in dag[node]:
            best[nbr] = max(best[nbr], best[node] + 1)
            indegree[nbr] -= 1
            if indegree[nbr] == 0:
                queue.append(nbr)

    return longest


def relation_structure_diagnostics(
    relation_out_neighbors: dict[str, set[str]],
    relation_in_neighbors: dict[str, set[str]],
    relation_undirected_neighbors: dict[str, set[str]],
    relation_node_ids: list[str],
    relation_edge_count: int,
    relation_undirected_edge_count: int,
    rng: random.Random,
    distance_source_count: int,
    hyperbolicity_landmarks: int,
    max_hyperbolicity_quadruples: int,
) -> dict[str, object] | None:
    if not relation_node_ids:
        return None

    components = connected_components(relation_undirected_neighbors, relation_node_ids)
    components.sort(key=len, reverse=True)
    largest_component = components[0] if components else []

    sccs, component_index = strongly_connected_components(relation_out_neighbors)
    scc_sizes = sorted((len(component) for component in sccs), reverse=True)
    nontrivial_scc_sizes = [size for size in scc_sizes if size > 1]

    out_degrees = [len(relation_out_neighbors[node_id]) for node_id in relation_node_ids]
    in_degrees = [len(relation_in_neighbors[node_id]) for node_id in relation_node_ids]
    undirected_degrees = [len(relation_undirected_neighbors[node_id]) for node_id in relation_node_ids]

    return {
        "num_nodes": len(relation_node_ids),
        "num_edges": relation_edge_count,
        "undirected_edge_count": relation_undirected_edge_count,
        "weak_component_summary": component_size_summary(components),
        "cycle_rank_undirected": relation_undirected_edge_count - len(relation_node_ids) + len(components),
        "out_degree_summary": summarize_values(out_degrees),
        "in_degree_summary": summarize_values(in_degrees),
        "undirected_degree_summary": summarize_values(undirected_degrees),
        "root_count_out_degree_zero": sum(1 for degree in out_degrees if degree == 0),
        "leaf_count_in_degree_zero": sum(1 for degree in in_degrees if degree == 0),
        "multi_parent_count": sum(1 for degree in out_degrees if degree >= 2),
        "multi_child_count": sum(1 for degree in in_degrees if degree >= 2),
        "scc_count": len(sccs),
        "largest_scc_size": scc_sizes[0] if scc_sizes else 0,
        "nontrivial_scc_count": len(nontrivial_scc_sizes),
        "nontrivial_scc_sizes_top10": nontrivial_scc_sizes[:10],
        "condensation_longest_path": condensation_longest_path(
            relation_out_neighbors,
            sccs,
            component_index,
        ),
        "largest_component_diagnostics": distance_and_hyperbolicity_diagnostics(
            adj=relation_undirected_neighbors,
            component_nodes=largest_component,
            rng=rng,
            distance_source_count=distance_source_count,
            hyperbolicity_landmarks=hyperbolicity_landmarks,
            max_hyperbolicity_quadruples=max_hyperbolicity_quadruples,
        ),
    }


def graph_diagnostics(
    graph_name: str,
    graph_root: Path,
    relation_edge_types: set[str],
    rng_seed: int,
    distance_source_count: int,
    hyperbolicity_landmarks: int,
    max_hyperbolicity_quadruples: int,
) -> dict[str, object]:
    declarations, edges = load_declaration_graph(graph_root)
    base_summary = summarize_graph(declarations, edges)
    effective_relation_edge_types = set(relation_edge_types)
    if not effective_relation_edge_types:
        effective_relation_edge_types = {
            row.get("edge_type", "")
            for row in edges
            if row.get("edge_type", "") and row.get("edge_type", "") != "uses"
        }
    indices = build_graph_indices(
        declarations=declarations,
        edges=edges,
        relation_edge_types=effective_relation_edge_types,
    )

    node_ids = indices["node_ids"]
    out_degrees = [len(indices["out_neighbors"][node_id]) for node_id in node_ids]
    in_degrees = [len(indices["in_neighbors"][node_id]) for node_id in node_ids]
    undirected_degrees = [len(indices["undirected_neighbors"][node_id]) for node_id in node_ids]

    components = connected_components(indices["undirected_neighbors"], node_ids)
    components.sort(key=len, reverse=True)
    largest_component = components[0] if components else []
    rng = random.Random(rng_seed)

    relation_types_detected = sorted(
        edge_type
        for edge_type in indices["edge_type_counts"].keys()
        if edge_type in effective_relation_edge_types
    )

    diagnostics = {
        "graph_name": graph_name,
        "graph_root": str(graph_root),
        "summary": base_summary,
        "edge_type_counts": indices["edge_type_counts"],
        "relation_edge_types": relation_types_detected,
        "out_degree_summary": summarize_values(out_degrees),
        "in_degree_summary": summarize_values(in_degrees),
        "undirected_degree_summary": summarize_values(undirected_degrees),
        "weak_component_summary": component_size_summary(components),
        "cycle_rank_undirected": indices["undirected_edge_count"] - len(node_ids) + len(components),
        "largest_component_diagnostics": distance_and_hyperbolicity_diagnostics(
            adj=indices["undirected_neighbors"],
            component_nodes=largest_component,
            rng=rng,
            distance_source_count=distance_source_count,
            hyperbolicity_landmarks=hyperbolicity_landmarks,
            max_hyperbolicity_quadruples=max_hyperbolicity_quadruples,
        ),
        "relation_structure": relation_structure_diagnostics(
            relation_out_neighbors=indices["relation_out_neighbors"],
            relation_in_neighbors=indices["relation_in_neighbors"],
            relation_undirected_neighbors=indices["relation_undirected_neighbors"],
            relation_node_ids=indices["relation_node_ids"],
            relation_edge_count=indices["relation_edge_count"],
            relation_undirected_edge_count=indices["relation_undirected_edge_count"],
            rng=rng,
            distance_source_count=distance_source_count,
            hyperbolicity_landmarks=hyperbolicity_landmarks,
            max_hyperbolicity_quadruples=max_hyperbolicity_quadruples,
        ),
    }
    return diagnostics


def fmt_float(value: float | None, precision: int = 3) -> str:
    if value is None:
        return "NA"
    return f"{value:.{precision}f}"


def fmt_int(value: int | None) -> str:
    if value is None:
        return "NA"
    return f"{value}"


def build_overview_table(rows: list[dict[str, object]]) -> list[str]:
    lines = [
        "| graph | nodes | edges | giant component | cycle rank | diameter est. | delta/maxdist |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        component_summary = row["weak_component_summary"]
        largest_component = component_summary["largest"]
        total_nodes = row["summary"]["num_declarations"]
        giant_ratio = 0.0 if total_nodes == 0 else largest_component / total_nodes
        largest_diag = row["largest_component_diagnostics"]
        hyper = largest_diag["hyperbolicity_proxy"]
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["graph_name"]),
                    fmt_int(row["summary"]["num_declarations"]),
                    fmt_int(row["summary"]["num_edges"]),
                    f"{largest_component}/{total_nodes} ({giant_ratio:.3f})",
                    fmt_int(row["cycle_rank_undirected"]),
                    fmt_int(largest_diag["diameter_estimate"]),
                    fmt_float(None if hyper is None else hyper["delta_over_diameter_estimate"]),
                ]
            )
            + " |"
        )
    return lines


def build_relation_table(rows: list[dict[str, object]]) -> list[str]:
    lines = [
        "| graph | relation nodes | relation edges | largest SCC | longest chain | multi-parent | delta/maxdist |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        relation = row["relation_structure"]
        if relation is None:
            lines.append(f"| {row['graph_name']} | 0 | 0 | 0 | 0 | 0 | NA |")
            continue
        relation_hyper = relation["largest_component_diagnostics"]["hyperbolicity_proxy"]
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["graph_name"]),
                    fmt_int(relation["num_nodes"]),
                    fmt_int(relation["num_edges"]),
                    fmt_int(relation["largest_scc_size"]),
                    fmt_int(relation["condensation_longest_path"]),
                    fmt_int(relation["multi_parent_count"]),
                    fmt_float(None if relation_hyper is None else relation_hyper["delta_over_diameter_estimate"]),
                ]
            )
            + " |"
        )
    return lines


def build_interpretation(rows: list[dict[str, object]]) -> list[str]:
    lines = ["## Interpretation", ""]
    for row in rows:
        graph_name = str(row["graph_name"])
        largest_diag = row["largest_component_diagnostics"]
        hyper = largest_diag["hyperbolicity_proxy"]
        relation = row["relation_structure"]
        lines.append(f"### {graph_name}")
        lines.append(
            "- Full graph: "
            f"{row['summary']['num_declarations']} nodes / {row['summary']['num_edges']} edges, "
            f"giant component {row['weak_component_summary']['largest']} nodes, "
            f"undirected cycle rank {row['cycle_rank_undirected']}."
        )
        if hyper is not None:
            lines.append(
                "- Full graph tree-likeness proxy: "
                f"diameter estimate {fmt_int(largest_diag['diameter_estimate'])}, "
                f"hyperbolicity delta/maxdist {fmt_float(hyper['delta_over_diameter_estimate'])}, "
                f"delta/mean-pair {fmt_float(hyper['delta_over_mean_pair_distance'])}."
            )
        if relation is None:
            lines.append("- No dedicated hierarchy edge types were detected in this graph.")
        else:
            relation_hyper = relation["largest_component_diagnostics"]["hyperbolicity_proxy"]
            lines.append(
                "- Relation-only layer: "
                f"{relation['num_nodes']} nodes / {relation['num_edges']} edges, "
                f"largest SCC {relation['largest_scc_size']}, "
                f"nontrivial SCC count {relation['nontrivial_scc_count']}, "
                f"condensation longest path {relation['condensation_longest_path']}."
            )
            lines.append(
                "- Relation branching: "
                f"multi-parent nodes {relation['multi_parent_count']}, "
                f"roots(out-degree=0) {relation['root_count_out_degree_zero']}, "
                f"leaves(in-degree=0) {relation['leaf_count_in_degree_zero']}."
            )
            if relation_hyper is not None:
                lines.append(
                    "- Relation tree-likeness proxy: "
                    f"delta/maxdist {fmt_float(relation_hyper['delta_over_diameter_estimate'])}, "
                    f"delta/mean-pair {fmt_float(relation_hyper['delta_over_mean_pair_distance'])}."
                )
        lines.append("")
    return lines


def build_report(config: dict, rows: list[dict[str, object]]) -> str:
    lines = [
        "# Graph Structure Diagnostics",
        "",
        f"- Seed: {config['seed']}",
        f"- Distance sample sources: {config['distance_sample_sources']}",
        f"- Hyperbolicity landmarks: {config['hyperbolicity_landmarks']}",
        f"- Max hyperbolicity quadruples: {config['max_hyperbolicity_quadruples']}",
        "",
        "## Overview",
        "",
        *build_overview_table(rows),
        "",
        "## Relation Layer",
        "",
        *build_relation_table(rows),
        "",
        *build_interpretation(rows),
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    workspace_root = Path.cwd().resolve()

    output_root = Path(config["output_root"])
    if not output_root.is_absolute():
        output_root = (workspace_root / output_root).resolve()
    ensure_dir(output_root)
    ensure_dir(output_root / "graphs")

    rows: list[dict[str, object]] = []
    for graph_cfg in config["graphs"]:
        graph_root = Path(graph_cfg["graph_root"])
        if not graph_root.is_absolute():
            graph_root = (workspace_root / graph_root).resolve()

        relation_edge_types = set(graph_cfg.get("relation_edge_types", []))

        diagnostics = graph_diagnostics(
            graph_name=str(graph_cfg["name"]),
            graph_root=graph_root,
            relation_edge_types=relation_edge_types,
            rng_seed=int(config["seed"]) + len(rows) * 1000,
            distance_source_count=int(config["distance_sample_sources"]),
            hyperbolicity_landmarks=int(config["hyperbolicity_landmarks"]),
            max_hyperbolicity_quadruples=int(config["max_hyperbolicity_quadruples"]),
        )

        rows.append(diagnostics)
        write_json(output_root / "graphs" / f"{graph_cfg['name']}.json", diagnostics)
        print(
            f"[done] diagnostics: {graph_cfg['name']} "
            f"nodes={diagnostics['summary']['num_declarations']} "
            f"edges={diagnostics['summary']['num_edges']}"
        )

    report = build_report(config, rows)
    (output_root / "report.md").write_text(report, encoding="utf-8")
    write_json(output_root / "summary.json", {"config": config, "graphs": rows})
    print(f"[done] report: {output_root / 'report.md'}")
    print(f"[done] summary: {output_root / 'summary.json'}")


if __name__ == "__main__":
    main()
