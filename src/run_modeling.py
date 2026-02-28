"""
Run baseline modeling.
"""
import json
from src.plot_results import save_roc_curve
from pathlib import Path
import pandas as pd

from src.modeling import train_baseline_model
from src.evaluation import make_lift_table


def main():
    path = Path("data/processed/features_labeled.csv")
    if not path.exists():
        raise FileNotFoundError ("Missing labeled dataset. Run: python -m scr.run_labeling")
    
    df = pd.read_csv(path)
    model, auc, test_df, probs, features = train_baseline_model(df)

    y_test = test_df["y_next_6m"].values 
    lift = make_lift_table(y_test, probs, n_bins=10)

    print(f"Baseline ROC-AUC: {auc:4f}\n")
    print("Lift table(bin 1 = top decile):")
    print(lift.to_string(index=False))
    #save lift table
    out_lift = Path("outputs/lift_table.csv")
    out_lift.parent.mkdir(parents=True, exist_ok=True)
    lift.to_csv(out_lift, index=False) 
    print(f"Saved lift table to: {out_lift}")

    #--- save ROC cuve ----

    roc_path = Path("outputs/figures/roc_curve.png")
    auc_plot = save_roc_curve(y_test, probs, roc_path)
    print(f"Saved ROC curve to: {roc_path}")
    
    #save metrics locally
    metrics = {
        "roc_auc": float(auc), 
        "features": features, 
        "test_rows": int (len(test_df)), 
        "positive_rate_test": float(test_df["y_next_6m"].mean()), 
        "top_decile_capture": float(lift.loc[lift["bin"]==1, "cum_positive_capture"].values[0]),
    }

    out_metrics = Path("outputs/model_metrics.json")
    out_metrics.parent.mkdir(parents=True, exist_ok=True)
    out_metrics.write_text(json.dumps(metrics,indent=2))

    print (f"\nSaved metrics to: {out_metrics}")

    
if __name__ == "__main__":
    main()