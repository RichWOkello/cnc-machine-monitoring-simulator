from pathlib import Path
import numpy as np
import pandas as pd

DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "machine_readings.csv"

def generate_readings(count: int = 100, seed: int | None = None) -> pd.DataFrame:
    """Generate realistic-looking synthetic CNC sensor readings."""
    rng = np.random.default_rng(seed)
    timestamps = pd.date_range(
        end=pd.Timestamp.now().floor("s"),
        periods=count,
        freq="s",
    )

    temperature = 48 + np.cumsum(rng.normal(0, 0.12, count))
    temperature += rng.normal(0, 1.1, count)
    vibration = np.clip(rng.normal(2.0, 0.35, count), 0.3, None)
    rpm = np.clip(rng.normal(4200, 180, count), 0, 8000)
    load = np.clip(rng.normal(62, 9, count), 0, 100)

    # Inject occasional faults so the alert system can be demonstrated.
    if count >= 20:
        for idx in rng.choice(np.arange(count), size=max(1, count // 25), replace=False):
            fault = rng.choice(["temperature", "vibration", "load"])
            if fault == "temperature":
                temperature[idx] += rng.uniform(18, 28)
            elif fault == "vibration":
                vibration[idx] += rng.uniform(3.5, 6.0)
            else:
                load[idx] = rng.uniform(96, 100)

    return pd.DataFrame({
        "Timestamp": timestamps,
        "Temperature_C": np.round(temperature, 2),
        "Vibration_mm_s": np.round(vibration, 2),
        "Spindle_RPM": np.round(rpm).astype(int),
        "Spindle_Load_pct": np.round(load, 1),
    })


def assess_machine_health(df: pd.DataFrame) -> pd.DataFrame:
    """Apply simple configurable thresholds to each sensor reading."""
    result = df.copy()
    conditions = [
        result["Temperature_C"] >= 85,
        result["Vibration_mm_s"] >= 5.5,
        result["Spindle_Load_pct"] >= 95,
        result["Temperature_C"] >= 75,
        result["Vibration_mm_s"] >= 4.0,
    ]
    labels = [
        "CRITICAL: High temperature",
        "WARNING: High vibration",
        "WARNING: High spindle load",
        "WARNING: Elevated temperature",
        "WARNING: Elevated vibration",
    ]
    result["Alert"] = np.select(conditions, labels, default="Normal")
    result["Status"] = np.where(
        result["Alert"].str.startswith("CRITICAL"),
        "Critical",
        np.where(result["Alert"].str.startswith("WARNING"), "Warning", "Normal"),
    )
    return result


def save_readings(df: pd.DataFrame, path: Path = OUTPUT_FILE) -> Path:
    """Append readings to CSV, writing headers for a new file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists() or path.stat().st_size == 0
    df.to_csv(path, mode="a", header=write_header, index=False)
    return path
