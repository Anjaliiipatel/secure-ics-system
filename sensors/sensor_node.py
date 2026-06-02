import json
import random
import time
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]

TELEMETRY_PATH = BASE_DIR / "logs" / "telemetry.json"

temperature = 72.0
pressure = 418.0
rpm = 1450

while True:

    temperature += random.uniform(-0.5, 0.5)
    pressure += random.uniform(-2, 2)
    rpm += random.randint(-15, 15)

    telemetry_point = {
        "timestamp": datetime.now().isoformat(),
        "temperature": round(temperature, 2),
        "pressure": round(pressure, 2),
        "rpm": rpm
    }

    try:

        with open(
            TELEMETRY_PATH,
            "r"
        ) as f:

            data = json.load(f)

    except:

        data = []

    data.append(telemetry_point)

    data = data[-100:]

    with open(
        TELEMETRY_PATH,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )

    time.sleep(1)