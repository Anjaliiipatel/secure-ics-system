import time

class ReplayDetector:
    def __init__(self, window_size_seconds=60):
        # Stores the largest timestamp received so far
        self.last_timestamp = 0
        # Time window within which packets are considered valid
        self.window_size = window_size_seconds
        # A set or dictionary to track seen packets within the window
        self.seen_packets = set()

    def is_replay(self, timestamp: int) -> bool:
        current_time = time.time()

        # 1. Reject stale packets (older than current - window)
        if timestamp < (current_time - self.window_size):
            return True  # Packet is too old, likely a replay
        
        # 2. Reject future packets (timestamp greater than current time)
        if timestamp > (current_time + 5):
            return True  # Packet is from the future, invalid
        
        # 3. Reject duplicate timestamps
        if timestamp <= self.last_timestamp:
            return True  # Duplicate or reordered packet
        
        # 4. Update state and accept
        self.last_timestamp = timestamp

        # Optional: cleanup self.seen_packets here
        return False
    