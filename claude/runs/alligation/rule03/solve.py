"""Independent Rule 3 solver: reads water, mixture price and milk price from the text and finds the milk by
trying the value balance M*y = (M + l)*x as a linear equation in M (no rule formula)."""
import re
from fractions import Fraction as F


def solve(rid, q):
    l, x, y = [F(v) for v in re.findall(r"\d+(?:\.\d+)?", q)]
    # value(M) = (M + l)x - M y is linear in M: value(0) + slope*M = 0
    v0, v1 = l * x, (1 + l) * x - y
    slope = v1 - v0
    return ("number", -v0 / slope)
