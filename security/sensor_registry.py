class SensorRegistry:

    def __init__(self):

        self.authorized_sensors = {

            "temp_01": {
                "type": "Temperature Sensor",
                "location": "Engine Bay",
                "status": "ACTIVE"
            },

            "pressure_01": {
                "type": "Pressure Sensor",
                "location": "Hydraulic System",
                "status": "ACTIVE"
            },

            "rpm_01": {
                "type": "RPM Sensor",
                "location": "Turbine Assembly",
                "status": "ACTIVE"
            },

            "gateway_01": {
                "type": "Industrial Gateway",
                "location": "DMZ",
                "status": "ACTIVE"
            }
        }

    # ==========================================
    # SENSOR VALIDATION
    # ==========================================

    def is_authorized(
        self,
        sensor_id
    ):

        return sensor_id in self.authorized_sensors

    # ==========================================
    # SENSOR DETAILS
    # ==========================================

    def get_sensor(
        self,
        sensor_id
    ):

        return self.authorized_sensors.get(
            sensor_id
        )

    # ==========================================
    # REGISTER SENSOR
    # ==========================================

    def register_sensor(
        self,
        sensor_id,
        sensor_type,
        location
    ):

        self.authorized_sensors[sensor_id] = {

            "type": sensor_type,
            "location": location,
            "status": "ACTIVE"
        }

    # ==========================================
    # REMOVE SENSOR
    # ==========================================

    def remove_sensor(
        self,
        sensor_id
    ):

        if sensor_id in self.authorized_sensors:

            del self.authorized_sensors[
                sensor_id
            ]

    # ==========================================
    # LIST SENSORS
    # ==========================================

    def list_sensors(self):

        return self.authorized_sensors