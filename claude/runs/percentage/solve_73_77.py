"""Independent solvers for Percentage Rules 73-77: the third person's income solved from the stated difference, the two
weights solved from the new total, the income solved from the savings left after both spends, the new consumption from
spending / price, and the expenditure from price x consumption - never through the rule formulas gen_73_77.py uses."""
import re
from fractions import Fraction as F
from solve_1_8 import pcts, rs, unknown
from solve_33_40 import push


def solve73(k, q):
    x, y = pcts(q)[:2]
    M = rs(q)[-1]
    c = unknown(lambda c: abs(c * (1 - y / 100) * (1 + x / 100) - c), M)
    b = c * (1 - y / 100)
    return ("pair", (b, c)) if re.search(r"incomes of \w+ and \w+\?", q) else ("number", b)


def solve74(k, q):
    a, b = (F(int(v)) for v in re.search(r"ratio (\d+) : (\d+)", q).groups())
    x, y = pcts(q)[:2]
    W = F(re.search(r"becomes ([\d.]+) kg", q)[1])
    kk = unknown(lambda k: (a + b) * k * (1 + y / 100), W)
    b_new = W - a * kk * (1 + x / 100)
    return ("number", (b_new - b * kk) / (b * kk) * 100)


def solve75(k, q):
    x, y = pcts(q)[:2]
    S = rs(q)[-1] / (12 if "end of the year" in q else 1)
    I = unknown(lambda i: i * (1 - x / 100) * (1 - y / 100), S)
    A = I * x / 100
    B = (I - A) * y / 100
    if "monthly salary." in q or "find his monthly salary" in q:
        return ("number", I)
    if "clothes and transport?" in q:
        return ("number", B)
    return ("triple", (I, A, B))


def solve76(k, q):
    x, y = pcts(q)[:2]
    W = F(int(re.search(r"If (\d+) kg", q)[1]))
    spend = 1 * W * (1 + y / 100)                               # old price taken as Rs 1 per kg
    return ("number", spend / (1 + x / 100))


def solve77(k, q):
    x = pcts(q)[0]
    return ("signed", push([x], F(100)) * push([-x], F(100)) / 100 - 100)
