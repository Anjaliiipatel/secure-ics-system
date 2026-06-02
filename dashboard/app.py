import json
import random
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_autorefresh import st_autorefresh


# =========================
# Page Config
# =========================

st.set_page_config(
    page_title="Secure ICS Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st_autorefresh(interval=1000, key="live_dashboard_refresh")


# =========================
# File Paths
# =========================

BASE_DIR = Path(__file__).resolve().parents[1]
TELEMETRY_FILE = BASE_DIR / "logs" / "telemetry.json"
LOG_FILE = BASE_DIR / "logs" / "system_logs.txt"


# =========================
# Data Loading
# =========================

def load_telemetry():
    try:
        with open(TELEMETRY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def load_logs():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            return file.readlines()[-12:]
    except Exception:
        return []


def fallback_telemetry():
    times = pd.date_range(end=pd.Timestamp.now(), periods=40, freq="s")

    return pd.DataFrame({
        "timestamp": times,
        "pressure": [418 + random.uniform(-5, 5) for _ in range(40)],
        "temperature": [72 + random.uniform(-2, 2) for _ in range(40)],
        "rpm": [1450 + random.randint(-40, 40) for _ in range(40)],
        "flow": [88 + random.uniform(-3, 3) for _ in range(40)],
        "voltage": [24.1 + random.uniform(-0.3, 0.3) for _ in range(40)],
    })


def live_telemetry_chart(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["pressure"],
        mode="lines",
        name="Pressure",
        line=dict(width=3),
        fill="tozeroy",
    ))

    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["temperature"],
        mode="lines",
        name="Temperature",
        line=dict(width=3),
        fill="tozeroy",
    ))

    fig.update_layout(
        template="plotly_dark",
        height=330,
        margin=dict(l=10, r=10, t=25, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E5E7EB"),
        legend=dict(orientation="h", y=1.08, x=0),
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title=""),
        transition=dict(duration=400),
    )

    return fig


def attack_surface_chart():
    points = 28

    df = pd.DataFrame({
        "t": list(range(points)),
        "attempts": [max(0, round(8 + random.random() * 8)) for _ in range(points)],
        "blocked": [max(0, round(6 + random.random() * 7)) for _ in range(points)],
    })

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["t"],
        y=df["attempts"],
        mode="lines",
        name="Attempts",
        line=dict(width=3),
    ))

    fig.add_trace(go.Scatter(
        x=df["t"],
        y=df["blocked"],
        mode="lines",
        name="Blocked",
        line=dict(width=3),
    ))

    fig.update_layout(
        template="plotly_dark",
        height=220,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E5E7EB"),
        legend=dict(orientation="h", y=1.12, x=0),
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title=""),
        transition=dict(duration=400),
    )

    return fig


# =========================
# Load Data
# =========================

telemetry = load_telemetry()

if telemetry:
    telemetry_df = pd.DataFrame(telemetry)
    telemetry_df["timestamp"] = pd.to_datetime(
        telemetry_df["timestamp"],
        errors="coerce"
    )

    required = {"timestamp", "pressure", "temperature", "rpm"}
    if not required.issubset(set(telemetry_df.columns)):
        telemetry_df = fallback_telemetry()

    if "flow" not in telemetry_df.columns:
        telemetry_df["flow"] = 88

    if "voltage" not in telemetry_df.columns:
        telemetry_df["voltage"] = 24.1
else:
    telemetry_df = fallback_telemetry()

latest = telemetry_df.iloc[-1]
logs = load_logs()

critical_logs = [log for log in logs if "CRITICAL" in log.upper()]
online_pct = 75
blocked_rate = 97


# =========================
# CSS
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(37,99,235,.24), transparent 35%),
        radial-gradient(circle at 90% 12%, rgba(124,58,237,.18), transparent 32%),
        radial-gradient(circle at 50% 100%, rgba(6,182,212,.13), transparent 40%),
        #020617;
    color: #E5E7EB;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.panel {
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 24px;
    padding: 20px;
    box-shadow: 0 20px 50px rgba(0,0,0,.32);
    backdrop-filter: blur(20px);
    animation: fadeUp .65s ease;
}

.header-title {
    color: #F8FAFC;
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.4px;
}

.header-subtitle {
    color: #94A3B8;
    font-size: .75rem;
    text-transform: uppercase;
    letter-spacing: .2em;
}

