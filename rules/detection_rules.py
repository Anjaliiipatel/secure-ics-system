class DetectionRules:

    def __init__(self):
        self.rule_hits = {
            "replay_rule": 0,
            "integrity_rule": 0,
            "unauthorized_sensor_rule": 0,
            "anomaly_rule": 0,
            "flood_rule": 0
        }

    def evaluate_replay(self, is_replay):
        if is_replay:
            self.rule_hits["replay_rule"] += 1

            return {
                "triggered": True,
                "rule": "Replay Detection Rule",
                "severity": "HIGH",
                "description": "Replay behavior detected from telemetry packet."
            }

        return {
            "triggered": False
        }

    def evaluate_integrity(self, is_valid):
        if not is_valid:
            self.rule_hits["integrity_rule"] += 1

            return {
                "triggered": True,
                "rule": "Integrity Validation Rule",
                "severity": "CRITICAL",
                "description": "Telemetry integrity validation failed."
            }

        return {
            "triggered": False
        }

    def evaluate_sensor_authorization(self, is_authorized):
        if not is_authorized:
            self.rule_hits["unauthorized_sensor_rule"] += 1

            return {
                "triggered": True,
                "rule": "Unauthorized Sensor Rule",
                "severity": "HIGH",
                "description": "Unauthorized sensor attempted to transmit telemetry."
            }

        return {
            "triggered": False
        }

    def evaluate_anomalies(self, alerts):
        if alerts:
            self.rule_hits["anomaly_rule"] += len(alerts)

            return {
                "triggered": True,
                "rule": "Telemetry Anomaly Rule",
                "severity": "MEDIUM",
                "description": "Telemetry anomaly detected from sensor values.",
                "alerts": alerts
            }

        return {
            "triggered": False
        }

    def evaluate_flood(self, packet_count, threshold=50):
        if packet_count > threshold:
            self.rule_hits["flood_rule"] += 1

            return {
                "triggered": True,
                "rule": "Flood Detection Rule",
                "severity": "CRITICAL",
                "description": "High-volume telemetry activity detected."
            }

        return {
            "triggered": False
        }

    def get_rule_statistics(self):
        return self.rule_hits


if __name__ == "__main__":
    rules = DetectionRules()

    print(rules.evaluate_replay(True))
    print(rules.evaluate_integrity(False))
    print(rules.evaluate_sensor_authorization(False))
    print(rules.evaluate_anomalies(["Temperature anomaly detected"]))
    print(rules.evaluate_flood(75))

    print("\nRule Statistics:")
    print(rules.get_rule_statistics())