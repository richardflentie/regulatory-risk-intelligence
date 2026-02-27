"""
feature_engineering.py

Builds a bank x month panel and rolling-window features from enforcement events.
"""

from __future__ import annotations
import pandas as pd


def make_monthly_panel(df_events: pd.DataFrame) -> pd.DataFrame:
    """
    Input df_events must contain:
      - institution (canonical name)
      - action_date (datetime)
    Returns a bank x month table with event_count per month.
    """
    df = df_events.copy()
    df["action_date"] = pd.to_datetime(df["action_date"], errors="coerce")
    df = df.dropna(subset=["action_date", "institution"])

    # Month bucket (month start)
    df["month"] = df["action_date"].dt.to_period("M").dt.to_timestamp()

    monthly = (
        df.groupby(["institution", "month"])
          .size()
          .reset_index(name="event_count")
          .sort_values(["institution", "month"])
    )
    return monthly


def fill_missing_months(monthly: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure every institution has continuous monthly rows (fills missing months with 0 events).
    """
    monthly = monthly.copy()
    all_banks = monthly["institution"].unique()

    min_m = monthly["month"].min()
    max_m = monthly["month"].max()
    all_months = pd.date_range(min_m, max_m, freq="MS")  # month start

    idx = pd.MultiIndex.from_product([all_banks, all_months], names=["institution", "month"])
    base = monthly.set_index(["institution", "month"]).reindex(idx).reset_index()
    base["event_count"] = base["event_count"].fillna(0).astype(int)

    return base.sort_values(["institution", "month"]).reset_index(drop=True)


def add_rolling_features(panel: pd.DataFrame, window_months: int = 6) -> pd.DataFrame:
    """
    Adds rolling features per bank:
      - events_last_{window}m: rolling sum of event_count over prior window months including current month
    """
    df = panel.copy()
    df = df.sort_values(["institution", "month"])

    col = f"events_last_{window_months}m"
    df[col] = (
        df.groupby("institution")["event_count"]
          .rolling(window=window_months, min_periods=1)
          .sum()
          .reset_index(level=0, drop=True)
          .astype(int)
    )
    return df


def add_peer_feature(panel: pd.DataFrame, window_months: int = 6) -> pd.DataFrame:
    """
    Adds peer activity feature:
      - peer_events_last_{window}m: total rolling events across all banks minus the bank's own rolling events
    """
    df = panel.copy()
    own_col = f"events_last_{window_months}m"
    peer_col = f"peer_events_last_{window_months}m"

    if own_col not in df.columns:
        df = add_rolling_features(df, window_months=window_months)

    # Total rolling events across all institutions by month
    total_by_month = df.groupby("month")[own_col].sum().rename("total_events_rolling").reset_index()
    df = df.merge(total_by_month, on="month", how="left")

    df[peer_col] = (df["total_events_rolling"] - df[own_col]).astype(int)
    df = df.drop(columns=["total_events_rolling"])

    return df