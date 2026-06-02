from flask import request, jsonify, Blueprint

from security.gateway import SecurityGateway


telemetry_bp = Blueprint(
    "telemetry",
    __name__
)

security_gateway = SecurityGateway()


@telemetry_bp.route(
    "/telemetry",
    methods=["POST"]
)
def receive_telemetry():

    """
    POST /telemetry

    Receives telemetry packets,
    runs them through the Security Gateway,
    and returns the security result.
    """

    data = request.get_json()

    if not data:

        return jsonify({
            "error":
            "No telemetry data provided"
        }), 400

    try:

        # Signature supplied by sender

        signature = data.get(
            "signature"
        )

        if not signature:

            return jsonify({
                "error":
                "Missing telemetry signature"
            }), 400

        # Remove signature before validation

        packet = data.copy()

        packet.pop(
            "signature",
            None
        )

        result = (
            security_gateway.process_packet(
                packet,
                signature
            )
        )

        if result["status"] == "REJECTED":

            return jsonify({
                "status":
                "rejected",

                "reason":
                result["reason"]
            }), 403

        return jsonify({

            "status":
            "accepted",

            "alerts":
            result["alerts"],

            "packet":
            result["packet"]

        }), 200

    except Exception as e:

        return jsonify({

            "status":
            "error",

            "details":
            str(e)

        }), 500