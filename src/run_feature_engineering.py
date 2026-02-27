"""
Run feature engineering end-to-end:
- load cleaned events
- build monthly panel
- add rolling and peer features
- save output
"""

from pathlib import Path
import pandas as pd

from src.feature_engineering import (
    make_monthly_panel,
    fill_missing_months,
    add_rolling_features,
    add_peer_feature,
)


def main():
    clean_path = Path("data/processed/occ_enforcement_clean.csv")
    out_path = Path("data/processed/features_monthly.csv")

    if not clean_path.exists():
        raise FileNotFoundError(
            f"Missing cleaned file: {clean_path}. Run preprocessing first: python -m src.run_preprocessing"
        )

    df_clean = pd.read_csv(clean_path)
    df_clean["action_date"] = pd.to_datetime(df_clean["action_date"], errors="coerce")

    monthly = make_monthly_panel(df_clean)
    panel = fill_missing_months(monthly)
    panel = add_rolling_features(panel, window_months=6)
    panel = add_peer_feature(panel, window_months=6)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(out_path, index=False)

    print(f"Saved features to: {out_path}")
    print(panel.head())


if __name__ == "__main__":
    main()