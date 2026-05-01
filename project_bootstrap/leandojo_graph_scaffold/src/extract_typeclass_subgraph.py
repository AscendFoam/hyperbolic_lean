from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


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


def infer_namespace(decl_name: str, module_name: str) -> str:
    if "." in decl_name:
        return ".".join(decl_name.split(".")[:-1])
    return module_name


def make_declaration_id(source_commit: str, decl_name: str) -> str:
    return f"{source_commit}::{decl_name}"


def build_declaration_index_lookup(path: Path | None) -> dict[str, dict[str, str]]:
    if path is None or not path.exists():
        return {}
    return {row["decl_name"]: row for row in read_tsv_rows(path)}


def build_relation_node_lookup(path: Path | None) -> dict[str, dict[str, str]]:
    if path is None or not path.exists():
        return {}
    return {row["decl_name"]: row for row in read_tsv_rows(path)}


def is_true_text(text: str) -> bool:
    return str(text).strip().lower() == "true"


def derive_decl_kind_from_relation_node(row: dict[str, str] | None) -> str:
    if row is None:
        return "unknown"
    if is_true_text(row.get("is_instance", "")):
        return "instance"
    if is_true_text(row.get("is_class", "")):
        return "class"
    if is_true_text(row.get("is_structure", "")):
        return "structure"
    return "unknown"


def infer_file_path(module_name: str) -> str:
    if not module_name:
        return ""
    return module_name.replace(".", "/") + ".lean"


def build_backfilled_declaration_row(
    decl_name: str,
    source_commit: str,
    trace_version: str,
    declaration_index_row: dict[str, str] | None,
    relation_node_row: dict[str, str] | None,
) -> tuple[dict[str, Any], str]:
    relation_decl_kind = derive_decl_kind_from_relation_node(relation_node_row)
    index_decl_kind = "" if declaration_index_row is None else declaration_index_row.get("decl_kind", "")
    decl_kind = relation_decl_kind if relation_decl_kind != "unknown" else (index_decl_kind or "unknown")

    module_name = ""
    line_start = ""
    line_end = ""
    if declaration_index_row is not None:
        module_name = declaration_index_row.get("module_name", "")
        line_start = declaration_index_row.get("line_start", "")
        line_end = declaration_index_row.get("line_end", "")

    namespace = infer_namespace(decl_name, module_name)
    file_path = infer_file_path(module_name or namespace)

    if declaration_index_row is not None and relation_node_row is not None:
        backfill_source = "coverage_backfill:index+relation_nodes"
    elif declaration_index_row is not None:
        backfill_source = "coverage_backfill:declaration_index"
    elif relation_node_row is not None:
        backfill_source = "coverage_backfill:relation_nodes"
    else:
        backfill_source = "coverage_backfill:unknown"

    row = {
        "declaration_id": make_declaration_id(source_commit, decl_name),
        "decl_name": decl_name,
        "decl_short_name": short_decl_name(decl_name),
        "raw_decl_name": short_decl_name(decl_name),
        "name_qualification_source": backfill_source,
        "decl_kind": decl_kind,
        "module_name": module_name,
        "file_path": file_path,
        "namespace": namespace,
        "line_start": line_start,
        "line_end": line_end,
        "signature_text": "",
        "body_text": "",
        "docstring": "",
        "ast_size": "",
        "token_count": "",
        "dependency_depth": "",
        "source_commit": source_commit,
        "trace_version": trace_version,
        "source_trace_file": "",
    }
    return row, backfill_source


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


