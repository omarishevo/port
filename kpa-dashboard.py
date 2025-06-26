import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import random

# --- Page Config ---
st.set_page_config(
    page_title="KPA Traffic Dashboard (Lightweight)",
    page_icon="🚢",
    layout="wide"
)

# --- Generate Data ---
def generate_data():
    dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(365)]
    vehicle_counts = [random.randint(400, 600) + int(50 * np.sin(i/10)) for i in range(365)]
    wait_times = [max(10, min(300, int(random.gauss(90, 30)))) for _ in range(365)]
    gates = random.choices(["Gate 12", "Gate 9", "Gate 15", "Gate 24"], k=365)
    cargo_types = random.choices(["Containerized", "Bulk", "Refrigerated", "Breakbulk"], k=365)
    
    return {
        "date": dates,
        "vehicle_count": vehicle_counts,
        "wait_time_minutes": wait_times,
        "gate": gates,
        "cargo_type": cargo_types
    }

data = generate_data()

# --- Dashboard UI ---
st.title("🚢 KPA Port Traffic Analytics")
st.markdown("""
<div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <h3 style="color: #0d6efd;">Port Operations Performance Monitoring</h3>
    <p>Simplified analytics using Streamlit-native features</p>
</div>
""", unsafe_allow_html=True)

# --- Key Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Avg Vehicles/Day", f"{int(np.mean(data['vehicle_count'])):,}")
col2.metric("Avg Wait Time", f"{int(np.mean(data['wait_time_minutes']))} mins")
col3.metric("Busiest Gate", "Gate 12", "35% of traffic")

# --- Tabs ---
tab1, tab2 = st.tabs(["Traffic Trends", "Gate Analysis"])

with tab1:
    st.subheader("Daily Vehicle Count")
    st.line_chart(data["vehicle_count"])  # This works because it's a list

    st.subheader("Cargo Type Distribution")
    # Count each cargo type
    cargo_counts = {
        cargo: data["cargo_type"].count(cargo) 
        for cargo in set(data["cargo_type"])
    }

    # Convert to 2D format for st.bar_chart
    cargo_labels = list(cargo_counts.keys())
    cargo_values = list(cargo_counts.values())
    cargo_chart_data = {"Cargo Type": cargo_labels, "Count": cargo_values}
    st.write("### Cargo Volumes")
    st.bar_chart(data={"Count": cargo_values})  # shows chart
    # Manually show labels
    for label, value in zip(cargo_labels, cargo_values):
        st.write(f"- {label}: {value}")

with tab2:
    st.subheader("Wait Time by Gate")
    # Calculate average wait per gate
    gate_wait_times = {}
    for gate in set(data["gate"]):
        total_wait = 0
        count = 0
        for g, wait in zip(data["gate"], data["wait_time_minutes"]):
            if g == gate:
                total_wait += wait
                count += 1
        avg_wait = total_wait / count if count > 0 else 0
        gate_wait_times[gate] = avg_wait

    # Convert to chart-compatible structure
    gate_labels = list(gate_wait_times.keys())
    gate_values = list(gate_wait_times.values())
    st.write("### Average Wait Times by Gate")
    st.bar_chart(data={"Avg Wait (mins)": gate_values})  # chart
    for label, value in zip(gate_labels, gate_values):
        st.write(f"- {label}: {value:.1f} mins")

# --- Footer ---
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
