import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parents[1]

IOC_DATABASE_FILE = (
    BASE_DIR /
    "threat_hunting" /
    "ioc_database.json"
)


class IOCEngine:

    def __init__(self):
        self.database_file = IOC_DATABASE_FILE

    def load_iocs(self):
        if not self.database_file.exists():
            return []

        with open(self.database_file, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def save_iocs(self, iocs):
        self.database_file.parent.mkdir(exist_ok=True)

        with open(self.database_file, "w", encoding="utf-8") as file:
            json.dump(iocs, file, indent=4)

    def create_ioc(
        self,
        ioc_type,
        severity,
        source="unknown",
        description="Security indicator detected."
    ):
        iocs = self.load_iocs()

        ioc_id = f"IOC-{len(iocs) + 1:03d}"

        ioc = {
            "id": ioc_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": ioc_type,
            "severity": severity,
            "source": source,
            "status": "ACTIVE",
            "description": description
        }

        iocs.append(ioc)
        self.save_iocs(iocs)

        return ioc

    def get_active_iocs(self):
        return [
            ioc for ioc in self.load_iocs()
            if ioc.get("status") == "ACTIVE"
        ]

    def close_ioc(self, ioc_id):
        iocs = self.load_iocs()

        for ioc in iocs:
            if ioc.get("id") == ioc_id:
                ioc["status"] = "RESOLVED"

        self.save_iocs(iocs)

    def get_ioc_summary(self):
        active_iocs = self.get_active_iocs()

        return {
            "active_iocs": len(active_iocs),
            "critical_iocs": len([
                ioc for ioc in active_iocs
                if ioc.get("severity") == "CRITICAL"
            ]),
            "high_iocs": len([
                ioc for ioc in active_iocs
                if ioc.get("severity") == "HIGH"
            ]),
            "medium_iocs": len([
                ioc for ioc in active_iocs
                if ioc.get("severity") == "MEDIUM"
            ])
        }


if __name__ == "__main__":
    engine = IOCEngine()

    test_ioc = engine.create_ioc(
        "Replay Attack",
        "HIGH",
        source="temp_01",
        description="Replay attack indicator created during test."
    )

    print("Created IOC:")
    print(test_ioc)

    print("\nIOC Summary:")
    print(engine.get_ioc_summary())