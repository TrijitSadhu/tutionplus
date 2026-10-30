"""Independent solvers for Profit and Loss Rules 18-21. Rules 18 and 21 push Rs 100 through the two sales with the direction word
of each per cent; Rules 19 and 20 solve "actual sale + Rs X = wished sale" for the cost (linear in the cost, solved from two trial
costs) - never through the rule formulas gen_18_21.py uses."""
import re
from fractions import Fraction as F
from solve_13_17 import changes, push


def nums(q):
    return [F(x) for x in re.findall(r"\d+(?:\.\d+)?", q)]


def make(n):
    def solve(k, q):
        try:
            if n in (18, 21):
                v = push(F(100), changes(q)) - 100
                return ("signed", v) if n == 18 else ("number", -v)
            x, X, y = nums(q)[:3]
            if "value of" in q or "value." in q:             # offered x% below the value; Rs X more is y% above it
                first = 1 - x / 100
            else:
                first = 1 + x / 100 if n == 19 else 1 - x / 100
            f = lambda c: c * first + X - c * (1 + y / 100)
            cp = -f(F(0)) / (f(F(1)) - f(F(0)))
            return ("number", cp * first if "For how much was" in q else cp)
        except Exception:
            return ("unsolved", q[:40])
    return solve
