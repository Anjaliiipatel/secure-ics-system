def process_packet(self, packet, signature):

    self.stats["packets_received"] += 1

    # STEP 1: Validate packet integrity
    valid, message = self.validator.validate_packet(
        packet,
        signature
    )

    if not valid:

        self.stats["packets_rejected"] += 1
        self.stats["integrity_failures"] += 1

        self.log_event(
            "CRITICAL",
            "Integrity Failure",
            message
        )

        self.incident_manager.create_incident(
            "Integrity Failure",
            "CRITICAL"
        )

        self.ioc_engine.create_ioc(
            "Integrity Failure",
            "CRITICAL",
            source=packet.get("sensor_id", "unknown"),
            description="Telemetry packet failed HMAC integrity validation."
        )

        return {
            "status": "REJECTED",
            "reason": message
        }

    # STEP 2: Sensor authorization
    authorized = self.sensor_registry.is_authorized(
        packet["sensor_id"]
    )

    if not authorized:

        self.stats["packets_rejected"] += 1
        self.stats["unauthorized_sensors_blocked"] += 1

        self.log_event(
            "HIGH",
            "Unauthorized Sensor",
            f"Unauthorized sensor: {packet['sensor_id']}"
        )

        self.incident_manager.create_incident(
            "Unauthorized Sensor",
            "HIGH"
        )

        self.ioc_engine.create_ioc(
            "Unauthorized Sensor",
            "HIGH",
            source=packet.get("sensor_id", "unknown"),
            description="Unauthorized device attempted to send telemetry."
        )

        return {
            "status": "REJECTED",
            "reason": f"Unauthorized sensor: {packet['sensor_id']}"
        }

    # STEP 3: Replay detection
    replay, replay_message = self.replay_detector.is_replay(
        packet["timestamp"]
    )

    if replay:

        self.stats["packets_rejected"] += 1
        self.stats["replay_attacks_blocked"] += 1

        self.log_event(
            "HIGH",
            "Replay Attack",
            replay_message
        )

        self.incident_manager.create_incident(
            "Replay Attack",
            "HIGH"
        )

        self.ioc_engine.create_ioc(
            "Replay Attack",
            "HIGH",
            source=packet.get("sensor_id", "unknown"),
            description="Replay attack indicator detected from telemetry timestamp."
        )

        return {
            "status": "REJECTED",
            "reason": replay_message
        }

    # STEP 4: Anomaly detection
    telemetry = {
        "temperature": packet.get("temperature", 0),
        "pressure": packet.get("pressure", 0),
        "rpm": packet.get("rpm", 0)
    }

    alerts = self.anomaly_detector.analyze(
        telemetry
    )

    if alerts:

        self.stats["anomalies_detected"] += len(alerts)

        self.ioc_engine.create_ioc(
            "Telemetry Anomaly",
            "MEDIUM",
            source=packet.get("sensor_id", "unknown"),
            description="Abnormal telemetry behavior detected."
        )

        for alert in alerts:

            self.log_event(
                alert["severity"],
                alert["alert_type"],
                alert["description"]
            )

    # STEP 5: Accept packet
    self.stats["packets_accepted"] += 1

    self.log_event(
        "INFO",
        "Telemetry Accepted",
        "Telemetry packet passed all security checks"
    )

    return {
        "status": "ACCEPTED",
        "alerts": alerts,
        "packet": packet
    }