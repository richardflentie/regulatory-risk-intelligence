import pandas as pd
def make_lift_table(y_true, y_score, n_bins: int = 10) -> pd.DataFrame:
    """
    Create a decile lift table based on predicted probabilities.
    Returns a dataframe with bin stats (bin 1 = highest scores).
    """
    df = pd.DataFrame({"y_true": y_true, "y_score": y_score}).dropna()
    df = df.sort_values("y_score", ascending=False).reset_index(drop=True)

    # Assign bins by rank (top decile = bin 1)
    df["bin"] = pd.qcut(df.index, q=n_bins, labels=False, duplicates="drop") + 1

    out = (
        df.groupby("bin", as_index=False)
          .agg(
              count=("y_true", "size"),
              positives=("y_true", "sum"),
              avg_score=("y_score", "mean"),
          )
          .sort_values("bin")
          .reset_index(drop=True)
    )

    out["positive_rate"] = out["positives"] / out["count"]

    total_positives = out["positives"].sum()
    out["cum_positives"] = out["positives"].cumsum()
    out["cum_positive_capture"] = out["cum_positives"] / (total_positives if total_positives else 1)

    return out