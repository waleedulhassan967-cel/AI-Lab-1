# Lab 2 Task 3 (reflex and stateful agents)
"""Lab 2 - Reflex and stateful classroom agents.
The stateful agent remembers the previous target mode and reports whether a
command must be sent, so identical commands are not repeated.
"""


class ReflexClassroomAgent:
    """Memoryless baseline (same policy as lab2_percepts.py)."""

    def act(self, temp, occupied):
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"


class StatefulClassroomAgent:
    """Same thresholds and occupancy priority, plus one internal variable:
    previous_mode. act() returns (target_mode, send_command)."""

    def __init__(self):
        self.previous_mode = None   # nothing commanded yet

    def act(self, temp, occupied):
        if not occupied:
            target = "ECO"
        elif temp > 26:
            target = "COOL"
        elif temp < 20:
            target = "WARM"
        else:
            target = "IDLE"
        send = target != self.previous_mode   # command only on a change
        self.previous_mode = target
        return target, send
