"""Independent solvers for Time and Work Rules 36-40. Each reads the numbers from the question text and solves with
one-day rates, a linear solve or brute force - never through the rule formula gen_36_40.py uses."""
import re
from fractions import Fraction as F
from solve_5_10 import nums


def linear(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def solve36(rid, q):
    x, y, a = nums(q)[:3]                    # B leaves a days before the end
    return ("number", linear(lambda T: T / x + (T - a) / y - 1))


def solve37(rid, q):
    x, y, a = nums(q)[:3]                    # A leaves a days before the end
    return ("number", linear(lambda T: (T - a) / x + T / y - 1))


def solve38(rid, q):
    x, a, b = nums(q)[:3]
    left = 1 - a / x
    B = b / left
    if "together" in q:
        return ("number", 1 / (1 / x + 1 / B))
    return ("number", B)


def solve39(rid, q):
    x, y, a = nums(q)[:3]
    return ("number", next(F(k, 12) for k in range(1, 12000) if F(k, 12) / x + (F(k, 12) + a) / y == 1))


def solve40(rid, q):
    n = nums(q)
    x, y, a = n[:3]                          # first-named worker x days, second y days, starter works a days alone
    m = re.match(r"(\w+) and (\w+) can complete", q)
    starter = re.search(r"(\w+) start", q).group(1)
    if m and starter == m.group(2):          # the second-named person starts
        x, y = y, x
    left = 1 - a / x
    t = left / (1 / x + 1 / y)
    return ("number", a + t if "In all" in q else t)
