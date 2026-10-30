"""Independent Rule 7 solver: one litre of mixture holds w litres of water; its cost (1 - w)x marked up by P%
must equal the selling price y. Solves for w (no rule formula)."""
from fractions import Fraction as F
from validate import numbers


def solve(rid, q):
    v = numbers(q)
    x, y, P = v[:3]
    if "kilolitre" in q:                 # Rs per kilolitre -> paise per litre
        x = x * 100 / 1000
    w = 1 - y / (x * (1 + P / 100))
    if "water to milk" in q:
        return ("ratio", w / (1 - w))
    if "each litre" in q:
        return ("number", w)
    return ("ratio", (1 - w) / w)
