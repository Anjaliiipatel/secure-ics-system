import time


class ReplayDetector:
    """
    Detects replay attacks using a sliding time window.

    Security Controls:
    - Reject stale packets
    - Reject future-dated packets
    - Reject duplicate timestamps
    - Automatically clean up old entries
    """

    def __init__(self, window_size_seconds=60):

        # Time window for valid packets
        self.window_size = window_size_seconds

        # Track recently seen timestamps
        self.seen_packets = {}

    # =====================================================
    # CLEANUP EXPIRED TIMESTAMPS
    # =====================================================

    def cleanup(self):

        current_time = time.time()

        expired_timestamps = []

        for timestamp in self.seen_packets:

            if current_time - timestamp > self.window_size:
                expired_timestamps.append(timestamp)

        for timestamp in expired_timestamps:
            del self.seen_packets[timestamp]

    # =====================================================
    # REPLAY DETECTION
    # =====================================================

    def is_replay(self, timestamp: float):

        current_time = time.time()

        # Remove old entries first
        self.cleanup()

        # -----------------------------------------
        # Check 1: Stale Packet
        # -----------------------------------------

        if timestamp < (current_time - self.window_size):

            return (
                True,
                "Stale packet detected"
            )

        # -----------------------------------------
        # Check 2: Future Packet
        # -----------------------------------------

        if timestamp > (current_time + 5):

            return (
                True,
                "Future timestamp detected"
            )

        # -----------------------------------------
        # Check 3: Duplicate Packet
        # -----------------------------------------

        if timestamp in self.seen_packets:

            return (
                True,
                "Replay attack detected"
            )

        # -----------------------------------------
        # Accept Packet
        # -----------------------------------------

        self.seen_packets[timestamp] = current_time

        return (
            False,
            "Packet accepted"
        )

    # =====================================================
    # STATISTICS
    # =====================================================

    def get_tracked_packets(self):

        return len(self.seen_packets)


# =====================================================
# TESTING
# =====================================================

if __name__ == "__main__":

    detector = ReplayDetector()

    print("\n----- Test 1: Valid Packet -----")

    timestamp = time.time()

    replay, message = detector.is_replay(
        timestamp
    )

    print(
        f"Replay: {replay}"
    )

    print(
        f"Message: {message}"
    )

    print("\n----- Test 2: Replay Attack -----")

    replay, message = detector.is_replay(
        timestamp
    )

    print(
        f"Replay: {replay}"
    )

    print(
        f"Message: {message}"
    )

    print("\n----- Test 3: Future Packet -----")

    future_timestamp = time.time() + 100

    replay, message = detector.is_replay(
        future_timestamp
    )

    print(
        f"Replay: {replay}"
    )

    print(
        f"Message: {message}"
    )

    print("\n----- Test 4: Stale Packet -----")

    old_timestamp = time.time() - 500

    replay, message = detector.is_replay(
        old_timestamp
    )

    print(
        f"Replay: {replay}"
    )

    print(
        f"Message: {message}"
    )

    print("\n----- Statistics -----")

    print(
        f"Tracked Packets: {detector.get_tracked_packets()}"
    ) 