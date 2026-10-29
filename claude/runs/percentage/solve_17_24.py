"""Independent solvers for Percentage Rules 17-24. They read the numbers from the question text and play the story
forward step by step (or year by year); a starting amount is found by solving that simulation as a linear function of
the start - never through the rule formulas gen_17_24.py uses."""
import re
from fractions import Fraction as F
from solve_1_8 import others, pcts, rs, unknown

WORDS = {"two": 2, "three": 3, "four": 4}


def run(start, steps_, sign):
    cur = start
    for p in steps_:
        cur = cur + sign * cur * p / 100
    return cur


def final_amount(q):
    m = re.search(r"(\d+) m (\d+) cm", q)
    return F(int(m[1])) + F(int(m[2]), 100) if m else rs(q)[-1]


def solve17(k, q):
    return ("number", unknown(lambda s: run(s, pcts(q), -1), final_amount(q)))


def solve18(k, q):
    return ("number", run(rs(q)[0], pcts(q), -1))


def solve19(k, q):
    return ("number", unknown(lambda s: run(s, pcts(q), 1), final_amount(q)))


def solve20(k, q):
    return ("number", run(rs(q)[0], pcts(q), 1))


def solve_population(k, q):
    r = pcts(q)[0]
    yrs = [int(y) for y in re.findall(r"year (\d{4})", q)]
    if yrs:
        n = abs(yrs[0] - yrs[1])
    else:
        w = re.search(r"(\d+|two|three|four) years", q)[1]
        n = int(w) if w.isdigit() else WORDS[w]
    size = max(others(q) + rs(q))
    grow = any(w in q for w in ("increase", "grows", "grow by"))
    assert grow != any(w in q for w in ("decrease", "falls")), q
    sign = 1 if grow else -1
    year = lambda p: run(p, [r] * n, sign)                    # one step per year
    if "ago" in q or re.search(r"what were its", q):
        return ("number", unknown(year, size))
    return ("number", year(size))


solve21 = solve22 = solve23 = solve24 = solve_population
