import pandas as pd
import sqlite3
import os
import joblib
from sklearn.preprocessing import MinMaxScaler

def normalize_features(baseline_limit=100):
    """
    Normalizes features based on a 'Healthy Baseline'.
    baseline_limit: The number of initial files assumed to be 100% healthy.
    """
    # 1. Path Setup
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, "database", "phm_data.db")
    model_dir = os.path.join(BASE_DIR, "models")
    os.makedirs(model_dir, exist_ok=True)

    # 2. Load Data from SQLite
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM extracted_features", conn)
    except Exception as e:
        print(f"❌ Error: Could not find extracted_features table. Run feature_extraction.py first. {e}")
        return None

    # Separate metadata (File names) from the actual numerical data
    file_names = df["File"]
    features = df.drop(columns=["File"])

    # 3. Baseline-Driven Scaling
    # We fit the scaler ONLY on the first 100 files (The Healthy State)
    scaler = MinMaxScaler()
    
    # Safety check if we have enough data for the baseline
    actual_baseline = min(baseline_limit, len(features))
    scaler.fit(features.iloc[:actual_baseline])

    # 4. Save the Scaler (For Real-Time use later)
    scaler_path = os.path.join(model_dir, "scaler.pkl")
    joblib.dump(scaler, scaler_path)

    # 5. Transform all data (all 700 files) using that healthy baseline
    scaled_values = scaler.transform(features)
    normalized_df = pd.DataFrame(scaled_values, columns=features.columns)
    normalized_df["File"] = file_names

    # 6. Store back in DB for the Anomaly Detection step
    normalized_df.to_sql("normalized_features", conn, if_exists="replace", index=False)
    conn.close()

    # Save a CSV for your report
    output_path = os.path.join(BASE_DIR, "outputs", "normalized_features.csv")
    normalized_df.to_csv(output_path, index=False)

    print(f"✅ Normalization Complete. Scaler fitted on first {actual_baseline} files.")
    print(f"💾 Scaler saved to {scaler_path}")
    
    return normalized_df

if __name__ == "__main__":
    normalize_features()