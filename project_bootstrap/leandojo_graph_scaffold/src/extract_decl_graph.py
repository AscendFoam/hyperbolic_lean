from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Iterable


REQUIRED_FIELDS = {
    "decl_name",
    "decl_kind",
    "module_name",
    "file_path",
    "dependencies",
}


def load_config(config_path: Path) -> dict:
    return json.loads(config_path.read_text(encoding="utf-8"))


def iter_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_no}: {exc}") from exc


def validate_record(record: dict, line_no: int) -> None:
    missing = REQUIRED_FIELDS - set(record.keys())
    if missing:
        raise ValueError(f"Line {line_no} missing required fields: {sorted(missing)}")
    if not isinstance(record["dependencies"], list):
        raise ValueError(f"Line {line_no} field 'dependencies' must be a list")


def make_declaration_id(source_commit: str, decl_name: str) -> str:
    return f"{source_commit}::{decl_name}"


def normalize_record(record: dict, source_commit: str) -> dict:
    decl_name = record["decl_name"]
    return {
        "declaration_id": make_declaration_id(source_commit, decl_name),
        "decl_name": decl_name,
        "decl_kind": record["decl_kind"],
        "module_name": record["module_name"],
        "file_path": record["file_path"],
        "namespace": record.get("namespace", ""),
        "line_start": record.get("line_start", ""),
        "line_end": record.get("line_end", ""),
        "signature_text": record.get("signature_text", ""),
        "body_text": record.get("body_text", ""),
        "docstring": record.get("docstring", ""),
        "ast_size": record.get("ast_size", ""),
        "token_count": record.get("token_count", ""),
        "dependency_depth": record.get("dependency_depth", ""),
        "source_commit": source_commit,
        "trace_version": record.get("trace_version", ""),
    }


def build_rows(records: list[dict], source_commit: str, edge_type: str, drop_self_edges: bool) -> tuple[list[dict], list[dict], dict]:
    declarations: list[dict] = []
    edges: list[dict] = []
    decl_kind_counter: Counter[str] = Counter()
    edge_type_counter: Counter[str] = Counter()

    seen_decls: set[str] = set()
    seen_edges: set[str] = set()

    for record in records:
        decl_row = normalize_record(record, source_commit)
        declarations.append(decl_row)
        seen_decls.add(decl_row["declaration_id"])
        decl_kind_counter[decl_row["decl_kind"]] += 1

    for record in records:
        src_id = make_declaration_id(source_commit, record["decl_name"])
        for dep_name in record["dependencies"]:
            dst_id = make_declaration_id(source_commit, dep_name)
            if drop_self_edges and src_id == dst_id:
                continue
            edge_id = f"{src_id}--{edge_type}--{dst_id}"
            if edge_id in seen_edges:
                continue
            seen_edges.add(edge_id)
            edges.append(
                {
                    "edge_id": edge_id,
                    "src_id": src_id,
                    "dst_id": dst_id,
                    "edge_type": edge_type,
                    "evidence_source": "normalized_trace",
                    "weight": 1.0,
                    "is_direct": True,
                    "source_commit": source_commit,
                }
            )
            edge_type_counter[edge_type] += 1

    stats = {
        "source_commit": source_commit,
        "num_declarations": len(declarations),
        "num_edges": len(edges),
        "decl_kind_counts": dict(sorted(decl_kind_counter.items())),
        "edge_type_counts": dict(sorted(edge_type_counter.items())),
    }
    return declarations, edges, stats


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract declaration graph CSVs from a normalized LeanDojo trace JSONL."
    )
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    normalized_trace_path = Path(config["normalized_trace_path"])
    output_root = Path(config["output_root"])
    source_commit = config["source_commit"]
    edge_type = config.get("edge_type", "uses")
    drop_self_edges = bool(config.get("drop_self_edges", True))

    output_root.mkdir(parents=True, exist_ok=True)

    raw_records: list[dict] = []
    for line_no, record in enumerate(iter_jsonl(normalized_trace_path), start=1):
        validate_record(record, line_no)
        raw_records.append(record)

    declarations, edges, stats = build_rows(
        records=raw_records,
        source_commit=source_commit,
        edge_type=edge_type,
        drop_self_edges=drop_self_edges,
    )

    decl_fields = [
        "declaration_id",
        "decl_name",
        "decl_kind",
        "module_name",
        "file_path",
        "namespace",
        "line_start",
        "line_end",
        "signature_text",
        "body_text",
        "docstring",
        "ast_size",
        "token_count",
        "dependency_depth",
        "source_commit",
        "trace_version",
    ]
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

    write_csv(output_root / "declarations.csv", declarations, decl_fields)
    write_csv(output_root / "edges.csv", edges, edge_fields)
    (output_root / "stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"[done] declarations: {len(declarations)}")
    print(f"[done] edges: {len(edges)}")
    print(f"[done] output: {output_root}")


if __name__ == "__main__":
    main()
