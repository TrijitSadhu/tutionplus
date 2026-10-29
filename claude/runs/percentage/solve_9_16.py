"""Independent solvers for Percentage Rules 9-16. They read the numbers from the question text and work with actual
values (a third number of 7, a factory of 40 men working 9 hours) or solve the story as a linear function of the
unknown - never through the rule formulas gen_9_16.py uses."""
import re
from fractions import Fraction as F
from solve_1_8 import pcts, rs, unknown

UP = ("increased", "goes up", "increase of", "raised", "rises")
DOWN = ("decreased", "cut", "reduced", "falls", "decrease of", "lowered")


def solve_wage(k, q):
    x, W = pcts(q)[0], rs(q)[-1]
    up = any(w in q for w in UP)
    assert up != any(w in q for w in DOWN), q
    s = 1 if up else -1
    return ("number", unknown(lambda w: w + s * w * x / 100, W))


def solve11(k, q):
    x = pcts(q)[0]
    men, hrs = F(40), F(9)                                   # any factory: production = men x hours
    target = men * hrs
    new_hrs = unknown(lambda h: men * (100 - x) / 100 * h, target)
    return ("number", (new_hrs - hrs) / hrs * 100)


def two_numbers(q):
    """Actual values of the first and second numbers for a third number of 7."""
    third = F(7)
    m = re.search(r"(\d+) and (\d+) per cent", q)            # "20 and 28 per cent less than a third number"
    x, y = (F(m[1]), F(m[2])) if m else pcts(q)[:2]
    if re.search(r"more than a third", q):
        return third * (1 + x / 100), third * (1 + y / 100)
    if re.search(r"less than a third", q):
        return third * (1 - x / 100), third * (1 - y / 100)
    assert re.search(r"of a third", q), q
    return third * x / 100, third * y / 100


def solve_rel(k, q):
    first, second = two_numbers(q)
    m = re.search(r"how much per cent is the (first|second) number less than the (first|second)", q)
    if m:
        a, b = (first, second) if m[1] == "first" else (second, first)
        return ("number", (b - a) / b * 100)
    m = re.search(r"(first|second) of the (first|second)", q)
    a, b = (first, second) if m[1] == "first" else (second, first)
    return ("number", a / b * 100)


solve9 = solve10 = solve_wage
solve12 = solve13 = solve14 = solve15 = solve16 = solve_rel
