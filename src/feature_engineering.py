import pandas as pd

print("Loading frame-level fish data...")
df = pd.read_csv("data/processed/fish_features.csv")

print("Computing behavioral summary features...")

summary = df.groupby("FishID").agg({
    "Speed": ["mean", "max", "std"],
    "Frame": "count"
})

# Flatten multi-level column names
summary.columns = [
    "AvgSpeed",
    "MaxSpeed",
    "StdSpeed",
    "TotalFrames"
]

# Convert FishID from index back to a normal column
summary = summary.reset_index()

# Replace NaN values (can happen if a fish has only one frame)
summary = summary.fillna(0)

# Save the summary dataset
summary.to_csv(
    "data/processed/fish_behavior_summary.csv",
    index=False
)

print("Feature engineering complete!")
print("Saved to data/processed/fish_behavior_summary.csv")
print()
print(summary.head())