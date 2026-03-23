from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterable


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


def normalize_generic_json_record(
    record: dict[str, Any],
    adapter_cfg: dict[str, Any],
    source_commit: str,
    trace_version: str,
    source_file: Path,
) -> tuple[dict[str, Any] | None, str | None]:
    decl_name = find_first_scalar(record, adapter_cfg["decl_name_keys"])
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

    normalized = {
        "decl_name": decl_name,
        "decl_kind": decl_kind,
        "module_name": module_name,
        "file_path": file_path,
        "dependencies": dependencies,
        "module_dependencies": [],
        "namespace": record.get("namespace", ""),
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


def has_more_specific_decl_child(node: ET.Element) -> bool:
    node_full_name = node.attrib.get("full_name") or node.attrib.get("name")
    node_kind = classify_decl_kind_from_tag(node.tag)
    if node_kind != "def":
        return False
    for child in node.iter():
        if child is node:
            continue
        child_kind = classify_decl_kind_from_tag(child.tag)
        if child_kind is None or child_kind == "def":
            continue
        child_full_name = child.attrib.get("full_name") or child.attrib.get("name")
        if child_full_name and child_full_name == node_full_name:
            return True
    return False


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
    if file_path.endswith(".lean"):
        return file_path[:-5].replace("/", ".").replace("\\", ".")
    if "." in decl_name:
        return ".".join(decl_name.split(".")[:-1])
    return Path(file_path).stem


def normalize_leandojo_trace_xml_file(
    trace_xml_path: Path,
    source_commit: str,
    trace_version: str,
) -> list[dict[str, Any]]:
    tree = ET.parse(trace_xml_path)
    root = tree.getroot()
    traced_file_path = root.attrib.get("path", str(trace_xml_path))
    dep_paths_path = trace_xml_path.with_suffix("").with_suffix(".dep_paths")
    module_dependencies = read_dep_paths(dep_paths_path)

    normalized: list[dict[str, Any]] = []
    seen_decls: set[str] = set()

    for elem in root.iter():
        decl_kind = classify_decl_kind_from_tag(elem.tag)
        if decl_kind is None:
            continue
        if has_more_specific_decl_child(elem):
            continue
        decl_name = elem.attrib.get("full_name") or elem.attrib.get("name")
        if not decl_name or decl_name in seen_decls:
            continue
        seen_decls.add(decl_name)

        line_start, _ = parse_line_col(elem.attrib.get("start"))
        line_end, _ = parse_line_col(elem.attrib.get("end"))
        module_name = infer_module_name(traced_file_path, decl_name)
        signature_text = collect_decl_text(elem)
        dependencies = collect_decl_dependencies(elem, decl_name)

        normalized.append(
            {
                "decl_name": decl_name,
                "decl_kind": decl_kind,
                "module_name": module_name,
                "file_path": traced_file_path,
                "dependencies": dependencies,
                "module_dependencies": module_dependencies,
                "namespace": module_name,
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
    adapter_cfg = config["adapter"]
    source_commit = config["source_commit"]
    trace_version = config["trace_version"]
    adapter_name = adapter_cfg["name"]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    skip_report_path.parent.mkdir(parents=True, exist_ok=True)

    normalized_count = 0
    skipped: dict[str, int] = {}
    seen_keys: set[tuple[str, str]] = set()

    with output_path.open("w", encoding="utf-8") as out_f:
        for file_path in iter_input_files(input_root, input_glob):
            if not file_path.is_file():
                continue
            try:
                if adapter_name == "leandojo_trace_xml":
                    records = normalize_leandojo_trace_xml_file(
                        trace_xml_path=file_path,
                        source_commit=source_commit,
                        trace_version=trace_version,
                    )
                    for normalized in records:
                        dedup_key = (normalized["decl_name"], normalized["file_path"])
                        if dedup_key in seen_keys:
                            continue
                        seen_keys.add(dedup_key)
                        out_f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        normalized_count += 1
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

                    dedup_key = (normalized["decl_name"], normalized["file_path"])
                    if dedup_key in seen_keys:
                        continue
                    seen_keys.add(dedup_key)

                    out_f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                    normalized_count += 1
            except Exception as exc:  # noqa: BLE001
                key = f"file_error:{type(exc).__name__}"
                skipped[key] = skipped.get(key, 0) + 1

    skip_report = {
        "input_root": str(input_root),
        "input_glob": input_glob,
        "input_format": input_format,
        "adapter_name": adapter_name,
        "normalized_count": normalized_count,
        "skipped": skipped,
    }
    skip_report_path.write_text(
        json.dumps(skip_report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"[done] normalized records: {normalized_count}")
    print(f"[done] output: {output_path}")
    print(f"[done] skip report: {skip_report_path}")


if __name__ == "__main__":
    main()
