import os
import json
from pathlib import Path
from flask import Flask, render_template, jsonify
from controller.controller_api import telemetry_bp

app = Flask(__name__)
app.register_blueprint(telemetry_bp)

BASE_DIR = Path(__file__).resolve().parent

def load_json_file(path, fallback):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return fallback

def load_log_file(path, limit=20):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.readlines()[-limit:]
    except Exception:
        return []
    
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/health")
def health_check():
    return jsonify({
        "status": "online",
        "service": "Secure ICS Controller API"
    })

@app.route("/api/telemetry")
def api_telemetry():
    return jsonify(load_json_file(
        BASE_DIR / "logs" / "telemetry.json",
        []
    ))

@app.route("/api/events")
def api_events():
    return jsonify({
        "events": load_log_file(
            BASE_DIR / "logs" / "system_logs.txt",
            20
        )
    })

@app.route("/api/incidents")
def api_incidents():
    return jsonify(load_json_file(
        BASE_DIR / "incidents" / "incidents.json",
        []
    ))

@app.route("/api/iocs")
def api_iocs():
    return jsonify(load_json_file(
        BASE_DIR / "threat_hunting" / "ioc_database.json",
        []
    ))

@app.route("/api/mitre")
def api_mitre():
    try:
        from threat_intel.mitre_mapping import MitreMapper
        from analytics.security_analytics import SecurityAnalytics

        analytics = SecurityAnalytics()
        mitre_mapper = MitreMapper()

        return jsonify(
            mitre_mapper.get_detected_mappings(
                analytics.get_attack_counts()
            )
        )
    except Exception:
        return jsonify([])
    
@app.route("/api/threat-score")
def api_threat_score():
    try:
        from analytics.threat_score import ThreatScore

        threat = ThreatScore()

        return jsonify(
            threat.get_dashboard_data()
        )
    except Exception:
        return jsonify({
            "score": 0,
            "level": "LOW"
        })
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )