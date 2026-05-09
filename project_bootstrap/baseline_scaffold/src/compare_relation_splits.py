"""Compare structural diagnostics and baseline results across relation provenance splits.

Reads:
  - artifacts/diagnostics/relation_split_v1/summary.json
  - artifacts/diagnostics/task_structure_relation_split_v1/summary.json
  - artifacts/baselines/relation_seed_sweeps/*/aggregate_summary.json

Outputs:
  - artifacts/diagnostics/relation_split_comparison/report.md
  - artifacts/diagnostics/relation_split_comparison/summary.json
"""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

SPLIT_ORDER = ["explicit_only", "synthesized_only", "hierarchy_mixed", "full_with_uses"]
SPLIT_LABELS = {
    "explicit_only": "explicit (extends only)",
    "synthesized_only": "synthesized (instance_of only)",
    "hierarchy_mixed": "mixed (extends + instance_of)",
    "full_with_uses": "full (+ uses edges)",
}


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def extract_structure_metrics(diagnostics: dict) -> list[dict]:
    rows = []
    graphs = diagnostics.get("graphs", diagnostics.get("summary", {}))
    if isinstance(graphs, list):
        for g in graphs:
            name = g.get("graph_name", g.get("name", ""))
            split = name.replace("batteries_", "").replace("_reference", "")
            if split not in SPLIT_ORDER:
                continue
            rel = g.get("relation_structure", g.get("full_structure", {}))
            hyp = rel.get("largest_component_diagnostics", {}).get("hyperbolicity_proxy", {})
            rows.append({
                "split": split,
                "label": SPLIT_LABELS.get(split, split),
                "nodes": g.get("summary", {}).get("num_declarations", rel.get("num_nodes", 0)),
                "edges": g.get("summary", {}).get("num_edges", rel.get("num_edges", 0)),
                "longest_chain": rel.get("condensation_longest_path", "N/A"),
                "weak_components": rel.get("weak_component_summary", {}).get("count", "N/A"),
                "largest_component": rel.get("weak_component_summary", {}).get("largest", "N/A"),
                "multi_parent": rel.get("multi_parent_count", "N/A"),
                "leaf_count": rel.get("leaf_count_in_degree_zero", "N/A"),
                "delta_maxdist": hyp.get("delta_over_maxdist", "N/A"),
            })
    return rows


def extract_task_metrics(task_diag: dict) -> list[dict]:
    rows = []
    analyses = task_diag.get("analyses", [])
    for a in analyses:
        name = a.get("name", "")
        split = name.replace("_gcn", "").replace("_hgcn", "")
        test = a.get("split_diagnostics", {}).get("test", {})
        rows.append({
            "split": split,
            "label": SPLIT_LABELS.get(split, split),
            "test_queries": test.get("num_queries", "N/A"),
            "unique_sources": test.get("unique_sources", "N/A"),
            "avg_positives_per_sr": test.get("positives_per_source_relation_summary", {}).get("mean", "N/A"),
            "avg_non_target": test.get("non_target_true_ancestors_summary", {}).get("mean", "N/A"),
            "random_mrr": test.get("random_ranking_baseline", {}).get("mrr", {}).get("mean", "N/A"),
            "ceiling_mrr": test.get("positive_block_ceiling", {}).get("mrr", {}).get("mean", "N/A"),
        })
    return rows


def extract_baseline_metrics(sweep_root: Path) -> list[dict]:
    rows = []
    for sweep_dir in sorted(sweep_root.iterdir()):
        if not sweep_dir.is_dir():
            continue
        agg_path = sweep_dir / "aggregate.json"
        if not agg_path.exists():
            agg_path = sweep_dir / "aggregate_summary.json"
        agg = load_json(agg_path)
        if not agg:
            continue

        dir_name = sweep_dir.name
        if "explicit_only" in dir_name:
            split = "explicit_only"
        elif "synthesized_only" in dir_name:
            split = "synthesized_only"
        elif "hierarchy_mixed" in dir_name:
            split = "hierarchy_mixed"
        else:
            continue

        model = "HGCN" if "hgcn" in dir_name else "GCN"

        metrics = agg.get("metrics", {})
        def get_metric(name: str) -> str:
            m = metrics.get(name, {})
            mean = m.get("mean")
            std = m.get("std")
            if mean is None:
                return "N/A"
            if std is None:
                return f"{mean:.4f}"
            return f"{mean:.4f} +/- {std:.4f}"

        rows.append({
            "split": split,
            "label": SPLIT_LABELS.get(split, split),
            "model": model,
            "test_ap": get_metric("test_average_precision"),
            "test_auroc": get_metric("test_auroc"),
            "cal_f1": get_metric("calibrated_test_f1"),
            "test_mrr": get_metric("ranking_test_mrr"),
            "g_map": get_metric("grouped_test_map"),
            "g_ndcg": get_metric("grouped_test_ndcg"),
            "g_mrr": get_metric("grouped_test_mrr"),
            "r_at_10": get_metric("grouped_test_recall_at_10"),
        })
    return rows


