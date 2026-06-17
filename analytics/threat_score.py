from analytics.security_analytics import SecurityAnalytics


class ThreatScore:

    THREAT_WEIGHTS = {

        "Replay Attack": 10,

        "Integrity Failure": 25,

        "Unauthorized Sensor": 15,

        "Telemetry Anomaly": 5
    }

    def __init__(self):

        self.analytics = SecurityAnalytics()

    # ==========================================
    # CALCULATE SCORE
    # ==========================================

    def calculate_score(self):

        attacks = (
            self.analytics.get_attack_counts()
        )

        score = 0

        for attack_type, count in attacks.items():

            weight = self.THREAT_WEIGHTS.get(
                attack_type,
                0
            )

            score += (
                weight * count
            )

        return min(
            score,
            100
        )

    # ==========================================
    # THREAT LEVEL
    # ==========================================

    def get_threat_level(self):

        score = self.calculate_score()

        if score >= 75:

            return "CRITICAL"

        elif score >= 50:

            return "HIGH"

        elif score >= 25:

            return "MEDIUM"

        return "LOW"

    # ==========================================
    # DASHBOARD DATA
    # ==========================================

    def get_dashboard_data(self):

        return {

            "score":
            self.calculate_score(),

            "level":
            self.get_threat_level()
        }


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    threat = ThreatScore()

    print(
        threat.get_dashboard_data()
    )