from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_tsv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def short_decl_name(name: str) -> str:
    return name.split(".")[-1]


def build_name_indices(rows: list[dict[str, str]]) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]], dict[str, list[dict[str, str]]]]:
    exact: dict[str, dict[str, str]] = {}
    short_to_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        exact[row["decl_name"]] = row
        short_to_rows[short_decl_name(row["decl_name"])].append(row)

    unique_short = {name: candidates[0] for name, candidates in short_to_rows.items() if len(candidates) == 1}
    ambiguous_short = {name: candidates for name, candidates in short_to_rows.items() if len(candidates) > 1}
    return exact, unique_short, ambiguous_short


def resolve_name(
    name: str,
    exact_names: dict[str, dict[str, str]],
    unique_short_names: dict[str, dict[str, str]],
    ambiguous_short_names: dict[str, list[dict[str, str]]],
) -> tuple[str, dict[str, str] | list[dict[str, str]] | None]:
    if name in exact_names:
        return "exact", exact_names[name]
    short = short_decl_name(name)
    if short in unique_short_names:
        return "unique_short", unique_short_names[short]
    if short in ambiguous_short_names:
        return "ambiguous_short", ambiguous_short_names[short]
    return "missing", None


def kind_of_match(match: dict[str, str] | list[dict[str, str]] | None) -> str | list[str] | None:
    if match is None:
        return None
    if isinstance(match, list):
        return sorted({row["decl_kind"] for row in match})
    return match["decl_kind"]


def line_info(index_by_name: dict[str, dict[str, str]], name: str) -> dict[str, str] | None:
    row = index_by_name.get(name)
    if row is None:
        return None
    return {
        "decl_kind": row.get("decl_kind", ""),
        "module_name": row.get("module_name", ""),
        "line_start": row.get("line_start", ""),
        "line_end": row.get("line_end", ""),
    }


