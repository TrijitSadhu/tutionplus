"""Independent solver for Ratio and Proportion Rules 26-33, keyed by row id / payload key; reads the numbers from the question in order.
Incomes and expenses: the income multiplier solved from 'income - expense = saving' for both persons (a linear solve, then the
expenses read off). Changed numbers: the multiplier k tried 1, 2, 3 ... until the new ratio fits. Inverse proportion: a real
distance (job) shared out and the times measured. Marbles: totals tried until every share is whole. Sum and difference: the two
numbers themselves. Never the rule formula."""
import re
from fractions import Fraction as F
from math import gcd

from solve_1_5 import vals
from solve_18_25 import plain, three, try_k, two


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def lowest(ts):
    g = 0
    for t in ts:
        g = gcd(g, int(t))
    return tuple(F(int(t) // g) for t in ts)


ROWS = {734: 26, 735: 27, 736: 29, 737: 30, 738: 31, 739: 32, 740: 33}


def solve(k, q):
    try:
        r = ROWS[k] if isinstance(k, int) else int(re.match(r"r(\d+)_", k)[1])
        if r in (26, 27):
            (a, b), (c, d) = two(q)[:2]
            X = F(re.search(r"Rs (\d+)", q)[1])
            kk = lin(lambda t: (a * t - X) * d - (b * t - X) * c)   # the two expenses must be in the ratio c : d
            i1, i2 = a * kk, b * kk
            return ("pair", (i1, i2)) if r == 26 else ("pair", (i1 - X, i2 - X))
        if r in (28, 29, 30, 31):
            (a, b), (c, d) = two(q)[:2]
            x = plain(q, [(a, b), (c, d)])[0]
            s = -1 if "taken" in q else 1
            kk = try_k(lambda t: a * t + s * x > 0 and b * t + s * x > 0 and F(a * t + s * x) / (b * t + s * x) == F(c, d))
            p, qq = a * kk, b * kk
            return ("number", p + qq if "sum" in q else abs(p - qq))
        if r == 32:
            if "marbles" in q:
                fr = [F(int(x), int(y)) for x, y in re.findall(r"\\frac\{(\d+)\}\{(\d+)\}", q)]
                tot = sum(fr)
                n = try_k(lambda t: all((t * f / tot).denominator == 1 for f in fr))
                return ("number", n)
            parts = three(q)[0]
            D = F(parts[0] * parts[1] * parts[2])                    # the same distance / job for all three
            times = [D / p for p in parts]
            return ("terms", lowest(times))
        if r == 33:
            A, a = vals(q)[:2]
            big, small = (A + a) / 2, (A - a) / 2
            return ("ratio", big / small)
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
