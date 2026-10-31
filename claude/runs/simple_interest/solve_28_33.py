"""Independent solver for Simple Interest Rules 28-33, keyed by row id / payload key; reads the numbers from the question in order.
Interest is added up month by month (solve_1_6.interest), never with the rule formulas: Rule 28 counts months until the two loans'
interests differ by A, Rules 29 / 30 / 33 solve the month-by-month interests linearly for the unknown, Rule 31 tries rates in 1/4 %
steps until one sum fits both amounts, Rule 32 runs the loan month by month with the part payment taken off the principal."""
import re
from fractions import Fraction as F

from solve_1_6 import interest, lin, months, vals


def rule_of(k):
    return {790: 28, 791: 29, 792: 30, 793: 31, 794: 32, 795: 33}.get(k) or int(re.match(r"r(\d+)_", k)[1])


def solve(k, q):
    try:
        v = vals(q)
        r = rule_of(k)
        if r == 28:                                     # P1, P2, r, A
            P1, P2, R, A = v[:4]
            for mth in range(1, 12 * 100):
                if interest(P2, R, mth) - interest(P1, R, mth) == A:
                    return ("number", F(mth, 12))
            return ("unsolved", "no time")
        if r == 29:
            if "months" in q:                           # m1, r1, D, m2, r2 (sentence order)
                m1, r1, D, m2, r2 = v[:5]
                return ("number", lin(lambda P: interest(P, r1, int(m1)) - interest(P, r2, int(m2)) - D))
            if "differ by" in q:                        # t1, t2, r, D
                t1, t2, R, D = v[:4]
                return ("number", lin(lambda P: interest(P, R, months(t2)) - interest(P, R, months(t1)) - D))
            r1, t1, r2, t2, D = v[:5]
            return ("number", lin(lambda P: interest(P, r1, months(t1)) - interest(P, r2, months(t2)) - D))
        if r == 30:                                     # X, t, D -> rate gap
            X, t, D = v[:3]
            base = F(9)
            return ("number", lin(lambda d: interest(X, base + d, months(t)) - interest(X, base, months(t)) - D))
        if r == 31:                                     # A1, t1, A2, t2 (or "after dt more years")
            A1, t1, A2, t2 = v[:4]
            if "more years" in q:
                t2 = t1 + t2
            for i in range(1, 161):
                R = F(i, 4)
                P = lin(lambda p: p + interest(p, R, months(t1)) - A1)
                if P + interest(P, R, months(t2)) == A2:
                    return ("number", R)
            return ("unsolved", "no rate")
        if r == 32:                                     # X, t1, x1, t2, x2
            X, t1, x1, t2, x2 = v[:5]

            def owed(R):
                bal, acc = X, F(0)
                for mth in range(1, months(t2) + 1):
                    acc += bal * R / 1200
                    if mth == months(t1):
                        bal -= x1
                return bal + acc
            return ("number", lin(lambda R: owed(R) - x2))
        if r == 33:                                     # P, r1, r2, t, A
            P, r1, r2, t, A = v[:5]
            return ("number", lin(lambda y: interest(y, r1, months(t)) + interest(P - y, r2, months(t)) - A))
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
