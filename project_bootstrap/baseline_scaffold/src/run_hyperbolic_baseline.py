from __future__ import annotations

import argparse
import copy
import csv
import importlib.util
import math
from typing import Any
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
    parser = argparse.ArgumentParser(description="Pure PyTorch hyperbolic baseline.")
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


def artanh(x, torch):
    eps = 1e-6
    x = torch.clamp(x, min=-1 + eps, max=1 - eps)
    return 0.5 * (torch.log1p(x) - torch.log1p(-x))


def project_ball(x, c: float, torch):
    eps = 1e-5
    max_norm = (1.0 - eps) / (c ** 0.5)
    norm = torch.norm(x, dim=-1, keepdim=True).clamp_min(eps)
    scale = torch.clamp(max_norm / norm, max=1.0)
    return x * scale


def expmap0(u, c: float, torch):
    eps = 1e-6
    sqrt_c = c ** 0.5
    norm = torch.norm(u, dim=-1, keepdim=True).clamp_min(eps)
    gamma = torch.tanh(sqrt_c * norm) * u / (sqrt_c * norm)
    return project_ball(gamma, c, torch)


def logmap0(y, c: float, torch):
    eps = 1e-6
    sqrt_c = c ** 0.5
    y = project_ball(y, c, torch)
    norm = torch.norm(y, dim=-1, keepdim=True).clamp_min(eps)
    return artanh(sqrt_c * norm, torch) * y / (sqrt_c * norm)


def poincare_distance(x, y, c: float, torch):
    eps = 1e-6
    sqrt_c = c ** 0.5
    max_sq_norm = (1.0 - eps) / c
    x_sq = torch.sum(x * x, dim=-1).clamp_max(max_sq_norm)
    y_sq = torch.sum(y * y, dim=-1).clamp_max(max_sq_norm)
    diff_sq = torch.sum((x - y) * (x - y), dim=-1)
    denom = (1.0 - c * x_sq) * (1.0 - c * y_sq)
    z = 1.0 + 2.0 * c * diff_sq / denom.clamp_min(eps)
    z = torch.clamp(z, min=1.0 + eps)
    return torch.acosh(z) / sqrt_c


def build_edge_feature_tensor(src_tangent, dst_tangent, torch):
    return torch.cat(
        [
            src_tangent * dst_tangent,
            torch.abs(src_tangent - dst_tangent),
            src_tangent + dst_tangent,
        ],
        dim=1,
    )


def gate_value_from_logit(logit, torch):
    return 2.0 * torch.sigmoid(logit)


def gate_logit_from_init(gate_init: float) -> float:
    eps = 1e-4
    clipped = min(max(gate_init / 2.0, eps), 1.0 - eps)
    return math.log(clipped / (1.0 - clipped))


def build_hgcn_distance_terms(model_impl, dist, torch, F) -> dict[str, Any]:
    mode = str(getattr(model_impl, "distance_signal_mode", "log1p_zscore_tanh"))
    eps = 1e-6
    dist_sq = dist * dist
    scale = F.softplus(model_impl.log_scale) + eps
    zero = torch.zeros((), dtype=dist.dtype, device=dist.device)
    one = torch.ones((), dtype=dist.dtype, device=dist.device)
    log1p_dist_sq = torch.log1p(dist_sq)

    if mode == "raw_dist_sq":
        raw_signal = dist_sq
        pre_activation = dist_sq
        distance_signal = dist_sq
        center = zero
        spread = one
    elif mode == "log1p_zscore":
        raw_signal = log1p_dist_sq
        center = raw_signal.mean()
        spread = raw_signal.std(unbiased=False).clamp_min(eps)
        pre_activation = (raw_signal - center) / spread
        distance_signal = pre_activation
    elif mode == "log1p_zscore_tanh":
        raw_signal = log1p_dist_sq
        center = raw_signal.mean()
        spread = raw_signal.std(unbiased=False).clamp_min(eps)
        pre_activation = (raw_signal - center) / spread
        distance_signal = torch.tanh(pre_activation)
        stats_source = "batch"
    elif mode == "log1p_running_zscore_tanh":
        raw_signal = log1p_dist_sq
        batch_center = raw_signal.mean()
        batch_spread = raw_signal.std(unbiased=False).clamp_min(eps)
        running_initialized = bool(
            getattr(model_impl, "distance_signal_running_initialized", zero).detach().cpu().item() > 0.5
        )
        if model_impl.training:
            momentum = float(getattr(model_impl, "distance_stat_momentum", 0.1))
            if not running_initialized:
                model_impl.distance_signal_running_center.copy_(batch_center.detach())
                model_impl.distance_signal_running_spread.copy_(batch_spread.detach())
                model_impl.distance_signal_running_initialized.fill_(1.0)
            else:
                model_impl.distance_signal_running_center.mul_(1.0 - momentum).add_(momentum * batch_center.detach())
                model_impl.distance_signal_running_spread.mul_(1.0 - momentum).add_(momentum * batch_spread.detach())
            center = batch_center
            spread = batch_spread
            stats_source = "batch_train_running_updated"
        elif running_initialized:
            center = model_impl.distance_signal_running_center.detach()
            spread = model_impl.distance_signal_running_spread.detach().clamp_min(eps)
            stats_source = "running_eval"
        else:
            center = batch_center
            spread = batch_spread
            stats_source = "batch_eval_fallback"
        pre_activation = (raw_signal - center) / spread
        distance_signal = torch.tanh(pre_activation)
    else:
        raise ValueError(f"Unsupported distance_signal_mode: {mode}")

    distance_penalty = -scale * distance_signal
    return {
        "mode": mode,
        "scale": scale,
        "distance_squared": dist_sq,
        "raw_signal": raw_signal,
        "pre_activation": pre_activation,
        "signal": distance_signal,
        "penalty": distance_penalty,
        "center": center,
        "spread": spread,
        "stats_source": stats_source if "stats_source" in locals() else "batch",
    }


