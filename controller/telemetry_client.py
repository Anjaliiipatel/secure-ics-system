import random
import time
import requests

from security.validation import TelemetryValidator


# =====================================================
# CONFIGURATION
# =====================================================

API_URL = "http://127.0.0.1:5000/telemetry"

validator = TelemetryValidator(
    "super_secret_aerospace_key"
)

SENSOR_ID = "temp_01"


# =====================================================
# TELEMETRY GENERATION
# =====================================================

def generate_telemetry():

    return {

        "sensor_id": SENSOR_ID,

        "temperature": round(
            random.uniform(68, 85),
            2
        ),

        "pressure": round(
            random.uniform(390, 450),
            2
        ),

        "rpm": random.randint(
            1300,
            1700
        ),

        "timestamp": time.time()
    }


# =====================================================
# TRANSMIT TELEMETRY
# =====================================================

def send_packet():

    packet = generate_telemetry()

    signature = validator.generate_signature(
        packet
    )

    packet["signature"] = signature

    try:

        response = requests.post(
            API_URL,
            json=packet,
            timeout=5
        )

        print(
            f"[{response.status_code}] "
            f"{response.json()}"
        )

    except Exception as e:

        print(
            f"Connection Error: {e}"
        )


# =====================================================
# MAIN LOOP
# =====================================================

if __name__ == "__main__":

    print(
        "\nStarting Telemetry Client...\n"
    )

    while True:

        send_packet()

        time.sleep(0.5)