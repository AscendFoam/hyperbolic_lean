from __future__ import annotations

import argparse
import copy
import importlib.util
from pathlib import Path

from common import (
    build_run_manifest,
    ensure_dir,
    load_config,
    load_declaration_graph,
    sample_negative_edges,
    split_seed_offset,
    split_edges,
    set_global_random_seed,
    summarize_graph,
    write_edge_split_csv,
    write_json,
)
from eval_utils import build_calibrated_metrics, summarize_score_distribution


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pure PyTorch GCN baseline.")
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


def import_training_deps() -> tuple:
    import numpy as np
    import torch
    import torch.nn.functional as F
    from sklearn.metrics import (
        accuracy_score,
        average_precision_score,
        f1_score,
        roc_auc_score,
    )

    return np, torch, F, accuracy_score, average_precision_score, f1_score, roc_auc_score


def read_split_examples(split_path: Path) -> list[tuple[str, str, int]]:
    import csv

    rows: list[tuple[str, str, int]] = []
    with split_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append((row["src_id"], row["dst_id"], int(row["label"])))
    return rows


def build_edge_tensors(edge_examples, node_to_idx: dict[str, int], torch):
    edges: list[list[int]] = []
    labels: list[float] = []
    for src_id, dst_id, label in edge_examples:
        if src_id not in node_to_idx or dst_id not in node_to_idx:
            continue
        edges.append([node_to_idx[src_id], node_to_idx[dst_id]])
        labels.append(float(label))
    if not edges:
        raise ValueError("No valid edge examples were found after node-id filtering.")
    return (
        torch.tensor(edges, dtype=torch.long),
        torch.tensor(labels, dtype=torch.float32),
    )


def build_normalized_adjacency(num_nodes: int, train_positive_edges: list[tuple[int, int]], symmetrize: bool, torch):
    edge_pairs: set[tuple[int, int]] = set()
    for src_idx, dst_idx in train_positive_edges:
        edge_pairs.add((src_idx, dst_idx))
        if symmetrize:
            edge_pairs.add((dst_idx, src_idx))
    for node_idx in range(num_nodes):
        edge_pairs.add((node_idx, node_idx))

    src = torch.tensor([s for s, _ in edge_pairs], dtype=torch.long)
    dst = torch.tensor([d for _, d in edge_pairs], dtype=torch.long)
    degree = torch.zeros(num_nodes, dtype=torch.float32)
    degree.index_add_(0, src, torch.ones(len(edge_pairs), dtype=torch.float32))
    deg_inv_sqrt = degree.pow(-0.5)
    deg_inv_sqrt[torch.isinf(deg_inv_sqrt)] = 0.0
    values = deg_inv_sqrt[src] * deg_inv_sqrt[dst]

    adjacency = torch.sparse_coo_tensor(
        torch.stack([src, dst], dim=0),
        values,
        (num_nodes, num_nodes),
    ).coalesce()
    return adjacency


class GCNLinkPredictor:
    def __init__(self, num_nodes: int, config: dict, torch, F):
        self.torch = torch
        self.F = F
        input_dim = int(config.get("input_dim", config.get("embedding_dim", 64)))
        hidden_dim = int(config.get("hidden_dim", 64))
        output_dim = int(config.get("output_dim", config.get("embedding_dim", 32)))
        dropout = float(config.get("dropout", 0.2))

        class _Model(torch.nn.Module):
            def __init__(self, num_nodes: int, input_dim: int, hidden_dim: int, output_dim: int, dropout: float):
                super().__init__()
                self.node_features = torch.nn.Parameter(torch.empty(num_nodes, input_dim))
                self.lin1 = torch.nn.Linear(input_dim, hidden_dim, bias=False)
                self.lin2 = torch.nn.Linear(hidden_dim, output_dim, bias=False)
                self.dropout = dropout
                torch.nn.init.xavier_uniform_(self.node_features)
                torch.nn.init.xavier_uniform_(self.lin1.weight)
                torch.nn.init.xavier_uniform_(self.lin2.weight)

            def encode(self, adjacency):
                h = torch.sparse.mm(adjacency, self.node_features)
                h = self.lin1(h)
                h = torch.relu(h)
                h = torch.nn.functional.dropout(h, p=self.dropout, training=self.training)
                h = torch.sparse.mm(adjacency, h)
                h = self.lin2(h)
                return h

            def decode(self, embeddings, edge_index):
                src_vec = embeddings[edge_index[:, 0]]
                dst_vec = embeddings[edge_index[:, 1]]
                return torch.sum(src_vec * dst_vec, dim=1)

        self.model = _Model(num_nodes, input_dim, hidden_dim, output_dim, dropout)

    def parameters(self):
        return self.model.parameters()

    def train(self):
        self.model.train()

    def eval(self):
        self.model.eval()

    def encode(self, adjacency):
        return self.model.encode(adjacency)

    def decode(self, embeddings, edge_index):
        return self.model.decode(embeddings, edge_index)

    def state_dict(self):
        return self.model.state_dict()

    def load_state_dict(self, state_dict):
        self.model.load_state_dict(state_dict)


