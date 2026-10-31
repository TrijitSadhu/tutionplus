"""Independent solver for Ratio and Proportion Rules 1-5, keyed by row id / payload key; reads the numbers from the question in order.
Ratios: multiplied out as fractions, roots found by trying every whole number. Proportions: the unknown is found by bisection on the
difference of the two ratios (never by cross-multiplying), then snapped to the exact fraction and checked. Rule of three: worked
in man-days, rupees per kg-km, hectares per ox-day ... (the unit rate), never with the product-of-means formula. Shares: one part
found by a linear solve of the parts adding up to the sum."""
import re
from fractions import Fraction as F


def vals(q):
    out = []
    for a, b, n in re.findall(r"\\frac\{(\d+)\}\{(\d+)\}|(\d+(?:\.\d+)?)", q):
        out.append(F(int(a), int(b)) if a else F(n))
    return out


def ratios(q):
    return [(int(a), int(b)) for a, b in re.findall(r"(\d+)\s*:\s*(\d+)", q)]


def lin(f):
    return -f(F(0)) / (f(F(1)) - f(F(0)))


def red(x, y):
    v = F(x, y)
    return ("ratio", v)


def bisect(f, lo=1e-9, hi=1e7):
    """root of a function that changes sign once on (lo, hi); snapped to the nearest simple fraction and checked exactly."""
    flo = f(lo)
    for _ in range(200):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo = mid
        else:
            hi = mid
    x = F((lo + hi) / 2).limit_denominator(10000)
    assert f(x) == 0, x
    return x


def whole_root(n, k):
    hits = [r for r in range(1, 10000) if r ** k == n]
    assert len(hits) == 1
    return hits[0]


