from src.simulator import generate_readings


def test_generate_readings():
    df = generate_readings(10, seed=42)

    assert len(df) == 10
    assert "Temperature_C" in df.columns
    assert "Vibration_mm_s" in df.columns