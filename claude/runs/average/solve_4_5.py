"""Independent solver for Average Rules 4-5, keyed by row id / payload key; reads the numbers from the question in order and adds
up the totals item by item (a loop over every member, not the group formula), then shares them out."""
import re
from fractions import Fraction as F


def nums(q):
    return [F(t) for t in re.findall(r"\d+(?:\.\d+)?", q)]


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def pool(pairs):
    """pairs of (count, value): list every member and average them."""
    members = []
    for c, a in pairs:
        members += [a] * int(c)
    return F(sum(members), len(members))


def solve(k, q):
    try:
        v = nums(q)
        if k == "r4_e4":                                       # of N workers, a earn x and b earn y
            return ("number", pool([(v[1], v[2]), (v[3], v[4])]))
        if k in (490, 492, "r4_e3", "r4_ex2"):                  # count, average, count, average
            if k == 492:
                v = v[:4]
            return ("number", pool([(v[0], v[1]), (v[2], v[3])]))
        if k == 491:                                            # 5 pens for Rs 135, 7 pens for Rs 165
            c1, t1, c2, t2 = v[:4]
            return ("number", (t1 + t2) / (c1 + c2))
        if k == 493:                                            # Rs a1 for m1 months, Rs a2 for m2 months, saving
            a1, m1, a2, m2, save = v[:5]
            return ("number", (a1 * m1 + a2 * m2 + save) / (m1 + m2))
        if k in (494, 495, "r4_ex1", "r4_e5"):                 # three (count, value) groups
            return ("number", pool([(v[0], v[1]), (v[2], v[3]), (v[4], v[5])]))
        if k == 496:                                            # out of N, a at h1, b at h2, the rest at h3
            N, a, h1, b, h2, h3 = v[:6]
            return ("number", pool([(a, h1), (b, h2), (N - a - b, h3)]))
        if k == 497:                                            # Monday-Friday and Saturday-Sunday
            return ("number", pool([(5, v[0]), (2, v[1])]))
        if k == 498:
            return ("number", pool([(v[0], v[1]), (v[2], v[3])]))
        if k == 499:
            n, avg, kk, newavg = v[:4]
            return ("number", lin(lambda y: (n * avg + kk * y) / (n + kk) - newavg))
        if k in ("r4_e6", "r4_e15"):                            # of N, a at x, the rest at y
            N, a, x, y = v[:4]
            return ("number", pool([(a, x), (N - a, y)]))
        if k == "r4_e16":                                       # a of the N at x, the others at y
            a, N, x, y = v[:4]
            return ("number", pool([(a, x), (N - a, y)]))
        if k == "r4_e14":
            return ("number", pool([(v[0], v[1]), (v[2], v[3]), (v[4], v[5]), (v[6], v[7])]))
        if k in (500, "r5_e1", "r5_e2", "r5_e5", "r5_e6", "r5_e7"):   # N at x, n of them at y -> the rest
            N, x, n, y = v[:4]
            rest = [x] * int(N)
            total = sum(rest) - n * y
            return ("number", total / (N - n))
        if k == 501:
            N, x, n1, y1, n2, y2 = v[:6]
            return ("number", (N * x - n1 * y1 - n2 * y2) / (N - n1 - n2))
        if k == 502:                                            # N cows for Rs T, n of them average y
            N, T, n, y = v[:4]
            return ("number", (T - n * y) / (N - n))
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
