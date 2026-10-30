"""Independent solver for Average Rules 12-17, keyed by row id / payload key; reads the numbers from the question in order and
searches: the number who passed by trying every head count, the middle result by trying every whole number until the group totals
fit, the innings averages by a linear solve of the before/after totals - never the rule formula."""
import re
from fractions import Fraction as F


def nums(q):
    return [F(t) for t in re.findall(r"\d+(?:\.\d+)?", q)]


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def passed(n, T, P, Fl):
    hits = [p for p in range(int(n) + 1) if p * P + (n - p) * Fl == n * T]
    assert len(hits) == 1
    return F(hits[0])


def middle_shared(n, a, b, c):
    """odd n; the first k and the last k (k = (n+1)/2) share the middle result."""
    k = (n + 1) / 2
    hits = [m for m in range(1, 10000) if (k * b - m) + m + (k * c - m) == n * a]
    assert len(hits) == 1
    return F(hits[0])


def between(n, a, p, b, q, c, step=F(1, 100)):
    hits = [i * step for i in range(1, int(n * a / step) + 1) if p * b + i * step + q * c == n * a]
    assert len(hits) == 1
    return hits[0]


def solve(k, q):
    try:
        v = nums(q)
        if k == 506 or str(k).startswith("r12_"):
            return ("number", passed(*v[:4]))
        if k == 507 or str(k).startswith("r13_"):
            n = v[0]
            return ("number", n - passed(*v[:4]))
        if k == 508 or str(k).startswith("r14_"):              # n, a, k, b, k, c
            n, a, _, b, _, c = v[:6]
            return ("number", middle_shared(n, a, b, c))
        if k in ("r15_ex", "r15_e2", "r15_e3", "r15_e4", "r15_e5"):   # n, a, p, b, q, c
            n, a, p, b, qq, c = v[:6]
            return ("number", between(n, a, p, b, qq, c, F(1)))
        if k == "r15_e1":                                      # the number between the groups is left out
            n, a, p, b, qq, c = v[:6]
            mid = between(n, a, p, b, qq, c)
            return ("number", (n * a - mid) / (n - 1))
        if k == 509 or k in ("r16_e1", "r16_e3", "r16_e4", "r16_e5"):   # score, n, rise
            x, n, y = v[:3]
        elif k == "r16_e2":                                    # nth innings, out d short of a century
            n, d, y = v[:3]
            x = 100 - d
        else:
            x = None
        if x is not None:
            A = lin(lambda A: ((n - 1) * A + x) / n - (A + y))  # A = average before the innings
            return ("number", A + y)
        if k in (510, "r17_e2", "r17_e3", "r17_e4"):           # n innings, average x, target y
            n, x, y = v[:3]
        elif k in ("r17_e1", "r17_e5"):                        # average x from n innings, target y
            x, n, y = v[:3]
        else:
            return ("unsolved", "unknown key")
        return ("number", lin(lambda r: (n * x + r) / (n + 1) - y))
    except Exception:
        return ("unsolved", q[:40])
