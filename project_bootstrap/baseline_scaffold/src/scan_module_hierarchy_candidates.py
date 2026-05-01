from __future__ import annotations

import argparse
import csv
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

from common import ensure_dir, load_config, load_declaration_graph, summarize_graph, write_json
from run_graph_diagnostics import (
    build_graph_indices,
    component_size_summary,
    connected_components,
    distance_and_hyperbolicity_diagnostics,
    relation_structure_diagnostics,
    summarize_values,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan module-level hierarchy candidates from a declaration graph.")
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


def choose_scope_value(row: dict, field_priority: list[str]) -> str:
    for field_name in field_priority:
        value = str(row.get(field_name, "")).strip()
        if value:
            return value
    return ""


def scope_prefix(scope_value: str, depth: int) -> str:
    parts = [part for part in scope_value.split(".") if part]
    if not parts:
        return ""
    return ".".join(parts[:depth])


def matches_prefix_allowlist(prefix: str, allowlist: list[str]) -> bool:
    if not allowlist:
        return True
    return any(prefix == item or prefix.startswith(item + ".") for item in allowlist)


def candidate_slug(depth: int, prefix: str) -> str:
    safe = prefix.replace(".", "_").replace("/", "_").replace("\\", "_")
    return f"d{depth}_{safe}"


def write_csv_rows(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def build_parent_adjacency(edges: list[dict], relation_edge_types: set[str]) -> dict[str, set[str]]:
    parents: dict[str, set[str]] = defaultdict(set)
    for row in edges:
        if row.get("edge_type", "") not in relation_edge_types:
            continue
        parents[row["src_id"]].add(row["dst_id"])
    return parents


def ancestor_closure(seed_ids: set[str], parent_adj: dict[str, set[str]]) -> set[str]:
    retained = set(seed_ids)
    frontier = list(seed_ids)
    while frontier:
        node_id = frontier.pop()
        for parent_id in parent_adj.get(node_id, set()):
            if parent_id in retained:
                continue
            retained.add(parent_id)
            frontier.append(parent_id)
    return retained


def compute_subset_diagnostics(
    graph_name: str,
    declarations: list[dict],
    edges: list[dict],
    relation_edge_types: set[str],
    rng_seed: int,
    distance_source_count: int,
    hyperbolicity_landmarks: int,
    max_hyperbolicity_quadruples: int,
) -> dict[str, object]:
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
    rng = random.Random(rng_seed)
    node_ids = indices["node_ids"]
    out_degrees = [len(indices["out_neighbors"][node_id]) for node_id in node_ids]
    in_degrees = [len(indices["in_neighbors"][node_id]) for node_id in node_ids]
    undirected_degrees = [len(indices["undirected_neighbors"][node_id]) for node_id in node_ids]

    components = connected_components(indices["undirected_neighbors"], node_ids)
    components.sort(key=len, reverse=True)
    largest_component = components[0] if components else []

    relation_types_detected = sorted(
        edge_type
        for edge_type in indices["edge_type_counts"].keys()
        if edge_type in effective_relation_edge_types
    )

    return {
        "graph_name": graph_name,
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


def candidate_score(relation: dict | None, edge_type_counts: dict[str, int]) -> float:
    if relation is None or relation.get("num_nodes", 0) == 0:
        return 0.0
    relation_nodes = int(relation["num_nodes"])
    largest_component = int(relation["weak_component_summary"]["largest"])
    longest_chain = int(relation["condensation_longest_path"])
    leaf_ratio = 1.0 if relation_nodes == 0 else float(relation["leaf_count_in_degree_zero"]) / relation_nodes
    extends_edges = int(edge_type_counts.get("extends", 0))
    relation_edges = int(relation["num_edges"])
    extends_share = 0.0 if relation_edges == 0 else extends_edges / relation_edges
    return (
        longest_chain
        * math.log2(largest_component + 1)
        * max(0.0, 1.0 - leaf_ratio)
        * (1.0 + extends_share)
    )


def format_float(value: float | None, precision: int = 3) -> str:
    if value is None:
        return "NA"
    return f"{value:.{precision}f}"


def build_report(config: dict, candidates_by_depth: dict[int, list[dict]]) -> str:
    lines = [
        "# Module Hierarchy Candidate Scan",
        "",
        f"- Graph root: {config['graph_root']}",
        f"- Candidate depths: {config['candidate_depths']}",
        f"- Candidate prefix allowlist: {config.get('candidate_prefix_allowlist', [])}",
        f"- Module field priority: {config['module_field_priority']}",
        f"- Ancestor closure on relation edges: {bool(config.get('expand_to_ancestor_closure', True))}",
        "",
    ]

    for depth in config["candidate_depths"]:
        rows = candidates_by_depth.get(int(depth), [])
        lines.extend(
            [
                f"## Depth {depth}",
                "",
                "| prefix | seed decls | retained decls | relation nodes | relation edges | extends | longest chain | giant relation comp | leaf ratio | score |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        if not rows:
            lines.append("| (none) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | NA | 0.000 |")
            lines.append("")
            continue

        top_k = min(int(config.get("top_k_per_depth", 20)), len(rows))
        for row in rows[:top_k]:
            relation = row["diagnostics"]["relation_structure"]
            giant_component = 0 if relation is None else relation["weak_component_summary"]["largest"]
            leaf_ratio = None
            if relation is not None and relation["num_nodes"]:
                leaf_ratio = relation["leaf_count_in_degree_zero"] / relation["num_nodes"]
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(row["prefix"]),
                        str(row["seed_declarations"]),
                        str(row["retained_declarations"]),
                        str(0 if relation is None else relation["num_nodes"]),
                        str(0 if relation is None else relation["num_edges"]),
                        str(row["diagnostics"]["edge_type_counts"].get("extends", 0)),
                        str(0 if relation is None else relation["condensation_longest_path"]),
                        str(giant_component),
                        format_float(leaf_ratio),
                        format_float(row["hierarchy_score"]),
                    ]
                )
                + " |"
            )

        internal_rows = [row for row in rows if row["is_internal"]]
        lines.extend(["", f"### Depth {depth} Internal-Only Highlights", ""])
        if not internal_rows:
            lines.append("- No internal candidates passed the thresholds.")
            lines.append("")
            continue

        for row in internal_rows[: min(10, len(internal_rows))]:
            relation = row["diagnostics"]["relation_structure"]
            leaf_ratio = None
            if relation is not None and relation["num_nodes"]:
                leaf_ratio = relation["leaf_count_in_degree_zero"] / relation["num_nodes"]
            lines.append(
                "- "
                f"`{row['prefix']}`: chain={0 if relation is None else relation['condensation_longest_path']}, "
                f"relation_nodes={0 if relation is None else relation['num_nodes']}, "
                f"relation_edges={0 if relation is None else relation['num_edges']}, "
                f"largest_component={0 if relation is None else relation['weak_component_summary']['largest']}, "
                f"leaf_ratio={format_float(leaf_ratio)}, "
                f"score={format_float(row['hierarchy_score'])}."
            )
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    workspace_root = Path.cwd().resolve()

    graph_root = Path(config["graph_root"])
    if not graph_root.is_absolute():
        graph_root = (workspace_root / graph_root).resolve()

    output_root = Path(config["output_root"])
    if not output_root.is_absolute():
        output_root = (workspace_root / output_root).resolve()
    ensure_dir(output_root)
    ensure_dir(output_root / "candidate_graphs")

    declarations, edges = load_declaration_graph(graph_root)
    decl_by_id = {row["declaration_id"]: row for row in declarations}

    relation_edge_types = {str(edge_type) for edge_type in config.get("relation_edge_types", []) if str(edge_type).strip()}
    if not relation_edge_types:
        relation_edge_types = {
            row.get("edge_type", "")
            for row in edges
            if row.get("edge_type", "") and row.get("edge_type", "") != "uses"
        }

    field_priority = [str(field_name) for field_name in config.get("module_field_priority", ["module_name", "namespace"])]
    candidate_depths = [int(depth) for depth in config.get("candidate_depths", [2, 3])]
    candidate_prefix_allowlist = [str(item) for item in config.get("candidate_prefix_allowlist", []) if str(item).strip()]
    internal_prefixes = [str(item) for item in config.get("internal_prefixes", []) if str(item).strip()]
    min_seed_declarations = int(config.get("min_seed_declarations", 16))
    min_seed_relation_nodes = int(config.get("min_seed_relation_nodes", 8))
    min_retained_relation_edges = int(config.get("min_retained_relation_edges", 8))
    top_k_per_depth = int(config.get("top_k_per_depth", 20))
    materialize_top_k_per_depth = int(config.get("materialize_top_k_per_depth", 5))
    expand_to_ancestor_closure = bool(config.get("expand_to_ancestor_closure", True))

    parent_adj = build_parent_adjacency(edges, relation_edge_types)
    all_edge_fields = list(edges[0].keys()) if edges else ["edge_id", "src_id", "dst_id", "edge_type"]
    all_decl_fields = list(declarations[0].keys()) if declarations else ["declaration_id"]

    prefix_to_seed_ids_by_depth: dict[int, dict[str, set[str]]] = {depth: defaultdict(set) for depth in candidate_depths}
    for row in declarations:
        scope_value = choose_scope_value(row, field_priority)
        if not scope_value:
            continue
        for depth in candidate_depths:
            prefix = scope_prefix(scope_value, depth)
            if not prefix or not matches_prefix_allowlist(prefix, candidate_prefix_allowlist):
                continue
            prefix_to_seed_ids_by_depth[depth][prefix].add(row["declaration_id"])

    candidates_by_depth: dict[int, list[dict]] = {}
    ranking_rows: list[dict[str, object]] = []

    for depth in candidate_depths:
        candidate_rows: list[dict] = []
        for prefix, seed_ids in sorted(prefix_to_seed_ids_by_depth[depth].items()):
            seed_declarations = [decl_by_id[node_id] for node_id in seed_ids if node_id in decl_by_id]
            if len(seed_declarations) < min_seed_declarations:
                continue

            retained_ids = ancestor_closure(seed_ids, parent_adj) if expand_to_ancestor_closure else set(seed_ids)
            retained_declarations = [decl_by_id[node_id] for node_id in retained_ids if node_id in decl_by_id]
            retained_id_set = {row["declaration_id"] for row in retained_declarations}
            retained_edges = [
                row for row in edges
                if row["src_id"] in retained_id_set and row["dst_id"] in retained_id_set
            ]

            diagnostics = compute_subset_diagnostics(
                graph_name=f"d{depth}:{prefix}",
                declarations=retained_declarations,
                edges=retained_edges,
                relation_edge_types=relation_edge_types,
                rng_seed=int(config.get("seed", 42)) + depth * 1000 + len(candidate_rows),
                distance_source_count=int(config.get("distance_sample_sources", 16)),
                hyperbolicity_landmarks=int(config.get("hyperbolicity_landmarks", 12)),
                max_hyperbolicity_quadruples=int(config.get("max_hyperbolicity_quadruples", 256)),
            )

            relation = diagnostics["relation_structure"]
            relation_nodes = 0 if relation is None else int(relation["num_nodes"])
            relation_edges = 0 if relation is None else int(relation["num_edges"])
            seed_relation_nodes = sum(
                1
                for row in seed_declarations
                if row["declaration_id"] in retained_id_set
                and any(
                    edge_row.get("edge_type", "") in relation_edge_types
                    and (edge_row["src_id"] == row["declaration_id"] or edge_row["dst_id"] == row["declaration_id"])
                    for edge_row in retained_edges
                )
            )
            if seed_relation_nodes < min_seed_relation_nodes or relation_edges < min_retained_relation_edges:
                continue

            score = candidate_score(relation, diagnostics["edge_type_counts"])
            is_internal = matches_prefix_allowlist(prefix, internal_prefixes)
            row = {
                "depth": depth,
                "prefix": prefix,
                "seed_declarations": len(seed_declarations),
                "seed_relation_nodes": seed_relation_nodes,
                "retained_declarations": len(retained_declarations),
                "retained_edges": len(retained_edges),
                "ancestor_added_nodes": len(retained_id_set - seed_ids),
                "is_internal": is_internal,
                "hierarchy_score": score,
                "diagnostics": diagnostics,
            }
            candidate_rows.append(row)

        candidate_rows.sort(
            key=lambda row: (
                -int(row["diagnostics"]["relation_structure"]["condensation_longest_path"]) if row["diagnostics"]["relation_structure"] is not None else 0,
                -float(row["hierarchy_score"]),
                -int(row["diagnostics"]["relation_structure"]["weak_component_summary"]["largest"]) if row["diagnostics"]["relation_structure"] is not None else 0,
                -int(row["diagnostics"]["relation_structure"]["num_edges"]) if row["diagnostics"]["relation_structure"] is not None else 0,
                str(row["prefix"]),
            )
        )
        candidates_by_depth[depth] = candidate_rows

        for row in candidate_rows:
            relation = row["diagnostics"]["relation_structure"]
            leaf_ratio = None
            giant_component = None
            longest_chain = None
            relation_nodes = None
            relation_edges = None
            if relation is not None:
                relation_nodes = int(relation["num_nodes"])
                relation_edges = int(relation["num_edges"])
                giant_component = int(relation["weak_component_summary"]["largest"])
                longest_chain = int(relation["condensation_longest_path"])
                leaf_ratio = (
                    None
                    if relation_nodes == 0
                    else float(relation["leaf_count_in_degree_zero"]) / relation_nodes
                )
            ranking_rows.append(
                {
                    "depth": row["depth"],
                    "prefix": row["prefix"],
                    "is_internal": row["is_internal"],
                    "seed_declarations": row["seed_declarations"],
                    "seed_relation_nodes": row["seed_relation_nodes"],
                    "retained_declarations": row["retained_declarations"],
                    "retained_edges": row["retained_edges"],
                    "ancestor_added_nodes": row["ancestor_added_nodes"],
                    "relation_nodes": relation_nodes,
                    "relation_edges": relation_edges,
                    "extends_edges": row["diagnostics"]["edge_type_counts"].get("extends", 0),
                    "instance_of_edges": row["diagnostics"]["edge_type_counts"].get("instance_of", 0),
                    "uses_edges": row["diagnostics"]["edge_type_counts"].get("uses", 0),
                    "largest_relation_component": giant_component,
                    "longest_chain": longest_chain,
                    "leaf_ratio": leaf_ratio,
                    "hierarchy_score": row["hierarchy_score"],
                }
            )

        for rank, row in enumerate(candidate_rows[:materialize_top_k_per_depth], start=1):
            relation = row["diagnostics"]["relation_structure"]
            if relation is None:
                continue
            slug = candidate_slug(depth, str(row["prefix"]))
            candidate_root = output_root / "candidate_graphs" / f"{rank:02d}_{slug}"
            ensure_dir(candidate_root)

            seed_prefix = str(row["prefix"])
            seed_ids = prefix_to_seed_ids_by_depth[depth][seed_prefix]
            retained_ids = ancestor_closure(seed_ids, parent_adj) if expand_to_ancestor_closure else set(seed_ids)
            retained_declarations = [decl_by_id[node_id] for node_id in retained_ids if node_id in decl_by_id]
            retained_id_set = {item["declaration_id"] for item in retained_declarations}
            retained_edges = [
                edge_row for edge_row in edges
                if edge_row["src_id"] in retained_id_set and edge_row["dst_id"] in retained_id_set
            ]

            write_csv_rows(candidate_root / "declarations.csv", retained_declarations, all_decl_fields)
            write_csv_rows(candidate_root / "edges.csv", retained_edges, all_edge_fields)
            write_json(
                candidate_root / "stats.json",
                {
                    "rank": rank,
                    "depth": depth,
                    "prefix": row["prefix"],
                    "seed_declarations": row["seed_declarations"],
                    "seed_relation_nodes": row["seed_relation_nodes"],
                    "retained_declarations": row["retained_declarations"],
                    "retained_edges": row["retained_edges"],
                    "ancestor_added_nodes": row["ancestor_added_nodes"],
                    "is_internal": row["is_internal"],
                    "hierarchy_score": row["hierarchy_score"],
                    "diagnostics": row["diagnostics"],
                },
            )

    report = build_report(config, candidates_by_depth)
    (output_root / "report.md").write_text(report, encoding="utf-8")
    write_json(output_root / "summary.json", {"config": config, "candidates_by_depth": candidates_by_depth})

    ranking_fields = [
        "depth",
        "prefix",
        "is_internal",
        "seed_declarations",
        "seed_relation_nodes",
        "retained_declarations",
        "retained_edges",
        "ancestor_added_nodes",
        "relation_nodes",
        "relation_edges",
        "extends_edges",
        "instance_of_edges",
        "uses_edges",
        "largest_relation_component",
        "longest_chain",
        "leaf_ratio",
        "hierarchy_score",
    ]
    write_csv_rows(output_root / "ranking.csv", ranking_rows, ranking_fields)

    for depth in candidate_depths:
        print(f"[done] depth {depth}: {len(candidates_by_depth.get(depth, []))} candidates")
    print(f"[done] report: {output_root / 'report.md'}")
    print(f"[done] summary: {output_root / 'summary.json'}")
    print(f"[done] ranking: {output_root / 'ranking.csv'}")


if __name__ == "__main__":
    main()
