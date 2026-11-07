# Lab 5 Task 2 (alpha-beta: leaf counter and pruning trace)
# alphabeta() is the supplied code from the Lab 5 manual (Section 5.2).
import math
from lab5_minimax import minimax_counted, pad_scores


def alphabeta(depth, index, maxTurn, scores, target, alpha, beta):
    if depth == target:
        return scores[index]
    if maxTurn:
        value = float('-inf')
        for i in range(2):
            value = max(value, alphabeta(depth + 1, index * 2 + i, False, scores, target, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for i in range(2):
            value = min(value, alphabeta(depth + 1, index * 2 + i, True, scores, target, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def alphabeta_counted(depth, index, maxTurn, scores, target, alpha, beta, counter):
    """Same logic as alphabeta(); counter['leaves'] is incremented in the terminal case."""
    if depth == target:
        counter["leaves"] += 1
        return scores[index]
    if maxTurn:
        value = float('-inf')
        for i in range(2):
            value = max(value, alphabeta_counted(depth + 1, index * 2 + i, False, scores, target, alpha, beta, counter))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    value = float('inf')
    for i in range(2):
        value = min(value, alphabeta_counted(depth + 1, index * 2 + i, True, scores, target, alpha, beta, counter))
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value


def alphabeta_trace(scores, target):
    """Same logic again, but records one row per node (pre-order) and the leaves evaluated."""
    rows, leaves = [], []

    def rec(depth, index, maxTurn, alpha, beta):
        if depth == target:
            leaves.append(index)
            return scores[index]
        row = dict(node=f"d{depth}.{index}", kind="MAX" if maxTurn else "MIN", alpha=alpha, beta=beta,
                   visited=0, pruned=False, value=None)
        rows.append(row)
        value = float('-inf') if maxTurn else float('inf')
        for i in range(2):
            child = rec(depth + 1, index * 2 + i, not maxTurn, alpha, beta)
            row["visited"] += 1
            if maxTurn:
                value = max(value, child); alpha = max(alpha, value)
            else:
                value = min(value, child); beta = min(beta, value)
            if alpha >= beta:
                row["pruned"] = i == 0      # pruning only skips the second child
                break
        row["value"] = value
        return value

    root = rec(0, 0, True, float('-inf'), float('inf'))
    skipped = [i for i in range(len(scores)) if i not in leaves]
    return root, rows, leaves, skipped


def show(title, scores):
    depth = int(math.log2(len(scores)))
    root, rows, leaves, skipped = alphabeta_trace(scores, depth)
    print(f"== {title}: leaves {scores} ==")
    print(f"{'node':<7}{'type':<5}{'alpha':<7}{'beta':<7}{'children visited':<18}{'value':<7}pruned")
    for r in rows:
        print(f"{r['node']:<7}{r['kind']:<5}{r['alpha']!s:<7}{r['beta']!s:<7}{r['visited']:<18}{r['value']!s:<7}"
              f"{'YES (2nd child skipped)' if r['pruned'] else 'no'}")
    print("Root value:", root, "| leaves evaluated (index):", leaves, "| leaves pruned (index):", skipped)
    return root, leaves, skipped


if __name__ == "__main__":
    # Tree 1: the Section 5.1 tree, padded with 0 (same tree as Task 1)
    s1, d1 = pad_scores([3, 5, 2, 9, 0, 7])
    r1, l1, k1 = show("Tree 1 (Section 5.1, padded)", s1)
    print()
    # Tree 2: the Section 5.2 tree exactly as supplied
    s2 = [3, 5, 2, 9, 3, 5, 2, 9]
    r2, l2, k2 = show("Tree 2 (Section 5.2 supplied)", s2)
    print("\nSupplied alphabeta() output for tree 2:",
          alphabeta(0, 0, True, s2, int(math.log2(len(s2))), float('-inf'), float('inf')))

    print("\n== Leaf counters: Minimax vs alpha-beta (same ordering) ==")
    for name, s in (("Tree 1", s1), ("Tree 2", s2)):
        d = int(math.log2(len(s)))
        cm, ca = {"leaves": 0}, {"leaves": 0}
        vm = minimax_counted(0, 0, True, s, d, cm)
        va = alphabeta_counted(0, 0, True, s, d, float('-inf'), float('inf'), ca)
        print(f"{name}: minimax value {vm}, leaves {cm['leaves']} | alpha-beta value {va}, leaves {ca['leaves']}")
        assert vm == va and ca["leaves"] <= cm["leaves"]
    assert r1 == 5 and len(l1) == 8 and not k1        # no pruning in the original order of tree 1
    assert r2 == 5 and l2 == [0, 1, 2, 3, 4, 5] and k2 == [6, 7]
    print("All checks passed.")
