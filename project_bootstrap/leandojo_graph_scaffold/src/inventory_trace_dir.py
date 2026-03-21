from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def inventory_trace_dir(trace_root: Path) -> dict:
    suffix_counter: Counter[str] = Counter()
    depth_counter: Counter[int] = Counter()
    sample_files: list[dict] = []
    total_files = 0
    total_dirs = 0

    for path in trace_root.rglob("*"):
        if path.is_dir():
            total_dirs += 1
            continue
        total_files += 1
        rel_path = path.relative_to(trace_root)
        depth = len(rel_path.parts)
        suffix = "".join(path.suffixes) or "<no_suffix>"
        suffix_counter[suffix] += 1
        depth_counter[depth] += 1

        if len(sample_files) < 50:
            sample_files.append(
                {
                    "relative_path": str(rel_path),
                    "suffix": suffix,
                    "size_bytes": path.stat().st_size,
                }
            )

    return {
        "trace_root": str(trace_root),
        "total_files": total_files,
        "total_dirs": total_dirs,
        "suffix_counts": dict(sorted(suffix_counter.items())),
        "depth_counts": dict(sorted(depth_counter.items())),
        "sample_files": sample_files,
    }


def write_outputs(output_root: Path, summary: dict) -> None:
    output_root.mkdir(parents=True, exist_ok=True)

    summary_path = output_root / "inventory_summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    csv_path = output_root / "inventory_suffix_counts.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["suffix", "count"])
        for suffix, count in summary["suffix_counts"].items():
            writer.writerow([suffix, count])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory a LeanDojo trace directory before writing any parser."
    )
    parser.add_argument("--trace-root", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = inventory_trace_dir(args.trace_root)
    write_outputs(args.output_root, summary)
    print(f"[done] inventory written to: {args.output_root}")


if __name__ == "__main__":
    main()
