import subprocess

def run_pipeline():
    subprocess.run(["python", "src/detect_fish.py"], check=True)
    subprocess.run(["python", "src/track_fish.py"], check=True)
    subprocess.run(["python", "src/feature_engineering.py"], check=True)
    subprocess.run(["python", "src/train_anomaly_model.py"], check=True)