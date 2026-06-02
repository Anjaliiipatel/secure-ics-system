import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="ICS Operations Command",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #1A2440 0%, #070B14 45%, #030712 100%);
    color: #E5E7EB;
}

#MainMenu, footer, header {visibility: hidden;}

.block-container {
    padding-top: 2rem;
}

.hero {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 28px;
    padding: 30px;
    margin-bottom: 25px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
    animation: fadeUp 0.8s ease;
}

.main-title {
    font-size: 3.2rem;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -1px;
}

.subtitle {
    color: #94A3B8;
    font-size: 1rem;
    margin-top: 8px;
}

.status-pill {
    display: inline-block;
    margin-top: 18px;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(16,185,129,0.15);
    color: #34D399;
    border: 1px solid rgba(52,211,153,0.35);
    font-weight: 700;
    font-size: 0.85rem;
}

.section-title {
    color: #F8FAFC;
    font-size: 1.45rem;
    font-weight: 750;
    margin-top: 26px;
    margin-bottom: 10px;
}

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    animation: fadeUp 0.9s ease;
}

[data-testid="metric-container"] label {
    color: #94A3B8 !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}

.glass-card {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 18px;
    margin-bottom: 12px;
    box-shadow: 0 12px 32px rgba(0,0,0,0.28);
    animation: fadeUp 1s ease;
}

.badge-green {color:#34D399; font-weight:800;}
.badge-amber {color:#FBBF24; font-weight:800;}
.badge-red {color:#F87171; font-weight:800;}

@keyframes fadeUp {
    from {opacity: 0; transform: translateY(18px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Operations")
    st.radio(
        "Navigation",
        ["Command", "Telemetry", "Threats", "Fleet", "Logs"],
        label_visibility="collapsed"
    )
    st.divider()
    st.success("Gateway Online")
    st.info("mTLS · Zero Trust · ICS/OT")

st.markdown("""
<div class="hero">
    <div class="main-title">ICS Operations Command</div>
    <div class="subtitle">
        Secure Distributed ICS Platform · Systems Security Monitoring Console
    </div>
    <div class="status-pill">SYSTEM NOMINAL</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Mission Status</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Devices Online", "75%", "6/8 up")
c2.metric("Critical Alerts", "0", "last 5m")
c3.metric("Threats Blocked", "97%", "+12 events")
c4.metric("Throughput", "1.42 Gb/s", "+3.1%")

st.markdown('<div class="section-title">Live Telemetry</div>', unsafe_allow_html=True)

t1, t2, t3, t4 = st.columns(4)
t1.metric("Pressure", "418 kPa", "+4")
t2.metric("Temperature", "72 °C", "-1")
t3.metric("Flow", "88 L/m", "+2.4")
t4.metric("Voltage", "24.1 V", "+0.1")

st.markdown('<div class="section-title">Attack Surface — 24h</div>', unsafe_allow_html=True)

attack_data = pd.DataFrame({
    "Hour": list(range(24)),
    "Attempts": np.random.randint(2, 18, 24),
    "Blocked": np.random.randint(2, 18, 24)
})

fig = px.area(
    attack_data,
    x="Hour",
    y=["Attempts", "Blocked"],
    template="plotly_dark"
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=20, b=10),
    legend=dict(orientation="h")
)

st.plotly_chart(fig, use_container_width=True)

left, right = st.columns([1.25, 1])

with left:
    st.markdown('<div class="section-title">Operational Status</div>', unsafe_allow_html=True)

    fleet = pd.DataFrame({
        "Device": ["PLC-01", "PLC-04", "RTU-12", "HMI-02", "Gateway-01", "Sensor S-118"],
        "Type": ["PLC", "PLC", "RTU", "HMI", "Gateway", "Sensor"],
        "Zone": ["Zone A", "Zone A", "Zone B", "Control Room", "DMZ", "Zone C"],
        "Load": ["38%", "81%", "47%", "22%", "64%", "0%"],
        "Status": ["ONLINE", "DEGRADED", "ONLINE", "ONLINE", "ONLINE", "OFFLINE"]
    })

    st.dataframe(fleet, use_container_width=True, hide_index=True)

with right:
    st.markdown('<div class="section-title">Security Alerts</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <span class="badge-green">LOW</span><br>
        Authentication validation successful
    </div>
    <div class="glass-card">
        <span class="badge-amber">MEDIUM</span><br>
        Sensor drift observed on Zone C telemetry
    </div>
    <div class="glass-card">
        <span class="badge-green">INFO</span><br>
        ingest stream: ws://ics-gateway/telemetry
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">Recent Security Events</div>', unsafe_allow_html=True)

events = [
    "2026-06-01 14:03:11 | INFO | Gateway heartbeat received",
    "2026-06-01 14:04:02 | LOW | Authentication validation successful",
    "2026-06-01 14:07:18 | MEDIUM | Sensor drift observed",
    "2026-06-01 14:09:55 | INFO | Telemetry packet validated"
]

for event in events:
    st.code(event)

st.caption("Modbus · DNP3 · OPC-UA · uptime 99.982%")