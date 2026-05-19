def simulate_flood(engine):
    print(" Starting Flood Attack...")

    # burst 50 requests in 1 second
    for _ in range(50):
        engine.analyze("SENSOR_X", "rpm", 2500)
    
    # should trigger the "Rate Limit" (CRITICAL) alert
    print("Flood complete. Check engine for CRITICAL alerts.")