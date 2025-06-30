import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="KPA Stakeholder Analytics Dashboard",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Styling ---
st.markdown("""
<style>
    .header { color: #0d6efd; }
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    dates = pd.date_range(start="2023-01-01", end="2023-12-31")
    return pd.DataFrame({
        "date": dates,
        "vehicle_count": np.random.poisson(500, len(dates)) + (np.sin(np.linspace(0, 10, len(dates))) * 100).astype(int),
        "wait_time_minutes": np.random.normal(90, 30, len(dates)).clip(10, 360),
        "gate": np.random.choice(["Gate 12", "Gate 9", "Gate 15", "Gate 24"], len(dates), p=[0.35, 0.25, 0.2, 0.2]),
        "issue_type": np.random.choice(["Clearance Delays", "Slow Processing", "Too Many Trucks", "Security Checks"], len(dates), p=[0.4, 0.3, 0.2, 0.1]),
        "department": np.random.choice(["Operations", "Security", "Logistics", "Customs"], len(dates)),
        "hour": np.random.choice(range(6, 21), len(dates))
    })

df = load_data()

# --- Dashboard Layout ---
st.title("🚢 KPA Stakeholder Traffic Analytics Dashboard")

# --- Header Section ---
st.markdown("""
<div class="card">
<h3 class="header">General Objectives</h3>
<ul>
    <li><strong>Traffic Volume & Pattern:</strong> Analyze gate load and peak hours to optimize flow</li>
    <li><strong>Congestion Causes:</strong> Identify and mitigate systemic bottlenecks</li>
    <li><strong>Operational Efficiency:</strong> Benchmark resource use and streamline processing</li>
    <li><strong>Policy Strategy:</strong> Implement data-driven reforms for short and long-term gains</li>
</ul>
</div>
""", unsafe_allow_html=True)

# --- Key Metrics ---
cols = st.columns(4)
with cols[0]:
    st.metric("Avg Daily Vehicles", f"{int(df['vehicle_count'].mean()):,}", "5% above target")
with cols[1]:
    st.metric("Avg Wait Time", f"{int(df['wait_time_minutes'].mean())} mins", "12% longer than benchmark")
with cols[2]:
    st.metric("Peak Hour Congestion", "60%", "10AM–2PM daily")
with cols[3]:
    st.metric("Gate 12 Load", "35%", "Primary bottleneck")

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🚦 Traffic Patterns", 
    "⚠️ Congestion Analysis", 
    "⚙️ Operational Efficiency", 
    "📜 Policy Recommendations"
])

# --- Tab 1: Traffic Patterns ---
with tab1:
    st.header("Traffic Volume and Pattern Assessment")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Vehicle Count Over Time")
        st.line_chart(df.groupby("date")["vehicle_count"].sum())
    with col2:
        st.subheader("Gate Utilization (%)")
        gate_counts = df["gate"].value_counts(normalize=True) * 100
        gate_df = pd.DataFrame({"Gate": gate_counts.index, "Utilization": gate_counts.values}).set_index("Gate")
        st.bar_chart(gate_df)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Hourly Traffic Distribution")
        hour_counts = df["hour"].value_counts().sort_index()
        hour_df = pd.DataFrame({"Hour": hour_counts.index, "Count": hour_counts.values}).set_index("Hour")
        st.bar_chart(hour_df)

# --- Tab 2: Congestion Analysis ---
with tab2:
    st.header("Congestion Cause Identification")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Delay Causes Distribution")
        issue_dist = df["issue_type"].value_counts(normalize=True) * 100
        issue_df = pd.DataFrame({"Issue": issue_dist.index, "Percent": issue_dist.values}).set_index("Issue")
        st.bar_chart(issue_df)

    with col2:
        st.subheader("Wait Time Ranges")
        bins = [0, 30, 60, 120, 240, 360]
        labels = ["0–30", "31–60", "61–120", "121–240", "241–360"]
        wait_ranges = pd.cut(df["wait_time_minutes"], bins=bins, labels=labels, include_lowest=True)
        wait_range_counts = wait_ranges.value_counts().sort_index()
        wait_range_df = pd.DataFrame({
            "Range": [str(label) for label in wait_range_counts.index],
            "Count": wait_range_counts.values
        }).set_index("Range")
        st.bar_chart(wait_range_df)

# --- Tab 3: Operational Efficiency ---
with tab3:
    st.header("Operational Efficiency Evaluation")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Processing Time by Department")
        dept_means = df.groupby("department")["wait_time_minutes"].mean()
        dept_means_df = pd.DataFrame({
            "Department": dept_means.index,
            "Average Wait Time": dept_means.values
        }).set_index("Department")
        st.bar_chart(dept_means_df)
    with col2:
        st.subheader("Department Workload")
        dept_counts = df["department"].value_counts()
        dept_counts_df = pd.DataFrame({
            "Department": dept_counts.index,
            "Count": dept_counts.values
        }).set_index("Department")
        st.bar_chart(dept_counts_df)

# --- Tab 4: Policy Recommendations ---
with tab4:
    st.header("Strategic Policy Implementation")
    st.subheader("Implementation Roadmap")
    st.markdown("""
    - **Immediate (0–3 months):**
        - Implement Electronic Truck Appointment System (ETAS)
        - Create temporary truck holding areas
    - **Medium-Term (3–12 months):**
        - Digitize 100% of documentation
        - Implement single-window clearance
    - **Long-Term (1–3 years):**
        - Build dedicated cargo lanes
        - Automate inspection processes
    """)

# --- Footer ---
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6c757d;">
    <p>KPA Operational Analytics • Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>
""", unsafe_allow_html=True)