.top-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border: 1px solid rgba(255,255,255,.10);
    background: rgba(255,255,255,.045);
    border-radius: 10px;
    padding: 8px 12px;
    font-size: .76rem;
    color: #CBD5E1;
    font-family: monospace;
}

.nominal {
    color: #10B981;
    border-color: rgba(16,185,129,.35);
    background: rgba(16,185,129,.10);
}

.section-title {
    color: #F8FAFC;
    font-size: .95rem;
    font-weight: 750;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #94A3B8;
    font-size: .78rem;
    margin-bottom: 16px;
}

.metric-card {
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 18px;
    padding: 18px;
    animation: fadeUp .75s ease;
}

.metric-label {
    color: #94A3B8;
    font-size: .68rem;
    text-transform: uppercase;
    letter-spacing: .16em;
    font-weight: 700;
}

.metric-value {
    color: #F8FAFC;
    font-family: monospace;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 8px;
}

.metric-trend {
    color: #94A3B8;
    font-family: monospace;
    font-size: .75rem;
    margin-top: 4px;
}

.status-dot {
    height: 8px;
    width: 8px;
    border-radius: 999px;
    display: inline-block;
    background: #10B981;
    box-shadow: 0 0 12px rgba(16,185,129,.85);
    animation: pulse 1.4s infinite;
}

.warn-dot {
    background: #F59E0B;
    box-shadow: 0 0 12px rgba(245,158,11,.85);
}

.crit-dot {
    background: #EF4444;
    box-shadow: 0 0 12px rgba(239,68,68,.85);
}

.telemetry-mini {
    background: rgba(255,255,255,.035);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 14px;
    padding: 14px;
}

.mini-label {
    color: #94A3B8;
    font-size: .65rem;
    text-transform: uppercase;
    letter-spacing: .15em;
}

.mini-value {
    color: #F8FAFC;
    font-family: monospace;
    font-size: 1.25rem;
    font-weight: 700;
    margin-top: 6px;
}

.alert-card {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 10px;
}

.badge {
    display: inline-block;
    border-radius: 999px;
    padding: 4px 8px;
    font-size: .62rem;
    font-weight: 800;
    letter-spacing: .08em;
    margin-bottom: 6px;
}

.info {
    color: #38BDF8;
    background: rgba(56,189,248,.12);
    border: 1px solid rgba(56,189,248,.25);
}

.warning {
    color: #F59E0B;
    background: rgba(245,158,11,.12);
    border: 1px solid rgba(245,158,11,.25);
}

.critical {
    color: #EF4444;
    background: rgba(239,68,68,.12);
    border: 1px solid rgba(239,68,68,.25);
}

.success {
    color: #10B981;
    background: rgba(16,185,129,.12);
    border: 1px solid rgba(16,185,129,.25);
}

.device-row {
    display: grid;
    grid-template-columns: 1.4fr .8fr .8fr .8fr .8fr;
    gap: 10px;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,.07);
    padding: 10px 4px;
    font-size: .8rem;
}

.device-head {
    color: #94A3B8;
    font-size: .65rem;
    text-transform: uppercase;
    letter-spacing: .15em;
}

.device-name {
    color: #F8FAFC;
    font-family: monospace;
}

