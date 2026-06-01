import sqlite3
import pandas as pd
import numpy as np
import os


def estimate_rul():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, "database", "phm_data.db")

    conn = sqlite3.connect(db_path)

    df = pd.read_sql("SELECT * FROM health_index", conn)

    # ✅ Step 1: sort by time
    df = df.sort_values(by="File").reset_index(drop=True)

    # ✅ Step 2: smooth health
    df["Smoothed_HI"] = df["Health_Index"].rolling(window=5, min_periods=1).mean()

    # ✅ Step 3: normalize
    h = df["Smoothed_HI"]
    h_norm = (h - h.min()) / (h.max() - h.min() + 1e-8)  # avoid divide by zero

    # ✅ Step 4: convert to RUL
    max_life = len(df)
    rul = h_norm * max_life

    # ✅ Step 5: smooth RUL (no forced decreasing)
    rul = pd.Series(rul).rolling(window=5, min_periods=1).mean()

    df["Estimated_RUL"] = rul

    df.to_sql("rul_results", conn, if_exists="replace", index=False)

    conn.close()

    print("✅ FINAL RUL (fixed, no zeros, stable)")

    return df


if __name__ == "__main__":
    estimate_rul()