from flask import Blueprint, request, jsonify
from pathlib import Path
import json

from security.gateway import SecurityGateway

# =====================================================
# CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[1]

TELEMETRY_FILE = (
    BASE_DIR /
    "logs" /
    "telemetry.json"
)

# =====================================================
# TELEMETRY STORAGE
# =====================================================

def save_telemetry(packet):

    try:

        if TELEMETRY_FILE.exists():

            with open(
                TELEMETRY_FILE,
                "r"
            ) as file:

                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []

        else:

            data = []

        data.append(packet)

        # Keep most recent 100 packets

        data = data[-100:]

        with open(
            TELEMETRY_FILE,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    except Exception as e:

        print(
            f"Telemetry Storage Error: {e}"
        )

# =====================================================
# FLASK BLUEPRINT
# =====================================================

telemetry_bp = Blueprint(
    "telemetry",
    __name__
)

# =====================================================
# SECURITY GATEWAY
# =====================================================

security_gateway = SecurityGateway()

# =====================================================
# ROUTES
# =====================================================

@telemetry_bp.route(
    "/telemetry",
    methods=["POST"]
)
def receive_telemetry():

    """
    POST /telemetry

    Receives telemetry packets,
    processes them through the
    Security Gateway,
    and stores accepted packets.
    """

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "No telemetry data provided"
        }), 400

    try:

        # =============================================
        # Retrieve Signature
        # =============================================

        signature = data.get(
            "signature"
        )

        if not signature:

            return jsonify({
                "status": "error",
                "message": "Missing telemetry signature"
            }), 400

        # =============================================
        # Remove Signature Before Validation
        # =============================================

        packet = data.copy()

        packet.pop(
            "signature",
            None
        )

        # =============================================
        # Security Gateway Processing
        # =============================================

        result = (
            security_gateway.process_packet(
                packet,
                signature
            )
        )

        # =============================================
        # Rejected Packet
        # =============================================

        if result["status"] == "REJECTED":

            return jsonify({

                "status": "rejected",

                "reason":
                result["reason"]

            }), 403

        # =============================================
        # Store Accepted Packet
        # =============================================

        save_telemetry(packet)

        # =============================================
        # Successful Response
        # =============================================

        return jsonify({

            "status": "accepted",

            "alerts":
            result["alerts"],

            "packet":
            packet

        }), 200

    except Exception as e:

        return jsonify({

            "status": "error",

            "details":
            str(e)

        }), 500