def build_hgcn_decoder_outputs(model_impl, src_vec, dst_vec, curvature: float, torch, F) -> dict[str, Any]:
    dist = poincare_distance(src_vec, dst_vec, curvature, torch)
    src_tangent = logmap0(src_vec, curvature, torch)
    dst_tangent = logmap0(dst_vec, curvature, torch)
    edge_features = build_edge_feature_tensor(src_tangent, dst_tangent, torch)
    mlp_logits = model_impl.edge_mlp(edge_features).squeeze(-1)
    dist_terms = build_hgcn_distance_terms(model_impl, dist, torch, F)

    residual_gate = None
    mlp_contribution = mlp_logits
    if getattr(model_impl, "decoder_version", "v2") == "v3":
        residual_gate = gate_value_from_logit(model_impl.residual_gate_logit, torch)
        mlp_contribution = residual_gate * mlp_logits

    logits = mlp_contribution + model_impl.decoder_bias + dist_terms["penalty"]
    return {
        "dist": dist,
        "src_tangent": src_tangent,
        "dst_tangent": dst_tangent,
        "edge_features": edge_features,
        "mlp_logits": mlp_logits,
        "mlp_contribution": mlp_contribution,
        "residual_gate": residual_gate,
        "distance_terms": dist_terms,
        "logits": logits,
    }


def summarize_tensor_by_label(values, labels, summarize_score_distribution) -> dict[str, Any]:
    return summarize_score_distribution(values, labels)


