"""Independent solvers for Time and Work Rules 5-10. Each reads the numbers from the question text (number words
such as "Five", "twice", "thrice" turned into digits first) and solves with one-day rates, a linear solve or brute
force - never through the rule formula gen_5_10.py uses."""
import re
from fractions import Fraction as F
from validate import numbers
from solve_1_4 import finish_time, lin_solve

WORDS = {"twice": "2 times", "thrice": "3 times", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6",
         "seven": "7", "eight": "8", "nine": "9", "ten": "10"}


def nums(q):
    q = re.sub(r"\b(" + "|".join(WORDS) + r")\b", lambda m: WORDS[m[1].lower()], q, flags=re.I)
    return numbers(q)


def solve5(rid, q):
    n = nums(q)
    if "half as long" in q:                       # rates: A u, B u/2, C = A + B
        u = 1 / n[-1] / (1 + F(1, 2) + 1 + F(1, 2))
        return ("triple", (1 / u, 2 / u, 1 / (u + u / 2)))
    if "as much time as B" in q:                  # A takes 2x B's time and 3x C's time: rates u, 2u, 3u
        u = 1 / n[-1] / 6
        return ("triple", (1 / u, 1 / (2 * u), 1 / (3 * u)))
    if "children" in q:
        m, tm, w, tw, c, tc = n[:6]
        return ("number", 1 / (1 / (m * tm) + 1 / (w * tw) + 1 / (c * tc)))
    if "A, B and C together in" in q:
        x, y, t = n[:3]
        return ("number", 1 / (1 / t - 1 / x - 1 / y))
    x, y, z = n[:3]
    return ("number", finish_time(1 / x + 1 / y + 1 / z))


def solve6(rid, q):
    n = nums(q)
    low = q.lower()
    if "respectively" in low:
        x, y, z = n[:3]
        return ("number", 1 / (1 / x + 1 / y + 1 / z))
    if "help of c" in low or "c alone will finish" in low:
        ab, abc = n[:2]
        return ("number", 1 / (1 / abc - 1 / ab))
    if "can a and b do it" in low:                # B, B + C, A + B + C -> A + B
        b, bc, abc = n[:3]
        a, b_, c = lin_solve([[0, 1, 0], [0, 1, 1], [1, 1, 1]], [1 / b, 1 / bc, 1 / abc])
        return ("number", 1 / (a + b_))
    if "a and c together take" in low:            # A + B, B + C, A + B + C -> (A + C, B)
        ab, bc, abc = n[:3]
        a, b, c = lin_solve([[1, 1, 0], [0, 1, 1], [1, 1, 1]], [1 / ab, 1 / bc, 1 / abc])
        return ("pair", (1 / (a + c), 1 / b))
    if "calls in b" in low:
        p, d, e = n[:3]
        ab = (1 - p) / e
        return ("number", 1 / (ab - p / d))
    if "stops after" in low:                      # both work k days, then A alone
        ab, b, k = n[:3]
        return ("number", (1 - k / ab) / (1 / ab - 1 / b))
    if "called off" in low:
        ab, k, m = n[:3]
        a = (1 - k / ab) / m
        return ("pair", (1 / a, 1 / (1 / ab - a)))
    if "which b alone" in low:                    # A + B + C, B, B + C -> A + B
        abc, b, bc = n[:3]
        a = 1 / abc - 1 / bc
        return ("number", 1 / (a + 1 / b))
    if "b alone works" in low:                    # B alone k days, then A alone
        ab, b, k = n[:3]
        return ("number", (1 - k / b) / (1 / ab - 1 / b))
    ab, t = n[:2]
    return ("number", 1 / (1 / ab - 1 / t))


def solve7(rid, q):
    n = nums(q.replace("three men together", "men together"))
    if "as much as" in q:                         # T first, then "A and C work n times as much as B", "A and B ... m times ... C"
        T, nb, mc = n[:3]
    else:                                         # "B would take n times as long as A and C", "C m times as long as A and B", T
        nb, mc, T = n[:3]
    a, b, c = lin_solve([[1, -nb, 1], [1, 1, -mc], [1, 1, 1]], [0, 0, 1 / T])
    if "each" in q:
        return ("triple", (1 / a, 1 / b, 1 / c))
    return ("number", 1 / (b + c))


def solve8(rid, q):
    n = nums(q)
    if "whereas" in q:
        x1, D, y1, _, x2, y2 = n[:6]
    else:
        x1, y1, D, x2, y2 = n[:5]
    rate = x2 / (x1 * D) + y2 / (y1 * D)
    part = F(1, 2) if "half" in q else F(1)
    return ("number", part / rate)


def solve9(rid, q):
    n = nums(q)
    low = q.lower()
    if "children" in low:                         # a child takes f times ("twice") a man's time
        c, m, D, f, m2 = n[:5]
        man = 1 / ((c / f + m) * D)
        return ("number", 1 / (m2 * man))
    if "as much as 5 boys" in low or "can do as much as" in low:
        m1, b1, D, m2, b2, em, eb = n[:7]
        boy = 1 / ((m1 * eb / em + b1) * D)
        return ("number", 1 / ((m2 * eb / em + b2) * boy))
    if "times as" in low:                         # a1 M + b1 B = k (a2 M + b2 B), B = 1
        a1, b1, k = n[:3]
        a2, b2 = (n[3], n[4]) if len(n) >= 5 else (1, 1)
        M = (k * b2 - b1) / (a1 - k * a2)
        return ("ratio", M)
    if "hire" in low:                             # (a1 M + b1 B) d1 = (a2 M + b2 B) d2, B = 1
        a1, b1, d1, a2, b2, d2 = n[:6]
        M = (d2 * b2 - d1 * b1) / (d1 * a1 - d2 * a2)
        return ("ratio", 1 / M)
    a1, b1, x, a2, b2, y = n[:6]
    man, boy = lin_solve([[a1 * x, b1 * x], [a2 * y, b2 * y]], [1, 1])
    if "how long" in low:
        a3, b3 = n[6:8]
        return ("number", finish_time(a3 * man + b3 * boy))
    if "work of a boy with that of a man" in low:
        return ("ratio", boy / man)
    return ("ratio", man / boy)


def solve10(rid, q):
    D, x, d = nums(q)[:3]
    M = next(M for M in range(int(x) + 1, 100000) if M * D == (M - x) * (D + d))
    return ("number", F(M))
