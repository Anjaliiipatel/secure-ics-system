Secure ICS Telemetry & Detection Platform
Overview

The Secure ICS Telemetry & Detection Platform is a cybersecurity-focused Industrial Control System (ICS) simulation environment designed to demonstrate secure telemetry communications, attack detection, security monitoring, and Zero Trust security principles within Operational Technology (OT) environments.

The platform simulates industrial sensor devices transmitting telemetry to a centralized controller through a secure telemetry pipeline. Security controls are applied at multiple layers to validate data integrity, authenticate devices, detect malicious activity, and provide real-time monitoring capabilities.

This project models security concepts commonly found in aerospace, manufacturing, energy, transportation, and critical infrastructure environments.

Key Features
Zero Trust telemetry communications
Device authentication and authorization
HMAC SHA-256 telemetry integrity validation
Replay attack detection and prevention
Behavioral anomaly detection
Real-time security monitoring dashboard
Centralized telemetry storage and logging
Industrial cyber attack simulation framework
Architecture
Sensor Nodes
      ↓
Telemetry Client
      ↓
Flask Controller API
      ↓
Security Gateway
      ├── Telemetry Validator
      ├── Sensor Registry
      ├── Replay Detector
      └── Anomaly Detector
      ↓
Telemetry Storage
      ↓
Streamlit Security Dashboard
Security Pipeline
Telemetry Packet
        ↓
┌─────────────────────┐
│ Security Gateway    │
└─────────┬───────────┘
          │
          ▼
  Telemetry Validator
          │
          ▼
   Sensor Registry
          │
          ▼
   Replay Detector
          │
          ▼
  Anomaly Detector
          │
          ▼
 Accept / Reject
Objectives
Simulate distributed industrial telemetry systems
Implement Zero Trust communication principles
Detect and mitigate cyber attacks targeting ICS environments
Demonstrate layered security engineering practices
Build centralized security monitoring capabilities
Explore Operational Technology (OT) cybersecurity concepts
Model realistic industrial attack scenarios
Core Components
Sensor Nodes

Simulated industrial devices that generate:

Temperature telemetry
Pressure telemetry
RPM telemetry
Timestamp information
Telemetry Client

Generates and securely transmits telemetry packets to the Controller API.

Controller API

Receives telemetry, validates requests, and forwards packets to the Security Gateway.

Security Gateway

Centralized security enforcement layer responsible for:

Packet validation
Device authentication
Replay attack protection
Anomaly detection
Security event generation
Telemetry acceptance and rejection decisions
Telemetry Validator

Performs:

Schema validation
Data type validation
Timestamp validation
HMAC SHA-256 signature verification
Sensor Registry

Maintains trusted device identities and enforces authentication policies.

Replay Detector

Detects:

Duplicate packets
Replayed packets
Stale telemetry
Invalid timestamps
Anomaly Detector

Monitors telemetry for:

Abnormal operating conditions
Behavioral deviations
Potential security threats
Security Dashboard

Provides real-time visibility into:

Live telemetry
Security alerts
Attack activity
Operational status
Security metrics
Attack Simulation Framework

The platform includes adversarial testing scenarios designed to emulate realistic industrial cyber threats.

Replay Attack

Reuses captured telemetry packets to validate replay detection controls.

Data Tampering Attack

Modifies telemetry after signing to verify integrity validation mechanisms.

Unauthorized Node Attack

Attempts communication from an unregistered device.

Spoofing Attack

Injects malicious telemetry values to evaluate anomaly detection capabilities.

Flooding Attack

Generates excessive telemetry traffic to test platform resiliency.

Project Structure
secure-ics-system/

├── app.py

├── controller/
│   ├── controller_api.py
│   └── telemetry_client.py

├── security/
│   ├── gateway.py
│   ├── validation.py
│   ├── sensor_registry.py
│   ├── replay_detection.py
│   └── anomaly_detection.py

├── attacks/
│   ├── replay_attack.py
│   ├── spoof_attack.py
│   ├── tamper_attack.py
│   ├── flood_attack.py
│   └── unauthorized_node.py

├── logs/
│   ├── telemetry.json
│   └── system_logs.txt

├── docs/

└── dashboard.py
Installation
Clone Repository
git clone https://github.com/yourusername/secure-ics-system.git

cd secure-ics-system
Create Virtual Environment

Windows:

python -m venv venv
venv\Scripts\activate

Linux/macOS:

python3 -m venv venv
source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Running the Platform
Start Controller API
python -m controller.controller_api
Start Telemetry Client

Open a second terminal:

python -m controller.telemetry_client
Launch Dashboard

Open a third terminal:

streamlit run dashboard.py

Access:

http://localhost:8501
Running Attack Simulations

Replay Attack

python attacks/replay_attack.py

Data Tampering Attack

python attacks/tamper_attack.py

Unauthorized Device Attack

python attacks/unauthorized_node.py

Spoofing Attack

python attacks/spoof_attack.py

Flooding Attack

python attacks/flood_attack.py
Dashboard Metrics
Telemetry Monitoring
Packets Received
Packets Accepted
Packets Rejected
Security Monitoring
Replay Attacks Blocked
Integrity Failures
Unauthorized Devices
Anomalies Detected
Operational Monitoring
Live Telemetry Feed
Security Event Feed
Attack Activity Timeline
System Health Status
Logs
logs/

├── telemetry.json
└── system_logs.txt

Telemetry and security events are stored for monitoring, auditing, and forensic analysis.

Technologies
Technology	Purpose
Python	Core platform development
Flask	Telemetry API services
Streamlit	Security monitoring dashboard
Docker	Containerized deployment
Git/GitHub	Version control
HMAC SHA-256	Telemetry integrity validation
Future Improvements
MQTT integration
TLS-encrypted telemetry communications
Machine learning anomaly detection
SIEM integration
Grafana dashboards
Role-Based Access Control (RBAC)
Secure secret management
Distributed multi-node deployment
Automated incident response
Threat correlation and analytics