def build_hyperbolic_decoder_diagnostics(model, embeddings, edge_index, labels, summarize_score_distribution, torch, F) -> dict[str, Any]:
    model_impl = model.model.model
    src_vec = embeddings[edge_index[:, 0]]
    dst_vec = embeddings[edge_index[:, 1]]
    decoder_outputs = build_hgcn_decoder_outputs(model_impl, src_vec, dst_vec, model.curvature, torch, F)
    dist = decoder_outputs["dist"]
    dist_terms = decoder_outputs["distance_terms"]
    dist_sq = dist_terms["distance_squared"]
    distance_penalty = dist_terms["penalty"]
    decoder_bias = model_impl.decoder_bias.detach()

    diagnostics: dict[str, Any] = {
        "distance": summarize_tensor_by_label(dist, labels, summarize_score_distribution),
        "distance_squared": summarize_tensor_by_label(dist_sq, labels, summarize_score_distribution),
        "distance_penalty": summarize_tensor_by_label(distance_penalty, labels, summarize_score_distribution),
        "decoder_bias": float(decoder_bias.cpu().item()),
        "distance_scale": float(dist_terms["scale"].detach().cpu().item()),
    }

    if model.model_variant == "poincare_gcn_v1":
        logits = decoder_bias + distance_penalty
        diagnostics["reconstructed_logits"] = summarize_tensor_by_label(logits, labels, summarize_score_distribution)
        return diagnostics

    if model.model_variant in {"hgcn_residual_v2", "hgcn_residual_v3"}:
        src_tangent = decoder_outputs["src_tangent"]
        dst_tangent = decoder_outputs["dst_tangent"]
        edge_features = decoder_outputs["edge_features"]
        mlp_logits = decoder_outputs["mlp_logits"]
        mlp_contribution = decoder_outputs["mlp_contribution"]
        logits = decoder_outputs["logits"]
        diagnostics["distance_signal_mode"] = dist_terms["mode"]
        diagnostics["distance_stats_source"] = dist_terms["stats_source"]
        diagnostics["distance_raw_signal"] = summarize_tensor_by_label(
            dist_terms["raw_signal"], labels, summarize_score_distribution
        )
        diagnostics["distance_signal_pre_activation"] = summarize_tensor_by_label(
            dist_terms["pre_activation"], labels, summarize_score_distribution
        )
        diagnostics["distance_signal"] = summarize_tensor_by_label(
            dist_terms["signal"], labels, summarize_score_distribution
        )
        diagnostics["distance_signal_center"] = float(dist_terms["center"].detach().cpu().item())
        diagnostics["distance_signal_spread"] = float(dist_terms["spread"].detach().cpu().item())
        if hasattr(model_impl, "distance_signal_running_center"):
            diagnostics["distance_signal_running_center"] = float(
                model_impl.distance_signal_running_center.detach().cpu().item()
            )
            diagnostics["distance_signal_running_spread"] = float(
                model_impl.distance_signal_running_spread.detach().cpu().item()
            )
        diagnostics["mlp_logits"] = summarize_tensor_by_label(mlp_logits, labels, summarize_score_distribution)
        diagnostics["mlp_contribution"] = summarize_tensor_by_label(
            mlp_contribution, labels, summarize_score_distribution
        )
        if decoder_outputs["residual_gate"] is not None:
            diagnostics["residual_gate"] = float(decoder_outputs["residual_gate"].detach().cpu().item())
        diagnostics["reconstructed_logits"] = summarize_tensor_by_label(logits, labels, summarize_score_distribution)
        diagnostics["raw_feature_norm"] = {
            "src_tangent_mean_norm": float(torch.norm(src_tangent, dim=1).mean().detach().cpu().item()),
            "dst_tangent_mean_norm": float(torch.norm(dst_tangent, dim=1).mean().detach().cpu().item()),
            "edge_feature_mean_norm": float(torch.norm(edge_features, dim=1).mean().detach().cpu().item()),
        }
    return diagnostics


def check_finite(name: str, tensor, torch) -> None:
    if torch.isfinite(tensor).all():
        return
    raise ValueError(f"{name} contains non-finite values.")


class HyperbolicLinkPredictor:
    def __init__(self, num_nodes: int, config: dict, torch, F):
        self.torch = torch
        self.F = F
        self.model_variant = str(config.get("model_variant", "poincare_gcn_v1"))
        input_dim = int(config.get("input_dim", 64))
        hidden_dim = int(config.get("hidden_dim", 64))
        output_dim = int(config.get("output_dim", 32))
        dropout = float(config.get("dropout", 0.2))
        curvature = float(config.get("curvature", 1.0))
        decoder_hidden_dim = int(config.get("decoder_hidden_dim", max(output_dim * 2, 32)))
        distance_signal_mode = str(config.get("distance_signal_mode", "log1p_zscore_tanh"))
        distance_stat_momentum = float(config.get("distance_stat_momentum", 0.1))
        residual_gate_init = float(config.get("residual_gate_init", 1.0))
        self.curvature = curvature

        if self.model_variant == "poincare_gcn_v1":
            self.model = PoincareGCNModel(
                num_nodes=num_nodes,
                input_dim=input_dim,
                hidden_dim=hidden_dim,
                output_dim=output_dim,
                dropout=dropout,
                curvature=curvature,
                torch=torch,
                F=F,
            )
        elif self.model_variant == "hgcn_residual_v2":
            self.model = HGCNResidualV2Model(
                num_nodes=num_nodes,
                input_dim=input_dim,
                hidden_dim=hidden_dim,
                output_dim=output_dim,
                dropout=dropout,
                curvature=curvature,
                decoder_hidden_dim=decoder_hidden_dim,
                distance_signal_mode=distance_signal_mode,
                torch=torch,
                F=F,
            )
        elif self.model_variant == "hgcn_residual_v3":
            self.model = HGCNResidualV3Model(
                num_nodes=num_nodes,
                input_dim=input_dim,
                hidden_dim=hidden_dim,
                output_dim=output_dim,
                dropout=dropout,
                curvature=curvature,
                decoder_hidden_dim=decoder_hidden_dim,
                distance_signal_mode=distance_signal_mode,
                distance_stat_momentum=distance_stat_momentum,
                residual_gate_init=residual_gate_init,
                torch=torch,
                F=F,
            )
        else:
            raise ValueError(f"Unsupported model_variant: {self.model_variant}")

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


