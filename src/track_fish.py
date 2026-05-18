from ultralytics import YOLO
import pandas as pd
import numpy as np

print("Loading YOLO model...")
model = YOLO("yolov8n.pt")

print("Running tracking...")
results = model.track(
    "data/raw/fish_video.mp4",
    save=True,
    persist=True
)

records = []
previous_positions = {}

print("Extracting positions and speeds...")

for frame_number, result in enumerate(results):
    if result.boxes.id is None:
        continue

    ids = result.boxes.id.cpu().numpy().astype(int)
    boxes = result.boxes.xyxy.cpu().numpy()

    for fish_id, box in zip(ids, boxes):
        x1, y1, x2, y2 = box
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        speed = 0.0
        if fish_id in previous_positions:
            prev_x, prev_y = previous_positions[fish_id]
            speed = np.sqrt(
                (center_x - prev_x) ** 2 +
                (center_y - prev_y) ** 2
            )

        previous_positions[fish_id] = (center_x, center_y)

        records.append({
            "FishID": fish_id,
            "Frame": frame_number,
            "CenterX": center_x,
            "CenterY": center_y,
            "Speed": speed
        })

df = pd.DataFrame(records)
df.to_csv("data/processed/fish_features.csv", index=False)

print("Tracking complete!")
print("CSV saved to data/processed/fish_features.csv")