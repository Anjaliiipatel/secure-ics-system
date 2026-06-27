import json
import csv
from pathlib import Path
from datetime import datetime

from analytics.security_analytics import SecurityAnalytics
from analytics.threat_score import ThreatScore
from incidents.incident_manager import IncidentManager


BASE_DIR = Path(__file__).resolve().parents[1]

REPORTS_DIR = BASE_DIR / "reports"

CSV_REPORT_FILE = REPORTS_DIR / "daily_security_report.csv"
TEXT_REPORT_FILE = REPORTS_DIR / "daily_security_report.txt"
JSON_REPORT_FILE = REPORTS_DIR / "daily_security_report.json"


class SecurityReportGenerator:

    def __init__(self):
        self.analytics = SecurityAnalytics()
        self.threat_score = ThreatScore()
        self.incident_manager = IncidentManager()

    def generate_report_data(self):
        summary = self.analytics.get_dashboard_summary()
        threat_data = self.threat_score.get_dashboard_data()
        open_incidents = self.incident_manager.get_open_incidents()

        report = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "threat_level": threat_data.get("level", "LOW"),
            "threat_score": threat_data.get("score", 0),
            "total_events": summary.get("total_events", 0),
            "total_attacks": summary.get("total_attacks", 0),
            "replay_attacks": summary.get("replay_attacks", 0),
            "integrity_failures": summary.get("integrity_failures", 0),
            "unauthorized_sensors": summary.get("unauthorized_sensors", 0),
            "anomalies": summary.get("anomalies", 0),
            "open_incidents": len(open_incidents),
            "incidents": open_incidents,
        }

        return report

    def generate_text_report(self):
        report = self.generate_report_data()

        lines = [
            "================================================",
            "        SECURE ICS DAILY SECURITY REPORT",
            "================================================",
            "",
            f"Generated At: {report['generated_at']}",
            "",
            "Security Posture",
            "----------------",
            f"Threat Level: {report['threat_level']}",
            f"Threat Score: {report['threat_score']}/100",
            "",
            "Security Event Summary",
            "----------------------",
            f"Total Events: {report['total_events']}",
            f"Total Attacks: {report['total_attacks']}",
            f"Replay Attacks: {report['replay_attacks']}",
            f"Integrity Failures: {report['integrity_failures']}",
            f"Unauthorized Sensors: {report['unauthorized_sensors']}",
            f"Telemetry Anomalies: {report['anomalies']}",
            "",
            "Incident Summary",
            "----------------",
            f"Open Incidents: {report['open_incidents']}",
            "",
        ]

        if report["incidents"]:
            for incident in report["incidents"]:
                lines.extend([
                    f"{incident.get('id', 'INC')} | "
                    f"{incident.get('type', 'Security Event')} | "
                    f"{incident.get('severity', 'INFO')} | "
                    f"{incident.get('status', 'OPEN')}",
                ])
        else:
            lines.append("No open incidents.")

        lines.extend([
            "",
            "Recommendations",
            "---------------",
            "- Review high-severity incidents first.",
            "- Validate unauthorized sensor activity.",
            "- Investigate repeated replay or integrity failures.",
            "- Continue monitoring telemetry anomalies.",
            "",
            "================================================",
        ])

        return "\n".join(lines)

    def save_text_report(self):
        REPORTS_DIR.mkdir(exist_ok=True)

        report_text = self.generate_text_report()

        with open(TEXT_REPORT_FILE, "w", encoding="utf-8") as file:
            file.write(report_text)

        return TEXT_REPORT_FILE

    def save_json_report(self):
        REPORTS_DIR.mkdir(exist_ok=True)

        report_data = self.generate_report_data()

        with open(JSON_REPORT_FILE, "w", encoding="utf-8") as file:
            json.dump(report_data, file, indent=4)

        return JSON_REPORT_FILE

    def generate_all_reports(self):
        text_path = self.save_text_report()
        json_path = self.save_json_report()
        csv_path = self.save_csv_report()

        return {
            "text_report": str(text_path),
            "json_report": str(json_path),
            "csv_report": str(csv_path)
        }

    def save_csv_report(self):
        REPORTS_DIR.mkdir(exist_ok=True)

        report = self.generate_report_data()

        rows = [
            ["Metric", "Value"],
            ["Generated At", report["generated_at"]],
            ["Threat Level", report["threat_level"]],
            ["Threat Score", report["threat_score"]],
            ["Total Events", report["total_events"]],
            ["Total Attacks", report["total_attacks"]],
            ["Replay Attacks", report["replay_attacks"]],
            ["Integrity Failures", report["integrity_failures"]],
            ["Unauthorized Sensors", report["unauthorized_sensors"]],
            ["Telemetry Anomalies", report["anomalies"]],
            ["Open Incidents", report["open_incidents"]],
        ]

        with open(CSV_REPORT_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        return CSV_REPORT_FILE


if __name__ == "__main__":
    generator = SecurityReportGenerator()

    reports = generator.generate_all_reports()

    print("Reports generated:")
    print(reports)