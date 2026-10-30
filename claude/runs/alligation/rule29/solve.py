"""Independent Rule 29 solver: tries every whole-litre cask size, simulates the two draw-and-refill operations
litre by litre and keeps the size that gives the stated ratio (no rule formula)."""
import re
from fractions import Fraction as F
from validate import numbers


def solve(rid, q):
    L = numbers(q)[0]
    a, b = (F(x) for x in re.findall(r"(\d+)\s*:\s*(\d+)", q)[-1])
    hits = []
    for C in range(int(L) + 1, 2001):
        first = F(C)
        for _ in range(2):
            first -= first * L / C
        if first * b == (C - first) * a:
            hits.append(F(C))
    assert len(hits) == 1, hits
    return ("number", hits[0])
