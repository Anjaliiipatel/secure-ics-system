import streamlit as st
import pandas as pd

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Secure ICS Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Custom Styling
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0A0F1C;
}

h1 {
    color: #E6EDF3;
    font-weight: 700;
}

h2, h3 {
    color: #C9D1D9;
}

[data-testid="metric-container"] {
    background-color: #161B22;
    border: 1px solid #30363D;
    padding: 15px;
    border-radius: 12px;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.title("Platform Modules")

    st.markdown("""
    - Dashboard
    - Telemetry
    - Detection Engine
    - Security Events
    - Attack Activity
    - System Logs
    """)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown("""
# 🛡️ Secure Distributed ICS Security Platform

### Systems Security Monitoring Console

Operational Technology Security • Telemetry Assurance • Threat Detection
""")

st.success(
    "System Status: OPERATIONAL | Detection Engine Active | Security Gateway Online"
)

# --------------------------------------------------
# Metrics
# --------------------------------------------------

st.header("System Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Sensors Online",
    "3"
)

col2.metric(
    "Active Alerts",
    "2"
)

col3.metric(
    "Threat Events",
    "12"
)

col4.metric(
    "System Health",
    "98%"
)

# --------------------------------------------------
# Telemetry Overview
# --------------------------------------------------

st.header("Live Telemetry")

telemetry_df = pd.DataFrame({
    "Sensor": [
        "TEMP_01",
        "PRESS_01",
        "RPM_01"
    ],
    "Value": [
        72.4,
        31.2,
        1450
    ],
    "Status": [
        "NORMAL",
        "NORMAL",
        "NORMAL"
    ]
})

st.dataframe(
    telemetry_df,
    use_container_width=True
)

# --------------------------------------------------
# Security Alerts
# --------------------------------------------------

st.header("Security Alerts")

st.warning(
    "HIGH - Telemetry anomaly detected on TEMP_01"
)

st.error(
    "CRITICAL - Replay attack detected"
)

# --------------------------------------------------
# Attack Activity
# --------------------------------------------------

st.header("Attack Activity")

attack_df = pd.DataFrame({
    "Attack Type": [
        "Spoofing",
        "Replay",
        "Flooding",
        "Tampering"
    ],
    "Events Detected": [
        4,
        2,
        1,
        3
    ]
})

st.dataframe(
    attack_df,
    use_container_width=True
)

# --------------------------------------------------
# Recent Security Events
# --------------------------------------------------

st.header("Recent Security Events")

sample_logs = [
    "2026-05-20 14:03:11 | HIGH | Telemetry anomaly detected",
    "2026-05-20 14:04:02 | CRITICAL | Replay attack detected",
    "2026-05-20 14:07:18 | MEDIUM | Authentication failure",
    "2026-05-20 14:09:55 | HIGH | Tampered telemetry rejected"
]

for log in sample_logs:
    st.code(log)

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Secure Distributed ICS Platform | Systems Security Engineering Project"
)