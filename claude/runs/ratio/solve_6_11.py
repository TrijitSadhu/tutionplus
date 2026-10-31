"""Independent solver for Ratio and Proportion Rules 6-11, keyed by row id / payload key; reads the numbers from the question in order.
Coins: every count (or set count) is tried until the money adds up. Mixtures: real litres of milk and water are poured and measured.
Numbers in a ratio: the multiplier k is tried 1, 2, 3, ... until the stated difference / sum comes out (then the asked quantity is
read off the actual numbers). Never the rule formula."""
import re
from fractions import Fraction as F
from math import gcd

from solve_1_5 import vals


def two(q):
    return [(int(a), int(b)) for a, b in re.findall(r"(?<![\d:] )(\d+) : (\d+)(?! :)", q)]


def three(q):
    return [tuple(map(int, t)) for t in re.findall(r"(\d+) : (\d+) : (\d+)", q)]


def amount(q):
    """the money in the bag: 'Rs 84', 'Rs 64.75' - not a coin ('Rs 5 coins')."""
    hits = [F(a) for a in re.findall(r"Rs (\d+(?:\.\d+)?)(?! coins)", q)]
    return hits[-1]


def red(x, y):
    return ("ratio", F(x) / F(y))


def try_k(ok, step=F(1), hi=100000):
    for i in range(1, hi):
        k = i * step
        if ok(k):
            return k
    raise ValueError("no k")


COINS = {"r6_e1": ([6, 5, 4], [1, F(1, 2), F(1, 4)]), "r6_e2": ([2, 3, 5], [F(1, 2), F(1, 5), F(1, 10)]), "r6_e4": ([3, 8, 12], [1, F(1, 2), F(1, 4)])}


def solve(k, q):
    try:
        v = vals(q)
        r = int(re.match(r"r(\d+)_", k)[1]) if isinstance(k, str) else {715: 6, 716: 7, 717: 8, 719: 10, 720: 11}[k]
        if r == 6:
            if k in (715, "r6_e5", "r6_e6"):                     # equal numbers
                values = {715: [5, 2, 1], "r6_e5": [1, F(1, 2), F(1, 4)], "r6_e6": [F(1, 2), F(1, 4), F(1, 5), F(1, 20)]}[k]
                total = amount(q)
                return ("number", try_k(lambda n: n * sum(values) == total))
            if k in COINS:                                      # numbers in a ratio, amount given
                counts, values = COINS[k]
                total = amount(q)
                kk = try_k(lambda t: sum(c * t * w for c, w in zip(counts, values)) == total)
                if k == "r6_e1":
                    return ("triple", tuple(c * kk for c in counts))
                return ("number", counts[{"r6_e2": 0, "r6_e4": 1}[k]] * kk)
            vr = three(q)[0]                                     # values in a ratio, coins given
            coins = F(re.search(r"(\d+) coins in all", q)[1])
            per = [F(1), F(1, 2), F(1, 4)]
            u = try_k(lambda t: sum(p * t / w for p, w in zip(vr, per)) == coins, F(1, 4))
            if k == "r6_ex2":
                return ("number", sum(vr) * u)
            return ("number", vr[2] * u / per[2])
        if r == 7:
            w1, m1, w2, m2 = v[:4]
            s1, s2 = m1 / (m1 + w1), m2 / (m2 + w2)
            return red(s1, s2)
        if r == 8:
            (a, b), (c, d) = two(q)[:2]
            Q = F(1000)
            milk = Q * F(a, a + b) + Q * F(c, c + d)
            water = Q * F(b, a + b) + Q * F(d, c + d)
            return red(milk, water)
        if r == 9:
            (w1, m1), (w2, m2), (x, y) = two(q)[:3]
            L1, L2 = F(x * 100), F(y * 100)
            water = L1 * F(w1, w1 + m1) + L2 * F(w2, w2 + m2)
            milk = L1 * F(m1, w1 + m1) + L2 * F(m2, w2 + m2)
            return red(water, milk)
        if r == 10:
            t3 = three(q)
            if t3:                                               # P, Q, R in a ratio; one amount more than another
                parts = t3[0]
                rest = [t for t in v if t not in map(F, parts)]
                diff = rest[0]
                i, j = (0, 2) if "R gets" in q else (0, 1)
                kk = try_k(lambda t: parts[j] * t - parts[i] * t == diff)
                if "for a year" in q:
                    return ("number", parts[1] * kk * 12)
                return ("number", parts[2] * kk)
            (a, b) = two(q)[0]
            diff = [t for t in v if t not in (F(a), F(b))][0]
            kk = try_k(lambda t: abs(b * t - a * t) == diff)
            p, s = a * kk, b * kk
            lo, hi = min(p, s), max(p, s)
            if "Find the numbers" in q:
                return ("pair", (F(p), F(s)))
            if "sum of the numbers" in q:
                return ("number", F(p + s))
            if "remainder" in q:
                return ("number", F(hi % lo))
            if "least number" in q:
                return ("number", F((p * s) % (p + s)))
            if "product" in q:
                return ("number", F(p * s))
            if "price of the cycle" in q:
                return ("number", F(hi))
        if r == 11:
            parts = three(q)[0]
            total = [t for t in v if t not in map(F, parts)][0]
            kk = try_k(lambda t: sum(parts) * t == total, F(1))
            sh = [p * kk for p in parts]
            if "HCF" in q:
                return ("number", F(gcd(*map(int, sh))))
            if "ratio of" in q:
                return red(sh[1] - sh[0], sh[2] - sh[1])
            if "difference" in q:
                return ("number", sh[1] - sh[0])
            return ("number", sh[1] if "Y get" in q else sh[2])
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
