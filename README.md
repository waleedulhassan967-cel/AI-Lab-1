# AI Lab 5 - Adversarial Search: Minimax & Alpha-Beta Pruning

## Files
- `Lab5_Report.docx`: report for Tasks 1-3 (manual Minimax trace, leaf counters, alpha-beta trace, reordering experiments, edge cases)
- `lab5_minimax.py`: supplied Minimax, bottom-up level table, root action, and a leaf-counting version
- `lab5_alphabeta.py`: supplied alpha-beta, leaf-counting version, and a per-node pruning trace
- `lab5_reorder.py`: branch reordering (original / best-first / worst-first / all 128 child-swap arrangements) and edge cases
- `outputs/`: captured outputs of the three scripts

## Requirements
- Python 3 (standard library only)
- Microsoft Word or a compatible DOCX reader for the report

## Run
```bash
python lab5_minimax.py
python lab5_alphabeta.py
python lab5_reorder.py
```

Each script uses `assert` statements and prints "All checks passed" on success.

Tree 1 is the Section 5.1 scores [3, 5, 2, 9, 0, 7] padded with 0 to 8 leaves (the padding value is
an assumption of the supplied driver). Tree 2 is the Section 5.2 scores [3, 5, 2, 9, 3, 5, 2, 9].
The leaf counter is incremented in the terminal case.
