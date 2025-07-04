import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from modules.preprocess import load_data, preprocess
from modules.risk_analysis import detect_anomalies, cluster_risks
from modules.interventions import suggest_interventions

# Streamlit Page Setup 
st.set_page_config(page_title="Workplace Wellness Risk Monitor", layout="wide")

st.markdown("<h1 style='color:#1f77b4;'>🏥 Workplace Wellness Risk Monitor</h1>", unsafe_allow_html=True)
st.markdown("An intelligent system to identify employees at risk of occupational health issues and suggest targeted wellness interventions.")

#  File Upload -Sidebar
st.sidebar.header("📂 Upload Employee Health Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

#  Loading Data
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = load_data("data/raw_data.csv")

rows_before = len(df)

#  Remove fully empty rows
df.dropna(how='all', inplace=True)

#  Remove rows missing required fields
df.dropna(subset=['employee_id', 'heart_rate', 'blood_pressure', 'fatigue_score'], how='any', inplace=True)

rows_after = len(df)

# Optional Warning for Skipped Rows
if rows_after < rows_before:
    st.warning(f"⚠️ Removed {rows_before - rows_after} incomplete or empty rows from the dataset.")


#  Raw Data Preview 
with st.expander("📋 Preview Raw Data", expanded=True):
    st.caption(f"Showing {len(df)} cleaned employee records")
    st.dataframe(df, height=400)

# Preprocess & Analyze 
df_processed = preprocess(df)
features = ['heart_rate', 'blood_pressure', 'fatigue_score']

df_processed = detect_anomalies(df_processed, features)
df_processed = cluster_risks(df_processed, features)
df_processed = suggest_interventions(df_processed)

#  Show Processed Data 
show_table = st.sidebar.checkbox("📋 Show Processed Data Table")
if show_table:
    st.subheader("📋 Full Processed Data")
    st.dataframe(df_processed[['employee_id', 'heart_rate', 'blood_pressure', 'fatigue_score',
                               'is_anomaly', 'risk_group', 'intervention']], height=400)

#  Bar chart
st.markdown("### 📊 Employee Risk Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("👥 Total Employees", len(df_processed))
with col2:
    st.metric("⚠️ Anomalies Detected", df_processed['is_anomaly'].sum())
with col3:
    st.metric("🔴 High Risk Employees", (df_processed['risk_group'] == 2).sum())

#Chart Toggle
show_chart = st.checkbox("📉 Show Risk Group Bar Chart")

if show_chart:
    st.markdown("### 📊 Risk Group Distribution")
    counts = df_processed['risk_group'].value_counts().sort_index()
    labels = ['Low', 'Medium', 'High']
    colors = ['green', 'orange', 'red']

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(labels, counts, color=colors)
    ax.set_title("Employees by Risk Group")
    ax.set_ylabel("Number of Employees")
    st.pyplot(fig)

# Top N High-Risk Employees 
st.markdown("### 🔍 View Top N High-Risk Employees")
high_risk = df_processed[df_processed['risk_group'] == 2]
max_n = len(high_risk)

if max_n == 0:
    st.warning("There are no high-risk employees currently.")
else:
    n = st.number_input(
        f"Enter number of employees to view (max = {max_n})",
        min_value=1,
        max_value=max_n,
        value=min(3, max_n),
        step=1
    )
    top_n = high_risk.sort_values(by='fatigue_score', ascending=False).head(n)
    st.dataframe(top_n[['employee_id', 'heart_rate', 'blood_pressure', 'fatigue_score', 'intervention']], height=300)


#  Download Button 
st.download_button("⬇️ Download Full Processed Data",
                   data=df_processed.to_csv(index=False),
                   file_name="processed_results.csv",
                   mime="text/csv")
