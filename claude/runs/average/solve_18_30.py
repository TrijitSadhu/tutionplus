"""Independent solver for Average Rules 18-30, keyed by row id / payload key. Speeds: a real trip of 1000 km split as the question says,
time added stretch by stretch, distance over time. Head counts: every count tried until the totals balance. Mess bill and the
container: a linear solve of the before / after totals. Number series: the actual list is built and averaged. Never the rule formula.
Numbers are read in order; \\frac{a}{b} and p% are read as one fraction each."""
import re
from fractions import Fraction as F


def vals(q):
    out = []
    for a, b, pc, n in re.findall(r"\\frac\{(\d+)\}\{(\d+)\}|(\d+(?:\.\d+)?)%|(\d+(?:\.\d+)?)", q):
        out.append(F(int(a), int(b)) if a else F(pc) / 100 if pc else F(n))
    return out


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def mean(xs):
    return F(sum(xs), len(xs))


def trip(parts):
    """parts of (distance, speed): total distance over total time, hour by hour sums."""
    return sum(d for d, _ in parts) / sum(d / s for d, s in parts)


def count_balance(x, n, y, z):
    """n at y and m at z must average x -> m (tried one by one)."""
    hits = [m for m in range(1, 20000) if n * y + m * z == x * (n + m)]
    assert len(hits) == 1
    return F(hits[0])


def listed(q):
    v = [int(t) for t in re.findall(r"\d+", q)]
    if r"\ldots" in q:                                   # a, b, c, ..., last (a count may come first)
        a, b, _, last = v[-4:]
        return list(range(a, last + 1, b - a))
    return v


def solve(k, q):
    try:
        v = vals(q)
        r = int(re.match(r"r(\d+)_", k)[1]) if isinstance(k, str) else {511: 18, 512: 19, 513: 20, 515: 21, 514: 22, 516: 24, 517: 25, 518: 26}[k]
        if r == 18:
            x, y = v[:2]
            return ("number", trip([(500, x), (500, y)]))
        if r == 19:
            return ("number", trip([(F(1000, 3), s) for s in v[:3]]))
        if r == 20:
            return ("number", trip([(v[i], v[i + 1]) for i in (0, 2, 4)]))
        if r == 21:
            if k == "r21_e5":                            # speed first, then its share
                s1, f1, s2, f2, s3 = v[:5]
            elif k == "r21_e1":                          # each third
                f1, s1, s2, s3 = v[:4]
                f2 = f1
            else:
                f1, s1, f2, s2, s3 = v[:5]
            return ("number", trip([(1000 * f1, s1), (1000 * f2, s2), (1000 * (1 - f1 - f2), s3)]))
        if r == 22:
            x, n, y, z = v[:4]
            return ("number", count_balance(x, n, y, z))
        if r == 23:
            x, y, z, n = v[:4]
            boys = count_balance(x, n, z, y)
            return ("number", boys + n if "in all" in q else boys)
        if r == 24:
            N, z, y, x = v[:4]
            A = lin(lambda A: N * A + y - (N + z) * (A - x))
            return ("number", N * A)
        if r == 25:
            n = int(max(v))
            return ("number", mean(range(1, n + 1)))
        if r == 26:
            n, a, rise = v[:3]
            items = [a] * int(n)
            return ("number", lin(lambda w: mean(items + [w]) - (a + rise)))
        if r in (27, 28):
            xs = list(range(int(v[0]), int(v[1]) + 1)) if k == "r28_e3" else listed(q)
            return ("number", mean(xs))
        if r == 29:
            return ("number", mean(range(1, int(max(v)) + 1, 2)))
        if r == 30:
            return ("number", mean(range(2, int(max(v)) + 1, 2)))
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
