"""Independent solver for Ratio and Proportion Rules 34-39, keyed by row id / payload key; reads the numbers from the question in order.
Added / taken numbers: every whole number tried until the new ratio comes out. Vessels: every vessel size (in half litres) tried -
the mixture is actually drawn off in its own ratio and topped up, then the ratio is measured. Wage bill: workers x pay before and
after. Candles: the heights checked minute by minute. Never the rule formula."""
import re
from fractions import Fraction as F

from solve_18_25 import plain, two


def red(x, y):
    return ("ratio", F(x) / F(y))


ROWS = {741: 34, 742: 35, 743: 37, 744: 38, 745: 39}


def vessel(a, b, q, c, d, filler):
    for i in range(1, 20000):
        V = F(i, 2)
        if V <= q:
            continue
        A, Bq = V * F(a, a + b), V * F(b, a + b)
        A, Bq = A - q * F(a, a + b), Bq - q * F(b, a + b)        # draw off q litres of the mixture
        if filler == "A":
            A += q
        else:
            Bq += q
        if A / Bq == F(c, d):
            return V
    raise ValueError("no vessel")


def solve(k, q):
    try:
        r = ROWS[k] if isinstance(k, int) else int(re.match(r"r(\d+)_", k)[1])
        rs = two(q)
        if r in (34, 35):
            (a, b), (c, d) = rs[:2]
            s = -1 if r == 35 else 1
            for x in range(1, 5000):
                if a + s * x > 0 and F(a + s * x, b + s * x) == F(c, d):
                    return ("number", F(x))
            return ("unsolved", "no x")
        if r in (36, 37):
            (a, b), (c, d) = rs[:2]
            qq = plain(q, rs[:2])[0]
            filler = "A" if "amount of P" in q else "B"
            V = vessel(a, b, qq, c, d, filler)
            A, Bq = V * F(a, a + b), V * F(b, a + b)
            if r == 37:
                return ("number", V)
            if "how much does the tank hold" in q:
                return ("pair", (Bq, V))
            return ("number", A if "liquid A was" in q else Bq)
        if r == 38:
            (p, qq), (rr, s) = rs[:2]
            workers_old, workers_new = p * 10, qq * 10
            pay_old, pay_new = rr * 100, s * 100
            return red(workers_old * pay_old, workers_new * pay_new)
        if r == 39:
            (x, y) = rs[0]
            T1, T2 = [F(t) for t in re.findall(r"in (\d+) hours", q)][:2]
            for minute in range(1, int(T2 * 60)):
                t = F(minute, 60)
                h1, h2 = 1 - t / T1, 1 - t / T2
                if h1 / h2 == F(x, y):
                    return ("pair", (F(minute // 60), F(minute % 60)))
            return ("unsolved", "no time")
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
