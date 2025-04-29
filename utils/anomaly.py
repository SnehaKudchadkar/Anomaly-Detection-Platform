import pandas as pd
from pyod.models.iforest import IForest
from sklearn.preprocessing import StandardScaler

def detect_anomalies(df):
    numeric_df = df.select_dtypes(include=["int64", "float64"]).dropna(axis=1)
    if numeric_df.empty:
        return df, pd.DataFrame()

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_df)

    model = IForest()
    model.fit(scaled_data)
    predictions = model.predict(scaled_data)

    df["Anomaly"] = predictions
    anomalies = df[df["Anomaly"] == 1]

    return df, anomalies
