import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parents[1]

INCIDENT_FILE = (
    BASE_DIR /
    "incidents" /
    "incidents.json"
)


class IncidentManager:

    def __init__(self):

        self.incident_file = INCIDENT_FILE

    # ==========================================
    # LOAD INCIDENTS
    # ==========================================

    def load_incidents(self):

        if not self.incident_file.exists():

            return []

        with open(
            self.incident_file,
            "r"
        ) as file:

            try:
                return json.load(file)

            except json.JSONDecodeError:

                return []

    # ==========================================
    # SAVE INCIDENTS
    # ==========================================

    def save_incidents(
        self,
        incidents
    ):

        with open(
            self.incident_file,
            "w"
        ) as file:

            json.dump(
                incidents,
                file,
                indent=4
            )

    # ==========================================
    # CREATE INCIDENT
    # ==========================================

    def create_incident(
        self,
        incident_type,
        severity
    ):

        incidents = self.load_incidents()

        incident_id = (
            f"INC-{len(incidents)+1:03d}"
        )

        incident = {

            "id":
            incident_id,

            "type":
            incident_type,

            "severity":
            severity,

            "status":
            "OPEN",

            "created":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        incidents.append(
            incident
        )

        self.save_incidents(
            incidents
        )

        return incident

    # ==========================================
    # CLOSE INCIDENT
    # ==========================================

    def close_incident(
        self,
        incident_id
    ):

        incidents = self.load_incidents()

        for incident in incidents:

            if incident["id"] == incident_id:

                incident[
                    "status"
                ] = "CLOSED"

        self.save_incidents(
            incidents
        )

    # ==========================================
    # OPEN INCIDENTS
    # ==========================================

    def get_open_incidents(self):

        incidents = self.load_incidents()

        return [

            incident

            for incident in incidents

            if incident["status"]
            == "OPEN"
        ]


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    manager = IncidentManager()

    manager.create_incident(
        "Replay Attack",
        "HIGH"
    )

    manager.create_incident(
        "Unauthorized Sensor",
        "MEDIUM"
    )

    print(
        manager.get_open_incidents()
    )