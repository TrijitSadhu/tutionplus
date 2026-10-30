"""Independent solver for Profit and Loss Rules 22-24. Reads x, y, X, z from the question in that order and solves
"real sale +/- Rs X = (cheaper cost) x (1 + z%)" for the cost price (linear in the cost, solved from two trial costs) - never
through the rule formulas gen_22_24.py uses."""
import re
from fractions import Fraction as F


def make(n):
    def solve(k, q):
        try:
            x, y, X, z = [F(v) for v in re.findall(r"\d+(?:\.\d+)?", q)][:4]
            first = 1 - x / 100 if n == 23 else 1 + x / 100
            sign = -1 if n == 24 else 1                      # Rs X less (24) or more (22, 23)
            f = lambda c: c * first + sign * X - c * (1 - y / 100) * (1 + z / 100)
            return ("number", -f(F(0)) / (f(F(1)) - f(F(0))))
        except Exception:
            return ("unsolved", q[:40])
    return solve
