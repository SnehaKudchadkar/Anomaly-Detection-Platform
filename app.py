import streamlit as st
import pandas as pd
from utils.anomaly import detect_anomalies
from utils.explain import explain_anomalies

st.set_page_config(page_title="Universal Anomaly Detection App", layout="wide")

st.title("🔍 Universal Anomaly Detection App")
st.markdown("Upload any CSV data and detect anomalies across various data types.")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    if st.button("Run Anomaly Detection"):
        with st.spinner("Analyzing..."):
            result_df, anomalies = detect_anomalies(df)
            st.success("Anomaly Detection Completed")
            st.subheader("Anomaly Detection Result")
            st.dataframe(result_df)

            if not anomalies.empty:
                st.subheader("📌 Detected Anomalies Explained")
                for idx, row in anomalies.iterrows():
                    explanation = explain_anomalies(row)
                    st.markdown(f"**Row {idx}:** {explanation}")
            else:
                st.info("No significant anomalies detected.")
