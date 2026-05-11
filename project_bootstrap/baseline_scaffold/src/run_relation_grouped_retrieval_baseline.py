"""Relation-aware grouped retrieval training with InfoNCE loss.

Replaces binary edge classification with query-grouped softmax training,
aligning the training objective with grouped multi-positive retrieval evaluation.
Supports both GCN and HGCN encoders via ``model_type`` config flag.
"""

from __future__ import annotations

import argparse
import copy
import random
from collections import defaultdict
from pathlib import Path

from common import load_config, set_global_random_seed, write_json
from eval_utils import build_calibrated_metrics, summarize_score_distribution
from relation_baseline_common import (
    build_edge_tensors,
    build_ranking_task_metrics,
    build_relation_aware_adjacency,
    build_relation_type_index,
    evaluate_split,
    fmt_metric,
    import_training_deps,
    load_relation_split_triplets,
    prepare_relation_run_data,
)
from relation_tasks import build_message_edges_for_training
from run_relation_gcn_baseline import RelationAwareGCNLinkPredictor
from run_relation_hyperbolic_baseline import RelationAwareHyperbolicLinkPredictor


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Grouped retrieval training with InfoNCE loss."
    )
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


# ---------------------------------------------------------------------------
# query group construction
# ---------------------------------------------------------------------------

def build_query_groups(
    split_examples: list[tuple],
    all_positive_set: set[tuple],
    candidate_pools: dict[str, list[str]],
    negative_ratio: float,
    rng: random.Random,
) -> list[dict]:
    """Organize training examples into query groups for grouped softmax.

    Each group: (src, relation) -> {positives, negatives}.
    """
    grouped: dict[tuple, list[str]] = defaultdict(list)
    for src, dst, rel, label in split_examples:
        if label == 1:
            grouped[(src, rel)].append(dst)

    query_groups: list[dict] = []
    for (src, rel), positives in grouped.items():
        pool = candidate_pools.get(rel, [])
        # Exclude true positives and self from negative candidates
        neg_candidates = [
            c for c in pool
            if c != src and (src, c, rel) not in all_positive_set
        ]
        n_neg = max(1, int(len(positives) * negative_ratio))
        if len(neg_candidates) < n_neg:
            neg_sample = list(neg_candidates)
        else:
            neg_sample = rng.sample(neg_candidates, n_neg)

        query_groups.append({
            "src": src,
            "relation": rel,
            "positives": positives,
            "negatives": neg_sample,
        })
    return query_groups


def resample_negatives(
    query_groups: list[dict],
    all_positive_set: set[tuple],
    candidate_pools: dict[str, list[str]],
    negative_ratio: float,
    rng: random.Random,
) -> list[dict]:
    """Resample negatives for existing query groups (keeps positives fixed)."""
    new_groups = []
    for g in query_groups:
        src, rel, positives = g["src"], g["relation"], g["positives"]
        pool = candidate_pools.get(rel, [])
        neg_candidates = [
            c for c in pool
            if c != src and (src, c, rel) not in all_positive_set
        ]
        n_neg = max(1, int(len(positives) * negative_ratio))
        if len(neg_candidates) < n_neg:
            neg_sample = list(neg_candidates)
        else:
            neg_sample = rng.sample(neg_candidates, n_neg)
        new_groups.append({
            "src": src,
            "relation": rel,
            "positives": positives,
            "negatives": neg_sample,
        })
    return new_groups


# ---------------------------------------------------------------------------
# grouped softmax loss
# ---------------------------------------------------------------------------

def grouped_softmax_loss(scores, positive_mask, torch, F):
    """InfoNCE: negative mean log-prob of positives under softmax over candidates."""
    log_probs = F.log_softmax(scores, dim=0)
    pos_log_probs = log_probs[positive_mask]
    if pos_log_probs.numel() == 0:
        return torch.tensor(0.0, requires_grad=True)
    return -pos_log_probs.mean()


# ---------------------------------------------------------------------------
# training loop
# ---------------------------------------------------------------------------

