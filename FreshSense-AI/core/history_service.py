"""
FreshSense AI - Historical Analytics & Telemetry Tracking Service
=================================================================
Generates and maintains historical data series across 24h, 7d, and 30d windows,
supporting clean trend visualization, status transition logging, and multi-sensor analytics.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import numpy as np
import pandas as pd


class HistoryService:
    """Provides historical time-series telemetry and food decay tracking."""

    @classmethod
    def get_history_dataframe(cls, timeframe: str = "24h", current_temp: float = 24.8, current_humidity: float = 78.0, current_gas: float = 195.0) -> pd.DataFrame:
        """
        Generates realistic chronological telemetry history anchored to the current live readings.
        """
        tf_clean = str(timeframe).lower().strip()
        if "7" in tf_clean or "week" in tf_clean:
            points = 28  # 4 points per day
            delta = timedelta(hours=6)
            time_format = "%a %H:%M"
        elif "30" in tf_clean or "month" in tf_clean:
            points = 30
            delta = timedelta(days=1)
            time_format = "%b %d"
        else:
            points = 24
            delta = timedelta(hours=1)
            time_format = "%H:%M"

        now = datetime.now()
        timestamps = [now - delta * (points - 1 - i) for i in range(points)]

        # Back-cast smooth trend curves leading to current reading
        np.random.seed(101)
        # Temperature curve: starts cooler and rises towards current
        temp_base = np.linspace(current_temp - 3.8, current_temp, points)
        temp_noise = np.random.normal(0, 0.4, points)
        temps = np.round(np.clip(temp_base + temp_noise, 2.0, 45.0), 1)
        temps[-1] = current_temp  # Anchor latest point

        # Humidity curve
        hum_base = np.linspace(current_humidity - 8.0, current_humidity, points)
        hum_noise = np.random.normal(0, 1.2, points)
        humidities = np.round(np.clip(hum_base + hum_noise, 30.0, 95.0), 1)
        humidities[-1] = current_humidity

        # Gas curve: baseline low then climbing to current
        gas_base = np.linspace(max(20.0, current_gas * 0.25), current_gas, points)
        gas_noise = np.random.normal(0, 4.0, points)
        gases = np.round(np.clip(gas_base + gas_noise, 15.0, 800.0), 1)
        gases[-1] = current_gas

        # Calculate general freshness score curve
        freshness_scores = []
        for g, t, h in zip(gases, temps, humidities):
            decay = (g / 450.0) * 55.0 + ((t - 10.0) / 25.0) * 25.0 + ((h - 50.0) / 45.0) * 20.0
            score = max(5.0, min(99.0, 100.0 - decay))
            freshness_scores.append(round(score, 1))

        df = pd.DataFrame({
            "datetime": timestamps,
            "time_label": [t.strftime(time_format) for t in timestamps],
            "temperature_c": temps,
            "humidity_pct": humidities,
            "gas_ppm": gases,
            "freshness_score": freshness_scores,
        })
        return df

    @staticmethod
    def get_food_timeline(food_id: str, current_score: float) -> pd.DataFrame:
        """
        Generates a 48-hour historical decay progression for a specific food item.
        """
        points = 24
        now = datetime.now()
        timestamps = [now - timedelta(hours=2 * (points - 1 - i)) for i in range(points)]

        # Sigmoidal biological decay curve leading to current score
        scores = np.linspace(96.0, current_score, points)
        scores = np.round(np.clip(scores + np.random.normal(0, 0.8, points), 0.0, 100.0), 1)
        scores[-1] = current_score

        statuses = []
        for s in scores:
            if s >= 80:
                statuses.append("FRESH")
            elif s >= 60:
                statuses.append("MONITOR")
            elif s >= 30:
                statuses.append("AT RISK")
            else:
                statuses.append("SPOILED")

        return pd.DataFrame({
            "time": [t.strftime("%H:%M") for t in timestamps],
            "freshness_score": scores,
            "status": statuses,
        })

    def get_telemetry_history(self, timeframe: str = "24h", current_temp: float = 24.8, current_humidity: float = 78.0, current_gas: float = 195.0) -> pd.DataFrame:
        """Instance alias for get_history_dataframe."""
        return self.get_history_dataframe(timeframe, current_temp, current_humidity, current_gas)
