import hashlib
import hmac
import json
import time


class TelemetryValidator:

    REQUIRED_FIELDS = [
        "sensor_id",
        "temperature",
        "pressure",
        "rpm",
        "timestamp"
    ]

    MAX_PACKET_AGE = 30

    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode("utf-8")

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

    def validate_signature(
        self,
        payload: dict,
        received_signature: str
    ):

        computed_signature = self.generate_signature(
            payload
        )

        if not hmac.compare_digest(
            computed_signature,
            received_signature
        ):
            return False, "Telemetry signature mismatch"

        return True, "Signature validated"

    def validate_schema(self, payload: dict):

        for field in self.REQUIRED_FIELDS:
            if field not in payload:
                return False, f"Missing required field: {field}"

        return True, "Schema validation passed"

    def validate_data_types(self, payload: dict):

        if not isinstance(payload["sensor_id"], str):
            return False, "sensor_id must be a string"

        numeric_fields = [
            "temperature",
            "pressure",
            "rpm",
            "timestamp"
        ]

        for field in numeric_fields:
            if not isinstance(payload[field], (int, float)):
                return False, f"{field} must be numeric"

        return True, "Data type validation passed"

    def validate_timestamp(self, payload: dict):

        packet_time = payload["timestamp"]
        current_time = time.time()

        if abs(current_time - packet_time) > self.MAX_PACKET_AGE:
            return False, "Telemetry packet expired"

        return True, "Timestamp validation passed"

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

        type_ok, type_msg = self.validate_data_types(
            payload
        )

        if not type_ok:
            return False, type_msg

        timestamp_ok, timestamp_msg = self.validate_timestamp(
            payload
        )

        if not timestamp_ok:
            return False, timestamp_msg

        signature_ok, signature_msg = self.validate_signature(
            payload,
            received_signature
        )

        if not signature_ok:
            return False, signature_msg

        return True, "Telemetry packet validated successfully"


if __name__ == "__main__":

    validator = TelemetryValidator(
        "super_secret_aerospace_key"
    )

    telemetry_data = {
        "sensor_id": "temp_01",
        "temperature": 72,
        "pressure": 410,
        "rpm": 1500,
        "timestamp": time.time()
    }

    signature = validator.generate_signature(
        telemetry_data
    )

    valid, message = validator.validate_packet(
        telemetry_data,
        signature
    )

    print(f"Validation Result: {valid}")
    print(f"Message: {message}")