def train_grouped_retrieval(
    model,
    adjacency_by_relation,
    query_groups_train,
    query_groups_val,
    node_to_idx,
    relation_to_idx,
    candidate_pools,
    all_positive_set,
    split_examples_val_ranking,
    data,
    config: dict,
    torch,
    F,
    accuracy_score,
    average_precision_score,
    f1_score,
    roc_auc_score,
    negative_ratio: float,
    resample_negatives_flag: bool,
):
    learning_rate = float(config.get("learning_rate", 0.01))
    weight_decay = float(config.get("weight_decay", 1e-4))
    epochs = int(config.get("epochs", 80))
    eval_every = int(config.get("eval_every", 5))
    early_stopping_patience = int(config.get("early_stopping_patience", 8))

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    rng = random.Random(int(config["seed"]) + 1)
    history: list[dict] = []
    best_state = None
    best_epoch = 0
    best_val_grouped_map = float("-inf")
    patience = 0

    for epoch in range(1, epochs + 1):
        model.train()

        if resample_negatives_flag and epoch > 1:
            query_groups_train = resample_negatives(
                query_groups_train, all_positive_set, candidate_pools,
                negative_ratio, rng,
            )

        embeddings = model.encode(adjacency_by_relation)
        total_loss = torch.tensor(0.0)
        n_queries = 0

        for g in query_groups_train:
            src_idx = node_to_idx[g["src"]]
            rel_idx = relation_to_idx[g["relation"]]
            all_dst = g["positives"] + g["negatives"]
            pos_mask = [True] * len(g["positives"]) + [False] * len(g["negatives"])

            dst_indices = [node_to_idx[d] for d in all_dst if d in node_to_idx]
            if len(dst_indices) != len(all_dst):
                valid = [d for d in all_dst if d in node_to_idx]
                valid_pos = [d for d in g["positives"] if d in node_to_idx]
                pos_mask = [True] * len(valid_pos) + [False] * (len(valid) - len(valid_pos))
                all_dst = valid
                dst_indices = [node_to_idx[d] for d in all_dst]

            if not any(pos_mask):
                continue

            edge_index = torch.tensor(
                [[src_idx, di] for di in dst_indices], dtype=torch.long
            )
            rel_ids = torch.tensor([rel_idx] * len(dst_indices), dtype=torch.long)
            pos_mask_t = torch.tensor(pos_mask, dtype=torch.bool)

            scores = model.decode(embeddings, edge_index, rel_ids)
            total_loss = total_loss + grouped_softmax_loss(scores, pos_mask_t, torch, F)
            n_queries += 1

        if n_queries > 0:
            avg_loss = total_loss / n_queries
        else:
            avg_loss = total_loss

        optimizer.zero_grad()
        avg_loss.backward()
        optimizer.step()

        epoch_record = {"epoch": epoch, "train_loss": float(avg_loss.detach().item())}

        should_eval = epoch == 1 or epoch % eval_every == 0 or epoch == epochs
        if should_eval:
            model.eval()
            with torch.no_grad():
                eval_embeddings = model.encode(adjacency_by_relation)
                eval_emb_np = eval_embeddings.detach().cpu().numpy()
                eval_emb_t = torch.tensor(eval_emb_np, dtype=torch.float32)

            # Binary metrics for logging
            val_edges_t, val_rel_t, val_labels_t = build_edge_tensors(
                split_examples_val_ranking, node_to_idx, relation_to_idx, torch
            )
            with torch.no_grad():
                val_logits = model.decode(eval_emb_t, val_edges_t, val_rel_t)
            val_metrics = evaluate_split(
                val_logits, val_labels_t,
                accuracy_score, average_precision_score, f1_score, roc_auc_score,
            )

            # Grouped retrieval metrics for model selection
            ranking_metrics = build_ranking_task_metrics(
                model=model,
                embeddings=eval_emb_t,
                split_examples={
                    "val": split_examples_val_ranking,
                    "test": [],
                },
                relation_candidate_pools=data["relation_candidate_pools"],
                node_to_idx=node_to_idx,
                relation_to_idx=relation_to_idx,
                positive_hop_lookup=data["positive_hop_lookup"],
                torch=torch,
            )
            val_grouped_map = ranking_metrics["val"].get("grouped", {}).get("map")
            epoch_record["val_ap"] = val_metrics["average_precision"]
            epoch_record["val_grouped_map"] = val_grouped_map

            print(
                f"[epoch {epoch}/{epochs}] "
                f"train_loss={epoch_record['train_loss']:.6f} "
                f"val AP={fmt_metric(val_metrics['average_precision'])} "
                f"val gMAP={fmt_metric(val_grouped_map)}"
            )

            current_metric = val_grouped_map if val_grouped_map is not None else float("-inf")
            if current_metric > best_val_grouped_map:
                best_val_grouped_map = current_metric
                best_epoch = epoch
                patience = 0
                best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            else:
                patience += 1
                if patience >= early_stopping_patience:
                    history.append(epoch_record)
                    print(f"[early-stop] no validation grouped MAP improvement for {early_stopping_patience} evals")
                    break
        else:
            print(f"[epoch {epoch}/{epochs}] train_loss={epoch_record['train_loss']:.6f}")
        history.append(epoch_record)

    if best_state is not None:
        model.load_state_dict(best_state)

    model.eval()
    with torch.no_grad():
        final_embeddings = model.encode(adjacency_by_relation)
    return final_embeddings.detach().cpu().numpy(), {
        "best_epoch": best_epoch,
        "best_val_grouped_map": None if best_val_grouped_map == float("-inf") else float(best_val_grouped_map),
        "training_loss": "grouped_softmax",
        "history": history,
    }


