"""Independent solvers for Profit and Loss Rules 8-12 (the dishonest dealer). Each reads the numbers from the question and prices
the deal in money: what the buyer pays for the stated measure against what the goods really handed over cost the dealer - never
through the rule formulas gen_8_12.py use."""
import re
from fractions import Fraction as F


def nums(q):
    return [F(x) for x in re.findall(r"\d+(?:\.\d+)?", q)]


def deal(paid, real_cost):
    return (paid - real_cost) * 100 / real_cost


def make(n):
    def solve(k, q):
        try:
            v = nums(q)
            if n == 8:                                       # false measure (g for 1 kg, or cm for a metre), sold at cost
                false = v[-1] if "cm" not in q else v[0]
                false = [x for x in v if x not in (1,)][0]
                true = F(100) if ("cm" in q or "metre" in q) else F(1000)
                return ("number", deal(true, false))         # Re 1 per small unit: paid for `true`, gives `false`
            if n == 9:                                       # profit p, weight w% less: price 100 units at Re 1
                p, w = v[:2]
                return ("number", deal(100 + p, 100 - w))
            if n == 10:                                      # loss x, gives y in place of z
                x, y = v[:2]
                z = v[2] if len(v) > 2 and v[2] != 1 else (F(100) if "cm" in q else F(1000))
                paid = z * (100 - x) / 100                   # Re 1 per unit of the true measure, less the stated loss
                return ("signed", deal(paid, y))
            if n == 11:                                      # loss x, weight y% less
                x, y = v[:2]
                return ("signed", deal(100 - x, 100 - y))
            X = [x for x in v if x > 100][0]                 # Rule 12: X g for 1 kg, gain x%
            x = [x for x in v if x != X and x != 1][0]
            return ("signed", deal(1000 * (100 + x) / 100, X))
        except Exception:
            return ("unsolved", q[:40])
    return solve
