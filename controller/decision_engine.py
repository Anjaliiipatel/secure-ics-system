import logging

# Configure alerting mechanism
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DecisionEngine")

def trigger_alert(metric_name, value, threshold):
    """Action to take when threshold is exceeded."""
    logger.warning(f"ALERT: {metric_name} value {value} exceeded threshold of {threshold}!")

class DecisionEngine:
    def __init__(self, thresholds):
        self.thresholds = thresholds
    
    def process_telemetry(self, telemetry_data):
        """Processes incoming data and triggers rules."""
        temperature = telemetry_data.get("temperature")

        if temperature and temperature > self.thresholds['temp_max']:
            trigger_alert("Temperature", temperature, self.thresholds['temp_max'])

if __name__ == "__main__":
    config = {'temp_max': 90}
    engine = DecisionEngine(config)

    #Simulated telemetry data
    data = {'temperature': 92, 'location': 'cabinet_1'}

    #Process
    engine.process_telemetry(data)