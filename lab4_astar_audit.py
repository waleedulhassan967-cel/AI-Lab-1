# Lab 4 Task 1 (heuristic audit and manual-trace check)
# Checks admissibility (h <= true remaining cost), consistency on every edge, and the first
# three A* expansions against the hand calculation in the report.
import heapq
from lab4_astar import graph, h, astar, astar_trace, print_trace, path_cost


def true_remaining(graph, goal):
    """Exact cheapest remaining cost from every node to the goal (Dijkstra from each node)."""
    out = {}
    for s in graph:
        dist = {s: 0}; pq = [(0, s)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]: continue
            for v, w in graph.get(u, []):
                if d + w < dist.get(v, float("inf")):
                    dist[v] = d + w; heapq.heappush(pq, (d + w, v))
        out[s] = dist.get(goal, float("inf"))
    return out


def audit(graph, h, goal, label):
    print(f"== Heuristic audit: {label} ==")
    true = true_remaining(graph, goal)
    admissible = True
    print(f"{'node':<6}{'h':<5}{'true':<6}{'h <= true?'}")
    for n in graph:
        ok = h[n] <= true[n]; admissible &= ok
        print(f"{n:<6}{h[n]:<5}{true[n]:<6}{'yes' if ok else 'NO (overestimate)'}")
    consistent = True
    print(f"{'edge':<8}{'h(u)':<6}{'cost+h(v)':<12}{'h(u) <= cost+h(v)?'}")
    for u in graph:
        for v, w in graph[u]:
            ok = h[u] <= w + h[v]; consistent &= ok
            print(f"{u}->{v:<5}{h[u]:<6}{str(w) + '+' + str(h[v]) + '=' + str(w + h[v]):<12}{'yes' if ok else 'NO'}")
    print(f"Admissible: {admissible} | Consistent: {consistent}\n")
    return true, admissible, consistent


if __name__ == "__main__":
    print("Supplied run:", astar(graph, h, "S", "G"))
    print()
    true, adm, con = audit(graph, h, "G", "supplied heuristic")
    assert true == {"S": 6, "A": 5, "B": 5, "C": 3, "G": 0} and adm and con

    res = astar_trace(graph, h, "S", "G")
    print_trace("A* trace (first three expansions are S, A, C)", res, graph)
    first3 = [(s["node"], s["g"], s["h"], s["f"]) for s in res["steps"][:3]]
    print("\nFirst three expansions (node, g, h, f):", first3)
    assert first3 == [("S", 0, 5, 5), ("A", 1, 4, 5), ("C", 3, 2, 5)]
    g_entry = res["steps"][2]["frontier"]
    assert g_entry == [(6, 6, "G"), (8, 4, "B")]          # G (6,0,6) beats B (4,4,8)
    assert astar(graph, h, "S", "G") == (res["cost"], res["path"])
    assert path_cost(graph, res["path"]) == 6
    print("All checks passed.")
