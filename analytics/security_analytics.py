from pathlib import Path
from collections import Counter

import attacks

BASE_DIR = Path(__file__).resolve().parents[1]

LOG_FILE = (
    BASE_DIR / "logs" / "security.log"
)

class SecurityAnalytics:
    def __init__(self):
        self.log_file = LOG_FILE

    #load logs
    def load_logs(self):
        if not self.log_file.exists():
            return []
        with open(self.log_file, "r") as file:
            return file.readlines()

    #attack counts
    def get_attack_counts(self):
        logs = self.load_logs()
        attack_counter = Counter()

        for log in logs:
            if "Replay Attack" in log:
                attack_counter["Replay Attack"] += 1
            elif "Integrity Failure" in log:
                attack_counter["Integrity Failure"] += 1
            elif "Unauthorized Sensor" in log:
                attack_counter["Telemetry Attack"] += 1

        return dict(attack_counter)
    #total events
    def get_total_events(self):
        return len(self.load_logs())
    
    #total attacks
    def get_total_attacks(self):
        counts = self.get_attack_counts()

        return sum(counts.values())
    
    #dashboard summary
    def get_dashboard_summary(self):
        attacks = self.get_attack_counts()
        return {
            "total_events":
            self.get_total_events(),

            "total_attacks": 
            self.get_total_attacks(),

            "replay_attacks":
            attacks.get(
                "Replay Attack", 
                0),
            
            "integrity_failures":
            attacks.get(
                "Integrity Failure",
                0),
            
            "unauthorized_sensors":
            attacks.get(
                "Unauthorized Sensor",
                0),
            
            "anomalies":
            attacks.get(
                "Telemetry Anomaly",
                0
            )
        }
# testing
if __name__ == "__main__":
    analytics = SecurityAnalytics()
    print(analytics.get_dashboard_summary())
        