# Lab 2 Task 3 (percept trace for the reflex agent)
"""Lab 2 - Reflex classroom agent: percept/action trace.
Run: python lab2_percepts.py
Temperature is in degrees Celsius; occupied is a Boolean.
ECO / COOL / WARM / IDLE are simulated mode labels (no hardware is controlled).
"""


class ClassroomAgent:
    """Simple reflex agent: action depends only on the current percept."""

    def act(self, temp, occupied):
        if not occupied:          # empty room has priority over temperature
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"             # exactly 20 or 26 falls here (strict < and >)


if __name__ == "__main__":
    agent = ClassroomAgent()
    percepts = [(29, True), (29, True), (20, True),
                (26, True), (19, True), (29, False)]
    for step, percept in enumerate(percepts, 1):
        print(step, percept, "target mode", agent.act(*percept))
