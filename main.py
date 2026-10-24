from src.simulator import generate_readings, assess_machine_health, save_readings


def main():
    print("=" * 52)
    print("       CNC MACHINE MONITORING SIMULATOR")
    print("=" * 52)

    try:
        count = int(input("Number of readings to simulate [100]: ") or "100")
        if not 1 <= count <= 10000:
            raise ValueError
    except ValueError:
        print("Please enter a whole number between 1 and 10000.")
        return

    readings = generate_readings(count=count)
    readings = assess_machine_health(readings)
    output = save_readings(readings)

    print("\nLatest readings:")
    print(readings.tail(10).to_string(index=False))
    print("\nMachine status summary:")
    print(readings["Status"].value_counts().to_string())
    print(f"\nAverage spindle temperature: {readings['Temperature_C'].mean():.1f} °C")
    print(f"Maximum vibration: {readings['Vibration_mm_s'].max():.2f} mm/s RMS")
    print(f"Average spindle load: {readings['Spindle_Load_pct'].mean():.1f}%")
    print(f"\nReadings saved to: {output.resolve()}")
    print("Run `streamlit run dashboard.py` for the interactive dashboard.")


if __name__ == "__main__":
    main()
