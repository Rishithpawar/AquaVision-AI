import numpy as np
import pandas as pd

# Step 1: Create a NumPy array of fish speeds (meters per second)
speeds = np.array([2.3, 4.1, 3.7, 8.2])

# Step 2: Perform numerical calculations
print("Fish Speeds:", speeds)
print("Average Speed:", np.mean(speeds))
print("Maximum Speed:", np.max(speeds))
print("Minimum Speed:", np.min(speeds))

# Step 3: Create a Pandas DataFrame (table)
df = pd.DataFrame({
    "FishID": [1, 2, 3, 4],
    "Speed": speeds,
    "Status": ["Normal", "Normal", "Normal", "Abnormal"]
})

# Step 4: Display the table
print("\nFish Data:")
print(df)

# Step 5: Save the table to a CSV file
df.to_csv("data/fish_behavior.csv", index=False)

print("\nCSV file saved to data/fish_behavior.csv")