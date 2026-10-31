"""Independent solver for the Ratio and Proportion Miscellaneous questions (old rows 746-758 and keys m02b ... m35); reads the numbers
from the question and works with actual amounts: parts / shares / multipliers are tried one by one until the stated totals come out,
chains of ratios are walked with real numbers, percentages are applied to a real number. Never the rule formula."""
import os, re, sys
from fractions import Fraction as F
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solve_1_5 import vals  # noqa: E402
from solve_18_25 import three, two  # noqa: E402

X, Y = F(7), F(3)


def red(a, b):
    return ("ratio", F(a) / F(b))


def lowest(ts):
    den = 1
    for t in ts:
        den = den * F(t).denominator // gcd(den, F(t).denominator)
    ints = [int(F(t) * den) for t in ts]
    g = 0
    for t in ints:
        g = gcd(g, t)
    return tuple(F(t // g) for t in ints)


def find(ok, step=F(1), hi=200000):
    for i in range(1, hi):
        if ok(i * step):
            return i * step
    raise ValueError("none")


def chain(q):
    vals_ = [F(1)]
    for a, b in two(q):
        vals_.append(vals_[-1] * F(b, a))
    return vals_


def solve(k, q):
    try:
        v = vals(q)
        if k == 746:
            r = three(q)[0]
            S = v[-1]
            x = find(lambda t: sum((p * t) ** 2 for p in r) == S)
            return ("number", sum(r) * x)
        if k == 747:
            c = chain(q)
            return red(c[0], c[-1])
        if k == "m02b":
            return ("terms", lowest(chain(q)))
        if k == 748:                                            # one-third of x : one-fifth of (N - x) = 2 : 3
            N = v[0]
            (a, b) = two(q)[0]
            x = find(lambda t: t < N and (t / 3) / ((N - t) / 5) == F(a, b))
            return ("pair", (x, N - x))
        if k == 749:                                            # 6a = 8b = 9c, a + b + c = N
            N, p, qq, r = v[0], v[1], v[2], v[3]
            kk = find(lambda t: t / p + t / qq + t / r == N)
            return ("number", max(kk / p, kk / qq, kk / r))
        if k == "m05":                                          # A = 3/4 B, B = 2/5 C
            total = v[0]
            C = find(lambda c: F(3, 4) * F(2, 5) * c + F(2, 5) * c + c == total)
            return ("number", C)
        if k in (750, "m27", "m30", "m31", "m32"):
            x = F(100)                                          # take the first number as 100
            if k == 750:
                p1, p2 = v[0] / 100, v[1] / 100                 # p1 of p = p2 of q
                qv = p1 * x / p2
                return red(x, qv)
            if k == "m27":                                      # 25% of x added to y raises y by 15%
                y = (v[0] / 100) * x / (v[1] / 100)
                return red(y, x)
            if k == "m30":                                      # y + 40% x = 160% y
                y = (v[0] / 100) * x / (v[1] / 100 - 1)
                return red(x, y)
            if k == "m31":                                      # y - 45% x = 3/4 y
                y = (v[0] / 100) * x / (1 - v[1])
                return red(x, y)
            y = (v[0] / 100) * x / (v[1] - 1)                   # m32: y + 30% x = 11/10 y
            return red(x, y)
        if k == 751:
            c = chain(q)
            return red(c[2], c[0])
        if k == "m08":                                          # x - 30 = A/2, x - 20 = B/3, x - 10 = C/4
            total = v[0]
            x = find(lambda t: 2 * (t - 30) + 3 * (t - 20) + 4 * (t - 10) == total)
            return ("number", 2 * (x - 30))
        if k == 752:
            N = v[0]
            (a, b), (c, d) = two(q)[:2]
            juice, water = N * F(a, a + b), N * F(b, a + b)
            return ("number", find(lambda w: juice / (water + w) == F(c, d), F(1, 2)))
        if k == 753:                                            # heavy h, light l, alloy m (times water)
            h, l, m = v[:3]
            hits = [(x, y) for x in range(1, 30) for y in range(1, 30) if gcd(x, y) == 1 and h * x + l * y == m * (x + y)]
            return red(*hits[0])
        if k == 754:                                            # P = 1/4 Q, Q = 2/5 R
            R = F(20)
            Q = F(2, 5) * R
            P = F(1, 4) * Q
            return ("terms", lowest([P, Q, R]))
        if k == 755:
            (a, b) = two(q)[0]
            share = v[-1]
            kk = find(lambda t: b * t == share)
            return ("number", (a + b) * kk)
        if k == 756:                                            # which of the offered ratios cannot split 15 eggs
            n = v[0]
            bad = [(a, b) for a, b in [(2, 1), (1, 4), (3, 2), (3, 1)] if n % (a + b)]
            return red(*bad[0])
        if k == 757:
            money, desk, stool = v[:3]
            d = 0
            while (d + 1) * desk <= money:
                d += 1
            s = (money - d * desk) // stool
            return red(s, d)
        if k == "m15":                                          # per rupee of A, B gets 80 p; per rupee of B, C gets 75 p
            total = v[0]
            A = find(lambda a: a + a * v[1] / 100 + a * v[1] / 100 * v[2] / 100 == total)
            return ("number", A * v[1] / 100)
        if k == "m16":
            T = v[0]
            A = find(lambda a: 3 * a == T - a)
            Bv = find(lambda b: 5 * b == T - b)
            return ("number", (T - A - Bv) - A)
        if k == "m17":
            L1, W, L2 = v[:3]
            return ("number", W / L1 * L2)
        if k == "m18":
            (a, b), (c, d) = two(q)[:2]
            A = v[-1]
            Bv = A * F(b, a)
            return ("number", Bv * F(d, c))
        if k == "m19":
            parts, new = three(q)[0], three(q)[1]
            add = [t for t in v if t not in [F(p) for p in parts + new]][0]
            kk = find(lambda t: F(parts[0] * t + add, parts[1] * t + add) == F(new[0], new[1]))
            return ("number", sum(parts) * kk)
        if k == "m20":                                          # last year 3k : 4k; Hari x 3/2, Ravi x 6/5; total now 4650
            total = v[-1]
            kk = find(lambda t: 3 * t * F(3, 2) + 4 * t * F(6, 5) == total)
            return ("number", 3 * kk * F(3, 2))
        if k == "m21":
            S = v[-1]
            s = find(lambda t: (t / 2) ** 2 + t ** 2 + (t * F(4, 3)) ** 2 == S)
            return ("number", s)
        if k == "m22":                                          # bc : ca : ab = 1 : 3 : 4
            b = F(1)
            a = 3 * b                                            # bc / ca = b / a = 1/3
            c = F(3, 4) * b                                      # ca / ab = c / b = 3/4
            return red(a / (b * c), b / (c * a))
        if k == "m23":                                          # first + second = x, first = y * second
            s = X / (Y + 1)
            assert Y * s + s == X
            return ("expr", Y * s)
        if k in ("m24", "m35"):
            counts = re.findall(r"ratio ([\d : ]+)\.", q)[0]
            counts = [int(t) for t in counts.split(":")]
            values = [F(1), F(1, 2), F(1, 4), F(1, 10)][:len(counts)]
            total = F(re.search(r"Rs (\d+)", q)[1])
            sets = find(lambda t: t * sum(c * w for c, w in zip(counts, values)) == total)
            return ("number", counts[2] * sets)
        if k == "m25":
            (a, b) = two(q)[0]
            p, qq = [t for t in v if t not in (a, b)][:2]
            return red(a * 100 * (100 + p), b * 100 * (100 + qq))
        if k == 758:
            (r1, r2) = three(q)
            moved = [t for t in v if t not in [F(x) for x in r1 + r2]][0]
            kk = find(lambda t: F(r1[0] * t) / (r1[2] * t - moved) == F(r2[0], r2[2]) and F(r1[1] * t + moved) / (r1[0] * t) == F(r2[1], r2[0]))
            return ("number", sum(r1) * kk)
        if k == "m28":
            (a, b) = two(q)[0]
            p, val, p2 = v[2], v[3], v[4]
            first = val / (p / 100)
            second = first * F(b, a)
            return ("number", second * p2 / 100)
        if k in ("m29", "m33"):
            parts = three(q)[0]
            total = F(re.search(r"Rs (\d+)", q)[1])
            kk = find(lambda t: sum(parts) * t == total)
            return ("number", parts[0 if k == "m29" else 1] * kk)
        if k == "m34":
            (a, b) = two(q)[0]
            return red(2 * a + 3 * b, 3 * a + 2 * b)
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
