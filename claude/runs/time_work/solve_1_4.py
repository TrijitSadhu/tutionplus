"""Independent solvers for Time and Work Rules 1-4. Each reads the numbers from the question text and solves by
brute force, day-by-day simulation or a linear solve of the one-day rates - never through the rule formula
gen_1_4.py uses."""
from fractions import Fraction as F
from validate import numbers


def lin_solve(m, b):
    """Gauss-Jordan elimination on Fractions."""
    n = len(b)
    a = [[F(x) for x in row] + [F(v)] for row, v in zip(m, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[p] = a[p], a[c]
        a[c] = [x / a[c][c] for x in a[c]]
        for r in range(n):
            if r != c and a[r][c] != 0:
                a[r] = [x - a[r][c] * y for x, y in zip(a[r], a[c])]
    return [row[-1] for row in a]


def finish_time(rate, work=F(1)):
    """Days needed at `rate` per day, counted day by day (the last day may be a part-day)."""
    t, done = 0, F(0)
    while done + rate <= work:
        done += rate
        t += 1
    return t + (work - done) / rate


def solve1(rid, q):
    n = numbers(q)
    if "trees" in q:
        M1, W1, D1, leave, D2 = n[:5]
        per_man_hour = W1 / (M1 * D1)
        return ("number", sum((M1 - leave) * per_man_hour for _ in range(int(D2))))
    if "works of the same type" in q:
        D1, k = n[:2]
        return ("number", finish_time(1 / D1, F(k)))
    M1, D1, D2 = n[:3]
    M = next(M for M in range(1, 100000) if M * D2 >= M1 * D1)
    assert M * D2 == M1 * D1
    return ("number", F(M))


def solve2(rid, q):
    n = numbers(q)
    if "woman" in q:
        hw, hm, hb, T1, M1, D1, men, women, boys, T2 = n[:10]
        job = M1 * T1 * D1 / hm                           # in "parts", a part = what a woman does in hw hours
        per_hour = men / hm + women / hw + boys / hb
        return ("number", finish_time(per_hour * T2, job))
    M1, W1, D1, T1, M2, W2, T2 = n[:7]
    toys_per_man_hour = W1 / (M1 * D1 * T1)
    return ("number", finish_time(M2 * T2 * toys_per_man_hour, W2))


def solve3(rid, q):
    n = numbers(q)
    x, y, z = n[:3]
    a, b, c = lin_solve([[1, 1, 0], [0, 1, 1], [1, 0, 1]], [1 / x, 1 / y, 1 / z])
    if "each" in q:
        return ("triple", (1 / a, 1 / b, 1 / c))
    if "leaves" in q:
        d_all, d_bc = n[3:5]
        left = 1 - d_all * (a + b + c) - d_bc * (b + c)
        return ("number", finish_time(c, left))
    return ("number", finish_time(a + b + c))


def solve4(rid, q):
    n = numbers(q)
    if "finishes it in" in q or "completes the rest" in q:
        x, y, k, m = n[:4]
        left = 1 - k * (1 / x + 1 / y)
        return ("number", 1 / (left / m))
    if "takes as long as A and B" in q:
        x, y = n[:2]
        c = 1 / x + 1 / y
        return ("number", finish_time(1 / y + c))
    if "A and C" in q:
        ta, tbc, tac = n[:3]
        a, b, c = lin_solve([[1, 0, 0], [0, 1, 1], [1, 0, 1]], [1 / ta, 1 / tbc, 1 / tac])
        return ("number", 1 / b)
    if "remainder" in q:
        p, d, e = n[:3]
        return ("number", finish_time((1 - p) / e))
    if "women" in q:
        g1, x, g2, y = n[:4]
        return ("number", finish_time(1 / x + 1 / y))
    if len(n) >= 4 and n[0] < 1 and n[2] < 1:            # A does p of it in d days, B does r of it in e days
        p, d, r, e = n[:4]
        return ("number", finish_time(p / d + r / e))
    x, y = n[:2]
    return ("number", finish_time(1 / x + 1 / y))
