"""Independent solver for Profit and Loss Rule 45: reads the cost, the fraction sold first, its loss and the overall profit, and works
with the real money - what the first part brings in, what the whole must bring in, what the rest costs - not the rule formula."""
import re
from fractions import Fraction as F


def solve(k, q):
    try:
        A = F(re.search(r"Rs (\d+)", q).group(1))
        n = F(*map(int, re.search(r"\\frac\{(\d+)\}\{(\d+)\}", q).groups()))
        x = F(re.search(r"loss of (\d+(?:\.\d+)?)%", q).group(1))
        y = F(re.findall(r"profit of (\d+(?:\.\d+)?)%", q)[-1])
        first_takings = A * n * (1 - x / 100)
        rest_cost = A * (1 - n)
        rest_takings = A * (1 + y / 100) - first_takings
        return ("number", (rest_takings - rest_cost) / rest_cost * 100)
    except Exception:
        return ("unsolved", q[:40])
