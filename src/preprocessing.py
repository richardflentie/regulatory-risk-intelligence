"""
preprocessing.py

Cleans and standardizes OCC enforcement actions data for downstream feature engineering.
"""

from __future__ import annotations

from typing import Optional
import pandas as pd

from .bank_alias import normalize_bank_name


def preprocess_occ_enforcement(
    df: pd.DataFrame,
    institution_col: str = "institution",
    date_col: str = "action_date",
    action_type_col: Optional[str] = None,
) -> pd.DataFrame:
    """
    Standardize column names, parse dates, normalize bank names, and drop unusable rows.

    Returns a dataframe with at least:
      - action_date (datetime64[ns])
      - institution_raw (str)
      - institution (str)
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["action_date", "institution_raw", "institution"])

    work = df.copy()

    # --- Validate required columns ---
    if institution_col not in work.columns:
        raise KeyError(f"Missing institution column: '{institution_col}'")
    if date_col not in work.columns:
        raise KeyError(f"Missing date column: '{date_col}'")

    # --- Parse dates ---
    work[date_col] = pd.to_datetime(work[date_col], errors="coerce")

    # --- Standardize institution ---
    work["institution_raw"] = work[institution_col].astype(str)
    work["institution"] = work["institution_raw"].apply(normalize_bank_name)

    # --- Optional action type ---
    if action_type_col and action_type_col in work.columns:
        work["action_type"] = work[action_type_col].astype(str)
    elif "action_type" in work.columns:
        work["action_type"] = work["action_type"].astype(str)

    # --- Drop unusable rows ---
    work = work.dropna(subset=[date_col])
    work = work[work["institution_raw"].str.strip().ne("")]

    # --- Select + order core columns ---
    keep_cols = ["institution_raw", "institution", date_col]
    if "action_type" in work.columns:
        keep_cols.append("action_type")

    # Keep any id-like field if it exists
    for candidate in ["id", "action_id", "enforcement_id"]:
        if candidate in work.columns and candidate not in keep_cols:
            keep_cols.insert(0, candidate)
            break

    out = work.loc[:, [c for c in keep_cols if c in work.columns]].copy()
    out = out.rename(columns={date_col: "action_date"})
    out = out.sort_values("action_date").reset_index(drop=True)

    return out