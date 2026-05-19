class DecisionEngine:
    def __init__(self, monitor_ref):
        self.monitor = monitor_ref

    def process_telemetry(self, sensor_id, data_type, value, anomaly_alerts):
        """
        Coordinates between security alerts and physical safety.
        """
        # 1. Immediate Operational Response
        if data_type == "temperature" and value > 95:
            self._execute_safety_protocol("COOLING_INIT", sensor_id)

        if data_type == "pressure" and value < 20:
            self._execute_safety_protocol("EMERGENCY_SHUTDOWN", sensor_id)

        # 2. Security-Based Response
        for alert in anomaly_alerts:
            self.monitor.log_event(alert) # Send to monitoring
            
            if alert['severity'] == 'CRITICAL':
                self._isolate_sensor(alert['sensor_id'])

    def _execute_safety_protocol(self, action, target):
        print(f"[CONTROL] {action} triggered for {target}!")

    def _isolate_sensor(self, sensor_id):
        print(f"[SECURITY] Isolating compromised sensor: {sensor_id}")
