# Lab 5 Tasks 1-2 (Minimax: manual bottom-up trace and leaf counter)
# minimax() is the supplied code from the Lab 5 manual (Section 5.1).
import math


def minimax(curDepth, nodeIndex, maxTurn, scores, targetDepth):
    # Base case: targetDepth reached
    if curDepth == targetDepth:
        return scores[nodeIndex]
    if maxTurn:
        return max(
            minimax(curDepth + 1, nodeIndex * 2, False, scores, targetDepth),
            minimax(curDepth + 1, nodeIndex * 2 + 1, False, scores, targetDepth))
    else:
        return min(
            minimax(curDepth + 1, nodeIndex * 2, True, scores, targetDepth),
            minimax(curDepth + 1, nodeIndex * 2 + 1, True, scores, targetDepth))


def minimax_counted(curDepth, nodeIndex, maxTurn, scores, targetDepth, counter):
    """Same logic as minimax(); counter['leaves'] is incremented in the terminal case."""
    if curDepth == targetDepth:
        counter["leaves"] += 1
        return scores[nodeIndex]
    vals = [minimax_counted(curDepth + 1, nodeIndex * 2 + i, not maxTurn, scores, targetDepth, counter)
            for i in range(2)]
    return max(vals) if maxTurn else min(vals)


def pad_scores(scores, pad_value=0):
    """Pad to a complete binary tree exactly like the supplied driver (pad value 0 by default)."""
    s = list(scores)
    depth = math.ceil(math.log2(len(s)))
    s += [pad_value] * (2 ** depth - len(s))
    return s, depth


def level_table(scores, depth):
    """Bottom-up values of every node. Level 0 is the root (MAX); levels alternate MAX/MIN."""
    levels = {depth: list(scores)}
    for d in range(depth - 1, -1, -1):
        is_max = (d % 2 == 0)
        prev = levels[d + 1]
        levels[d] = [(max if is_max else min)(prev[2 * i], prev[2 * i + 1]) for i in range(len(prev) // 2)]
    return levels


def root_action(scores, depth):
    """Index of the root child (0 = left, 1 = right) with the higher Minimax value (first on ties)."""
    vals = [minimax(1, i, False, scores, depth) for i in range(2)]
    return vals, vals.index(max(vals))


if __name__ == "__main__":
    scores, depth = pad_scores([3, 5, 2, 9, 0, 7])
    print("Supplied tree: scores padded with 0 to", scores, "| depth", depth)
    print("The optimal value is:", minimax(0, 0, True, scores, depth))
    print("\n== Manual bottom-up trace (level: node values left to right) ==")
    lv = level_table(scores, depth)
    for d in range(depth, -1, -1):
        kind = "leaves" if d == depth else ("MAX" if d % 2 == 0 else "MIN")
        print(f"level {d} ({kind}): {lv[d]}")
    print("Root children values (MIN nodes):", lv[1], "-> MAX picks", max(lv[1]))
    vals, act = root_action(scores, depth)
    print("Chosen root action:", ["Left", "Right"][act], "with value", vals[act])
    c = {"leaves": 0}
    v = minimax_counted(0, 0, True, scores, depth, c)
    print("Counted minimax:", v, "| leaves evaluated:", c["leaves"], "of", len(scores))
    assert v == minimax(0, 0, True, scores, depth) == 5 and c["leaves"] == 8 and act == 0
    assert lv[2] == [5, 9, 7, 0] and lv[1] == [5, 0]
    print("All checks passed.")
