"""Independent solvers for Time and Work Rules 21-30. Each reads the numbers from the question text (number words
turned into digits first) and solves with one-day rates, a linear solve, brute force or a day-by-day count - never
through the rule formula gen_21_30.py uses."""
from fractions import Fraction as F
from solve_1_4 import finish_time, lin_solve
from solve_5_10 import nums


def solve21(rid, q):
    x, y, z, dc, db = nums(q)[:5]            # C leaves dc days before the end, B db days before
    # T/x + (T - db)/y + (T - dc)/z = 1 is linear in T: solve it from two trial values
    f = lambda T: T / x + (T - db) / y + (T - dc) / z - 1
    return ("number", -f(F(0)) / (f(F(1)) - f(F(0))))


def solve22(rid, q):
    M, D, d, m = nums(q)[:4]
    return ("number", finish_time(M - m, M * (D - d)))          # man-days of food left, eaten by M - m men a day


def solve23(rid, q):
    x, y = nums(q)[:2]                       # A + B in x days, C alone y days, A = B + C
    a, b, c = lin_solve([[1, -1, -1], [1, 1, 0], [0, 0, 1]], [0, 1 / x, 1 / y])
    return ("number", 1 / (a if "can A alone" in q else b))


def solve24(rid, q):
    x, D, d1, y, d2 = nums(q)[:5]
    work = x * d1 + (x + y) * (D - d1 - d2)                    # man-days actually spent
    days = finish_time(x, work)                                  # the first team alone
    return ("number", days - D if "delayed" in q else days)


def solve25(rid, q):
    x, y, z, d1, d2 = nums(q)[:5]            # A leaves after d1 days, B leaves d2 days before the end
    f = lambda T: d1 / x + (T - d2) / y + T / z - 1
    return ("number", -f(F(0)) / (f(F(1)) - f(F(0))))


def solve26(rid, q):
    a1, b1, a2, b2 = nums(q)[:4]
    a, b = lin_solve([[a1, b1], [a2, b2]], [1, 1])
    return ("pair", (1 / a, 1 / b))


def solve27(rid, q):
    x, y, d = nums(q)[:3]
    left = 1 - d * (1 / x + 1 / y)
    return ("number", finish_time(1 / y, left))


def solve28(rid, q):
    p, x, r = nums(q)[:3]
    return ("number", finish_time(p / x, r))                   # work p per x days -> days for r


def solve29(rid, q):
    n = nums(q)
    M1, T1, D1, M2, T2, W2, m1, h1, m2, h2 = n[:10]
    second_per_first = (m2 * h2) / (m1 * h1)                    # one first-group man-hour in second-group man-hours
    job = M1 * T1 * D1 * second_per_first * W2
    return ("number", finish_time(M2 * T2, job))


def solve30(rid, q):
    x, y = nums(q)[:2]
    T = next(F(k, 4) for k in range(1, 40000) if 1 / (F(k, 4) + x) + 1 / (F(k, 4) + y) == 1 / F(k, 4))
    return ("number", T)
