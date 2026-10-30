"""Independent solver for Profit and Loss Rule 38: reads x, A, B, y and solves "old price + B = (100 + y)% of (cost + A)" for the
cost (linear, from two trial costs) - not through the rule formula gen_38.py uses."""
import re
from fractions import Fraction as F


def solve(k, q):
    try:
        x, A, B, y = [F(t) for t in re.findall(r"\d+(?:\.\d+)?", q)][:4]
        f = lambda c: c * (1 + x / 100) + B - (c + A) * (1 + y / 100)
        return ("number", -f(F(0)) / (f(F(1)) - f(F(0))))
    except Exception:
        return ("unsolved", q[:40])
