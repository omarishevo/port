import streamlit as st
import numpy as np
from datetime import datetime, timedelta

# --- Page Config ---
st.set_page_config(
    page_title="KPA Traffic Dashboard (Lightweight)",
    page_icon="🚢",
    layout="wide"
)

# --- Generate Data (No Pandas) ---
def generate_data():
    dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(365)]
    vehicle_counts = np.random.poisson(500, 365) + (np.sin(np.linspace(0, 10, 365)) * 100).astype(int)
    wait_times = np.clip(np.random.normal(90, 30, 365), 10, 300)
    gates = np.random.choice(["Gate 12", "Gate 9", "Gate 15", "Gate 24"], 365)
    cargo_types = np.random.choice(["Containerized", "Bulk", "Refrigerated", "Breakbulk"], 365)
    
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
    st.line_chart({"Vehicles": data["vehicle_count"]})  # Streamlit built-in
    
    st.subheader("Cargo Type Distribution")
    cargo_counts = {cargo: list(data["cargo_type"]).count(cargo) for cargo in set(data["cargo_type"])}
    st.bar_chart(cargo_counts)

with tab2:
    st.subheader("Wait Time by Gate")
    gate_data = {
        "Gate 12": [t for g, t in zip(data["gate"], data["wait_time_minutes"]) if g == "Gate 12"],
        "Gate 9": [t for g, t in zip(data["gate"], data["wait_time_minutes"]) if g == "Gate 9"],
    }
    st.bar_chart({
        "Avg Wait Time (Gate 12)": np.mean(gate_data["Gate 12"]),
        "Avg Wait Time (Gate 9)": np.mean(gate_data["Gate 9"]),
    })

# --- Footer ---
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
