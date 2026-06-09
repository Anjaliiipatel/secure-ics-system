import requests
import random
import time

API_URL = "http://127.0.0.1:5000/telemetry"

while True:

    packet = {
        "sensor_id": "temp_01",
        "temperature": random.randint(65, 90),
        "pressure": random.randint(380, 450),
        "rpm": random.randint(1200, 1800),
        "timestamp": int(time.time())
    }

    try:

        response = requests.post(
            API_URL,
            json=packet
        )

        print(
            f"Status: {response.status_code}"
        )

        print(
            response.json()
        )

    except Exception as e:

        print(
            f"Connection Error: {e}"
        )

    time.sleep(2)