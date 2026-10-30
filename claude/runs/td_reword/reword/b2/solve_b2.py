"""Independent solver for Time & Distance rewording batch 2 (Rules 4-11), keyed by row id. Reads the numbers from the question
in order and finds the answer by searching for the distance (or time) that makes the story's own times agree, or by moving the
travellers hour by hour - never through the rule formulas gen_b2.py uses."""
from fractions import Fraction as F
from validate import numbers


def search(ok, step=F(1, 20), top=5000):
    """Smallest multiple of `step` that satisfies ok."""
    k = 1
    while k * step <= top:
        if ok(k * step):
            return k * step
        k += 1
    raise ValueError("no answer")


def solve(rid, q):
    try:
        v = numbers(q)
        if rid in (1443, 1444, 1445, 1446):            # x, late min, y, early min
            x, l, y, e = v[:4]
            return ("number", search(lambda D: D / x - D / y == (l + e) / 60))
        if rid in (1447, 1448, 1449):                  # x, late1, increase, late2
            x, l1, inc, l2 = v[:4]
            return ("number", search(lambda D: D / x - D / (x + inc) == (l1 - l2) / 60))
        if rid == 1450:                                # x, late1, y, late2
            x, l1, y, l2 = v[:4]
            return ("number", search(lambda D: D / x - D / y == (l1 - l2) / 60))
        if rid in (1451, 1453, 1454):                  # go x, back y, total T
            x, y, T = v[:3]
            return ("number", search(lambda D: D / x + D / y == T))
        if rid == 1452:                                # x, y, hours, minutes
            x, y, hh, mm = v[:4]
            return ("number", search(lambda D: D / x + D / y == hh + mm / 60))
        if rid in (1456, 1457, 1458, 1459):            # T, first-half speed, second-half speed
            T, a, b = v[:3]
            return ("number", search(lambda D: (D / 2) / a + (D / 2) / b == T))
        if rid == 1464:                                # D, x (from P), head start t, y (from Q): step time in tiny slices
            D, x, t, y = v[:4]
            meet = search(lambda s: x * s + y * (s + t) >= D, F(1, 1000), 100)
            return ("number", x * meet)
        if rid == 1468:                                # x, head start, y, t after the second starts
            x, hh, y, t = v[:4]
            return ("number", x * (hh + t) + y * t)
        if rid in (1473, 1475):                        # fraction a/b of speed, delay minutes
            p, d = v[:2]
            return ("number", search(lambda T: T / p - T == d))
        if rid == 1478:                                # D, x, start later (h), arrive earlier (h)
            D, x, late, early = v[:4]
            y = D / (D / x - late - early)
            s = search(lambda s: y * (s - late) >= x * s and s > late, F(1, 100), 100)
            return ("number", x * s)
        raise KeyError(rid)
    except Exception:
        return ("unsolved", q[:40])
