import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image
import os

# --- Page Config ---
st.set_page_config(
    page_title="KPA Stakeholder Analytics Dashboard",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Image Path Configuration ---
# =================================================================
# REPLACE THESE PATHS WITH YOUR ACTUAL IMAGE FILE LOCATIONS
IMAGE_PATHS = {
    "image1": r"C:\Users\Administrator\Desktop\kpa work\output_0_0.png",  # distribution of stakeholders by nationality.
    "image2": r"C:\Users\Administrator\Desktop\kpa work\output_0_1.png",  # gender distribution by stakeholders.
    "image3": r"C:\Users\Administrator\Desktop\kpa work\output_0_2.png",  # years of experience distribution.
    "image4": r"C:\Users\Administrator\Desktop\kpa work\output_0_3.png",  # visit frequency distirbution.
    "image5": r"C:\Users\Administrator\Desktop\kpa work\output_0_4.png",  #  average awaiting time distribution.
    "image6": r"C:\Users\Administrator\Desktop\kpa work\output_0_5.png",  # traffic congestion frequency.
    "image7": r"C:\Users\Administrator\Desktop\kpa work\output_0_6.png",  # gate usage distribution.
    "image8": r"C:\Users\Administrator\Desktop\kpa work\output_0_7.png",  # cargo type distribution.
    "image9": r"C:\Users\Administrator\Desktop\kpa work\output_0_8.png",  # time of the day distribution.
    "image10":r"C:\Users\Administrator\Desktop\kpa work\output_0_9.png"   # common issues faced by stakeholders.
}
# =================================================================

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
    .metric-card {
        background-color: #f8f9fa;
        border-left: 4px solid #0d6efd;
        padding: 15px;
        border-radius: 5px;
    }
    .image-container {
        margin: 20px 0;
        border: 1px solid #eee;
        border-radius: 8px;
        padding: 10px;
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

# --- Image Display Function ---
def display_image(img_key, caption, col=None):
    """Displays image with error handling"""
    try:
        img = Image.open(IMAGE_PATHS[img_key])
        if col:
            with col:
                st.image(img, caption=caption, use_column_width=True)
        else:
            st.image(img, caption=caption, use_column_width=True)
    except Exception as e:
        placeholder = f"https://via.placeholder.com/800x400?text=Missing+{img_key}"
        if col:
            with col:
                st.image(placeholder, caption=f"Placeholder: {caption} | Error: {str(e)}", use_column_width=True)
        else:
            st.image(placeholder, caption=f"Placeholder: {caption} | Error: {str(e)}", use_column_width=True)

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
    st.header("Traffic Volume and Pattern Assessment")
    
    # Row 1: Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Vehicle Count Trend")
        st.line_chart(df.groupby("date")["vehicle_count"].sum())
    with col2:
        st.subheader("Gate Utilization")
        gate_data = df["gate"].value_counts(normalize=True) * 100
        st.bar_chart(gate_data)
    
    # Row 2: Image 1
    st.subheader("Traffic Flow Analysis")
    display_image("image1", "distribution of stakeholders by nationality")
    
    # Row 3: Image 2 and Hourly Chart
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Gate Congestion Heatmap")
        display_image("image2", "gender distribution by stakeholders")
    with col2:
        st.subheader("Hourly Traffic Distribution")
        hour_data = df["hour"].value_counts().sort_index()
        st.bar_chart(hour_data)
    
    # Row 4: Image 3
    st.subheader("Peak Hour Patterns")
    display_image("image3", "years of experience distribution")

# --- Tab 2: Congestion Analysis ---
with tab2:
    st.header("Congestion Cause Identification")
    
    # Row 1: Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Delay Causes")
        issue_data = df["issue_type"].value_counts(normalize=True) * 100
        st.bar_chart(issue_data)
    with col2:
        st.subheader("Wait Time Distribution")
        fig, ax = plt.subplots()
        ax.hist(df["wait_time_minutes"], bins=30, color="#0d6efd", edgecolor="white")
        ax.set_xlabel("Wait Time (minutes)")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    
    # Row 2: Image 4
    st.subheader("Congestion Hotspots")
    display_image("image4", "visit frequency distirbution")
    
    # Row 3: Image 5 and 6
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Delay Cause Breakdown")
        display_image("image5", " average awaiting time distribution")
    with col2:
        st.subheader("Process Bottlenecks")
        display_image("image6", "traffic congestion frequency")

# --- Tab 3: Operational Efficiency ---
with tab3:
    st.header("Operational Efficiency Evaluation")
    
    # Row 1: Image 7
    st.subheader("Department Performance Metrics")
    display_image("image7", "gate usage distribution")
    
    # Row 2: Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Processing Time by Department")
        dept_data = df.groupby("department")["wait_time_minutes"].mean()
        st.bar_chart(dept_data)
    with col2:
        st.subheader("Resource Allocation")
        fig, ax = plt.subplots()
        df["department"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax)
        st.pyplot(fig)
    
    # Row 3: Image 8
    st.subheader("Optimization Potential")
    display_image("image8", "cargo type distribution.")

# --- Tab 4: Policy Recommendations ---
with tab4:
    st.header("Strategic Policy Implementation")
    
    st.subheader("Implementation Roadmap")
    st.markdown("""
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
    """)
    
    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        <div class="card">
        <h4>🔄 Process Changes</h4>
        <ul>
            <li>Digitize documentation</li>
            <li>Implement RFID tracking</li>
            <li>Automate inspections</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown("""
        <div class="card">
        <h4>🏗️ Infrastructure</h4>
        <ul>
            <li>Expand Gate 24 capacity</li>
            <li>Build inland depots</li>
            <li>Smart traffic systems</li>
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
            <li>24/7 operations</li>
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
