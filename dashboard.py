import pandas as pd
import streamlit as st

from src.simulator import generate_readings, assess_machine_health, save_readings

st.set_page_config(page_title="CNC Machine Monitor", page_icon="⚙️", layout="wide")
st.title("⚙️ CNC Machine Monitoring Simulator")
st.caption("Synthetic sensor data for demonstration and learning — not connected to real equipment.")

with st.sidebar:
    st.header("Simulation controls")
    count = st.slider("Number of readings", min_value=50, max_value=1000, value=250, step=50)
    seed = st.number_input("Random seed (repeatable results)", min_value=0, max_value=999999, value=42)
    run = st.button("Generate readings", type="primary", use_container_width=True)

if "readings" not in st.session_state or run:
    st.session_state.readings = assess_machine_health(
        generate_readings(count=int(count), seed=int(seed))
    )

df = st.session_state.readings
latest = df.iloc[-1]
normal_count = int((df["Status"] == "Normal").sum())
warning_count = int((df["Status"] == "Warning").sum())
critical_count = int((df["Status"] == "Critical").sum())

a, b, c, d = st.columns(4)
a.metric("Latest temperature", f"{latest['Temperature_C']:.1f} °C")
b.metric("Latest vibration", f"{latest['Vibration_mm_s']:.2f} mm/s")
c.metric("Spindle speed", f"{latest['Spindle_RPM']:.0f} RPM")
d.metric("Spindle load", f"{latest['Spindle_Load_pct']:.1f}%")

st.subheader("Machine health")
x, y, z = st.columns(3)
x.metric("Normal readings", normal_count)
y.metric("Warnings", warning_count)
z.metric("Critical readings", critical_count)

if latest["Status"] == "Critical":
    st.error(f"Latest reading: {latest['Alert']}")
elif latest["Status"] == "Warning":
    st.warning(f"Latest reading: {latest['Alert']}")
else:
    st.success("Latest reading is within the configured limits.")

st.subheader("Sensor trends")
chart_data = df.set_index("Timestamp")[[
    "Temperature_C", "Vibration_mm_s", "Spindle_Load_pct"
]]
st.line_chart(chart_data, height=320)

st.subheader("Alerts and recent readings")
alerts = df[df["Status"] != "Normal"].sort_values("Timestamp", ascending=False)
if alerts.empty:
    st.info("No alerts in this simulation.")
else:
    st.dataframe(alerts[["Timestamp", "Temperature_C", "Vibration_mm_s",
                         "Spindle_Load_pct", "Status", "Alert"]],
                 use_container_width=True, hide_index=True)

st.dataframe(df.tail(15).sort_values("Timestamp", ascending=False),
             use_container_width=True, hide_index=True)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download this simulation as CSV", csv,
                   file_name="cnc_machine_readings.csv", mime="text/csv")

if st.button("Append these readings to data/machine_readings.csv"):
    path = save_readings(df)
    st.success(f"Saved readings to {path}")
