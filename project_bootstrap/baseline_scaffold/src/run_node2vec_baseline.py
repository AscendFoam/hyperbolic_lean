from __future__ import annotations

import argparse
import importlib.util
import math
import random
from pathlib import Path

from common import (
    build_run_manifest,
    ensure_dir,
    load_config,
    load_declaration_graph,
    sample_negative_edges,
    split_edges,
    summarize_graph,
    write_edge_split_csv,
    write_json,
)


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Node2Vec baseline.")
    parser.add_argument("--config", required=True, type=Path)
    return parser.parse_args()


def import_training_deps() -> tuple:
    import networkx as nx
    import numpy as np
    import torch
    import torch.nn.functional as F
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (
        accuracy_score,
        average_precision_score,
        f1_score,
        roc_auc_score,
    )

    return nx, np, torch, F, LogisticRegression, accuracy_score, average_precision_score, f1_score, roc_auc_score


def build_graph(nx, node_ids: list[str], positive_edges: list[tuple[str, str]], symmetrize: bool):
    graph = nx.Graph() if symmetrize else nx.DiGraph()
    graph.add_nodes_from(node_ids)
    graph.add_edges_from(positive_edges)
    return graph


def node2vec_next_node(graph, prev_node: int | None, current_node: int, p: float, q: float, rng: random.Random) -> int | None:
    neighbors = list(graph.neighbors(current_node))
    if not neighbors:
        return None
    if prev_node is None:
        return rng.choice(neighbors)

    weights: list[float] = []
    for dst in neighbors:
        if dst == prev_node:
            weight = 1.0 / p
        elif graph.has_edge(dst, prev_node) or graph.has_edge(prev_node, dst):
            weight = 1.0
        else:
            weight = 1.0 / q
        weights.append(weight)

    total = sum(weights)
    if total <= 0:
        return rng.choice(neighbors)

    r = rng.random() * total
    cumsum = 0.0
    for dst, w in zip(neighbors, weights):
        cumsum += w
        if r <= cumsum:
            return dst
    return neighbors[-1]


