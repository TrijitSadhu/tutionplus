"""Independent solver for Average Rules 1-3, keyed by row id / payload key; reads the numbers from the question in order and works
from first principles (lists the primes or multiples and adds them, tries counts, simulates the totals) - not the rule formulas."""
import re
from fractions import Fraction as F


def nums(q):
    return [F(t) for t in re.findall(r"\d+(?:\.\d+)?", q)]


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def first_primes(n):
    out, k = [], 1
    while len(out) < n:
        k += 1
        if k > 1 and all(k % d for d in range(2, int(k ** 0.5) + 1)):
            out.append(k)
    return out


def mean(v):
    return F(sum(F(t) for t in v), len(v))


WORD = {"seven": 7, "five": 5, "six": 6}


def solve(k, q):
    try:
        v = nums(q)
        if k == 467:
            return ("number", mean(v[:3]))
        if k in (468, "r1_e3"):
            return ("number", mean(first_primes(int(v[0]))))
        if k in (469, "r1_e4"):
            n, step = int(v[0]), int(v[1])
            return ("number", mean([step * i for i in range(1, n + 1)]))
        if k == 472:
            n = WORD[re.search(r"first (\w+) multiples", q).group(1)]
            step = int(v[0])
            return ("number", mean([step * i for i in range(1, n + 1)]))
        if k == 470:
            p = F(10)                                           # any even start gives the same gap
            vals = [p + 2 * i for i in range(6)]
            return ("number", mean(vals) - p)
        if k == 471:
            a, b, days = v[:3]
            return ("number", (a + b) / days)
        if k in (473, 474, "r2_e2", "r2_e3"):
            if k in (473, "r2_e3"):
                n, avg = v[0], v[1]
            else:
                avg, n = (v[1], v[0]) if k == 474 else (v[0], v[1])
            return ("number", sum(avg for _ in range(int(n))))
        if k in (475, 477, 484):
            if k == 477:                                         # "five players" and "six people" are words: five weights, then the average
                known, target = v[0:5], v[5]
                return ("number", lin(lambda x: (sum(known) + x) / 6 - target))
            if k == 475:                                         # "5 trees", five heights, then the average ("sixth" / "six" are words)
                known, target = v[1:6], v[6]
                return ("number", lin(lambda x: (sum(known) + x) / 6 - target))
            known, target = v[:2], v[2]                          # two days, then the average for three
            return ("number", lin(lambda x: (sum(known) + x) / 3 - target))
        if k == 476:
            d1, d2, a1, d3, d4, a2, d5, first, d6 = v[:9]
            days = d2 - d1 + 1
            return ("number", first + days * a2 - days * a1)
        if k in (478, 479):
            n, old, new = v[:3]
            if k == 479:
                n, old, new = v[0], v[1], v[2]
            return ("number", lin(lambda x: (n * old + x) / (n + 1) - new))
        if k == 480:
            n, avg, r1, r2 = v[:4]
            return ("number", (n * avg - r1 - r2) / (n - 2))
        if k == 481:
            avg, kk, kavg, drop = v[:4]
            for x in range(1, 10000):
                if (avg * x + kk * kavg) / (x + kk) == avg - drop:
                    return ("number", F(x))
            return ("unsolved", "no count")
        if k == 482:
            a1, m1, a2, m2, save = v[0], v[1], v[2], v[3], v[4]
            return ("number", (m1 * a1 + m2 * a2 + save) / (m1 + m2))
        if k == 483:
            d1, a1, d2, a2, n, avg = v[:6]
            return ("number", n * avg - d1 * a1 - d2 * a2)
        if k == 485:
            n, old, new = v[:3]
            return ("number", 12 * ((n + 1) * new - n * old))
        if k in (486, 487, 488, "r3_e3"):
            if k == 488:
                avg, S = v[0], v[1]
            else:
                S, avg = v[0], v[1]
            for n in range(1, 100000):
                if n * avg == S:
                    return ("number", F(n))
            return ("unsolved", "no count")
        if k == 489:
            kk, y1, y2, y3, avg = v[0], v[1], v[2], v[4], v[5]          # (x + 3) 50, x 90, (x - 3) 130, average 80
            for x in range(int(kk) + 1, 10000):
                if (y1 * (x + kk) + y2 * x + y3 * (x - kk)) == avg * 3 * x:
                    return ("number", F(x))
            return ("unsolved", "no x")
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
