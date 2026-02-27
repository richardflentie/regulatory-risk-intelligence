"""
labeling.py

Creates forward-looking labels for time-series modeling.
"""

from __future__ import annotations
import pandas as pd


def add_future_event_label(panel: pd.DataFrame, horizon_months: int = 6) -> pd.DataFrame:
    """
    Adds y_next_{horizon}m label:
      1 if there is >=1 event in the next horizon_months (excluding current month),
      0 otherwise.

    Requires columns:
      - institution
      - month (datetime-like)
      - event_count (int)
    """
    df = panel.copy()
    df["month"] = pd.to_datetime(df["month"], errors="coerce")
    df = df.sort_values(["institution", "month"]).reset_index(drop=True)

    # For each institution, look ahead into the next N months (exclude current month)
    future_sum = (
        df.groupby("institution")["event_count"]
          .transform(lambda s: s.shift(-1).rolling(horizon_months, min_periods=1).sum())
    )

    label_col = f"y_next_{horizon_months}m"
    df[label_col] = (future_sum.fillna(0) > 0).astype(int)

    return df
