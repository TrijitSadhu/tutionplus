"""Independent solvers for Percentage Rules 41-48. Changes get their direction from the nearby words (solve_33_40), then
two factors of 100 each are changed and multiplied (rules 42-47), a value of 100 is cut twice (41), a bill is solved
from the two ways of paying it, and the maximum marks are found by trying every whole number - never through the rule
formulas gen_41_48.py uses."""
import re
from fractions import Fraction as F
from solve_1_8 import pcts, rs, unknown
from solve_33_40 import push, signed_changes


def solve41(k, q):
    if "bill" in q:
        single, each = pcts(q)[:2]
        gap = rs(q)[-1]
        return ("number", unknown(lambda b: abs(push([-single], b) - push([-each, -each], b)), gap))
    return ("number", 100 - push(signed_changes(q)))


def solve_product(k, q):
    a, b = signed_changes(q)[:2]
    return ("signed", push([a], F(100)) * push([b], F(100)) / 100 - 100)


def solve48(k, q):
    x = pcts(q)[0]
    m = re.search(r"gets (\d+) marks,? (?:and )?fails by (\d+)", q)
    need = int(m[1]) + int(m[2])
    hits = [M for M in range(1, 20001) if F(M) * x / 100 == need]
    assert len(hits) == 1, (q, hits)
    return ("number", F(hits[0]))


solve42 = solve43 = solve44 = solve45 = solve46 = solve47 = solve_product
