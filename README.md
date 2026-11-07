# AI Lab 4 - Informed Search: Heuristics & A*

## Files
- `Lab4_Report.docx`: report for Tasks 1-3 (heuristic audit, manual g/h/f, A* vs UCS, overestimate experiment, edge case)
- `lab4_astar.py`: supplied A* plus a traced version that records every step and the frontier
- `lab4_astar_audit.py`: admissibility and consistency audit, first-three-expansions check
- `lab4_compare.py`: A* vs UCS control (h = 0), h(C) = 10 experiment, sweep of h(C), edge cases
- `outputs/`: captured outputs of the two runnable scripts

## Requirements
- Python 3 (standard library only)
- Microsoft Word or a compatible DOCX reader for the report

## Run
```bash
python lab4_astar_audit.py
python lab4_compare.py
```

Both scripts use `assert` statements and print "All checks passed" on success.

The graph and heuristic are supplied by the manual and are abstract time estimates.
A node is counted as expanded when its successors are examined; goal processing and
stale queue entries are not counted as expansions.
