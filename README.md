# AI Lab 2 - Intelligent Agents & the PEAS Framework

## Files
- `Lab2_Report.docx`: report for Tasks 1-3 (PEAS, environment classification, reflex vs stateful agent, edge case)
- `lab2_percepts.py`: reflex classroom agent with the percept/action trace
- `lab2_model.py`: reflex agent and stateful agent that remembers the previous mode
- `lab2_check.py`: tests for repeated percepts, exact boundaries, mode transition, empty room and a noisy edge case
- `outputs/`: captured outputs and `mode_transition_trace.csv`

## Requirements
- Python 3
- Microsoft Word or a compatible DOCX reader for the report

## Run
```bash
python lab2_percepts.py
python lab2_check.py
```

Temperature is in degrees Celsius. `ECO`, `COOL`, `WARM` and `IDLE` are simulated mode labels,
not real hardware control. An empty room has priority over temperature.
