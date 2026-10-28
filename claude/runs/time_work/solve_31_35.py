"""Independent solvers for Time and Work Rules 31-35. Each reads the numbers from the question text and solves by a
day-by-day (or hour-by-hour) simulation, a linear solve or brute force - never through the rule gen_31_35.py uses."""
import math
from fractions import Fraction as F
from solve_1_4 import finish_time, lin_solve
from solve_5_10 import nums
from validate import numbers


def solve31(rid, q):
    n = nums(q)
    if "assist" in q:                                    # man, woman, boy times; men, women, days -> boys
        tm, tw, tb, men, women, d = n[:6]
        left = 1 - men * d / tm - women * d / tw
        return ("number", left / (d / tb))
    if "C finishes it" in q:                             # A + B, B + C, days of A, B, C -> each alone
        ab, bc, da, db, dc = n[:5]
        a, b, c = lin_solve([[1, 1, 0], [0, 1, 1], [da, db, dc]], [1 / ab, 1 / bc, 1])
        return ("triple", (1 / a, 1 / b, 1 / c))
    if "helped on every" in q:
        ta, tb, tc, k = n[:4]
        done, day = F(0), 0
        while True:
            day += 1
            rate = 1 / ta + ((1 / tb + 1 / tc) if day % k == 0 else 0)
            if done + rate >= 1:
                return ("number", day - 1 + (1 - done) / rate)
            done += rate
    if "C joins A" in q:
        ta, tb, both, alone, with_c = n[:5]
        left = 1 - both * (1 / ta + 1 / tb) - alone / ta - with_c / ta
        return ("number", with_c / left)
    if "joined B" in q:                                  # B alone first, A joins for the last d days
        ta, tb, d = n[:3]
        return ("number", next(F(k, 4) for k in range(1, 4000) if d / ta + (F(k, 4) + d) / tb == 1))
    if "days less than B" in q:
        less, da, total = n[:3]
        x = next(F(k) for k in range(1, 1000) if da / F(k) + (total - da) / (F(k) + less) == 1)
        return ("pair", (x, x + less))
    if "help of C" in q:
        ta, tb, T = n[:3]
        return ("number", 1 / (1 / T - 1 / ta - 1 / tb))
    ta, tb, z = n[:3]                                    # began together, A left after some days, B finished in z
    return ("number", next(F(k, 4) for k in range(1, 4000) if F(k, 4) / ta + (F(k, 4) + z) / tb == 1))


def alternate(first, second):
    """Hour-by-hour (or day-by-day) simulation: returns the time taken."""
    done, t = F(0), 0
    while True:
        rate = 1 / (first if t % 2 == 0 else second)
        if done + rate >= 1:
            return t + (1 - done) / rate
        done += rate
        t += 1


def solve32(rid, q):
    n = numbers(q)                                       # digits only: "Two women, Ganga and Jamuna" must not add a 2
    x, y = n[:2]
    b_first = "B starts" in q
    T = alternate(y, x) if b_first else alternate(x, y)
    if " am" in q.lower() or "o'clock" in q:            # clock time: start hour is the third number
        minutes = (n[2] * 60 + T * 60)
        assert minutes.denominator == 1
        h24, m = divmod(int(minutes), 60)
        return ("pair", (F((h24 % 12) or 12), F(m)))
    if "On which day" in q:
        return ("number", n[2] + math.ceil(T) - 1)
    return ("number", T)


def solve33(rid, q):
    T, a, b = nums(q)[:3]
    return ("number", 1 / (1 / T - 1 / a - 1 / b))


def solve34(rid, q):
    x, y, a = nums(q)[:3]
    return ("number", finish_time(1 / y, 1 - a / x))


def solve35(rid, q):
    n = nums(q)
    if "working together" in q:                          # A + B together, B alone, B works d days
        ab, b, d = n[:3]
        return ("number", (1 - d / b) / (1 / ab - 1 / b))
    if "B and C start" in q:
        a, b, c, d = n[:4]
        return ("number", (1 - d * (1 / b + 1 / c)) * a)
    x, y, d = n[:3]                                      # A alone x, B alone y, B works d days
    return ("number", finish_time(1 / x, 1 - d / y))
