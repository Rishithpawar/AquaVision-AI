import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

print("Loading behavioral summary data...")
df = pd.read_csv("data/processed/fish_behavior_summary.csv")

features = ["AvgSpeed", "MaxSpeed", "StdSpeed", "TotalFrames"]
X = df[features]

print("Training Isolation Forest model...")
model = IsolationForest(
    n_estimators=100,
    contamination=0.1,
    random_state=42
)

model.fit(X)

# Predictions
df["Anomaly"] = model.predict(X)
df["Status"] = df["Anomaly"].map({
    1: "Normal",
    -1: "Abnormal"
})

# Raw anomaly scores (lower = more anomalous)
scores = model.decision_function(X)

# Convert to 0-100 risk score
# Invert scores so higher means more risky
risk = (scores.max() - scores) / (scores.max() - scores.min()) * 100
df["RiskScore"] = risk.round(1)

# Alert levels
def get_alert_level(r):
    if r < 30:
        return "Healthy"
    elif r < 70:
        return "Warning"
    else:
        return "Critical"

# Recommendations
def get_recommendation(level):
    if level == "Healthy":
        return "Continue routine monitoring"
    elif level == "Warning":
        return "Inspect dissolved oxygen and water quality"
    else:
        return "Immediate investigation recommended"

df["AlertLevel"] = df["RiskScore"].apply(get_alert_level)
df["Recommendation"] = df["AlertLevel"].apply(get_recommendation)

# Save results
df.to_csv("data/processed/fish_anomaly_results.csv", index=False)

# Save model
joblib.dump(model, "models/anomaly_detector.pkl")

print("Enhanced anomaly detection complete!")
print(df[[
    'FishID',
    'RiskScore',
    'AlertLevel',
    'Recommendation'
]].head())