import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import json
import html
import random
from datetime import datetime, timezone

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from analytics.security_analytics import SecurityAnalytics
from analytics.threat_score import ThreatScore
from incidents.incident_manager import IncidentManager
from reports.report_generator import SecurityReportGenerator


# =========================
# Page Config
# =========================

st.set_page_config(
    page_title="Secure ICS SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st_autorefresh(
    interval=250,
    key="live_dashboard_refresh"
)


# =========================
# File Paths
# =========================

CURRENT_DIR = Path(__file__).resolve().parent

if (CURRENT_DIR / "logs").exists():
    BASE_DIR = CURRENT_DIR
else:
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
            return file.readlines()[-20:]
    except Exception:
        return []


def fallback_telemetry():
    times = pd.date_range(
        end=pd.Timestamp.now(),
        periods=40,
        freq="s"
    )

    return pd.DataFrame({
        "timestamp": times,
        "pressure": [418 + random.uniform(-5, 5) for _ in range(40)],
        "temperature": [72 + random.uniform(-2, 2) for _ in range(40)],
        "rpm": [1450 + random.randint(-40, 40) for _ in range(40)],
        "flow": [88 + random.uniform(-3, 3) for _ in range(40)],
        "voltage": [24.1 + random.uniform(-0.3, 0.3) for _ in range(40)],
    })


# =========================
# Charts
# =========================

def live_telemetry_chart(df):
    df = df.sort_values(by="timestamp").tail(60)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["pressure"],
        mode="lines",
        name="Pressure",
        line=dict(width=3, shape="spline"),
        fill="tozeroy",
    ))

    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["temperature"],
        mode="lines",
        name="Temperature",
        line=dict(width=3, shape="spline"),
    ))

    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["rpm"],
        mode="lines",
        name="RPM",
        line=dict(width=3, shape="spline"),
    ))

    fig.update_layout(
        template="plotly_dark",
        height=360,
        margin=dict(l=10, r=10, t=25, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E5E7EB"),
        legend=dict(orientation="h", y=1.08, x=0),
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title=""),
        transition=dict(duration=250),
    )

    return fig


def attack_distribution_chart(distribution):
    fig = go.Figure()

    if distribution:
        fig.add_trace(go.Pie(
            labels=list(distribution.keys()),
            values=list(distribution.values()),
            hole=0.58,
            textinfo="label+percent",
        ))
    else:
        fig.add_trace(go.Pie(
            labels=["No Threat Data"],
            values=[1],
            hole=0.58,
            textinfo="label",
        ))

    fig.update_layout(
        template="plotly_dark",
        height=300,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E5E7EB"),
        showlegend=True,
        legend=dict(orientation="h", y=-0.1, x=0),
    )

    return fig


# =========================
# Load Telemetry
# =========================

telemetry = load_telemetry()

if telemetry:
    telemetry_df = pd.DataFrame(telemetry)

    telemetry_df["timestamp"] = pd.to_datetime(
        telemetry_df["timestamp"],
        errors="coerce"
    )

    required = {
        "timestamp",
        "pressure",
        "temperature",
        "rpm"
    }

    if not required.issubset(set(telemetry_df.columns)):
        telemetry_df = fallback_telemetry()

    if "flow" not in telemetry_df.columns:
        telemetry_df["flow"] = 88

    if "voltage" not in telemetry_df.columns:
        telemetry_df["voltage"] = 24.1

else:
    telemetry_df = fallback_telemetry()

latest = telemetry_df.iloc[-1]
telemetry_df = telemetry_df.sort_values(
    by="timestamp"
).tail(60)

logs = load_logs()


# =========================
# Week 7 Analytics
# =========================

analytics = SecurityAnalytics()
threat_engine = ThreatScore()
incident_manager = IncidentManager()

dashboard_summary = analytics.get_dashboard_summary()
attack_distribution = analytics.get_attack_percentages()
threat_data = threat_engine.get_dashboard_data()
open_incidents = incident_manager.get_open_incidents()
report_generator = SecurityReportGenerator()

latest_log = logs[-1] if logs else ""

previous_latest_log = st.session_state.get(
    "previous_latest_log",
    ""
)

