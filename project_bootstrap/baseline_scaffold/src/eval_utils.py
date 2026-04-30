from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)


def logits_to_probabilities(logits, labels):
    prob = logits.sigmoid().detach().cpu().numpy().astype(np.float64)
    y = labels.detach().cpu().numpy().astype(int)
    return prob, y


def evaluate_probabilities(prob, y, threshold: float) -> dict:
    pred = (prob >= threshold).astype(int)

    auroc = None
    average_precision = None
    if len(set(y.tolist())) >= 2:
        auroc = float(roc_auc_score(y, prob))
    if int(y.sum()) > 0:
        average_precision = float(average_precision_score(y, prob))

    return {
        "threshold": float(threshold),
        "auroc": auroc,
        "average_precision": average_precision,
        "accuracy": float(accuracy_score(y, pred)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "brier": float(brier_score_loss(y, prob)),
        "num_examples": int(len(y)),
        "num_positive": int(y.sum()),
        "num_negative": int(len(y) - y.sum()),
        "predicted_positive_rate": float(pred.mean()),
    }


def select_threshold_by_max_f1(prob, y) -> tuple[float, dict]:
    precision, recall, thresholds = precision_recall_curve(y, prob)
    if len(thresholds) == 0:
        threshold = 0.5
        return threshold, evaluate_probabilities(prob, y, threshold)

    precision = precision[:-1]
    recall = recall[:-1]
    denom = precision + recall
    f1 = np.divide(2.0 * precision * recall, denom, out=np.zeros_like(denom), where=denom > 0)
    best_idx = int(np.argmax(f1))
    threshold = float(thresholds[best_idx])
    return threshold, evaluate_probabilities(prob, y, threshold)


def fit_temperature_scaler(val_logits, val_labels, torch) -> float:
    logits = val_logits.detach().clone()
    labels = val_labels.detach().clone()
    criterion = torch.nn.BCEWithLogitsLoss()
    log_temperature = torch.nn.Parameter(torch.zeros(1, dtype=logits.dtype, device=logits.device))
    optimizer = torch.optim.LBFGS([log_temperature], lr=0.1, max_iter=50, line_search_fn="strong_wolfe")

    def closure():
        optimizer.zero_grad()
        temperature = torch.exp(log_temperature).clamp_min(1e-3)
        loss = criterion(logits / temperature, labels)
        loss.backward()
        return loss

    optimizer.step(closure)
    temperature = float(torch.exp(log_temperature).detach().cpu().item())
    return max(temperature, 1e-3)


def build_calibrated_metrics(val_logits, val_labels, test_logits, test_labels, torch) -> dict:
    val_prob_raw, val_y = logits_to_probabilities(val_logits, val_labels)
    test_prob_raw, test_y = logits_to_probabilities(test_logits, test_labels)

    default_threshold = 0.5
    raw_metrics = {
        "val": evaluate_probabilities(val_prob_raw, val_y, default_threshold),
        "test": evaluate_probabilities(test_prob_raw, test_y, default_threshold),
    }

    temperature = fit_temperature_scaler(val_logits, val_labels, torch)
    val_logits_calibrated = val_logits.detach() / temperature
    test_logits_calibrated = test_logits.detach() / temperature
    val_prob_calibrated, _ = logits_to_probabilities(val_logits_calibrated, val_labels)
    test_prob_calibrated, _ = logits_to_probabilities(test_logits_calibrated, test_labels)

    selected_threshold, val_selected_metrics = select_threshold_by_max_f1(val_prob_calibrated, val_y)
    calibrated_metrics = {
        "temperature": float(temperature),
        "threshold_selection": "val_max_f1_after_temperature_scaling",
        "selected_threshold": float(selected_threshold),
        "val": val_selected_metrics,
        "test": evaluate_probabilities(test_prob_calibrated, test_y, selected_threshold),
    }

    return {
        "raw": raw_metrics,
        "calibrated": calibrated_metrics,
    }


def summarize_score_distribution(logits, labels) -> dict:
    logit_np = logits.detach().cpu().numpy().astype(np.float64)
    prob_np = logits.sigmoid().detach().cpu().numpy().astype(np.float64)
    y = labels.detach().cpu().numpy().astype(int)

    def stats(arr: np.ndarray) -> dict:
        if arr.size == 0:
            return {
                "count": 0,
                "mean": None,
                "std": None,
                "min": None,
                "p05": None,
                "p25": None,
                "p50": None,
                "p75": None,
                "p95": None,
                "max": None,
            }
        percentiles = np.percentile(arr, [5, 25, 50, 75, 95])
        return {
            "count": int(arr.size),
            "mean": float(arr.mean()),
            "std": float(arr.std()),
            "min": float(arr.min()),
            "p05": float(percentiles[0]),
            "p25": float(percentiles[1]),
            "p50": float(percentiles[2]),
            "p75": float(percentiles[3]),
            "p95": float(percentiles[4]),
            "max": float(arr.max()),
        }

    pos_mask = y == 1
    neg_mask = y == 0

    return {
        "all": {
            "logits": stats(logit_np),
            "probabilities": stats(prob_np),
            "predicted_positive_rate_at_0_5": float((prob_np >= 0.5).mean()) if prob_np.size else 0.0,
        },
        "positive": {
            "logits": stats(logit_np[pos_mask]),
            "probabilities": stats(prob_np[pos_mask]),
        },
        "negative": {
            "logits": stats(logit_np[neg_mask]),
            "probabilities": stats(prob_np[neg_mask]),
        },
    }
