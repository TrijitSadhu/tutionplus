"""Independent solver for Simple Interest Rules 34-39, keyed by row id / payload key; reads the numbers from the question in order.
Interest is added up month by month (solve_1_6.interest), never with the rule formulas: Rule 34 lends the three parts of a trial
capital, Rule 35 tries rates in steps of a twelfth (the years run as that many months), Rule 36 finds the sum from the interest and adds it
back, Rule 37 solves the two loans' interest for the rate, Rule 38 counts the months the first deposit needs and runs the second one
over them, Rule 39 counts months on Rs 100 (or solves for the rate)."""
import re
from fractions import Fraction as F

from solve_1_6 import interest, lin, months, vals


def rule_of(k):
    return {796: 34, 797: 35, 798: 37, 799: 38, 800: 39}.get(k) or int(re.match(r"r(\d+)_", k)[1])


def solve(k, q):
    try:
        v = vals(q)
        r = rule_of(k)
        if r == 34:                                     # f1, r1, f2, r2, r3, [t], A
            f1, r1, f2, r2, r3 = v[:5]
            t, A = (v[5], v[6]) if len(v) >= 7 else (F(1), v[5])

            def got(C):
                return interest(f1 * C, r1, months(t)) + interest(f2 * C, r2, months(t)) + interest((1 - f1 - f2) * C, r3, months(t))
            return ("number", lin(lambda C: got(C) - A))
        if r == 35:                                     # P, I; years = rate
            P, I = v[:2]
            for k12 in range(1, 12 * 40):
                R = F(k12, 12)
                if interest(P, R, k12) == I:           # R per cent for R years = 12R months
                    return ("number", R)
            return ("unsolved", "no rate")
        if r == 36:                                     # r, t, I -> amount
            R, t, I = v[:3]
            P = lin(lambda P: interest(P, R, months(t)) - I)
            return ("number", P + I)
        if r == 37:                                     # P1, t1, P2, t2, I
            P1, t1, P2, t2, I = v[:5]
            return ("number", lin(lambda R: interest(P1, R, months(t1)) + interest(P2, R, months(t2)) - I))
        if r == 38:                                     # P1, r1, I1, I2, P2
            P1, r1, I1, I2, P2 = v[:5]
            got = F(0)
            for mth in range(1, 12 * 100):
                got += P1 * r1 / 1200
                if got == I1:
                    return ("number", lin(lambda R: interest(P2, R, mth) - I2))
            return ("unsolved", "no time")
        if r == 39:
            n = F(2) if re.search(r"double", q) else F(3) if re.search(r"treble", q) else None
            x = v[0]
            need = 100 * (n - 1)
            if re.search(r"how many years|in what time|how long", q, re.I):
                got = F(0)
                for mth in range(1, 12 * 200):
                    got += 100 * x / 1200
                    if got == need:
                        return ("number", F(mth, 12))
                return ("unsolved", "no time")
            return ("number", lin(lambda R: interest(F(100), R, months(x)) - need))
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