new_event_detected = (
    latest_log != previous_latest_log
)

st.session_state["previous_latest_log"] = latest_log


# =========================
# Derived Metrics
# =========================

critical_logs = [
    log for log in logs
    if "CRITICAL" in log.upper()
]

gateway_stats = {
    "packets_received": len(telemetry_df),
    "packets_accepted": max(
        len(telemetry_df) - len(critical_logs),
        0
    ),
    "packets_rejected": len(critical_logs),
    "replay_attacks_blocked": dashboard_summary.get(
        "replay_attacks",
        0
    ),
    "anomalies_detected": dashboard_summary.get(
        "anomalies",
        0
    ),
}


# =========================
# Threat Styling
# =========================

threat_level = threat_data.get("level", "LOW")
threat_score = threat_data.get("score", 0)

if threat_level == "CRITICAL":
    threat_badge = "critical"
elif threat_level == "HIGH":
    threat_badge = "warning"
elif threat_level == "MEDIUM":
    threat_badge = "info"
else:
    threat_badge = "success"


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
    font-size: 1.55rem;
    font-weight: 850;
    letter-spacing: -0.5px;
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

.threat-card {
    background:
        linear-gradient(135deg, rgba(239,68,68,.16), rgba(59,130,246,.08)),
        rgba(255,255,255,.045);
    border: 1px solid rgba(239,68,68,.28);
    border-radius: 20px;
    padding: 20px;
    box-shadow:
        0 0 28px rgba(239,68,68,.18),
        0 20px 50px rgba(0,0,0,.32);
    animation: threatPulse 2.5s infinite;
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
    animation: slideIn .45s ease;
}

.live-new-event {
    background: rgba(16,185,129,.10);
    border: 1px solid rgba(16,185,129,.45);
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 10px;
    animation: liveSlideIn .55s ease, livePulse 1.2s ease;
    box-shadow: 0 0 24px rgba(16,185,129,.30);
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
    box-shadow: 0 0 14px rgba(245,158,11,.25);
}

.critical {
    color: #EF4444;
    background: rgba(239,68,68,.12);
    border: 1px solid rgba(239,68,68,.25);
    box-shadow: 0 0 18px rgba(239,68,68,.35);
}

.success {
    color: #10B981;
    background: rgba(16,185,129,.12);
    border: 1px solid rgba(16,185,129,.25);
}

.muted {
    color: #94A3B8;
}

@keyframes liveSlideIn {
    from {
        opacity: 0;
        transform: translateX(28px) scale(.98);
    }

    to {
        opacity: 1;
        transform: translateX(0px) scale(1);
    }
}

@keyframes livePulse {
    0% {
        box-shadow: 0 0 0 rgba(16,185,129,0);
    }

    50% {
        box-shadow: 0 0 28px rgba(16,185,129,.45);
    }

    100% {
        box-shadow: 0 0 12px rgba(16,185,129,.18);
    }
}

@keyframes threatPulse {
    0% {
        box-shadow: 0 0 12px rgba(239,68,68,.10);
    }

    50% {
        box-shadow: 0 0 30px rgba(239,68,68,.26);
    }

    100% {
        box-shadow: 0 0 12px rgba(239,68,68,.10);
    }
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

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(20px);
    }

    to {
        opacity: 1;
        transform: translateX(0px);
    }
}
</style>
""", unsafe_allow_html=True)


# =========================
# Header
# =========================

utc_now = datetime.now(timezone.utc).strftime("%H:%M:%S")

left, right = st.columns([2.4, 1.2])

with left:
    st.markdown("""
    <div class="header-subtitle">Industrial Security Operations Center</div>
    <div class="header-title">Secure ICS Security Operations Command</div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div style="display:flex; gap:10px; justify-content:flex-end; flex-wrap:wrap;">
        <div class="top-chip">UTC {utc_now}</div>
        <div class="top-chip nominal"><span class="status-dot"></span> GATEWAY ONLINE</div>
        <div class="top-chip">⚡ LIVE TELEMETRY</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# =========================
# SOC Executive Metrics
# =========================

c1, c2, c3, c4 = st.columns(4)

