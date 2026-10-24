# CNC Machine Monitoring Simulator

A small Python project that simulates CNC milling machine sensor readings, flags abnormal conditions, and displays a monitoring dashboard.

> **Important:** This project uses synthetic data. It is an educational simulator, not a safety system and not connected to a physical CNC machine.

## Features

- Simulated spindle temperature, vibration, RPM, and load
- Rule-based warning and critical alerts
- CSV export and local data persistence
- Interactive Streamlit dashboard with sensor trends
- Repeatable simulations using a random seed

## Project structure

```text
cnc-machine-monitoring-simulator/
├── main.py
├── dashboard.py
├── requirements.txt
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   └── simulator.py
└── data/
```

## Requirements

- Python 3.10 or newer
- pip

## Run locally in VS Code

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the command-line simulator

```bash
python main.py
```

### 4. Run the dashboard

```bash
streamlit run dashboard.py
```

Streamlit will open the dashboard in your browser.

## Initial alert thresholds

| Sensor | Normal | Warning | Critical |
|---|---:|---:|---:|
| Spindle temperature | Below 75 °C | 75–84.9 °C | 85 °C or higher |
| Vibration | Below 4.0 mm/s | 4.0–5.49 mm/s | 5.5 mm/s or higher |
| Spindle load | Below 95% | 95% or higher | No separate critical threshold |

These are illustrative thresholds for the demo only. Real thresholds depend on machine specifications, sensor placement, operating conditions, and manufacturer guidance.

## Example workflow

1. Generate synthetic sensor readings.
2. Apply threshold-based health checks.
3. Review warning and critical events.
4. Explore trends in the dashboard.
5. Download the data as CSV for further analysis.

## Ideas for version 2

- Configurable thresholds in a settings file
- Moving-average trend detection
- Machine downtime and fault-duration metrics
- Automated PDF shift report
- Unit tests and continuous integration
- Optional connection to real sensor data through a clearly defined interface

## License

MIT 
