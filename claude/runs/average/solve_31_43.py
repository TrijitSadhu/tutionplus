"""Independent solver for Average Rules 31-43, keyed by row id / payload key. Series: the actual list of numbers (or their squares /
cubes) is built and averaged. Misread numbers: a real list with the wrong values in it is fixed and averaged again. Geometric mean:
every whole number is tried until its power gives the product. Overlapping averages: actual values are picked for the shared items
and the unknown one is found by a linear solve. Consecutive numbers: every start is tried until the average fits. Never the rule formula."""
import re
from fractions import Fraction as F

from solve_18_30 import lin, listed, mean, vals

ROWS = {519: 32, 520: 33, 521: 34, 522: 35, 523: 38, 524: 40, 525: 41, 526: 43}


def ints(q):
    return [int(t) for t in re.findall(r"\d+", q)]


def team(n, avg, fixed):
    others = [F(avg) + (i % 3 - 1) * F(i, 4) for i in range(int(n) - len(fixed))]
    others[0] += int(n) * F(avg) - sum(fixed) - sum(others)
    return list(fixed) + others


def fixed_average(n, A, wrong, right):
    xs = team(n, A, [F(w) for w in wrong])
    xs[:len(wrong)] = [F(c) for c in right]
    return mean(xs)


def solve(k, q):
    try:
        r = ROWS[k] if isinstance(k, int) else int(re.match(r"r(\d+)_", k)[1])
        n = max(ints(q))
        if r == 31:
            return ("number", mean([i * i for i in range(1, n + 1)]))
        if r == 32:
            return ("number", mean([i ** 3 for i in range(1, n + 1)]))
        if r == 33:
            return ("number", mean(list(range(2, 2 * n + 1, 2))))
        if r == 34:
            return ("number", mean(list(range(1, 2 * n, 2))))
        if r == 35:
            return ("number", mean([i * i for i in range(2, 2 * n + 1, 2)]))
        if r == 36:
            return ("number", mean([i * i for i in range(2, n + 1, 2)]))
        if r == 37:
            return ("number", mean([i * i for i in range(1, n + 1, 2)]))
        v = vals(q)
        if r == 38:
            if k == "r38_e3":                                   # n, A, three correct, three wrong
                return ("number", fixed_average(v[0], v[1], v[5:8], v[2:5]))
            if k in (523, "r38_e2", "r38_e4"):                  # n, A, correct, wrong
                return ("number", fixed_average(v[0], v[1], [v[3]], [v[2]]))
            return ("number", fixed_average(v[0], v[1], [v[2]], [v[3]]))   # n, A, wrong, correct
        if r == 39:
            xs = ints(q)
            P = 1
            for x in xs:
                P *= x
            hits = [g for g in range(1, 10000) if g ** len(xs) == P]
            assert len(hits) == 1
            return ("number", F(hits[0]))
        if r == 40:
            xs = ints(q)
            return ("number", len(xs) / sum(F(1, x) for x in xs))
        if r == 41:
            return ("number", mean(listed(q)))
        if r == 42:
            if k == "r42_e5":                                   # (H+G)/2 = a, (H+A)/2 = b -> A - G
                a, b = v[:2]
                H = F(50)
                return ("number", (2 * b - H) - (2 * a - H))
            if k == "r42_e6":                                   # four subjects, three shared
                x = v[0]
                shared, phys = [F(60), F(55), F(70)], F(40)
                bio = lin(lambda b: mean(shared + [b]) - mean(shared + [phys]) - x)
                return ("number", bio - phys)
            if k in ("r42_e7", "r42_e8"):                       # Mon-Wed a1, Tue-Thu a2, Thursday
                a1, a2, thu = v[:3]
                tue_wed = 3 * a2 - thu
                return ("number", 3 * a1 - tue_wed)
            if k == "r42_e9":                                   # Mon-Wed a1, Tue-Thu a2, Thu = f Mon
                a1, a2, f = v[:3]
                mon = lin(lambda m: (3 * a1 - m) - (3 * a2 - f * m))     # Tue + Wed from both sides
                return ("number", f * mon)
            x = max(v)                                          # first and second vs second and third (1st, 2nd are read too)
            second, third = F(100), F(40)
            first = lin(lambda a: (a + second) / 2 - (second + third) / 2 - x)
            return ("number", first - third)
        if r == 43:
            cnt, avg = v[:2]
            odd = "odd" in q
            for s in range(1, 1000):
                if (s % 2 == 1) != odd:
                    continue
                xs = [s + 2 * i for i in range(int(cnt))]
                if mean(xs) == avg:
                    return ("number", F(xs[-1] - xs[0]))
            return ("unsolved", "no start")
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
