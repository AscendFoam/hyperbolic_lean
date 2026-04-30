from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Iterable


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_no}: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"Line {line_no} is not a JSON object.")
            yield value


def matches_module_prefix(module_name: str, prefixes: list[str]) -> bool:
    return any(module_name == prefix or module_name.startswith(prefix + ".") for prefix in prefixes)


def filter_records(records: list[dict], include_module_prefixes: list[str], keep_only_internal_dependencies: bool) -> tuple[list[dict], dict]:
    kept_records = [
        record for record in records
        if matches_module_prefix(str(record.get("module_name", "")), include_module_prefixes)
    ]
    kept_decl_names = {str(record.get("decl_name", "")) for record in kept_records}

    decl_kind_counts: Counter[str] = Counter()
    module_counts: Counter[str] = Counter()
    dependency_retained = 0
    dependency_dropped = 0

    filtered_records: list[dict] = []
    for record in kept_records:
        dependencies = [str(dep) for dep in record.get("dependencies", []) if str(dep).strip()]
        if keep_only_internal_dependencies:
            kept_dependencies = [dep for dep in dependencies if dep in kept_decl_names]
            dependency_dropped += len(dependencies) - len(kept_dependencies)
        else:
            kept_dependencies = dependencies
        dependency_retained += len(kept_dependencies)

        updated = dict(record)
        updated["dependencies"] = kept_dependencies
        filtered_records.append(updated)

        decl_kind_counts[str(updated.get("decl_kind", ""))] += 1
        module_counts[str(updated.get("module_name", ""))] += 1

    stats = {
        "include_module_prefixes": include_module_prefixes,
        "keep_only_internal_dependencies": keep_only_internal_dependencies,
        "num_records": len(filtered_records),
        "num_unique_decl_names": len(kept_decl_names),
        "dependency_retained": dependency_retained,
        "dependency_dropped": dependency_dropped,
        "decl_kind_counts": dict(sorted(decl_kind_counts.items())),
        "top_module_counts": dict(module_counts.most_common(30)),
    }
    return filtered_records, stats


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Filter a normalized declaration trace by module prefixes.")
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    input_path = Path(config["input_path"])
    output_path = Path(config["output_path"])
    stats_path = Path(config["stats_path"])
    include_module_prefixes = [str(prefix) for prefix in config.get("include_module_prefixes", []) if str(prefix).strip()]
    keep_only_internal_dependencies = bool(config.get("keep_only_internal_dependencies", True))

    if not include_module_prefixes:
        raise ValueError("include_module_prefixes must be a non-empty list.")

    records = list(iter_jsonl(input_path))
    filtered_records, stats = filter_records(
        records=records,
        include_module_prefixes=include_module_prefixes,
        keep_only_internal_dependencies=keep_only_internal_dependencies,
    )
    stats["input_path"] = str(input_path)
    stats["output_path"] = str(output_path)
    stats["stats_path"] = str(stats_path)

    write_jsonl(output_path, filtered_records)
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    stats_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[done] records: {len(filtered_records)}")
    print(f"[done] output: {output_path}")
    print(f"[done] stats: {stats_path}")


if __name__ == "__main__":
    main()