def build_markdown_report(summary: dict[str, Any]) -> str:
    lines = [
        "# Precise Hierarchy Mismatch Audit",
        "",
        f"- Relation rows: {summary['total_relations']}",
        f"- Matched exact relations kept: {summary['matched_edges']}",
        f"- Dropped relations: {summary['dropped_relations']}",
        f"- Duplicate relations after resolution: {summary['duplicate_relations']}",
        "",
        "## Drop Breakdown",
        "",
        "| reason | count | share |",
        "| --- | ---: | ---: |",
    ]

    dropped_total = max(1, summary["dropped_relations"])
    for reason, count in summary["drop_reason_counts"].items():
        lines.append(f"| {reason} | {count} | {count / dropped_total:.3f} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `src_in_nodes_tsv_but_missing_from_index_and_trace` means the Lean meta exporter can see the declaration as a hierarchy node, but the trace pipeline has neither a declaration range nor a normalized declaration row for it. These are mostly generated declarations such as `*_sizeOf_inst` and helper coercion projections.",
            "- `src_in_index_but_missing_from_normalized_trace` means the declaration exists in the declaration index with a source range, but it still failed to enter the normalized trace. This is the most actionable bucket because it points to trace coverage or normalization gaps.",
            "- `src_ambiguous_short` means the declaration exists in the declaration index, but the normalized trace only retained short-name candidates such as `instInhabited` / `instBEq` without enough namespace context to recover the fully qualified source declaration.",
            "",
            "## Top Examples",
            "",
        ]
    )

    for reason, rows in summary["drop_reason_examples"].items():
        lines.append(f"### {reason}")
        if not rows:
            lines.append("- No examples recorded.")
            lines.append("")
            continue
        for row in rows[:8]:
            line = (
                f"- `{row['src_name']}` -> `{row['dst_name']}` "
                f"({row['relation_type']}); "
                f"src_mode={row['src_mode']}, dst_mode={row['dst_mode']}"
            )
            if row.get("src_index_info"):
                idx = row["src_index_info"]
                line += f", index={idx['module_name']}:{idx['line_start']}"
            if row.get("src_short_candidates"):
                line += f", short_candidates={', '.join(row['src_short_candidates'][:6])}"
            lines.append(line)
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit dropped exact relations in the precise hierarchy subgraph.")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    workspace_root = Path.cwd().resolve()

    closed_world_graph_root = (workspace_root / config["closed_world_graph_root"]).resolve()
    precise_graph_root = (workspace_root / config["precise_graph_root"]).resolve()
    relation_edges_path = (workspace_root / config["relation_edges_path"]).resolve()
    relation_nodes_path = (workspace_root / config["relation_nodes_path"]).resolve()
    declaration_index_path = (workspace_root / config["declaration_index_path"]).resolve()
    normalized_trace_path = (workspace_root / config["normalized_trace_path"]).resolve()
    output_root = (workspace_root / config["output_root"]).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    closed_world_rows = read_csv_rows(closed_world_graph_root / "declarations.csv")
    precise_rows = read_csv_rows(precise_graph_root / "declarations.csv")
    relation_rows = read_tsv_rows(relation_edges_path)
    relation_node_rows = read_tsv_rows(relation_nodes_path)
    declaration_index_rows = read_tsv_rows(declaration_index_path)
    normalized_rows = [
        json.loads(line)
        for line in normalized_trace_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    precise_exact, precise_unique_short, precise_ambiguous_short = build_name_indices(precise_rows)
    class_like_rows = [row for row in precise_rows if row.get("decl_kind", "") in {"class", "structure"}]
    class_exact, class_unique_short, class_ambiguous_short = build_name_indices(class_like_rows)
    closed_exact, closed_unique_short, closed_ambiguous_short = build_name_indices(closed_world_rows)

    relation_node_names = {row["decl_name"] for row in relation_node_rows}
    declaration_index_by_name = {row["decl_name"]: row for row in declaration_index_rows}
    normalized_decl_names = {row["decl_name"] for row in normalized_rows}
    normalized_short_candidates: dict[str, set[str]] = defaultdict(set)
    for row in normalized_rows:
        normalized_short_candidates[short_decl_name(row["decl_name"])].add(row["decl_name"])

    drop_reason_counts: Counter[str] = Counter()
    relation_reason_counts: Counter[str] = Counter()
    duplicate_relations = 0
    matched_edges = 0
    seen_edge_ids: set[str] = set()
    drop_reason_examples: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in relation_rows:
        relation_type = row.get("relation_type", "")
        edge_type = None
        if relation_type == "extends":
            edge_type = "extends"
        elif relation_type == "instance_of":
            edge_type = "instance_of"

        src_mode, src_match = resolve_name(
            row["src_name"],
            precise_exact,
            precise_unique_short,
            precise_ambiguous_short,
        )
        dst_mode, dst_match = resolve_name(
            row["dst_name"],
            class_exact,
            class_unique_short,
            class_ambiguous_short,
        )

        if edge_type and src_mode in {"exact", "unique_short"} and dst_mode in {"exact", "unique_short"}:
            src_row = src_match if isinstance(src_match, dict) else None
            dst_row = dst_match if isinstance(dst_match, dict) else None
            if src_row is not None and dst_row is not None:
                edge_id = f"{src_row['declaration_id']}--{edge_type}--{dst_row['declaration_id']}"
                if src_row["declaration_id"] == dst_row["declaration_id"]:
                    reason = "self_loop"
                elif edge_id in seen_edge_ids:
                    duplicate_relations += 1
                    reason = "duplicate_after_resolution"
                else:
                    seen_edge_ids.add(edge_id)
                    matched_edges += 1
                    relation_reason_counts[f"{relation_type}::matched"] += 1
                    continue
            else:
                reason = "unexpected_non_dict_resolution"
        elif edge_type is None:
            reason = "unknown_relation_type"
        elif src_mode == "ambiguous_short":
            reason = "src_ambiguous_short"
        elif dst_mode == "ambiguous_short":
            reason = "dst_ambiguous_short"
        elif src_mode == "missing":
            if row["src_name"] in declaration_index_by_name:
                if row["src_name"] in normalized_decl_names:
                    reason = "src_in_index_and_normalized_but_not_precise_graph"
                else:
                    reason = "src_in_index_but_missing_from_normalized_trace"
            elif row["src_name"] in relation_node_names:
                reason = "src_in_nodes_tsv_but_missing_from_index_and_trace"
            else:
                reason = "src_missing_from_nodes_tsv_and_index"
        elif dst_mode == "missing":
            closed_mode, closed_match = resolve_name(
                row["dst_name"],
                closed_exact,
                closed_unique_short,
                closed_ambiguous_short,
            )
            if closed_mode in {"exact", "unique_short"}:
                closed_row = closed_match if isinstance(closed_match, dict) else None
                kind = "" if closed_row is None else closed_row.get("decl_kind", "")
                reason = f"dst_present_but_not_class_like:{kind}"
            else:
                reason = "dst_missing_from_closed_world"
        else:
            reason = "other"

        drop_reason_counts[reason] += 1
        relation_reason_counts[f"{relation_type}::{reason}"] += 1
        if len(drop_reason_examples[reason]) < int(config.get("max_examples_per_reason", 12)):
            drop_reason_examples[reason].append(
                {
                    "src_name": row["src_name"],
                    "dst_name": row["dst_name"],
                    "relation_type": relation_type,
                    "src_mode": src_mode,
                    "dst_mode": dst_mode,
                    "src_in_relation_nodes_tsv": row["src_name"] in relation_node_names,
                    "src_in_declaration_index": row["src_name"] in declaration_index_by_name,
                    "src_in_normalized_trace": row["src_name"] in normalized_decl_names,
                    "src_index_info": line_info(declaration_index_by_name, row["src_name"]),
                    "src_short_candidates": sorted(normalized_short_candidates.get(short_decl_name(row["src_name"]), set()))[:12],
                    "dst_closed_world_kind": kind_of_match(
                        resolve_name(
                            row["dst_name"],
                            closed_exact,
                            closed_unique_short,
                            closed_ambiguous_short,
                        )[1]
                    ),
                }
            )

    summary = {
        "total_relations": len(relation_rows),
        "matched_edges": matched_edges,
        "dropped_relations": sum(drop_reason_counts.values()),
        "duplicate_relations": duplicate_relations,
        "drop_reason_counts": dict(sorted(drop_reason_counts.items())),
        "relation_reason_counts": dict(sorted(relation_reason_counts.items())),
        "drop_reason_examples": drop_reason_examples,
    }

    (output_root / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_root / "report.md").write_text(
        build_markdown_report(summary),
        encoding="utf-8",
    )

    print(f"[done] matched edges: {matched_edges}")
    print(f"[done] dropped relations: {summary['dropped_relations']}")
    print(f"[done] duplicate relations: {duplicate_relations}")
    print(f"[done] report: {output_root / 'report.md'}")
    print(f"[done] summary: {output_root / 'summary.json'}")


if __name__ == "__main__":
    main()
