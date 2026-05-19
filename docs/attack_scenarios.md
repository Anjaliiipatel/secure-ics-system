# Attack Scenarios

## Overview

This document defines adversarial simulation scenarios used to validate the Secure Distributed ICS Security Platform.

The purpose of these scenarios is not offensive exploitation. These simulations are used for defensive security validation, telemetry resilience testing, and detection engineering in a controlled ICS/OT-style environment.

---

# Scenario 1: Sensor Spoofing

## Description

A rogue or compromised node attempts to send falsified telemetry while pretending to be a trusted sensor.

## Example Behavior

- Fake temperature values
- Fake pressure readings
- Fake RPM values
- Invalid sensor identity

## Security Impact

- Incorrect controller decisions
- False operational state
- Potential unsafe response logic

## Detection Method

- Authentication failure detection
- Behavioral anomaly detection
- Threshold anomaly detection

## Mitigation

- API key validation
- Sensor identity verification
- Telemetry integrity validation
- Alert logging

---

# Scenario 2: Replay Attack

## Description

An attacker resends previously captured valid telemetry packets to make stale data appear current.

## Example Behavior

- Reusing old timestamps
- Resending previously valid packets
- Attempting to bypass authentication using old data

## Security Impact

- Duplicate telemetry processing
- Incorrect operational awareness
- Delayed detection of real conditions

## Detection Method

- Timestamp reuse detection
- Stale packet validation
- Replay alert generation

## Mitigation

- Timestamp freshness checks
- Replay detection cache
- Reject duplicate packets
- Log replay attempts

---

# Scenario 3: Telemetry Tampering

## Description

Telemetry values are modified during transmission without updating the integrity signature.

## Example Behavior

Original packet:

```json
{
  "sensor_id": "TEMP_01",
  "temperature": 72.4
}