def simulate_tamper(engine):
    print("... Starting Tamper Attack... ")

    # attacker modifies with payload to 96 but keeps the old 'OK' metadata
    print(engine.analyze("TEMP_01", "temperature", 96))
    