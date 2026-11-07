# Lab 3 Task 3 (weighted graph, UCS and BFS comparison)
# Edge weights are travel-cost units (all nonnegative). They are a documented lab assumption
# chosen so that BFS (A->C->G, cost 12) and UCS (A->B->E->G, cost 3) differ, as in Manual 3.7.
# C->G is the ADDED corridor; it is not in the original manual trace graph.
import heapq
from collections import deque

weighted = {
    "A": {"B": 1, "C": 5},
    "B": {"D": 4, "E": 1},
    "C": {"F": 3, "G": 7},     # C->G (7) is the added corridor
    "D": {},
    "E": {"G": 1},
    "F": {},
    "G": {},
}
ADDED_EDGES = [("C", "G")]


def ucs(g, start, goal):
    """Uniform-cost search. Returns (path, cost, processing order [(node, g)]).
    Ties are broken by insertion order (counter), which follows successor order."""
    for u in g:
        for v, w in g[u].items():
            if w < 0:
                raise ValueError(f"negative edge {u}->{v}: UCS requires nonnegative costs")
    counter = 0
    frontier = [(0, counter, start, [start])]
    processed, order = set(), []
    while frontier:
        cost, _, node, path = heapq.heappop(frontier)
        if node in processed:
            continue                      # stale, more expensive duplicate entry
        processed.add(node); order.append((node, cost))
        if node == goal:
            return path, cost, order
        for nxt, w in g[node].items():
            if nxt not in processed:
                counter += 1
                heapq.heappush(frontier, (cost + w, counter, nxt, path + [nxt]))
    return None, None, order


def bfs_weighted(g, start, goal):
    """BFS on the same topology, ignoring weights. Returns (path, processing order)."""
    q = deque([(start, [start])]); seen = {start}; order = []
    while q:
        node, path = q.popleft(); order.append(node)
        if node == goal:
            return path, order
        for n in g[node]:
            if n not in seen:
                seen.add(n); q.append((n, path + [n]))
    return None, order


def path_cost(g, path):
    """Independent check: add up the edge weights of a path directly from the table."""
    return sum(g[a][b] for a, b in zip(path, path[1:]))


if __name__ == "__main__":
    print("== Weighted graph (edge: cost) ==")
    for u in weighted:
        for v, w in weighted[u].items():
            note = "  <- added corridor" if (u, v) in ADDED_EDGES else ""
            print(f"{u}->{v}: {w}{note}")

    path, cost, order = ucs(weighted, "A", "G")
    print("\n== UCS (start A, goal G) ==")
    print("Processing order (node, accumulated cost):", order)
    print("Path:", " -> ".join(path), "| hops:", len(path) - 1, "| UCS cost:", cost)
    print("Independent edge sum:", " + ".join(str(weighted[a][b]) for a, b in zip(path, path[1:])),
          "=", path_cost(weighted, path))

    bpath, border = bfs_weighted(weighted, "A", "G")
    print("\n== BFS on the same topology ==")
    print("Processing order:", border)
    print("Path:", " -> ".join(bpath), "| hops:", len(bpath) - 1, "| cost:", path_cost(weighted, bpath),
          "| edge sum:", " + ".join(str(weighted[a][b]) for a, b in zip(bpath, bpath[1:])))

    print("\n== Edge cases ==")
    print("start == goal:", ucs(weighted, "A", "A"))
    w2 = dict(weighted); w2["H"] = {}
    print("unreachable goal H:", ucs(w2, "A", "H")[:2])
    neg = {"A": {"B": 2}, "B": {"C": -1}, "C": {}}
    try:
        ucs(neg, "A", "C")
    except ValueError as e:
        print("negative edge:", e)

    assert path == ["A", "B", "E", "G"] and cost == 3 == path_cost(weighted, path)
    assert bpath == ["A", "C", "G"] and path_cost(weighted, bpath) == 12
    assert len(bpath) - 1 < len(path) - 1
    print("\nAll checks passed.")