def generate_walks(graph, num_nodes: int, walk_length: int, num_walks_per_node: int, p: float, q: float, seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    nodes = list(range(num_nodes))
    walks: list[list[int]] = []
    for _ in range(num_walks_per_node):
        rng.shuffle(nodes)
        for start in nodes:
            walk = [start]
            prev = None
            current = start
            for _step in range(walk_length - 1):
                nxt = node2vec_next_node(graph, prev, current, p, q, rng)
                if nxt is None:
                    break
                walk.append(nxt)
                prev, current = current, nxt
            walks.append(walk)
    return walks


def generate_skipgram_pairs(walks: list[list[int]], window_size: int) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for walk in walks:
        for i, center in enumerate(walk):
            left = max(0, i - window_size)
            right = min(len(walk), i + window_size + 1)
            for j in range(left, right):
                if j == i:
                    continue
                pairs.append((center, walk[j]))
    return pairs


def build_negative_distribution(graph, num_nodes: int, np) -> object:
    degrees = np.zeros(num_nodes, dtype=np.float64)
    for node in range(num_nodes):
        degrees[node] = max(1, graph.degree(node))
    probs = np.power(degrees, 0.75)
    probs = probs / probs.sum()
    return probs


def train_node2vec_embeddings(
    graph,
    num_nodes: int,
    config: dict,
    torch,
    F,
    np,
) -> object:
    embedding_dim = int(config["embedding_dim"])
    walk_length = int(config["walk_length"])
    num_walks_per_node = int(config["num_walks_per_node"])
    window_size = int(config["window_size"])
    num_negative_samples = int(config["num_negative_samples"])
    epochs = int(config["epochs"])
    batch_size = int(config["batch_size"])
    learning_rate = float(config["learning_rate"])
    p = float(config["p"])
    q = float(config["q"])
    seed = int(config["seed"])

    walks = generate_walks(
        graph=graph,
        num_nodes=num_nodes,
        walk_length=walk_length,
        num_walks_per_node=num_walks_per_node,
        p=p,
        q=q,
        seed=seed,
    )
    pairs = generate_skipgram_pairs(walks, window_size)
    if not pairs:
        raise ValueError("No skip-gram pairs were generated. Graph may be too sparse.")

    negative_probs = build_negative_distribution(graph, num_nodes, np)
    rng = np.random.default_rng(seed)

    target_emb = torch.nn.Embedding(num_nodes, embedding_dim)
    context_emb = torch.nn.Embedding(num_nodes, embedding_dim)
    torch.nn.init.xavier_uniform_(target_emb.weight)
    torch.nn.init.xavier_uniform_(context_emb.weight)
    optimizer = torch.optim.Adam(
        list(target_emb.parameters()) + list(context_emb.parameters()),
        lr=learning_rate,
    )

    device = torch.device("cpu")
    target_emb.to(device)
    context_emb.to(device)

    for epoch in range(epochs):
        random.Random(seed + epoch).shuffle(pairs)
        epoch_loss = 0.0
        num_batches = math.ceil(len(pairs) / batch_size)

        for batch_idx in range(num_batches):
            batch = pairs[batch_idx * batch_size:(batch_idx + 1) * batch_size]
            centers = torch.tensor([x[0] for x in batch], dtype=torch.long, device=device)
            positives = torch.tensor([x[1] for x in batch], dtype=torch.long, device=device)
            negatives_np = rng.choice(
                num_nodes,
                size=(len(batch), num_negative_samples),
                p=negative_probs,
            )
            negatives = torch.tensor(negatives_np, dtype=torch.long, device=device)

            center_vec = target_emb(centers)
            pos_vec = context_emb(positives)
            neg_vec = context_emb(negatives)

            pos_score = torch.sum(center_vec * pos_vec, dim=1)
            neg_score = torch.sum(center_vec.unsqueeze(1) * neg_vec, dim=2)

            loss = -F.logsigmoid(pos_score).mean() - F.logsigmoid(-neg_score).mean()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.detach().item()

        print(f"[epoch {epoch + 1}/{epochs}] loss={epoch_loss / max(1, num_batches):.6f}")

    return target_emb.weight.detach().cpu().numpy(), {
        "num_walks": len(walks),
        "num_pairs": len(pairs),
    }


def build_edge_features(
    edge_examples: list[tuple[str, str, int]],
    embeddings,
    node_to_idx: dict[str, int],
    np,
    operator: str,
):
    xs = []
    ys = []
    for src_id, dst_id, label in edge_examples:
        if src_id not in node_to_idx or dst_id not in node_to_idx:
            continue
        src_vec = embeddings[node_to_idx[src_id]]
        dst_vec = embeddings[node_to_idx[dst_id]]
        if operator == "hadamard":
            feat = src_vec * dst_vec
        elif operator == "l1":
            feat = np.abs(src_vec - dst_vec)
        elif operator == "concat":
            feat = np.concatenate([src_vec, dst_vec], axis=0)
        else:
            raise ValueError(f"Unsupported eval_operator: {operator}")
        xs.append(feat)
        ys.append(label)
    return np.stack(xs), np.asarray(ys)


def read_split_examples(split_path: Path) -> list[tuple[str, str, int]]:
    import csv

    rows: list[tuple[str, str, int]] = []
    with split_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append((row["src_id"], row["dst_id"], int(row["label"])))
    return rows


def evaluate_link_prediction(
    artifacts_root: Path,
    embeddings,
    node_to_idx: dict[str, int],
    LogisticRegression,
    accuracy_score,
    average_precision_score,
    f1_score,
    roc_auc_score,
    np,
    operator: str,
) -> dict:
    train_examples = read_split_examples(artifacts_root / "train_edges.csv")
    val_examples = read_split_examples(artifacts_root / "val_edges.csv")
    test_examples = read_split_examples(artifacts_root / "test_edges.csv")

    x_train, y_train = build_edge_features(train_examples, embeddings, node_to_idx, np, operator)
    x_val, y_val = build_edge_features(val_examples, embeddings, node_to_idx, np, operator)
    x_test, y_test = build_edge_features(test_examples, embeddings, node_to_idx, np, operator)

    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(x_train, y_train)

    def evaluate_split(x, y) -> dict:
        prob = clf.predict_proba(x)[:, 1]
        pred = (prob >= 0.5).astype(int)
        unique_classes = set(y.tolist())
        auroc = None
        average_precision = None
        if len(unique_classes) >= 2:
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

    return {
        "val": evaluate_split(x_val, y_val),
        "test": evaluate_split(x_test, y_test),
    }


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

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

    for split_name, positive_edges in split.items():
        negatives = sample_negative_edges(
            node_ids=node_ids,
            positive_pairs=positive_pairs,
            num_samples=int(len(positive_edges) * negative_ratio),
            seed=int(config["seed"]) + hash(split_name) % 10000,
        )
        write_edge_split_csv(
            path=artifacts_root / f"{split_name}_edges.csv",
            split_name=split_name,
            positives=positive_edges,
            negatives=negatives,
        )

    dependency_status = {
        "networkx": has_module("networkx"),
        "numpy": has_module("numpy"),
        "torch": has_module("torch"),
        "sklearn": has_module("sklearn"),
    }
    manifest = build_run_manifest(config, graph_summary, dependency_status)
    write_json(artifacts_root / "run_manifest.json", manifest)

    if config.get("dry_run", False) or not all(dependency_status.values()):
        notes = {
            "mode": "dry_run",
            "message": (
                "Node2Vec baseline completed data validation and split generation. "
                "Set dry_run=false and ensure networkx/numpy/torch/sklearn are available to train."
            ),
        }
        write_json(artifacts_root / "node2vec_dry_run_summary.json", notes)
        print("[done] dry-run completed")
        print(f"[done] artifacts: {artifacts_root}")
        return

    (
        nx,
        np,
        torch,
        F,
        LogisticRegression,
        accuracy_score,
        average_precision_score,
        f1_score,
        roc_auc_score,
    ) = import_training_deps()

    node_to_idx = {node_id: idx for idx, node_id in enumerate(node_ids)}
    train_positive_edges = [(node_to_idx[s], node_to_idx[d]) for s, d in split["train"] if s in node_to_idx and d in node_to_idx]
    graph = build_graph(
        nx=nx,
        node_ids=list(range(len(node_ids))),
        positive_edges=train_positive_edges,
        symmetrize=bool(config.get("symmetrize_graph", True)),
    )

    embeddings, train_stats = train_node2vec_embeddings(
        graph=graph,
        num_nodes=len(node_ids),
        config=config,
        torch=torch,
        F=F,
        np=np,
    )

    np.save(artifacts_root / "node_embeddings.npy", embeddings)
    write_json(artifacts_root / "training_stats.json", train_stats)

    metrics = evaluate_link_prediction(
        artifacts_root=artifacts_root,
        embeddings=embeddings,
        node_to_idx=node_to_idx,
        LogisticRegression=LogisticRegression,
        accuracy_score=accuracy_score,
        average_precision_score=average_precision_score,
        f1_score=f1_score,
        roc_auc_score=roc_auc_score,
        np=np,
        operator=str(config.get("eval_operator", "hadamard")),
    )
    write_json(artifacts_root / "metrics.json", metrics)

    def fmt_metric(value) -> str:
        if value is None:
            return "NA"
        return f"{value:.4f}"

    print("[done] node2vec training completed")
    print(f"[done] val AP: {fmt_metric(metrics['val']['average_precision'])}")
    print(f"[done] test AP: {fmt_metric(metrics['test']['average_precision'])}")
    print(f"[done] artifacts: {artifacts_root}")


if __name__ == "__main__":
    main()
