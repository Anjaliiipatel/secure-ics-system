import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Secure ICS Platform",
    page_icon="🛡️",
    layout="wide"
)

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def load_telemetry():
    try:
        with open("../logs/telemetry.json", "r") as f:
            return json.load(f)
    except:
        return []

def load_logs():
    try:
        with open("../logs/system_logs.txt", "r") as f:
            return f.readlines()[-15:]
    except:
        return []

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        180deg,
        #0B1020 0%,
        #111827 100%
    );
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.hero {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 25px;
}

.main-title {
    color: white;
    font-size: 3rem;
    font-weight: 700;
}

.subtitle {
    color: #94A3B8;
}

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 15px;
}

.section-header {
    color: white;
    font-size: 1.4rem;
    font-weight: 600;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("Platform Modules")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Telemetry",
            "Alerts",
            "Threat Activity",
            "System Logs"
        ]
    )

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
</div>

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# PLATFORM STATUS
# --------------------------------------------------

st.markdown(
    '<div class="section-header">Platform Status</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Sensors Online", "3")
col2.metric("Active Alerts", "2")
col3.metric("Threat Events", "12")
col4.metric("System Health", "98%")

# --------------------------------------------------
# LIVE TELEMETRY
# --------------------------------------------------

st.markdown(
    '<div class="section-header">Live Telemetry</div>',
    unsafe_allow_html=True
)

t1, t2, t3 = st.columns(3)

t1.metric("Temperature", "72.4 °F", "+0.8")
t2.metric("Pressure", "31.2 PSI", "-0.2")
t3.metric("RPM", "1450", "+35")

# --------------------------------------------------
# SECURITY ALERTS
# --------------------------------------------------

st.markdown(
    '<div class="section-header">Security Alerts</div>',
    unsafe_allow_html=True
)

alert1, alert2 = st.columns(2)

with alert1:
    st.error(
        "CRITICAL • Replay attack detected"
    )

with alert2:
    st.warning(
        "HIGH • Telemetry anomaly detected"
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
    "Events": [
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

chart_data = pd.DataFrame({
    "Time": range(30),
    "Temperature":
        np.random.normal(
            72,
            2,
            30
        )
})

fig = px.line(
    chart_data,
    x="Time",
    y="Temperature"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0B1020",
    plot_bgcolor="#0B1020"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# RECENT SECURITY EVENTS
# --------------------------------------------------

st.markdown(
    '<div class="section-header">Recent Security Events</div>',
    unsafe_allow_html=True
)

logs = load_logs()

if logs:

    for log in reversed(logs):
        st.code(log)

else:

    st.info(
        "No security events found."
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Secure Distributed ICS Security Platform | Systems Security Engineering Project"
)