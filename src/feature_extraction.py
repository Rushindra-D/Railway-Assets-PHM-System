import os
import numpy as np
import pandas as pd
import sqlite3
from scipy.stats import kurtosis, skew

def extract_features_from_signal(signal):
    """
    Extracts 9 key statistical fingerprints from a vibration signal.
    These are the 'features' that represent the health of the railway asset.
    """
    mean = np.mean(signal)
    std = np.std(signal)
    variance = np.var(signal)
    rms = np.sqrt(np.mean(signal ** 2))
    peak = np.max(np.abs(signal))
    peak_to_peak = np.max(signal) - np.min(signal)
    crest_factor = peak / rms if rms != 0 else 0
    
    # Kurtosis is the most important for early-stage crack detection
    kur = kurtosis(signal) 
    skw = skew(signal)

    return {
        "Mean": mean,
        "Std": std,
        "Variance": variance,
        "RMS": rms,
        "Kurtosis": kur,
        "Skewness": skw,
        "Peak": peak,
        "Peak_to_Peak": peak_to_peak,
        "Crest_Factor": crest_factor
    }

def process_dataset(dataset_path, limit=700):
    """
    Processes the first 700 files to simulate 'No Run-to-Failure' monitoring.
    """
    # 1. Get and sort the files numerically/alphabetically
    files = sorted(
        [f for f in os.listdir(dataset_path) if os.path.isfile(os.path.join(dataset_path, f))]
    )
    
    # Apply your 700-file constraint
    files_to_process = files[:limit]
    all_features = []

    print(f"🚀 Starting Extraction on {len(files_to_process)} files...")

    for file in files_to_process:
        file_path = os.path.join(dataset_path, file)

        try:
            # NASA Bearing dataset usually has 4 columns; we use the first sensor (Channel 1)
            data = np.loadtxt(file_path)
            signal = data[:, 0] if len(data.shape) > 1 else data

            # Extract physics-based features
            features = extract_features_from_signal(signal)
            features["File"] = file # Keep track of the timestamp/filename

            all_features.append(features)

        except Exception as e:
            print(f"❌ Error reading {file}: {e}")

    # 2. Convert to DataFrame
    df = pd.DataFrame(all_features)

    # 3. Store in Database (Crucial for the PHM Pipeline)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(BASE_DIR, "database")
    os.makedirs(db_dir, exist_ok=True) # Create folder if it doesn't exist
    
    db_path = os.path.join(db_dir, "phm_data.db")
    conn = sqlite3.connect(db_path)
    
    # We use 'replace' here because this is the first step of the project
    df.to_sql("extracted_features", conn, if_exists="replace", index=False)
    conn.close()

    # 4. Save CSV for your Excel/Report analysis
    output_dir = os.path.join(BASE_DIR, "outputs")
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(os.path.join(output_dir, "extracted_features.csv"), index=False)

    print(f"✅ Feature Extraction Completed. {len(df)} rows stored in DB.")
    return df

if __name__ == "__main__":
    # Path setup
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Ensure this path matches where your NASA dataset is stored
    dataset_path = os.path.join(BASE_DIR, "data", "Bearing dataset")

    process_dataset(dataset_path)