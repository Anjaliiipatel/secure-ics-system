import requests
import time

from security.validation import TelemetryValidator


API_URL = "http://127.0.0.1:5000/telemetry"

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

# attacker modifies packet AFTER signing

packet["temperature"] = 500

packet["signature"] = signature

response = requests.post(
    API_URL,
    json=packet
)

print("\nTamper Attack Result:\n")

print(
    response.status_code
)

print(
    response.json()
)
    