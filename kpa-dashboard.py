import streamlit as st
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

# Call image generator before dashboard loads
generate_dashboard_images()

# Your existing Streamlit dashboard code follows here...
