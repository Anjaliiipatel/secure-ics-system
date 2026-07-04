from flask import Flask
from controller.controller_api import telemetry_bp

app = Flask(__name__)

app.register_blueprint(telemetry_bp)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/health")
def health_check():
    return {
        "status": "online",
        "service": "Secure ICS Controller API"
    }

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )