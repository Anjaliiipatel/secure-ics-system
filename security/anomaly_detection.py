import statistics
import time

# Store recent telemetry history
telemetry_history = {
    "temperature": [],
    "pressure": [],
    "rpm": []
}

# Maximum history length
MAX_HISTORY = 20


def log_alert(alert):
    """
    Write alert to centralized log file.
    """

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    with open("../logs/system_logs.txt", "a") as log_file:
        log_file.write(
            f"{timestamp} | "
            f"{alert['severity']} | "
            f"{alert['alert_type']} | "
            f"{alert['description']}\n"
        )


def classify_severity(alert_type):
    """
    Assign severity classification.
    """

    severity_map = {
        "Telemetry Anomaly": "HIGH",
        "Replay Attack": "HIGH",
        "Flooding Attack": "CRITICAL",
        "Integrity Failure": "CRITICAL",
        "Authentication Failure": "MEDIUM"
    }

    return severity_map.get(alert_type, "LOW")


def threshold_detection(telemetry):
    """
    Detect impossible or dangerous telemetry values.
    """

    alerts = []

    if telemetry["temperature"] > 95:
        alerts.append({
            "alert_type": "Telemetry Anomaly",
            "severity": classify_severity("Telemetry Anomaly"),
            "description": (
                f"Abnormal temperature detected: "
                f"{telemetry['temperature']}"
            )
        })

    if telemetry["pressure"] < 20:
        alerts.append({
            "alert_type": "Telemetry Anomaly",
            "severity": classify_severity("Telemetry Anomaly"),
            "description": (
                f"Abnormal pressure detected: "
                f"{telemetry['pressure']}"
            )
        })

    if telemetry["rpm"] > 5000:
        alerts.append({
            "alert_type": "Telemetry Anomaly",
            "severity": classify_severity("Telemetry Anomaly"),
            "description": (
                f"Abnormal RPM detected: "
                f"{telemetry['rpm']}"
            )
        })

    return alerts


def behavioral_detection(telemetry):
    """
    Compare telemetry against recent operational history.
    """

    alerts = []

    # Add telemetry to history
    telemetry_history["temperature"].append(telemetry["temperature"])
    telemetry_history["pressure"].append(telemetry["pressure"])
    telemetry_history["rpm"].append(telemetry["rpm"])

    # Limit history size
    for key in telemetry_history:
        if len(telemetry_history[key]) > MAX_HISTORY:
            telemetry_history[key].pop(0)

    # Only analyze if enough history exists
    if len(telemetry_history["temperature"]) < 5:
        return alerts

    temp_avg = statistics.mean(telemetry_history["temperature"])
    pressure_avg = statistics.mean(telemetry_history["pressure"])
    rpm_avg = statistics.mean(telemetry_history["rpm"])

    # Temperature deviation
    if abs(telemetry["temperature"] - temp_avg) > 20:
        alerts.append({
            "alert_type": "Telemetry Anomaly",
            "severity": "HIGH",
            "description": (
                f"Behavioral temperature deviation detected. "
                f"Current: {telemetry['temperature']} | "
                f"Average: {round(temp_avg, 2)}"
            )
        })

    # Pressure deviation
    if abs(telemetry["pressure"] - pressure_avg) > 10:
        alerts.append({
            "alert_type": "Telemetry Anomaly",
            "severity": "HIGH",
            "description": (
                f"Behavioral pressure deviation detected. "
                f"Current: {telemetry['pressure']} | "
                f"Average: {round(pressure_avg, 2)}"
            )
        })

    # RPM deviation
    if abs(telemetry["rpm"] - rpm_avg) > 2000:
        alerts.append({
            "alert_type": "Telemetry Anomaly",
            "severity": "HIGH",
            "description": (
                f"Behavioral RPM deviation detected. "
                f"Current: {telemetry['rpm']} | "
                f"Average: {round(rpm_avg, 2)}"
            )
        })

    return alerts


def analyze_telemetry(telemetry):
    """
    Run all telemetry detection checks.
    """

    alerts = []

    alerts.extend(threshold_detection(telemetry))
    alerts.extend(behavioral_detection(telemetry))

    # Log alerts
    for alert in alerts:
        log_alert(alert)

    return alerts