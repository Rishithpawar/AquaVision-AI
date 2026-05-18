from ultralytics import YOLO

print("Loading YOLO model...")

# Load a small pre-trained YOLO model
model = YOLO("yolov8n.pt")

print("Running detection on video...")

# Run detection
results = model(
    "data/raw/fish_video.mp4",
    save=True,
    project="outputs",
    name="fish_detection"
)

print("Detection complete!")
print("Output saved in outputs/fish_detection/")