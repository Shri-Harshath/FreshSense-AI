"""
FreshSense AI - Synthetic Food Spoilage Telemetry Generator
===========================================================
Simulates 1,200 realistic IoT sensor cycles of food decay over a 72-hour window.
Generates environmental telemetry including:
  - Temperature (°C)
  - Relative Humidity (%)
  - Volatile Gas Concentration (MQ-135 VOCs / Ammonia / Amines in ppm)
  - Elapsed Storage Time (0 to 72 hours)
  - Freshness Score (0.0 = completely spoiled to 100.0 = peak freshness)
"""

import os
import numpy as np
import pandas as pd


def generate_spoilage_data(n_samples: int = 1200, random_seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic sensor telemetry simulating food decay over 72 hours.

    Parameters:
        n_samples (int): Total number of sensor cycles to simulate (default: 1200).
        random_seed (int): Seed for pseudo-random number generator for reproducibility.

    Returns:
        pd.DataFrame: DataFrame containing 1,200 sensor cycles:
            - temperature_c: Ambient temperature in Celsius (1.0 to 38.0 °C)
            - humidity_pct: Relative humidity percentage (30.0% to 95.0%)
            - gas_ppm: Gas concentration in ppm representing VOCs/amines/NH3 (12 to 650 ppm)
            - hours_elapsed: Time food has been monitored (0.0 to 72.0 hours)
            - freshness_score: Food freshness index (0.0 to 100.0)
    """
    np.random.seed(random_seed)

    # 1. Simulate Elapsed Monitoring Time (0.0 to 72.0 hours)
    hours_elapsed = np.random.uniform(0.0, 72.0, size=n_samples)

    # 2. Simulate Multi-Regime Storage Temperatures (°C)
    # Different storage environments:
    #   - Refrigerated / Cold Chain (1 - 6 °C): ~30%
    #   - Cool / Pantry Storage (8 - 17 °C): ~25%
    #   - Ambient Room Temperature (18 - 26 °C): ~30%
    #   - Warm / Heat Stress Conditions (27 - 38 °C): ~15%
    temp_regimes = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.30, 0.25, 0.30, 0.15])
    temperature_c = np.zeros(n_samples)

    temperature_c[temp_regimes == 0] = np.random.normal(loc=4.0, scale=1.2, size=(temp_regimes == 0).sum())
    temperature_c[temp_regimes == 1] = np.random.normal(loc=13.5, scale=2.2, size=(temp_regimes == 1).sum())
    temperature_c[temp_regimes == 2] = np.random.normal(loc=22.5, scale=2.0, size=(temp_regimes == 2).sum())
    temperature_c[temp_regimes == 3] = np.random.normal(loc=32.0, scale=2.6, size=(temp_regimes == 3).sum())
    temperature_c = np.clip(temperature_c, 1.0, 38.0)

    # 3. Simulate Relative Humidity (%)
    # Base humidity distribution covering dry (30%) to tropical/humid (95%)
    humidity_pct = np.random.normal(loc=65.0, scale=14.0, size=n_samples)
    humidity_pct = np.clip(humidity_pct, 30.0, 95.0)

    # 4. Spoilage Kinetics & Biological Freshness Decay
    # Arrhenius temperature acceleration: reaction/microbial rate scales exponentially with temp
    temp_factor = np.exp(0.072 * (temperature_c - 4.0))

    # Moisture acceleration: high humidity (>70%) promotes rapid bacterial/fungal proliferation
    humidity_factor = 0.52 + 0.58 * ((humidity_pct / 100.0) ** 1.85)

    # Effective spoilage exposure hours
    effective_hours = hours_elapsed * temp_factor * humidity_factor

    # Sigmoidal biological decay curve with lag phase, exponential decay, and saturation
    decay_steepness = 2.25
    decay_halflife = 38.0
    base_freshness = 100.0 / (1.0 + (effective_hours / decay_halflife) ** decay_steepness)

    # Natural biological variation and measurement noise
    freshness_noise = np.random.normal(0, 2.2, size=n_samples)
    freshness_score = np.clip(base_freshness + freshness_noise, 0.0, 100.0)

    # 5. MQ-135 Gas Sensor Telemetry (ppm)
    # Pristine baseline (VOCs/Ethanol/Ammonia): ~18 to 35 ppm
    # Decomposing / spoiled release: rises up to 600+ ppm
    spoilage_ratio = (100.0 - freshness_score) / 100.0
    base_gas = 22.0 + 490.0 * (spoilage_ratio ** 1.85)

    # Higher temperatures increase VOC vapor pressure / volatile emission
    temp_evaporation = 1.0 + 0.016 * (temperature_c - 4.0)

    # Hardware noise & sensor drift (±7 ppm)
    gas_noise = np.random.normal(0, 7.5, size=n_samples)
    gas_ppm = np.clip(base_gas * temp_evaporation + gas_noise, 12.0, 650.0)

    # 6. Assemble DataFrame
    df = pd.DataFrame({
        "temperature_c": np.round(temperature_c, 2),
        "humidity_pct": np.round(humidity_pct, 2),
        "gas_ppm": np.round(gas_ppm, 2),
        "hours_elapsed": np.round(hours_elapsed, 2),
        "freshness_score": np.round(freshness_score, 2),
    })

    return df


def main():
    output_filename = "spoilage_data.csv"
    sample_count = 1200

    print("=" * 65)
    print("FreshSense AI - Synthetic Food Decay Telemetry Generator")
    print("=" * 65)
    print(f"[*] Simulating {sample_count:,} sensor cycles over 72-hour decay window...")

    df = generate_spoilage_data(n_samples=sample_count, random_seed=42)
    df.to_csv(output_filename, index=False)

    print(f"[+] Successfully generated and saved dataset to '{output_filename}'")
    print(f"[+] Total records: {len(df):,} rows x {len(df.columns)} columns")
    print(f"[+] Sensor telemetry features: {list(df.columns)}")

    print("\n" + "-" * 40 + " Telemetry Statistics " + "-" * 40)
    print(df.describe().round(2).to_string())

    print("\n" + "-" * 40 + " First 5 Sensor Cycles " + "-" * 40)
    print(df.head().to_string())

    print("\n" + "-" * 40 + " Feature Correlations with Freshness " + "-" * 40)
    correlations = df.corr()["freshness_score"].sort_values(ascending=False)
    for feature, corr in correlations.items():
        print(f"  {feature:<18}: {corr:>+.4f}")
    print("=" * 65)


if __name__ == "__main__":
    main()
