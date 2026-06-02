import statistics
import time
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "system_logs.txt"


class AnomalyDetector:

    # =====================================================
    # CONFIGURATION
    # =====================================================

    TEMPERATURE_MAX = 95
    PRESSURE_MIN = 20
    RPM_MAX = 5000

    TEMP_DEVIATION_THRESHOLD = 20
    PRESSURE_DEVIATION_THRESHOLD = 10
    RPM_DEVIATION_THRESHOLD = 2000

    MAX_HISTORY = 20

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        self.telemetry_history = {
            "temperature": [],
            "pressure": [],
            "rpm": []
        }

        self.stats = {
            "total_packets": 0,
            "alerts_generated": 0
        }

    # =====================================================
    # LOGGING
    # =====================================================

    def log_alert(self, alert):

        timestamp = time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(LOG_FILE, "a") as log_file:

            log_file.write(
                f"{timestamp} | "
                f"{alert['severity']} | "
                f"{alert['alert_type']} | "
                f"{alert['description']}\n"
            )

    # =====================================================
    # SEVERITY CLASSIFICATION
    # =====================================================

    def classify_severity(self, alert_type):

        severity_map = {
            "Telemetry Anomaly": "HIGH",
            "Replay Attack": "HIGH",
            "Flooding Attack": "CRITICAL",
            "Integrity Failure": "CRITICAL",
            "Authentication Failure": "MEDIUM"
        }

        return severity_map.get(
            alert_type,
            "LOW"
        )

    # =====================================================
    # THRESHOLD DETECTION
    # =====================================================

    def threshold_detection(self, telemetry):

        alerts = []

        if telemetry["temperature"] > self.TEMPERATURE_MAX:

            alerts.append({
                "alert_type": "Telemetry Anomaly",
                "severity": self.classify_severity(
                    "Telemetry Anomaly"
                ),
                "description":
                    f"Abnormal temperature detected: "
                    f"{telemetry['temperature']}"
            })

        if telemetry["pressure"] < self.PRESSURE_MIN:

            alerts.append({
                "alert_type": "Telemetry Anomaly",
                "severity": self.classify_severity(
                    "Telemetry Anomaly"
                ),
                "description":
                    f"Abnormal pressure detected: "
                    f"{telemetry['pressure']}"
            })

        if telemetry["rpm"] > self.RPM_MAX:

            alerts.append({
                "alert_type": "Telemetry Anomaly",
                "severity": self.classify_severity(
                    "Telemetry Anomaly"
                ),
                "description":
                    f"Abnormal RPM detected: "
                    f"{telemetry['rpm']}"
            })

        return alerts

    # =====================================================
    # HISTORY MANAGEMENT
    # =====================================================

    def update_history(self, telemetry):

        self.telemetry_history["temperature"].append(
            telemetry["temperature"]
        )

        self.telemetry_history["pressure"].append(
            telemetry["pressure"]
        )

        self.telemetry_history["rpm"].append(
            telemetry["rpm"]
        )

        for key in self.telemetry_history:

            if len(self.telemetry_history[key]) > self.MAX_HISTORY:

                self.telemetry_history[key].pop(0)

    # =====================================================
    # BEHAVIORAL DETECTION
    # =====================================================

    def behavioral_detection(self, telemetry):

        alerts = []

        self.update_history(
            telemetry
        )

        if len(
            self.telemetry_history["temperature"]
        ) < 5:

            return alerts

        temp_avg = statistics.mean(
            self.telemetry_history["temperature"]
        )

        pressure_avg = statistics.mean(
            self.telemetry_history["pressure"]
        )

        rpm_avg = statistics.mean(
            self.telemetry_history["rpm"]
        )

        if abs(
            telemetry["temperature"] - temp_avg
        ) > self.TEMP_DEVIATION_THRESHOLD:

            alerts.append({
                "alert_type": "Telemetry Anomaly",
                "severity": "HIGH",
                "description":
                    f"Temperature deviation detected. "
                    f"Current={telemetry['temperature']} "
                    f"Average={round(temp_avg,2)}"
            })

        if abs(
            telemetry["pressure"] - pressure_avg
        ) > self.PRESSURE_DEVIATION_THRESHOLD:

            alerts.append({
                "alert_type": "Telemetry Anomaly",
                "severity": "HIGH",
                "description":
                    f"Pressure deviation detected. "
                    f"Current={telemetry['pressure']} "
                    f"Average={round(pressure_avg,2)}"
            })

        if abs(
            telemetry["rpm"] - rpm_avg
        ) > self.RPM_DEVIATION_THRESHOLD:

            alerts.append({
                "alert_type": "Telemetry Anomaly",
                "severity": "HIGH",
                "description":
                    f"RPM deviation detected. "
                    f"Current={telemetry['rpm']} "
                    f"Average={round(rpm_avg,2)}"
            })

        return alerts

    # =====================================================
    # MAIN ANALYSIS PIPELINE
    # =====================================================

    def analyze(self, telemetry):

        self.stats["total_packets"] += 1

        alerts = []

        alerts.extend(
            self.threshold_detection(
                telemetry
            )
        )

        alerts.extend(
            self.behavioral_detection(
                telemetry
            )
        )

        self.stats["alerts_generated"] += len(
            alerts
        )

        for alert in alerts:
            self.log_alert(alert)

        return alerts

    # =====================================================
    # DASHBOARD METRICS
    # =====================================================

    def get_stats(self):

        return self.stats


# =====================================================
# TESTING
# =====================================================

if __name__ == "__main__":

    detector = AnomalyDetector()

    sample_packet = {
        "temperature": 120,
        "pressure": 10,
        "rpm": 7000
    }

    alerts = detector.analyze(
        sample_packet
    )

    print("\nAlerts Generated:\n")

    for alert in alerts:
        print(alert)

    print("\nStatistics:\n")

    print(
        detector.get_stats()
    )