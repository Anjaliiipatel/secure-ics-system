import time

def simulate_spoof(engine):
    print("... Starting Spoof Attack...")

    # target: impossible values
    print(engine.analyze("SPOOF_ID_99", "temperature", 500))

    # target: fake sensor identities
    print(engine.analyze("GHOST_SENSOR", "pressure", 50))
    