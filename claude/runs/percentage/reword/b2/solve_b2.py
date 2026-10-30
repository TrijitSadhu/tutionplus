"""Independent solver for Percentage rewording batch 2 (Rules 12-16). Reads the two per cents in order, builds the actual
first and second values from a third value of 7 (x% more / less than it, or x% of it - the rule folder says which), and
compares them as the question asks - never through the rule formulas gen_9_16.py uses."""
import re
from fractions import Fraction as F
from solve_1_8 import pcts

KIND = {12: "more", 13: "more", 14: "less", 15: "less", 16: "of"}


def make(n):
    def solve(k, q):
        try:
            return _solve(k, q)
        except Exception:
            return ("unsolved", q[:40])

    def _solve(k, q):
        x, y = pcts(q)[:2]
        third = F(7)
        kind = KIND[n]
        if kind == "more":
            val = {"first": third + third * x / 100, "second": third + third * y / 100}
        elif kind == "less":
            val = {"first": third - third * x / 100, "second": third - third * y / 100}
        else:
            val = {"first": third * x / 100, "second": third * y / 100}
        m = re.search(r"By what per cent is the (first|second) .*? less than the (first|second)", q)
        if m:
            a, b = val[m[1]], val[m[2]]
            return ("number", (b - a) / b * 100)
        m = re.search(r"What per cent of the (first|second) .*? is the (first|second)", q)
        return ("number", val[m[2]] / val[m[1]] * 100)
    return solve
