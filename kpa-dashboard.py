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
    .st-bb {
        background-color: white;
    }
    .st-at {
        background-color: #0d6efd;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
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

# Main Content
tab1, tab2, tab3, tab4 = st.tabs(["Traffic Patterns", "Congestion Analysis", "Operational Efficiency", "Policy Recommendations"])

with tab1:
    st.header("Traffic Volume and Patterns")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Daily Vehicle Volume Trend")
        st.line_chart(df.groupby('date')['vehicle_count'].sum())
    
    with col2:
        st.subheader("Gate Utilization Distribution")
        gate_dist = df['gate'].value_counts()
        st.dataframe(gate_dist.style.format("{:.1%}", subset=["count"]), height=300)
        st.bar_chart(gate_dist)
    
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
        wait_stats = df.groupby('gate')['wait_time_minutes'].agg(['mean', 'median', 'std'])
        st.dataframe(wait_stats.style.format("{:.1f}"))
    
    st.markdown("""
    <div class="card">
        <h4>Root Cause Analysis:</h4>
        <ul>
            <li>61.8% of delays caused by clearance processing</li>
            <li>Gate 12 has 40% longer wait times than other gates</li>
            <li>Afternoon hours account for 58.9% of congestion incidents</li>
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
    
    st.markdown("""
    <div class="card">
        <h4>Efficiency Findings:</h4>
        <ul>
            <li>67.7% of staff report excessive overtime due to processing delays</li>
            <li>Containerized cargo has 30% faster processing than bulk cargo</li>
            <li>Customs processing accounts for 45% of total wait time</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.header("Policy Recommendations")
    
    st.markdown("""
    <div class="card">
        <h4>Immediate Actions (0-3 months):</h4>
        <ol>
            <li>Implement Electronic Truck Appointment System (ETAS)</li>
            <li>Reallocate staff during peak hours (10AM-2PM)</li>
            <li>Launch pilot RFID clearance for frequent shippers</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h4>Medium-Term Solutions (3-12 months):</h4>
        <ol>
            <li>Digitize 100% of documentation processes</li>
            <li>Expand Gate 24 capacity to handle 25% of total traffic</li>
            <li>Implement unified customs-security clearance platform</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h4>Long-Term Infrastructure (1-3 years):</h4>
        <ol>
            <li>Build inland clearance depots to reduce port congestion</li>
            <li>Automate 80% of inspection processes with AI/ML</li>
            <li>Develop dedicated cargo corridors with smart traffic control</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>KPA Port Analytics • Last Updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
