"""Independent Rule 1 solver: reads the numbers straight from each question's text and solves it as a
weighted-average / two-equation problem (not with the alligation formula gen.py uses)."""
import re
from fractions import Fraction as F


def nums(q):
    q = re.sub(r"\\frac\{(\d+)\}\{(\d+)\}", r" FRAC\1/\2 ", q)
    return [F(x) for x in re.findall(r"(?<![/\w])\d+(?:\.\d+)?", q)], [F(int(a), int(b)) for a, b in re.findall(r"FRAC(\d+)/(\d+)", q)]


def first_to_second(p1, p2, m):
    """k = first/second with (p1*k + p2) / (k + 1) = m."""
    return ("ratio", (p2 - m) / (m - p1))


def two_by_two(a1, b1, c1, a2, b2, c2):
    """Cramer's rule for a1 u + b1 v = c1, a2 u + b2 v = c2."""
    det = a1 * b2 - a2 * b1
    return (c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det


def solve(rid, q):
    v, fr = nums(q)
    if rid in (680, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066):
        assert len(v) == 3, v
        return first_to_second(*v)
    if rid in (1067, 1069):
        p1, p2, sp = v[:3]
        cp = sp / (1 + fr[0])
        return first_to_second(p1, p2, cp)
    if rid == 1068:
        p1, p2, a, b = v
        return ("money" if False else "number", (p1 * a + p2 * b) / (a + b))
    if rid == 1070:
        wine, m = v
        return first_to_second(F(0), wine, m)            # water first, costs 0
    if rid == 1071:
        p1, p2, total, m = v
        return ("pair", two_by_two(1, 1, total, p1, p2, m * total))
    if rid == 1074:
        total, m, p1, p2 = v
        return ("pair", two_by_two(1, 1, total, p1, p2, m * total))
    if rid == 1072:
        total, cost, better, worse = v
        return ("pair", two_by_two(1, 1, total, better, worse, cost))     # (better, worse)
    if rid == 1073:
        w1, w2, total, m = v
        k, r = two_by_two(2, 1, total, w1 + w2, 0, m * total)              # each lot k, water r
        return ("number", r)
    raise KeyError(rid)
