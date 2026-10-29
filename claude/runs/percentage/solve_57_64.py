"""Independent solvers for Percentage Rules 57-64: the profit chain run forward and solved for the cost, the acid / milk /
iron kept fixed while the total is solved, 100 students followed through two schools, a family's 100 kg bill kept fixed
at the new price, the original price searched among all quarter-rupee prices (Rule 63), and the extra quantity solved
for one over the price (Rule 64) - never through the rule formulas gen_57_64.py uses."""
import re
from fractions import Fraction as F
from solve_1_8 import pcts, rs, unknown
from solve_17_24 import run

WORD = {"one": 1, "two": 2, "three": 3}


def solve57(k, q):
    return ("number", unknown(lambda c: run(c, pcts(q), 1), rs(q)[-1]))


def solve_water(k, q):
    x, y = pcts(q)[:2]
    A = F(int(re.search(r"(\d+) litres", q)[1]))
    T = unknown(lambda t: y * t / 100, x * A / 100)
    return ("number", abs(T - A))


def solve60(k, q):
    prev, new = pcts(q)[:2]
    M = F(int(re.search(r"(\d+) kg mixture", q)[1]))
    T = unknown(lambda t: new * t / 100, prev * M / 100)
    return ("number", T - M)


def solve61(k, q):
    p, a, extra = pcts(q)[:3]
    appeared_b = 100 + 100 * a / 100
    qualified_b = p + p * extra / 100
    return ("number", qualified_b / appeared_b * 100)


def solve62(k, q):
    Y = F(int(re.search(r"now being sold at Rs (\d+)", q)[1]))
    X = F(int(re.search(r"cost was Rs (\d+)", q)[1]))
    c = unknown(lambda c: Y * c, 100 * X)
    return ("number", abs(c - 100))


def solve63(k, q):
    d = F(int(re.search(r"reduction of (?:Rs|Re) (\d+)", q)[1]))
    w = re.search(r"(\d+|one|two|three) (?:kg|dozen) more", q)[1]
    more = F(int(w)) if w.isdigit() else F(WORD[w])
    E = rs(q)[-1]
    hits = [F(n, 4) for n in range(1, 40001) if F(n, 4) > d and E / (F(n, 4) - d) - E / F(n, 4) == more]
    assert len(hits) == 1, (q, hits)
    return ("number", hits[0])


def solve64(k, q):
    p = pcts(q)[0]
    more = F(int(re.search(r"(\d+) (?:kg )?more", q)[1]))
    E = F(1) if "for a rupee" in q else rs(q)[-1]
    u = unknown(lambda u: E * u * (1 / (1 - p / 100) - 1), more)      # u = 1 / original price
    O = 1 / u
    N = O * (1 - p / 100)
    if "reduced price and the original price" in q:
        return ("pair", (N, O))
    if "did a rupee buy before" in q:
        return ("number", u)
    return ("number", O)


solve58 = solve59 = solve_water
