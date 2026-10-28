"""Independent solvers for Time and Work Rules 11-20. Each reads the numbers from the question text (number words
turned into digits first) and solves with one-day rates, brute force or a day-by-day count - never through the rule
formula gen_11_20.py uses."""
from fractions import Fraction as F
from solve_1_4 import finish_time
from solve_5_10 import nums


def solve11(rid, q):
    n, D = nums(q)[:2]                       # "A is 3 times as fast as B ... 60 days less"
    t = next(F(k, 100) for k in range(1, 10 ** 6) if F(k, 100) * n - F(k, 100) == D)   # A's own time, by search
    return ("number", 1 / (1 / t + 1 / (n * t)))


def solve12(rid, q):
    d1, h1, d2, h2, h = nums(q)[:5]
    per_hour = 1 / (d1 * h1) + 1 / (d2 * h2)
    return ("number", finish_time(per_hour * h))


def solve13(rid, q):
    x, y = nums(q)[:2]
    a, b = 1 / x, 1 / y
    c = a + b
    tail = q[q.rfind("How long"):]
    if "A, B and C" in tail:
        return ("number", finish_time(a + b + c))
    if "A and C" in tail:
        return ("number", finish_time(a + c))
    return ("number", finish_time(b + c))


def solve14(rid, q):
    k, x = nums(q)[:2]                       # A does k times B's work; together x days
    if q.startswith("A and B together"):     # "A and B together ... in 9 days. If A does twice as much ..."
        x, k = k, x
    b = 1 / (x * (k + 1))
    if "each separately" in q:
        return ("pair", (1 / (k * b), 1 / b))
    return ("number", 1 / (k * b))


def solve15(rid, q):
    a1, b1, k = nums(q)[:3]                  # a1 M + b1 B = k (M + B), B = 1
    return ("ratio", (k - b1) / (a1 - k))


def solve16(rid, q):
    n = nums(q)
    if "then B left" in q:                   # together T days, worked k days, A alone m more days
        T, k, m = n[:3]
        return ("number", m / (1 - k / T))
    x, y, z = n[:3]
    return ("number", (1 - z / y) / (1 / x + 1 / y))


def solve17(rid, q):
    x1, x2, x3, D = nums(q)[:4]
    return ("number", finish_time(1 / (x1 * D) + 1 / (x2 * D) + 1 / (x3 * D)))


def solve18(rid, q):
    x, n, y = nums(q)[:3]
    return ("number", F(next(M for M in range(int(n) + 1, 100000) if M * x == (M - n) * y)))


def solve19(rid, q):
    D, x, d = nums(q)[:3]
    return ("number", F(next(M for M in range(1, 100000) if M * D == (M + x) * (D - d))))


def solve20(rid, q):
    D, x, y, d = nums(q)[:4]
    work = x * d + (x + y) * (D - d)         # man-days actually spent
    days, done = 0, F(0)
    while done + x <= work:                  # the first x men alone, day by day
        done += x
        days += 1
    days = days + (work - done) / x
    return ("number", days - D if "behind schedule" in q else days)
