"""Independent solvers for Profit and Loss Rules 4-7, keyed by row id. Rules 4-5 search for the old price that makes the
quantities bought before and after the change differ by the stated amount; Rules 6-7 price one article each way - never through
the rule formulas gen_4_7.py uses."""
import re
from fractions import Fraction as F

RED = {290, 932, 933, 934, 935, 936, 937, 938, 941, 942, 943}
RISE = {291, 939, 940, 944, 945}
ASK = {932: "orig", 933: "orig", 943: "red", 939: "orig", 940: "orig", 944: "orig", 945: "orig"}


def nums(q):
    return [F(x) for x in re.findall(r"\d+(?:\.\d+)?", q)]


def search(ok, step=F(1, 200), top=1000):
    k = 1
    while k * step <= top:
        if ok(k * step):
            return k * step
        k += 1
    raise ValueError("no answer")


def solve(k, q):
    try:
        v = nums(q)
        if k in RED or k in RISE:
            x, n, A = v[:3]
            f = (100 - x) / 100 if k in RED else (100 + x) / 100
            # quantity bought for Rs A is A/price; the two quantities differ by n - linear in 1/o, solved from two trial values
            gap = (lambda u: A * u / f - A * u - n) if k in RED else (lambda u: A * u - A * u / f - n)
            u = -gap(F(0)) / (gap(F(1)) - gap(F(0)))
            o = 1 / u
            new = o * f
            a = ASK.get(k, "both")
            if a == "orig":
                return ("number", o)
            if a == "red":
                return ("number", new)
            return ("pair", (new, o))
        a, b, c, d = v[:4]                                     # buys a for Rs b, sells c for Rs d
        one_cost, one_sale = b / a, d / c
        return ("signed", (one_sale - one_cost) * 100 / one_cost)
    except Exception:
        return ("unsolved", q[:40])
