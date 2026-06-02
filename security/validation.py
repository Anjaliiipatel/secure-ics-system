import hashlib
import hmac
import json
import time


class TelemetryValidator:

    AUTHORIZED_SENSORS = [
        "temp_01",
        "temp_02",
        "pressure_01",
        "rpm_01"
    ]

    REQUIRED_FIELDS = [
        "sensor_id",
        "value",
        "timestamp"
    ]

    MAX_PACKET_AGE = 30  # seconds

    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode("utf-8")

    # =====================================================
    # HMAC SIGNATURE GENERATION
    # =====================================================

    def generate_signature(self, payload: dict) -> str:

        payload_bytes = json.dumps(
            payload,
            sort_keys=True
        ).encode("utf-8")

        signature = hmac.new(
            self.secret_key,
            payload_bytes,
            hashlib.sha256
        ).hexdigest()

        return signature

    # =====================================================
    # SIGNATURE VALIDATION
    # =====================================================

    def validate_signature(
        self,
        payload: dict,
        received_signature: str
    ) -> bool:

        computed_signature = self.generate_signature(
            payload
        )

        return hmac.compare_digest(
            computed_signature,
            received_signature
        )

    # =====================================================
    # REQUIRED FIELD VALIDATION
    # =====================================================

    def validate_schema(self, payload: dict):

        for field in self.REQUIRED_FIELDS:

            if field not in payload:

                return (
                    False,
                    f"Missing required field: {field}"
                )

        return (
            True,
            "Schema validation passed"
        )

    # =====================================================
    # SENSOR AUTHENTICATION
    # =====================================================

    def validate_sensor(self, payload: dict):

        sensor_id = payload["sensor_id"]

        if sensor_id not in self.AUTHORIZED_SENSORS:

            return (
                False,
                f"Unauthorized sensor: {sensor_id}"
            )

        return (
            True,
            "Sensor authentication passed"
        )

    # =====================================================
    # TIMESTAMP VALIDATION
    # =====================================================

    def validate_timestamp(self, payload: dict):

        packet_time = payload["timestamp"]

        current_time = time.time()

        if abs(current_time - packet_time) > self.MAX_PACKET_AGE:

            return (
                False,
                "Telemetry packet expired"
            )

        return (
            True,
            "Timestamp validation passed"
        )

    # =====================================================
    # FULL TELEMETRY VALIDATION
    # =====================================================

    def validate_packet(
        self,
        payload: dict,
        received_signature: str
    ):

        schema_ok, schema_msg = self.validate_schema(
            payload
        )

        if not schema_ok:
            return False, schema_msg

        sensor_ok, sensor_msg = self.validate_sensor(
            payload
        )

        if not sensor_ok:
            return False, sensor_msg

        timestamp_ok, timestamp_msg = self.validate_timestamp(
            payload
        )

        if not timestamp_ok:
            return False, timestamp_msg

        signature_ok = self.validate_signature(
            payload,
            received_signature
        )

        if not signature_ok:

            return (
                False,
                "Signature validation failed"
            )

        return (
            True,
            "Telemetry packet validated successfully"
        )


# =====================================================
# TESTING
# =====================================================

if __name__ == "__main__":

    validator = TelemetryValidator(
        "super_secret_aerospace_key"
    )

    telemetry_data = {
        "sensor_id": "temp_01",
        "value": 98.6,
        "timestamp": time.time()
    }

    signature = validator.generate_signature(
        telemetry_data
    )

    valid, message = validator.validate_packet(
        telemetry_data,
        signature
    )

    print(
        f"Validation Result: {valid}"
    )

    print(
        f"Message: {message}"
    )

    tampered_data = telemetry_data.copy()

    tampered_data["value"] = 500.0

    valid, message = validator.validate_packet(
        tampered_data,
        signature
    )

    print(
        f"Tampered Result: {valid}"
    )

    print(
        f"Message: {message}"
    )