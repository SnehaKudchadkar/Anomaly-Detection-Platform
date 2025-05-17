import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.anomaly import detect_anomalies
from utils.explain import explain_anomalies

# Configure Streamlit page
st.set_page_config(page_title="Anomaly Detection", layout="wide")
st.title("🦟 Dengue Anomaly Detection (Goa Talukas)")
st.markdown("Upload a CSV with 'Date', 'Region', 'Confirmed Cases', and optional 'Deaths' columns.")

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
                
                # Plot confirmed cases
                sns.lineplot(data=region_df, x="Date", y="Confirmed Cases", label="Confirmed Cases", ax=ax, marker="o", color='blue')
                
                # Add death rate line if the column exists
                if "Deaths" in region_df.columns:
                    # Create a second y-axis for deaths (to handle different scales)
                    ax2 = ax.twinx()
                    sns.lineplot(data=region_df, x="Date", y="Deaths", label="Deaths", ax=ax2, marker="s", color='darkred', linestyle='--')
                    ax2.set_ylabel("Deaths", color='darkred')
                    ax2.tick_params(axis='y', colors='darkred')
                    
                    # Combine legends
                    lines1, labels1 = ax.get_legend_handles_labels()
                    lines2, labels2 = ax2.get_legend_handles_labels()
                    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
                else:
                    plt.legend()
                
                # Highlight anomalies
                anomaly_points = region_df[region_df["Anomaly"] == 1]
                plt.scatter(anomaly_points["Date"], anomaly_points["Confirmed Cases"], color='red', label="Anomaly", zorder=5, s=80)
                
                plt.title(f"🗺️ {region} - Weekly Dengue Cases and Deaths")
                plt.xlabel("Date")
                ax.set_ylabel("Confirmed Cases", color='blue')
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                
                # Show correlation value if both metrics exist
                if "Deaths" in region_df.columns:
                    correlation = region_df["Confirmed Cases"].corr(region_df["Deaths"])
                    st.write(f"📊 Correlation between Confirmed Cases and Deaths in {region}: **{correlation:.2f}**")
