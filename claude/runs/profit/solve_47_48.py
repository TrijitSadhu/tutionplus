"""Independent solver for Profit and Loss Rules 47 and 48: reads the cost, the fraction sold first and its loss / profit, and works
with the real money - the first part's takings, what the rest must bring in so takings equal cost - then reports the size of the
profit (Rule 47) or loss (Rule 48) per cent on the rest; not the rule formula."""
import re
from fractions import Fraction as F


def solve(k, q):
    try:
        A = F(re.search(r"Rs (\d+)", q).group(1))
        n = F(*map(int, re.search(r"\\frac\{(\d+)\}\{(\d+)\}", q).groups()))
        word, x = re.search(r"\b(loss|profit) of (\d+(?:\.\d+)?)%", q).groups()
        x = F(x) * (-1 if word == "loss" else 1)
        first_takings = A * n * (1 + x / 100)
        rest_cost = A * (1 - n)
        rest_takings = A - first_takings
        return ("number", abs(rest_takings - rest_cost) / rest_cost * 100)
    except Exception:
        return ("unsolved", q[:40])
