# Lab 4 shared module: supplied A* plus a traced version (same logic, records every step)
# astar() and the graph/heuristic are from the Lab 4 manual (Section 4.2).
# Queue entries are (f, g, node, path); ties on f are broken by smaller g, then node name.
import heapq


def astar(graph, h, start, goal):
    pq = [(h[start], 0, start, [start])]; best = {start: 0}
    while pq:
        f, g, node, path = heapq.heappop(pq)
        if node == goal: return g, path
        if g != best[node]: continue
        for nxt, w in graph.get(node, []):
            ng = g + w
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                heapq.heappush(pq, (ng + h[nxt], ng, nxt, path + [nxt]))


graph = {"S": [("A", 1), ("B", 4)], "A": [("C", 2)], "B": [("G", 5)], "C": [("G", 3)], "G": []}
h = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}


def astar_trace(graph, h, start, goal):
    """Same logic as astar(). Expansion = successors examined (goal and stale entries excluded)."""
    pq = [(h[start], 0, start, [start])]; best = {start: 0}
    steps, expanded, stale = [], [], 0
    cost = path = None
    while pq:
        f, g, node, p = heapq.heappop(pq)
        if node == goal:
            steps.append(dict(step=len(steps) + 1, event="goal processed", node=node, g=g, h=h[node], f=f,
                              succ=[], frontier=sorted((e[0], e[1], e[2]) for e in pq)))
            cost, path = g, p
            break
        if g != best[node]:
            stale += 1
            steps.append(dict(step=len(steps) + 1, event="stale ignored", node=node, g=g, h=h[node], f=f,
                              succ=[], frontier=sorted((e[0], e[1], e[2]) for e in pq)))
            continue
        succ = []
        for nxt, w in graph.get(node, []):
            ng = g + w
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                heapq.heappush(pq, (ng + h[nxt], ng, nxt, p + [nxt]))
                succ.append(dict(node=nxt, w=w, g=ng, h=h[nxt], f=ng + h[nxt], pushed=True))
            else:
                succ.append(dict(node=nxt, w=w, g=ng, h=h[nxt], f=ng + h[nxt], pushed=False,
                                 best=best[nxt]))
        expanded.append(node)
        steps.append(dict(step=len(steps) + 1, event="expanded", node=node, g=g, h=h[node], f=f,
                          succ=succ, frontier=sorted((e[0], e[1], e[2]) for e in pq)))
    return dict(cost=cost, path=path, expanded=expanded, stale=stale, steps=steps)


def path_cost(graph, path):
    """Independent check: add edge weights straight from the graph table."""
    total = 0
    for a, b in zip(path, path[1:]):
        total += dict(graph[a])[b]
    return total


def fmt_frontier(fr):
    return "[" + ", ".join(f"({n}: f={f}, g={g})" for f, g, n in fr) + "]"


def print_trace(title, res, graph):
    print(f"== {title} ==")
    for s in res["steps"]:
        print(f"step {s['step']}: {s['event']:<15} {s['node']} (g={s['g']}, h={s['h']}, f={s['f']})")
        for c in s["succ"]:
            tag = "pushed" if c["pushed"] else f"not pushed (best known g={c['best']})"
            print(f"    -> {c['node']}: g = {s['g']} + {c['w']} = {c['g']}, f = {c['g']} + {c['h']} = {c['f']}  {tag}")
        print("    frontier after:", fmt_frontier(s["frontier"]))
    if res["path"]:
        print("Path:", " -> ".join(res["path"]), "| returned cost:", res["cost"],
              "| independent sum:", path_cost(graph, res["path"]))
    else:
        print("Path: None")
    print("Expanded (successors examined):", res["expanded"], "| count:", len(res["expanded"]),
          "| stale entries ignored:", res["stale"])
