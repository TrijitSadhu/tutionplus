"""Independent solver for Time & Distance rewording batch 3 (Rules 14-29), keyed by row id. Reads the numbers from the question
in order and finds the answer by moving the travellers in small time steps, searching for the value that makes the story's
times agree, or checking speeds against both conditions - never through the rule formulas gen_b3.py uses."""
from fractions import Fraction as F
from validate import numbers


def search(ok, step=F(1, 20), top=5000, start=1):
    k = start
    while k * step <= top:
        if ok(k * step):
            return k * step
        k += 1
    raise ValueError("no answer")


def solve(rid, q):
    try:
        v = numbers(q)
        if rid in (1487, 1488):                        # D, slow a, fast b: B bounces at Q - follow the two stages
            D, a, b = v[:3]
            t_q = D / b                                # B reaches Q
            gap = D - a * t_q                          # A is still this far from Q
            t = t_q + gap / (a + b)                    # then they close the gap head-on
            return ("number", a * t if rid == 1487 else b * t)
        if rid in (1490, 1491, 1492):                  # after crossing: t1 (first), t2 (second), first speed
            t1, t2, s1 = v[:3]
            s2 = search(lambda s: (s1 * (s * t2 / s1)) == s * t2 and s * (s * t2 / s1) == s1 * t1, F(1, 4), 500)
            return ("number", s2)
        if rid == 1500:                                # x, y, extra minutes
            x, y, m = v[:3]
            return ("number", search(lambda D: D / x - D / y == m / 60))
        if rid == 1501:                                # uniform v, out a, back b, extra minutes
            vv, a, b, m = v[:4]
            return ("number", search(lambda D: D / a + D / b - 2 * D / vv == m / 60))
        if rid in (1503, 1504):                        # walker km/hr, minutes, metres
            w, mins, metres = v[:3]
            return ("number", search(lambda s: (s - w) * mins / 60 * 1000 == metres, F(1, 10), 200))
        if rid in (1509, 1511):                        # h m (walk + ride), h m saved by riding both ways
            h1, m1, h2, m2 = v[:4]
            T1, g = 60 * h1 + m1, 60 * h2 + m2
            ride = search(lambda r: 2 * r == T1 - g, F(1, 2), 2000)
            both = 2 * (T1 - ride)
            hh, mm = divmod(int(both), 60)
            return ("pair", (F(hh), F(mm)))
        if rid == 1520:                                # A hours, B head start, B hours (fractions of the road)
            a, b, c = v[:3]
            f = lambda t: t / a + (t + b) / c - 1      # part of the road covered by both, minus the whole road (linear in t)
            return ("number", -f(F(0)) / (f(F(1)) - f(F(0))))
        if rid in (1521, 1523):                        # minutes, km/hr, new minutes
            m1, s1, m2 = v[:3]
            D = s1 * m1 / 60
            return ("number", search(lambda s: s * m2 / 60 == D, F(1, 10), 500))
        if rid in (1529, 1530, 1531):                  # D, T (hours or minutes), part done, time used
            D, T, p, qq = v[:4]
            Th = T / 60 if "minutes" in q else T
            return ("number", search(lambda s: s * Th * (1 - qq) == D * (1 - p), F(1, 10), 500))
        if rid in (1532, 1534):                        # ride x, back y, total T
            x, y, T = v[:3]
            return ("number", search(lambda d: d / x + d / y == T))
        if rid == 1537:                                # D, T, fraction of train time saved, hours early
            D, T, f, e = v[:4]
            tr = search(lambda t: f * t == e, F(1, 100), 100)
            va = D / (T - e)
            air = va * (T - tr)
            return ("ratio", air / (D - air))
        if rid in (1541, 1542, 1543):                  # hours early, slower by p, D km
            t, p, D = v[:3]
            return ("number", search(lambda s: s > p and D / (s - p) - D / s == t, F(1), 1000))
        raise KeyError(rid)
    except Exception:
        return ("unsolved", q[:40])
