# Secure ICS Security Operations Platform

## Overview

The Secure ICS Telemetry & Detection Platform is a cybersecurity-focused Industrial Control System (ICS) simulation environment designed to demonstrate secure telemetry communications, attack detection, security monitoring, and Zero Trust security principles within Operational Technology (OT) environments.

The platform simulates industrial sensor devices transmitting telemetry to a centralized controller through a secure telemetry pipeline. Security controls are applied at multiple layers to validate data integrity, authenticate devices, detect malicious activity, and provide real-time monitoring capabilities.

This project models security concepts commonly found in aerospace, manufacturing, energy, transportation, and critical infrastructure environments.

### Key Features

* Zero Trust telemetry communications
* Device authentication and authorization
* HMAC SHA-256 telemetry integrity validation
* Replay attack detection and prevention
* Behavioral anomaly detection
* Real-time security monitoring dashboard
* Centralized telemetry storage and logging
* Industrial cyber attack simulation framework
* Security analytics engine
* Threat scoring and historical threat trends
* Incident management system
* Executive security report generation
* Multi-format report export (TXT, JSON, CSV, PDF)
* MITRE ATT&CK technique mapping
* SOC-style operational dashboard
---

## Architecture

```text
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
Security Analytics
      ├── Threat Score
      ├── Incident Manager
      ├── MITRE ATT&CK Mapper
      ├── Threat Trends
      └── Report Generator
      ↓
SOC Dashboard
```

---

## Security Pipeline

<img width="1844" height="3948" alt="image" src="https://github.com/user-attachments/assets/844432f6-569a-4bb2-b89c-a968cc35a888" />


---

## Objectives

* Simulate distributed industrial telemetry systems
* Implement Zero Trust communication principles
* Detect and mitigate cyber attacks targeting ICS environments
* Demonstrate layered security engineering practices
* Build centralized security monitoring capabilities
* Explore Operational Technology (OT) cybersecurity concepts
* Model realistic industrial attack scenarios

---

## Core Components

### Sensor Nodes

Simulated industrial devices that generate:

* Temperature telemetry
* Pressure telemetry
* RPM telemetry
* Timestamp information

### Telemetry Client

Generates and securely transmits telemetry packets to the Controller API.

### Controller API

Receives telemetry data, validates requests, and forwards packets to the Security Gateway.

### Security Gateway

Acts as the centralized security enforcement layer responsible for:

* Packet validation
* Device authentication
* Replay attack protection
* Anomaly detection integration
* Security event generation
* Telemetry acceptance and rejection decisions

### Telemetry Validator

Performs:

* Schema validation
* Data type validation
* Timestamp validation
* HMAC SHA-256 integrity verification

### Sensor Registry

Maintains authorized device identities and enforces device authentication policies.

### Replay Detector

Identifies stale, duplicate, and replayed telemetry packets.

### Anomaly Detector

Monitors telemetry behavior for:

* Abnormal operating conditions
* Behavioral deviations
* Potential security threats

### Telemetry Storage

Stores accepted telemetry and security events for analysis and visualization.

## Security Intelligence
* Threat Score Engine
* Incident Manager
* MITRE ATT&CK Mapping
* Historical Threat Tracking
* Executive Report Generator
  
### Security Dashboard

Provides real-time visibility into:

* Live telemetry
* Security alerts
* Attack activity
* Operational status
* Security metrics
* Threat Score
* Threat Level
* Open Incidents
* MITRE ATT&CK Techniques
* Historical Threat Trend

## Security Reports

Document that the platform generates:

* TXT reports
* JSON reports
* CSV reports
* PDF executive reports
---

## Attack Simulation Framework

The platform includes multiple adversarial testing scenarios designed to emulate realistic industrial cyber threats.

### Replay Attack

Reuses previously captured telemetry packets to validate replay detection controls.

### Data Tampering Attack

Modifies telemetry after signing to verify integrity validation mechanisms.

### Unauthorized Node Attack

Attempts communication from an unregistered device to test authentication enforcement.

### Spoofing Attack

Injects malicious telemetry values to evaluate anomaly detection capabilities.

### Flooding Attack

Generates high volumes of telemetry traffic to test platform resiliency and monitoring effectiveness.

---

## Project Structure

```text
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

analytics/
│   ├── security_analytics.py
│   ├── threat_score.py
│   └── threat_trends.py

reports/
│   ├── report_generator.py
│   └── pdf_export.py

threat_intel/
│   └── mitre_mapping.py

incidents/
│   ├── incident_manager.py
│   └── incidents.json

dashboard/
│   └── dashboard.py
├── docs/

└── dashboard.py

```

---

## Installation

### Prerequisites

* Python 3.11+
* Git
* Pip
* Docker (Optional)

### Clone Repository

```bash
git clone https://github.com/yourusername/secure-ics-system.git

cd secure-ics-system
```

### Create Virtual Environment

#### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Platform

### Step 1: Start Controller API

Open a terminal from the project root directory:

```bash
python -m app.py
```

Expected Output:

```text
* Running on http://127.0.0.1:5000
```

The Controller API will begin accepting telemetry packets.

---

### Step 2: Start Telemetry Client

Open a second terminal and activate the virtual environment.

Run:

```bash
python -m controller.telemetry_client
```

Example Output:

```text
Sending telemetry packet...
Telemetry Accepted

Sending telemetry packet...
Telemetry Accepted
```

Telemetry packets will pass through the complete security pipeline before being accepted.

---

### Step 3: Launch Security Dashboard

Open a third terminal and run:

```bash
streamlit run dashboard.py
```

Open the dashboard in your browser:

```text
http://localhost:8501
```

---

## Running Attack Simulations

Open a new terminal and execute any attack scenario.

### Replay Attack

```bash
python attacks/replay_attack.py
```

### Data Tampering Attack

```bash
python attacks/tamper_attack.py
```

### Unauthorized Device Attack

```bash
python attacks/unauthorized_node.py
```

### Spoofing Attack

```bash
python attacks/spoof_attack.py
```

### Flooding Attack

```bash
python attacks/flood_attack.py
```

Security alerts and attack activity will be displayed in real time through the dashboard.

---

## Dashboard Metrics

### Telemetry Monitoring

* Packets Received
* Packets Accepted
* Packets Rejected

### Security Monitoring

* Replay Attacks Blocked
* Integrity Failures
* Unauthorized Devices
* Anomalies Detected

### Operational Monitoring

* Live Telemetry Feed
* Security Event Feed
* Attack Activity Timeline
* System Health Status

---

## Logs

Telemetry and security events are stored locally for monitoring, auditing, and forensic analysis.

```text
logs/

├── telemetry.json
└── system_logs.txt
```

---

## Technologies

| Technology   | Purpose                        |
| ------------ | ------------------------------ |
| Python       | Core platform development      |
| Flask        | Telemetry API services         |
| Streamlit    | Security monitoring dashboard  |
| Docker       | Containerized deployment       |
| Git/GitHub   | Version control                |
| HMAC SHA-256 | Telemetry integrity validation |

---

## Future Improvements

* MQTT integration for industrial messaging
* TLS-encrypted telemetry communications
* Machine learning-based anomaly detection
* SIEM integration
* Grafana dashboards
* Role-Based Access Control (RBAC)
* Secure secret management
* Distributed multi-node deployment

---

## Disclaimer

This project is intended for cybersecurity education, research, and demonstration purposes only. All attack simulations are executed within a controlled environment and are designed to demonstrate defensive security concepts.
