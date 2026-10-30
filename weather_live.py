"""Optional live 10-day environmental forecast from Open-Meteo (free, no API key).

Returns the same four variables the model was trained on, as daily values:
temperature (°C, mean), humidity (%, mean), rainfall (mm/day, total), wind speed (m/s, mean).
If the request fails (offline, blocked network), the app falls back to typical conditions.
"""
from __future__ import annotations

import pandas as pd
import requests

URL = "https://api.open-meteo.com/v1/forecast"

CITIES = {
    "Johor Bahru": (1.4655, 103.7578),
    "Alor Setar": (6.1248, 100.3678),
    "Kota Bharu": (6.1399, 102.2422),
    "Bandaraya Melaka": (2.1960, 102.2405),
    "Seremban": (2.7297, 101.9381),
    "Kuantan": (3.7634, 103.2202),
    "Ipoh": (4.5841, 101.0829),
    "Kangar": (6.4455, 100.2002),
    "George Town": (5.4112, 100.3354),
    "Kota Kinabalu": (5.9804, 116.0735),
    "Kuching": (1.5531, 110.3450),
    "Shah Alam": (3.0733, 101.5185),
    "Kuala Terengganu": (5.3302, 103.1408),
    "Kuala Lumpur": (3.1409, 101.6932),
    "Putrajaya": (2.9264, 101.6964),
    "Labuan": (5.2852, 115.2478),
}

def fetch_daily_conditions(lat: float, lon: float, days: int = 10, timeout: int = 6) -> pd.DataFrame:
    params = {
        "latitude": lat, "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "wind_speed_unit": "ms", "timezone": "Asia/Kuala_Lumpur", "forecast_days": days,
    }
    r = requests.get(URL, params=params, timeout=timeout)
    r.raise_for_status()
    h = pd.DataFrame(r.json()["hourly"])
    h["date"] = pd.to_datetime(h["time"]).dt.normalize()
    daily = h.groupby("date").agg(
        temperature_C=("temperature_2m", "mean"),
        humidity_pct=("relative_humidity_2m", "mean"),
        rainfall_mm_per_day=("precipitation", "sum"),
        wind_speed_m_s=("wind_speed_10m", "mean"),
    ).reset_index()
    return daily.head(days)