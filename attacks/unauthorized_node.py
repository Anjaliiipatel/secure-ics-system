import requests
import time

from security.validation import TelemetryValidator


API_URL = "http://127.0.0.1:5000/telemetry"

validator = TelemetryValidator(
    "super_secret_aerospace_key"
)

packet = {

    "sensor_id": "hacker_device",

    "temperature": 72,

    "pressure": 410,

    "rpm": 1500,

    "timestamp": time.time()
}

signature = validator.generate_signature(
    packet
)

packet["signature"] = signature

response = requests.post(
    API_URL,
    json=packet
)

print(
    response.status_code
)

print(
    response.json()
)