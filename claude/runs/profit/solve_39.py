"""Independent solver for Profit and Loss Rule 39: reads the two fractions, the three rates and the total, and solves
"profit on part 1 + part 2 + the rest = total" for the value (linear, from two trial values) - not through the rule formula."""
import re
from fractions import Fraction as F


def solve(k, q):
    try:
        fr = [F(int(a), int(b)) for a, b in re.findall(r"\\frac\{(\d+)\}\{(\d+)\}", q)][:2]
        rates = [F(t) for t in re.findall(r"(\d+(?:\.\d+)?)%", q)][:3]
        total = F(re.findall(r"Rs (\d+(?:\.\d+)?)", q)[0])
        shares = fr + [1 - sum(fr)]
        f = lambda V: sum(V * s * r / 100 for s, r in zip(shares, rates)) - total
        return ("number", -f(F(0)) / (f(F(1)) - f(F(0))))
    except Exception:
        return ("unsolved", q[:40])
