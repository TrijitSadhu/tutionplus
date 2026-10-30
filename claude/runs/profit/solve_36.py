"""Independent solver for Profit and Loss Rule 36. Reads x, y and the rupee gain, writes the two sales as two linear equations in
the two cost prices and solves them by elimination (Cramer) - not through the rule formula gen_36.py uses."""
import re
from fractions import Fraction as F


def solve(k, q):
    try:
        x, y, X = [F(t) for t in re.findall(r"\d+(?:\.\d+)?", q)][:3]
        # first sale:  (x/100) a - (y/100) b = X ;  second sale: -(y/100) a + (x/100) b = 0
        a11, a12, b1 = x / 100, -y / 100, X
        a21, a22, b2 = -y / 100, x / 100, F(0)
        det = a11 * a22 - a12 * a21
        a = (b1 * a22 - a12 * b2) / det
        b = (a11 * b2 - b1 * a21) / det
        return ("pair", (a, b))
    except Exception:
        return ("unsolved", q[:40])
