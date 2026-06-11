import hashlib
import hmac
import json


class TelemetryValidator:

    REQUIRED_FIELDS = [
        "sensor_id",
        "temperature",
        "pressure",
        "rpm",
        "timestamp"
    ]

    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode("utf-8")

    # =====================================================
    # SIGNATURE GENERATION
    # =====================================================

    def generate_signature(
        self,
        payload: dict
    ) -> str:

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
    ):

        computed_signature = (
            self.generate_signature(payload)
        )

        valid = hmac.compare_digest(
            computed_signature,
            received_signature
        )

        if not valid:
            return (
                False,
                "Telemetry signature mismatch"
            )

        return (
            True,
            "Signature validated"
        )

    # =====================================================
    # FIELD VALIDATION
    # =====================================================

    def validate_required_fields(
        self,
        payload: dict
    ):

        for field in self.REQUIRED_FIELDS:

            if field not in payload:

                return (
                    False,
                    f"Missing field: {field}"
                )

        return (
            True,
            "Required fields present"
        )

    # =====================================================
    # DATA TYPE VALIDATION
    # =====================================================

    def validate_data_types(
        self,
        payload: dict
    ):

        if not isinstance(
            payload["sensor_id"],
            str
        ):
            return (
                False,
                "sensor_id must be string"
            )

        numeric_fields = [
            "temperature",
            "pressure",
            "rpm",
            "timestamp"
        ]

        for field in numeric_fields:

            if not isinstance(
                payload[field],
                (int, float)
            ):
                return (
                    False,
                    f"{field} must be numeric"
                )

        return (
            True,
            "Data types valid"
        )

    # =====================================================
    # SENSOR RANGE VALIDATION
    # =====================================================

    def validate_ranges(
        self,
        payload: dict
    ):

        if not (
            -50 <= payload["temperature"] <= 200
        ):
            return (
                False,
                "Temperature out of range"
            )

        if not (
            0 <= payload["pressure"] <= 1000
        ):
            return (
                False,
                "Pressure out of range"
            )

        if not (
            0 <= payload["rpm"] <= 10000
        ):
            return (
                False,
                "RPM out of range"
            )

        return (
            True,
            "Sensor values valid"
        )

    # =====================================================
    # COMPLETE PACKET VALIDATION
    # =====================================================

    def validate_packet(
        self,
        payload: dict,
        signature: str
    ):

        valid, message = (
            self.validate_required_fields(
                payload
            )
        )

        if not valid:
            return (
                False,
                message
            )

        valid, message = (
            self.validate_data_types(
                payload
            )
        )

        if not valid:
            return (
                False,
                message
            )

        valid, message = (
            self.validate_ranges(
                payload
            )
        )

        if not valid:
            return (
                False,
                message
            )

        valid, message = (
            self.validate_signature(
                payload,
                signature
            )
        )

        if not valid:
            return (
                False,
                message
            )

        return (
            True,
            "Telemetry packet validated"
        )


# =====================================================
# TESTING
# =====================================================

if __name__ == "__main__":

    validator = TelemetryValidator(
        "super_secret_aerospace_key"
    )

    packet = {
        "sensor_id": "temp_01",
        "temperature": 72,
        "pressure": 410,
        "rpm": 1500,
        "timestamp": 1718000000
    }

    signature = (
        validator.generate_signature(
            packet
        )
    )

    result = validator.validate_packet(
        packet,
        signature
    )

    print(result)