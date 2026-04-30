from __future__ import annotations

import argparse
import csv
import json
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

QUALIFICATION_PRIORITY = {
    "xml_full_name": 5,
    "ancestor_full_name": 4,
    "declaration_index": 3,
    "raw_qualified_name": 2,
    "generic_input": 1,
    "declaration_index_backfill": 0,
    "unknown": 0,
}


def load_config(config_path: Path) -> dict[str, Any]:
    return json.loads(config_path.read_text(encoding="utf-8"))


def iter_input_files(input_root: Path, input_glob: str) -> Iterable[Path]:
    yield from input_root.glob(input_glob)


def iter_records_from_file(path: Path, input_format: str) -> Iterable[dict[str, Any]]:
    if input_format == "jsonl":
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                value = json.loads(line)
                if isinstance(value, dict):
                    yield value
    elif input_format == "json":
        value = json.loads(path.read_text(encoding="utf-8"))
        yield from iter_records_from_json_value(value)
    elif input_format == "xml":
        # XML files are handled by the dedicated adapter below.
        return
        yield  # pragma: no cover
    else:
        raise ValueError(f"Unsupported input_format: {input_format}")


def iter_records_from_json_value(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for v in value.values():
            yield from iter_records_from_json_value(v)
    elif isinstance(value, list):
        for item in value:
            yield from iter_records_from_json_value(item)


def find_first_scalar(record: dict[str, Any], keys: list[str]) -> str | None:
    for key in keys:
        if key in record and isinstance(record[key], (str, int, float)):
            return str(record[key])
    return None


def find_first_list(record: dict[str, Any], keys: list[str]) -> list[str] | None:
    for key in keys:
        if key in record and isinstance(record[key], list):
            items: list[str] = []
            for item in record[key]:
                if isinstance(item, (str, int, float)):
                    items.append(str(item))
                elif isinstance(item, dict):
                    candidate = (
                        item.get("decl_name")
                        or item.get("name")
                        or item.get("full_name")
                        or item.get("target")
                    )
                    if candidate is not None:
                        items.append(str(candidate))
            return items
    return None


def short_decl_name(decl_name: str) -> str:
    return decl_name.split(".")[-1]


def infer_namespace(decl_name: str, module_name: str) -> str:
    if "." in decl_name:
        return ".".join(decl_name.split(".")[:-1])
    return module_name


def parse_index_line_value(value: str | None) -> int | str:
    if value is None:
        return ""
    text = str(value).strip()
    if not text:
        return ""
    if text.isdigit():
        return int(text)
    return text


def normalize_generic_json_record(
    record: dict[str, Any],
    adapter_cfg: dict[str, Any],
    source_commit: str,
    trace_version: str,
    source_file: Path,
) -> tuple[dict[str, Any] | None, str | None]:
    decl_name_keys = adapter_cfg.get("decl_full_name_keys", []) + adapter_cfg["decl_name_keys"]
    decl_name = find_first_scalar(record, decl_name_keys)
    decl_kind = find_first_scalar(record, adapter_cfg["decl_kind_keys"])
    module_name = find_first_scalar(record, adapter_cfg["module_name_keys"])
    file_path = find_first_scalar(record, adapter_cfg["file_path_keys"])
    dependencies = find_first_list(record, adapter_cfg["dependency_keys"])

    if not decl_name:
        return None, "missing_decl_name"
    if not decl_kind:
        decl_kind = "unknown"
    if not module_name:
        module_name = source_file.stem
    if not file_path:
        file_path = str(source_file)
    if dependencies is None:
        dependencies = []

    raw_decl_name = find_first_scalar(record, adapter_cfg["decl_name_keys"]) or decl_name
    namespace = record.get("namespace") or infer_namespace(decl_name, module_name)
    normalized = {
        "decl_name": decl_name,
        "decl_short_name": short_decl_name(decl_name),
        "raw_decl_name": raw_decl_name,
        "name_qualification_source": "generic_input",
        "decl_kind": decl_kind,
        "module_name": module_name,
        "file_path": file_path,
        "dependencies": dependencies,
        "module_dependencies": [],
        "namespace": namespace,
        "line_start": record.get("line_start", ""),
        "line_end": record.get("line_end", ""),
        "signature_text": record.get("signature_text", record.get("type", "")),
        "body_text": record.get("body_text", ""),
        "docstring": record.get("docstring", ""),
        "ast_size": record.get("ast_size", ""),
        "token_count": record.get("token_count", ""),
        "dependency_depth": record.get("dependency_depth", ""),
        "source_commit": source_commit,
        "trace_version": trace_version,
        "source_trace_file": str(source_file),
    }
    return normalized, None


def parse_line_col(text: str | None) -> tuple[int | str, int | str]:
    if not text or not text.startswith("(") or "," not in text:
        return "", ""
    inner = text.strip()[1:-1]
    parts = [p.strip() for p in inner.split(",")]
    if len(parts) != 2:
        return "", ""
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return "", ""


def classify_decl_kind_from_tag(tag: str) -> str | None:
    lower = tag.lower()
    if "theorem" in lower:
        return "theorem"
    if "lemma" in lower:
        return "lemma"
    if "instance" in lower:
        return "instance"
    if "class" in lower:
        return "class"
    if "structure" in lower:
        return "structure"
    if "inductive" in lower:
        return "inductive"
    if "def" in lower or "declaration" in lower or "abbrev" in lower or "opaque" in lower:
        return "def"
    return None


def classify_decl_kind_from_xml_node(node: ET.Element) -> str | None:
    # Lean's XML wraps both `class` and `structure` declarations in
    # `CommandStructureNode`; the actual distinction is carried by the
    # immediate keyword child node.
    if node.tag == "CommandStructureNode":
        child_tags = {child.tag for child in list(node)}
        if "CommandClasstkNode" in child_tags:
            return "class"
        if "CommandStructuretkNode" in child_tags:
            return "structure"
    return classify_decl_kind_from_tag(node.tag)


def collect_decl_text(node: ET.Element, max_len: int = 500) -> str:
    parts: list[str] = []
    for child in node.iter():
        val = child.attrib.get("val") or child.attrib.get("raw_val")
        if val:
            parts.append(val)
    text = " ".join(parts).strip()
    return text[:max_len]


def collect_decl_dependencies(node: ET.Element, decl_name: str) -> list[str]:
    deps: list[str] = []
    seen: set[str] = set()
    for child in node.iter():
        full_name = child.attrib.get("full_name")
        if not full_name or full_name == decl_name:
            continue
        if full_name in seen:
            continue
        seen.add(full_name)
        deps.append(full_name)
    return deps


def read_dep_paths(dep_paths_path: Path) -> list[str]:
    if not dep_paths_path.exists():
        return []
    lines = dep_paths_path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip()]


