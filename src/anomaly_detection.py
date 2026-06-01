import sqlite3
import pandas as pd
import os
import joblib
from sklearn.ensemble import IsolationForest

def compute_health_index(baseline_limit=100):
    """
    Trains an Isolation Forest on the healthy baseline and scores all 700 files.
    Higher Score = Healthy | Lower Score = Anomaly
    """
    # 1. Path Setup
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, "database", "phm_data.db")
    model_dir = os.path.join(BASE_DIR, "models")
    os.makedirs(model_dir, exist_ok=True)

    # 2. Load Normalized Data
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM normalized_features", conn)
    except Exception as e:
        print(f"❌ Error: Normalized features not found. Run normalization.py first. {e}")
        return None

    file_names = df["File"]
    features = df.drop(columns=["File"])

    # 3. Train Isolation Forest (The "Health Detector")
    # We fit the model ONLY on the first 100 'Healthy' files.
    # contamination='auto' lets the model decide the outlier threshold.
    model = IsolationForest(n_estimators=100, contamination='auto', random_state=42)
    
    actual_baseline = min(baseline_limit, len(features))
    model.fit(features.iloc[:actual_baseline])

    # 4. Save the Model
    model_path = os.path.join(model_dir, "anomaly_model.pkl")
    joblib.dump(model, model_path)

    # 5. Generate Anomaly Scores
    # decision_function returns scores where higher is 'more normal'
    raw_scores = model.decision_function(features)

    # 6. Convert to Health Index (0.0 to 1.0)
    # We want 1.0 to represent 'Perfect Baseline Health'
    min_s = raw_scores.min()
    max_s = raw_scores.max()
    
    # Mathematical scaling to 0-1 range
    health_index = (raw_scores - min_s) / (max_s - min_s)
    
    # Clip to ensure no values are mathematically impossible
    health_index = health_index.clip(0, 1)

    # 7. Store Results
    results = pd.DataFrame({
        "File": file_names,
        "Anomaly_Score": raw_scores,
        "Health_Index": health_index
    })

    results.to_sql("health_index", conn, if_exists="replace", index=False)
    conn.close()

    # Save CSV for the final report
    output_path = os.path.join(BASE_DIR, "outputs", "health_index.csv")
    results.to_csv(output_path, index=False)

    print(f"✅ Anomaly Detection Complete. Model trained on {actual_baseline} healthy files.")
    print(f"💾 Anomaly Model saved to {model_path}")
    
    return results

if __name__ == "__main__":
    compute_health_index()