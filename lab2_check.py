# Lab 2 Task 3 (tests, edge case and trace output)
"""Lab 2 - Tests, traces and edge-case analysis.
Run: python lab2_check.py
Writes outputs/mode_transition_trace.csv and prints all results.
"""
import csv
import os

from lab2_model import ReflexClassroomAgent, StatefulClassroomAgent

os.makedirs("outputs", exist_ok=True)


def run_stateful(percepts):
    agent = StatefulClassroomAgent()
    rows = []
    for step, (temp, occ) in enumerate(percepts, 1):
        prev = agent.previous_mode
        target, send = agent.act(temp, occ)
        rows.append((step, prev, temp, occ, target, send))
    return rows


def show(title, rows):
    print("\n== " + title + " ==")
    print(f"{'step':<5}{'previous':<10}{'percept':<14}{'target':<8}{'outcome'}")
    for step, prev, t, o, target, send in rows:
        print(f"{step:<5}{str(prev):<10}{str((t, o)):<14}{target:<8}"
              f"{'SEND ' + target if send else 'no command'}")


# ---- Test 1: reflex vs stateful on repeated percepts
base = [(29, True), (29, True), (20, True), (26, True), (19, True), (29, False)]
reflex = ReflexClassroomAgent()
print("== Reflex agent (always issues a command) ==")
for i, p in enumerate(base, 1):
    print(i, p, reflex.act(*p), "-> command sent")
rows_base = run_stateful(base)
show("Stateful agent: repeated percepts + boundaries + empty room", rows_base)
assert [r[4] for r in rows_base] == ["COOL", "COOL", "IDLE", "IDLE", "WARM", "ECO"]
assert [r[5] for r in rows_base] == [True, False, True, False, True, True]

# ---- Test 2: full mode transition
transition = [(29, True), (24, True), (17, True), (17, False), (29, True)]
rows_tr = run_stateful(transition)
show("Mode transition COOL -> IDLE -> WARM -> ECO -> COOL", rows_tr)
assert [r[4] for r in rows_tr] == ["COOL", "IDLE", "WARM", "ECO", "COOL"]
assert all(r[5] for r in rows_tr)

# ---- Test 3: exact boundaries (occupied)
rows_b = run_stateful([(20, True), (26, True), (26.1, True), (19.9, True)])
show("Exact boundaries", rows_b)
assert [r[4] for r in rows_b] == ["IDLE", "IDLE", "COOL", "WARM"]

# ---- Test 4: empty room has priority over temperature
rows_e = run_stateful([(35, False), (10, False), (35, True)])
show("Empty room priority", rows_e)
assert [r[4] for r in rows_e] == ["ECO", "ECO", "COOL"]
assert [r[5] for r in rows_e] == [True, False, True]

# ---- Edge case: noisy sensor around 26 C (no hysteresis)
noisy = [26.2, 25.9, 26.3, 25.8, 26.4, 25.7]
rows_n = run_stateful([(t, True) for t in noisy])
show("EDGE CASE: noisy readings around 26 C (occupied)", rows_n)
sent = sum(r[5] for r in rows_n)
print(f"Commands sent for {len(noisy)} noisy readings: {sent} (chattering)")
assert sent == len(noisy)

# ---- Proposed improvement: hysteresis band (demonstration only)
class HysteresisAgent(StatefulClassroomAgent):
    """Cool above 26, but stay COOL until temp falls to 25 or below."""

    def act(self, temp, occupied):
        if occupied and self.previous_mode == "COOL" and 25 < temp <= 26:
            target = "COOL"
        elif not occupied:
            target = "ECO"
        elif temp > 26:
            target = "COOL"
        elif temp < 20:
            target = "WARM"
        else:
            target = "IDLE"
        send = target != self.previous_mode
        self.previous_mode = target
        return target, send


h = HysteresisAgent()
h_sent = 0
print("\n== Improvement demo: hysteresis band (cool>26, release<=25) ==")
for t in noisy:
    tg, s = h.act(t, True)
    h_sent += s
    print(t, tg, "SEND" if s else "no command")
print(f"Commands sent with hysteresis: {h_sent}")
assert h_sent == 1

# ---- Save complete trace as CSV
with open("outputs/mode_transition_trace.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["test", "step", "previous_mode", "temp_C", "occupied",
                "target_mode", "send_command"])
    for name, rows in [("repeated", rows_base), ("transition", rows_tr),
                       ("boundaries", rows_b), ("empty_room", rows_e),
                       ("noisy_26C", rows_n)]:
        for r in rows:
            w.writerow([name, *r])

print("\nAll checks passed. Trace saved to outputs/mode_transition_trace.csv")
