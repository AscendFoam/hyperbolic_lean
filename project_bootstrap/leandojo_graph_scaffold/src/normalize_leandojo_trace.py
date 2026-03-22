from __future__ import annotations

import argparse
import json
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


def normalize_record(
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
                for record in iter_records_from_file(file_path, input_format):
                    if not isinstance(record, dict):
                        continue
                    normalized, reason = normalize_record(
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
