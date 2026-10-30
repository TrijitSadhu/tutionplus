"""Independent solver for Profit and Loss Rule 41: reads the total cost and the loss / gain rates and solves "price of the loss item
= price of the gain item" for the loss item's cost (linear, from two trial costs) - not through the rule formula."""
import re
from fractions import Fraction as F


def solve(k, q):
    try:
        P = F(re.findall(r"Rs (\d+)", q)[0])
        x = F(re.search(r"loss of (\d+(?:\.\d+)?)%", q).group(1))
        y = F(re.search(r"gain of (\d+(?:\.\d+)?)%", q).group(1))
        f = lambda c: c * (100 - x) - (P - c) * (100 + y)
        c = -f(F(0)) / (f(F(1)) - f(F(0)))
        return ("pair", (c, P - c))
    except Exception:
        return ("unsolved", q[:40])
