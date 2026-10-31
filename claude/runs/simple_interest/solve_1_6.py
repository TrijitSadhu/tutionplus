"""Independent solver for Simple Interest Rules 1-6, keyed by row id / payload key; reads the numbers from the question in order.
Interest is added up month by month (or day by day), never with PRT/100 in one go; an unknown principal or rate is found by a
linear solve of that running total, an unknown time by counting months until the interest (or amount) is reached."""
import re
from fractions import Fraction as F


def vals(q):
    """numbers in order: 2\\frac{2}{3} and \\frac{9}{25} as one number each, 937.50 as a decimal."""
    out = []
    for whole, a, b, n in re.findall(r"(\d+)?\\frac\{(\d+)\}\{(\d+)\}|(\d+(?:\.\d+)?)", q):
        out.append(F(int(whole or 0)) + F(int(a), int(b)) if a else F(n))
    return out


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def interest(P, R, months=None, days=None):
    """simple interest added month by month (or day by day for days)."""
    total = F(0)
    if days is not None:
        for _ in range(int(days)):
            total += P * R / 100 / 365
        return total
    for _ in range(int(months)):
        total += P * R / 100 / 12
    return total


def months(years):
    m = F(years) * 12
    assert m.denominator == 1
    return int(m)


def count_months(ok, hi=1200):
    for m in range(1, hi):
        if ok(m):
            return F(m, 12)
    raise ValueError("no time")


def solve(k, q):
    try:
        v = vals(q)
        r = {759: 1, 760: 1, 761: 1, 762: 1, 763: 1, 764: 2, 765: 3, 766: 4, 767: 5, 768: 6}.get(k) or int(re.match(r"r(\d+)_", k)[1])
        if r == 1:
            if k == 759 or k in ("r1_e2", "r1_e11"):              # P, R, T -> interest
                P, R, T = v[:3]
                return ("number", interest(P, R, months(T)))
            if k == "r1_e1":
                P, R = v[:2]
                return ("number", interest(P, R, 12))
            if k == "r1_e3":                                     # P, R, T -> interest and amount
                P, R, T = v[:3]
                I = interest(P, R, months(T))
                return ("pair", (I, P + I))
            if k == "r1_e4":                                     # P, R, T, cash -> the goat
                P, R, T, cash = v[:4]
                return ("number", P + interest(P, R, months(T)) - cash)
            if k == "r1_e5":                                     # P, days, R
                P, d, R = v[:3]
                return ("number", interest(P, R, days=d))
            if k == 760:                                         # R, I, T -> P
                R, I, T = v[:3]
                return ("number", lin(lambda P: interest(P, R, months(T)) - I))
            if k == "r1_e6":                                     # I, T, R -> P
                I, T, R = v[:3]
                return ("number", lin(lambda P: interest(P, R, months(T)) - I))
            if k == "r1_e13":                                    # T, R, I -> P
                T, R, I = v[:3]
                return ("number", lin(lambda P: interest(P, R, months(T)) - I))
            if k == 761:                                         # P, A, years, months -> R
                P, A, y, mo = v[:4]
                return ("number", lin(lambda R: interest(P, R, int(y * 12 + mo)) - (A - P)))
            if k in ("r1_e7", "r1_e9"):                          # P, A, T -> R
                P, A, T = v[:3]
                return ("number", lin(lambda R: interest(P, R, months(T)) - (A - P)))
            if k == "r1_e14":                                    # P, T, I -> R
                P, T, I = v[:3]
                return ("number", lin(lambda R: interest(P, R, months(T)) - I))
            if k == "r1_e15":                                    # P = 1, I, T -> R
                P, I, T = v[:3]
                return ("number", lin(lambda R: interest(P, R, months(T)) - I))
            if k in (762, "r1_e8"):                              # P, A, R -> T
                P, A, R = v[:3]
                return ("number", count_months(lambda m: P + interest(P, R, m) == A))
            if k == "r1_e10":                                    # P, R, A -> T
                P, R, A = v[:3]
                return ("number", count_months(lambda m: P + interest(P, R, m) == A))
            if k == "r1_e12":                                    # P, R, I -> T
                P, R, I = v[:3]
                return ("number", count_months(lambda m: interest(P, R, m) == I))
            if k == 763:                                         # x% for x years earns x, at x = 7
                x = F(7)
                return ("expr", lin(lambda P: interest(P, x, months(x)) - x))
            if k == "r1_e16":                                    # Rs a a day at R%
                per, R = v[:2]
                return ("number", lin(lambda P: interest(P, R, days=365) - 365 * per))
        if r == 2:
            P, dI, dT = v[:3]
            return ("number", lin(lambda R: interest(P, R, months(dT)) - dI))
        if r == 3:
            if "total" in q or "in all" in q:                    # x1, r1, r2, whole rate -> total
                x1, r1, r2, avg = v[:4]
                x2 = lin(lambda y: interest(x1, r1, 12) + interest(y, r2, 12) - interest(x1 + y, avg, 12))
                return ("number", x1 + x2)
            x1, r1, x2, r2 = v[:4]
            return ("number", (interest(x1, r1, 12) + interest(x2, r2, 12)) / (x1 + x2) * 100)
        if r == 4:                                               # interest = f of the sum, years = rate
            f = v[0]
            P = F(100)
            for i in range(1, 1200):
                rr = F(i, 12)
                if interest(P, rr, i) == f * P:
                    return ("number", rr)
            return ("unsolved", "no rate")
        if r == 5:
            if k == "r5_e3":                                     # t, P1, dI, P2
                t, P1, dI, P2 = v[:4]
            else:                                                # P1, P2, t, dI
                P1, P2, t, dI = v[:4]
            return ("number", lin(lambda R: interest(P1, R, months(t)) - interest(P2, R, months(t)) - dI))
        if r == 6:
            if k == "r6_e4":                                     # P, t, dI -> difference of rates
                P, t, dI = v[:3]
                return ("number", lin(lambda d: interest(P, 10 + d, months(t)) - interest(P, F(10), months(t)) - dI))
            P, dI, dR = v[:3]
            return ("number", count_months(lambda m: interest(P, 10 + dR, m) - interest(P, F(10), m) == dI))
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
