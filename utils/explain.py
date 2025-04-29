def explain_anomalies(row):
    explanation = "This row differs significantly from normal patterns in the dataset. "
    if row.isnull().any():
        explanation += "It contains missing values. "
    if "Anomaly" in row and row["Anomaly"] == 1:
        explanation += "It has been flagged as an outlier by the anomaly detection algorithm."
    return explanation
