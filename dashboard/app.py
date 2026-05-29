import streamlit as st

st.set_page_config(
    page_title="Secure ICS Platform",
    layout="wide"
)

st.title("Secure Distributed ICS Security Platform")

st.subheader("Operational Telemetry & Threat Modeling Dashboard")

st.header("System Status")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Active Sensors", "3")
col2.metric("Alerts Generated", "12")
col3.metric("Replay Attacks", "2")
col4.metric("System Status", "Operational")

st.header("Telemetry Overview")

telemetry_data = {
    "Temperature": "72.4 °F",
    "Pressure": "31.2 PSI",
    "RPM": "1450"
}
st.write(telemetry_data)

st.header("Security Alerts")

alerts = [
    {
        "severity": "HIGH",
        "message": "Telemetry anomaly detected"
    },
    {
        "severity": "MEDIUM",
        "message": "Replay attack detected"
    }
]

for alert in alerts:
    st.error(
        f"{alert['severity']} ALERT: {alert['message']}"
    )
st.header("Attack Activity")

attack_events = [
    "Spoofing attempt detected",
    "Replay attack blocked",
    "Tampered telemetry rejected"
]
for event in attack_events:
    st.warning(event)

st.header("Recent Security Events")

sample_logs = [
    "2026-05-15 14:03:11 | HIGH | Telemetry anomaly detected",
    "2026-05-15 14:04:02 | CRITICAL | Replay attack detected"
]
for log in sample_logs:
    st.code(log)
    