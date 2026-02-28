from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve, roc_auc_score


def save_roc_curve(y_true, y_score, out_path: Path) -> float:
    """
    Save ROC curve plot and return AUC.
    """
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auc = roc_auc_score(y_true, y_score)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.plot(fpr, tpr)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"ROC Curve (AUC={auc:.4f})")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()

    return float(auc)