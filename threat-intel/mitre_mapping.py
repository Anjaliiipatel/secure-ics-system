class MitreMapper:

    MITRE_MAP = {
        "Replay Attack": {
            "technique_id": "T1557",
            "technique": "Adversary-in-the-Middle",
            "tactic": "Credential Access / Collection",
            "description": "Replay activity may indicate interception or reuse of captured telemetry traffic."
        },

        "Integrity Failure": {
            "technique_id": "T1565",
            "technique": "Data Manipulation",
            "tactic": "Impact",
            "description": "Telemetry tampering aligns with manipulation of transmitted operational data."
        },

        "Unauthorized Sensor": {
            "technique_id": "T1036",
            "technique": "Masquerading",
            "tactic": "Defense Evasion",
            "description": "Unauthorized devices may attempt to appear as trusted industrial assets."
        },

        "Telemetry Anomaly": {
            "technique_id": "T0831",
            "technique": "Manipulation of Control",
            "tactic": "Impair Process Control",
            "description": "Abnormal telemetry may indicate attempted manipulation of industrial process values."
        },

        "Flood Attack": {
            "technique_id": "T1499",
            "technique": "Endpoint Denial of Service",
            "tactic": "Impact",
            "description": "High-volume telemetry activity may indicate an availability-focused attack."
        }
    }

    def get_mapping(self, event_type):
        return self.MITRE_MAP.get(
            event_type,
            {
                "technique_id": "N/A",
                "technique": "Unmapped",
                "tactic": "Unknown",
                "description": "No MITRE ATT&CK mapping available."
            }
        )

    def get_all_mappings(self):
        return self.MITRE_MAP

    def get_detected_mappings(self, attack_counts):
        detected = []

        for attack_type, count in attack_counts.items():
            if count > 0:
                mapping = self.get_mapping(attack_type)
                detected.append({
                    "event_type": attack_type,
                    "count": count,
                    **mapping
                })

        return detected


if __name__ == "__main__":
    mapper = MitreMapper()

    sample_counts = {
        "Replay Attack": 2,
        "Integrity Failure": 1,
        "Unauthorized Sensor": 3
    }

    print(mapper.get_detected_mappings(sample_counts))