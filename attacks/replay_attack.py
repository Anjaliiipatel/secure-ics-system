import time
def simulate_replat(engine):
    print(" ...Starting Spoof Attack...")

    # capture a valid "normal" packet
    valid_packet = {"id": "TEMP_O1", "type": "temperature", "value": 72}

    # resend the same "valid" packet multiple times
    for _ in range(3):
        print(engine.analyze(valid_packet["id"], valid_packet["type"], valid_packet["value"]))
        time.sleep(1)
