import time
import requests

from security.validation import TelemetryValidator

validator = TelemetryValidator(
    "super_secret_aerospace_key"
)

packet = {
    "sensor_id": "temp_01",
    "temperature": 72,
    "pressure": 410,
    "rpm": 1500,
    "timestamp": time.time()
}

signature = validator.generate_signature(
    packet
)

packet["signature"] = signature

#send original packet
requests.post(
    "http://localhost:5000/telemetry", 
    json=packet
)

#replay some packet
for _ in range(3):
    response = requests.post(
        "http://127.0.0.1:5000/telemetry",
        json=packet
    )

    print(response.status_code)
    print(response.json())
