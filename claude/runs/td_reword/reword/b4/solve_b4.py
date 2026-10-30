"""Independent solver for Time & Distance rewording batch 4 (Rules 34-48), keyed by row id. Reads the numbers from the question
in order and finds the answer by searching for the speed/distance that makes the story's own times agree, adding up the legs,
or counting leaps - never through the rule formulas gen_b4.py uses."""
from fractions import Fraction as F
from validate import numbers


def search(ok, step=F(1, 20), top=5000):
    k = 1
    while k * step <= top:
        if ok(k * step):
            return k * step
        k += 1
    raise ValueError("no answer")


def solve(rid, q):
    try:
        v = numbers(q)
        if rid in (1568, 1569, 1571):                  # faster a saves m1 min, slower b costs m2 min
            a, m1, b, m2 = v[:4]
            # for a trial speed S the first condition gives the distance; keep the S where the second condition also holds
            def dist(S):
                return S * (S + a) / a * m1 / 60
            S = search(lambda S: S > b and dist(S) / (S - b) - dist(S) / S == m2 / 60, F(1, 4), 500)
            return ("number", dist(S) if rid == 1568 else S)
        if rid in (1577, 1580, 1581):                  # d1 km in t1 h, d2 km in t2 h
            d1, t1, d2, t2 = v[:4]
            return ("number", (d1 + d2) / (t1 + t2))
        if rid in (1579, 1584):                        # three (km, km/hr) legs
            legs = list(zip(v[0:6:2], v[1:6:2]))
            return ("number", sum(d for d, s in legs) / sum(d / s for d, s in legs))
        if rid == 1582:                                # three (hours, km/hr) legs
            legs = list(zip(v[0:6:2], v[1:6:2]))
            return ("number", sum(t * s for t, s in legs) / sum(t for t, s in legs))
        if rid in (1587, 1588, 1589):                  # T hours, x faster, t hours
            T, x, t = v[:3]
            return ("number", search(lambda S: S * T == (S + x) * t, F(1, 2), 1000))
        if rid == 1593:                                # D km in T h at x and y: km at x
            D, T, x, y = v[:4]
            return ("number", search(lambda d: d / x + (D - d) / y == T, F(1, 2), D))
        if rid in (1594, 1595, 1596):                  # time (min or h), fraction, x, y
            T, f, x, y = v[:4]
            Th = T / 60 if "minutes" in q else T
            return ("number", search(lambda D: f * D / x + (1 - f) * D / y == Th, F(1, 20), 1000))
        if rid == 1601:                                # thief speed, hours, minutes, owner speed
            x, hh, mm, y = v[:4]
            lead = x * (hh + mm / 60)
            return ("number", search(lambda c: y * c == lead + x * c, F(1, 20), 100))
        if rid in (1610, 1612):                        # speed ratio a : b, minutes more for A
            a, b, mins = v[:3]
            tb = search(lambda tb: tb * b / a - tb == mins / 60, F(1, 60), 100)    # same distance: times opposite to speeds
            return ("pair", (tb * b / a, tb))
        if rid in (1614, 1615, 1616, 1617):            # fraction, s1, s2, D km
            f, s1, s2, D = v[:4]
            return ("number", D / (f * D / s1 + (1 - f) * D / s2))
        if rid == 1632:                                # L hare leaps ahead; hare h while greyhound g; g1 greyhound leaps = h1 hare leaps
            L, h, g, g1, h1 = v[:5]
            leaps, gap = 0, L * g1                     # count in units of 1/g1 hare leap so every step is exact
            while gap > 0:                             # one round: greyhound makes g leaps, hare h leaps
                gap -= g * h1 - h * g1
                leaps += g
            # back up inside the last round to the exact leap where he draws level
            per_leap = (g * h1 - h * g1) / g
            return ("number", leaps + gap / per_leap)
        raise KeyError(rid)
    except Exception:
        return ("unsolved", q[:40])
