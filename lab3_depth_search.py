# Lab 3 Task 2 (DLS and IDDFS with path-local cycle check)
# Depth counts edges; the root has depth 0. Status is FOUND, CUTOFF or FAILURE.
from lab3_bfs_dfs import graph

FOUND, CUTOFF, FAILURE = "FOUND", "CUTOFF", "FAILURE"


def dls(g, node, goal, limit, path, visited):
    """Depth-limited DFS. 'path' is the current path only (path-local cycle check)."""
    visited.append(node)
    if node == goal:
        return FOUND, path
    children = [n for n in g.get(node, []) if n not in path]   # skip nodes already on this path
    if limit == 0:
        # at the limit: CUTOFF if a deeper continuation exists, otherwise this branch is exhausted
        return (CUTOFF, None) if children else (FAILURE, None)
    cutoff = False
    for n in children:
        status, result = dls(g, n, goal, limit - 1, path + [n], visited)
        if status == FOUND:
            return FOUND, result
        if status == CUTOFF:
            cutoff = True
    return (CUTOFF, None) if cutoff else (FAILURE, None)


def run_dls(g, start, goal, limit):
    visited = []
    status, path = dls(g, start, goal, limit, [start], visited)
    return status, path, visited


def iddfs(g, start, goal, max_depth):
    """Repeat DLS with limits 0,1,2,... A fresh path-local check is used every iteration
    (no global visited set is carried between limits)."""
    attempts = []
    for limit in range(max_depth + 1):
        status, path, visited = run_dls(g, start, goal, limit)
        attempts.append((limit, status, path, len(visited)))
        if status == FOUND:
            return FOUND, path, attempts
        if status == FAILURE:          # whole reachable space exhausted: deeper limits cannot help
            return FAILURE, None, attempts
    return CUTOFF, None, attempts


def fmt(path):
    return " -> ".join(path) if path else "None"


if __name__ == "__main__":
    print("== DLS on the original graph (start A, goal G) ==")
    for limit in (1, 2, 3, 4):
        status, path, visited = run_dls(graph, "A", "G", limit)
        print(f"limit {limit}: {status:<8} path={fmt(path):<14} visited={visited}")

    print("\n== IDDFS on the original graph ==")
    for m in (1, 2, 3, 4):
        status, path, attempts = iddfs(graph, "A", "G", m)
        print(f"max depth {m}: {status:<8} path={fmt(path):<14} limits attempted={[a[0] for a in attempts]}"
              f" total node visits={sum(a[3] for a in attempts)}")
        for limit, st, p, n in attempts:
            print(f"    limit {limit}: {st:<8} visits={n}")

    print("\n== Edge cases ==")
    s, p, v = run_dls(graph, "A", "A", 0)
    print("start == goal (limit 0):", s, fmt(p), "visited", v)

    g_iso = dict(graph); g_iso["H"] = []          # H exists but has no corridor to it
    s, p, v = run_dls(g_iso, "A", "H", 10)
    print("unreachable goal H, limit 10:", s, "visited", v)
    s2, p2, a2 = iddfs(g_iso, "A", "H", 10)
    print("IDDFS unreachable goal H, max 10:", s2, "limits attempted", [a[0] for a in a2])

    cyc = {"A": ["B"], "B": ["A", "C"], "C": []}   # A <-> B is a cycle
    s, p, v = run_dls(cyc, "A", "D", 6)
    print("cycle graph A<->B, goal D unreachable, limit 6:", s, "visited", v)
    s, p, v = run_dls(cyc, "A", "C", 6)
    print("cycle graph A<->B, goal C, limit 6:", s, fmt(p), "visited", v)

    # bounded-search caution
    s, p, v = run_dls(graph, "A", "G", 2)
    print("limit 2 on original graph:", s, "-> bounded result only, NOT proof that G is unreachable")

    assert [run_dls(graph, "A", "G", L)[0] for L in (1, 2, 3, 4)] == [CUTOFF, CUTOFF, FOUND, FOUND]
    assert run_dls(graph, "A", "G", 3)[1] == ["A", "B", "E", "G"]
    assert iddfs(graph, "A", "G", 2)[0] == CUTOFF and iddfs(graph, "A", "G", 3)[0] == FOUND
    assert run_dls(g_iso, "A", "H", 10)[0] == FAILURE
    assert run_dls(cyc, "A", "D", 6)[0] == FAILURE
    print("\nAll checks passed.")
