"""Independent solvers for Percentage Rules 49-56: maximum marks by trying every whole number, rectangle sides of 100
changed and multiplied, a class of 100 students marked one by one for 'failed in both', income/expenditure of 100
followed through, the salt kept equal before and after evaporation, and the library split run backwards - never
through the rule formulas gen_49_56.py uses."""
import re
from fractions import Fraction as F
from solve_1_8 import others, pcts, unknown
from solve_17_24 import run


def solve49(k, q):
    x, y = pcts(q)[:2]
    a = int(re.search(r"fails by (\d+)", q)[1])
    b = int(re.search(r"gets (\d+) marks more", q)[1])
    hits = [M for M in range(1, 20001) if F(M) * x / 100 + a == F(M) * y / 100 - b]
    assert len(hits) == 1, (q, hits)
    M = F(hits[0])
    if "pass percentage" in q:
        return ("number", (M * x / 100 + a) / M * 100)
    return ("number", M)


def sides(q):
    out = []
    for m in re.finditer(r"(\d+)% in (excess|deficit)|increased by (\d+)%|the other by (\d+)%", q):
        if m[1]:
            out.append(F(m[1]) * (1 if m[2] == "excess" else -1))
        elif m[3]:
            out.append(F(m[3]))
        else:
            out.append(F(m[4]))
    return out


def area_change(q):
    a, b = sides(q)[:2]
    return (100 + a) * (100 + b) / 100 - 100


def solve50(k, q):
    return ("signed", area_change(q))


def solve51(k, q):
    return ("number", area_change(q))


def solve52(k, q):
    return ("number", -area_change(q))


def solve53(k, q):
    ps = pcts(q)
    both = ps[2]
    first, second = ps[0], ps[1]
    fail_a = set(range(0, int(first)))                         # students 0..99, one per per cent
    fail_b = set(range(int(first) - int(both), int(first) - int(both) + int(second)))
    assert len(fail_a & fail_b) == both
    return ("number", F(sum(1 for s in range(100) if s not in fail_a | fail_b)))


def solve54(k, q):
    x, y, z = pcts(q)[:3]
    inc, spend = F(100), x
    old = inc - spend
    new = inc + inc * y / 100 - (spend + spend * z / 100)
    return ("number", (new - old) / old * 100)


def solve55(k, q):
    x, y = pcts(q)[:2]
    A = others(q)[0]
    return ("number", unknown(lambda s: x * s / 100 - y * (s - A) / 100, 0))


def solve56(k, q):
    return ("number", unknown(lambda t: run(t, pcts(q), -1), max(others(q))))
