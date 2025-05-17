import pandas as pd
import numpy as np
from stumpy import stump

def detect_anomalies(df, window_size=10, severity_threshold=2.5):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    result_df = []

    for region in df["Region"].unique():
        region_df = df[df["Region"] == region].copy().sort_values("Date")
        values = region_df["Confirmed Cases"].values.astype(float)

        # Skip if not enough data
        if len(values) < window_size * 2:
            region_df["Anomaly"] = 0
            region_df["Anomaly_Severity"] = 0
            result_df.append(region_df)
            continue

        # Matrix Profile
        mp = stump(values, m=window_size)
        profile = mp[:, 0]
        profile = np.concatenate([profile, [np.nan] * (window_size - 1)])
        region_df["MatrixProfile"] = profile

        # Normalize
        mp_z = (profile - np.nanmean(profile)) / (np.nanstd(profile) + 1e-5)
        mp_z = np.nan_to_num(mp_z)

        case_z = (values - np.mean(values)) / (np.std(values) + 1e-5)
        combined_z = np.maximum(np.abs(mp_z), np.abs(case_z))

        # Mark anomalies
        region_df["Anomaly"] = (combined_z > severity_threshold).astype(int)
        region_df["Anomaly_Severity"] = combined_z

        result_df.append(region_df)

    final_df = pd.concat(result_df, ignore_index=True)
    anomalies = final_df[final_df["Anomaly"] == 1]
    return final_df, anomalies
