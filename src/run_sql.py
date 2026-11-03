
import sqlite3
import pandas as pd
from src.config import DB_PATH, SQL_DIR

def main():
    sql_text = (SQL_DIR / "analysis.sql").read_text()
    queries = [q.strip() for q in sql_text.split(";") if q.strip()]

    with sqlite3.connect(DB_PATH) as conn:
        for i, q in enumerate(queries, 1):
            print(f"\n=== Query {i} ===")
            print(pd.read_sql(q, conn))   # yahan kya aayega?

if __name__ == "__main__":
    main()
