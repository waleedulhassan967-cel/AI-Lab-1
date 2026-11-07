# Lab 5 Task 3 (reordering branches) and edge cases
# Reordering swaps the two children of a node; this never changes the Minimax value.
import math
from collections import Counter
from lab5_minimax import minimax, minimax_counted, pad_scores
from lab5_alphabeta import alphabeta, alphabeta_counted, alphabeta_trace


def build(scores):
    """Nested-list complete binary tree from a flat list of leaf scores."""
    if len(scores) == 1:
        return scores[0]
    mid = len(scores) // 2
    return [build(scores[:mid]), build(scores[mid:])]


def flatten(t):
    return [t] if not isinstance(t, list) else flatten(t[0]) + flatten(t[1])


def value(t, is_max):
    if not isinstance(t, list):
        return t
    a, b = value(t[0], not is_max), value(t[1], not is_max)
    return max(a, b) if is_max else min(a, b)


def ordered(t, is_max, best_first):
    """Order children so the better one for the player to move comes first (best_first=True)
    or last (False)."""
    if not isinstance(t, list):
        return t
    kids = [ordered(c, not is_max, best_first) for c in t]
    vals = [value(c, not is_max) for c in kids]
    better_first = (vals[0] >= vals[1]) if is_max else (vals[0] <= vals[1])
    if better_first != best_first:
        kids = kids[::-1]
    return kids


def variants(t):
    """All arrangements obtained by swapping children at any internal node (2^(internal nodes))."""
    if not isinstance(t, list):
        return [t]
    L, R = variants(t[0]), variants(t[1])
    return [[l, r] for l in L for r in R] + [[r, l] for l in L for r in R]


def counts(flat):
    d = int(math.log2(len(flat)))
    cm, ca = {"leaves": 0}, {"leaves": 0}
    vm = minimax_counted(0, 0, True, flat, d, cm)
    va = alphabeta_counted(0, 0, True, flat, d, float('-inf'), float('inf'), ca)
    assert vm == va                      # pruning must never change the value
    return vm, cm["leaves"], ca["leaves"]


if __name__ == "__main__":
    base, depth = pad_scores([3, 5, 2, 9, 0, 7])
    tree = build(base)
    orders = {"original": base,
              "best-first": flatten(ordered(tree, True, True)),
              "worst-first": flatten(ordered(tree, True, False))}
    print("== Task 3: reordering tree 1 (leaf order left to right) ==")
    print(f"{'ordering':<13}{'leaf order':<28}{'value':<7}{'minimax leaves':<16}{'alpha-beta leaves'}")
    for name, flat in orders.items():
        v, m, a = counts(flat)
        print(f"{name:<13}{str(flat):<28}{v:<7}{m:<16}{a}")
    for name, flat in orders.items():
        root, rows, leaves, skipped = alphabeta_trace(flat, depth)
        print(f"  {name}: evaluated leaf positions {leaves}, pruned leaf positions {skipped}")

    allv = variants(tree)
    dist = Counter(); values = set()
    for t in allv:
        v, m, a = counts(flatten(t))
        dist[a] += 1; values.add(v)
    print(f"\nAll {len(allv)} child-swap arrangements of tree 1: root values {sorted(values)}")
    print("alpha-beta leaves evaluated -> number of arrangements:", dict(sorted(dist.items())))
    assert values == {5} and min(dist) <= 8 and max(dist) <= 8

    tree2 = build([3, 5, 2, 9, 3, 5, 2, 9])
    dist2 = Counter(); values2 = set()
    for t in variants(tree2):
        v, m, a = counts(flatten(t)); dist2[a] += 1; values2.add(v)
    print(f"All {sum(dist2.values())} child-swap arrangements of tree 2: root values {sorted(values2)}")
    print("alpha-beta leaves evaluated -> number of arrangements:", dict(sorted(dist2.items())))
    assert values2 == {5}
    for name, flat in (("tree 2 best-first", flatten(ordered(tree2, True, True))),
                       ("tree 2 worst-first", flatten(ordered(tree2, True, False)))):
        v, m, a = counts(flat)
        print(f"{name}: leaf order {flat}, value {v}, alpha-beta leaves {a}")

    print("\n== Edge cases ==")
    # 1. padding value changes the game
    for pad in (0, 100):
        s, d = pad_scores([3, 5, 2, 9, 0, 7], pad)
        print(f"pad with {pad:<3}: tree {s} -> minimax value {minimax(0, 0, True, s, d)}")
    # 2. supplied alphabeta() driver with a non power-of-two list silently drops leaves
    six = [3, 5, 2, 9, 0, 7]
    d_int = int(math.log2(len(six)))
    print("supplied alphabeta driver on 6 scores: depth = int(log2(6)) =", d_int,
          "->", alphabeta(0, 0, True, six, d_int, float('-inf'), float('inf')),
          "(uses only the first 4 leaves; padded tree gives 5)")
    # 3. equal leaves
    eq = [4] * 8
    print("all leaves equal (4):", counts(eq), "(value, minimax leaves, alpha-beta leaves)")
    # 4. single leaf
    print("single leaf [7]:", minimax(0, 0, True, [7], math.ceil(math.log2(1))))
    # 5. negative utilities
    neg = [-3, -5, -2, -9, -1, -7, -4, -8]
    print("negative utilities:", counts(neg))
    s100, d100 = pad_scores([3, 5, 2, 9, 0, 7], 100)
    assert minimax(0, 0, True, s100, d100) == 7
    assert alphabeta(0, 0, True, six, d_int, float('-inf'), float('inf')) == 3
    assert counts(eq)[0] == 4 and counts(neg)[0] == -3
    print("All checks passed.")
