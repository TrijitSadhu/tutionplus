"""Independent solver for Simple Interest Rules 7-13, keyed by row id / payload key; reads the numbers from the question in order.
Interest is added up month by month, never with PRT/100 or the rule formulas: Rule 7 follows each yearly payment to the due date,
Rule 8 steps through the months with the rate of each period, Rule 9 counts months on Rs 100, Rules 10/11 try times month by month
until one sum fits both amounts, Rule 12 compares two rates on a trial sum, Rule 13 tries rates in steps of 1/4 % until one sum fits
both amounts."""
import re
from fractions import Fraction as F

from solve_1_6 import interest, lin, months, vals


def rule_of(k):
    return {769: 7, 770: 8, 771: 9, 772: 10, 773: 11, 774: 12, 775: 13}.get(k) or int(re.match(r"r(\d+)_", k)[1])


def two_amounts(r1, A1, r2, A2, hi=12 * 60):
    """(months, sum) for which one sum amounts to A1 at r1% and to A2 at r2% in the same number of months."""
    g1 = g2 = F(0)                                  # interest on Re 1 so far at each rate
    for m in range(1, hi):
        g1 += r1 / 1200
        g2 += r2 / 1200
        P = A1 / (1 + g1)
        if P * (1 + g2) == A2:
            return m, P
    raise ValueError("no time")


def solve(k, q):
    try:
        v = vals(q)
        r = rule_of(k)
        if r == 7:                                      # debt A due in t years, r% - equal payments at the end of each year
            A, t, R = v[:3]
            n = int(t)
            assert n == t
            return ("number", lin(lambda x: sum(x + interest(x, R, 12 * (n - y)) for y in range(1, n + 1)) - A))
        if r == 8:                                      # r1 for t1, r2 for t2, r3 after t1 + t2; interest I in T years
            r1, t1, r2, t2, r3, t12, I, T = v[:8]
            assert t12 == t1 + t2

            def total(P):
                s = F(0)
                for mth in range(months(T)):
                    yr = F(mth, 12)
                    s += P * (r1 if yr < t1 else r2 if yr < t1 + t2 else r3) / 1200
                return s
            return ("number", lin(lambda P: total(P) - I))
        if r == 9:
            if re.search(r"doubl", q):
                x, rest = F(2), v
            elif re.search(r"trebl|three times|thrice", q):
                x, rest = F(3), v
            else:
                x, rest = v[0], v[1:]
            need = 100 * (x - 1)                        # interest on Rs 100
            if re.search(r"how many years|how long|in what time", q, re.I):
                R = rest[0]
                got = F(0)
                for mth in range(1, 12 * 200):
                    got += 100 * R / 1200
                    if got == need:
                        return ("number", F(mth, 12))
                return ("unsolved", "no time")
            t = rest[0]
            return ("number", lin(lambda R: interest(F(100), R, months(t)) - need))
        if r in (10, 11):                               # r1, A1, r2, A2
            r1, A1, r2, A2 = v[:4]
            m, P = two_amounts(r1, A1, r2, A2)
            return ("number", F(m, 12) if r == 10 else P)
        if r == 12:                                     # t years, x% higher, Rs A more
            t, x, A = v[:3]
            base = F(5)
            return ("number", lin(lambda P: interest(P, base + x, months(t)) - interest(P, base, months(t)) - A))
        if r == 13:                                     # A1 after t1 years, A2 after t2 years
            A1, t1, A2, t2 = v[:4]
            for i in range(1, 161):
                R = F(i, 4)
                P = lin(lambda p: p + interest(p, R, months(t1)) - A1)
                if P + interest(P, R, months(t2)) == A2:
                    return ("pair", (P, R)) if (k == 775 or k in ("r13_e5", "r13_e6", "r13_e7")) else ("number", P)
            return ("unsolved", "no rate")
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
