from pathlib import Path
from datetime import datetime
import time

from security.validator import TelemetryValidator
from security.replay_detector import ReplayDetector
from security.anomaly_detector import AnomalyDetector


BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "system_logs.txt"


class SecurityGateway:

    def __init__(self):

        # Security Components

        self.validator = TelemetryValidator(
            "super_secret_aerospace_key"
        )

        self.replay_detector = ReplayDetector()

        self.anomaly_detector = AnomalyDetector()

        # Gateway Statistics

        self.stats = {
            "packets_received": 0,
            "packets_accepted": 0,
            "packets_rejected": 0,
            "replay_attacks_blocked": 0,
            "integrity_failures": 0,
            "anomalies_detected": 0
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
        # Validate packet
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

        # ---------------------------------------------
        # STEP 2
        # Replay Detection
        # ---------------------------------------------

        replay, replay_message = (
            self.replay_detector.is_replay(
                packet["timestamp"]
            )
        )

        if replay:

            self.stats[
                "replay_attacks_blocked"
            ] += 1

            self.stats[
                "packets_rejected"
            ] += 1

            self.log_event(
                "HIGH",
                "Replay Attack",
                replay_message
            )

            return {
                "status": "REJECTED",
                "reason": replay_message
            }

        # ---------------------------------------------
        # STEP 3
        # Anomaly Detection
        # ---------------------------------------------

        telemetry = {
            "temperature": packet.get(
                "temperature",
                packet.get("value", 0)
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

            self.stats[
                "anomalies_detected"
            ] += len(alerts)

        # ---------------------------------------------
        # STEP 4
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
# TESTING
# =====================================================

if __name__ == "__main__":

    gateway = SecurityGateway()

    packet = {
        "sensor_id": "temp_01",
        "value": 72,
        "temperature": 72,
        "pressure": 410,
        "rpm": 1500,
        "timestamp": time.time()
    }

    signature = gateway.validator.generate_signature(
        packet
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