# ---------------------------------------------------------------------------
# main experiment runner
# ---------------------------------------------------------------------------

def run_grouped_retrieval_experiment(config: dict) -> dict:
    data = prepare_relation_run_data(config)
    artifacts_root = data["artifacts_root"]

    if config.get("dry_run", False):
        notes = {"mode": "dry_run", "message": "Grouped retrieval dry run."}
        write_json(artifacts_root / "grouped_retrieval_dry_run.json", notes)
        return {"config": copy.deepcopy(config), "metrics": None}

    (np, torch, F, accuracy_score, average_precision_score,
     f1_score, roc_auc_score) = import_training_deps()
    seed_status = set_global_random_seed(int(config["seed"]), np=np, torch=torch)

    declarations = data["declarations"]
    edges = data["edges"]
    prediction_relation_types = data["prediction_relation_types"]
    message_relation_types = data["message_relation_types"]
    relation_to_idx = build_relation_type_index(prediction_relation_types)
    message_relation_to_idx = build_relation_type_index(message_relation_types)
    node_ids = [row["declaration_id"] for row in declarations]
    node_to_idx = {nid: idx for idx, nid in enumerate(node_ids)}

    split_examples = load_relation_split_triplets(artifacts_root)
    held_out_direct_examples = {
        (src, dst, rel)
        for split_name in ["val", "test"]
        for src, dst, rel, label in split_examples[split_name]
        if label == 1 and rel in set(message_relation_types)
    }
    message_edges = build_message_edges_for_training(
        edges=edges,
        message_relation_types=message_relation_types,
        held_out_direct_examples=held_out_direct_examples,
        exclude_held_out_direct_edges=bool(config.get("exclude_held_out_direct_edges", True)),
    )
    indexed_message_edges = []
    for row in message_edges:
        if row["edge_type"] not in message_relation_to_idx:
            continue
        if row["src_id"] not in node_to_idx or row["dst_id"] not in node_to_idx:
            continue
        indexed_message_edges.append({
            **row,
            "src_idx": node_to_idx[row["src_id"]],
            "dst_idx": node_to_idx[row["dst_id"]],
        })
    adjacency_by_relation = build_relation_aware_adjacency(
        num_nodes=len(node_ids),
        train_message_edges=indexed_message_edges,
        relation_to_idx=message_relation_to_idx,
        symmetrize=bool(config.get("symmetrize_graph", True)),
        torch=torch,
    )

    # Build all-positive set for negative exclusion
    all_positive_set = set()
    for split_name in ["train", "val", "test"]:
        for src, dst, rel, label in split_examples[split_name]:
            if label == 1:
                all_positive_set.add((src, dst, rel))

    negative_ratio = float(config.get("negative_ratio", 10.0))
    resample_flag = bool(config.get("resample_negatives_every_epoch", True))
    rng = random.Random(int(config["seed"]))

    train_positives = [
        (src, dst, rel, label)
        for src, dst, rel, label in split_examples["train"]
        if label == 1
    ]
    query_groups_train = build_query_groups(
        train_positives, all_positive_set,
        data["relation_candidate_pools"], negative_ratio, rng,
    )
    print(f"[info] {len(query_groups_train)} query groups in training set")

    # Build model
    model_type = str(config.get("model_type", "gcn")).lower()
    if model_type == "hgcn":
        model = RelationAwareHyperbolicLinkPredictor(
            num_nodes=len(node_ids),
            prediction_relation_types=prediction_relation_types,
            message_relation_types=message_relation_types,
            config=config,
            torch=torch,
            F=F,
        )
        model_label = "hyperbolic"
    else:
        model = RelationAwareGCNLinkPredictor(
            num_nodes=len(node_ids),
            prediction_relation_types=prediction_relation_types,
            message_relation_types=message_relation_types,
            config=config,
            torch=torch,
        )
        model_label = "gcn"

    # Train
    embeddings, train_stats = train_grouped_retrieval(
        model=model,
        adjacency_by_relation=adjacency_by_relation,
        query_groups_train=query_groups_train,
        query_groups_val=None,
        node_to_idx=node_to_idx,
        relation_to_idx=relation_to_idx,
        candidate_pools=data["relation_candidate_pools"],
        all_positive_set=all_positive_set,
        split_examples_val_ranking=split_examples["val"],
        data=data,
        config=config,
        torch=torch,
        F=F,
        accuracy_score=accuracy_score,
        average_precision_score=average_precision_score,
        f1_score=f1_score,
        roc_auc_score=roc_auc_score,
        negative_ratio=negative_ratio,
        resample_negatives_flag=resample_flag,
    )

    np.save(artifacts_root / "node_embeddings.npy", embeddings)
    write_json(artifacts_root / "training_stats.json", train_stats)

    # Final evaluation
    with torch.no_grad():
        final_emb = torch.tensor(embeddings, dtype=torch.float32)
        val_edges_t, val_rel_t, val_labels_t = build_edge_tensors(
            split_examples["val"], node_to_idx, relation_to_idx, torch
        )
        test_edges_t, test_rel_t, test_labels_t = build_edge_tensors(
            split_examples["test"], node_to_idx, relation_to_idx, torch
        )
        val_logits = model.decode(final_emb, val_edges_t, val_rel_t)
        test_logits = model.decode(final_emb, test_edges_t, test_rel_t)

    metrics = {
        "val": evaluate_split(val_logits, val_labels_t, accuracy_score, average_precision_score, f1_score, roc_auc_score),
        "test": evaluate_split(test_logits, test_labels_t, accuracy_score, average_precision_score, f1_score, roc_auc_score),
    }
    metrics.update(build_calibrated_metrics(val_logits, val_labels_t, test_logits, test_labels_t, torch))
    if str(config["task"]) in {"parent_prediction", "ancestor_ranking"}:
        metrics["ranking"] = build_ranking_task_metrics(
            model=model,
            embeddings=final_emb,
            split_examples=split_examples,
            relation_candidate_pools=data["relation_candidate_pools"],
            node_to_idx=node_to_idx,
            relation_to_idx=relation_to_idx,
            positive_hop_lookup=data["positive_hop_lookup"],
            torch=torch,
        )
    write_json(artifacts_root / "metrics.json", metrics)

    # Result summary
    result_summary = {
        "run_id": config["run_id"],
        "task": config["task"],
        "model_type": model_type,
        "training_loss": "grouped_softmax",
        "relations": prediction_relation_types,
        "best_epoch": train_stats["best_epoch"],
        "val_average_precision": metrics["val"]["average_precision"],
        "val_auroc": metrics["val"]["auroc"],
        "test_average_precision": metrics["test"]["average_precision"],
        "test_auroc": metrics["test"]["auroc"],
        "test_f1": metrics["test"]["f1"],
        "calibrated_test_f1": metrics["calibrated"]["test"]["f1"],
    }
    if "ranking" in metrics:
        result_summary["ranking_test_mrr"] = metrics["ranking"]["test"]["mrr"]
        result_summary["ranking_test_hits_at_1"] = metrics["ranking"]["test"]["hits_at_1"]
        result_summary["ranking_test_hits_at_10"] = metrics["ranking"]["test"]["hits_at_10"]
        grouped = metrics["ranking"]["test"].get("grouped", {})
        result_summary["grouped_test_map"] = grouped.get("map")
        result_summary["grouped_test_ndcg"] = grouped.get("ndcg")
        result_summary["grouped_test_ndcg_at_10"] = grouped.get("ndcg_at_10")
        result_summary["grouped_test_mrr"] = grouped.get("grouped_mrr")
        result_summary["grouped_test_recall_at_1"] = grouped.get("recall_at_1")
        result_summary["grouped_test_recall_at_3"] = grouped.get("recall_at_3")
        result_summary["grouped_test_recall_at_5"] = grouped.get("recall_at_5")
        result_summary["grouped_test_recall_at_10"] = grouped.get("recall_at_10")
    write_json(artifacts_root / "result_summary.json", result_summary)

    print(f"[done] relation-aware {model_label} grouped retrieval training completed")
    print(f"[done] task: {config['task']}, loss: grouped_softmax")
    print(f"[done] relations: {', '.join(prediction_relation_types)}")
    print(f"[done] val AP: {fmt_metric(metrics['val']['average_precision'])}")
    print(f"[done] test AP: {fmt_metric(metrics['test']['average_precision'])}")
    if "ranking" in metrics:
        grouped = metrics["ranking"]["test"].get("grouped", {})
        print(f"[done] test MRR: {fmt_metric(metrics['ranking']['test']['mrr'])}")
        print(f"[done] grouped test MAP: {fmt_metric(grouped.get('map'))}")
        print(f"[done] grouped test Recall@10: {fmt_metric(grouped.get('recall_at_10'))}")
    print(f"[done] artifacts: {artifacts_root}")

    return {
        "config": copy.deepcopy(config),
        "artifacts_root": str(artifacts_root),
        "metrics": metrics,
        "training_stats": train_stats,
        "result_summary": result_summary,
    }


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    run_grouped_retrieval_experiment(config)


if __name__ == "__main__":
    main()
