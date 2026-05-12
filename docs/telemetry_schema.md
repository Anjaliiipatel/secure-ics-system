# Telemetry Schema
## Example Telemetry Packet
```json
{
    "sensor_id": "TEMP_01", 
    "temperature": 72.4,
    "pressure": 31.2,
    "rpm": 1400,
    "timestamp": 1746783000,
    "api_key": "sensor_1_key",
    "signature": "sha256_hash"
}
```

## Field Definitons
sensor_id: String, Unique identifier for the sensor node
temperature: Float, Simulated temperature telemetry
pressure: Float, Simulated pressure telemetry
rpm: Integer, Simulated rotational speed
timestamp: Integer, Unix timestamp used for replay protection
api_key: String, Sensor authentication credential
signature: String, SHA-256 integrity verification hash

## Security Objectives
## Authetication
The api_key field verifies trusted sensor identity

## Integrity
The signature field validates telemetry integrity

## Replay Protection
The timestampy field prevents replay attacks.

## Validation
All telemetry fields must conform to expected data types and ranges