def solve(k, q):
    try:
        v = vals(q)
        r = int(re.match(r"r(\d+)_", k)[1]) if isinstance(k, str) else {708: 2, 709: 3, 710: 3, 711: 4, 712: 4, 713: 5, 714: 5}[k]
        if r == 1:
            rs = ratios(q)
            if "subduplicate" in q:
                return red(whole_root(rs[0][0], 2), whole_root(rs[0][1], 2))
            if "subtriplicate" in q:
                return red(whole_root(rs[0][0], 3), whole_root(rs[0][1], 3))
            if "duplicate" in q:
                return red(rs[0][0] ** 2, rs[0][1] ** 2)
            if "triplicate" in q:
                return red(rs[0][0] ** 3, rs[0][1] ** 3)
            top = bot = 1
            for a, b in rs:
                top, bot = top * a, bot * b
            return red(top, bot)
        if r == 2:
            if "fourth proportional" in q:                      # a : b :: c : x
                a, b, c = v[-3:]
                return ("number", bisect(lambda x: F(a) / F(b) - F(c) / F(x)))
            if "both blanks" in q:                              # a / x = x / d
                a, d = v[:2]
                hits = [x for x in range(1, 10000) if F(a, x) == F(x) / d]
                return ("number", F(hits[0]))
            m = re.search(r"(\S+) : (\S+) (?:::|=) (\S+) : ([^\s.?]+)", q.replace("?", "X").replace(" x ", " X ").replace(" x.", " X."))
            t = [s.rstrip(".") for s in m.groups()]
            i = [j for j, s in enumerate(t) if s in ("X", "x")][0]
            nums = [F(s) if j != i else None for j, s in enumerate(t)]

            def f(x):
                w = [n if n is not None else F(x) for n in nums]
                return w[0] / w[1] - w[2] / w[3]
            return ("number", bisect(f))
        if r == 3:
            if "mean" in q or "x : 63" in q or "true proportion" in q:   # a : x = x : c
                a, c = v[-2:]
                return ("number", bisect(lambda x: F(a) / F(x) - F(x) / F(c)))
            a, b = v[-2:] if k != 709 else (v[-2], v[-1])
            return ("number", bisect(lambda x: F(a) / F(b) - F(b) / F(x)))
        if r == 4:
            if k == 711:
                n1, cost, n2 = v[:3]
                return ("number", cost / n1 * n2)
            if k == 712:
                w1, d1, w2 = v[:3]
                return ("number", w1 * d1 / w2)
            if k == "r4_ex3":
                p, d, after, left = v[:4]
                return ("number", p * (d - after) / (p - left))
            if k == "r4_ex4":
                t1, a1, d1, t2, d2 = v[:5]
                return ("number", a1 / (t1 * d1) * t2 * d2)
            if k == "r4_e1":
                m1, d1, m2 = v[:3]
                return ("number", m1 * d1 * 2 / m2)
            if k == "r4_e2":
                p1, n1, d1, d2, p2 = v[:5]
                money = n1 * d1 * p1
                return ("number", money / (d2 * p2))
            if k == "r4_e3":
                f1, m1, d1, f2, m2 = v[:5]
                per = m1 / (f1 * d1)
                return ("number", m2 / (f2 * per))
            if k == "r4_e4":
                c1, s1, r1, c2, s2 = v[:5]
                return ("number", r1 / (c1 * s1) * c2 * s2)
            if k == "r4_e5":
                c1, f1, d1, f2, c2 = v[:5]
                return ("number", f2 / (c2 * (f1 / (c1 * d1))))
            if k == "r4_e6":
                w1, k1, c1, w2, k2 = v[:5]
                return ("number", c1 / (w1 * k1) * w2 * k2 / 2)
            if k == "r4_e7":
                m1, d1, part, d2 = v[:4]
                return ("number", m1 * d1 * part / d2)
            if k == "r4_e8":
                m1, d1, a1, m2, a2 = v[:5]
                return ("number", a2 / (m2 * (a1 / (m1 * d1))))
            if k == "r4_e9":
                a2, d2, o1, a1, d1 = v[:5]
                return ("number", a2 / (d2 * (a1 / (o1 * d1))))
            if k == "r4_e10":
                m1, d1, h1, times, d2, h2 = v[:6]
                return ("number", m1 * d1 * h1 * times / (d2 * h2))
            if k == "r4_e11":                                   # 40 days, rest 8 h; 3 x as far, 2 x as fast, rest 14 h
                d1, rest1, far, fast, rest2 = v[:5]
                hours = d1 * (24 - rest1) * far / fast
                return ("number", hours / (24 - rest2))
            if k == "r4_e12":
                men, w1, g1, w2, g2 = v[:5]
                food = men * w1 * 7 * g1
                return ("number", men - food / (w2 * 7 * g2))
            if k == "r4_e13":
                d1, absent, d2 = v[:3]
                hits = [x for x in range(int(absent) + 1, 5000) if x * d1 == (x - absent) * d2]
                return ("number", F(hits[0]))
            if k == "r4_e14":
                km1, d1, rest1, km2, rest2, fast = v[:6]
                speed = km1 / (d1 * (24 - rest1))
                return ("number", km2 / (fast * speed) / (24 - rest2))
            if k == "r4_e15":
                t1, t2, e1, e2, d1 = v[:5]
                return ("number", e2 / (t2 * (e1 / (t1 * d1))))
            if k == "r4_e16":
                m1, l1, d1, h1, h2, m2, l2 = v[:7]
                per = l1 / (m1 * d1 * h1)
                return ("number", l2 / (m2 * h2 * per))
        if r == 5:
            (a, b), x = ratios(q)[0], [t for t in v if t not in (F(ratios(q)[0][0]), F(ratios(q)[0][1]))][0]
            part = lin(lambda t: a * t + b * t - x)
            p, s = a * part, b * part
            if "Find the numbers" in q:
                return ("pair", (p, s))
            if "difference" in q or "more" in q:
                return ("number", abs(p - s))
            if "product" in q:
                return ("number", p * s)
            if "women" in q or "town" in q:
                return ("number", s)
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
