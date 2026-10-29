"""Independent solvers for Percentage Rules 33-40. Each percentage in the question gets its direction from the nearest
direction word ("increased", "reduced", "discount", "higher" ...), then a starting value of 100 is pushed through the
changes in the order they happen; the other-side rules (33-35) compare actual values or solve for the consumption that
keeps the bill fixed - never through the rule formulas gen_33_40.py uses."""
import re
from fractions import Fraction as F
from validate import numbers
from solve_1_8 import NUM, pcts, unknown

UP = r"increas|higher|rais|rise|grow|marks|above|goes up"
DOWN = r"decreas|reduc|discount|cut|fall|lower|diminish"


def signed_changes(q):
    words = [(m.start(), m.end(), 1 if re.match(UP, m.group(0)) else -1) for m in re.finditer(rf"{UP}|{DOWN}", q)]
    out = []
    for m in re.finditer(rf"({NUM})(?:\\\))?\s*(?:\\%|%)", q):
        if not re.search(r"\d", m.group(1)):
            continue
        after = [w for w in words if 0 <= w[0] - m.end() <= 2]               # "20% higher": the word right after the number
        before = [w for w in words if w[1] <= m.start()]                      # otherwise the last direction word before it
        near = after[0] if after else before[-1]
        out.append(near[2] * numbers(m.group(1))[0])
    return out


def push(changes, start=F(100)):
    v = start
    for c in changes:
        v = v + v * c / 100
    return v


def solve33(k, q):
    r = pcts(q)[0]
    if "bring it back" in q:
        low = push([-r])
        return ("number", unknown(lambda p: push([p], low), F(100)))      # the % rise taking the cut price back to 100
    c = unknown(lambda c: (100 - r) * c, F(100) * 100)                      # consumption that keeps price x consumption = 10000
    return ("number", c - 100)


def solve34(k, q):
    r = pcts(q)[0]
    b = F(7)
    a = b + b * r / 100
    return ("number", (a - b) / a * 100)


def solve35(k, q):
    r = pcts(q)[0]
    b = F(7)
    a = b - b * r / 100
    return ("number", (b - a) / a * 100)


def solve_signed(k, q):
    return ("signed", push(signed_changes(q)) - 100)


def solve_up(k, q):
    return ("number", push(signed_changes(q)) - 100)


def solve40(k, q):
    return ("number", 100 - push(signed_changes(q)))


solve36 = solve37 = solve_signed
solve38 = solve39 = solve_up