def apply_coverage_aware_backfill(
    kept_declarations: list[dict],
    include_decl_kinds: set[str],
    relation_rows: list[dict],
    source_commit: str,
    trace_version: str,
    backfill_cfg: dict[str, Any] | None,
) -> dict[str, Any]:
    if not backfill_cfg or not bool(backfill_cfg.get("enabled", False)):
        return {
            "enabled": False,
            "added_declarations": 0,
            "added_decl_kind_counts": {},
            "added_source_counts": {},
            "requested_endpoint_counts": {},
            "unresolved_names": 0,
            "skipped_by_kind": 0,
        }

    declaration_index_lookup = build_declaration_index_lookup(
        Path(backfill_cfg["declaration_index_path"]) if backfill_cfg.get("declaration_index_path") else None
    )
    relation_node_lookup = build_relation_node_lookup(
        Path(backfill_cfg["relation_nodes_path"]) if backfill_cfg.get("relation_nodes_path") else None
    )
    backfill_relation_types = set(backfill_cfg.get("relation_types", ["extends", "instance_of"]))
    endpoint_roles = set(backfill_cfg.get("endpoint_roles", ["src", "dst"]))
    allowed_decl_kinds = {
        str(kind)
        for kind in backfill_cfg.get("include_decl_kinds", sorted(include_decl_kinds))
        if str(kind).strip()
    }

    kept_by_name = {row["decl_name"]: row for row in kept_declarations}
    requested_names: set[str] = set()
    requested_endpoint_counts: Counter[str] = Counter()
    for row in relation_rows:
        relation_type = row.get("relation_type", "")
        if relation_type not in backfill_relation_types:
            continue
        if "src" in endpoint_roles and row.get("src_name", "") not in kept_by_name:
            requested_names.add(row["src_name"])
            requested_endpoint_counts[f"{relation_type}:src"] += 1
        if "dst" in endpoint_roles and row.get("dst_name", "") not in kept_by_name:
            requested_names.add(row["dst_name"])
            requested_endpoint_counts[f"{relation_type}:dst"] += 1

    added_decl_kind_counts: Counter[str] = Counter()
    added_source_counts: Counter[str] = Counter()
    unresolved_names: list[str] = []
    skipped_by_kind = 0

    for decl_name in sorted(requested_names):
        if decl_name in kept_by_name:
            continue
        declaration_index_row = declaration_index_lookup.get(decl_name)
        relation_node_row = relation_node_lookup.get(decl_name)
        if declaration_index_row is None and relation_node_row is None:
            unresolved_names.append(decl_name)
            continue

        candidate_row, backfill_source = build_backfilled_declaration_row(
            decl_name=decl_name,
            source_commit=source_commit,
            trace_version=trace_version,
            declaration_index_row=declaration_index_row,
            relation_node_row=relation_node_row,
        )
        if allowed_decl_kinds and candidate_row["decl_kind"] not in allowed_decl_kinds:
            skipped_by_kind += 1
            continue

        kept_declarations.append(candidate_row)
        kept_by_name[decl_name] = candidate_row
        added_decl_kind_counts[candidate_row["decl_kind"]] += 1
        added_source_counts[backfill_source] += 1

    return {
        "enabled": True,
        "added_declarations": sum(added_decl_kind_counts.values()),
        "added_decl_kind_counts": dict(sorted(added_decl_kind_counts.items())),
        "added_source_counts": dict(sorted(added_source_counts.items())),
        "requested_endpoint_counts": dict(sorted(requested_endpoint_counts.items())),
        "requested_unique_names": len(requested_names),
        "unresolved_names": len(unresolved_names),
        "unresolved_name_examples": unresolved_names[:20],
        "skipped_by_kind": skipped_by_kind,
        "relation_types": sorted(backfill_relation_types),
        "endpoint_roles": sorted(endpoint_roles),
        "include_decl_kinds": sorted(allowed_decl_kinds),
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
    trace_version = str(config.get("trace_version", ""))
    add_exact_extends_edges = bool(config.get("add_exact_extends_edges", relation_edges_path is not None))
    add_exact_instance_of_edges = bool(config.get("add_exact_instance_of_edges", relation_edges_path is not None))
    exact_extends_edge_type = str(config.get("exact_extends_edge_type", "extends"))
    exact_instance_of_edge_type = str(config.get("exact_instance_of_edge_type", "instance_of"))
    prefer_exact_relations = bool(config.get("prefer_exact_relations", relation_edges_path is not None))

    declarations = read_csv_rows(graph_root / "declarations.csv")
    edges = read_csv_rows(graph_root / "edges.csv")

    kept_declarations = [row for row in declarations if row.get("decl_kind", "") in include_decl_kinds]

    kept_edges: list[dict] = []
    seen_edge_ids: set[str] = set()
    edge_type_counts: Counter[str] = Counter()
    inferred_extends = 0
    inferred_instance_of = 0
    source_commit = config["source_commit"]
    relation_rows: list[dict] = []

    if relation_edges_path is not None:
        if relation_format != "tsv":
            raise ValueError(f"Unsupported relation_format: {relation_format}")
        relation_rows = read_tsv_rows(relation_edges_path)
    elif prefer_exact_relations:
        raise ValueError("prefer_exact_relations=true but relation_edges_path is not configured.")

    coverage_backfill_summary = apply_coverage_aware_backfill(
        kept_declarations=kept_declarations,
        include_decl_kinds=include_decl_kinds,
        relation_rows=relation_rows,
        source_commit=source_commit,
        trace_version=trace_version,
        backfill_cfg=config.get("coverage_aware_backfill"),
    )

    kept_ids = {row["declaration_id"] for row in kept_declarations}
    kept_exact_names, kept_unique_short_names = build_name_indices(kept_declarations)
    class_like_rows = [row for row in kept_declarations if row.get("decl_kind", "") in class_like_decl_kinds]
    exact_names, unique_short_names = build_name_indices(class_like_rows)

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

    exact_relation_stats = {
        "exact_extends_edge_count": 0,
        "exact_instance_of_edge_count": 0,
        "skipped_exact_relation_rows_missing_nodes": 0,
        "skipped_exact_relation_rows_disabled_or_unknown": 0,
    }
    if relation_rows:
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
        "coverage_aware_backfill": coverage_backfill_summary,
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
