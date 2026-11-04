"""Step 1: fetch the Hillstrom dataset, add treatment/target columns, save to SQLite.

Run from repo root:  python -m src.load_data
"""
import sqlite3

import pandas as pd
from sklift.datasets import fetch_hillstrom

from src.config import CONTROL_LABEL, DATA_DIR, DB_PATH, TABLE_NAME


def load_raw() -> pd.DataFrame:
    """Download Hillstrom (cached after the first time) and return ONE dataframe."""
    # target_col="all" -> target is a dataframe with visit, conversion, spend
    ds = fetch_hillstrom(target_col="all")

    df = ds.data.copy()                      # features: recency, history, mens, ...
    df["segment"] = ds.treatment.values      # original label: Mens / Womens / No E-Mail
    df["visit"] = ds.target["visit"].values
    df["conversion"] = ds.target["conversion"].values
    df["spend"] = ds.target["spend"].values
    return df


def add_modeling_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Create the columns our whole project uses."""
    # treatment = 1 if the customer got ANY email``, 0 if they got No E-Mail
    df["treatment"] = (df["segment"] != CONTROL_LABEL).astype(int)

    # target = our retention proxy: did the customer visit the site within 2 weeks?
    df["target"] = df["visit"]

    # A unique id per customer (the raw file has none)
    df.insert(0, "customer_id", range(1, len(df) + 1))
    return df


def save_to_sqlite(df: pd.DataFrame) -> None:
    """Write the dataframe to the `customers` table (replaces it if it exists)."""
    DATA_DIR.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)


def main() -> None:
    df = add_modeling_columns(load_raw())
    save_to_sqlite(df)

    # ---- Sanity checks: always look at your data before modeling ----
    print(f"Rows: {len(df):,} | Columns: {df.shape[1]}")
    print("\nColumns:", list(df.columns))
    print("\nMissing values per column:\n", df.isna().sum()[df.isna().sum() > 0])
    print("\nOriginal segment counts:\n", df["segment"].value_counts())
    print("\nTreatment counts (1 = any email, 0 = no email):\n", df["treatment"].value_counts())
    print("\nVisit rate by treatment:\n", df.groupby("treatment")["target"].mean().round(4))
    print(f"\nSaved table '{TABLE_NAME}' to {DB_PATH}")


if __name__ == "__main__":
    main()