cards = [
    ("Threat Level", threat_level, "Current Risk"),
    ("Threat Score", f"{threat_score}/100", "Risk Index"),
    ("Open Incidents", len(open_incidents), "Active Cases"),
    ("Gateway Health", "ONLINE", "Nominal"),
]

for index, (col, (label, value, trend)) in enumerate(
    zip([c1, c2, c3, c4], cards)
):
    with col:
        card_class = "threat-card" if index == 0 else "metric-card"

        st.markdown(f"""
        <div class="{card_class}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-trend">{trend}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# =========================
# Security Gateway Status
# =========================

st.markdown("""
<div class="panel">
    <div class="section-title">Security Gateway Status</div>
    <div class="section-subtitle">Telemetry Validation Layer</div>
</div>
""", unsafe_allow_html=True)

g1, g2, g3, g4 = st.columns(4)

g1.metric("Validator", "ONLINE")
g2.metric("Replay Detector", "ONLINE")
g3.metric("Anomaly Detector", "ONLINE")
g4.metric("Authentication", "ONLINE")

st.markdown("<br>", unsafe_allow_html=True)


# =========================
# Main Content
# =========================

main_left, main_right = st.columns([2, 1])

with main_left:

    # =========================
    # Live Telemetry
    # =========================

    st.markdown("""
    <div class="panel">
        <div class="section-title">Live Telemetry</div>
        <div class="section-subtitle">Pressure · Temperature · Flow · Voltage</div>
    """, unsafe_allow_html=True)

    st.plotly_chart(
        live_telemetry_chart(telemetry_df),
        use_container_width=True
    )

    mini1, mini2, mini3, mini4 = st.columns(4)

    mini_values = [
        ("Pressure", f"{float(latest['pressure']):.1f}", "kPa"),
        ("Temp", f"{float(latest['temperature']):.1f}", "°F"),
        ("Flow", f"{float(latest['flow']):.1f}", "L/m"),
        ("Voltage", f"{float(latest['voltage']):.1f}", "V"),
    ]

    for col, (label, value, unit) in zip(
        [mini1, mini2, mini3, mini4],
        mini_values
    ):
        with col:
            st.markdown(f"""
            <div class="telemetry-mini">
                <div class="mini-label">{label}</div>
                <div class="mini-value">{value}<span class="muted" style="font-size:.75rem;"> {unit}</span></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # Threat Intelligence Row
    # =========================

    a1, a2 = st.columns(2)

    with a1:
        st.markdown("""
        <div class="panel">
            <div class="section-title">Attack Distribution</div>
            <div class="section-subtitle">Threat categories from system logs</div>
        """, unsafe_allow_html=True)

        st.plotly_chart(
            attack_distribution_chart(attack_distribution),
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with a2:
        st.markdown("""
        <div class="panel">
            <div class="section-title">Attack Monitor</div>
            <div class="section-subtitle">Live security activity feed</div>
        """, unsafe_allow_html=True)

        recent_security_events = logs[-6:]

        if recent_security_events:
            for index, event in enumerate(reversed(recent_security_events)):
                upper = event.upper()

                if "CRITICAL" in upper or "REPLAY" in upper:
                    badge = "critical"
                    label = "LIVE CRITICAL"
                elif "HIGH" in upper or "ANOMALY" in upper:
                    badge = "warning"
                    label = "LIVE ALERT"
                elif "ACCEPTED" in upper or "VALIDATED" in upper:
                    badge = "success"
                    label = "VALIDATED"
                else:
                    badge = "info"
                    label = "EVENT"

                live_class = (
                    "live-new-event"
                    if index == 0 and new_event_detected
                    else "alert-card"
                )

                st.markdown(f"""
                <div class="{live_class}">
                    <span class="badge {badge}">
                        {label}
                    </span><br>
                    <span class="muted">
                        {html.escape(event.strip())}
                    </span>
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

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # Operational Status
    # =========================

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

    header1, header2, header3, header4, header5 = st.columns([2, 1, 1, 1, 1])

    header1.markdown("**Device**")
    header2.markdown("**Type**")
    header3.markdown("**Zone**")
    header4.markdown("**Load**")
    header5.markdown("**Status**")

    st.divider()

    for device, dtype, zone, load, status in devices:
        d1, d2, d3, d4, d5 = st.columns([2, 1, 1, 1, 1])

        d1.markdown(device)
        d2.markdown(dtype)
        d3.markdown(zone)
        d4.markdown(load)

        if status == "ONLINE":
            d5.success(status)
        elif status == "DEGRADED":
            d5.warning(status)
        else:
            d5.error(status)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # Security Metrics
    # =========================

    st.markdown("""
    <div class="panel">
        <div class="section-title">Security Metrics</div>
        <div class="section-subtitle">Analytics Summary</div>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Total Events", dashboard_summary.get("total_events", 0))
    m2.metric("Total Attacks", dashboard_summary.get("total_attacks", 0))
    m3.metric("Replay", dashboard_summary.get("replay_attacks", 0))
    m4.metric("Integrity", dashboard_summary.get("integrity_failures", 0))


with main_right:

    # =========================
    # Open Incidents
    # =========================

    st.markdown("""
    <div class="panel">
        <div class="section-title">Open Incidents</div>
        <div class="section-subtitle">Active Security Cases</div>
    """, unsafe_allow_html=True)

    if open_incidents:
        for incident in reversed(open_incidents[-6:]):
            severity = incident.get("severity", "INFO")

            if severity == "CRITICAL":
                badge = "critical"
            elif severity == "HIGH":
                badge = "warning"
            elif severity == "MEDIUM":
                badge = "info"
            else:
                badge = "success"

            st.markdown(f"""
            <div class="alert-card">
                <span class="badge {badge}">
                    {html.escape(incident.get("id", "INC"))}
                </span><br>
                <strong>
                    {html.escape(incident.get("type", "Security Event"))}
                </strong><br>
                <span class="muted">
                    Severity: {html.escape(severity)} · Status: {html.escape(incident.get("status", "OPEN"))}
                </span><br>
                <span class="muted">
                    {html.escape(incident.get("created", ""))}
                </span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-card">
            <span class="badge success">CLEAR</span><br>
            <span class="muted">No open incidents.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # Security Timeline
    # =========================

    st.markdown("""
    <div class="panel">
        <div class="section-title">Security Timeline</div>
        <div class="section-subtitle">Real-time Event Feed</div>
    """, unsafe_allow_html=True)

    if logs:
        for log in reversed(logs[-10:]):
            upper = log.upper()

            if "CRITICAL" in upper:
                badge = "critical"
                label = "CRITICAL"
            elif "HIGH" in upper or "MEDIUM" in upper:
                badge = "warning"
                label = "WARNING"
            elif "ACCEPTED" in upper:
                badge = "success"
                label = "ACCEPTED"
            else:
                badge = "info"
                label = "INFO"

            st.markdown(f"""
            <div class="alert-card">
                <span class="badge {badge}">
                    {label}
                </span><br>
                <span class="muted">
                    {html.escape(log.strip())}
                </span>
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
    # Security Reports
    # =========================

    

    st.markdown("""
    <div class="panel">
        <div class="section-title">Security Reports</div>
        <div class="section-subtitle">Generate executive security summaries</div>
    </div>
    """, unsafe_allow_html=True)

    if "generated_reports" not in st.session_state:
        st.session_state["generated_reports"] = None

    if st.button("📄 Generate Security Report"):
        st.session_state["generated_reports"] = (
            report_generator.generate_all_reports()
    )

    st.success("Security reports generated!")

    if st.session_state["generated_reports"]:

        for label, path in st.session_state["generated_reports"].items():

            with open(path, "rb") as file:
                st.download_button(
                    label=f"Download {label}",
                    data=file,
                    file_name=Path(path).name,
                    mime="application/octet-stream"
                )

# =========================
# Footer
# =========================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="muted" style="display:flex; justify-content:space-between; font-family:monospace; font-size:.75rem;">
    <div>ingest stream: http://127.0.0.1:5000/telemetry</div>
    <div>HMAC SHA-256 · Replay Protection · Sensor Registry · SOC Monitoring</div>
</div>
""", unsafe_allow_html=True)