def infer_module_name(file_path: str, decl_name: str) -> str:
    normalized = file_path.replace("\\", "/")
    if normalized.endswith(".lean"):
        base = normalized[:-5]
        for marker in ["/src/lean/", "/build/ir/", "/build/lib/"]:
            if marker in base:
                suffix = base.split(marker, 1)[1]
                return suffix.replace("/", ".").strip(".")
        return base.replace("/", ".").strip(".")
    if "." in decl_name:
        return ".".join(decl_name.split(".")[:-1])
    return Path(file_path).stem


def build_parent_map(root: ET.Element) -> dict[ET.Element, ET.Element | None]:
    parent_map: dict[ET.Element, ET.Element | None] = {root: None}
    stack = [root]
    while stack:
        node = stack.pop()
        for child in list(node):
            parent_map[child] = node
            stack.append(child)
    return parent_map


def iter_decl_ancestors(node: ET.Element, parent_map: dict[ET.Element, ET.Element | None]) -> Iterable[ET.Element]:
    current = parent_map.get(node)
    while current is not None:
        if classify_decl_kind_from_tag(current.tag) is not None:
            yield current
        current = parent_map.get(current)


def build_declaration_index_lookup(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {
            "rows": [],
            "strict": defaultdict(list),
            "line_kind": defaultdict(list),
            "line_only": defaultdict(list),
            "by_name": {},
        }

    rows: list[dict[str, Any]] = []
    strict: dict[tuple, list[dict[str, Any]]] = defaultdict(list)
    line_kind: dict[tuple, list[dict[str, Any]]] = defaultdict(list)
    line_only: dict[tuple, list[dict[str, Any]]] = defaultdict(list)
    by_name: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rows.append(row)
            module_name = row.get("module_name", "")
            line_start = row.get("line_start", "")
            line_end = row.get("line_end", "")
            decl_kind = row.get("decl_kind", "")
            strict[(module_name, line_start, line_end, decl_kind)].append(row)
            line_kind[(module_name, line_start, decl_kind)].append(row)
            line_only[(module_name, line_start)].append(row)
            decl_name = row.get("decl_name", "")
            if decl_name and decl_name not in by_name:
                by_name[decl_name] = row
    return {
        "rows": rows,
        "strict": strict,
        "line_kind": line_kind,
        "line_only": line_only,
        "by_name": by_name,
    }


def score_normalized_record(record: dict[str, Any], decl_index_row: dict[str, Any] | None) -> tuple[int, ...]:
    qualification_source = record.get("name_qualification_source", "unknown")
    return (
        int(decl_index_row is not None and record.get("module_name", "") == decl_index_row.get("module_name", "")),
        int(decl_index_row is not None and str(record.get("line_start", "")) == decl_index_row.get("line_start", "")),
        int(decl_index_row is not None and str(record.get("line_end", "")) == decl_index_row.get("line_end", "")),
        int(decl_index_row is not None and record.get("decl_kind", "") == decl_index_row.get("decl_kind", "")),
        QUALIFICATION_PRIORITY.get(qualification_source, 0),
        int(bool(record.get("signature_text", ""))),
    )


def choose_preferred_record(
    existing: dict[str, Any],
    candidate: dict[str, Any],
    decl_index_lookup: dict[str, Any],
) -> dict[str, Any]:
    decl_index_row = decl_index_lookup["by_name"].get(candidate["decl_name"])
    if score_normalized_record(candidate, decl_index_row) > score_normalized_record(existing, decl_index_row):
        return candidate
    return existing


def choose_index_match(candidates: list[dict[str, Any]], raw_name: str | None) -> dict[str, Any] | None:
    if not candidates:
        return None
    if raw_name:
        exact = [row for row in candidates if row.get("decl_name", "") == raw_name]
        if len(exact) == 1:
            return exact[0]
        suffix = [row for row in candidates if short_decl_name(row.get("decl_name", "")) == raw_name]
        if len(suffix) == 1:
            return suffix[0]
    if len(candidates) == 1:
        return candidates[0]
    return None


def resolve_decl_name_from_index(
    lookup: dict[str, Any],
    module_name: str,
    line_start: int | str,
    line_end: int | str,
    decl_kind: str,
    raw_name: str | None,
) -> str | None:
    line_start_text = str(line_start)
    line_end_text = str(line_end)
    for bucket_name, key in [
        ("strict", (module_name, line_start_text, line_end_text, decl_kind)),
        ("line_kind", (module_name, line_start_text, decl_kind)),
        ("line_only", (module_name, line_start_text)),
    ]:
        match = choose_index_match(lookup[bucket_name].get(key, []), raw_name)
        if match is not None:
            return match["decl_name"]
    return None


def resolve_xml_decl_name(
    node: ET.Element,
    parent_map: dict[ET.Element, ET.Element | None],
    decl_index_lookup: dict[str, Any],
    module_name: str,
    line_start: int | str,
    line_end: int | str,
    decl_kind: str,
) -> tuple[str | None, str | None, str | None]:
    raw_name = node.attrib.get("name")
    full_name = node.attrib.get("full_name")
    if full_name:
        return full_name, raw_name or short_decl_name(full_name), "xml_full_name"

    for ancestor in iter_decl_ancestors(node, parent_map):
        ancestor_full_name = ancestor.attrib.get("full_name")
        ancestor_name = ancestor.attrib.get("name")
        if not ancestor_full_name:
            continue
        if raw_name is None:
            return ancestor_full_name, None, "ancestor_full_name"
        if raw_name == ancestor_full_name or raw_name == ancestor_name or raw_name == short_decl_name(ancestor_full_name):
            return ancestor_full_name, raw_name, "ancestor_full_name"

    indexed_name = resolve_decl_name_from_index(
        lookup=decl_index_lookup,
        module_name=module_name,
        line_start=line_start,
        line_end=line_end,
        decl_kind=decl_kind,
        raw_name=raw_name,
    )
    if indexed_name:
        return indexed_name, raw_name or short_decl_name(indexed_name), "declaration_index"

    if raw_name and "." in raw_name:
        return raw_name, short_decl_name(raw_name), "raw_qualified_name"

    return None, raw_name, None


def normalize_leandojo_trace_xml_file(
    trace_xml_path: Path,
    source_commit: str,
    trace_version: str,
    decl_index_lookup: dict[str, Any],
) -> list[dict[str, Any]]:
    tree = ET.parse(trace_xml_path)
    root = tree.getroot()
    parent_map = build_parent_map(root)
    traced_file_path = root.attrib.get("path", str(trace_xml_path))
    dep_paths_path = trace_xml_path.with_suffix("").with_suffix(".dep_paths")
    module_dependencies = read_dep_paths(dep_paths_path)

    normalized: list[dict[str, Any]] = []
    seen_decls: set[str] = set()

    for elem in root.iter():
        if elem.tag == "CommandDeclarationNode":
            continue
        decl_kind = classify_decl_kind_from_xml_node(elem)
        if decl_kind is None:
            continue
        line_start, _ = parse_line_col(elem.attrib.get("start"))
        line_end, _ = parse_line_col(elem.attrib.get("end"))
        module_name = infer_module_name(traced_file_path, elem.attrib.get("full_name") or elem.attrib.get("name") or "")
        decl_name, raw_decl_name, qualification_source = resolve_xml_decl_name(
            node=elem,
            parent_map=parent_map,
            decl_index_lookup=decl_index_lookup,
            module_name=module_name,
            line_start=line_start,
            line_end=line_end,
            decl_kind=decl_kind,
        )
        if not decl_name or decl_name in seen_decls:
            continue
        seen_decls.add(decl_name)

        signature_text = collect_decl_text(elem)
        dependencies = collect_decl_dependencies(elem, decl_name)
        namespace = infer_namespace(decl_name, module_name)

        normalized.append(
            {
                "decl_name": decl_name,
                "decl_short_name": short_decl_name(decl_name),
                "raw_decl_name": raw_decl_name or short_decl_name(decl_name),
                "name_qualification_source": qualification_source or "unknown",
                "decl_kind": decl_kind,
                "module_name": module_name,
                "file_path": traced_file_path,
                "dependencies": dependencies,
                "module_dependencies": module_dependencies,
                "namespace": namespace,
                "line_start": line_start,
                "line_end": line_end,
                "signature_text": signature_text,
                "body_text": "",
                "docstring": "",
                "ast_size": "",
                "token_count": "",
                "dependency_depth": "",
                "source_commit": source_commit,
                "trace_version": trace_version,
                "source_trace_file": str(trace_xml_path),
            }
        )
    return normalized


def score_module_context(record: dict[str, Any]) -> tuple[int, int, int]:
    return (
        int(bool(record.get("file_path", ""))),
        int(bool(record.get("module_dependencies"))),
        int(bool(record.get("source_trace_file", ""))),
    )


def build_module_context(records: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    context_by_module: dict[str, dict[str, Any]] = {}
    for record in records:
        module_name = record.get("module_name", "")
        if not module_name:
            continue
        candidate = {
            "file_path": record.get("file_path", ""),
            "module_dependencies": list(record.get("module_dependencies", [])),
            "source_trace_file": record.get("source_trace_file", ""),
        }
        existing = context_by_module.get(module_name)
        if existing is None or score_module_context(candidate) > score_module_context(existing):
            context_by_module[module_name] = candidate
    return context_by_module


def infer_backfill_file_path(module_name: str, module_context: dict[str, Any] | None) -> str:
    if module_context and module_context.get("file_path"):
        return str(module_context["file_path"])
    if module_name:
        return module_name.replace(".", "/") + ".lean"
    return ""


def build_backfill_record(
    row: dict[str, Any],
    module_context: dict[str, Any] | None,
    source_commit: str,
    trace_version: str,
) -> dict[str, Any]:
    decl_name = row["decl_name"]
    module_name = row.get("module_name", "") or infer_namespace(decl_name, "")
    file_path = infer_backfill_file_path(module_name, module_context)
    return {
        "decl_name": decl_name,
        "decl_short_name": row.get("decl_short_name", "") or short_decl_name(decl_name),
        "raw_decl_name": row.get("decl_short_name", "") or short_decl_name(decl_name),
        "name_qualification_source": "declaration_index_backfill",
        "decl_kind": row.get("decl_kind", "") or "unknown",
        "module_name": module_name,
        "file_path": file_path,
        "dependencies": [],
        "module_dependencies": [] if module_context is None else list(module_context.get("module_dependencies", [])),
        "namespace": infer_namespace(decl_name, module_name),
        "line_start": parse_index_line_value(row.get("line_start")),
        "line_end": parse_index_line_value(row.get("line_end")),
        "signature_text": "",
        "body_text": "",
        "docstring": "",
        "ast_size": "",
        "token_count": "",
        "dependency_depth": "",
        "source_commit": source_commit,
        "trace_version": trace_version,
        "source_trace_file": "" if module_context is None else str(module_context.get("source_trace_file", "")),
    }


def apply_declaration_index_backfill(
    best_records_by_decl: dict[str, dict[str, Any]],
    decl_index_lookup: dict[str, Any],
    source_commit: str,
    trace_version: str,
    backfill_cfg: dict[str, Any] | None,
) -> dict[str, Any]:
    if not backfill_cfg or not bool(backfill_cfg.get("enabled", False)):
        return {
            "enabled": False,
            "added": 0,
            "added_decl_kind_counts": {},
        }

    include_decl_kinds = {
        str(kind)
        for kind in backfill_cfg.get("include_decl_kinds", [])
        if str(kind).strip()
    }
    require_line_start = bool(backfill_cfg.get("require_line_start", True))
    module_context_by_name = build_module_context(best_records_by_decl.values())
    added_decl_kind_counts: Counter[str] = Counter()
    added = 0

    for row in decl_index_lookup.get("rows", []):
        decl_name = row.get("decl_name", "")
        if not decl_name or decl_name in best_records_by_decl:
            continue
        decl_kind = row.get("decl_kind", "")
        if include_decl_kinds and decl_kind not in include_decl_kinds:
            continue
        if require_line_start and not str(row.get("line_start", "")).strip():
            continue
        module_context = module_context_by_name.get(row.get("module_name", ""))
        best_records_by_decl[decl_name] = build_backfill_record(
            row=row,
            module_context=module_context,
            source_commit=source_commit,
            trace_version=trace_version,
        )
        added += 1
        added_decl_kind_counts[decl_kind or "unknown"] += 1

    return {
        "enabled": True,
        "added": added,
        "added_decl_kind_counts": dict(sorted(added_decl_kind_counts.items())),
        "include_decl_kinds": sorted(include_decl_kinds),
        "require_line_start": require_line_start,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize raw LeanDojo trace files into declaration-level JSONL."
    )
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    input_root = Path(config["input_root"])
    input_glob = config["input_glob"]
    input_format = config["input_format"]
    output_path = Path(config["output_path"])
    skip_report_path = Path(config["skip_report_path"])
    declaration_index_path = Path(config["declaration_index_path"]) if config.get("declaration_index_path") else None
    adapter_cfg = config["adapter"]
    backfill_cfg = config.get("declaration_index_backfill")
    source_commit = config["source_commit"]
    trace_version = config["trace_version"]
    adapter_name = adapter_cfg["name"]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    skip_report_path.parent.mkdir(parents=True, exist_ok=True)

    skipped: dict[str, int] = {}
    best_records_by_decl: dict[str, dict[str, Any]] = {}
    qualification_source_counts: Counter[str] = Counter()
    canonical_duplicate_records_resolved = 0
    decl_index_lookup = build_declaration_index_lookup(declaration_index_path)

    for file_path in iter_input_files(input_root, input_glob):
        if not file_path.is_file():
            continue
        try:
            if adapter_name == "leandojo_trace_xml":
                records = normalize_leandojo_trace_xml_file(
                    trace_xml_path=file_path,
                    source_commit=source_commit,
                    trace_version=trace_version,
                    decl_index_lookup=decl_index_lookup,
                )
                for normalized in records:
                    existing = best_records_by_decl.get(normalized["decl_name"])
                    if existing is None:
                        best_records_by_decl[normalized["decl_name"]] = normalized
                        continue
                    best_records_by_decl[normalized["decl_name"]] = choose_preferred_record(
                        existing=existing,
                        candidate=normalized,
                        decl_index_lookup=decl_index_lookup,
                    )
                    canonical_duplicate_records_resolved += 1
                if not records:
                    skipped["no_decls_found"] = skipped.get("no_decls_found", 0) + 1
                continue

            for record in iter_records_from_file(file_path, input_format):
                if not isinstance(record, dict):
                    continue
                normalized, reason = normalize_generic_json_record(
                    record=record,
                    adapter_cfg=adapter_cfg,
                    source_commit=source_commit,
                    trace_version=trace_version,
                    source_file=file_path,
                )
                if normalized is None:
                    key = reason or "unknown_reason"
                    skipped[key] = skipped.get(key, 0) + 1
                    continue

                existing = best_records_by_decl.get(normalized["decl_name"])
                if existing is None:
                    best_records_by_decl[normalized["decl_name"]] = normalized
                    continue
                best_records_by_decl[normalized["decl_name"]] = choose_preferred_record(
                    existing=existing,
                    candidate=normalized,
                    decl_index_lookup=decl_index_lookup,
                )
                canonical_duplicate_records_resolved += 1
        except Exception as exc:  # noqa: BLE001
            key = f"file_error:{type(exc).__name__}"
            skipped[key] = skipped.get(key, 0) + 1

    backfill_summary = apply_declaration_index_backfill(
        best_records_by_decl=best_records_by_decl,
        decl_index_lookup=decl_index_lookup,
        source_commit=source_commit,
        trace_version=trace_version,
        backfill_cfg=backfill_cfg,
    )

    normalized_count = 0
    with output_path.open("w", encoding="utf-8") as out_f:
        for normalized in best_records_by_decl.values():
            qualification_source_counts[normalized.get("name_qualification_source", "unknown")] += 1
            out_f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
            normalized_count += 1

    skip_report = {
        "input_root": str(input_root),
        "input_glob": input_glob,
        "input_format": input_format,
        "adapter_name": adapter_name,
        "declaration_index_path": None if declaration_index_path is None else str(declaration_index_path),
        "normalized_count": normalized_count,
        "canonical_duplicate_records_resolved": canonical_duplicate_records_resolved,
        "declaration_index_backfill": backfill_summary,
        "name_qualification_source_counts": dict(sorted(qualification_source_counts.items())),
        "skipped": skipped,
    }
    skip_report_path.write_text(
        json.dumps(skip_report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"[done] normalized records: {normalized_count}")
    if backfill_summary.get("enabled"):
        print(f"[done] declaration-index backfilled records: {backfill_summary['added']}")
    print(f"[done] output: {output_path}")
    print(f"[done] skip report: {skip_report_path}")


if __name__ == "__main__":
    main()
