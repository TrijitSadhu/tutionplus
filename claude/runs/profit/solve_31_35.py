"""Independent solver for Profit and Loss Rules 31-35. Reads the numbers in order and solves the story's own statement for the cost
price - the new selling price equals the new profit per cent of the new cost (31, 34, 35), or the cut price equals the second
per cent of the cost (32, 33) - as a linear equation from two trial costs; never through the rule formulas gen_31_35.py uses."""
import re
from fractions import Fraction as F


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def make(n):
    def solve(k, q):
        try:
            v = [F(t) for t in re.findall(r"\d+(?:\.\d+)?", q)]
            if n == 31:
                x, A, y = v[:3]
                cp = lin(lambda c: (c * (1 + x / 100) - A) - (c - A) * (1 + (x + y) / 100))
                return ("number", cp)
            if n in (32, 33):
                x, X, y = v[:3]
                after = (1 - y / 100) if n == 32 else (1 + y / 100)
                cp = lin(lambda c: c * (1 + x / 100) - X - c * after)
                sp = cp * (1 + x / 100)
                both = re.search(r"cost price and the first selling price", q)
                return ("pair", (cp, sp)) if both else ("number", sp)
            P, c_, s_, p = v[:4]
            if n == 34:
                cp = lin(lambda c: (c * (1 + P / 100) - s_) - (c - c_) * (1 + (P + p) / 100))
            else:
                cp = lin(lambda c: (c * (1 + P / 100) + s_) - (c + c_) * (1 + (P - p) / 100))
            return ("number", cp)
        except Exception:
            return ("unsolved", q[:40])
    return solve
