import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Secure ICS Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        180deg,
        #0B1020 0%,
        #111827 100%
    );
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Hero Section */
.hero {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 25px;

    padding: 30px;

    margin-bottom: 25px;
}

/* Typography */
.main-title {
    color: white;

    font-size: 3rem;

    font-weight: 700;
}

.subtitle {
    color: #94A3B8;

    font-size: 1rem;

    margin-top: 10px;
}

.section-header {
    color: white;

    font-size: 1.5rem;

    font-weight: 600;

    margin-top: 20px;

    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("Platform Modules")

    st.markdown("""
    - Dashboard
    - Telemetry
    - Detection Engine
    - Threat Activity
    - Analytics
    - System Logs
    """)

    st.divider()

    st.success("Platform Status: Operational")

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown("""
<div class="hero">

<div class="main-title">
🛡️ Secure Distributed ICS Security Platform
</div>

<div class="subtitle">
Systems Security Monitoring Console

Operational Technology Security • Telemetry Assurance • Threat Detection
</div>

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SYSTEM STATUS
# --------------------------------------------------

st.markdown(
    '<div class="section-header">Platform Status</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Sensors Online",
        "3",
        "+1"
    )

with col2:
    st.metric(
        "Active Alerts",
        "2",
        "-1"
    )

with col3:
    st.metric(
        "Threat Events",
        "12",
        "+3"
    )

with col4:
    st.metric(
        "System Health",
        "98%",
        "+2%"
    )

# --------------------------------------------------
# TELEMETRY SECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-header">Live Telemetry</div>',
    unsafe_allow_html=True
)

telemetry_col1, telemetry_col2, telemetry_col3 = st.columns(3)

with telemetry_col1:
    st.metric(
        "Temperature",
        "72.4 °F",
        "+1.2"
    )

with telemetry_col2:
    st.metric(
        "Pressure",
        "31.2 PSI",
        "-0.3"
    )

with telemetry_col3:
    st.metric(
        "RPM",
        "1450",
        "+25"
    )

# --------------------------------------------------
# SECURITY EVENTS
# --------------------------------------------------

st.markdown(
    '<div class="section-header">Security Events</div>',
    unsafe_allow_html=True
)

alert_col1, alert_col2 = st.columns(2)

with alert_col1:

    st.error(
        "CRITICAL • Replay attack detected"
    )

    st.warning(
        "HIGH • Telemetry anomaly detected"
    )

with alert_col2:

    st.info(
        "LOW • Sensor drift observed"
    )

    st.success(
        "Authentication validation successful"
    )

# --------------------------------------------------
# ATTACK ACTIVITY
# --------------------------------------------------

st.markdown(
    '<div class="section-header">Attack Activity</div>',
    unsafe_allow_html=True
)

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
# TELEMETRY ANALYTICS
# --------------------------------------------------

st.markdown(
    '<div class="section-header">Telemetry Analytics</div>',
    unsafe_allow_html=True
)

np.random.seed(42)

temperature_data = pd.DataFrame({
    "Temperature": np.random.normal(
        72,
        2,
        30
    )
})

st.line_chart(
    temperature_data,
    use_container_width=True
)

# --------------------------------------------------
# RECENT EVENTS
# --------------------------------------------------

st.markdown(
    '<div class="section-header">Recent Security Events</div>',
    unsafe_allow_html=True
)

events = [
    "2026-06-01 14:03:11 | HIGH | Telemetry anomaly detected",
    "2026-06-01 14:04:02 | CRITICAL | Replay attack detected",
    "2026-06-01 14:07:18 | MEDIUM | Authentication failure",
    "2026-06-01 14:09:55 | HIGH | Tampered telemetry rejected"
]

for event in events:
    st.code(event)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Secure Distributed ICS Security Platform | Systems Security Engineering Project"
)