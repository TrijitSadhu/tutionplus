"""Independent solver for Profit and Loss Rule 40: reads the fraction, the two rates with their profit/loss words and the overall
result, and solves "gain on part 1 + gain on the rest = overall gain" with signed gains (linear, from two trial values) - not
through the rule formula."""
import re
from fractions import Fraction as F


def solve(k, q):
    try:
        x = F(*map(int, re.findall(r"\\frac\{(\d+)\}\{(\d+)\}", q)[0]))
        words = re.findall(r"\b(profit|loss)\b", q)
        rates = [F(t) for t in re.findall(r"(\d+(?:\.\d+)?)%", q)][:2]
        total = F(re.findall(r"Rs (\d+(?:\.\d+)?)", q)[0])
        sign = [1 if w == "profit" else -1 for w in words[:3]]
        f = lambda V: sign[0] * V * x * rates[0] / 100 + sign[1] * V * (1 - x) * rates[1] / 100 - sign[2] * total
        return ("number", -f(F(0)) / (f(F(1)) - f(F(0))))
    except Exception:
        return ("unsolved", q[:40])
