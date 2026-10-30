"""Independent solvers for Profit and Loss Rules 1-3, keyed by row id or payload key. Each reads the numbers from the question
text and works the deal through article by article, or searches for the cost price that makes the story's own statements
true - never through the rule formulas gen_1_3.py uses."""
import re
from fractions import Fraction as F


def nums(q):
    return [F(x) for x in re.findall(r"\d+(?:\.\d+)?", q.replace(",", ""))]


def search(ok, step=F(1, 100), top=100000):
    k = 1
    while k * step <= top:
        if ok(k * step):
            return k * step
        k += 1
    raise ValueError("no answer")


def signed_pct(cost, got):
    return (got - cost) * 100 / cost


def solve(k, q):
    try:
        v = nums(q)
        if k in (278, 279):                                      # buys for a, sells for b: amount of profit / loss
            a, b = v[:2]
            return ("number", abs(b - a))
        if k in ("r1_e1", "r1_e2"):
            a, b = v[:2]
            return ("signed", b - a)
        if k == "r1_e3":                                         # sold for hi: profit twice the profit at lo
            hi, lo = v[:2]
            return ("number", search(lambda c: hi - c == 2 * (lo - c), F(1), hi))
        if k in (280, 281, 916, "r2_e1"):                        # paid a, got b
            a, b = v[:2]
            p = signed_pct(a, b)
            return ("signed", p) if k == "r2_e1" else ("number", abs(p))
        if k == "r2_e2":                                         # profit Rs a on cost Rs b
            gain, cost = v[:2]
            return ("number", gain * 100 / cost)
        if k in (282, 917):                                      # price, repairs, sale
            a, extra, sp = v[:3]
            return ("signed", signed_pct(a + extra, sp))
        if k in (283, 918, 284, 919):                            # dozens, rate per dozen, [carriage], price each
            doz, rate = v[:2]
            extra = v[2] if k in (283, 918) else F(0)
            each = v[-1]
            pieces = [each] * int(doz * 12)                      # sell them one by one
            p = signed_pct(doz * rate + extra, sum(pieces))
            return ("signed", p) if k in (283, 918) else ("number", p)
        if k in (285, 920):                                      # sells N, gain = SP of k: try a selling price of Rs 1 each
            N, kk = v[:2]
            sp = N * 1
            return ("number", signed_pct(sp - kk, sp))
        if k in (921, 922):                                      # sold for sp at a loss of l%
            sp, l = v[:2]
            return ("number", search(lambda c: c - c * l / 100 == sp, F(1, 10), 100000))
        if k in (287, 923):                                      # n articles for Rs total, sold Rs each
            n, total, each = v[:3]
            return ("number", signed_pct(total, n * each))
        if k in (286, 924):                                      # n units at rate, two extra costs, gain g%: SP of one unit
            n, rate, e1, e2, g = v[:5]
            cost_one = (n * rate + e1 + e2) / n
            return ("number", search(lambda s: (s - cost_one) * 100 == g * cost_one, F(1, 100), 100000))
        if k in (288, 925):                                      # buys a for Rs b, sells c for Rs d: one article each way
            a, b, c, d = v[:4]
            return ("number", signed_pct(b / a, d / c))
        if k == 926:                                             # marked, sold
            mp, sp = v[:2]
            return ("number", (mp - sp) * 100 / mp)
        if k in (289, 927, 928, 929, 930, 931):                  # profit at x = loss at y, then z%
            x, y, z = v[:3]
            c = search(lambda c: x - c == c - y, F(1), x)
            return ("number", c + c * z / 100)
        raise KeyError(k)
    except Exception:
        return ("unsolved", q[:40])
