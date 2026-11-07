# Lab 4 Tasks 2-3 (A* vs UCS control, overestimate experiment, edge cases)
from lab4_astar import graph, h, astar_trace, print_trace, path_cost
from lab4_astar_audit import audit

h_zero = {n: 0 for n in h}                      # UCS control: same code, h = 0 everywhere
h_over = dict(h); h_over["C"] = 10              # ONE value changed: h(C) 2 -> 10


def summary(name, res):
    return (f"{name:<22}{' -> '.join(res['path']) if res['path'] else 'None':<18}"
            f"cost={res['cost']!s:<5}independent={path_cost(graph, res['path']) if res['path'] else None!s:<5}"
            f"expanded={len(res['expanded'])} {res['expanded']} stale={res['stale']}")


if __name__ == "__main__":
    astar_res = astar_trace(graph, h, "S", "G")
    ucs_res = astar_trace(graph, h_zero, "S", "G")
    print_trace("A* (supplied heuristic)", astar_res, graph); print()
    print_trace("UCS control (h = 0 everywhere)", ucs_res, graph); print()
    print("== Task 2 comparison (same graph, start S, goal G; goal excluded from expansion count) ==")
    print(summary("A* (supplied h)", astar_res)); print(summary("UCS control (h=0)", ucs_res))
    assert astar_res["cost"] == ucs_res["cost"] == 6
    assert astar_res["expanded"] == ["S", "A", "C"] and ucs_res["expanded"] == ["S", "A", "C", "B"]

    print("\n== Task 3: overestimate experiment (only h(C) changed: 2 -> 10; true remaining cost of C = 3) ==")
    audit(graph, h_over, "G", "h(C) = 10")
    over_res = astar_trace(graph, h_over, "S", "G")
    print_trace("A* with h(C)=10", over_res, graph); print()
    print(summary("A* original h", astar_res)); print(summary("A* h(C)=10", over_res))
    assert over_res["path"] == ["S", "B", "G"] and over_res["cost"] == 9
    assert "C" not in over_res["expanded"] and over_res["expanded"] == ["S", "A", "B"]

    print("\n== Sweep: other overestimates of h(C) (true remaining cost 3) ==")
    print(f"{'h(C)':<6}{'path':<18}{'cost':<6}{'expanded':<22}{'result'}")
    sweep = []
    for val in range(2, 13):
        hv = dict(h); hv["C"] = val
        r = astar_trace(graph, hv, "S", "G")
        status = "optimal" if r["cost"] == 6 else "NOT optimal"
        sweep.append((val, r["path"], r["cost"], r["expanded"], status))
        print(f"{val:<6}{' -> '.join(r['path']):<18}{r['cost']:<6}{str(r['expanded']):<22}{status}")
    assert [s[4] for s in sweep if s[0] <= 6] == ["optimal"] * 5       # 2..6 unchanged (4,5,6 overestimate!)
    assert all(s[4] == "NOT optimal" for s in sweep if s[0] >= 7)

    print("\n== Edge cases ==")
    r = astar_trace(graph, h, "S", "S")
    print("start == goal:", r["path"], r["cost"], "expanded", r["expanded"])
    g2 = dict(graph); g2["Z"] = []; h2 = dict(h); h2["Z"] = 0
    r = astar_trace(g2, h2, "S", "Z")
    print("unreachable goal Z:", r["path"], r["cost"], "expanded", r["expanded"])
    # a graph where a node is reached twice, so a stale entry appears
    g3 = {"S": [("A", 5), ("B", 1)], "B": [("A", 1)], "A": [("G", 10)], "G": []}
    h3 = {"S": 0, "A": 0, "B": 0, "G": 0}
    r = astar_trace(g3, h3, "S", "G")
    print("improved-path graph:", r["path"], r["cost"], "expanded", r["expanded"], "stale ignored", r["stale"])
    assert r["stale"] == 1 and r["cost"] == 12 and r["path"] == ["S", "B", "A", "G"]
    print("\nAll checks passed.")
