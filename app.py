import os
from flask import Flask
from controller.controller_api import telemetry_bp

app = Flask(__name__)

app.register_blueprint(telemetry_bp)

@app.route("/")
def health_check():
    return {
        "status": "online",
        "service": "Secure ICS Controller API"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
