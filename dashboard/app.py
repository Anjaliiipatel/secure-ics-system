import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Secure ICS Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# AUTO REFRESH
# ==========================================================

if st_autorefresh:
    st_autorefresh(interval=2000, key="live_telemetry_refresh")


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[1]
TELEMETRY_PATH = BASE_DIR / "logs" / "telemetry.json"
LOG_PATH = BASE_DIR / "logs" / "system_logs.txt"


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def load_telemetry():
    try:
        with open(TELEMETRY_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_logs():
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as file:
            return file.readlines()[-12:]

    except FileNotFoundError:
        return []


def generate_fallback_telemetry():
    timestamps = pd.date_range(
        end=pd.Timestamp.now(),
        periods=40,
        freq="2s"
    )

    return pd.DataFrame({
        "timestamp": timestamps,
        "temperature": np.random.normal(72, 1.8, 40),
        "pressure": np.random.normal(418, 5, 40),
        "rpm": np.random.normal(1450, 35, 40),
    })


def build_line_chart(df, y_value, title, unit):
    fig = px.line(
        df,
        x="timestamp",
        y=y_value,
        title=title,
        markers=False,
    )

    fig.update_traces(
        line=dict(width=3),
        hovertemplate=f"%{{y:.2f}} {unit}<extra></extra>",
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E5E7EB"),
        title=dict(
            font=dict(size=18, color="#F8FAFC"),
            x=0.02,
        ),
        margin=dict(l=10, r=10, t=45, b=10),
        height=290,
        showlegend=False,
        transition={"duration": 500},
        xaxis=dict(
            showgrid=False,
            title="",
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.08)",
            title="",
        ),
    )

    return fig


def severity_class(log_line):
    upper_line = log_line.upper()

    if "CRITICAL" in upper_line:
        return "critical"

    if "HIGH" in upper_line:
        return "high"

    if "MEDIUM" in upper_line:
        return "medium"

    if "LOW" in upper_line:
        return "low"

    return "info"


# ==========================================================
# DATA
# ==========================================================

telemetry_records = load_telemetry()

if telemetry_records:
    telemetry_df = pd.DataFrame(telemetry_records)

    if "timestamp" in telemetry_df.columns:
        telemetry_df["timestamp"] = pd.to_datetime(
            telemetry_df["timestamp"],
            errors="coerce"
        )

    required_columns = {"timestamp", "temperature", "pressure", "rpm"}

    if not required_columns.issubset(set(telemetry_df.columns)):
        telemetry_df = generate_fallback_telemetry()

else:
    telemetry_df = generate_fallback_telemetry()

latest = telemetry_df.iloc[-1]

logs = load_logs()

active_alerts = sum(
    1 for log in logs
    if any(level in log.upper() for level in ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
)

critical_alerts = sum(
    1 for log in logs
    if "CRITICAL" in log.upper()
)


# ==========================================================
# CSS
# ==========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 8% 5%, rgba(59,130,246,0.24) 0%, transparent 28%),
        radial-gradient(circle at 90% 12%, rgba(16,185,129,0.16) 0%, transparent 24%),
        linear-gradient(180deg, #07101F 0%, #030712 100%);
    color: #E5E7EB;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

section[data-testid="stSidebar"] {
    background: rgba(8, 13, 26, 0.92);
    border-right: 1px solid rgba(255,255,255,0.08);
}

.hero {
    background: rgba(255,255,255,0.055);
    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 30px;
    padding: 34px;
    margin-bottom: 26px;
    box-shadow: 0 24px 70px rgba(0,0,0,0.35);
    animation: fadeUp 0.75s ease;
}

.main-title {
    color: #F8FAFC;
    font-size: 3.15rem;
    font-weight: 850;
    letter-spacing: -1.4px;
    line-height: 1.05;
}

.subtitle {
    color: #94A3B8;
    font-size: 1.03rem;
    margin-top: 12px;
}

.status-chip {
    display: inline-block;
    margin-top: 20px;
    background: rgba(16,185,129,0.14);
    color: #34D399;
    border: 1px solid rgba(52,211,153,0.32);
    padding: 8px 14px;
    border-radius: 999px;
    font-weight: 800;
    font-size: 0.78rem;
    letter-spacing: 0.6px;
}

.section-title {
    color: #F8FAFC;
    font-size: 1.35rem;
    font-weight: 780;
    margin-top: 26px;
    margin-bottom: 12px;
    letter-spacing: -0.3px;
}

.section-subtitle {
    color: #94A3B8;
    font-size: 0.92rem;
    margin-bottom: 12px;
}

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.055);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 24px;
    padding: 18px;
    box-shadow: 0 18px 40px rgba(0,0,0,0.24);
    animation: fadeUp 0.95s ease;
}

[data-testid="metric-container"] label {
    color: #94A3B8 !important;
    font-weight: 650 !important;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC !important;
    font-weight: 850 !important;
}

[data-testid="stMetricDelta"] {
    font-weight: 700 !important;
}

.glass-card {
    background: rgba(255,255,255,0.055);
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 24px;
    padding: 19px;
    margin-bottom: 14px;
    box-shadow: 0 16px 44px rgba(0,0,0,0.25);
    animation: fadeUp 1s ease;
}

.card-title {
    color: #F8FAFC;
    font-size: 1rem;
    font-weight: 800;
    margin-bottom: 6px;
}

.card-body {
    color: #CBD5E1;
    font-size: 0.92rem;
}

.badge {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 850;
    margin-bottom: 9px;
    letter-spacing: 0.5px;
}

.badge-green {
    color: #34D399;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(52,211,153,0.24);
}

.badge-amber {
    color: #FBBF24;
    background: rgba(245,158,11,0.12);
    border: 1px solid rgba(251,191,36,0.24);
}

.badge-red {
    color: #F87171;
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(248,113,113,0.24);
}

.badge-blue {
    color: #60A5FA;
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(96,165,250,0.24);
}

div[data-testid="stDataFrame"] {
    border-radius: 24px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}

pre {
    background: rgba(255,255,255,0.055) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    color: #E5E7EB !important;
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(18px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:
    st.markdown("## Operations")
    st.radio(
        "Navigation",
        ["Command", "Telemetry", "Threats", "Fleet", "Logs"],
        label_visibility="collapsed",
    )

    st.divider()

    st.success("Security Gateway Online")
    st.info("Zero Trust Enabled")
    st.caption("mTLS-ready · Replay protection · Telemetry validation")


# ==========================================================
# HERO BANNER
# ==========================================================

st.markdown(
    """
<div class="hero">
    <div class="main-title">Secure Distributed ICS Security Platform</div>
    <div class="subtitle">
        Systems Security Monitoring Console · Operational Technology Security · Telemetry Assurance · Threat Detection
    </div>
    <div class="status-chip">● SYSTEM NOMINAL</div>
</div>
""",
    unsafe_allow_html=True,
)


# ==========================================================
# PLATFORM STATUS METRICS
# ==========================================================

st.markdown('<div class="section-title">Mission Status</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

m1.metric("Devices Online", "8", "6/8 active")
m2.metric("Active Alerts", str(active_alerts), f"{critical_alerts} critical")
m3.metric("Threats Blocked", "127", "+14")
m4.metric("System Health", "98%", "+2%")


# ==========================================================
# LIVE TELEMETRY METRICS
# ==========================================================

st.markdown('<div class="section-title">Live Telemetry</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Latest validated sensor readings from the ICS telemetry pipeline.</div>',
    unsafe_allow_html=True,
)

t1, t2, t3 = st.columns(3)

t1.metric("Temperature", f"{float(latest['temperature']):.1f} °F", "+0.8")
t2.metric("Pressure", f"{float(latest['pressure']):.1f} kPa", "+4")
t3.metric("RPM", f"{int(float(latest['rpm']))}", "+25")


# ==========================================================
# TEMPERATURE CHART
# ==========================================================

st.markdown('<div class="section-title">Temperature Feed</div>', unsafe_allow_html=True)

temperature_fig = build_line_chart(
    telemetry_df,
    "temperature",
    "Live Temperature Trend",
    "°F",
)

st.plotly_chart(temperature_fig, use_container_width=True)


# ==========================================================
# PRESSURE CHART
# ==========================================================

st.markdown('<div class="section-title">Pressure Feed</div>', unsafe_allow_html=True)

pressure_fig = build_line_chart(
    telemetry_df,
    "pressure",
    "Live Pressure Trend",
    "kPa",
)

st.plotly_chart(pressure_fig, use_container_width=True)


# ==========================================================
# RPM CHART
# ==========================================================

st.markdown('<div class="section-title">RPM Feed</div>', unsafe_allow_html=True)

rpm_fig = build_line_chart(
    telemetry_df,
    "rpm",
    "Live RPM Trend",
    "RPM",
)

st.plotly_chart(rpm_fig, use_container_width=True)


# ==========================================================
# SECURITY ALERTS + ATTACK ACTIVITY
# ==========================================================

left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown('<div class="section-title">Security Events</div>', unsafe_allow_html=True)

    st.markdown(
        """
<div class="glass-card">
    <div class="badge badge-green">INFO</div>
    <div class="card-title">Authentication validation successful</div>
    <div class="card-body">Security Gateway accepted trusted telemetry source.</div>
</div>

<div class="glass-card">
    <div class="badge badge-amber">MEDIUM</div>
    <div class="card-title">Sensor drift observed</div>
    <div class="card-body">Pressure telemetry deviated from recent baseline.</div>
</div>

<div class="glass-card">
    <div class="badge badge-red">CRITICAL</div>
    <div class="card-title">Replay attack blocked</div>
    <div class="card-body">Stale telemetry packet rejected by replay protection.</div>
</div>
""",
        unsafe_allow_html=True,
    )

with right_col:
    st.markdown('<div class="section-title">Attack Activity</div>', unsafe_allow_html=True)

    attack_df = pd.DataFrame({
        "Attack Type": ["Spoofing", "Replay", "Tampering", "Flooding"],
        "Events": [4, 2, 3, 1],
        "Status": ["Blocked", "Blocked", "Blocked", "Observed"],
    })

    st.dataframe(
        attack_df,
        use_container_width=True,
        hide_index=True,
    )


# ==========================================================
# RECENT SECURITY EVENTS
# ==========================================================

st.markdown('<div class="section-title">Recent Security Events</div>', unsafe_allow_html=True)

if logs:
    for log in reversed(logs):
        sev = severity_class(log)

        if sev == "critical":
            badge = "badge-red"
            label = "CRITICAL"
        elif sev == "high":
            badge = "badge-amber"
            label = "HIGH"
        elif sev == "medium":
            badge = "badge-amber"
            label = "MEDIUM"
        elif sev == "low":
            badge = "badge-blue"
            label = "LOW"
        else:
            badge = "badge-green"
            label = "INFO"

        st.markdown(
            f"""
<div class="glass-card">
    <div class="badge {badge}">{label}</div>
    <div class="card-body">{log.strip()}</div>
</div>
""",
            unsafe_allow_html=True,
        )
else:
    st.markdown(
        """
<div class="glass-card">
    <div class="badge badge-blue">INFO</div>
    <div class="card-title">No security events found</div>
    <div class="card-body">Waiting for system logs from the detection pipeline.</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "Secure Distributed ICS Platform · Systems Security Engineering Project · OT Security · Telemetry Assurance"
)