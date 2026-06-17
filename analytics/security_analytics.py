from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parents[1]

LOG_FILE = (
    BASE_DIR /
    "logs" /
    "system_logs.txt"
)


class SecurityAnalytics:

    def __init__(self):

        self.log_file = LOG_FILE

    # ==========================================
    # LOAD LOG FILE
    # ==========================================

    def load_logs(self):

        if not self.log_file.exists():

            return []

        with open(
            self.log_file,
            "r"
        ) as file:

            return file.readlines()

    # ==========================================
    # ATTACK COUNTS
    # ==========================================

    def get_attack_counts(self):

        logs = self.load_logs()

        attack_counter = Counter()

        for log in logs:

            if "Replay Attack" in log:

                attack_counter[
                    "Replay Attack"
                ] += 1

            elif "Integrity Failure" in log:

                attack_counter[
                    "Integrity Failure"
                ] += 1

            elif "Unauthorized Sensor" in log:

                attack_counter[
                    "Unauthorized Sensor"
                ] += 1

            elif "Telemetry Anomaly" in log:

                attack_counter[
                    "Telemetry Anomaly"
                ] += 1

        return dict(
            attack_counter
        )

    # ==========================================
    # TOTAL EVENTS
    # ==========================================

    def get_total_events(self):

        return len(
            self.load_logs()
        )

    # ==========================================
    # TOTAL ATTACKS
    # ==========================================

    def get_total_attacks(self):

        counts = self.get_attack_counts()

        return sum(
            counts.values()
        )

    # ==========================================
    # DASHBOARD SUMMARY
    # ==========================================

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
                0
            ),

            "integrity_failures":
            attacks.get(
                "Integrity Failure",
                0
            ),

            "unauthorized_sensors":
            attacks.get(
                "Unauthorized Sensor",
                0
            ),

            "anomalies":
            attacks.get(
                "Telemetry Anomaly",
                0
            )
        }

    # ==========================================
    # ATTACK PERCENTAGES
    # ==========================================

    def get_attack_percentages(self):

        counts = self.get_attack_counts()

        total = self.get_total_attacks()

        if total == 0:

            return {}

        percentages = {}

        for attack_type, count in counts.items():

            percentages[
                attack_type
            ] = round(
                (count / total) * 100,
                2
            )

        return percentages


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    analytics = SecurityAnalytics()

    print(
        "\n=== DASHBOARD SUMMARY ===\n"
    )

    print(
        analytics.get_dashboard_summary()
    )

    print(
        "\n=== ATTACK DISTRIBUTION ===\n"
    )

    print(
        analytics.get_attack_percentages()
    )
    