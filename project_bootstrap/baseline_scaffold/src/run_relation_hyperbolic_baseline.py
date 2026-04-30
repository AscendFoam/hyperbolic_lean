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
from run_hyperbolic_baseline import (
    build_edge_feature_tensor,
    build_hgcn_distance_terms,
    check_finite,
    expmap0,
    gate_logit_from_init,
    logmap0,
    poincare_distance,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Relation-aware pure PyTorch hyperbolic baseline.")
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


class RelationAwareHyperbolicLinkPredictor:
    def __init__(self, num_nodes: int, prediction_relation_types: list[str], message_relation_types: list[str], config: dict, torch, F):
        self.torch = torch
        self.F = F
        self.model_variant = str(config.get("model_variant", "relation_hgcn_residual_v3"))
        input_dim = int(config.get("input_dim", 16))
        hidden_dim = int(config.get("hidden_dim", 16))
        output_dim = int(config.get("output_dim", 16))
        dropout = float(config.get("dropout", 0.15))
        curvature = float(config.get("curvature", 1.0))
        decoder_hidden_dim = int(config.get("decoder_hidden_dim", output_dim))
        distance_signal_mode = str(config.get("distance_signal_mode", "log1p_running_zscore_tanh"))
        distance_stat_momentum = float(config.get("distance_stat_momentum", 0.1))
        residual_gate_init = float(config.get("residual_gate_init", 1.0))
        self.curvature = curvature

        prediction_relation_count = len(prediction_relation_types)
        message_relation_count = len(message_relation_types)

        class _Model(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.decoder_version = "v3"
                self.node_features = torch.nn.Parameter(torch.empty(num_nodes, input_dim))
                self.input_proj = torch.nn.Linear(input_dim, hidden_dim, bias=False)
                self.self_loop_hidden = torch.nn.Linear(hidden_dim, hidden_dim, bias=False)
                self.self_loop_out = torch.nn.Linear(hidden_dim, output_dim, bias=False)
                self.rel_agg1 = torch.nn.ModuleList(
                    [torch.nn.Linear(hidden_dim, hidden_dim, bias=False) for _ in range(message_relation_count)]
                )
                self.rel_agg2 = torch.nn.ModuleList(
                    [torch.nn.Linear(hidden_dim, hidden_dim, bias=False) for _ in range(message_relation_count)]
                )
                self.skip_hidden = torch.nn.Linear(hidden_dim, hidden_dim, bias=False)
                self.norm1 = torch.nn.LayerNorm(hidden_dim)
                self.norm2 = torch.nn.LayerNorm(hidden_dim)
                self.distance_signal_mode = distance_signal_mode
                self.distance_stat_momentum = distance_stat_momentum
                self.prediction_relation_embeddings = torch.nn.Embedding(prediction_relation_count, output_dim)
                self.edge_mlp = torch.nn.Sequential(
                    torch.nn.Linear(output_dim * 4, decoder_hidden_dim),
                    torch.nn.ReLU(),
                    torch.nn.Dropout(p=dropout),
                    torch.nn.Linear(decoder_hidden_dim, 1),
                )
                self.log_scale = torch.nn.Parameter(torch.tensor(0.0))
                self.decoder_bias = torch.nn.Parameter(torch.tensor(0.0))
                self.residual_gate_logit = torch.nn.Parameter(
                    torch.tensor(gate_logit_from_init(residual_gate_init), dtype=torch.float32)
                )
                self.register_buffer("distance_signal_running_center", torch.tensor(0.0))
                self.register_buffer("distance_signal_running_spread", torch.tensor(1.0))
                self.register_buffer("distance_signal_running_initialized", torch.tensor(0.0))
                torch.nn.init.xavier_uniform_(self.node_features)
                for module in [
                    self.input_proj,
                    self.self_loop_hidden,
                    self.self_loop_out,
                    self.skip_hidden,
                ] + list(self.rel_agg1) + list(self.rel_agg2):
                    torch.nn.init.xavier_uniform_(module.weight)
                torch.nn.init.xavier_uniform_(self.prediction_relation_embeddings.weight)
                for module in self.edge_mlp:
                    if isinstance(module, torch.nn.Linear):
                        torch.nn.init.xavier_uniform_(module.weight)
                        if module.bias is not None:
                            torch.nn.init.zeros_(module.bias)

            def _aggregate(self, adjacency_by_relation, inputs, relation_layers, skip_layer):
                outputs = skip_layer(inputs)
                for relation_idx, adjacency in adjacency_by_relation.items():
                    relation_inputs = torch.sparse.mm(adjacency, inputs)
                    outputs = outputs + relation_layers[relation_idx](relation_inputs)
                return outputs

            def encode(self, adjacency_by_relation):
                h0 = self.input_proj(self.node_features)
                h = self._aggregate(adjacency_by_relation, h0, self.rel_agg1, self.self_loop_hidden)
                h = self.norm1(h)
                h = torch.nn.functional.gelu(h)
                h = torch.nn.functional.dropout(h, p=dropout, training=self.training)

                x = expmap0(h, curvature, torch)
                tangent_h = logmap0(x, curvature, torch)
                tangent_h = self._aggregate(adjacency_by_relation, tangent_h, self.rel_agg2, self.skip_hidden)
                tangent_h = tangent_h + self.skip_hidden(h0)
                tangent_h = self.norm2(tangent_h)
                tangent_h = torch.nn.functional.gelu(tangent_h)
                tangent_h = torch.nn.functional.dropout(tangent_h, p=dropout, training=self.training)
                tangent_h = self.self_loop_out(tangent_h)
                return expmap0(tangent_h, curvature, torch)

            def decode(self, embeddings, edge_index, relation_ids):
                src_vec = embeddings[edge_index[:, 0]]
                dst_vec = embeddings[edge_index[:, 1]]
                dist = poincare_distance(src_vec, dst_vec, curvature, torch)
                src_tangent = logmap0(src_vec, curvature, torch)
                dst_tangent = logmap0(dst_vec, curvature, torch)
                relation_vec = self.prediction_relation_embeddings(relation_ids)
                edge_features = torch.cat(
                    [
                        build_edge_feature_tensor(src_tangent, dst_tangent, torch),
                        relation_vec,
                    ],
                    dim=1,
                )
                mlp_logits = self.edge_mlp(edge_features).squeeze(-1)
                dist_terms = build_hgcn_distance_terms(self, dist, torch, F)
                residual_gate = 2.0 * torch.sigmoid(self.residual_gate_logit)
                mlp_contribution = residual_gate * mlp_logits
                return mlp_contribution + self.decoder_bias + dist_terms["penalty"]

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


def summarize_relation_hyperbolic_decoder(model, embeddings, edge_index, relation_ids, labels, torch, F):
    model_impl = model.model
    src_vec = embeddings[edge_index[:, 0]]
    dst_vec = embeddings[edge_index[:, 1]]
    relation_vec = model_impl.prediction_relation_embeddings(relation_ids)
    dist = poincare_distance(src_vec, dst_vec, model.curvature, torch)
    src_tangent = logmap0(src_vec, model.curvature, torch)
    dst_tangent = logmap0(dst_vec, model.curvature, torch)
    edge_features = torch.cat([build_edge_feature_tensor(src_tangent, dst_tangent, torch), relation_vec], dim=1)
    mlp_logits = model_impl.edge_mlp(edge_features).squeeze(-1)
    dist_terms = build_hgcn_distance_terms(model_impl, dist, torch, F)
    residual_gate = 2.0 * torch.sigmoid(model_impl.residual_gate_logit)
    mlp_contribution = residual_gate * mlp_logits
    logits = mlp_contribution + model_impl.decoder_bias + dist_terms["penalty"]

    base = {
        "distance": summarize_score_distribution(dist, labels),
        "distance_squared": summarize_score_distribution(dist_terms["distance_squared"], labels),
        "distance_penalty": summarize_score_distribution(dist_terms["penalty"], labels),
        "decoder_bias": float(model_impl.decoder_bias.detach().cpu().item()),
        "distance_scale": float(dist_terms["scale"].detach().cpu().item()),
        "distance_signal_mode": dist_terms["mode"],
        "distance_stats_source": dist_terms["stats_source"],
        "distance_raw_signal": summarize_score_distribution(dist_terms["raw_signal"], labels),
        "distance_signal_pre_activation": summarize_score_distribution(dist_terms["pre_activation"], labels),
        "distance_signal": summarize_score_distribution(dist_terms["signal"], labels),
        "distance_signal_center": float(dist_terms["center"].detach().cpu().item()),
        "distance_signal_spread": float(dist_terms["spread"].detach().cpu().item()),
        "mlp_logits": summarize_score_distribution(mlp_logits, labels),
        "mlp_contribution": summarize_score_distribution(mlp_contribution, labels),
        "residual_gate": float(residual_gate.detach().cpu().item()),
        "reconstructed_logits": summarize_score_distribution(logits, labels),
        "raw_feature_norm": {
            "src_tangent_mean_norm": float(torch.norm(src_tangent, dim=1).mean().detach().cpu().item()),
            "dst_tangent_mean_norm": float(torch.norm(dst_tangent, dim=1).mean().detach().cpu().item()),
            "edge_feature_mean_norm": float(torch.norm(edge_features, dim=1).mean().detach().cpu().item()),
        },
    }
    if hasattr(model_impl, "distance_signal_running_center"):
        base["distance_signal_running_center"] = float(model_impl.distance_signal_running_center.detach().cpu().item())
        base["distance_signal_running_spread"] = float(model_impl.distance_signal_running_spread.detach().cpu().item())

    return {
        "base": base,
        "relation_embedding_norm_mean": float(torch.norm(relation_vec, dim=1).mean().detach().cpu().item()),
        "relation_embedding_norm_std": float(torch.norm(relation_vec, dim=1).std(unbiased=False).detach().cpu().item()),
        "mlp_logits_with_relation": summarize_score_distribution(mlp_logits, labels),
        "mlp_contribution_with_relation": summarize_score_distribution(mlp_contribution, labels),
        "reconstructed_logits_with_relation": summarize_score_distribution(logits, labels),
    }


def train_relation_hyperbolic_model(
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
    learning_rate = float(config.get("learning_rate", 0.001))
    weight_decay = float(config.get("weight_decay", 1e-4))
    epochs = int(config.get("epochs", 60))
    eval_every = int(config.get("eval_every", 5))
    early_stopping_patience = int(config.get("early_stopping_patience", 6))
    grad_clip_norm = float(config.get("grad_clip_norm", 1.0))

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
        check_finite("train_embeddings", embeddings, torch)
        train_logits = model.decode(embeddings, train_edges, train_relation_ids)
        check_finite("train_logits", train_logits, torch)
        loss = criterion(train_logits, train_labels)
        check_finite("train_loss", loss, torch)

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=grad_clip_norm)
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
        "grad_clip_norm": grad_clip_norm,
        "model_variant": str(config.get("model_variant", "relation_hgcn_residual_v3")),
        "history": history,
    }


def run_relation_hyperbolic_experiment(config: dict) -> dict:
    data = prepare_relation_run_data(config)
    artifacts_root = data["artifacts_root"]

    if config.get("dry_run", False) or not all(data["dependency_status"].values()):
        notes = {
            "mode": "dry_run",
            "message": (
                "Relation-aware hyperbolic baseline completed task construction and split generation. "
                "Set dry_run=false and ensure torch/numpy/sklearn are available to train."
            ),
        }
        write_json(artifacts_root / "relation_hyperbolic_dry_run_summary.json", notes)
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
        F,
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

    model = RelationAwareHyperbolicLinkPredictor(
        len(node_ids),
        prediction_relation_types=prediction_relation_types,
        message_relation_types=message_relation_types,
        config=config,
        torch=torch,
        F=F,
    )
    embeddings, train_stats = train_relation_hyperbolic_model(
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
    metrics["decoder_diagnostics"] = {
        "val": summarize_relation_hyperbolic_decoder(model, final_embeddings, val_edges, val_relation_ids, val_labels, torch, F),
        "test": summarize_relation_hyperbolic_decoder(model, final_embeddings, test_edges, test_relation_ids, test_labels, torch, F),
    }
    if str(config["task"]) in {"parent_prediction", "ancestor_ranking"}:
        metrics["ranking"] = build_ranking_task_metrics(
            model=model,
            embeddings=final_embeddings,
            split_examples=split_examples,
            relation_candidate_pools=data["relation_candidate_pools"],
            node_to_idx=node_to_idx,
            relation_to_idx=relation_to_idx,
            torch=torch,
        )
    write_json(artifacts_root / "metrics.json", metrics)

    result_summary = {
        "run_id": config["run_id"],
        "task": config["task"],
        "model_variant": str(config.get("model_variant", "relation_hgcn_residual_v3")),
        "relation_types": prediction_relation_types,
        "message_relation_types": message_relation_types,
        "curvature": float(config.get("curvature", 1.0)),
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
    write_json(artifacts_root / "result_summary.json", result_summary)

    print("[done] relation-aware hyperbolic training completed")
    print(f"[done] task: {config['task']}")
    print(f"[done] variant: {result_summary['model_variant']}")
    print(f"[done] relations: {', '.join(prediction_relation_types)}")
    print(f"[done] val AP: {fmt_metric(metrics['val']['average_precision'])}")
    print(f"[done] test AP: {fmt_metric(metrics['test']['average_precision'])}")
    if "ranking" in metrics:
        print(f"[done] test MRR: {fmt_metric(metrics['ranking']['test']['mrr'])}")
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
    run_relation_hyperbolic_experiment(config)


if __name__ == "__main__":
    main()
