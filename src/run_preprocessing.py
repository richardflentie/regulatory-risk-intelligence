"""
Run preprocessing end-to-end:
- load raw CSV
- preprocess
- save processed output
"""
from pathlib import Path
import pandas as pd
from src.preprocessing import preprocess_occ_enforcement

def main():
    raw_path = Path("data/raw/occ_enforcement.csv")
    out_path = Path("data/processed/occ_enforcement_clean.csv")

    if not raw_path.exists():
        raise FileNotFoundError(f"Missing raw file: {raw_path}")

    df_raw = pd.read_csv(raw_path)

    df_clean = preprocess_occ_enforcement(
        df_raw,
        institution_col="BankName",
        date_col="event_date",
        action_type_col="EnforcementTypeDescription",
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(out_path, index=False)

    print(f"Saved cleaned file to: {out_path}")
    print(df_clean.head())


if __name__ == "__main__":
    main()