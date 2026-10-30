"""Independent Rule 6 solver: converts every amount to paise and tries every possible number of boys."""
import re
from fractions import Fraction as F


def amounts(q):
    found = []
    for m in re.finditer(r"(Rs|Re)\s*\\?\(?\s*(\d+(?:\.\d+)?)", q):
        found.append((m.start(), F(m[2]) * 100))
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*(rupees)", q):
        found.append((m.start(), F(m[1]) * 100))
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*\\?\)?\s*(P|paise)\b", q):
        found.append((m.start(), F(m[1])))
    return [v for _, v in sorted(found)]


def solve(rid, q):
    N = int(re.search(r"\d+", q)[0])
    X, x, y = amounts(q)
    boys = [b for b in range(N + 1) if b * x + (N - b) * y == X]
    assert len(boys) == 1, boys
    b, g = F(boys[0]), F(N - boys[0])
    if "ratio of boys to girls" in q:
        return ("ratio", b / g)
    if "girls and boys" in q:
        return ("pair", (g, b))
    return ("pair", (b, g))
