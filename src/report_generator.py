from datetime import datetime
from pathlib import Path

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(result, do, temperature, ph, ammonia):
    """
    Generate a professional PDF report and return the file path.
    """

    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"pond_health_report_{timestamp}.pdf"

    doc = SimpleDocTemplate(str(report_path), pagesize=A4)

    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(
        Paragraph("AquaVision AI - Pond Health Report", styles["Title"])
    )
    story.append(Spacer(1, 20))

    # Report lines
    lines = [
        f"Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"Pond Health Score: {result['PondHealthScore']}/100",
        f"Stress Level: {result['StressLevel']}",
        f"Behavioral Anomaly Rate: "
        f"{result['BehavioralAnomalyRate']:.2f}%",
        f"Average Behavior Risk: "
        f"{result['AverageBehaviorRisk']:.2f}%",
        "",
        "Water Quality Readings:",
        f"- Dissolved Oxygen: {do} mg/L",
        f"- Temperature: {temperature} °C",
        f"- pH: {ph}",
        f"- Ammonia: {ammonia} mg/L",
        "",
        f"Likely Root Cause: {result['LikelyCause']}",
        "",
        f"Recommended Actions: {result['Recommendation']}",
    ]

    block = []
    for line in lines:
        if line == "":
            block.append(Spacer(1, 10))
        else:
            block.append(
                Paragraph(line, styles["Normal"])
            )

    story.append(KeepTogether(block))

    # Build PDF
    doc.build(story)

    return report_path