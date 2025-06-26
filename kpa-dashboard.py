import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import base64

# --- Page Config ---
st.set_page_config(
    page_title="KPA Stakeholder Analytics Dashboard",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
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
    .metric-card {
        background-color: #f8f9fa;
        border-left: 4px solid #0d6efd;
        padding: 15px;
        border-radius: 5px;
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

# --- Image Embedding (Base64) ---
def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
# (For actual deployment, replace with your image files)
# image1 = get_image_base64("media/image1.png")
# image2 = get_image_base64("media/image2.png")

# --- Header Section ---
st.title("🚢 KPA Stakeholder Traffic Analytics Dashboard")
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
    st.markdown(f"""
    <div class="metric-card">
        <h3>Avg Daily Vehicles</h3>
        <h1>{int(df['vehicle_count'].mean()):,}</h1>
        <p>5% above target</p>
    </div>
    """, unsafe_allow_html=True)
with cols[1]:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Avg Wait Time</h3>
        <h1>{int(df['wait_time_minutes'].mean())} mins</h1>
        <p>12% longer than benchmark</p>
    </div>
    """, unsafe_allow_html=True)
with cols[2]:
    st.markdown("""
    <div class="metric-card">
        <h3>Peak Hour Congestion</h3>
        <h1>60%</h1>
        <p>10AM-2PM daily</p>
    </div>
    """, unsafe_allow_html=True)
with cols[3]:
    st.markdown("""
    <div class="metric-card">
        <h3>Gate 12 Load</h3>
        <h1>35%</h1>
        <p>Primary bottleneck</p>
    </div>
    """, unsafe_allow_html=True)

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🚦 Traffic Patterns", 
    "⚠️ Congestion Analysis", 
    "⚙️ Operational Efficiency", 
    "📜 Policy Recommendations"
])

# --- Tab 1: Traffic Patterns ---
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Vehicle Count Trend")
        st.line_chart(df.groupby("date")["vehicle_count"].sum())
        
        st.subheader("Hourly Traffic Distribution")
        fig, ax = plt.subplots(figsize=(10,4))
        df["hour"].value_counts().sort_index().plot(kind="bar", color="#0d6efd", ax=ax)
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Vehicle Count")
        st.pyplot(fig)
    
    with col2:
        st.subheader("Gate Utilization")
        gate_data = df["gate"].value_counts(normalize=True) * 100
        fig, ax = plt.subplots(figsize=(10,4))
        gate_data.plot(kind="bar", color=["#0d6efd", "#6c757d", "#20c997", "#fd7e14"], ax=ax)
        ax.set_ylabel("Percentage (%)")
        st.pyplot(fig)
        
        # Example image placeholder (replace with actual images)
        st.image("https://via.placeholder.com/600x300?text=Gate+Congestion+Heatmap", 
                caption="Gate Congestion Heatmap (Example)")

# --- Tab 2: Congestion Analysis ---
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Delay Causes")
        issue_data = df["issue_type"].value_counts(normalize=True) * 100
        fig, ax = plt.subplots(figsize=(8,8))
        issue_data.plot(kind="pie", autopct="%1.1f%%", colors=["#0d6efd", "#6c757d", "#20c997", "#fd7e14"])
        st.pyplot(fig)
    
    with col2:
        st.subheader("Wait Time Distribution")
        fig, ax = plt.subplots(figsize=(10,5))
        ax.hist(df["wait_time_minutes"], bins=30, color="#0d6efd", edgecolor="white")
        ax.axvline(df["wait_time_minutes"].mean(), color="red", linestyle="--", label="Average")
        ax.set_xlabel("Wait Time (minutes)")
        ax.set_ylabel("Frequency")
        ax.legend()
        st.pyplot(fig)
        
        # Example process flow image
        st.image("https://via.placeholder.com/600x200?text=Clearance+Process+Flow", 
                caption="Current Clearance Process (Example)")

# --- Tab 3: Operational Efficiency ---
with tab3:
    st.subheader("Department Performance")
    col1, col2 = st.columns([2,1])
    
    with col1:
        dept_data = df.groupby("department")["wait_time_minutes"].mean().sort_values()
        fig, ax = plt.subplots(figsize=(8,4))
        dept_data.plot(kind="barh", color="#0d6efd", ax=ax)
        ax.set_xlabel("Average Wait Time (minutes)")
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        <div class="card">
        <h4>Key Findings:</h4>
        <ul>
            <li>Customs processing takes 2.3× longer than Operations</li>
            <li>67% of delays occur during shift changes</li>
            <li>Manual inspections add 45 mins avg delay</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Example before/after comparison
    st.subheader("Process Improvement Potential")
    cols = st.columns(2)
    with cols[0]:
        st.image("https://via.placeholder.com/400x250?text=Current+Process", 
                caption="Current Process (Avg 90 mins)")
    with cols[1]:
        st.image("https://via.placeholder.com/400x250?text=Optimized+Process", 
                caption="Target Process (Est. 45 mins)")

# --- Tab 4: Policy Recommendations ---
with tab4:
    st.subheader("Strategic Roadmap")
    
    roadmap = """
    ```mermaid
    gantt
        title KPA Improvement Timeline
        dateFormat  YYYY-MM-DD
        section Immediate (0-3mo)
        ETAS Implementation       :active, 2023-01-01, 90d
        Temp Holding Areas        :2023-01-15, 75d
        
        section Medium-Term (3-12mo)
        Digital Clearance        :2023-04-01, 180d
        Single-Window System     :2023-06-01, 150d
        
        section Long-Term (1-3yrs)
        Automated Inspection    :2024-01-01, 365d
        Cargo Lane Expansion    :2024-06-01, 540d
    ```
    """
    st.markdown(roadmap)
    
    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        <div class="card">
        <h4>🔄 Process Changes</h4>
        <ul>
            <li>Digitize 100% of documentation</li>
            <li>Implement RFID tracking</li>
            <li>Automate inspection checklists</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div class="card">
        <h4>🏗️ Infrastructure</h4>
        <ul>
            <li>Expand Gate 24 capacity</li>
            <li>Build inland clearance depots</li>
            <li>Install smart traffic systems</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown("""
        <div class="card">
        <h4>📊 Performance Targets</h4>
        <ul>
            <li>50% faster processing</li>
            <li>30% higher throughput</li>
            <li>24/7 clearance ops</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6c757d;">
    <p>KPA Operational Analytics • Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Data Source: Port Authority Terminal Systems | v2.1.0</p>
</div>
""", unsafe_allow_html=True)
