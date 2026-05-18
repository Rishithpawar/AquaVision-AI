import pandas as pd

def compute_pond_health(do, temperature, ph, ammonia):
    # Load video-based anomaly results
    df = pd.read_csv("data/processed/fish_anomaly_results.csv")

    # Population metrics
    abnormal_rate = (df["Status"] == "Abnormal").mean() * 100
    avg_risk = df["RiskScore"].mean()

    # Start with a perfect score
    score = 100.0
    causes = []
    recommendations = []

    # Behavioral penalty
    score -= abnormal_rate * 0.8

    # Dissolved Oxygen
    if do < 4:
        score -= 25
        causes.append("Low dissolved oxygen")
        recommendations.append("Start aeration immediately")
    elif do < 5:
        score -= 10
        causes.append("Moderately low dissolved oxygen")
        recommendations.append("Increase aeration and monitor DO")

    # Temperature (generic warm-water fish ranges)
    if temperature < 22 or temperature > 32:
        score -= 10
        causes.append("Temperature outside optimal range")
        recommendations.append("Inspect temperature conditions")

    # pH
    if ph < 6.5 or ph > 8.5:
        score -= 10
        causes.append("pH outside optimal range")
        recommendations.append("Adjust water chemistry")

    # Ammonia
    if ammonia > 0.5:
        score -= 20
        causes.append("High ammonia")
        recommendations.append("Perform partial water exchange")

    # Bound score to [0, 100]
    score = max(0, min(100, score))

    # Stress level
    if score >= 85:
        stress_level = "Healthy"
    elif score >= 60:
        stress_level = "Elevated Stress"
    else:
        stress_level = "Critical"

    # Likely cause
    likely_cause = ", ".join(causes) if causes else "No major issues detected"

    # Recommendation text
    if recommendations:
        recommendation = " | ".join(sorted(set(recommendations)))
    else:
        recommendation = "Continue routine monitoring"

    return {
        "PondHealthScore": round(score, 1),
        "StressLevel": stress_level,
        "BehavioralAnomalyRate": round(abnormal_rate, 2),
        "AverageBehaviorRisk": round(avg_risk, 2),
        "LikelyCause": likely_cause,
        "Recommendation": recommendation
    }

if __name__ == "__main__":
    # Example values (will later come from dashboard inputs)
    result = compute_pond_health(
        do=4.2,
        temperature=29.0,
        ph=7.4,
        ammonia=0.2
    )

    print("\nPond Health Assessment\n")
    for key, value in result.items():
        print(f"{key}: {value}")