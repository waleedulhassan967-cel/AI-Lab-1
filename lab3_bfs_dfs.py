# Lab 3 Task 1 (BFS and DFS with manual-trace output)
# Supplied graph and supplied bfs/dfs code are from the Lab 3 manual (Section 3.2).
# Trace convention: a node is "processed" when it is removed from the queue/stack;
# the goal is included; already-processed duplicates are skipped.
from collections import deque

graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": ["G"], "F": [], "G": []}


def bfs(start, goal):
    q = deque([(start, [start])]); seen = {start}
    while q:
        node, path = q.popleft()
        if node == goal: return path
        for n in graph[node]:
            if n not in seen:
                seen.add(n); q.append((n, path + [n]))


def dfs(start, goal):
    stack = [(start, [start])]; seen = set()
    while stack:
        node, path = stack.pop()
        if node == goal: return path
        if node in seen: continue
        seen.add(node)
        for n in reversed(graph[node]): stack.append((n, path + [n]))


def bfs_trace(start, goal):
    """Same logic as bfs(), but records every processed node and the frontier."""
    q = deque([(start, [start])]); seen = {start}
    steps, order = [], []
    while q:
        node, path = q.popleft()
        order.append(node)
        if node == goal:
            steps.append((len(order), node, [x for x, _ in q], path, "goal"))
            return path, order, steps
        for n in graph[node]:
            if n not in seen:
                seen.add(n); q.append((n, path + [n]))
        steps.append((len(order), node, [x for x, _ in q], path, ""))
    return None, order, steps


def dfs_trace(start, goal):
    """Same logic as dfs(); stack is listed bottom -> top (top is popped next)."""
    stack = [(start, [start])]; seen = set()
    steps, order = [], []
    while stack:
        node, path = stack.pop()
        if node == goal:
            order.append(node)
            steps.append((len(order), node, [x for x, _ in stack], path, "goal"))
            return path, order, steps
        if node in seen:
            steps.append((len(order), node, [x for x, _ in stack], path, "duplicate skipped"))
            continue
        seen.add(node); order.append(node)
        for n in reversed(graph[node]): stack.append((n, path + [n]))
        steps.append((len(order), node, [x for x, _ in stack], path, ""))
    return None, order, steps


def show(name, path, order, steps, frontier_name):
    print(f"== {name} trace (start A, goal G) ==")
    print(f"{'step':<5}{'processed':<11}{frontier_name:<22}{'path to node'}")
    for s, node, fr, p, note in steps:
        print(f"{s:<5}{node:<11}{str(fr):<22}{'->'.join(p)} {note}")
    print("Final path :", " -> ".join(path))
    print("Visit order:", ", ".join(order), f"({len(order)} nodes processed, goal included)")


if __name__ == "__main__":
    bp, bo, bs = bfs_trace("A", "G")
    dp, do, ds = dfs_trace("A", "G")
    show("BFS", bp, bo, bs, "queue (front->back)")
    print()
    show("DFS", dp, do, ds, "stack (bottom->top)")
    print()
    # verify against the supplied code
    assert bp == bfs("A", "G") and dp == dfs("A", "G")
    assert bo == list("ABCDEFG") and do == list("ABDEG")
    print("Verified: traced paths equal supplied bfs()/dfs() output:")
    print(bfs("A", "G")); print(dfs("A", "G"))
