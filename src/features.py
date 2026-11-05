"""Step 3: build the model matrix (encoded features) and make a stratified train/test split.

Run from repo root:  python -m src.features
"""
import sqlite3

import pandas as pd
from sklearn.model_selection import train_test_split

from src.config import DB_PATH, RANDOM_SEED, TABLE_NAME, TEST_SIZE

# Only information known BEFORE the email was sent. Never visit / conversion / spend (leakage!).
NUMERIC_FEATURES = ["recency", "history", "mens", "womens", "newbie"]
CATEGORICAL_FEATURES = ["zip_code", "channel"]


def load_customers() -> pd.DataFrame:
    """Read the customers table written in Step 1."""
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql(f"SELECT * FROM {TABLE_NAME}", conn)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return the feature matrix X: numeric columns + one-hot encoded categoricals."""
    X = df[["customer_id"] + NUMERIC_FEATURES + CATEGORICAL_FEATURES].copy()
    X = X.set_index("customer_id")     # keep customer_id as the index to map predictions back later

    # one-hot: zip_code -> zip_code_Urban, zip_code_Rural, ...  (dtype=int gives 0/1, not True/False)
    X = pd.get_dummies(X, columns=CATEGORICAL_FEATURES, dtype=int)
    return X


def split_data(df: pd.DataFrame):
    """Stratified 70/30 split on treatment+target combined.

    Returns X_train, X_test, t_train, t_test, y_train, y_test
      X = features, t = treatment (0/1), y = target (visit 0/1)
    """
    X = build_features(df)
    t = df.set_index("customer_id")["treatment"]
    y = df.set_index("customer_id")["target"]

    # 4 combos: (t=0,y=0) (t=0,y=1) (t=1,y=0) (t=1,y=1) -> keep the same mix in train and test
    strata = t.astype(str) + "_" + y.astype(str)

    return train_test_split(
        X, t, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
        stratify=strata,
    )


def main() -> None:
    df = load_customers()
    X_train, X_test, t_train, t_test, y_train, y_test = split_data(df)

    print(f"Feature columns ({X_train.shape[1]}):", list(X_train.columns))
    print(f"\nTrain rows: {len(X_train):,} | Test rows: {len(X_test):,}")

    # Sanity check: train and test should look the same
    summary = pd.DataFrame({
        "treated_share": [t_train.mean(), t_test.mean()],
        "visit_rate": [y_train.mean(), y_test.mean()],
        "uplift_pp": [
            (y_train[t_train == 1].mean() - y_train[t_train == 0].mean()) * 100,
            (y_test[t_test == 1].mean() - y_test[t_test == 0].mean()) * 100,
        ],
    }, index=["train", "test"]).round(4)
    print("\nTrain vs test check:\n", summary)

    print("\nFirst 3 rows of X_train:\n", X_train.head(3).to_string())


if __name__ == "__main__":
    main()
