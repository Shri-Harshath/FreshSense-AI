import os
import joblib
import numpy as np
import pandas as pd
from train_model import train

def test_ml_pipeline():
    print("[*] Testing ML model loading...")
    if not os.path.exists("freshness_model.pkl"):
        print("    [!] freshness_model.pkl not found, training on-the-fly...")
        train()
    model = joblib.load("freshness_model.pkl")
    print("    [+] Model successfully loaded.")
    
    features = ["temperature_c", "humidity_pct", "gas_ppm", "hours_elapsed"]
    
    # Test case 1: Fresh food (low temp, low gas, low hours)
    fresh_sample = pd.DataFrame([[4.0, 50.0, 30.0, 2.0]], columns=features)
    score_fresh = float(model.predict(fresh_sample)[0])
    print(f"    [+] Fresh sample score: {score_fresh:.2f}/100 (Expected: > 70)")
    assert score_fresh > 60, f"Expected fresh score > 60, got {score_fresh}"

    # Test case 2: Spoiled food (high temp, high gas, high hours)
    spoiled_sample = pd.DataFrame([[35.0, 85.0, 450.0, 48.0]], columns=features)
    score_spoiled = float(model.predict(spoiled_sample)[0])
    print(f"    [+] Spoiled sample score: {score_spoiled:.2f}/100 (Expected: < 40)")
    assert score_spoiled < 50, f"Expected spoiled score < 50, got {score_spoiled}"

    print("[SUCCESS] All ML inference tests passed successfully!")

if __name__ == "__main__":
    test_ml_pipeline()
