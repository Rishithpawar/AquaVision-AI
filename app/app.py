import os
from pathlib import Path

import pandas as pd
import streamlit as st

from src.run_pipeline import run_pipeline
from src.pond_health_engine import compute_pond_health
from src.history_logger import log_pond_health
from src.report_generator import generate_pdf_report

# ======================================================
# Page Configuration
# ======================================================
st.set_page_config(
    page_title="AquaVision AI",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# Custom CSS Styling
# ======================================================
st.markdown(
    """
    <style>
    .main {
        padding-top: 1rem;
    }

    .hero {
        padding: 1.5rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #0f172a, #1e3a8a);
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 800;
    }

    .hero p {
        margin-top: 0.5rem;
        font-size: 1.1rem;
        opacity: 0.9;
    }

    .metric-card {
        background: #ffffff;
        padding: 1rem;
        border-radius: 18px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        text-align: center;
    }

    .metric-title {
        font-size: 0.9rem;
        color: #6b7280;
        font-weight: 600;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        margin-top: 0.25rem;
    }

    .healthy {
        color: #059669;
    }

    .warning {
        color: #d97706;
    }

    .critical {
        color: #dc2626;
    }

    .section-card {
        background: #ffffff;
        padding: 1.25rem;
        border-radius: 18px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }

    .recommendation-box {
        background: #eff6ff;
        border-left: 6px solid #2563eb;
        padding: 1rem;
        border-radius: 12px;
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# Helper Function
# ======================================================
def get_status_class(stress_level):
    if stress_level == "Healthy":
        return "healthy"
    elif stress_level == "Elevated Stress":
        return "warning"
    else:
        return "critical"


# ======================================================
# Hero Section
# ======================================================
st.markdown(
    """
    <div class="hero">
        <h1>🐟 AquaVision AI</h1>
        <p>
            AI-Powered Aquaculture Monitoring and Early Warning System<br>
            Integrating CCTV Video Analytics and Water Quality Intelligence
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================================
# Sidebar Inputs
# ======================================================
st.sidebar.title("⚙️ Control Panel")

# Video Upload
st.sidebar.header("🎥 CCTV Video Input")
uploaded_file = st.sidebar.file_uploader(
    "Upload CCTV Footage",
    type=["mp4", "avi", "mov"]
)

if uploaded_file is not None:
    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/fish_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.sidebar.success("✅ Video uploaded successfully")

st.sidebar.divider()

# Water Quality Inputs
st.sidebar.header("📡 Water Quality Inputs")

do = st.sidebar.number_input(
    "Dissolved Oxygen (mg/L)",
    min_value=0.0,
    max_value=20.0,
    value=4.2,
    step=0.1
)

temperature = st.sidebar.number_input(
    "Temperature (°C)",
    min_value=0.0,
    max_value=50.0,
    value=29.0,
    step=0.1
)

ph = st.sidebar.number_input(
    "pH",
    min_value=0.0,
    max_value=14.0,
    value=7.4,
    step=0.1
)

ammonia = st.sidebar.number_input(
    "Ammonia (mg/L)",
    min_value=0.0,
    max_value=10.0,
    value=0.2,
    step=0.1
)

st.sidebar.divider()
# ======================================================
# Run Pipeline Button
# ======================================================
if st.sidebar.button("🚀 Analyze Pond", use_container_width=True):
    if uploaded_file is None:
        st.sidebar.error("Please upload a CCTV video first.")
        st.stop()

    # Capture the CURRENT sidebar values immediately
    current_do = do
    current_temperature = temperature
    current_ph = ph
    current_ammonia = ammonia

    with st.spinner("Running full AI pipeline... This may take several minutes."):
        # Run computer vision + ML pipeline
        run_pipeline()

        # Compute pond health using the CURRENT values
        analysis_result = compute_pond_health(
            do=current_do,
            temperature=current_temperature,
            ph=current_ph,
            ammonia=current_ammonia
        )

        # Save the CURRENT values to history
        log_pond_health(
            result=analysis_result,
            do=current_do,
            temperature=current_temperature,
            ph=current_ph,
            ammonia=current_ammonia
        )

        # Save these exact values for dashboard display
        st.session_state["analysis_inputs"] = {
            "do": current_do,
            "temperature": current_temperature,
            "ph": current_ph,
            "ammonia": current_ammonia,
        }

    st.sidebar.success("🎉 Analysis completed successfully!")

# ======================================================
# Check for Results
# ======================================================
results_file = "data/processed/fish_anomaly_results.csv"

if not os.path.exists(results_file):
    st.info(
        "👈 Upload CCTV footage, enter sensor values, and click 'Analyze Pond' to generate results."
    )
    st.stop()

# ======================================================
# Compute Pond Health (for display)
# ======================================================
if "analysis_inputs" in st.session_state:
    inputs = st.session_state["analysis_inputs"]
else:
    # Before the first analysis, use current sidebar values
    inputs = {
        "do": do,
        "temperature": temperature,
        "ph": ph,
        "ammonia": ammonia,
    }

# Use the stored analysis inputs
do = inputs["do"]
temperature = inputs["temperature"]
ph = inputs["ph"]
ammonia = inputs["ammonia"]

# Compute pond health using these exact values
result = compute_pond_health(
    do=do,
    temperature=temperature,
    ph=ph,
    ammonia=ammonia
)

status_class = get_status_class(result["StressLevel"])

# ======================================================
# KPI Cards
# ======================================================
col1, col2, col3, col4 = st.columns(4)

metrics = [
    ("Pond Health Score", f"{result['PondHealthScore']}/100"),
    ("Stress Level", result["StressLevel"]),
    ("Behavioral Anomaly Rate", f"{result['BehavioralAnomalyRate']:.2f}%"),
    ("Average Risk", f"{result['AverageBehaviorRisk']:.1f}%")
]

for col, (title, value) in zip([col1, col2, col3, col4], metrics):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">{title}</div>
                <div class="metric-value {status_class}">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")

# ======================================================
# Alert Banner
# ======================================================
if result["StressLevel"] == "Healthy":
    st.success("🟢 Pond conditions are healthy. Continue routine monitoring.")
elif result["StressLevel"] == "Elevated Stress":
    st.warning("🟡 Elevated stress detected. Review recommendations below.")
else:
    st.error("🔴 Critical conditions detected. Immediate intervention is recommended.")

# ======================================================
# Cause and Recommendations
# ======================================================
left, right = st.columns([1, 1])

with left:
    st.markdown(
        f"""
        <div class="section-card" style="color: #111827;">
            <h3 style="color: #111827; margin-bottom: 15px;">
                🧠 Likely Root Cause
            </h3>
            <p style="font-size: 20px; color: #111827; margin: 0;">
                {result['LikelyCause']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    st.markdown(
        f"""
        <div class="section-card" style="color: #111827;">
            <h3 style="color: #111827; margin-bottom: 15px;">
                🚨 Recommended Actions
            </h3>
            <div
                class="recommendation-box"
                style="
                    margin-top: 10px;
                    color: #111827;
                    font-size: 20px;
                    font-weight: 600;
                "
            >
                {result['Recommendation']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ======================================================
# Sensor Summary
# ======================================================
with st.expander("📡 Current Water Quality Readings"):
    sensor_df = pd.DataFrame({
        "Parameter": [
            "Dissolved Oxygen (mg/L)",
            "Temperature (°C)",
            "pH",
            "Ammonia (mg/L)"
        ],
        "Value": [do, temperature, ph, ammonia]
    })
    st.dataframe(sensor_df, use_container_width=True)

# ======================================================
# Historical Trends
# ======================================================
history_file = Path("data/history/pond_health_log.csv")

if history_file.exists():
    history_df = pd.read_csv(history_file)

    if len(history_df) >= 1:
        st.subheader("📈 Historical Trends")

        history_df["Timestamp"] = pd.to_datetime(
            history_df["Timestamp"],
            format="mixed",
            errors="coerce"
        )

        # Remove invalid timestamps if any
        history_df = history_df.dropna(subset=["Timestamp"])
        history_df = history_df.sort_values("Timestamp")

        with st.expander("📄 View Historical Log"):
            st.dataframe(history_df, use_container_width=True)

        st.line_chart(
            history_df.set_index("Timestamp")[
                ["PondHealthScore", "BehavioralAnomalyRate", "DO"]
            ]
        )
else:
    st.info(
        "📈 Historical trends will appear after you run the analysis at least once."
    )

# ======================================================
# Load Detailed Results
# ======================================================
df = pd.read_csv(results_file)

if "RiskScore" in df.columns:
    df = df.sort_values("RiskScore", ascending=False)

# ======================================================
# Tabs
# ======================================================
tab1, tab2, tab3 = st.tabs([
    "📊 Population Analytics",
    "📋 Detailed Results",
    "📈 Executive Summary"
])

# ======================================================
# Tab 1 - Population Analytics
# ======================================================
with tab1:
    if "RiskScore" in df.columns and "FishID" in df.columns:
        st.subheader("Population Risk Distribution")
        st.bar_chart(df.set_index("FishID")["RiskScore"])

    if "AlertLevel" in df.columns:
        st.subheader("Alert Level Distribution")
        st.bar_chart(df["AlertLevel"].value_counts())

# ======================================================
# Tab 2 - Detailed Results
# ======================================================
with tab2:
    st.subheader("Behavioral Analysis Results")
    st.dataframe(df, use_container_width=True)

# ======================================================
# Tab 3 - Executive Summary
# ======================================================
with tab3:
    st.subheader("📌 Operational Summary")

    st.write(f"**Pond Health Score:** {result['PondHealthScore']}/100")
    st.write(f"**Stress Level:** {result['StressLevel']}")
    st.write(
        f"**Behavioral Anomaly Rate:** "
        f"{result['BehavioralAnomalyRate']:.2f}%"
    )
    st.write(f"**Likely Cause:** {result['LikelyCause']}")
    st.write(f"**Recommended Action:** {result['Recommendation']}")

# ======================================================
# PDF Report Download
# ======================================================
st.subheader("📄 Download Report")

report_path = generate_pdf_report(
    result=result,
    do=do,
    temperature=temperature,
    ph=ph,
    ammonia=ammonia
)

with open(report_path, "rb") as pdf_file:
    st.download_button(
        label="📥 Download Pond Health PDF Report",
        data=pdf_file,
        file_name=report_path.name,
        mime="application/pdf",
        use_container_width=True,
    )
    
# ======================================================
# Footer
# ======================================================
st.divider()

st.caption(
    "AquaVision AI combines computer vision, machine learning, "
    "and water-quality analytics to provide pond-level health "
    "assessment and early warning recommendations for aquaculture."
)