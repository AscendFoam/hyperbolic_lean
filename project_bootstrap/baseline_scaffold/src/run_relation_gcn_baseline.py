from __future__ import annotations

import argparse
import copy

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


def flatten_grouped_hop_bucket_summary(grouped: dict) -> dict[str, float | None]:
    flattened: dict[str, float | None] = {}
    hop_buckets = grouped.get("hop_buckets", {})
    for bucket_name in ["hop_2", "hop_3", "hop_4_plus"]:
        bucket_metrics = hop_buckets.get(bucket_name, {})
        for metric_name in [
            "map",
            "ndcg",
            "grouped_mrr",
            "recall_at_1",
            "recall_at_3",
            "recall_at_5",
            "recall_at_10",
        ]:
            flattened[f"{bucket_name}_{metric_name}"] = bucket_metrics.get(metric_name, {}).get("mean")
    return flattened


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Relation-aware pure PyTorch GCN baseline.")
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


class RelationAwareGCNLinkPredictor:
    def __init__(
        self,
        num_nodes: int,
        prediction_relation_types: list[str],
        message_relation_types: list[str],
        config: dict,
        torch,
    ):
        input_dim = int(config.get("input_dim", 16))
        hidden_dim = int(config.get("hidden_dim", 16))
        output_dim = int(config.get("output_dim", 16))
        dropout = float(config.get("dropout", 0.2))
        prediction_relation_count = len(prediction_relation_types)
        message_relation_count = len(message_relation_types)

        class _Model(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.node_features = torch.nn.Parameter(torch.empty(num_nodes, input_dim))
                self.self_loop_weight = torch.nn.Linear(input_dim, hidden_dim, bias=False)
                self.rel_lin1 = torch.nn.ModuleList(
                    [torch.nn.Linear(input_dim, hidden_dim, bias=False) for _ in range(message_relation_count)]
                )
                self.rel_lin2 = torch.nn.ModuleList(
                    [torch.nn.Linear(hidden_dim, output_dim, bias=False) for _ in range(message_relation_count)]
                )
                self.self_loop_out = torch.nn.Linear(hidden_dim, output_dim, bias=False)
                self.relation_embeddings = torch.nn.Embedding(prediction_relation_count, output_dim)
                self.decoder = torch.nn.Sequential(
                    torch.nn.Linear(output_dim * 3, hidden_dim),
                    torch.nn.ReLU(),
                    torch.nn.Dropout(p=dropout),
                    torch.nn.Linear(hidden_dim, 1),
                )
                self.dropout = dropout
                torch.nn.init.xavier_uniform_(self.node_features)
                torch.nn.init.xavier_uniform_(self.self_loop_weight.weight)
                torch.nn.init.xavier_uniform_(self.self_loop_out.weight)
                torch.nn.init.xavier_uniform_(self.relation_embeddings.weight)
                for module in list(self.rel_lin1) + list(self.rel_lin2):
                    torch.nn.init.xavier_uniform_(module.weight)
                for module in self.decoder:
                    if isinstance(module, torch.nn.Linear):
                        torch.nn.init.xavier_uniform_(module.weight)
                        if module.bias is not None:
                            torch.nn.init.zeros_(module.bias)

            def _aggregate(self, adjacency_by_relation, inputs, linear_layers, skip_layer):
                outputs = skip_layer(inputs)
                for relation_idx, adjacency in adjacency_by_relation.items():
                    relation_inputs = torch.sparse.mm(adjacency, inputs)
                    outputs = outputs + linear_layers[relation_idx](relation_inputs)
                return outputs

            def encode(self, adjacency_by_relation):
                h = self._aggregate(adjacency_by_relation, self.node_features, self.rel_lin1, self.self_loop_weight)
                h = torch.relu(h)
                h = torch.nn.functional.dropout(h, p=self.dropout, training=self.training)
                h = self._aggregate(adjacency_by_relation, h, self.rel_lin2, self.self_loop_out)
                return h

            def decode(self, embeddings, edge_index, relation_ids):
                src_vec = embeddings[edge_index[:, 0]]
                dst_vec = embeddings[edge_index[:, 1]]
                rel_vec = self.relation_embeddings(relation_ids)
                features = torch.cat([src_vec * dst_vec, torch.abs(src_vec - dst_vec), rel_vec], dim=1)
                return self.decoder(features).squeeze(-1)

        self.model = _Model()

    def parameters(self):
        return self.model.parameters()

    def train(self):
        self.model.train()

    def eval(self):
        self.model.eval()

    def encode(self, adjacency_by_relation):
        return self.model.encode(adjacency_by_relation)

    def decode(self, embeddings, edge_index, relation_ids):
        return self.model.decode(embeddings, edge_index, relation_ids)

    def state_dict(self):
        return self.model.state_dict()

    def load_state_dict(self, state_dict):
        self.model.load_state_dict(state_dict)


def train_relation_gcn(
    model,
    adjacency_by_relation,
    train_edges,
    train_relation_ids,
    train_labels,
    val_edges,
    val_relation_ids,
    val_labels,
    config: dict,
    torch,
    accuracy_score,
    average_precision_score,
    f1_score,
    roc_auc_score,
):
    learning_rate = float(config.get("learning_rate", 0.01))
    weight_decay = float(config.get("weight_decay", 1e-4))
    epochs = int(config.get("epochs", 60))
    eval_every = int(config.get("eval_every", 5))
    early_stopping_patience = int(config.get("early_stopping_patience", 6))

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    criterion = torch.nn.BCEWithLogitsLoss()
    history: list[dict] = []
    best_state = None
    best_epoch = 0
    best_val_ap = float("-inf")
    patience = 0

    for epoch in range(1, epochs + 1):
        model.train()
        embeddings = model.encode(adjacency_by_relation)
        train_logits = model.decode(embeddings, train_edges, train_relation_ids)
        loss = criterion(train_logits, train_labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_record = {"epoch": epoch, "train_loss": float(loss.detach().item())}
        should_eval = epoch == 1 or epoch % eval_every == 0 or epoch == epochs
        if should_eval:
            model.eval()
            with torch.no_grad():
                embeddings = model.encode(adjacency_by_relation)
                val_logits = model.decode(embeddings, val_edges, val_relation_ids)
                val_metrics = evaluate_split(
                    val_logits,
                    val_labels,
                    accuracy_score,
                    average_precision_score,
                    f1_score,
                    roc_auc_score,
                )
            epoch_record["val_average_precision"] = val_metrics["average_precision"]
            epoch_record["val_auroc"] = val_metrics["auroc"]
            print(
                f"[epoch {epoch}/{epochs}] "
                f"train_loss={epoch_record['train_loss']:.6f} "
                f"val AP={fmt_metric(val_metrics['average_precision'])} "
                f"val AUROC={fmt_metric(val_metrics['auroc'])}"
            )
            current_val_ap = val_metrics["average_precision"]
            if current_val_ap is not None and current_val_ap > best_val_ap:
                best_val_ap = current_val_ap
                best_epoch = epoch
                patience = 0
                best_state = {
                    key: value.detach().cpu().clone()
                    for key, value in model.state_dict().items()
                }
            else:
                patience += 1
                if patience >= early_stopping_patience:
                    history.append(epoch_record)
                    print(f"[early-stop] no validation AP improvement for {early_stopping_patience} evals")
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
        "best_val_average_precision": None if best_val_ap == float("-inf") else float(best_val_ap),
        "num_train_examples": int(train_labels.shape[0]),
        "num_val_examples": int(val_labels.shape[0]),
        "history": history,
    }


def run_relation_gcn_experiment(config: dict) -> dict:
    data = prepare_relation_run_data(config)
    artifacts_root = data["artifacts_root"]

    if config.get("dry_run", False) or not all(data["dependency_status"].values()):
        notes = {
            "mode": "dry_run",
            "message": (
                "Relation-aware GCN baseline completed task construction and split generation. "
                "Set dry_run=false and ensure torch/numpy/sklearn are available to train."
            ),
        }
        write_json(artifacts_root / "relation_gcn_dry_run_summary.json", notes)
        return {
            "config": copy.deepcopy(config),
            "artifacts_root": str(artifacts_root),
            "graph_summary": data["graph_summary"],
            "task_summary": data["task_summary"],
            "metrics": None,
            "training_stats": None,
        }

    (
        np,
        torch,
        _F,
        accuracy_score,
        average_precision_score,
        f1_score,
        roc_auc_score,
    ) = import_training_deps()
    seed_status = set_global_random_seed(int(config["seed"]), np=np, torch=torch)

    declarations = data["declarations"]
    edges = data["edges"]
    prediction_relation_types = data["prediction_relation_types"]
    message_relation_types = data["message_relation_types"]
    relation_to_idx = build_relation_type_index(prediction_relation_types)
    message_relation_to_idx = build_relation_type_index(message_relation_types)
    node_ids = [row["declaration_id"] for row in declarations]
    node_to_idx = {node_id: idx for idx, node_id in enumerate(node_ids)}

    split_examples = load_relation_split_triplets(artifacts_root)
    held_out_direct_examples = {
        (src_id, dst_id, relation_type)
        for split_name in ["val", "test"]
        for src_id, dst_id, relation_type, label in split_examples[split_name]
        if label == 1 and relation_type in set(message_relation_types)
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
        indexed_message_edges.append(
            {
                **row,
                "src_idx": node_to_idx[row["src_id"]],
                "dst_idx": node_to_idx[row["dst_id"]],
            }
        )
    adjacency_by_relation = build_relation_aware_adjacency(
        num_nodes=len(node_ids),
        train_message_edges=indexed_message_edges,
        relation_to_idx=message_relation_to_idx,
        symmetrize=bool(config.get("symmetrize_graph", True)),
        torch=torch,
    )

    train_edges, train_relation_ids, train_labels = build_edge_tensors(split_examples["train"], node_to_idx, relation_to_idx, torch)
    val_edges, val_relation_ids, val_labels = build_edge_tensors(split_examples["val"], node_to_idx, relation_to_idx, torch)
    test_edges, test_relation_ids, test_labels = build_edge_tensors(split_examples["test"], node_to_idx, relation_to_idx, torch)

    model = RelationAwareGCNLinkPredictor(
        len(node_ids),
        prediction_relation_types=prediction_relation_types,
        message_relation_types=message_relation_types,
        config=config,
        torch=torch,
    )
    embeddings, train_stats = train_relation_gcn(
        model=model,
        adjacency_by_relation=adjacency_by_relation,
        train_edges=train_edges,
        train_relation_ids=train_relation_ids,
        train_labels=train_labels,
        val_edges=val_edges,
        val_relation_ids=val_relation_ids,
        val_labels=val_labels,
        config=config,
        torch=torch,
        accuracy_score=accuracy_score,
        average_precision_score=average_precision_score,
        f1_score=f1_score,
        roc_auc_score=roc_auc_score,
    )

    np.save(artifacts_root / "node_embeddings.npy", embeddings)
    write_json(artifacts_root / "training_stats.json", train_stats)
    write_json(artifacts_root / "relation_type_index.json", relation_to_idx)
    write_json(artifacts_root / "message_relation_type_index.json", message_relation_to_idx)

    with torch.no_grad():
        final_embeddings = torch.tensor(embeddings, dtype=torch.float32)
        val_logits = model.decode(final_embeddings, val_edges, val_relation_ids)
        test_logits = model.decode(final_embeddings, test_edges, test_relation_ids)

    metrics = {
        "val": evaluate_split(val_logits, val_labels, accuracy_score, average_precision_score, f1_score, roc_auc_score),
        "test": evaluate_split(test_logits, test_labels, accuracy_score, average_precision_score, f1_score, roc_auc_score),
    }
    metrics.update(build_calibrated_metrics(val_logits, val_labels, test_logits, test_labels, torch))
    metrics["score_diagnostics"] = {
        "seed_status": seed_status,
        "val": summarize_score_distribution(val_logits, val_labels),
        "test": summarize_score_distribution(test_logits, test_labels),
    }
    if str(config["task"]) in {"parent_prediction", "ancestor_ranking"}:
        metrics["ranking"] = build_ranking_task_metrics(
            model=model,
            embeddings=final_embeddings,
            split_examples=split_examples,
            relation_candidate_pools=data["relation_candidate_pools"],
            node_to_idx=node_to_idx,
            relation_to_idx=relation_to_idx,
            positive_hop_lookup=data["positive_hop_lookup"],
            torch=torch,
        )
    write_json(artifacts_root / "metrics.json", metrics)

    result_summary = {
        "run_id": config["run_id"],
        "task": config["task"],
        "relation_types": prediction_relation_types,
        "message_relation_types": message_relation_types,
        "input_dim": int(config.get("input_dim", 16)),
        "hidden_dim": int(config.get("hidden_dim", 16)),
        "output_dim": int(config.get("output_dim", 16)),
        "artifacts_root": str(artifacts_root),
        "best_epoch": train_stats["best_epoch"],
        "val_average_precision": metrics["val"]["average_precision"],
        "val_auroc": metrics["val"]["auroc"],
        "test_average_precision": metrics["test"]["average_precision"],
        "test_auroc": metrics["test"]["auroc"],
        "test_f1": metrics["test"]["f1"],
        "calibrated_temperature": metrics["calibrated"]["temperature"],
        "calibrated_threshold": metrics["calibrated"]["selected_threshold"],
        "calibrated_test_f1": metrics["calibrated"]["test"]["f1"],
        "task_summary": data["task_summary"],
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
        result_summary.update(flatten_grouped_hop_bucket_summary(grouped))
    write_json(artifacts_root / "result_summary.json", result_summary)

    print("[done] relation-aware gcn training completed")
    print(f"[done] task: {config['task']}")
    print(f"[done] relations: {', '.join(prediction_relation_types)}")
    print(f"[done] val AP: {fmt_metric(metrics['val']['average_precision'])}")
    print(f"[done] test AP: {fmt_metric(metrics['test']['average_precision'])}")
    if "ranking" in metrics:
        print(f"[done] test MRR: {fmt_metric(metrics['ranking']['test']['mrr'])}")
        grouped = metrics["ranking"]["test"].get("grouped", {})
        print(f"[done] grouped test MAP: {fmt_metric(grouped.get('map'))}")
        print(f"[done] grouped test Recall@10: {fmt_metric(grouped.get('recall_at_10'))}")
    print(f"[done] artifacts: {artifacts_root}")

    return {
        "config": copy.deepcopy(config),
        "artifacts_root": str(artifacts_root),
        "graph_summary": data["graph_summary"],
        "task_summary": data["task_summary"],
        "negative_sampling_stats": data["negative_sampling_stats"],
        "metrics": metrics,
        "training_stats": train_stats,
        "result_summary": result_summary,
    }


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    run_relation_gcn_experiment(config)


if __name__ == "__main__":
    main()
