
## `docs/detection_engine.md`

```markdown
# Detection Engine

## Overview

The Detection Engine is responsible for identifying suspicious telemetry behavior within the Secure Distributed ICS Security Platform.

It analyzes telemetry after authentication, integrity validation, and replay protection have been performed. The goal is to detect abnormal operational behavior and generate security alerts for monitoring and logging.

---

# Detection Objectives

The Detection Engine is designed to:

- Identify unsafe telemetry values
- Detect abnormal operational deviations
- Classify alert severity
- Support adversarial simulation testing
- Generate security events for centralized logging
- Improve operational visibility within the simulated ICS environment

---

# Detection Types

## 1. Threshold Detection

Threshold detection identifies telemetry values outside expected operational ranges.

## Example Conditions

| Telemetry Field | Alert Condition |
|---|---|
| Temperature | Greater than 95 |
| Pressure | Less than 20 |
| RPM | Greater than 5000 |

## Purpose

Threshold detection helps identify:

- Spoofed telemetry
- Unsafe operational values
- Extreme sensor readings
- Potential cyber-physical manipulation

---

# 2. Behavioral Detection

Behavioral detection compares current telemetry against recent historical telemetry values.

## Example

If the recent average temperature is `72` and the current value is `130`, the system may classify this as a behavioral anomaly.

## Purpose

Behavioral detection helps identify:

- Sudden telemetry spikes
- Unexpected operational drift
- Suspicious deviations from normal behavior
- Gradual manipulation attempts

---

# 3. Replay Detection Integration

Replay detection identifies duplicate or stale telemetry packets based on timestamp reuse or freshness checks.

## Purpose

Replay detection helps prevent:

- Reuse of old telemetry
- Stale operational data
- Duplicate packet processing
- Attempts to bypass live telemetry monitoring

---

# 4. Integrity Failure Detection

Integrity validation failures occur when telemetry values do not match their expected cryptographic signature.

## Purpose

Integrity failure detection helps identify:

- Tampered telemetry
- Modified payloads
- Unauthorized data manipulation
- Man-in-the-middle style alteration attempts

---

# Alert Severity Levels

| Severity | Meaning |
|---|---|
| LOW | Minor irregularity or informational event |
| MEDIUM | Suspicious behavior requiring review |
| HIGH | Likely malicious or unsafe telemetry behavior |
| CRITICAL | Severe threat to system availability or integrity |

---

# Alert Object Format

Example alert object:

```json
{
  "alert_type": "Telemetry Anomaly",
  "severity": "HIGH",
  "sensor_id": "TEMP_01",
  "description": "Abnormal temperature spike detected",
  "timestamp": "2026-05-19 14:30:00"
}