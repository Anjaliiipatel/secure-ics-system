import time
import statistics
from collections import deque

class AnomalyDetectionEngine:
    def __init__(self):
        self.LIMITS = {
            # Static thresholds
            "temperature": {"max": 95},
            "rpm": {"max": 5000},
            "pressure": {"min": 20}
        }
        # stores last 10 readings per sensor ID
        self.history= {}

        # rate-based tracking
        self.request_timestamps = deque(maxlen=100)
        self.FLOOD_THRESHOLD = 20

    def analyze(self, sensor_id, data_type, value):
        alerts = []
        now = time.time()

        # detection type 1: thresholds
        limit = self.LIMITS.get(data_type, {})
        if "max" in limit and value > limit["max"]:
            alerts.append(self._generate_alert("Threshold Breach", "HIGH", sensor_id, f"Extreme {data_type}"))
        
        # detection type 2: behavioral anomalies
        if sensor_id not in self.history:
            self.history[sensor_id] = deque(maxlen=10)
        
        if len(self.history[sensor_id]) == 10:
            avg = statistics.mean(self.history[sensor_id])
            if abs(value - avg) > (avg * 0.4):
                alerts.append(self._generate_alert("Behavioral Anomaly", "MEDIUM", sensor_id, f"{data_type} Suddent telemetry spike"))

        self.history[sensor_id].append(value)

        # detection type 3: rate-based anomalies
        self.request_timestamps.append(now)
        if len(self.request_timestamps) > 1:
            timespan = now - self.request_timestamps[0]
            if timespan > 0 and (len(self.request_timestamps) / timespan) > self.FLOOD_THRESHOLD:
                alerts.append(self._generate_alert())
        return alerts
    
    def _generate_alert(self, alert_type, severity, sensor_id, description):
        return {
            "alert_type": alert_type,
            "severity": severity,
            "sensor_id": sensor_id,
            "description": description,
            "timestamp": time.time()
        }

engine = AnomalyDetectionEngine()

for _ in range(10): engine.analyze("TEMP_01", "temperature", 72)

print(engine.analyze("TEMP_01", "temperature", 135)) 