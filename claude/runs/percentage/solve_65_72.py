"""Independent solvers for Percentage Rules 65-72: the split solved for one part, the tank capacity solved from the
filled share, three changes applied to 100 one after another, price x consumption on 100 x 100, three subjects counted by
marking 100 students one region at a time, and 100 houses sorted by occupants - never through the rule formulas
gen_65_72.py uses."""
import re
from fractions import Fraction as F
from solve_1_8 import others, pcts, unknown
from solve_33_40 import push, signed_changes


def solve65(k, q):
    N, p = others(q)[0], pcts(q)[0]
    x = unknown(lambda x: x + x * p / 100, N)
    return ("pair", (x, N - x))


def tank(q):
    X, x = others(q)[0], pcts(q)[0]
    return X, unknown(lambda c: c * (100 - x) / 100, X)


def solve66(k, q):
    X, C = tank(q)
    return ("number", C - X)


def solve67(k, q):
    return ("number", tank(q)[1])


def solve68(k, q):
    return ("number", push(pcts(q)[:3]) - 100)


def solve69(k, q):
    return ("number", 100 - push([-p for p in pcts(q)[:3]]))


def solve70(k, q):
    a, b = signed_changes(q)[:2]
    return ("ratio", push([a], F(100)) * push([b], F(100)) / 10000)


def solve71(k, q):
    m, e, h, me, eh, mh, al = (int(v) for v in pcts(q)[:7])
    students = [set() for _ in range(100)]                    # which subjects each of 100 students failed
    nxt = 0

    def mark(count, subjects):
        nonlocal nxt
        for s in range(nxt, nxt + count):
            students[s] |= subjects
        nxt += count

    mark(al, {"M", "E", "H"})
    mark(me - al, {"M", "E"}); mark(eh - al, {"E", "H"}); mark(mh - al, {"M", "H"})
    for subj, total in (("M", m), ("E", e), ("H", h)):
        mark(total - sum(1 for s in students if subj in s), {subj})
    assert [sum(1 for s in students if x in s) for x in "MEH"] == [m, e, h]
    return ("number", F(sum(1 for s in students if not s)))


def solve72(k, q):
    x, y = pcts(q)[:2]
    houses = []
    for i in range(100 * 100):                                  # 10000 houses so every share is a whole number
        houses.append("many" if i < 100 * x else "one")
    one = [i for i, h in enumerate(houses) if h == "one"]
    for i in one[:int(len(one) * y / 100)]:
        houses[i] = "male"
    return ("number", F(sum(1 for h in houses if h == "one"), 100))
