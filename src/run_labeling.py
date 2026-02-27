"""
Run labeling end-to-end:
- load feature panel
- add forward-looking label
- save labeled dataset
"""

from pathlib import Path
import pandas as pd

from src.labeling import add_future_event_label


def main():
    in_path = Path("data/processed/features_monthly.csv")
    out_path = Path("data/processed/features_labeled.csv")

    if not in_path.exists():
        raise FileNotFoundError(
            f"Missing features file: {in_path}. Run feature engineering first: python -m src.run_feature_engineering"
        )

    df = pd.read_csv(in_path)
    labeled = add_future_event_label(df, horizon_months=6)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    labeled.to_csv(out_path, index=False)

    print(f"Saved labeled dataset to: {out_path}")
    print(labeled.head())


if __name__ == "__main__":
    main()
    