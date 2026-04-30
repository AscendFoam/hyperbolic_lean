from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


IDENT_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_'.]*")
EXTENDS_PATTERN = re.compile(
    r"\b(?:class|structure)\b.*?\bextends\b(?P<parents>.*?)(?:\bwhere\b|:=|$)",
    re.IGNORECASE | re.DOTALL,
)
INSTANCE_HEAD_PATTERN = re.compile(
    r"\binstance\b.*?:\s*(?P<head>.*?)(?:\bwhere\b|:=|$)",
    re.IGNORECASE | re.DOTALL,
)


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_tsv_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def normalize_text(text: str) -> str:
    return (text or "").replace("\n", " ").replace("\r", " ").strip()


def short_decl_name(decl_name: str) -> str:
    return decl_name.split(".")[-1]


def build_name_indices(rows: list[dict]) -> tuple[dict[str, str], dict[str, str]]:
    exact: dict[str, str] = {}
    short_to_ids: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        exact[row["decl_name"]] = row["declaration_id"]
        short_to_ids[short_decl_name(row["decl_name"])].add(row["declaration_id"])

    unique_short: dict[str, str] = {}
    for name, ids in short_to_ids.items():
        if len(ids) == 1:
            unique_short[name] = next(iter(ids))
    return exact, unique_short


def resolve_identifier(token: str, exact_names: dict[str, str], unique_short_names: dict[str, str]) -> str | None:
    if token in exact_names:
        return exact_names[token]
    return unique_short_names.get(token)


def resolve_relation_decl_name(name: str, exact_names: dict[str, str], unique_short_names: dict[str, str]) -> str | None:
    if name in exact_names:
        return exact_names[name]
    return unique_short_names.get(short_decl_name(name))


def infer_extends_targets(
    row: dict,
    exact_names: dict[str, str],
    unique_short_names: dict[str, str],
) -> set[str]:
    text = normalize_text(row.get("signature_text", ""))
    if not text:
        return set()
    match = EXTENDS_PATTERN.search(text)
    if not match:
        return set()
    parents_text = match.group("parents")
    targets: set[str] = set()
    for token in IDENT_PATTERN.findall(parents_text):
        resolved = resolve_identifier(token, exact_names, unique_short_names)
        if resolved and resolved != row["declaration_id"]:
            targets.add(resolved)
    return targets


def infer_instance_targets(
    row: dict,
    exact_names: dict[str, str],
    unique_short_names: dict[str, str],
) -> set[str]:
    text = " ".join(
        [
            normalize_text(row.get("signature_text", "")),
            normalize_text(row.get("body_text", "")),
        ]
    ).strip()
    if not text:
        return set()
    match = INSTANCE_HEAD_PATTERN.search(text)
    if not match:
        return set()
    head = match.group("head")
    targets: set[str] = set()
    for token in IDENT_PATTERN.findall(head):
        resolved = resolve_identifier(token, exact_names, unique_short_names)
        if resolved and resolved != row["declaration_id"]:
            targets.add(resolved)
    return targets


def build_edge_row(src_id: str, dst_id: str, edge_type: str, source_commit: str, evidence_source: str) -> dict:
    return {
        "edge_id": f"{src_id}--{edge_type}--{dst_id}",
        "src_id": src_id,
        "dst_id": dst_id,
        "edge_type": edge_type,
        "evidence_source": evidence_source,
        "weight": 1.0,
        "is_direct": True,
        "source_commit": source_commit,
    }


