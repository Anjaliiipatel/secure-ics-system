# Week 6 Report – Secure ICS Telemetry & Detection Platform

## Overview

The primary objective of Week 6 was to integrate the previously developed security modules into a fully functioning telemetry security platform. This involved connecting simulated sensor devices to a centralized controller API, processing telemetry through a Security Gateway, storing validated telemetry, and displaying operational and security data through a real-time dashboard.

## Objectives

* Develop an end-to-end telemetry pipeline.
* Integrate telemetry validation, replay detection, anomaly detection, and sensor authentication into a unified Security Gateway.
* Implement live telemetry transmission between sensor nodes and the controller API.
* Store validated telemetry for dashboard visualization.
* Test security controls using simulated attack scenarios.
* Improve dashboard monitoring capabilities.

## Work Completed

### Telemetry Pipeline Integration

A telemetry client was developed to simulate industrial sensor devices transmitting operational data to the controller API. Each telemetry packet contains:

* Sensor Identifier
* Temperature Reading
* Pressure Reading
* RPM Reading
* Timestamp
* HMAC Signature

The telemetry client continuously generates and transmits sensor data to the API, creating a live telemetry stream for testing and monitoring purposes.

### Controller API Development

The controller API was updated to:

* Receive telemetry packets through HTTP POST requests.
* Extract and validate packet signatures.
* Pass telemetry to the Security Gateway.
* Store accepted telemetry in a centralized telemetry file.
* Return processing results to clients.

This component serves as the primary entry point into the monitoring platform.

### Security Gateway Integration

The Security Gateway was expanded into a centralized security processing layer responsible for:

* Packet Validation
* Sensor Authentication
* Replay Attack Detection
* Behavioral Anomaly Detection
* Security Event Logging

Telemetry packets are processed through multiple validation stages before acceptance.

### Sensor Authentication

A Sensor Registry was implemented to maintain a list of authorized devices.

The gateway now verifies sensor identities before telemetry is accepted. Packets originating from unauthorized devices are rejected and logged as security events.

### Telemetry Storage

Validated telemetry packets are stored within a centralized telemetry repository. This repository serves as the primary data source for dashboard visualization and operational analytics.

### Dashboard Enhancements

The Streamlit dashboard was updated to provide:

* Live telemetry visualization
* Security Gateway status monitoring
* Security metrics
* Attack monitoring
* Real-time event feeds
* Operational status monitoring

The dashboard automatically refreshes to display incoming telemetry and newly detected security events.

## Security Testing

Multiple attack simulations were executed to validate security controls.

### Replay Attack

A replay attack was simulated by retransmitting previously accepted telemetry packets.

Result:

* Replay detection successfully identified duplicate packets.
* Gateway rejected replayed telemetry.
* Security event logged.

### Tampering Attack

Telemetry data was modified after packet signing.

Result:

* HMAC validation failed.
* Packet rejected.
* Integrity failure logged.

### Unauthorized Node Attack

Telemetry was transmitted from an unregistered sensor.

Result:

* Sensor authentication failed.
* Gateway rejected the packet.
* Unauthorized device activity logged.

### Spoofing Attack

Abnormal telemetry values were transmitted to simulate sensor manipulation.

Result:

* Anomaly detection generated alerts.
* Security event recorded.

### Flood Attack

A high volume of telemetry packets was transmitted in rapid succession.

Result:

* Gateway successfully processed incoming traffic.
* Telemetry logging and monitoring remained operational.

## Results

By the end of Week 6, the project successfully demonstrated:

* End-to-end telemetry transmission
* Real-time dashboard monitoring
* Secure packet validation
* Device authentication
* Replay attack protection
* Behavioral anomaly detection
* Security event logging
* Attack simulation testing

The platform now functions as a complete industrial telemetry security monitoring environment capable of detecting and responding to multiple simulated attack scenarios.

## Challenges Encountered

Several integration challenges were encountered during development:

* Python package import issues across project modules.
* Dashboard rendering errors during live telemetry integration.
* Security module integration within the controller API.
* Refactoring older attack simulation scripts to support the new telemetry pipeline.

These issues were resolved through restructuring project modules, updating imports, and redesigning attack simulation workflows.

## Next Steps

Planned objectives for Week 7 include:

* Security analytics and reporting
* Historical attack trend visualization
* Threat scoring mechanisms
* Incident response workflows
* Automated security report generation
* Dashboard enhancements for SOC-style monitoring

## Conclusion

Week 6 successfully transformed the Secure ICS Telemetry & Detection Platform from a collection of individual security modules into a fully integrated monitoring system. Live telemetry processing, security validation, attack detection, and real-time visualization are now operational, providing a strong foundation for advanced security analytics and incident response capabilities in future development phases.
