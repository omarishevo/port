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

# --- Absolute Image Paths for Local Machine ---
IMAGE_PATHS = {
    "image1": r"C:\Users\Administrator\Desktop\kpa work\output_0_0.png",
    "image2": r"C:\Users\Administrator\Desktop\kpa work\output_0_1.png",
    "image3": r"C:\Users\Administrator\Desktop\kpa work\output_0_2.png",
    "image4": r"C:\Users\Administrator\Desktop\kpa work\output_0_3.png",
    "image5": r"C:\Users\Administrator\Desktop\kpa work\output_0_4.png",
    "image6": r"C:\Users\Administrator\Desktop\kpa work\output_0_5.png",
    "image7": r"C:\Users\Administrator\Desktop\kpa work\output_0_6.png",
    "image8": r"C:\Users\Administrator\Desktop\kpa work\output_0_7.png",
    "image9": r"C:\Users\Administrator\Desktop\kpa work\output_0_8.png",
    "image10": r"C:\Users\Administrator\Desktop\kpa work\output_0_9.png"
}

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

# --- Image Display Function ---
def display_image(img_key, caption, col=None):
    try:
        img = Image.open(IMAGE_PATHS[img_key])
        if col:
            with col:
                st.image(img, caption=caption, use_container_width=True)
        else:
            st.image(img, caption=caption, use_container_width=True)
    except Exception as e:
        placeholder = f"https://via.placeholder.com/800x400?text=Missing+{img_key}"
        if col:
            with col:
                st.image(placeholder, caption=f"Missing: {caption}", use_container_width=True)
        else:
            st.image(placeholder, caption=f"Missing: {caption}", use_container_width=True)

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
        st.subheader("Image 1: Stakeholder Nationality")
        display_image("image1", "Distribution of stakeholders by nationality")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Gate Utilization (%)")
        gate_counts = df["gate"].value_counts(normalize=True) * 100
        gate_df = pd.DataFrame({"Gate": gate_counts.index, "Utilization": gate_counts.values}).set_index("Gate")
        st.bar_chart(gate_df)
    with col2:
        st.subheader("Image 2: Gender Distribution")
        display_image("image2", "Gender distribution by stakeholders")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Hourly Traffic Distribution")
        hour_counts = df["hour"].value_counts().sort_index()
        hour_df = pd.DataFrame({"Hour": hour_counts.index, "Count": hour_counts.values}).set_index("Hour")
        st.bar_chart(hour_df)
    with col2:
        st.subheader("Image 3: Experience Levels")
        display_image("image3", "Years of experience distribution")

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
        st.subheader("Image 4: Visit Frequency")
        display_image("image4", "Visit frequency distribution")

    col1, col2 = st.columns(2)
    with col1:
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
    with col2:
        st.subheader("Image 5: Awaiting Time")
        display_image("image5", "Average awaiting time distribution")

    st.subheader("Image 6: Traffic Congestion")
    display_image("image6", "Traffic congestion frequency")

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
        st.subheader("Image 7: Gate Usage")
        display_image("image7", "Gate usage distribution")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Department Workload")
        dept_counts = df["department"].value_counts()
        dept_counts_df = pd.DataFrame({
            "Department": dept_counts.index,
            "Count": dept_counts.values
        }).set_index("Department")
        st.bar_chart(dept_counts_df)
    with col2:
        st.subheader("Image 8: Cargo Types")
        display_image("image8", "Cargo type distribution")

    st.subheader("Image 9: Time of Day")
    display_image("image9", "Time of the day distribution")

