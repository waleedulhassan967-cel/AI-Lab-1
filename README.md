# AI Lab 3 - Uninformed Search: BFS, DFS, DLS, IDDFS & UCS

## Files
- `Lab3_Report.docx`: report for Tasks 1-3 (manual traces, DLS/IDDFS results, weighted graph, UCS vs BFS, edge case)
- `lab3_bfs_dfs.py`: supplied BFS/DFS plus traced versions that print the frontier after every step
- `lab3_depth_search.py`: DLS and IDDFS with path-local cycle check (FOUND / CUTOFF / FAILURE) and edge-case tests
- `lab3_ucs.py`: weighted graph, UCS, BFS on the same topology, independent path-cost check
- `outputs/`: captured outputs of the three scripts

## Requirements
- Python 3 (standard library only)
- Microsoft Word or a compatible DOCX reader for the report

## Run
```bash
python lab3_bfs_dfs.py
python lab3_depth_search.py
python lab3_ucs.py
```

Each script uses `assert` statements and prints "All checks passed" or "Verified" on success.

The edge weights and the added corridor C -> G are synthetic lab assumptions (Manual 3.7).
Search counts include the goal node when it is processed.
