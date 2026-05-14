import hashlib
import json
import hmac

class TelemetryValidator:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode('utf-8')
    
    def generate_signature(self, payload: dict) -> str:
        """
        Generate a SHA-256 HMAC signature for a telemetry payload.
        This ensures both integrity and authenticity
        """
        payload_bytes = json.dumps(payload, sort_keys=True).encode('utf-8')
        signature = hmac.new(
            self.secret_key,
            payload_bytes,
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def validate_telemetry(self, payload: dict, received_signature: str) -> bool:
        """
        Validate payload integrity using SHA-256 hashing.
        """
        computed_signature = self.generate_signature(payload)

        #Using hmac.compare_digest for timing attack resistance
        return hmac.compare_digest(computed_signature, received_signature)

if __name__ == "__main__":
    # Secret key should be securely stored, not hardcoded
    VALIDATOR = TelemetryValidator("super_secret_aerospace_key")

    # 1. Original Data
    telemetry_data = {
        "sensor_id": "temp_01",
        "value": 98.6,
        "timestamp": 1715655000
    }

    # 2. Sign the data before transmission
    sig = VALIDATOR.generate_signature(telemetry_data)
    print(f"Generated Signature: {sig}")

    # 3. Stimulate validation on the ground
    is_valid = VALIDATOR.validate_telemetry(telemetry_data, sig)
    print(f"Payload Valid: {is_valid}")

    # 4. Simulate tampering
    tampered_data = telemetry_data.copy()
    tampered_data["value"] = 150.0  # Tampering with the value
    is_valid_tampered = VALIDATOR.validate_telemetry(tampered_data, sig)
    print(f"Tampered Payload Valid: {is_valid_tampered}")