def fmt(value) -> str:
    if value is None or value == "N/A":
        return "N/A"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def build_report(
    structure_rows: list[dict],
    task_rows: list[dict],
    baseline_rows: list[dict],
) -> str:
    lines = ["# Relation Provenance Split Comparison", ""]

    # Structure table
    lines += [
        "## 1. Structural Diagnostics",
        "",
        "| split | nodes | edges | longest chain | components | largest comp | multi-parent | leaves | δ/diam |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in sorted(structure_rows, key=lambda x: SPLIT_ORDER.index(x["split"]) if x["split"] in SPLIT_ORDER else 99):
        lines.append(
            f"| {r['label']} | {r['nodes']} | {r['edges']} | {fmt(r['longest_chain'])} | "
            f"{fmt(r['weak_components'])} | {fmt(r['largest_component'])} | {fmt(r['multi_parent'])} | "
            f"{fmt(r['leaf_count'])} | {fmt(r['delta_maxdist'])} |"
        )
    lines.append("")

    # Task structure table
    lines += [
        "## 2. Task Structure",
        "",
        "| split | test queries | unique sources | avg positives/src-rel | avg non-target ancestors | random MRR | ceiling MRR |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in sorted(task_rows, key=lambda x: SPLIT_ORDER.index(x["split"]) if x["split"] in SPLIT_ORDER else 99):
        lines.append(
            f"| {r['label']} | {r['test_queries']} | {r['unique_sources']} | "
            f"{fmt(r['avg_positives_per_sr'])} | {fmt(r['avg_non_target'])} | "
            f"{fmt(r['random_mrr'])} | {fmt(r['ceiling_mrr'])} |"
        )
    lines.append("")

    # Baseline results table
    if baseline_rows:
        lines += [
            "## 3. Baseline Results (5-seed aggregate)",
            "",
            "| split | model | test AP | test AUROC | cal F1 | grouped MAP | grouped nDCG | grouped MRR | R@10 |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for r in sorted(
            baseline_rows,
            key=lambda x: (SPLIT_ORDER.index(x["split"]) if x["split"] in SPLIT_ORDER else 99, x["model"]),
        ):
            lines.append(
                f"| {r['label']} | {r['model']} | {r['test_ap']} | {r['test_auroc']} | "
                f"{r['cal_f1']} | {r['g_map']} | {r['g_ndcg']} | {r['g_mrr']} | {r['r_at_10']} |"
            )
        lines.append("")
    else:
        lines += [
            "## 3. Baseline Results",
            "",
            "No seed sweep results found yet. Run the seed sweep experiments first.",
            "",
        ]

    return "\n".join(lines) + "\n"


def main() -> None:
    print("Loading diagnostics data...")

    struct_diag = load_json(REPO_ROOT / "artifacts/diagnostics/relation_split_v1/summary.json")
    task_diag = load_json(REPO_ROOT / "artifacts/diagnostics/task_structure_relation_split_v1/summary.json")

    structure_rows = extract_structure_metrics(struct_diag) if struct_diag else []
    task_rows = extract_task_metrics(task_diag) if task_diag else []
    baseline_rows = extract_baseline_metrics(REPO_ROOT / "artifacts/baselines/relation_seed_sweeps")

    report = build_report(structure_rows, task_rows, baseline_rows)

    out_dir = REPO_ROOT / "artifacts/diagnostics/relation_split_comparison"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.md").write_text(report, encoding="utf-8")

    summary = {
        "structure": structure_rows,
        "task_structure": task_rows,
        "baselines": baseline_rows,
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"Report written to: {out_dir / 'report.md'}")
    print("\n" + report)


if __name__ == "__main__":
    main()
