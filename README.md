# AquaVision AI 🐟

AquaVision AI is an end-to-end aquaculture intelligence platform that combines computer vision, machine learning, and water-quality analytics to monitor pond health and provide early warning recommendations.

## features 
- Fish detection and tracking using YOLO
- Behavioral anomaly detection using Isolation Forest
- Water-quality sensor fusion (DO, Temperature, pH, Ammonia)
- Pond Health Score and stress classification
- Historical trend analytics
- Automated PDF report generation
- Interactive Streamlit dashboard

## tech stack
- Python
- Streamlit
- YOLO (Ultralytics)
- OpenCV
- Scikit-learn
- Pandas
- ReportLab

## running locally

```bash
pip install -r requirements.txt
python -m streamlit run app/app.py