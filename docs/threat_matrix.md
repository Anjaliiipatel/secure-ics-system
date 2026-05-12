## Threat Matrix
| Threat | Attack Description | Impact | Detection Method | Mitigation |
|---|---|---|---|---|
| Sensor Spoofing | Attacker sends falsified telemetry pretending to be a trusted sensor | Incorrect operational decisions | Behavioral anomaly detection | API authentication + integrity validation |
| Replay Attack | Previously captured packets are resent | Duplicate or stale telemetry accepted | Timestamp reuse detection | Timestamp validation |
| Flooding Attack | Excessive telemetry requests overwhelm the system | Service degradation or outage | Request rate monitoring | Rate limiting |
| Data Tampering | Telemetry modified during transmission | Corrupted operational data | Signature mismatch detection | SHA-256 integrity verification |
| Unauthorized Node Access | Rogue device attempts to join the system | Unauthorized telemetry injection | Authentication failure logging | API key validation |
| Invalid Payload Injection | Malformed or malicious payloads sent to controller | Parsing failures or instability | Schema validation failure | Input validation |
| Telemetry Manipulation | Sensor values intentionally altered to trigger false alerts | Unsafe controller behavior | Threshold anomaly detection | Behavioral analysis |
| Log Tampering | Attempts to modify or delete security logs | Loss of forensic visibility | Integrity monitoring | Centralized append-only logging |
