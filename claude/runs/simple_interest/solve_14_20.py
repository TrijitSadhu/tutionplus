"""Independent solver for Simple Interest Rules 14-20, keyed by row id / payload key; reads the numbers from the question in order.
Interest is added up month by month (solve_1_6.interest), never with the rule formulas: Rule 14 compares two rates on a trial sum,
Rule 15 finds the part by a linear solve of the two parts' interest, Rules 16/17 find the old rate from the first amount and run the
new rate, Rules 18/19 put a trial principal at the rate the first interest needs and run the bigger principal, Rule 20 finds the common
interest that makes the parts add up to the sum."""
import re
from fractions import Fraction as F

from solve_1_6 import interest, lin, months, vals

PAIR = {777, "r15_e6", 782, "r20_e2", "r20_e3", "r20_e4"}


def rule_of(k):
    return {776: 14, 777: 15, 778: 16, 779: 17, 780: 18, 781: 19, 782: 20}.get(k) or int(re.match(r"r(\d+)_", k)[1])


def part_for(r, t, I):
    """the principal that earns I at r% in t years."""
    return lin(lambda P: interest(P, r, months(t)) - I)


def solve(k, q):
    try:
        v = vals(q)
        r = rule_of(k)
        if r == 14:                                     # t years, x% lower, Rs A less
            t, x, A = v[:3]
            base = F(12)
            return ("number", lin(lambda P: interest(P, base, months(t)) - interest(P, base - x, months(t)) - A))
        if r == 15:
            if re.search(r"some more money", q):        # X1 at r1, more at r2, t years, interest I -> total
                X1, r1, r2, t, I = v[:5]
                X2 = lin(lambda y: interest(X1, r1, months(t)) + interest(y, r2, months(t)) - I)
                return ("number", X1 + X2)
            if re.search(r"for (\d+) years", q):        # X, r1, r2, t years, I -> both parts
                X, r1, r2, t, I = v[:5]
            else:                                       # X, r1, r2, I in one year
                X, r1, r2, I = v[:4]
                t = F(1)
            p1 = lin(lambda y: interest(y, r1, months(t)) + interest(X - y, r2, months(t)) - I)
            if k in PAIR:
                return ("pair", (p1, X - p1))
            ask = v[-1]                                 # "How much ... at <rate>%?"
            return ("number", p1 if ask == r1 else X - p1 if ask == r2 else None)
        if r in (16, 17):                               # X becomes A in t1 years; rate -/+ r; amount after t2 years
            X, A, t1, d, t2 = v[:5]
            R0 = lin(lambda R: interest(X, R, months(t1)) - (A - X))
            down = re.search(r"lowers|lower", q)
            up = re.search(r"raises|higher", q)
            assert bool(down) != bool(up)
            Rn = R0 - d if down else R0 + d
            return ("number", X + interest(X, Rn, months(t2)))
        if r in (18, 19):
            if r == 18:                                 # x, t, t, n, 2t
                x, t1, t2, n = v[0], v[1], v[2], v[3]
            else:                                       # x, t1, t2, n, t1 + t2
                x, t1, t2, n = v[:4]
            P = F(1000)
            R = lin(lambda R: interest(P, R, months(t1)) - x)
            return ("number", x + interest(n * P, R, months(t2)))
        if r == 20:
            X = v[0]
            rts = []
            rest = v[1:]
            while len(rest) >= 2 and len(rts) < 3:
                rts.append((rest[0], rest[1]))
                rest = rest[2:]
            if "three loans" not in q:
                rts = rts[:2]
            I = lin(lambda I: sum(part_for(rr, tt, I) for rr, tt in rts) - X)
            parts = [part_for(rr, tt, I) for rr, tt in rts]
            if k in PAIR:
                return ("pair", tuple(parts))
            return ("number", max(parts) - min(parts))
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
