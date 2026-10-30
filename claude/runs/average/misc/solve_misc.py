"""Independent solver for the Average Miscellaneous questions (keys m01-m20); reads the numbers from the question in order and works
with real values: totals day by day, actual trips (x = 7, y = 3 for the algebra ones), a search over the unknown member, the growth
rate tried in steps of 0.1%, ratios shared by trying every whole part. Never the rule formula."""
import os, re, sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solve_18_30 import lin, mean, vals  # noqa: E402

X, Y = F(7), F(3)


def search(ok, lo=1, hi=2000, step=F(1, 10)):
    hits = [lo + i * step for i in range(int((hi - lo) / step) + 1) if ok(lo + i * step)]
    assert len(hits) == 1, hits[:5]
    return hits[0]


def solve(k, q):
    try:
        v = vals(q)
        if k == "m01":                                         # first a days average p, first a+1 days average r
            p, a, r, b = v[:4]                                  # average, days, average, days
            return ("number", b * r - a * p)
        if k == "m02":                                         # x hours at s1, y hours at s2
            s1, s2 = v[:2]
            return ("expr", (s1 * X + s2 * Y) / (X + Y))
        if k == "m03":                                         # x km at s1, y km at s2
            s1, s2 = v[:2]
            return ("expr", (X + Y) / (X / s1 + Y / s2))
        if k == "m04":                                         # four equal sides
            side = F(3600)
            return ("number", 4 * side / sum(side / s for s in v[:4]))
        if k == "m05":                                         # average of three, ratio a : b : c
            avg, a, b, c = v[:4]
            part = search(lambda t: (a + b + c) * t == 3 * avg, 1, 200, F(1))
            return ("number", c * part)
        if k == "m06":                                         # three yearly growths -> one compound rate
            g = (1 + v[0]) * (1 + v[1]) * (1 + v[2])
            r = search(lambda t: (1 + t / 100) ** 3 == g, 0, 100, F(1, 10))
            return ("number", r)
        if k == "m07":                                         # rate on a share, rate on a share, rate on the rest
            r1, f1, r2, f2, r3 = v[:5]
            money = F(6000)
            ret = money * f1 * r1 + money * f2 * r2 + money * (1 - f1 - f2) * r3
            return ("number", ret / money * 100)
        if k == "m08":                                         # first = 2 x second = 4 x third, average a
            a = v[0]
            first = search(lambda t: t + t / 2 + t / 4 == 3 * a, 1, 1000, F(1))
            return ("number", first - first / 4)
        if k == "m09":                                         # 8 readings avg A; 2 avg p; 3 avg q; 6th = 7th - d1 = 8th - d2
            n, A, p, q2, _, d1, _, d2 = v[:8]                   # 'two' and 'three' are words
            c1, c2 = 2, 3
            x = lin(lambda t: c1 * p + c2 * q2 + t + (t + d1) + (t + d2) - n * A)
            return ("number", x)
        if k == "m10":                                         # family of n averaging A, youngest y years old
            n, A, y = v[:3]
            return ("number", (n * A - y - (n - 1) * y) / (n - 1))
        if k == "m11":                                         # couple averaged a at marriage t years ago; now with the child c
            a, t, c = v[:3]
            return ("number", 3 * c - (2 * a + 2 * t))
        if k in ("m12", "m19"):                                # t years ago m people averaged a; with one more now the average is b
            if k == "m12":
                t, m = F(6), F(3)                               # 'Six years ago', P, Q and R
                a, b = v[:2]
            else:
                t, m, a, b = F(3), F(4), v[0], v[1]
            return ("number", (m + 1) * b - (m * a + m * t))
        if k == "m13":                                         # t years ago two averaged a; now three average b; Kiran in s years
            t, a, b, s = F(3), v[0], v[1], v[2]
            return ("number", 3 * b - (2 * a + 2 * t) + s)
        if k == "m14":                                         # N average a; N-3 left average b; X = Y, Z = X + d
            N, a, M, b, d = v[:5]
            return ("number", search(lambda x: 3 * x + d == N * a - M * b, 1, 500, F(1, 2)))
        if k == "m15":                                         # first = 3 x second = third / 2, average a
            a = v[0]
            s = search(lambda t: 3 * t + t + 6 * t == 3 * a, 1, 500, F(1))
            return ("triple", (3 * s, s, 6 * s))
        if k == "m16":                                         # second = 3 x first = 2 x third, average a
            a = v[0]
            f = search(lambda t: t + 3 * t + F(3, 2) * t == 3 * a, 1, 500, F(1))
            return ("number", 3 * f)
        if k == "m17":                                         # sum S, a : b first:second, c : d second:third
            S, a, b, c, d = v[:5]
            second = search(lambda t: t * a / b + t + t * d / c == S, 1, 500, F(1))
            return ("number", second)
        if k == "m18":                                         # P,Q,R avg a1; +S avg a2; T = S + d replaces P, avg a3
            a1, a2, d, a3 = v[:4]
            S = 4 * a2 - 3 * a1
            T = S + d
            QR = 4 * a3 - S - T
            return ("number", 3 * a1 - QR)
        if k == "m20":                                         # K,L avg a; M for K avg b; M for L avg c
            a, b, c = v[:3]
            for K in range(1, 150):
                L = 2 * a - K
                M = 2 * b - L
                if K + M == 2 * c:
                    return ("triple", (F(K), L, M))
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
