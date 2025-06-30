import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image
import os

# --- Page Config ---
st.set_page_config(
    page_title="KPA Stakeholder Analytics Dashboard",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Placeholder Image Generator ---
def generate_placeholder_images():
    output_dir = "kpa_work"
    os.makedirs(output_dir, exist_ok=True)
    for i in range(10):
        img_path = os.path.join(output_dir, f"output_0_{i}.png")
        if not os.path.exists(img_path):
            from PIL import ImageDraw
            img = Image.new("RGB", (800, 400), color=(220, 220, 220))
            d = ImageDraw.Draw(img)
            d.text((100, 180), f"Placeholder Image {i+1}", fill=(0, 0, 0))
            img.save(img_path)
    return {f"image{i+1}": os.path.join(output_dir, f"output_0_{i}.png") for i in range(10)}

IMAGE_PATHS = generate_placeholder_images()

# --- Data Simulation ---
@st.cache_data
def load_data():
    dates = pd.date_range(start="2023-01-01", end="2023-12-31")
    return pd.DataFrame({
        "date": dates,
        "vehicle_count": np.random.poisson(500, len(dates)),
        "wait_time_minutes": np.random.normal(90, 30, len(dates)).clip(10, 360),
        "gate": np.random.choice(["Gate 12", "Gate 9", "Gate 15", "Gate 24"], len(dates)),
        "issue_type": np.random.choice(["Clearance Delays", "Slow Processing", "Too Many Trucks", "Security Checks"], len(dates)),
        "department": np.random.choice(["Operations", "Security", "Logistics", "Customs"], len(dates)),
        "hour": np.random.choice(range(6, 21), len(dates))
    })

df = load_data()

# --- Display Helper ---
def display_image(img_key, caption, col=None):
    try:
        img = Image.open(IMAGE_PATHS[img_key])
        if col:
            with col:
                st.image(img, caption=caption, use_container_width=True)
        else:
            st.image(img, caption=caption, use_container_width=True)
    except:
        st.warning(f"Image for {caption} is missing.")

# --- Dashboard Layout ---
st.title("🚢 KPA Stakeholder Traffic Analytics Dashboard")

# --- Header Section ---
st.markdown("""
<div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px;">
<h3 style="color: #0d6efd;">General Objectives</h3>
<ul>
    <li><strong>Traffic Volume & Pattern:</strong> Analyze gate load and peak hours</li>
    <li><strong>Congestion Causes:</strong> Identify systemic bottlenecks</li>
    <li><strong>Operational Efficiency:</strong> Streamline operations</li>
    <li><strong>Policy Strategy:</strong> Recommend reforms</li>
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

with tab1:
    st.header("Traffic Volume and Pattern Assessment")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Traffic Over Time")
        st.line_chart(df.groupby("date")["vehicle_count"].sum())
    with col2:
        st.subheader("Image 1: Nationality")
        display_image("image1", "Distribution of stakeholders by nationality")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Gate Utilization")
        st.bar_chart(df["gate"].value_counts())
    with col2:
        st.subheader("Image 2: Gender")
        display_image("image2", "Gender distribution")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Hourly Traffic")
        st.bar_chart(df["hour"].value_counts().sort_index())
    with col2:
        st.subheader("Image 3: Experience")
        display_image("image3", "Years of experience")

with tab2:
    st.header("Congestion Cause Identification")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Delays by Cause")
        st.bar_chart(df["issue_type"].value_counts())
    with col2:
        st.subheader("Image 4: Visit Frequency")
        display_image("image4", "Visit frequency")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Wait Time Range")
        bins = [0, 30, 60, 120, 240, 360]
        labels = ["0–30", "31–60", "61–120", "121–240", "241–360"]
        df["wait_range"] = pd.cut(df["wait_time_minutes"], bins=bins, labels=labels)
        st.bar_chart(df["wait_range"].value_counts().sort_index())
    with col2:
        st.subheader("Image 5: Awaiting Time")
        display_image("image5", "Average awaiting time")

    st.subheader("Image 6: Traffic Congestion")
    display_image("image6", "Congestion frequency")

with tab3:
    st.header("Operational Efficiency")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Avg Wait by Dept")
        st.bar_chart(df.groupby("department")["wait_time_minutes"].mean())
    with col2:
        st.subheader("Image 7: Gate Usage")
        display_image("image7", "Gate usage")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Department Load")
        st.bar_chart(df["department"].value_counts())
    with col2:
        st.subheader("Image 8: Cargo Types")
        display_image("image8", "Cargo type")

    st.subheader("Image 9: Time of Day")
    display_image("image9", "Time of day")

with tab4:
    st.header("Policy Recommendations")
    st.subheader("Image 10: Common Issues")
    display_image("image10", "Common issues faced by stakeholders")

    st.markdown("""
    - **Short-Term (0–3 months)**: Launch truck appointment system, improve signage  
    - **Medium-Term (3–12 months)**: Digitize all paperwork, automate check-ins  
    - **Long-Term (1–3 years)**: Build new lanes, expand inspection units
    """)

# --- Footer ---
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6c757d;">
    <p>KPA Operational Dashboard • Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>
""", unsafe_allow_html=True)