class PoincareGCNModel:
    def __init__(
        self,
        num_nodes: int,
        input_dim: int,
        hidden_dim: int,
        output_dim: int,
        dropout: float,
        curvature: float,
        torch,
        F,
    ):
        self.torch = torch
        self.F = F
        self.curvature = curvature
        self.dropout = dropout

        class _Model(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.node_features = torch.nn.Parameter(torch.empty(num_nodes, input_dim))
                self.lin1 = torch.nn.Linear(input_dim, hidden_dim, bias=False)
                self.lin2 = torch.nn.Linear(hidden_dim, output_dim, bias=False)
                self.log_scale = torch.nn.Parameter(torch.tensor(0.0))
                self.decoder_bias = torch.nn.Parameter(torch.tensor(0.0))
                torch.nn.init.xavier_uniform_(self.node_features)
                torch.nn.init.xavier_uniform_(self.lin1.weight)
                torch.nn.init.xavier_uniform_(self.lin2.weight)

            def encode(inner_self, adjacency):
                h = inner_self.node_features
                h = torch.sparse.mm(adjacency, h)
                h = inner_self.lin1(h)
                x = expmap0(h, curvature, torch)
                h = logmap0(x, curvature, torch)
                h = torch.relu(h)
                h = torch.nn.functional.dropout(h, p=dropout, training=inner_self.training)
                h = torch.sparse.mm(adjacency, h)
                h = inner_self.lin2(h)
                x = expmap0(h, curvature, torch)
                return x

            def decode(inner_self, embeddings, edge_index):
                src_vec = embeddings[edge_index[:, 0]]
                dst_vec = embeddings[edge_index[:, 1]]
                dist = poincare_distance(src_vec, dst_vec, curvature, torch)
                scale = F.softplus(inner_self.log_scale) + 1e-6
                return inner_self.decoder_bias - scale * dist * dist

        self.model = _Model()

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


class HGCNResidualV2Model:
    def __init__(
        self,
        num_nodes: int,
        input_dim: int,
        hidden_dim: int,
        output_dim: int,
        dropout: float,
        curvature: float,
        decoder_hidden_dim: int,
        distance_signal_mode: str,
        torch,
        F,
    ):
        self.torch = torch
        self.F = F
        self.curvature = curvature

        class _Model(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.decoder_version = "v2"
                self.node_features = torch.nn.Parameter(torch.empty(num_nodes, input_dim))
                self.input_proj = torch.nn.Linear(input_dim, hidden_dim, bias=False)
                self.agg1 = torch.nn.Linear(hidden_dim, hidden_dim, bias=False)
                self.agg2 = torch.nn.Linear(hidden_dim, hidden_dim, bias=False)
                self.out_proj = torch.nn.Linear(hidden_dim, output_dim, bias=False)
                self.skip_hidden = torch.nn.Linear(hidden_dim, hidden_dim, bias=False)
                self.norm1 = torch.nn.LayerNorm(hidden_dim)
                self.norm2 = torch.nn.LayerNorm(hidden_dim)
                self.distance_signal_mode = distance_signal_mode
                self.edge_mlp = torch.nn.Sequential(
                    torch.nn.Linear(output_dim * 3, decoder_hidden_dim),
                    torch.nn.ReLU(),
                    torch.nn.Dropout(p=dropout),
                    torch.nn.Linear(decoder_hidden_dim, 1),
                )
                self.log_scale = torch.nn.Parameter(torch.tensor(0.0))
                self.decoder_bias = torch.nn.Parameter(torch.tensor(0.0))
                torch.nn.init.xavier_uniform_(self.node_features)
                for module in [
                    self.input_proj,
                    self.agg1,
                    self.agg2,
                    self.out_proj,
                    self.skip_hidden,
                ]:
                    torch.nn.init.xavier_uniform_(module.weight)
                for module in self.edge_mlp:
                    if isinstance(module, torch.nn.Linear):
                        torch.nn.init.xavier_uniform_(module.weight)
                        if module.bias is not None:
                            torch.nn.init.zeros_(module.bias)

            def encode(inner_self, adjacency):
                h0 = inner_self.input_proj(inner_self.node_features)
                h = torch.sparse.mm(adjacency, h0)
                h = inner_self.agg1(h)
                h = inner_self.norm1(h)
                h = torch.nn.functional.gelu(h)
                h = torch.nn.functional.dropout(h, p=dropout, training=inner_self.training)

                x = expmap0(h, curvature, torch)
                tangent_h = logmap0(x, curvature, torch)
                tangent_h = torch.sparse.mm(adjacency, tangent_h)
                tangent_h = inner_self.agg2(tangent_h)
                tangent_h = tangent_h + inner_self.skip_hidden(h0)
                tangent_h = inner_self.norm2(tangent_h)
                tangent_h = torch.nn.functional.gelu(tangent_h)
                tangent_h = torch.nn.functional.dropout(tangent_h, p=dropout, training=inner_self.training)
                tangent_h = inner_self.out_proj(tangent_h)
                return expmap0(tangent_h, curvature, torch)

            def decode(inner_self, embeddings, edge_index):
                src_vec = embeddings[edge_index[:, 0]]
                dst_vec = embeddings[edge_index[:, 1]]
                dist = poincare_distance(src_vec, dst_vec, curvature, torch)
                src_tangent = logmap0(src_vec, curvature, torch)
                dst_tangent = logmap0(dst_vec, curvature, torch)
                edge_features = build_edge_feature_tensor(src_tangent, dst_tangent, torch)
                edge_logits = inner_self.edge_mlp(edge_features).squeeze(-1)
                dist_terms = build_hgcn_distance_terms(inner_self, dist, torch, F)
                return edge_logits + inner_self.decoder_bias + dist_terms["penalty"]

        self.model = _Model()

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


class HGCNResidualV3Model:
    def __init__(
        self,
        num_nodes: int,
        input_dim: int,
        hidden_dim: int,
        output_dim: int,
        dropout: float,
        curvature: float,
        decoder_hidden_dim: int,
        distance_signal_mode: str,
        distance_stat_momentum: float,
        residual_gate_init: float,
        torch,
        F,
    ):
        self.torch = torch
        self.F = F
        self.curvature = curvature

        class _Model(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.decoder_version = "v3"
                self.node_features = torch.nn.Parameter(torch.empty(num_nodes, input_dim))
                self.input_proj = torch.nn.Linear(input_dim, hidden_dim, bias=False)
                self.agg1 = torch.nn.Linear(hidden_dim, hidden_dim, bias=False)
                self.agg2 = torch.nn.Linear(hidden_dim, hidden_dim, bias=False)
                self.out_proj = torch.nn.Linear(hidden_dim, output_dim, bias=False)
                self.skip_hidden = torch.nn.Linear(hidden_dim, hidden_dim, bias=False)
                self.norm1 = torch.nn.LayerNorm(hidden_dim)
                self.norm2 = torch.nn.LayerNorm(hidden_dim)
                self.distance_signal_mode = distance_signal_mode
                self.distance_stat_momentum = distance_stat_momentum
                self.edge_mlp = torch.nn.Sequential(
                    torch.nn.Linear(output_dim * 3, decoder_hidden_dim),
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
                    self.agg1,
                    self.agg2,
                    self.out_proj,
                    self.skip_hidden,
                ]:
                    torch.nn.init.xavier_uniform_(module.weight)
                for module in self.edge_mlp:
                    if isinstance(module, torch.nn.Linear):
                        torch.nn.init.xavier_uniform_(module.weight)
                        if module.bias is not None:
                            torch.nn.init.zeros_(module.bias)

            def encode(inner_self, adjacency):
                h0 = inner_self.input_proj(inner_self.node_features)
                h = torch.sparse.mm(adjacency, h0)
                h = inner_self.agg1(h)
                h = inner_self.norm1(h)
                h = torch.nn.functional.gelu(h)
                h = torch.nn.functional.dropout(h, p=dropout, training=inner_self.training)

                x = expmap0(h, curvature, torch)
                tangent_h = logmap0(x, curvature, torch)
                tangent_h = torch.sparse.mm(adjacency, tangent_h)
                tangent_h = inner_self.agg2(tangent_h)
                tangent_h = tangent_h + inner_self.skip_hidden(h0)
                tangent_h = inner_self.norm2(tangent_h)
                tangent_h = torch.nn.functional.gelu(tangent_h)
                tangent_h = torch.nn.functional.dropout(tangent_h, p=dropout, training=inner_self.training)
                tangent_h = inner_self.out_proj(tangent_h)
                return expmap0(tangent_h, curvature, torch)

            def decode(inner_self, embeddings, edge_index):
                src_vec = embeddings[edge_index[:, 0]]
                dst_vec = embeddings[edge_index[:, 1]]
                decoder_outputs = build_hgcn_decoder_outputs(inner_self, src_vec, dst_vec, curvature, torch, F)
                return decoder_outputs["logits"]

        self.model = _Model()

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
    if not logits.isfinite().all():
        raise ValueError("Evaluation logits contain non-finite values.")
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
        "graph_root": graph_root,
        "artifacts_root": artifacts_root,
        "declarations": declarations,
        "edges": edges,
        "graph_summary": graph_summary,
        "split": split,
        "node_ids": node_ids,
        "dependency_status": dependency_status,
        "negative_sampling_stats": negative_sampling_stats,
    }


def train_hyperbolic_model(
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
    learning_rate = float(config.get("learning_rate", 0.001))
    weight_decay = float(config.get("weight_decay", 1e-4))
    epochs = int(config.get("epochs", 80))
    eval_every = int(config.get("eval_every", 5))
    early_stopping_patience = int(config.get("early_stopping_patience", 20))
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
        embeddings = model.encode(adjacency)
        check_finite("train_embeddings", embeddings, torch)
        train_logits = model.decode(embeddings, train_edges)
        check_finite("train_logits", train_logits, torch)
        loss = criterion(train_logits, train_labels)
        check_finite("train_loss", loss, torch)

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=grad_clip_norm)
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
        "grad_clip_norm": grad_clip_norm,
        "model_variant": str(config.get("model_variant", "poincare_gcn_v1")),
        "history": history,
    }


def run_hyperbolic_experiment(config: dict) -> dict:
    data = prepare_run_data(config)
    artifacts_root = data["artifacts_root"]

    if config.get("dry_run", False) or not all(data["dependency_status"].values()):
        notes = {
            "mode": "dry_run",
            "message": (
                "Hyperbolic baseline completed data validation and split generation. "
                "Set dry_run=false and ensure torch/numpy/sklearn are available to train."
            ),
        }
        write_json(artifacts_root / "hyperbolic_dry_run_summary.json", notes)
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

    model = HyperbolicLinkPredictor(len(node_ids), config, torch, F)
    embeddings, train_stats = train_hyperbolic_model(
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
    metrics["decoder_diagnostics"] = {
        "val": build_hyperbolic_decoder_diagnostics(
            model=model,
            embeddings=final_embeddings,
            edge_index=val_edges,
            labels=val_labels,
            summarize_score_distribution=summarize_score_distribution,
            torch=torch,
            F=F,
        ),
        "test": build_hyperbolic_decoder_diagnostics(
            model=model,
            embeddings=final_embeddings,
            edge_index=test_edges,
            labels=test_labels,
            summarize_score_distribution=summarize_score_distribution,
            torch=torch,
            F=F,
        ),
    }
    write_json(artifacts_root / "metrics.json", metrics)

    result_summary = {
        "run_id": config["run_id"],
        "model_variant": str(config.get("model_variant", "poincare_gcn_v1")),
        "curvature": float(config.get("curvature", 1.0)),
        "input_dim": int(config.get("input_dim", 64)),
        "hidden_dim": int(config.get("hidden_dim", 64)),
        "output_dim": int(config.get("output_dim", 32)),
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
        }
    write_json(artifacts_root / "result_summary.json", result_summary)

    print("[done] hyperbolic training completed")
    print(f"[done] variant: {result_summary['model_variant']}")
    print(f"[done] val AP: {fmt_metric(metrics['val']['average_precision'])}")
    print(f"[done] test AP: {fmt_metric(metrics['test']['average_precision'])}")
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
    run_hyperbolic_experiment(config)


if __name__ == "__main__":
    main()