def add_exact_relation_edges(
    relation_rows: list[dict],
    src_exact_names: dict[str, str],
    src_unique_short_names: dict[str, str],
    dst_exact_names: dict[str, str],
    dst_unique_short_names: dict[str, str],
    source_commit: str,
    add_extends_edges: bool,
    add_instance_of_edges: bool,
    extends_edge_type: str,
    instance_of_edge_type: str,
    kept_edges: list[dict],
    seen_edge_ids: set[str],
    edge_type_counts: Counter[str],
) -> dict[str, int]:
    added_extends = 0
    added_instance_of = 0
    skipped_missing_nodes = 0
    skipped_disabled_type = 0

    for row in relation_rows:
        relation_type = row.get("relation_type", "")
        edge_type = None
        if relation_type == "extends":
            if add_extends_edges:
                edge_type = extends_edge_type
            else:
                skipped_disabled_type += 1
                continue
        elif relation_type == "instance_of":
            if add_instance_of_edges:
                edge_type = instance_of_edge_type
            else:
                skipped_disabled_type += 1
                continue
        else:
            skipped_disabled_type += 1
            continue

        src_id = resolve_relation_decl_name(
            row.get("src_name", ""),
            exact_names=src_exact_names,
            unique_short_names=src_unique_short_names,
        )
        dst_id = resolve_relation_decl_name(
            row.get("dst_name", ""),
            exact_names=dst_exact_names,
            unique_short_names=dst_unique_short_names,
        )
        if not src_id or not dst_id or src_id == dst_id:
            skipped_missing_nodes += 1
            continue

        edge = build_edge_row(
            src_id=src_id,
            dst_id=dst_id,
            edge_type=edge_type,
            source_commit=source_commit,
            evidence_source=row.get("evidence_source", "lean_meta_exact"),
        )
        if edge["edge_id"] in seen_edge_ids:
            continue
        seen_edge_ids.add(edge["edge_id"])
        kept_edges.append(edge)
        edge_type_counts[edge["edge_type"]] += 1
        if relation_type == "extends":
            added_extends += 1
        elif relation_type == "instance_of":
            added_instance_of += 1

    return {
        "exact_extends_edge_count": added_extends,
        "exact_instance_of_edge_count": added_instance_of,
        "skipped_exact_relation_rows_missing_nodes": skipped_missing_nodes,
        "skipped_exact_relation_rows_disabled_or_unknown": skipped_disabled_type,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract a typeclass / inheritance-like subgraph.")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    graph_root = Path(config["graph_root"])
    output_root = Path(config["output_root"])
    output_root.mkdir(parents=True, exist_ok=True)

    include_decl_kinds = set(config.get("include_decl_kinds", ["class", "instance", "structure"]))
    class_like_decl_kinds = set(config.get("class_like_decl_kinds", ["class", "structure"]))
    keep_edge_types = set(config.get("keep_edge_types", ["uses"]))
    keep_induced_uses = bool(config.get("keep_induced_uses", True))
    add_extends_edges = bool(config.get("add_extends_inferred_edges", True))
    add_instance_of_edges = bool(config.get("add_instance_of_inferred_edges", True))
    relation_edges_path = Path(config["relation_edges_path"]) if config.get("relation_edges_path") else None
    relation_format = str(config.get("relation_format", "tsv"))
    add_exact_extends_edges = bool(config.get("add_exact_extends_edges", relation_edges_path is not None))
    add_exact_instance_of_edges = bool(config.get("add_exact_instance_of_edges", relation_edges_path is not None))
    exact_extends_edge_type = str(config.get("exact_extends_edge_type", "extends"))
    exact_instance_of_edge_type = str(config.get("exact_instance_of_edge_type", "instance_of"))
    prefer_exact_relations = bool(config.get("prefer_exact_relations", relation_edges_path is not None))

    declarations = read_csv_rows(graph_root / "declarations.csv")
    edges = read_csv_rows(graph_root / "edges.csv")

    kept_declarations = [row for row in declarations if row.get("decl_kind", "") in include_decl_kinds]
    kept_ids = {row["declaration_id"] for row in kept_declarations}
    kept_exact_names, kept_unique_short_names = build_name_indices(kept_declarations)
    class_like_rows = [row for row in kept_declarations if row.get("decl_kind", "") in class_like_decl_kinds]
    exact_names, unique_short_names = build_name_indices(class_like_rows)

    kept_edges: list[dict] = []
    seen_edge_ids: set[str] = set()
    edge_type_counts: Counter[str] = Counter()
    exact_relation_stats = {
        "exact_extends_edge_count": 0,
        "exact_instance_of_edge_count": 0,
        "skipped_exact_relation_rows_missing_nodes": 0,
        "skipped_exact_relation_rows_disabled_or_unknown": 0,
    }

    if keep_induced_uses:
        for row in edges:
            if row.get("edge_type", "") not in keep_edge_types:
                continue
            if row["src_id"] not in kept_ids or row["dst_id"] not in kept_ids:
                continue
            if row["edge_id"] in seen_edge_ids:
                continue
            seen_edge_ids.add(row["edge_id"])
            kept_edges.append(row)
            edge_type_counts[row["edge_type"]] += 1

    inferred_extends = 0
    inferred_instance_of = 0
    source_commit = config["source_commit"]
    relation_rows: list[dict] = []

    if relation_edges_path is not None:
        if relation_format != "tsv":
            raise ValueError(f"Unsupported relation_format: {relation_format}")
        relation_rows = read_tsv_rows(relation_edges_path)
        exact_relation_stats = add_exact_relation_edges(
            relation_rows=relation_rows,
            src_exact_names=kept_exact_names,
            src_unique_short_names=kept_unique_short_names,
            dst_exact_names=exact_names,
            dst_unique_short_names=unique_short_names,
            source_commit=source_commit,
            add_extends_edges=add_exact_extends_edges,
            add_instance_of_edges=add_exact_instance_of_edges,
            extends_edge_type=exact_extends_edge_type,
            instance_of_edge_type=exact_instance_of_edge_type,
            kept_edges=kept_edges,
            seen_edge_ids=seen_edge_ids,
            edge_type_counts=edge_type_counts,
        )
    elif prefer_exact_relations:
        raise ValueError("prefer_exact_relations=true but relation_edges_path is not configured.")

    for row in kept_declarations:
        if add_extends_edges and row.get("decl_kind", "") in class_like_decl_kinds:
            for dst_id in sorted(infer_extends_targets(row, exact_names, unique_short_names)):
                edge = build_edge_row(
                    src_id=row["declaration_id"],
                    dst_id=dst_id,
                    edge_type="extends_inferred",
                    source_commit=source_commit,
                    evidence_source="signature_regex",
                )
                if edge["edge_id"] in seen_edge_ids:
                    continue
                seen_edge_ids.add(edge["edge_id"])
                kept_edges.append(edge)
                edge_type_counts[edge["edge_type"]] += 1
                inferred_extends += 1

        if add_instance_of_edges and row.get("decl_kind", "") == "instance":
            for dst_id in sorted(infer_instance_targets(row, exact_names, unique_short_names)):
                edge = build_edge_row(
                    src_id=row["declaration_id"],
                    dst_id=dst_id,
                    edge_type="instance_of_inferred",
                    source_commit=source_commit,
                    evidence_source="signature_regex",
                )
                if edge["edge_id"] in seen_edge_ids:
                    continue
                seen_edge_ids.add(edge["edge_id"])
                kept_edges.append(edge)
                edge_type_counts[edge["edge_type"]] += 1
                inferred_instance_of += 1

    decl_kind_counts = Counter(row["decl_kind"] for row in kept_declarations)
    stats = {
        "graph_root": str(graph_root),
        "num_declarations": len(kept_declarations),
        "num_edges": len(kept_edges),
        "include_decl_kinds": sorted(include_decl_kinds),
        "class_like_decl_kinds": sorted(class_like_decl_kinds),
        "keep_induced_uses": keep_induced_uses,
        "add_extends_inferred_edges": add_extends_edges,
        "add_instance_of_inferred_edges": add_instance_of_edges,
        "relation_edges_path": None if relation_edges_path is None else str(relation_edges_path),
        "relation_format": relation_format if relation_edges_path is not None else None,
        "prefer_exact_relations": prefer_exact_relations,
        "add_exact_extends_edges": add_exact_extends_edges,
        "add_exact_instance_of_edges": add_exact_instance_of_edges,
        "decl_kind_counts": dict(sorted(decl_kind_counts.items())),
        "edge_type_counts": dict(sorted(edge_type_counts.items())),
        "inferred_extends_edge_count": inferred_extends,
        "inferred_instance_of_edge_count": inferred_instance_of,
        **exact_relation_stats,
    }

    decl_fields = list(kept_declarations[0].keys()) if kept_declarations else []
    edge_fields = [
        "edge_id",
        "src_id",
        "dst_id",
        "edge_type",
        "evidence_source",
        "weight",
        "is_direct",
        "source_commit",
    ]
    write_csv(output_root / "declarations.csv", kept_declarations, decl_fields)
    write_csv(output_root / "edges.csv", kept_edges, edge_fields)
    (output_root / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[done] declarations: {len(kept_declarations)}")
    print(f"[done] edges: {len(kept_edges)}")
    print(f"[done] exact extends edges: {exact_relation_stats['exact_extends_edge_count']}")
    print(f"[done] exact instance_of edges: {exact_relation_stats['exact_instance_of_edge_count']}")
    print(f"[done] inferred extends edges: {inferred_extends}")
    print(f"[done] inferred instance_of edges: {inferred_instance_of}")
    print(f"[done] output: {output_root}")


if __name__ == "__main__":
    main()
