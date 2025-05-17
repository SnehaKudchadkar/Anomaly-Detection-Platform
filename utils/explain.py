def explain_anomalies(row):
    explanations = []

    if row.isnull().any():
        missing = row[row.isnull()].index.tolist()
        explanations.append(f"⚠️ Missing values in: {', '.join(missing)}.")

    if row.get("Anomaly", 0) == 1:
        confirmed = row.get("Confirmed Cases", None)
        deaths = row.get("Deaths", None)
        suspected = row.get("Suspected Cases", None)
        region = row.get("Region", "Unknown Region")
        date = row.get("Date", "Unknown Date")

        if confirmed is not None and confirmed > 80:
            explanations.append(f"🚨 Unusually high confirmed cases ({confirmed}) in {region} during {date}.")
            explanations.append("🦟 Suggest increasing fogging and vector control.")
            explanations.append("📢 Run awareness campaigns in affected areas.")

        if deaths is not None and deaths > 2:
            explanations.append(f"☠️ High death count ({deaths}) in {region} during {date}.")
            explanations.append("🚑 Check hospital response capacity and escalate emergency preparedness.")

        if confirmed is not None and suspected is not None and suspected > confirmed + 30:
            explanations.append(f"❗ Disproportionately high suspected cases ({suspected}) vs confirmed cases ({confirmed}).")
            explanations.append("🧪 Improve diagnostics and reduce test turnaround time.")

        severity = row.get("Anomaly_Severity", None)
        if severity is not None and severity < 1.5:
            explanations.append("ℹ️ Low-severity anomaly. May be due to minor fluctuation or noise.")

    return "\n".join(f"• {e}" for e in explanations) if explanations else "ℹ️ No specific insight generated."
