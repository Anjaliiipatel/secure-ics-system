from pathlib import Path
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas


BASE_DIR = Path(__file__).resolve().parents[1]
PDF_REPORT_FILE = BASE_DIR / "reports" / "daily_security_report.pdf"


def generate_pdf_report(report_data):
    PDF_REPORT_FILE.parent.mkdir(exist_ok=True)

    pdf = canvas.Canvas(
        str(PDF_REPORT_FILE),
        pagesize=LETTER
    )

    width, height = LETTER
    y = height - 60

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(60, y, "Secure ICS Daily Security Report")

    y -= 35

    pdf.setFont("Helvetica", 10)
    pdf.drawString(60, y, f"Generated At: {report_data['generated_at']}")

    y -= 40

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, y, "Security Posture")

    y -= 25

    pdf.setFont("Helvetica", 11)
    pdf.drawString(80, y, f"Threat Level: {report_data['threat_level']}")

    y -= 18
    pdf.drawString(80, y, f"Threat Score: {report_data['threat_score']}/100")

    y -= 35

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, y, "Security Event Summary")

    y -= 25

    summary_items = [
        ("Total Events", report_data["total_events"]),
        ("Total Attacks", report_data["total_attacks"]),
        ("Replay Attacks", report_data["replay_attacks"]),
        ("Integrity Failures", report_data["integrity_failures"]),
        ("Unauthorized Sensors", report_data["unauthorized_sensors"]),
        ("Telemetry Anomalies", report_data["anomalies"]),
        ("Open Incidents", report_data["open_incidents"]),
    ]

    pdf.setFont("Helvetica", 11)

    for label, value in summary_items:
        pdf.drawString(80, y, f"{label}: {value}")
        y -= 18

    y -= 20

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, y, "Open Incidents")

    y -= 25

    pdf.setFont("Helvetica", 10)

    incidents = report_data.get("incidents", [])

    if incidents:
        for incident in incidents[:8]:
            line = (
                f"{incident.get('id', 'INC')} | "
                f"{incident.get('type', 'Security Event')} | "
                f"{incident.get('severity', 'INFO')} | "
                f"{incident.get('status', 'OPEN')}"
            )
            pdf.drawString(80, y, line)
            y -= 16
    else:
        pdf.drawString(80, y, "No open incidents.")
        y -= 16

    y -= 25

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, y, "Recommendations")

    y -= 25

    recommendations = [
        "Review high-severity incidents first.",
        "Investigate unauthorized sensor activity.",
        "Monitor replay and integrity failures.",
        "Continue observing telemetry anomalies.",
    ]

    pdf.setFont("Helvetica", 10)

    for item in recommendations:
        pdf.drawString(80, y, f"- {item}")
        y -= 16

    pdf.save()

    return PDF_REPORT_FILE