"""Independent solver for the Simple Interest Miscellaneous questions, keyed m01-m05; reads the numbers from the question in order.
Interest is added up month by month (solve_1_6.interest): M1 solves the two years' interests for the sum, M2 finds the rate from the
first sum and runs the second one, M3 solves the two loans for the lower rate, M4 runs a trial principal at the rate the interest
needs and multiplies it after half the time, M5 tries every whole number for the first interest and runs it at the same rate and time."""
import os, sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solve_1_6 import interest, lin, months, vals  # noqa: E402


def solve(k, q):
    try:
        v = vals(q)
        if k == "m01":                                  # r1, r2, extra yearly interest
            r1, r2, d = v[:3]
            return ("number", lin(lambda P: interest(P, r2, 12) - interest(P, r1, 12) - d))
        if k == "m02":                                  # P1, A1, t1, P2, t2
            P1, A1, t1, P2, t2 = v[:5]
            R = lin(lambda R: interest(P1, R, months(t1)) - (A1 - P1))
            return ("number", P2 + interest(P2, R, months(t2)))
        if k == "m03":                                  # X1, X2, the "1%" of 'a rate 1% higher', t, I
            X1, X2, one, t, I = v[:5]
            assert one == 1
            r = lin(lambda r: interest(X1, r, months(t)) + interest(X2, r + 1, months(t)) - I)
            return ("pair", (r, r + 1))
        if k == "m04":                                  # I, T, n, t
            I, T, n, t = v[:4]
            P = F(1000)
            R = lin(lambda R: interest(P, R, months(T)) - I)
            return ("number", interest(P, R, months(t)) + interest(n * P, R, months(T - t)))
        if k == "m05":                                  # P, z
            P, z = v[:2]
            for y in range(1, int(P)):                  # y is the interest on P; at the same rate and time y earns z
                R = lin(lambda R: interest(P, R, 12) - y)   # take the time as one year: R is the per cent the pair needs
                if interest(F(y), R, 12) == z:
                    return ("number", F(y))
            return ("unsolved", "no y")
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
