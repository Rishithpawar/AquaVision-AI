from pathlib import Path
from datetime import datetime
import pandas as pd


def log_pond_health(result, do, temperature, ph, ammonia):
    # Create history directory if needed
    history_dir = Path("data/history")
    history_dir.mkdir(parents=True, exist_ok=True)

    # Path to log file
    log_file = history_dir / "pond_health_log.csv"

    # Prepare one row of data
    row = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "PondHealthScore": result["PondHealthScore"],
        "StressLevel": result["StressLevel"],
        "BehavioralAnomalyRate": result["BehavioralAnomalyRate"],
        "AverageBehaviorRisk": result["AverageBehaviorRisk"],
        "LikelyCause": result["LikelyCause"],
        "Recommendation": result["Recommendation"],
        "DO": do,
        "Temperature": temperature,
        "pH": ph,
        "Ammonia": ammonia,
    }

    # Convert single row to DataFrame
    df = pd.DataFrame([row])

    # Append to CSV
    file_exists = log_file.exists()

    df.to_csv(
        log_file,
        mode="a",
        header=not file_exists,
        index=False
    )

    # Terminal confirmation
    print(f"History updated: {row['Timestamp']}")