# --- Tab 4: Policy Recommendations ---
with tab4:
    st.header("Strategic Policy Implementation")
    st.subheader("Image 10: Common Issues")
    display_image("image10", "Common issues faced by stakeholders")

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
""", unsafe_allow_html=True) remove the images path and include this code import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image
import os
import matplotlib.pyplot as plt
import seaborn as sns

# --- Generate Images for Dashboard ---
def generate_dashboard_images():
    output_dir = r"C:\\Users\\Administrator\\Desktop\\kpa work"
    os.makedirs(output_dir, exist_ok=True)
    sns.set(style="whitegrid")

    # 0. Stakeholder Nationality
    plt.figure(figsize=(8, 6))
    data = pd.Series(["Kenyan", "Tanzanian", "Ugandan", "Rwandese", "Other"]).sample(200, replace=True)
    sns.countplot(y=data, order=data.value_counts().index)
    plt.title("Distribution of Stakeholders by Nationality")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "output_0_0.png"))
    plt.close()

    # 1. Gender Distribution
    plt.figure(figsize=(6, 6))
    genders = pd.Series(np.random.choice(["Male", "Female"], 200, p=[0.7, 0.3]))
    genders.value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
    plt.title("Gender Distribution by Stakeholders")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "output_0_1.png"))
    plt.close()

    # 2. Years of Experience
    plt.figure(figsize=(8, 6))
    experience = np.random.choice(["0–2 yrs", "3–5 yrs", "6–10 yrs", "10+ yrs"], 200)
    sns.countplot(x=experience, order=["0–2 yrs", "3–5 yrs", "6–10 yrs", "10+ yrs"])
    plt.title("Years of Experience Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "output_0_2.png"))
    plt.close()

    # 3. Visit Frequency
    plt.figure(figsize=(8, 6))
    visits = np.random.choice(["Daily", "Weekly", "Monthly", "Rarely"], 200)
    sns.countplot(x=visits, order=["Daily", "Weekly", "Monthly", "Rarely"])
    plt.title("Visit Frequency Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "output_0_3.png"))
    plt.close()

    # 4. Average Awaiting Time
    plt.figure(figsize=(8, 6))
    waits = np.random.normal(90, 30, 200).clip(10, 360)
    sns.histplot(waits, bins=20, kde=True)
    plt.title("Average Awaiting Time (mins)")
    plt.xlabel("Minutes")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "output_0_4.png"))
    plt.close()

    # 5. Traffic Congestion Frequency
    plt.figure(figsize=(8, 6))
    congestion = np.random.choice(["Low", "Moderate", "High", "Severe"], 200)
    sns.countplot(x=congestion, order=["Low", "Moderate", "High", "Severe"])
    plt.title("Traffic Congestion Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "output_0_5.png"))
    plt.close()

    # 6. Gate Usage
    plt.figure(figsize=(8, 6))
    gates = np.random.choice(["Gate 12", "Gate 9", "Gate 15", "Gate 24"], 200)
    sns.countplot(y=gates, order=["Gate 12", "Gate 9", "Gate 15", "Gate 24"])
    plt.title("Gate Usage Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "output_0_6.png"))
    plt.close()

    # 7. Cargo Type
    plt.figure(figsize=(8, 6))
    cargo = np.random.choice(["Container", "Bulk", "Liquid", "Vehicles", "Other"], 200)
    sns.countplot(x=cargo, order=pd.Series(cargo).value_counts().index)
    plt.title("Cargo Type Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "output_0_7.png"))
    plt.close()

    # 8. Time of Day
    plt.figure(figsize=(8, 6))
    time_periods = np.random.choice(["Morning", "Midday", "Afternoon", "Evening"], 200)
    sns.countplot(x=time_periods, order=["Morning", "Midday", "Afternoon", "Evening"])
    plt.title("Time of the Day Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "output_0_8.png"))
    plt.close()

    # 9. Common Issues
    plt.figure(figsize=(8, 6))
    issues = ["Clearance Delays", "Too Many Trucks", "Security Checks", "Slow Processing"]
    counts = [120, 90, 45, 70]
    issue_df = pd.DataFrame({"Issue": issues, "Count": counts})
    sns.barplot(x="Count", y="Issue", data=issue_df, palette="mako")
    plt.title("Common Issues Faced by Stakeholders")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "output_0_9.png"))
    plt.close()

# Call image generator once before dashboard runs
generate_dashboard_images()

# Your existing Streamlit dashboard code follows here...
# (Not re-included here due to space. You can paste the dashboard code directly below this call.)
