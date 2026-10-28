"""Independent solvers for the book's Miscellaneous Time and Work problems (rows 261-277 and the new M4), keyed by row id.
Each reads the numbers from the question text and solves with one-day rates, a linear solve, brute force or a
day-by-day count - never through the rule gen_misc.py uses."""
import re
from fractions import Fraction as F
from solve_1_4 import finish_time, lin_solve
from solve_5_10 import nums
from validate import X_VAL, Y_VAL, numbers

WORDNUM = {"twelve": 12, "sixteen": 16, "twenty-four": 24, "thirty-two": 32}


def words(q):
    return [F(WORDNUM[w.lower()]) if w.lower() in WORDNUM else F(w)
            for w in re.findall(r"twenty-four|thirty-two|sixteen|twelve|\d+", q, flags=re.I)]


def solve(rid, q):
    if rid == 261:                                       # men or women times; 16m + 16w for 12 days; extra men for 2 days
        m1, d1, w1, d2, m, w, t, last = words(q)[:8]
        man, woman = 1 / (m1 * d1), 1 / (w1 * d2)
        left = 1 - t * (m * man + w * woman) - last * (m * man + w * woman)
        return ("number", left / (last * man))
    if rid == 262:
        m, w, D, k, m2, d, w2 = nums(q)[:7]
        man, woman = lin_solve([[m * D, w * D], [m * k + m2 * d, w * k]], [1, 1])
        return ("number", 1 / (w2 * woman))
    if rid == 263:
        m, w, D, one, dm = nums(q)[:5]
        man = 1 / dm
        woman = (1 / D - m * man) / w
        return ("number", 1 / woman)
    if rid == 264:
        m, D, w, D2, part, m2, w2 = numbers(q)[:7]
        man, woman = 1 / (m * D), part / (w * D2)
        return ("number", 1 / (m2 * man + w2 * woman))
    if rid == 265:
        a1, b1, h1, d1, a2, b2, h2, d2, a3, h3, d3 = numbers(q)[:11]
        man, boy = lin_solve([[a1 * d1, b1 * d1], [a2 * d2, b2 * d2]], [h1, h2])   # hectares a day
        return ("number", (h3 / d3 - a3 * man) / boy)
    if rid == 266:                                       # 25 men, 20 days; 15 leave; the rest take 37.5 more days
        M, D, leave, after = numbers(q)[:4]
        t = next(F(k, 4) for k in range(1, 4000) if M * F(k, 4) + (M - leave) * after == M * D)
        return ("number", t)
    if rid == 267:                                       # pages: A alone, A and B together, B's time for some pages
        pa, ha, pab, hab, pb = numbers(q)[:5]
        b_speed = pab / hab - pa / ha
        return ("number", pb / b_speed)
    if rid == 268:
        M, D, every, extra = numbers(q)[:4]
        need, done, day, men = M * D, F(0), 0, M
        while done < need:
            day += 1
            done += men
            if day % every == 0:
                men += extra
        return ("number", F(day))
    if rid == 269:
        D, half, extra = numbers(q)[:3]
        return ("number", F(next(M for M in range(1, 10000) if M * half == (M + extra) * (D - half))))
    if rid == 270:
        alone, worked, with_d = numbers(q)[:3]
        left = 1 - worked / alone
        both = left / with_d
        return ("number", 1 / both)
    if rid == 271:
        a, pct = numbers(q)[:2]
        return ("number", 1 / ((1 + pct / 100) / a))
    if rid == 272:
        m, D, after, join, replace = numbers(q)[:5]
        left = m * D - m * after
        return ("number", left / (m - replace + join))
    if rid == 273:
        a, b, c, hours = numbers(q)[:4]
        left = 1 - hours * (1 / a + 1 / b + 1 / c)
        return ("number", left / (1 / a + 1 / b))
    if rid == 274:                                       # A does half as much as B in three-fourth of the time
        T = numbers(q)[0]
        b = 1 / (T * (1 + F(1, 2) / F(3, 4)))
        return ("number", 1 / b)
    if rid == 275:                                       # A twice as efficient, B one-third as efficient
        T1, k_b, T2 = numbers(q)[:3]                     # digits only ("Two workers" must not count); "twice" -> 2
        k_a = F(2) if "twice" in q else F(1)
        a, b = lin_solve([[T1, T1], [k_a * T2, k_b * T2]], [1, 1])
        return ("number", 1 / a)
    if rid == 276:                                       # mows the lawn in x hours, rain after h hours: part left
        h = numbers(q)[0]
        return ("expr", 1 - h / X_VAL)
    if rid == 277:                                       # A: x cars an hour, B: y cars every k hours, over T hours
        k, T = numbers(q)[:2]
        return ("expr", T * X_VAL + T / k * Y_VAL)
    if rid == "m4":                                      # A, B alone; C takes p of (A + B)'s time; A + B work d days
        x, y, p, d = numbers(q)[:4]
        ab = 1 / x + 1 / y
        c_time = p / ab
        return ("number", (1 - d * ab) * c_time)
    raise KeyError(rid)
