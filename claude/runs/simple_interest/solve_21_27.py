"""Independent solver for Simple Interest Rules 21-27, keyed by row id / payload key; reads the numbers from the question in order.
Interest is added up month by month (solve_1_6.interest), never with the rule formulas: Rules 21 and 27 count months on Rs 100 and
find the rate / time from them, Rule 22 counts months for the second sum and grows the first over the same months, Rule 23 finds the
sum and counts months to the new amount, Rule 24 finds the common amount that makes the parts add up, Rules 25 / 26 solve the
month-by-month amount (or sum minus interest) for the sum."""
import re
from fractions import Fraction as F
from math import gcd

from solve_1_6 import interest, lin, months, vals


def rule_of(k):
    return {783: 21, 784: 22, 785: 23, 786: 24, 787: 25, 788: 26, 789: 27}.get(k) or int(re.match(r"r(\d+)_", k)[1])


def months_until(step, need, hi=12 * 600):
    """months of a steady monthly interest 'step' until 'need' is reached exactly."""
    got = F(0)
    for mth in range(1, hi):
        got += step
        if got == need:
            return mth
    raise ValueError("never reached")


def part_for(r, t, A):
    return lin(lambda P: P + interest(P, r, months(t)) - A)


def solve(k, q):
    try:
        v = vals(q)
        r = rule_of(k)
        if r == 21:                                     # n times at r% -> rate for m times in the same time
            n, R, m = v[:3]
            mth = months_until(100 * R / 1200, 100 * (n - 1))
            return ("number", lin(lambda x: interest(F(100), x, mth) - 100 * (m - 1)))
        if r == 22:                                     # A1 at r1, in the time P -> A2 at r2
            A1, r1, P, A2, r2 = v[:5]
            mth = months_until(P * r2 / 1200, A2 - P)
            return ("number", lin(lambda S: S + interest(S, r1, mth) - A1))
        if r == 23:                                     # A1 in t years at r% -> years to A2
            A1, t, R, A2 = v[:4]
            P = lin(lambda p: p + interest(p, R, months(t)) - A1)
            return ("number", F(months_until(P * R / 1200, A2 - P), 12))
        if r == 24:
            X = v[0]
            if "sons" in q:                             # X, ages a1, a2, turns M, r%
                a1, a2, Mt, R = v[1:5]
                rts = [(R, Mt - a1), (R, Mt - a2)]
            elif "first is lent" in q:                  # X, r1, t1, r2, t2, r3, t3
                rts = [(v[1], v[2]), (v[3], v[4]), (v[5], v[6])]
            else:                                       # X, t1, t2, t3, r%
                rts = [(v[4], v[1]), (v[4], v[2]), (v[4], v[3])]
            A = lin(lambda A: sum(part_for(rr, tt, A) for rr, tt in rts) - X)
            parts = [part_for(rr, tt, A) for rr, tt in rts]
            if "ratio" in q:
                d = 1
                for p in parts:
                    d = d * p.denominator // gcd(d, p.denominator)
                ints = [int(p * d) for p in parts]
                g = 0
                for x in ints:
                    g = gcd(g, x)
                return ("terms", tuple(F(x // g) for x in ints))
            if "difference" in q:
                return ("number", max(parts) - min(parts))
            return ("pair" if len(parts) == 2 else "triple", tuple(parts))
        if r == 25:                                     # amount A in t years at r%
            A, t, R = v[:3]
            return ("number", lin(lambda P: P + interest(P, R, months(t)) - A))
        if r == 26:                                     # r%, t years, interest Rs A short of the sum
            R, t, A = v[:3]
            return ("number", lin(lambda P: P - interest(P, R, months(t)) - A))
        if r == 27:                                     # n times in t years -> years for m times
            if re.search(r"doubles", q):
                n, (t, m) = F(2), v[:2]
            else:
                n, t, m = v[:3]
            R = lin(lambda x: interest(F(100), x, months(t)) - 100 * (n - 1))
            return ("number", F(months_until(100 * R / 1200, 100 * (m - 1)), 12))
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
