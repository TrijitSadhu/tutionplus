"""Independent solver for Ratio and Proportion Rules 12-17, keyed by row id / payload key; reads the numbers from the question in order.
Alloys: real kilograms are melted and weighed; the mixing ratio is found by trying every pair x, y up to 60. Mixtures and alloys:
the part is tried until the whole fits. Joined ratios: the middle number is tried 1, 2, 3 ... (or the quantities are walked along
the chain of fractions); hound and hare: the ground each covers while the hare makes its leaps. Never the rule formula."""
import re
from fractions import Fraction as F
from math import gcd

from solve_1_5 import vals


def pairs(q):
    return [(int(a), int(b)) for a, b in re.findall(r"(\d+) : (\d+)", q)]


def red(x, y):
    return ("ratio", F(x) / F(y))


def lowest(ts):
    g = 0
    for t in ts:
        g = gcd(g, t)
    return tuple(F(t // g) for t in ts)


def solve(k, q):
    try:
        v = vals(q)
        r = int(re.match(r"r(\d+)_", k)[1]) if isinstance(k, str) else {722: 13, 723: 14, 724: 15, 725: 16, 726: 17}[k]
        ps = pairs(q)
        if r == 12:
            (a, b), (c, d) = ps[:2]
            if "per cent" in q:                                 # melted x : y, per cent of the second metal (silver)
                x, y = ps[2]
                silver = x * F(b, a + b) + y * F(d, c + d)
                return ("number", silver / (x + y) * 100)
            if "equal amounts" in q:
                g = 10 * F(a, a + b) + 10 * F(c, c + d)
                return red(g, 20 - g)
            e, f = ps[2]
            hits = [(x, y) for x in range(1, 61) for y in range(1, 61) if gcd(x, y) == 1
                    and (x * F(a, a + b) + y * F(c, c + d)) / (x + y) == F(e, e + f)]
            assert len(hits) == 1
            return red(*hits[0])
        if r == 13:
            x = v[0] if k != "r13_e3" else v[0]
            a, b = ps[0]
            part = next(t for t in (F(i, 4) for i in range(1, 100000)) if (a + b) * t == x)
            milk, water = a * part, b * part
            if k == 722:
                return ("pair", (milk, water))
            return ("number", water if "water is there" in q or "is water" in q else milk)
        if r == 14:
            a, b = ps[0]
            m = re.search(r"(\w+) and (\w+) (?:are )?in the ratio", q)
            first, second = m[1], m[2]
            asked = q[q.rfind(".") + 1:] if "?" in q else q    # the last sentence names the metal asked for
            alloy = F(100)
            metal = alloy * (F(a, a + b) if first in asked else F(b, a + b))
            return ("number", metal / alloy * 100)
        if r == 15:
            (a, b), (c, d) = ps[:2]
            if "Rs" in q:                                       # first person's money given -> third person's
                have = [t for t in v if t not in (a, b, c, d)][0]
                B = have * F(b, a)
                return ("number", B * F(d, c))
            s = v[0]
            for B in range(1, int(s)):
                A, C = F(B * a, b), F(B * d, c)
                if A + B + C == s:
                    break
            if "Find the second" in q or "What is the second" in q:
                return ("number", F(B))
            if "more than the sum" in q:
                return ("number", C - A - B)
            return ("number", A + B)
        if r == 16:
            chain = [F(1)]
            for a, b in ps:
                chain.append(chain[-1] * F(b, a))
            den = 1
            for t in chain:
                den = den * t.denominator // gcd(den, t.denominator)
            ts = [int(t * den) for t in chain]
            if "share" in q:
                total = v[-1]
                who = "PQRST".index(re.search(r"([PQRST])'s share", q)[1])
                return ("number", total * ts[who] / sum(ts))
            return ("terms", lowest(ts))
        if r == 17:
            p, qq, m, n = v[:4]
            hare_leap = F(1)
            hound_leap = n * hare_leap / m
            return red(p * hound_leap, qq * hare_leap)
        return ("unsolved", "unknown key")
    except Exception:
        return ("unsolved", q[:40])
