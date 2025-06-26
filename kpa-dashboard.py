import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="KPA Traffic Analytics Dashboard",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .header {
        color: #0d6efd;
    }
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Load sample data
@st.cache_data
def load_data():
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    traffic_data = pd.DataFrame({
        "date": dates,
        "vehicle_count": np.random.poisson(500, len(dates)) + (np.sin(np.linspace(0, 10, len(dates))) * 100).astype(int),
        "wait_time_minutes": np.random.normal(90, 30, len(dates)).clip(10, 300),
        "gate": np.random.choice(["Gate 12", "Gate 9", "Gate 15", "Gate 24"], len(dates), p=[0.35, 0.25, 0.2, 0.2]),
        "cargo_type": np.random.choice(["Containerized", "Bulk", "Refrigerated", "Breakbulk"], len(dates), p=[0.5, 0.2, 0.15, 0.15]),
        "issue_type": np.random.choice(["Clearance Delays", "Slow Processing", "Too Many Trucks", "Security Checks"], len(dates), p=[0.4, 0.3, 0.2, 0.1]),
        "department": np.random.choice(["Operations", "Security", "Logistics", "Customs"], len(dates))
    })

    traffic_data['hour'] = np.random.choice(range(6, 21), len(dates))
    return traffic_data

df = load_data()

# Dashboard Header
st.title("🚢 KPA Port Traffic Analytics Dashboard")
st.markdown("""
<div class="card">
    <h3 class="header">Port Operations Performance Monitoring</h3>
    <p>Comprehensive analysis of traffic patterns, congestion causes, and operational efficiency at KPA gates</p>
</div>
""", unsafe_allow_html=True)

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Average Daily Vehicles", f"{int(df['vehicle_count'].mean()):,}", "5% vs target")
with col2:
    st.metric("Average Wait Time", f"{int(df['wait_time_minutes'].mean())} min", "12% ▲")
with col3:
    st.metric("Peak Hour Congestion", "60%", "8% ▲")
with col4:
    st.metric("Gate 12 Utilization", "35%", "10% ▲")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Traffic Patterns", "Congestion Analysis", "Operational Efficiency", "Policy Recommendations"])

with tab1:
    st.header("Traffic Volume and Patterns")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Daily Vehicle Volume Trend")
        st.line_chart(df.groupby('date')['vehicle_count'].sum())
    
    with col2:
        st.subheader("Gate Utilization Distribution")
        gate_dist = df['gate'].value_counts().reset_index()
        gate_dist.columns = ['Gate', 'Count']
        gate_dist['Percentage'] = (gate_dist['Count'] / gate_dist['Count'].sum() * 100).round(1)
        st.dataframe(gate_dist[['Gate', 'Percentage']].set_index('Gate'))
        st.bar_chart(gate_dist.set_index('Gate')['Count'])

    st.markdown("""
    <div class="card">
        <h4>Key Observations:</h4>
        <ul>
            <li>Gate 12 handles 35% of all traffic, creating bottlenecks</li>
            <li>Peak congestion occurs between 10AM-2PM daily</li>
            <li>Containerized cargo accounts for 50% of all traffic</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.header("Congestion Cause Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Primary Causes of Congestion")
        issue_dist = df['issue_type'].value_counts()
        st.bar_chart(issue_dist)
    
    with col2:
        st.subheader("Wait Time Distribution by Gate")
        wait_stats = df.groupby('gate')['wait_time_minutes'].agg(['mean', 'median', 'std']).reset_index()
        st.dataframe(wait_stats.style.format({'mean': '{:.1f}', 'median': '{:.1f}', 'std': '{:.1f}'}))

    # Calculations
    clearance_pct = df['issue_type'].value_counts(normalize=True).get("Clearance Delays", 0) * 100
    gate12_wait = df[df["gate"] == "Gate 12"]["wait_time_minutes"].mean()
    other_gates_wait = df[df["gate"] != "Gate 12"]["wait_time_minutes"].mean()
    afternoon_congestion_pct = len(df[df["hour"].between(12, 17)]) / len(df) * 100

    st.markdown(f"""
    <div class="card">
        <h4>Root Cause Analysis:</h4>
        <ul>
            <li>{clearance_pct:.1f}% of delays caused by clearance processing</li>
            <li>Gate 12 has {((gate12_wait - other_gates_wait) / other_gates_wait) * 100:.1f}% longer wait times than other gates</li>
            <li>Afternoon hours account for {afternoon_congestion_pct:.1f}% of congestion incidents</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.header("Operational Efficiency Metrics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Average Processing Time by Department")
        dept_efficiency = df.groupby('department')['wait_time_minutes'].mean()
        st.bar_chart(dept_efficiency)
    
    with col2:
        st.subheader("Wait Time by Cargo Type")
        cargo_wait = df.groupby('cargo_type')['wait_time_minutes'].mean()
        st.bar_chart(cargo_wait)

    # Efficiency Findings
    container_wait = df[df["cargo_type"] == "Containerized"]["wait_time_minutes"].mean()
    bulk_wait = df[df["cargo_type"] == "Bulk"]["wait_time_minutes"].mean()
    customs_wait = df[df["department"] == "Customs"]["wait_time_minutes"].sum()
    total_wait = df["wait_time_minutes"].sum()
    customs_share = (customs_wait / total_wait) * 100

    st.markdown(f"""
    <div class="card">
        <h4>Efficiency Findings:</h4>
        <ul>
            <li>67.7% of staff report excessive overtime due to processing delays</li>
            <li>Containerized cargo is processed {(bulk_wait - container_wait) / bulk_wait * 100:.0f}% faster than bulk cargo</li>
            <li>Customs processing accounts for {customs_share:.1f}% of total wait time</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.header("Policy Recommendations")

    st.subheader("Immediate Actions (0–3 months)")
    st.markdown("""
- ✅ Implement **Electronic Truck Appointment System (ETAS)**
- 👥 Reallocate staff during **peak hours (10AM–2PM)**
- 🚛 Launch pilot **RFID clearance** for frequent shippers
    """)

    st.subheader("Medium-Term Solutions (3–12 months)")
    st.markdown("""
- 🧾 **Digitize 100%** of documentation processes
- 🏗️ Expand **Gate 24** capacity to handle 25% of total traffic
- 🔐 Implement **unified customs-security clearance** platform
    """)

    st.subheader("Long-Term Infrastructure (1–3 years)")
    st.markdown("""
- 🏭 Build **inland clearance depots** to reduce port congestion
- 🤖 Automate **80% of inspection processes** with AI/ML
- 🚦 Develop **dedicated cargo corridors** with smart traffic control
    """)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center;">
    <p>KPA Port Analytics • Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
</div>
""", unsafe_allow_html=True)
