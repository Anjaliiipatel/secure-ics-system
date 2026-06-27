import json
from pathlib import Path
from datetime import datetime

from analytics.threat_score import ThreatScore


BASE_DIR = Path(__file__).resolve().parents[1]

THREAT_HISTORY_FILE = (
    BASE_DIR /
    "logs" /
    "threat_history.json"
)


class ThreatTrendTracker:

    def __init__(self):
        self.threat_engine = ThreatScore()
        self.history_file = THREAT_HISTORY_FILE

    def load_history(self):
        if not self.history_file.exists():
            return []

        with open(self.history_file, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def save_history(self, history):
        self.history_file.parent.mkdir(exist_ok=True)

        with open(self.history_file, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4)

    def record_snapshot(self):
        threat_data = self.threat_engine.get_dashboard_data()

        snapshot = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "score": threat_data.get("score", 0),
            "level": threat_data.get("level", "LOW")
        }

        history = self.load_history()

        history.append(snapshot)

        history = history[-100:]

        self.save_history(history)

        return snapshot

    def get_history(self):
        return self.load_history()


if __name__ == "__main__":
    tracker = ThreatTrendTracker()

    snapshot = tracker.record_snapshot()

    print("Threat snapshot recorded:")
    print(snapshot)