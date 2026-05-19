"""Ancestor Explanation Demo — Proof-side MVP CLI.

Loads T42 reviewed node embeddings and performs provenance-aware
ancestor retrieval ranking for declarations in reviewed candidate graphs.

This tool is the downstream manifestation of the provenance-conditional
finding (T42/T43), not an independent new contribution. It demonstrates
that edge provenance directly impacts the quality of hierarchy navigation
for proof engineers.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

# Ensure src directory is on path for common module import
_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

import numpy as np
from common import load_declaration_graph


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ancestor Explanation Demo: provenance-aware ancestor retrieval ranking",
    )
    parser.add_argument(
        "--declaration-name", required=True,
        help="Declaration identifier exactly as it appears in declarations.csv "
             "(e.g. c211948581bde9846a99e32d97a03f0d5307c31e::Subfield)",
    )
    parser.add_argument(
        "--candidate-graph", required=True,
        choices=["field_subfield", "order_ring"],
    )
    parser.add_argument(
        "--provenance-mode",
        choices=["explicit_only", "synthesized_only", "hierarchy_mixed"],
        help="Required unless --comparison-mode is explicit_vs_mixed",
    )
    parser.add_argument(
        "--model-type", required=True,
        choices=["gcn", "hgcn"],
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--comparison-mode", choices=["none", "explicit_vs_mixed"], default="none",
    )
    parser.add_argument(
        "--output-format", choices=["text", "json"], default="text",
    )
    parser.add_argument("--top-k", type=int, default=10)
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent


def _graph_dir(root: Path, candidate: str, provenance: str) -> Path:
    return root / f"data/processed/declaration_graph/mathlib_{candidate}_v1_{provenance}"


def _seed_dir(root: Path, model: str, candidate: str, provenance: str, seed: int) -> Path:
    prefix = f"provenance_{model}_{candidate}_{provenance}_t42"
    return (
        root / "artifacts/baselines/relation_seed_sweeps" / prefix
        / f"{prefix}_seed{seed}"
    )


def _fmt(val) -> str:
    if val is None:
        return "N/A"
    return f"{val:.4f}"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_graph(root: Path, candidate: str, provenance: str):
    gdir = _graph_dir(root, candidate, provenance)
    if not gdir.exists():
        raise FileNotFoundError(f"Graph directory not found: {gdir}")
    declarations, edges = load_declaration_graph(gdir)
    node_to_idx = {row["declaration_id"]: idx for idx, row in enumerate(declarations)}
    idx_to_node = {idx: row["declaration_id"] for idx, row in enumerate(declarations)}
    node_names = {row["declaration_id"]: row["decl_name"] for row in declarations}
    return declarations, edges, node_to_idx, idx_to_node, node_names


def load_embeddings(root: Path, model: str, candidate: str, provenance: str,
                    seed: int, expected_nodes: int):
    sdir = _seed_dir(root, model, candidate, provenance, seed)
    emb_path = sdir / "node_embeddings.npy"
    manifest_path = sdir / "run_manifest.json"

    if not emb_path.exists():
        raise FileNotFoundError(f"Embedding file not found: {emb_path}")

    embeddings = np.load(emb_path)

    if embeddings.shape[0] != expected_nodes:
        raise ValueError(
            f"Node ordering sanity check FAILED: embeddings have {embeddings.shape[0]} rows "
            f"but declarations.csv has {expected_nodes} rows. "
            "Aborting to prevent misaligned output."
        )

    manifest = None
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    return embeddings, manifest


# ---------------------------------------------------------------------------
# Ancestor graph
# ---------------------------------------------------------------------------

def build_parent_map(edges: list[dict]) -> dict[str, list[str]]:
    """src_id -> [dst_id] for extends edges (src extends dst => dst is parent)."""
    parents: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        if edge["edge_type"] == "extends":
            parents[edge["src_id"]].append(edge["dst_id"])
    return dict(parents)


def find_ancestors_bfs(query_id: str, parent_map: dict[str, list[str]]) -> dict[str, int]:
    """BFS returning {ancestor_id: min_hop_depth}."""
    ancestors: dict[str, int] = {}
    visited: set[str] = set()
    queue = [(query_id, 0)]
    while queue:
        node, depth = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        for parent in parent_map.get(node, []):
            if parent == query_id:
                continue
            if parent not in ancestors or depth + 1 < ancestors[parent]:
                ancestors[parent] = depth + 1
            if parent not in visited:
                queue.append((parent, depth + 1))
    return ancestors


# ---------------------------------------------------------------------------
# Scoring & metrics
# ---------------------------------------------------------------------------

def cosine_similarity(query_emb: np.ndarray, all_embs: np.ndarray) -> np.ndarray:
    qn = np.linalg.norm(query_emb)
    if qn == 0:
        return np.zeros(all_embs.shape[0])
    norms = np.linalg.norm(all_embs, axis=1)
    norms[norms == 0] = 1e-10
    return (all_embs @ query_emb) / (norms * qn)


def rank_and_score(query_idx: int, embeddings: np.ndarray,
                   node_to_idx: dict, idx_to_node: dict,
                   ground_truth: dict[str, int],
                   node_names: dict, top_k: int):
    sims = cosine_similarity(embeddings[query_idx], embeddings)
    order = np.argsort(-sims)
    query_id = idx_to_node[query_idx]
    gt_set = set(ground_truth)

    ranked = []
    rank = 0
    for idx in order:
        nid = idx_to_node[int(idx)]
        if nid == query_id:
            continue
        rank += 1
        ranked.append({
            "rank": rank,
            "declaration_id": nid,
            "decl_name": node_names.get(nid, nid),
            "score": float(sims[idx]),
            "is_true_ancestor": nid in gt_set,
            "hop_depth": ground_truth.get(nid),
            "relation_type": "extends" if nid in gt_set else None,
        })

    gt_count = len(gt_set)
    if gt_count == 0:
        metrics = {"map": None, "recall_at_1": None, "recall_at_3": None,
                    "recall_at_5": None, "recall_at_10": None,
                    "num_ground_truth": 0}
    else:
        hits = 0
        prec_sum = 0.0
        for item in ranked:
            if item["is_true_ancestor"]:
                hits += 1
                prec_sum += hits / item["rank"]
        ap = prec_sum / gt_count

        def _recall(k):
            top = [i for i in ranked if i["rank"] <= k]
            return sum(1 for i in top if i["is_true_ancestor"]) / gt_count

        metrics = {
            "map": float(ap),
            "recall_at_1": float(_recall(1)),
            "recall_at_3": float(_recall(3)),
            "recall_at_5": float(_recall(5)),
            "recall_at_10": float(_recall(10)),
            "num_ground_truth": gt_count,
        }

    hop_breakdown: dict[str, list] = {}
    for aid, depth in ground_truth.items():
        bucket = f"hop_{depth}" if depth <= 3 else "hop_4_plus"
        hop_breakdown.setdefault(bucket, []).append({
            "declaration_id": aid,
            "decl_name": node_names.get(aid, aid),
            "depth": depth,
        })

    return ranked[:top_k], metrics, hop_breakdown


# ---------------------------------------------------------------------------
# Single query
# ---------------------------------------------------------------------------

def run_single_query(root: Path, decl_name: str, candidate: str,
                     provenance: str, model: str, seed: int, top_k: int):
    decls, edges, n2i, i2n, names = load_graph(root, candidate, provenance)

    query_id = None
    for row in decls:
        if row["declaration_id"] == decl_name:
            query_id = row["declaration_id"]
            break
    if query_id is None:
        sample_ids = [row["declaration_id"] for row in decls[:3]]
        raise ValueError(
            f"Declaration '{decl_name}' not found in {candidate}/{provenance}. "
            f"Expected exact declaration_id format, e.g.: {sample_ids[0]}"
        )

    emb, manifest = load_embeddings(root, model, candidate, provenance, seed, len(decls))

    pmap = build_parent_map(edges)
    gt = find_ancestors_bfs(query_id, pmap)

    ranked, metrics, hop_bd = rank_and_score(
        n2i[query_id], emb, n2i, i2n, gt, names, top_k,
    )

    return {
        "query_declaration": query_id,
        "query_name": names.get(query_id, query_id),
        "candidate_graph": candidate,
        "provenance_mode": provenance,
        "model_type": model,
        "seed": seed,
        "ranked_ancestors": ranked,
        "ground_truth_ancestors": [
            {"declaration_id": aid, "decl_name": names.get(aid, aid), "hop_depth": d}
            for aid, d in sorted(gt.items(), key=lambda x: x[1])
        ],
        "metrics": metrics,
        "hop_depth_breakdown": hop_bd,
        "manifest_info": {
            "run_id": manifest.get("run_id") if manifest else None,
            "graph_root": manifest.get("graph_root") if manifest else None,
        },
    }


# ---------------------------------------------------------------------------
# Comparison mode
# ---------------------------------------------------------------------------

def run_comparison(root: Path, decl_name: str, candidate: str,
                   model: str, seed: int, top_k: int):
    r_explicit = run_single_query(root, decl_name, candidate, "explicit_only", model, seed, top_k)
    r_mixed = run_single_query(root, decl_name, candidate, "hierarchy_mixed", model, seed, top_k)

    exp_ids = {a["declaration_id"] for a in r_explicit["ranked_ancestors"]}
    mix_ids = {a["declaration_id"] for a in r_mixed["ranked_ancestors"]}

    only_explicit = exp_ids - mix_ids
    only_mixed = mix_ids - exp_ids

    def _name_lookup(result, aid):
        return next(
            (a["decl_name"] for a in result["ranked_ancestors"] if a["declaration_id"] == aid),
            aid,
        )

    em = r_explicit["metrics"]["map"]
    mm = r_mixed["metrics"]["map"]

    if em is not None and mm is not None:
        if em > mm:
            interp = (
                f"On explicit_only, {model.upper()} retrieves ancestors with higher quality "
                f"(MAP {em:.4f}) than on hierarchy_mixed (MAP {mm:.4f}). "
                "Synthesized edges dilute the hierarchical signal."
            )
        elif mm > em:
            interp = (
                f"On hierarchy_mixed, {model.upper()} retrieves ancestors with higher quality "
                f"(MAP {mm:.4f}) than on explicit_only (MAP {em:.4f}). "
                "Additional context from synthesized edges may help retrieval."
            )
        else:
            interp = "No quality difference between explicit_only and hierarchy_mixed."
    else:
        interp = "Insufficient ground truth ancestors for comparison."

    return {
        "query_declaration": r_explicit["query_declaration"],
        "query_name": r_explicit["query_name"],
        "candidate_graph": candidate,
        "model_type": model,
        "seed": seed,
        "explicit_only": r_explicit,
        "hierarchy_mixed": r_mixed,
        "comparison": {
            "only_in_explicit_top_k": [
                {"declaration_id": a, "decl_name": _name_lookup(r_explicit, a)}
                for a in only_explicit
            ],
            "only_in_mixed_top_k": [
                {"declaration_id": a, "decl_name": _name_lookup(r_mixed, a)}
                for a in only_mixed
            ],
        },
        "interpretation": interp,
    }


# ---------------------------------------------------------------------------
# Text formatting
# ---------------------------------------------------------------------------

def _format_single(result: dict) -> str:
    lines = []
    lines.append("=" * 72)
    lines.append("ANCESTOR EXPLANATION DEMO")
    lines.append("=" * 72)
    lines.append(f"Query:  {result['query_name']}")
    lines.append(f"        {result['query_declaration']}")
    lines.append(f"Graph:  {result['candidate_graph']}  |  "
                 f"Provenance: {result['provenance_mode']}")
    lines.append(f"Model:  {result['model_type'].upper()}  |  Seed: {result['seed']}")
    lines.append("-" * 72)

    gt = result["ground_truth_ancestors"]
    lines.append(f"Ground truth ancestors ({len(gt)}):")
    for a in gt:
        lines.append(f"  {a['decl_name']:<40} hop {a['hop_depth']}")

    lines.append(f"\nTop-{len(result['ranked_ancestors'])} ranked candidates:")
    lines.append(f"  {'Rank':>4}  {'Score':>8}  {'Name':<38}  {'GT':>2}  {'Hop':>4}")
    lines.append("  " + "-" * 64)
    for item in result["ranked_ancestors"]:
        gt_mark = " *" if item["is_true_ancestor"] else "  "
        hop = str(item["hop_depth"]) if item["hop_depth"] is not None else " -"
        lines.append(f"  {item['rank']:>4}  {item['score']:>8.4f}  "
                     f"{item['decl_name']:<38} {gt_mark}  {hop:>4}")

    m = result["metrics"]
    lines.append(f"\nRetrieval Metrics (single query):")
    lines.append(f"  MAP:       {_fmt(m['map'])}")
    lines.append(f"  Recall@1:  {_fmt(m['recall_at_1'])}")
    lines.append(f"  Recall@3:  {_fmt(m['recall_at_3'])}")
    lines.append(f"  Recall@5:  {_fmt(m['recall_at_5'])}")
    lines.append(f"  Recall@10: {_fmt(m['recall_at_10'])}")

    hbd = result.get("hop_depth_breakdown", {})
    if hbd:
        lines.append(f"\nHop Depth Breakdown:")
        for bucket in ["hop_1", "hop_2", "hop_3", "hop_4_plus"]:
            if bucket in hbd:
                names_str = ", ".join(a["decl_name"] for a in hbd[bucket])
                lines.append(f"  {bucket}: {len(hbd[bucket])} ancestors — {names_str}")

    mi = result.get("manifest_info", {})
    if mi.get("run_id"):
        lines.append(f"\nArtifact: {mi['run_id']}")
        lines.append(f"Graph:    {mi.get('graph_root', 'N/A')}")

    lines.append("=" * 72)
    return "\n".join(lines)


def _format_comparison(result: dict) -> str:
    lines = []
    lines.append("=" * 72)
    lines.append("ANCESTOR EXPLANATION DEMO — PROVENANCE COMPARISON")
    lines.append("=" * 72)
    lines.append(f"Query:  {result['query_name']}")
    lines.append(f"        {result['query_declaration']}")
    lines.append(f"Graph:  {result['candidate_graph']}  |  "
                 f"Model: {result['model_type'].upper()}  |  Seed: {result['seed']}")
    lines.append("=" * 72)

    for mode_key, mode_label in [("explicit_only", "EXPLICIT ONLY"),
                                  ("hierarchy_mixed", "HIERARCHY MIXED")]:
        r = result[mode_key]
        m = r["metrics"]
        lines.append(f"\n--- {mode_label} ---")
        lines.append(f"  Ground truth ancestors: {m['num_ground_truth']}")
        lines.append(f"  MAP={_fmt(m['map'])}  R@1={_fmt(m['recall_at_1'])}  "
                     f"R@3={_fmt(m['recall_at_3'])}  R@10={_fmt(m['recall_at_10'])}")
        lines.append(f"  Top-{len(r['ranked_ancestors'])} candidates:")
        for item in r["ranked_ancestors"]:
            gt_mark = "*" if item["is_true_ancestor"] else " "
            hop = str(item["hop_depth"]) if item["hop_depth"] is not None else "-"
            lines.append(f"    {item['rank']:>3}  {item['score']:>8.4f}  "
                         f"{item['decl_name']:<36} {gt_mark} hop={hop}")

    comp = result["comparison"]
    lines.append(f"\n--- TOP-K DIFF ---")
    oe = comp["only_in_explicit_top_k"]
    om = comp["only_in_mixed_top_k"]
    lines.append(f"  Only in explicit_only top-k ({len(oe)}):")
    for a in oe:
        lines.append(f"    + {a['decl_name']}")
    if not oe:
        lines.append("    (none)")
    lines.append(f"  Only in hierarchy_mixed top-k ({len(om)}):")
    for a in om:
        lines.append(f"    + {a['decl_name']}")
    if not om:
        lines.append("    (none)")

    lines.append(f"\nInterpretation: {result['interpretation']}")
    lines.append("=" * 72)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    root = _project_root()

    try:
        if args.comparison_mode == "explicit_vs_mixed":
            result = run_comparison(
                root, args.declaration_name, args.candidate_graph,
                args.model_type, args.seed, args.top_k,
            )
            if args.output_format == "json":
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(_format_comparison(result))
        else:
            if args.provenance_mode is None:
                print("ERROR: --provenance-mode is required when --comparison-mode is none",
                      file=sys.stderr)
                sys.exit(1)
            result = run_single_query(
                root, args.declaration_name, args.candidate_graph,
                args.provenance_mode, args.model_type, args.seed, args.top_k,
            )
            if args.output_format == "json":
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(_format_single(result))
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
