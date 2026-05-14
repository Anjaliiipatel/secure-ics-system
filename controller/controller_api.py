# setting up a POST endpoint that will receive data and processes it through a security pipeline
# uses Flask for creating the API and handling request

from flask import Flask, request, jsonify, Blueprint
# Import your security pipeline here
from security.pipeline import SecurityPipeline

#define the blueprint for organizational clarity
telemetry_bp = Blueprint('telemetry', __name__)
security_pipeline = SecurityPipeline()

@telemetry_bp.route('/telemetry', methods=['POST'])
def receive_telemetry():
    """
    POST /telemetry
    Receives telemetry, runs security processing, and returns results.
    """
    #receive telemetry
    data = request.get_json()

    if not data:
        return jsonify({"error": "No telemtry data provided"}), 400
    
    try:
        # Pass telemetry into security pipeline
        # This handles validate, threat detection, or data sanitization
        processed_result = security_pipeline.process(data)

        # Return Response
        return jsonify({
            "status": "success",
            "message": "Telemetry processed successfully",
            "data": processed_result
        }), 200
    except Exception as e:
        # basic error handling for pipeline failures
        return jsonify({"error": "Internal processing error", "details": str(e)}), 500
    