def evaluate_split(logits, labels, accuracy_score, average_precision_score, f1_score, roc_auc_score):
    prob = logits.sigmoid().detach().cpu().numpy()
    y = labels.detach().cpu().numpy().astype(int)
    pred = (prob >= 0.5).astype(int)

    auroc = None
    average_precision = None
    if len(set(y.tolist())) >= 2:
        auroc = float(roc_auc_score(y, prob))
    if int(y.sum()) > 0:
        average_precision = float(average_precision_score(y, prob))

    return {
        "auroc": auroc,
        "average_precision": average_precision,
        "accuracy": float(accuracy_score(y, pred)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "num_examples": int(len(y)),
        "num_positive": int(y.sum()),
        "num_negative": int(len(y) - y.sum()),
    }


def fmt_metric(value) -> str:
    if value is None:
        return "NA"
    return f"{value:.4f}"


def prepare_run_data(config: dict) -> dict:
    graph_root = Path(config["graph_root"])
    artifacts_root = Path(config["artifacts_root"])
    ensure_dir(artifacts_root)

    declarations, edges = load_declaration_graph(graph_root)
    graph_summary = summarize_graph(declarations, edges)

    split = split_edges(
        edges=edges,
        val_ratio=float(config["val_ratio"]),
        test_ratio=float(config["test_ratio"]),
        seed=int(config["seed"]),
    )

    node_ids = [row["declaration_id"] for row in declarations]
    positive_pairs = set(split["train"] + split["val"] + split["test"])
    negative_ratio = float(config.get("negative_ratio", 1.0))
    negative_strategy = str(config.get("negative_strategy", "same_module"))
    negative_fallback_strategy = str(config.get("negative_fallback_strategy", "random"))
    negative_sampling_stats: dict[str, dict] = {}

    for split_name, positive_edges in split.items():
        negatives, sampling_stats = sample_negative_edges(
            node_ids=node_ids,
            declarations=declarations,
            positive_pairs=positive_pairs,
            num_samples=int(len(positive_edges) * negative_ratio),
            seed=int(config["seed"]) + split_seed_offset(split_name),
            negative_strategy=negative_strategy,
            negative_fallback_strategy=negative_fallback_strategy,
        )
        negative_sampling_stats[split_name] = sampling_stats
        write_edge_split_csv(
            path=artifacts_root / f"{split_name}_edges.csv",
            split_name=split_name,
            positives=positive_edges,
            negatives=negatives,
        )

    dependency_status = {
        "torch": has_module("torch"),
        "numpy": has_module("numpy"),
        "sklearn": has_module("sklearn"),
    }
    manifest = build_run_manifest(config, graph_summary, dependency_status)
    write_json(artifacts_root / "run_manifest.json", manifest)
    write_json(artifacts_root / "negative_sampling_stats.json", negative_sampling_stats)

    return {
        "artifacts_root": artifacts_root,
        "graph_summary": graph_summary,
        "split": split,
        "node_ids": node_ids,
        "dependency_status": dependency_status,
        "negative_sampling_stats": negative_sampling_stats,
    }


def train_gcn(
    model,
    adjacency,
    train_edges,
    train_labels,
    val_edges,
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
    epochs = int(config.get("epochs", 80))
    eval_every = int(config.get("eval_every", 5))
    early_stopping_patience = int(config.get("early_stopping_patience", 20))

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    criterion = torch.nn.BCEWithLogitsLoss()

    history: list[dict] = []
    best_state = None
    best_epoch = 0
    best_val_ap = float("-inf")
    patience = 0

    for epoch in range(1, epochs + 1):
        model.train()
        embeddings = model.encode(adjacency)
        train_logits = model.decode(embeddings, train_edges)
        loss = criterion(train_logits, train_labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_record = {
            "epoch": epoch,
            "train_loss": float(loss.detach().item()),
        }

        should_eval = epoch == 1 or epoch % eval_every == 0 or epoch == epochs
        if should_eval:
            model.eval()
            with torch.no_grad():
                embeddings = model.encode(adjacency)
                val_logits = model.decode(embeddings, val_edges)
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
        final_embeddings = model.encode(adjacency)

    return final_embeddings.detach().cpu().numpy(), {
        "best_epoch": best_epoch,
        "best_val_average_precision": None if best_val_ap == float("-inf") else float(best_val_ap),
        "num_train_examples": int(train_labels.shape[0]),
        "num_val_examples": int(val_labels.shape[0]),
        "history": history,
    }


def run_gcn_experiment(config: dict) -> dict:
    data = prepare_run_data(config)
    artifacts_root = data["artifacts_root"]

    if config.get("dry_run", False) or not all(data["dependency_status"].values()):
        notes = {
            "mode": "dry_run",
            "message": (
                "GCN baseline completed data validation and split generation. "
                "Set dry_run=false and ensure torch/numpy/sklearn are available to train."
            ),
        }
        write_json(artifacts_root / "gcn_dry_run_summary.json", notes)
        print("[done] dry-run completed")
        print(f"[done] artifacts: {artifacts_root}")
        return {
            "config": copy.deepcopy(config),
            "artifacts_root": str(artifacts_root),
            "graph_summary": data["graph_summary"],
            "negative_sampling_stats": data["negative_sampling_stats"],
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

    node_ids = data["node_ids"]
    node_to_idx = {node_id: idx for idx, node_id in enumerate(node_ids)}
    split = data["split"]
    symmetrize = bool(config.get("symmetrize_graph", True))
    train_positive_edges = [
        (node_to_idx[src_id], node_to_idx[dst_id])
        for src_id, dst_id in split["train"]
        if src_id in node_to_idx and dst_id in node_to_idx
    ]
    adjacency = build_normalized_adjacency(
        num_nodes=len(node_ids),
        train_positive_edges=train_positive_edges,
        symmetrize=symmetrize,
        torch=torch,
    )

    train_edges, train_labels = build_edge_tensors(
        read_split_examples(artifacts_root / "train_edges.csv"),
        node_to_idx,
        torch,
    )
    val_edges, val_labels = build_edge_tensors(
        read_split_examples(artifacts_root / "val_edges.csv"),
        node_to_idx,
        torch,
    )
    test_edges, test_labels = build_edge_tensors(
        read_split_examples(artifacts_root / "test_edges.csv"),
        node_to_idx,
        torch,
    )

    model = GCNLinkPredictor(len(node_ids), config, torch, F)
    embeddings, train_stats = train_gcn(
        model=model,
        adjacency=adjacency,
        train_edges=train_edges,
        train_labels=train_labels,
        val_edges=val_edges,
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

    with torch.no_grad():
        final_embeddings = torch.tensor(embeddings, dtype=torch.float32)
        val_logits = model.decode(final_embeddings, val_edges)
        test_logits = model.decode(final_embeddings, test_edges)

    metrics = {
        "val": evaluate_split(
            val_logits,
            val_labels,
            accuracy_score,
            average_precision_score,
            f1_score,
            roc_auc_score,
        ),
        "test": evaluate_split(
            test_logits,
            test_labels,
            accuracy_score,
            average_precision_score,
            f1_score,
            roc_auc_score,
        ),
    }
    metrics.update(build_calibrated_metrics(val_logits, val_labels, test_logits, test_labels, torch))
    metrics["score_diagnostics"] = {
        "seed_status": seed_status,
        "val": summarize_score_distribution(val_logits, val_labels),
        "test": summarize_score_distribution(test_logits, test_labels),
    }
    write_json(artifacts_root / "metrics.json", metrics)

    result_summary = {
        "run_id": config["run_id"],
        "input_dim": int(config.get("input_dim", config.get("embedding_dim", 64))),
        "hidden_dim": int(config.get("hidden_dim", 64)),
        "output_dim": int(config.get("output_dim", config.get("embedding_dim", 32))),
        "artifacts_root": str(artifacts_root),
        "best_epoch": train_stats["best_epoch"],
        "val_average_precision": metrics["val"]["average_precision"],
        "val_auroc": metrics["val"]["auroc"],
        "test_average_precision": metrics["test"]["average_precision"],
        "test_auroc": metrics["test"]["auroc"],
        "test_f1": metrics["test"]["f1"],
        "calibrated_threshold": metrics["calibrated"]["selected_threshold"],
        "calibrated_temperature": metrics["calibrated"]["temperature"],
        "calibrated_test_f1": metrics["calibrated"]["test"]["f1"],
    }
    write_json(artifacts_root / "result_summary.json", result_summary)

    print("[done] gcn training completed")
    print(f"[done] val AP: {fmt_metric(metrics['val']['average_precision'])}")
    print(f"[done] test AP: {fmt_metric(metrics['test']['average_precision'])}")
    print(f"[done] calibrated test F1: {fmt_metric(metrics['calibrated']['test']['f1'])}")
    print(f"[done] artifacts: {artifacts_root}")

    return {
        "config": copy.deepcopy(config),
        "artifacts_root": str(artifacts_root),
        "graph_summary": data["graph_summary"],
        "negative_sampling_stats": data["negative_sampling_stats"],
        "metrics": metrics,
        "training_stats": train_stats,
        "result_summary": result_summary,
    }


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    run_gcn_experiment(config)


if __name__ == "__main__":
    main()
