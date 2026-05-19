import json
import time
from datetime import datetime

class MonitoringSystem:
    def __init__(self):
        self.security_logs = []

    def log_event(self, alert_object):
        """Formats and stores alerts for the future dashboard"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_id": hash(f"{alert_object['sensor_id']}_{time.time()}"), 
            "data": alert_object
        }
        self.security_logs.append(event)

        # real system, you'd write to a JSON file or DB
        print(f" [MONITOR] Registered {event['data']['severity']} alert: {event['data']['alert_type']}")

    def get_summary(self):
        """Quick summary for Week 4 prep."""
        return {
            "total_alerts": len(self.security_logs),
            "critical_count": len([1 for 1 in self.security_logs if 1['data']['severity'] == 'CRITICAL'])
        }