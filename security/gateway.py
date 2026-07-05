from pathlib import Path
from datetime import datetime
import time

from security.validation import TelemetryValidator
from security.replay_detection import ReplayDetector
from security.anomaly_detection import AnomalyDetector
from security.sensor_registry import SensorRegistry
from incidents.incident_manager import IncidentManager
from threat_hunting.ioc_engine import IOCEngine
from rules.detection_rules import DetectionRules


BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "system_logs.txt"


class SecurityGateway:

    def __init__(self):

        # =============================================
        # Security Components
        # =============================================

        self.validator = TelemetryValidator(
            "super_secret_aerospace_key"
        )

        self.replay_detector = ReplayDetector()

        self.anomaly_detector = AnomalyDetector()

        self.sensor_registry = SensorRegistry()

        self.incident_manager = IncidentManager()

        self.ioc_engine = IOCEngine()

        self.detection_rules = DetectionRules()

        # =============================================
        # Gateway Statistics
        # =============================================

        self.stats = {
            "packets_received": 0,
            "packets_accepted": 0,
            "packets_rejected": 0,
            "replay_attacks_blocked": 0,
            "integrity_failures": 0,
            "anomalies_detected": 0,
            "unauthorized_sensors_blocked": 0
        }

    # =====================================================
    # LOGGING
    # =====================================================

    def log_event(
        self,
        severity,
        event_type,
        description
    ):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(LOG_FILE, "a") as log_file:

            log_file.write(
                f"{timestamp} | "
                f"{severity} | "
                f"{event_type} | "
                f"{description}\n"
            )

    # =====================================================
    # PROCESS TELEMETRY
    # =====================================================

    def process_packet(
        self,
        packet,
        signature
    ):

        self.stats["packets_received"] += 1

        # ---------------------------------------------
        # STEP 1
        # Signature & Packet Validation
        # ---------------------------------------------

        valid, message = self.validator.validate_packet(
            packet,
            signature
        )

        if not valid:

            self.stats["packets_rejected"] += 1
            self.stats["integrity_failures"] += 1

            self.log_event(
                "CRITICAL",
                "Integrity Failure",
                message
            )
            
            return {
                "status": "REJECTED",
                "reason": message
            }
            self.incident_manager.create_incident(
                "Integrity Failure",
                "CRITICAL"
            )
        # ---------------------------------------------
        # STEP 2
        # Sensor Authentication
        # ---------------------------------------------
        authorized = self.sensor_registry.is_authorized(
            packet["sensor_id"]
        )

        if not authorized:
            self.stats["packets_rejected"] += 1
            self.stats["authentication_failures"] += 1

            self.log_event(
                "CRITICAL",
                "Authentication Failure",
                f"Unauthorized sensor: {packet['sensor_id']}"
            )

            return {
                "status": "REJECTED",
                "reason": f"Unauthorized sensor: {packet['sensor_id']}"
            }
            self.incident_manager.create_incident(
                "Authentication Failure",
                "CRITICAL"
            )
            self.ioc_engine.create_ioc(
                "Authentication Failure",
                "CRITICAL",
                source=packet.get("sensor_id", "unknown"),
                description="Telemetry packet failed authentication validation."
            )
            self.ioc_engine.create_ioc(
                "Unauthorized Sensor",
                "HIGH",
                source=packet.get("sensor_id", "unknown"),
                description="Unauthorized device attempted to send telemetry."
            )

        # ---------------------------------------------
        # STEP 4
        # Anomaly Detection
        # ---------------------------------------------

        telemetry = {

            "temperature": packet.get(
                "temperature",
                0
            ),

            "pressure": packet.get(
                "pressure",
                0
            ),

            "rpm": packet.get(
                "rpm",
                0
            )
        }

        alerts = self.anomaly_detector.analyze(
            telemetry
        )

        if alerts:
            self.ioc_engine.create_ioc(
                "Telemetry Anomaly",
                "MEDIUM",
                source=packet.get("sensor_id", "unknown"),
                description="Abnormal telemetry behavior detected."
        )
            self.stats[
                "anomalies_detected"
            ] += len(alerts)

            for alert in alerts:

                self.log_event(
                    alert["severity"],
                    alert["alert_type"],
                    alert["description"]
                )

        # ---------------------------------------------
        # STEP 5
        # Accept Packet
        # ---------------------------------------------

        self.stats[
            "packets_accepted"
        ] += 1

        self.log_event(
            "INFO",
            "Telemetry Accepted",
            "Telemetry packet passed all security checks"
        )

        return {

            "status": "ACCEPTED",

            "alerts": alerts,

            "packet": packet
        }

    # =====================================================
    # DASHBOARD METRICS
    # =====================================================

    def get_stats(self):

        return self.stats

    # =====================================================
    # RESET STATS
    # =====================================================

    def reset_stats(self):

        self.stats = {

            "packets_received": 0,
            "packets_accepted": 0,
            "packets_rejected": 0,
            "replay_attacks_blocked": 0,
            "integrity_failures": 0,
            "anomalies_detected": 0,
            "unauthorized_sensors_blocked": 0
        }


# =====================================================
# TESTING
# =====================================================

if __name__ == "__main__":

    gateway = SecurityGateway()

    packet = {

        "sensor_id": "temp_01",

        "temperature": 72,

        "pressure": 410,

        "rpm": 1500,

        "timestamp": time.time()
    }

    signature = (
        gateway.validator.generate_signature(
            packet
        )
    )

    result = gateway.process_packet(
        packet,
        signature
    )

    print("\nGateway Result:\n")

    print(result)

    print("\nGateway Statistics:\n")

    print(
        gateway.get_stats()
    )

