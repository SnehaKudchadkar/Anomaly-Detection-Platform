import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.anomaly import detect_anomalies
from utils.explain import explain_anomalies  # Add this if not already

# Configure Streamlit page
st.set_page_config(page_title="Anomaly Detection", layout="wide")
st.title("🦟 Dengue Anomaly Detection (Goa Talukas)")
st.markdown("Upload a CSV with 'Date', 'Region', and 'Confirmed Cases' columns.")

# File Upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["Date"] = pd.to_datetime(df["Date"])  # Ensure date format
    st.write("🗂️ Preview of Uploaded Data:")
    st.dataframe(df.head())

    # Sidebar Configuration
    st.sidebar.header("⚙️ Configuration")
    severity_threshold = st.sidebar.slider("Anomaly Severity Threshold", 0.0, 5.0, 2.5, step=0.1)
    window_size = st.sidebar.slider("Matrix Profile Window Size", 5, 30, 10)

    if st.button("🚀 Run Anomaly Detection"):
        with st.spinner("Running anomaly detection..."):
            result_df, anomalies = detect_anomalies(df, window_size=window_size, severity_threshold=severity_threshold)
            st.success("✅ Detection complete.")

            # Show result
            st.subheader("📋 Anomaly Detection Result")
            st.dataframe(anomalies)

            # Add explanations
            st.subheader("💡 Explanation of Detected Anomalies")
            if not anomalies.empty:
                anomalies["Explanation"] = anomalies.apply(explain_anomalies, axis=1)
                st.dataframe(anomalies[["Date", "Region", "Confirmed Cases", "Anomaly_Severity", "Explanation"]])
            else:
                st.info("No anomalies detected with the selected parameters.")

            # Plotting
            st.subheader("📈 Visual Context (Per Region)")
            for region in result_df["Region"].unique():
                region_df = result_df[result_df["Region"] == region].copy()
                fig, ax = plt.subplots(figsize=(10, 4))
                sns.lineplot(data=region_df, x="Date", y="Confirmed Cases", label="Confirmed Cases", ax=ax, marker="o")
                anomaly_points = region_df[region_df["Anomaly"] == 1]
                plt.scatter(anomaly_points["Date"], anomaly_points["Confirmed Cases"], color='red', label="Anomaly", zorder=5)
                plt.title(f"🗺️ {region} - Weekly Dengue Cases")
                plt.xlabel("Date")
                plt.ylabel("Confirmed Cases")
                plt.xticks(rotation=45)
                plt.legend()
                st.pyplot(fig)
