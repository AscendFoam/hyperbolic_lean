from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


DECL_FIELDS = [
    "declaration_id",
    "decl_name",
    "decl_short_name",
    "raw_decl_name",
    "name_qualification_source",
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
    "source_trace_file",
]

EDGE_FIELDS = [
    "edge_id",
    "src_id",
    "dst_id",
    "edge_type",
    "evidence_source",
    "weight",
    "is_direct",
    "source_commit",
]


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_tsv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def short_decl_name(decl_name: str) -> str:
    return decl_name.split(".")[-1]


def infer_namespace(decl_name: str, module_name: str) -> str:
    if "." in decl_name:
        return ".".join(decl_name.split(".")[:-1])
    return module_name


def infer_file_path(module_name: str) -> str:
    if not module_name:
        return ""
    return module_name.replace(".", "/") + ".lean"


def make_declaration_id(source_commit: str, decl_name: str) -> str:
    return f"{source_commit}::{decl_name}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a declaration graph scaffold from a declaration index TSV.")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    declaration_index_path = Path(config["declaration_index_path"])
    output_root = Path(config["output_root"])
    output_root.mkdir(parents=True, exist_ok=True)

    include_decl_kinds = {str(kind) for kind in config.get("include_decl_kinds", []) if str(kind).strip()}
    require_module_name = bool(config.get("require_module_name", True))
    require_line_start = bool(config.get("require_line_start", False))
    source_commit = str(config["source_commit"])
    trace_version = str(config.get("trace_version", ""))

    declarations: list[dict] = []
    seen_ids: set[str] = set()
    decl_kind_counts: Counter[str] = Counter()
    skipped_counts: Counter[str] = Counter()

    for row in read_tsv_rows(declaration_index_path):
        decl_name = row.get("decl_name", "").strip()
        decl_kind = row.get("decl_kind", "").strip()
        module_name = row.get("module_name", "").strip()
        line_start = row.get("line_start", "").strip()
        line_end = row.get("line_end", "").strip()

        if not decl_name:
            skipped_counts["missing_decl_name"] += 1
            continue
        if include_decl_kinds and decl_kind not in include_decl_kinds:
            skipped_counts["filtered_decl_kind"] += 1
            continue
        if require_module_name and not module_name:
            skipped_counts["missing_module_name"] += 1
            continue
        if require_line_start and not line_start:
            skipped_counts["missing_line_start"] += 1
            continue

        declaration_id = make_declaration_id(source_commit, decl_name)
        if declaration_id in seen_ids:
            skipped_counts["duplicate_declaration_id"] += 1
            continue
        seen_ids.add(declaration_id)

        declarations.append(
            {
                "declaration_id": declaration_id,
                "decl_name": decl_name,
                "decl_short_name": row.get("decl_short_name", "").strip() or short_decl_name(decl_name),
                "raw_decl_name": row.get("decl_short_name", "").strip() or short_decl_name(decl_name),
                "name_qualification_source": "declaration_index_only",
                "decl_kind": decl_kind or "unknown",
                "module_name": module_name,
                "file_path": infer_file_path(module_name),
                "namespace": infer_namespace(decl_name, module_name),
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
        )
        decl_kind_counts[decl_kind or "unknown"] += 1

    write_csv(output_root / "declarations.csv", declarations, DECL_FIELDS)
    write_csv(output_root / "edges.csv", [], EDGE_FIELDS)
    stats = {
        "declaration_index_path": str(declaration_index_path),
        "output_root": str(output_root),
        "source_commit": source_commit,
        "trace_version": trace_version,
        "include_decl_kinds": sorted(include_decl_kinds),
        "require_module_name": require_module_name,
        "require_line_start": require_line_start,
        "num_declarations": len(declarations),
        "num_edges": 0,
        "decl_kind_counts": dict(sorted(decl_kind_counts.items())),
        "skipped_counts": dict(sorted(skipped_counts.items())),
    }
    (output_root / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[done] declarations: {len(declarations)}")
    print(f"[done] edges: 0")
    print(f"[done] output: {output_root}")


if __name__ == "__main__":
    main()