.muted {
    color: #94A3B8;
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(14px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse {
    0% { opacity: .55; }
    50% { opacity: 1; }
    100% { opacity: .55; }
}
</style>
""", unsafe_allow_html=True)


# =========================
# Header
# =========================

utc_now = datetime.now(timezone.utc).strftime("%H:%M:%S")

left, right = st.columns([2.5, 1])

with left:
    st.markdown("""
    <div class="header-subtitle">Secure Distributed ICS Platform</div>
    <div class="header-title">Operations Command</div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div style="display:flex; gap:10px; justify-content:flex-end; flex-wrap:wrap;">
        <div class="top-chip">UTC {utc_now}</div>
        <div class="top-chip nominal"><span class="status-dot"></span> SYSTEM NOMINAL</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# =========================
# Mission Status
# =========================

c1, c2, c3, c4 = st.columns(4)

cards = [
    ("Devices Online", f"{online_pct}%", "6/8 up"),
    ("Critical Alerts", len(critical_logs), "last 5m"),
    ("Threats Blocked", f"{blocked_rate}%", "127/131 events"),
    ("Throughput", "1.42", "Gb/s  +3.1%"),
]

for col, (label, value, trend) in zip([c1, c2, c3, c4], cards):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-trend">{trend}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# =========================
# Main Content
# =========================

main_left, main_right = st.columns([2, 1])

with main_left:
    st.markdown("""
    <div class="panel">
        <div class="section-title">Live Telemetry</div>
        <div class="section-subtitle">Pressure · Temperature · Flow · Voltage</div>
    """, unsafe_allow_html=True)

    st.plotly_chart(live_telemetry_chart(telemetry_df), use_container_width=True)

    mini1, mini2, mini3, mini4 = st.columns(4)

    mini_values = [
        ("Pressure", f"{float(latest['pressure']):.1f}", "kPa"),
        ("Temp", f"{float(latest['temperature']):.1f}", "°F"),
        ("Flow", f"{float(latest['flow']):.1f}", "L/m"),
        ("Voltage", f"{float(latest['voltage']):.1f}", "V"),
    ]

    for col, (label, value, unit) in zip([mini1, mini2, mini3, mini4], mini_values):
        with col:
            st.markdown(f"""
            <div class="telemetry-mini">
                <div class="mini-label">{label}</div>
                <div class="mini-value">{value}<span class="muted" style="font-size:.75rem;"> {unit}</span></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    a1, a2 = st.columns(2)

    with a1:
        st.markdown("""
        <div class="panel">
            <div class="section-title">Attack Surface (24h)</div>
            <div class="section-subtitle">Attempts vs blocked</div>
        """, unsafe_allow_html=True)

        st.plotly_chart(attack_surface_chart(), use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with a2:
        st.markdown("""
        <div class="panel">
            <div class="section-title">Attack Monitor</div>
            <div class="section-subtitle">Recent adversarial validation events</div>
            <div class="alert-card"><span class="badge critical">CRITICAL</span><br>Replay vector blocked · sensor gateway</div>
            <div class="alert-card"><span class="badge warning">WARNING</span><br>Telemetry drift observed · pressure channel</div>
            <div class="alert-card"><span class="badge success">BLOCKED</span><br>Spoofing attempt rejected · TEMP_01</div>
            <div class="alert-card"><span class="badge info">INFO</span><br>Integrity validation successful · signed packet</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
# ==========================================================
# OPERATIONAL STATUS
# ==========================================================

st.markdown("""
<div class="panel">
    <div class="section-title">Operational Status</div>
    <div class="section-subtitle">ICS Device Fleet</div>
</div>
""", unsafe_allow_html=True)

devices = [
    ("🟢 PLC-01", "PLC", "Zone A", "38%", "ONLINE"),
    ("🟡 PLC-04", "PLC", "Zone A", "81%", "DEGRADED"),
    ("🟢 RTU-12", "RTU", "Zone B", "47%", "ONLINE"),
    ("🟢 Gateway-01", "Gateway", "DMZ", "64%", "ONLINE"),
]

header1, header2, header3, header4, header5 = st.columns([2,1,1,1,1])

header1.markdown("**Device**")
header2.markdown("**Type**")
header3.markdown("**Zone**")
header4.markdown("**Load**")
header5.markdown("**Status**")

st.divider()

for device, dtype, zone, load, status in devices:

    c1, c2, c3, c4, c5 = st.columns([2,1,1,1,1])

    c1.markdown(device)
    c2.markdown(dtype)
    c3.markdown(zone)
    c4.markdown(load)

    if status == "ONLINE":
        c5.success(status)
    elif status == "DEGRADED":
        c5.warning(status)
    else:
        c5.error(status)
        

with main_right:
    st.markdown("""
    <div class="panel">
        <div class="section-title">Security Alerts</div>
        <div class="section-subtitle">Real-time event feed</div>
    """, unsafe_allow_html=True)

    if logs:
        for log in reversed(logs[-8:]):
            upper = log.upper()

            if "CRITICAL" in upper:
                badge = "critical"
                label = "CRITICAL"
            elif "HIGH" in upper or "MEDIUM" in upper:
                badge = "warning"
                label = "WARNING"
            else:
                badge = "info"
                label = "INFO"

            st.markdown(f"""
            <div class="alert-card">
                <span class="badge {badge}">{label}</span><br>
                <span class="muted">{log.strip()}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-card">
            <span class="badge info">INFO</span><br>
            <span class="muted">Waiting for live security events.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# Footer
# =========================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="muted" style="display:flex; justify-content:space-between; font-family:monospace; font-size:.75rem;">
    <div>ingest stream: ws://ics-gateway/telemetry</div>
    <div>Modbus · DNP3 · OPC-UA · uptime 99.982%</div>
</div>
""", unsafe_allow_html=True)